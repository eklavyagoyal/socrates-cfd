"""Ground-truth labels and benchmark metrics; tables and figures.

    python scripts/analyze_benchmark.py

Inputs: results/baseline/truth.json, benchmark/manifest.yaml, results/benchmark/<system>/<case>.json.
Outputs: benchmark/labels.json, results/benchmark/metrics.json, reports/benchmark_tables.md, reports/figures/*.png

Metrics follow the pre-registered protocol (docs/design.md section 19), per label:
  flawed    -> REJECT = detected, ACCEPT = FALSE ACCEPTANCE, INCONCLUSIVE = missed (safe)
  credible  -> ACCEPT = correct acceptance, REJECT = false rejection, INCONCLUSIVE = undecided
  ambiguous -> reported separately (no verdict is wrong; INCONCLUSIVE was the pre-registered expectation)
ERROR results (infrastructure/LLM failures) are counted separately, never as INCONCLUSIVE.
Every (system, case) pair must have a current result; missing or stale ones are listed.
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
from socrates.orchestration.systems import is_infrastructure_error  # noqa: E402
from socrates.orchestration.truth import label_case  # noqa: E402

SYSTEMS = ["A", "B", "L-judge", "C-rule", "C-llm", "Bexh"]
NAMES = {"A": "A: OpenFOAM diagnostics", "B": "B: static verifier", "L-judge": "L: LLM judge (evidence only)",
         "C-rule": "C-rule: adaptive, rule planner", "C-llm": "C: adaptive, LLM critic",
         "Bexh": "B+exh: fixed exhaustive protocol"}
STATUS_COLORS = {"correct": "#0ca30c", "false_accept": "#d03b3b", "false_reject": "#ec835a",
                 "undecided": "#d9d8d4", "error": "#8a8986", "missing": "#ffffff"}


def setup_problems(ev: dict) -> list[str]:
    conf = ev.get("configuration") or {}
    out = []
    if conf.get("configured_reynolds") and abs(conf["configured_reynolds"] - conf["spec_reynolds"]) / conf["spec_reynolds"] > 1e-3:
        out.append(f"solves Re={conf['configured_reynolds']:.4g} instead of {conf['spec_reynolds']:.4g}")
    if conf.get("solver") == "simpleFoam":
        out.append("steady formulation of a periodic flow")
    return out  # pre-registered: wrong Re or wrong regime only; everything else is judged by its error


def outcome(label: str, verdict: str) -> str:
    if verdict in (None, "ERROR"):
        return "error"
    if label == "flawed":
        return {"REJECT": "correct", "ACCEPT": "false_accept"}.get(verdict, "undecided")
    if label == "credible":
        return {"ACCEPT": "correct", "REJECT": "false_reject"}.get(verdict, "undecided")
    return {"ACCEPT": "correct", "REJECT": "correct"}.get(verdict, "undecided")


def variance_table(bench: Path, cases: list[str], labels: dict) -> list[str]:
    """Independent repeats of C-llm (C-llm-r2, C-llm-r3, ...): verdict and experiment-sequence agreement."""
    reps = ["C-llm"] + sorted(d.name for d in bench.glob("C-llm-r*") if d.is_dir())
    if len(reps) < 2:
        return []
    out = ["", "### LLM run-to-run variance (independent repeats of C-llm)", "",
           "| case | label | " + " | ".join(reps) + " | same verdict | same experiment sequence |",
           "|---|---|" + "---|" * len(reps) + "---|---|"]
    n_same_v = n_same_seq = n = 0
    for cid in cases:
        rows = []
        for s in reps:
            f = bench / s / f"{cid}.json"
            r = json.loads(f.read_text()) if f.exists() else None
            if r is None or is_infrastructure_error(r):
                rows.append(None)
                continue
            seq = tuple((e["action"], json.dumps(e.get("params") or e.get("parameters") or {}, sort_keys=True))
                        for e in (r.get("experiments") or []) if e.get("run_id"))
            rows.append((r.get("final_verdict") or r.get("verdict"), seq))
        if any(x is None for x in rows):
            out.append(f"| {cid} | {labels[cid]['label']} | " + " | ".join("—" if x is None else x[0] for x in rows)
                       + " | incomplete | incomplete |")
            continue
        n += 1
        sv = len({x[0] for x in rows}) == 1
        ss = len({x[1] for x in rows}) == 1
        n_same_v += sv
        n_same_seq += ss
        cell = [f"{v} ({' → '.join(a[0].split('_')[0] for a in q) or 'none'})" for v, q in rows]
        out.append(f"| {cid} | {labels[cid]['label']} | " + " | ".join(cell) + f" | {'yes' if sv else '**no**'} | "
                   f"{'yes' if ss else 'no'} |")
    out += ["", f"Complete repeat sets: {n}; identical verdict in {n_same_v}/{n}; identical experiment sequence in "
                f"{n_same_seq}/{n}."]
    return out


def _rate(num: int, den: int):
    return None if den == 0 else num / den


def main() -> None:
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = ProblemSpec.from_yaml(REPO / man["problem_spec"])
    truth = json.loads((REPO / "results" / "baseline" / "truth.json").read_text())["truth"]
    T = {q: truth[q]["value"] for q in spec.requested_outputs}
    uT = {q: truth[q]["uncertainty_rel"] for q in spec.requested_outputs}
    store = RunStore(REPO / "results" / "runs")
    bench = REPO / "results" / "benchmark"

    labels, problems = {}, []
    for case in man["cases"]:
        roots = set()
        for s in SYSTEMS:
            f = bench / s / f"{case['id']}.json"
            if f.exists():
                rr = json.loads(f.read_text()).get("root_run")
                if rr:
                    roots.add(rr)
        if len(roots) != 1:
            labels[case["id"]] = {"label": "unrun", "intended": case["intended"]}
            problems.append(f"{case['id']}: " + ("no result with a root run" if not roots
                                                 else f"results disagree on the root run {sorted(roots)}"))
            continue
        root = roots.pop()
        ev = store.load(root).evidence or {}
        rep = (ev.get("qoi") or {}).get("reported") or {}
        lab = label_case(rep, T, spec.verification.requested_tolerance, setup_problems(ev), truth_uncertainty=uT)
        lab.update(intended=case["intended"], expected=case["expected_expert_judgement"], root_run=root,
                   reported={q: rep.get(q) for q in spec.requested_outputs},
                   revealing_experiment=case.get("revealing_experiment"))
        labels[case["id"]] = lab
    (REPO / "benchmark" / "labels.json").write_text(json.dumps(
        {"truth": T, "truth_uncertainty_rel": uT, "rule": man["tolerance_rule"], "cases": labels}, indent=1))
    cases = [c for c, v in labels.items() if v["label"] != "unrun"]

    metrics, matrix = {}, {}
    for s in SYSTEMS:
        if not (bench / s).exists():
            continue
        per_case, n_exp, rel_cost, wall, llm_cost, viol, untraced = {}, [], [], [], 0.0, 0, 0
        hit = miss = 0
        for cid in cases:
            f = bench / s / f"{cid}.json"
            if not f.exists():
                problems.append(f"{s}/{cid}: missing")
                matrix[(s, cid)] = ("—", "missing")
                continue
            r = json.loads(f.read_text())
            if r.get("root_run") and r["root_run"] != labels[cid]["root_run"]:
                problems.append(f"{s}/{cid}: stale (root {r['root_run']} != {labels[cid]['root_run']})")
            v = "ERROR" if is_infrastructure_error(r) else (r.get("final_verdict") or r.get("verdict"))
            lab = labels[cid]["label"]
            o = outcome(lab, v)
            matrix[(s, cid)] = (v, o)
            per_case[cid] = {"verdict": v, "label": lab, "outcome": o}
            exps = [e for e in (r.get("experiments") or []) if e.get("run_id")]
            if s in ("C-rule", "C-llm", "Bexh"):
                n_exp.append(len(exps))
                root_cs = ((store.load(labels[cid]["root_run"]).evidence or {}).get("cost") or {}).get("cell_steps") or 1
                cs = sum((((store.load(e["run_id"]).evidence or {}).get("cost") or {}).get("cell_steps") or 0) for e in exps)
                rel_cost.append(cs / root_cs)
                wall.append(sum(((store.load(e["run_id"]).provenance or {}).get("wall_seconds") or 0) for e in exps))
            if s in ("C-rule", "C-llm"):
                llm_cost += (r.get("cost") or {}).get("planner_cost_usd") or 0.0
                viol += len(r.get("authority_violations") or [])
                for h in r.get("history") or []:
                    untraced += ((h.get("meta") or {}).get("numeric_audit") or {}).get("n_untraced", 0)
                    untraced += ((h.get("review") or {}).get("numeric_audit") or {}).get("n_untraced", 0)
                rev = labels[cid].get("revealing_experiment")
                if lab == "flawed" and rev:
                    if exps and exps[0]["action"] == rev:
                        hit += 1
                    elif exps or v != "REJECT":
                        miss += 1  # wrong first experiment, or no experiment and not rejected
            if s == "L-judge":
                llm_cost += r.get("cost_usd") or 0.0
                untraced += (r.get("numeric_audit") or {}).get("n_untraced", 0)

        decided = [c for c in per_case.values() if c["outcome"] != "error"]  # rate denominators exclude errors

        def count(label, verdicts):
            return sum(1 for c in decided if c["label"] == label and c["verdict"] in verdicts)

        nf = sum(1 for c in decided if c["label"] == "flawed")
        nc = sum(1 for c in decided if c["label"] == "credible")
        na = sum(1 for c in decided if c["label"] == "ambiguous")
        n_err = len(per_case) - len(decided)
        errors_by_label = {lb: sum(1 for c in per_case.values() if c["outcome"] == "error" and c["label"] == lb)
                           for lb in ("flawed", "credible", "ambiguous")}
        metrics[s] = {"cases": per_case, "summary": {
            "n": len(per_case), "n_flawed": nf, "n_credible": nc, "n_ambiguous": na, "n_error": n_err,
            "errors_by_label": errors_by_label,
            "false_acceptance_rate": _rate(count("flawed", {"ACCEPT"}), nf),
            "detection_rate": _rate(count("flawed", {"REJECT"}), nf),
            "missed_but_safe_rate": _rate(count("flawed", {"INCONCLUSIVE"}), nf),
            "correct_acceptance_rate": _rate(count("credible", {"ACCEPT"}), nc),
            "false_rejection_rate": _rate(count("credible", {"REJECT"}), nc),
            "inconclusive_rate": _rate(sum(1 for c in decided if c["verdict"] == "INCONCLUSIVE"), len(decided)),
            "ambiguous_verdicts": {v: count("ambiguous", {v}) for v in ("ACCEPT", "REJECT", "INCONCLUSIVE")},
            "mean_experiments": (sum(n_exp) / len(n_exp)) if n_exp else 0.0,
            "total_experiments": sum(n_exp),
            "mean_compute_relative_to_root": (sum(rel_cost) / len(rel_cost)) if rel_cost else 0.0,
            "total_experiment_wall_hours": sum(wall) / 3600.0,
            "llm_cost_usd": llm_cost,
            "authority_violations": viol,
            "untraced_numbers": untraced,
            "first_experiment_targets_flaw": f"{hit}/{hit + miss}" if (hit + miss) else None,
        }}
    (bench / "metrics.json").write_text(json.dumps({"problems": problems, "metrics": metrics}, indent=1))
    systems = [s for s in SYSTEMS if s in metrics]

    # ---------------- tables ----------------
    L = []
    if problems:
        L += ["**Incomplete or stale results (excluded from nothing; listed for transparency):** " + "; ".join(problems), ""]
    L += ["| case | label | max err / τ | unstable | " + " | ".join(systems) + " |",
          "|---|---|---|---|" + "---|" * len(systems)]
    for cid in cases:
        lab = labels[cid]
        cells = []
        for s in systems:
            v, o = matrix.get((s, cid), ("—", "missing"))
            mark = {"correct": "✓", "false_accept": "✗✗", "false_reject": "✗", "undecided": "·", "error": "E", "missing": "?"}[o]
            cells.append(f"{v} {mark}")
        L.append(f"| {cid} | {lab['label']} | {lab['max_error_over_tolerance']:.2f} | "
                 f"{','.join(lab['label_unstable']) or ''} | " + " | ".join(cells) + " |")
    L += ["", "✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · E error · ? missing",
          ""]
    keys = [("n", "cases"), ("n_flawed", "flawed cases (decided)"), ("n_credible", "credible cases (decided)"),
            ("n_ambiguous", "ambiguous cases (decided)"),
            ("false_acceptance_rate", "**false acceptance** (flawed → ACCEPT)"), ("detection_rate", "detection (flawed → REJECT)"),
            ("missed_but_safe_rate", "missed but safe (flawed → INCONCLUSIVE)"),
            ("correct_acceptance_rate", "correct acceptance (credible → ACCEPT)"),
            ("false_rejection_rate", "false rejection (credible → REJECT)"), ("inconclusive_rate", "inconclusive (all decided)"),
            ("ambiguous_verdicts", "ambiguous cases: verdicts"), ("n_error", "errors (excluded from rates)"),
            ("errors_by_label", "errors by label"),
            ("mean_experiments", "mean extra simulations / case"), ("mean_compute_relative_to_root", "mean extra compute / case (× root)"),
            ("total_experiment_wall_hours", "total experiment wall time (h)"), ("llm_cost_usd", "LLM cost (USD)"),
            ("authority_violations", "authority violations"), ("untraced_numbers", "untraceable numbers in LLM text"),
            ("first_experiment_targets_flaw", "first experiment targets the flaw")]
    L += ["| metric | " + " | ".join(systems) + " |", "|---|" + "---|" * len(systems)]
    for k, name in keys:
        vals = []
        for s in systems:
            x = metrics[s]["summary"].get(k)
            if isinstance(x, dict):
                vals.append(" ".join(f"{a[:3]}:{b}" for a, b in x.items()))
            else:
                vals.append("—" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x)))
        L.append(f"| {name} | " + " | ".join(vals) + " |")
    L += variance_table(bench, cases, labels)
    (REPO / "reports" / "benchmark_tables.md").write_text("\n".join(L) + "\n")

    # ---------------- figures ----------------
    figdir = REPO / "reports" / "figures"
    figdir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(1.55 * len(systems) + 3.4, 0.42 * len(cases) + 1.5))
    for i, cid in enumerate(cases):
        for j, s in enumerate(systems):
            v, o = matrix.get((s, cid), ("", "missing"))
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=STATUS_COLORS[o], lw=0))
            ax.text(j + 0.5, i + 0.5, {"INCONCLUSIVE": "INCONCL."}.get(v, v), ha="center", va="center", fontsize=7.5,
                    color="#0b0b0b")
    ax.set_xlim(0, len(systems))
    ax.set_ylim(len(cases), 0)
    ax.set_xticks([j + 0.5 for j in range(len(systems))])
    ax.set_xticklabels([NAMES[s].split(":")[0] for s in systems], fontsize=8)
    ax.set_yticks([i + 0.5 for i in range(len(cases))])
    ax.set_yticklabels([f"{c}  [{labels[c]['label']}]" for c in cases], fontsize=7.5)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    keys_l = ["correct", "false_accept", "false_reject", "undecided", "error"]
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=STATUS_COLORS[k]) for k in keys_l],
              ["correct", "false acceptance (dangerous)", "false rejection", "inconclusive", "error"],
              loc="upper center", bbox_to_anchor=(0.5, -0.03), ncol=5, fontsize=7.5, frameon=False)
    ax.set_title("Verdict per case and system (text = verdict; colour = outcome vs ground-truth label)", fontsize=9)
    fig.tight_layout()
    fig.savefig(figdir / "verdict_matrix.png", dpi=160)
    plt.close(fig)

    panels = [("false_acceptance_rate", "False acceptance\n(flawed → ACCEPT)"), ("detection_rate", "Detection\n(flawed → REJECT)"),
              ("correct_acceptance_rate", "Correct acceptance\n(credible → ACCEPT)"),
              ("false_rejection_rate", "False rejection\n(credible → REJECT)")]
    fig, axs = plt.subplots(1, 4, figsize=(11.5, 0.42 * len(systems) + 1.6), sharey=True)
    for ax, (k, title) in zip(axs, panels):
        vals = [metrics[s]["summary"].get(k) for s in systems]
        ys = list(range(len(systems)))
        ax.barh(ys, [0 if v is None else v for v in vals], height=0.6, color="#2a78d6")
        for y, v in zip(ys, vals):
            ax.text((v or 0) + 0.02, y, "n/a" if v is None else f"{v:.2f}", va="center", fontsize=7.5, color="#52514e")
        ax.set_xlim(0, 1.15)
        ax.set_title(title, fontsize=8.5)
        ax.grid(axis="x", color="#e7e6e2", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axs[0].set_yticks(range(len(systems)))
    axs[0].set_yticklabels([f"{NAMES[s]} (n={metrics[s]['summary']['n']})" for s in systems], fontsize=7.5)
    axs[0].invert_yaxis()
    fig.suptitle("Pre-registered rates per system", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(figdir / "rates.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for s in systems:
        sm = metrics[s]["summary"]
        if sm["detection_rate"] is None:
            continue
        x, y = sm["mean_compute_relative_to_root"], sm["detection_rate"]
        ax.plot([x], [y], "o", ms=8, color="#2a78d6")
        fa = sm["false_acceptance_rate"]
        ax.annotate(f"{NAMES[s].split(':')[0]} (false acc. {fa:.2f})" if fa is not None else NAMES[s].split(":")[0],
                    (x, y), textcoords="offset points", xytext=(7, 4), fontsize=7.5, color="#52514e")
    ax.set_xlabel("mean extra compute per case (cell-steps / root run)", fontsize=8.5)
    ax.set_ylabel("detection rate on flawed cases", fontsize=8.5)
    ax.set_ylim(-0.03, 1.05)
    ax.grid(color="#e7e6e2", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Detection vs extra simulation cost", fontsize=9)
    fig.tight_layout()
    fig.savefig(figdir / "cost_vs_detection.png", dpi=160)
    plt.close(fig)
    print(json.dumps({"problems": problems, **{s: metrics[s]["summary"] for s in systems}}, indent=1, default=str))


if __name__ == "__main__":
    main()
