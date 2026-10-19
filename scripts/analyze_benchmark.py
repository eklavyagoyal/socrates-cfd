"""Compute ground-truth labels and benchmark metrics; write tables and figures.

    python scripts/analyze_benchmark.py

Inputs: results/baseline/truth.json (scripts/make_baseline_report.py),
benchmark/manifest.yaml, results/benchmark/<system>/<case>.json.
Outputs: benchmark/labels.json, results/benchmark/metrics.json,
reports/figures/*.png, reports/benchmark_tables.md (included by the report).
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.truth import label_case  # noqa: E402

SYSTEMS = ["A", "B", "L-judge", "C-rule", "C-llm", "Bexh"]
SYSTEM_NAMES = {
    "A": "A: OpenFOAM diagnostics",
    "B": "B: static verifier",
    "L-judge": "L: LLM judge, no experiments",
    "C-rule": "C-rule: adaptive, rule planner",
    "C-llm": "C: adaptive, LLM critic",
    "Bexh": "B+exh: fixed exhaustive protocol",
}
# status palette (reserved meanings): correct / dangerous / conservative / undecided
COLORS = {"correct": "#0ca30c", "false_accept": "#d03b3b", "false_reject": "#ec835a", "undecided": "#d9d8d4",
          "missing": "#ffffff"}


def setup_problems(ev: dict) -> list[str]:
    conf = ev.get("configuration") or {}
    out = []
    if conf.get("configured_reynolds") and abs(conf["configured_reynolds"] - conf["spec_reynolds"]) / conf["spec_reynolds"] > 1e-3:
        out.append(f"solves Re={conf['configured_reynolds']:.4g} instead of {conf['spec_reynolds']:.4g}")
    if conf.get("solver") == "simpleFoam":
        out.append("steady formulation of a periodic flow")
    return out


def outcome(label: str, verdict: str) -> str:
    v = {"INCONCLUSIVE": "INCONCLUSIVE", "ERROR": "INCONCLUSIVE"}.get(verdict, verdict)
    if label == "flawed":
        return {"REJECT": "correct", "ACCEPT": "false_accept"}.get(v, "undecided")
    if label == "credible":
        return {"ACCEPT": "correct", "REJECT": "false_reject"}.get(v, "undecided")
    # ambiguous: no verdict is wrong; ACCEPT/REJECT both defensible
    return {"ACCEPT": "correct", "REJECT": "correct"}.get(v, "undecided")


def main() -> None:
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = ProblemSpec.from_yaml(REPO / man["problem_spec"])
    truth = json.loads((REPO / "results" / "baseline" / "truth.json").read_text())
    T = {q: truth["truth"][q]["value"] for q in spec.requested_outputs}
    store = RunStore(REPO / "results" / "runs")
    bench = REPO / "results" / "benchmark"

    labels, rows = {}, []
    for case in man["cases"]:
        f = bench / "B" / f"{case['id']}.json"
        if not f.exists():
            continue
        root = json.loads(f.read_text())["root_run"]
        ev = store.load(root).evidence or {}
        rep = (ev.get("qoi") or {}).get("reported") or {}
        lab = label_case(rep, T, spec.verification.requested_tolerance, setup_problems(ev))
        lab.update(intended=case["intended"], expected=case["expected_expert_judgement"], root_run=root,
                   reported={q: rep.get(q) for q in spec.requested_outputs},
                   revealing_experiment=case.get("revealing_experiment"))
        labels[case["id"]] = lab
    (REPO / "benchmark" / "labels.json").write_text(json.dumps({"truth": T, "rule": man["tolerance_rule"], "cases": labels}, indent=1))

    metrics = {}
    matrix = {}
    for s in SYSTEMS:
        res = {}
        for cid in labels:
            f = bench / s / f"{cid}.json"
            if f.exists():
                res[cid] = json.loads(f.read_text())
        if not res:
            continue
        m = {"n": len(res), "by_label": {}, "cases": {}}
        n_exp, cell_steps, wall, llm_cost, viol, untraced, first_ok, first_n = [], [], [], 0.0, 0, 0, 0, 0
        for cid, r in res.items():
            v = r.get("final_verdict") or r.get("verdict")
            lab = labels[cid]["label"]
            o = outcome(lab, v)
            matrix[(s, cid)] = (v, o)
            m["cases"][cid] = {"verdict": v, "label": lab, "outcome": o}
            m["by_label"].setdefault(lab, {}).setdefault(v, 0)
            m["by_label"][lab][v] += 1
            exps = r.get("experiments") or []
            if s in ("C-rule", "C-llm"):
                n_exp.append(len(exps))
                cell_steps.append((r.get("cost") or {}).get("relative_to_root") or 0.0)
                wall.append((r.get("cost") or {}).get("experiment_wall_seconds") or 0.0)
                llm_cost += (r.get("cost") or {}).get("planner_cost_usd") or 0.0
                viol += len(r.get("authority_violations") or [])
                for h in r.get("history") or []:
                    untraced += ((h.get("meta") or {}).get("numeric_audit") or {}).get("n_untraced", 0)
                rev = labels[cid].get("revealing_experiment")
                executed = [e for e in exps if e.get("run_id")]
                if lab == "flawed" and rev and executed:
                    first_n += 1
                    first_ok += executed[0]["action"] == rev
            elif s == "Bexh":
                done = [e for e in exps if e.get("run_id")]
                n_exp.append(len(done))
                root_cs = ((store.load(r["root_run"]).evidence or {}).get("cost") or {}).get("cell_steps") or 1
                cell_steps.append(sum((e.get("cell_steps") or 0) for e in done) / root_cs)
                wall.append(sum((e.get("wall_seconds") or 0) for e in done))
            elif s == "L-judge":
                llm_cost += r.get("cost_usd") or 0.0
                untraced += (r.get("numeric_audit") or {}).get("n_untraced", 0)

        def rate(lab, verdict):
            d = m["by_label"].get(lab, {})
            n = sum(d.values())
            return (d.get(verdict, 0) / n) if n else None

        n_flawed = sum(m["by_label"].get("flawed", {}).values())
        n_cred = sum(m["by_label"].get("credible", {}).values())
        m["summary"] = {
            "n_flawed": n_flawed, "n_credible": n_cred,
            "n_ambiguous": sum(m["by_label"].get("ambiguous", {}).values()),
            "detection_rate": rate("flawed", "REJECT"),
            "false_acceptance_rate": rate("flawed", "ACCEPT"),
            "correct_acceptance_rate": rate("credible", "ACCEPT"),
            "false_rejection_rate": rate("credible", "REJECT"),
            "inconclusive_rate": sum(1 for c in m["cases"].values() if c["verdict"] in ("INCONCLUSIVE", "ERROR")) / len(res),
            "correct_decisions": sum(1 for c in m["cases"].values() if c["outcome"] == "correct"),
            "mean_experiments": (sum(n_exp) / len(n_exp)) if n_exp else 0.0,
            "total_experiments": sum(n_exp),
            "mean_compute_relative_to_root": (sum(cell_steps) / len(cell_steps)) if cell_steps else 0.0,
            "total_experiment_wall_hours": sum(wall) / 3600.0,
            "llm_cost_usd": llm_cost,
            "authority_violations": viol,
            "untraced_numbers": untraced,
            "first_experiment_targets_flaw": f"{first_ok}/{first_n}" if first_n else None,
        }
        metrics[s] = m
    (bench / "metrics.json").write_text(json.dumps(metrics, indent=1))

    # ---------------- tables ----------------
    lines = ["| case | label | max err/τ | " + " | ".join(s for s in SYSTEMS if s in metrics) + " |",
             "|---|---|---|" + "---|" * len([s for s in SYSTEMS if s in metrics])]
    for cid, lab in labels.items():
        cells = []
        for s in SYSTEMS:
            if s not in metrics:
                continue
            v, o = matrix.get((s, cid), ("—", "missing"))
            mark = {"correct": "✓", "false_accept": "✗✗", "false_reject": "✗", "undecided": "·", "missing": ""}[o]
            cells.append(f"{v} {mark}")
        lines.append(f"| {cid} | {lab['label']} | {lab['max_error_over_tolerance']:.2f} | " + " | ".join(cells) + " |")
    lines += ["", "✓ correct · ✗✗ false acceptance · ✗ false rejection · `·` undecided (INCONCLUSIVE)", ""]
    keys = ["detection_rate", "false_acceptance_rate", "correct_acceptance_rate", "false_rejection_rate",
            "inconclusive_rate", "correct_decisions", "mean_experiments", "mean_compute_relative_to_root",
            "total_experiment_wall_hours", "llm_cost_usd", "authority_violations", "untraced_numbers",
            "first_experiment_targets_flaw"]
    lines += ["| metric | " + " | ".join(s for s in SYSTEMS if s in metrics) + " |",
              "|---|" + "---|" * len([s for s in SYSTEMS if s in metrics])]
    for k in keys:
        vals = []
        for s in SYSTEMS:
            if s not in metrics:
                continue
            x = metrics[s]["summary"].get(k)
            vals.append("—" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x)))
        lines.append(f"| {k} | " + " | ".join(vals) + " |")
    (REPO / "reports" / "benchmark_tables.md").write_text("\n".join(lines) + "\n")

    # ---------------- figures ----------------
    figdir = REPO / "reports" / "figures"
    figdir.mkdir(parents=True, exist_ok=True)
    systems = [s for s in SYSTEMS if s in metrics]
    cases = list(labels)
    fig, ax = plt.subplots(figsize=(1.6 * len(systems) + 3.2, 0.42 * len(cases) + 1.4))
    for i, cid in enumerate(cases):
        for j, s in enumerate(systems):
            v, o = matrix.get((s, cid), ("", "missing"))
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=COLORS[o], lw=0))
            ax.text(j + 0.5, i + 0.5, {"INCONCLUSIVE": "INCONCL.", "ERROR": "ERROR"}.get(v, v), ha="center", va="center",
                    fontsize=7.5, color="#0b0b0b")
    ax.set_xlim(0, len(systems))
    ax.set_ylim(len(cases), 0)
    ax.set_xticks([j + 0.5 for j in range(len(systems))])
    ax.set_xticklabels([SYSTEM_NAMES[s].split(":")[0] for s in systems], fontsize=8)
    ax.set_yticks([i + 0.5 for i in range(len(cases))])
    ax.set_yticklabels([f"{c}  [{labels[c]['label']}]" for c in cases], fontsize=7.5)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[k]) for k in ("correct", "false_accept", "false_reject", "undecided")]
    ax.legend(handles, ["correct", "false acceptance (dangerous)", "false rejection", "inconclusive"],
              loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=4, fontsize=7.5, frameon=False)
    ax.set_title("Verdict per case and system (cell text = verdict; colour = correctness vs ground truth)", fontsize=9)
    fig.tight_layout()
    fig.savefig(figdir / "verdict_matrix.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for s in systems:
        sm = metrics[s]["summary"]
        x, y = sm["mean_compute_relative_to_root"], sm["correct_decisions"] / metrics[s]["n"]
        ax.plot([x], [y], "o", ms=8, color="#2a78d6")
        ax.annotate(SYSTEM_NAMES[s], (x, y), textcoords="offset points", xytext=(7, 4), fontsize=7.5, color="#52514e")
    ax.set_xlabel("mean extra compute per case (cell-steps / root run)", fontsize=8.5)
    ax.set_ylabel("fraction of cases decided correctly", fontsize=8.5)
    ax.set_ylim(-0.03, 1.05)
    ax.grid(color="#e7e6e2", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Correct decisions vs extra simulation cost", fontsize=9)
    fig.tight_layout()
    fig.savefig(figdir / "cost_vs_correct.png", dpi=160)
    plt.close(fig)
    print(json.dumps({s: metrics[s]["summary"] for s in metrics}, indent=1))


if __name__ == "__main__":
    main()
