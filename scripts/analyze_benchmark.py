"""Ground-truth labels and benchmark metrics; tables and figures.

    python scripts/analyze_benchmark.py

Inputs: results/baseline/truth.json, benchmark/manifest.yaml, results/benchmark/<system>/<case>.json.
Outputs: benchmark/labels.json, results/benchmark/metrics.json, reports/benchmark_tables.md, reports/figures/*.png

Metrics follow the pre-registered protocol (docs/design.md section 19), per label:
  flawed    -> REJECT = detected, ACCEPT = FALSE ACCEPTANCE, INCONCLUSIVE = missed (safe)
  credible  -> ACCEPT = correct acceptance, REJECT = false rejection, INCONCLUSIVE = undecided
  ambiguous -> reported separately with neutral outcome classes (no verdict is scored right or wrong;
               INCONCLUSIVE was the pre-registered expectation)
ERROR results (infrastructure/LLM failures) are counted separately, never as INCONCLUSIVE.
The root run of each case is the content-addressed run of its manifest definition (independent of any result
file).  Every (system, case) pair must have a current result: missing ones, and stale ones (other decision code,
another root, or evidence changed since), are listed and NOT counted in that system's rates.
Compute per system is the cost of the experiments it requested, as if it had run them alone (the shared run
store means the machine ran each distinct experiment once).

Further sections (after the benchmark tables): the attack cases (results/attacks/) labelled against the same
reference under both readings of the section-19 set-up clause; per-quantity verdict accuracy; the criterion-5b
decision rule of docs/methodology.md; calibration rows for the attack cases.  Attack results carry no
decision-code stamp: their replay status is read from results/analysis/replay.json (scripts/replay_verdicts.py).
"""

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.orchestration.evaluation import current_root, is_infrastructure_error, staleness  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.systems import decision_code_fingerprint  # noqa: E402
from socrates.orchestration.truth import label_case  # noqa: E402

SYSTEMS = ["A", "B", "L-judge", "C-rule", "C-llm", "Bexh"]
NAMES = {"A": "A: OpenFOAM diagnostics", "B": "B: static verifier", "L-judge": "L: LLM judge (evidence only)",
         "C-rule": "C-rule: adaptive, rule planner", "C-llm": "C: adaptive, LLM critic",
         "Bexh": "B+exh: fixed exhaustive protocol"}
STATUS_COLORS = {"correct": "#0ca30c", "false_accept": "#d03b3b", "false_reject": "#ec835a",
                 "undecided": "#d9d8d4", "error": "#8a8986", "missing": "#ffffff", "stale": "#ffffff",
                 "ambiguous_accept": "#9cc3ee", "ambiguous_reject": "#c9b8ea", "ambiguous_inconclusive": "#e8eef7"}
MARKS = {"correct": "✓", "false_accept": "✗✗", "false_reject": "✗", "undecided": "·", "error": "E", "missing": "?",
         "stale": "S", "ambiguous_accept": "~", "ambiguous_reject": "~", "ambiguous_inconclusive": "~·"}
ATT_SYSTEMS = ["B-v1", "L-judge", "C-rule-v1", "C-llm-v1", "C-llm-v1+review", "B-v2", "C-rule-v2"]  # make_reports order
# Attacks that change the problem itself, not its numerics (cases/attacks/<id>.yaml 'flaw').  They decide the label
# only under the set-up reading of the section-19 clause; X3 changes mesh and domain size only and is judged by its
# error (same list as scripts/posthoc_acceptance_rule.py).
ATTACK_SETUP_DEPARTURES = {
    "X1_cylinder_geometry": ["meshed cylinder diameter 1.05 D while Re, force reference and St assume D"],
    "X2_inlet_shear": ["sheared inlet profile; the problem specifies a uniform stream"],
}
SETUP_CLAUSE = "if the set-up answers a different problem (wrong Re or regime)"  # docs/design.md section 19, verbatim
SHORT = {"mean_drag_coefficient": "Cd", "strouhal_number": "St"}
READINGS = [("label_setup_reading", "set-up reading"), ("label_point_estimate", "strict reading, point estimates"),
            ("label", "strict reading, with mitigation")]


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
    return {"ACCEPT": "ambiguous_accept", "REJECT": "ambiguous_reject"}.get(verdict, "ambiguous_inconclusive")


def variance_table(bench: Path, cases: list[str], labels: dict, store: RunStore, fp: str, problems: list) -> list[str]:
    """Independent repeats of C-llm (C-llm-r2, C-llm-r3, ...): verdict and experiment-sequence agreement.

    Experiment run ids are content-addressed (config + initialisation incl. parent), so identical run-id
    sequences mean identical experiments on identical parents."""
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
            if r is not None:
                why = staleness(r, f, store, fp, labels[cid]["root_run"])
                if why:
                    if s != "C-llm":  # C-llm staleness is already listed by the main loop
                        problems.append(f"{s}/{cid}: stale ({why})")
                    r = None
            if r is None or is_infrastructure_error(r):
                rows.append(None)
                continue
            seq = tuple((e["action"], e["run_id"]) for e in (r.get("experiments") or []) if e.get("run_id"))
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


def verifier_verdict(r: dict) -> dict | None:
    """The deterministic verdict (with per_qoi) inside a stored result; None for systems without one (A, L-judge)."""
    if "per_qoi" in r:
        return r  # B, B-v1, B-v2: the result is the verdict
    if isinstance(r.get("verifier"), dict):
        return r["verifier"]  # Bexh
    v = r.get("verdict")
    return v if isinstance(v, dict) else None  # adaptive loop


def current_result(bench: Path, s: str, cid: str, labels: dict, store: RunStore, fp: str) -> dict | None:
    """The stored benchmark result if it exists, is current and is not an infrastructure error, else None."""
    f = bench / s / f"{cid}.json"
    if not f.exists():
        return None
    r = json.loads(f.read_text())
    if staleness(r, f, store, fp, labels[cid]["root_run"]) or is_infrastructure_error(r):
        return None
    return r


def _calibration_rows(items, uT: dict) -> tuple[list[str], dict]:
    """items: (case, system, verdict dict, |errors| of the root).  Rows for the quantities whose mesh, time and
    domain components all carry an estimate, and the coverage counts."""
    rows, n = [], {"covered": 0, "covered_within_truth_unc": 0, "total": 0}
    for cid, s, v, errors in items:
        for q, pq in ((v or {}).get("per_qoi") or {}).items():
            cu = pq.get("component_uncertainty") or {}
            if not all(k in cu for k in ("mesh", "time", "domain")):
                continue
            bias = cu.get("averaging", 0.0)
            rss = sum(x**2 for k, x in cu.items() if k != "averaging") ** 0.5
            U = bias + rss
            e = errors.get(q)
            if e is None:
                continue
            cov = e <= U
            cov2 = e <= (U**2 + uT.get(q, 0.0) ** 2) ** 0.5
            n["total"] += 1
            n["covered"] += cov
            n["covered_within_truth_unc"] += cov2
            rows.append(f"| {cid} | {s} | {q} | {e:.2%} | {U:.2%} | {pq['verdict']} | {'yes' if cov else ('within U(T)' if cov2 else '**NO**')} |")
    return rows, n


def calibration_table(bench: Path, cases: list[str], labels: dict, uT: dict, store: RunStore, fp: str,
                      att_items: list) -> tuple[list[str], dict]:
    """Are the verifier's uncertainty estimates honest?  For every adaptive/exhaustive result in which all three
    discretisation components (mesh, time, domain) carry an estimate, compare the verifier's total
    U = averaging bias + RSS(other components) for the ROOT's reported value with that value's error against the
    in-house reference (an independent estimate: the reference uses chains around the baseline, not around the case).
    Attack results (att_items, same tuple layout as _calibration_rows) are tabulated and counted separately."""
    items = []
    for s in ("C-rule", "C-llm", "Bexh"):
        for cid in cases:
            r = current_result(bench, s, cid, labels, store, fp)
            if r is not None:
                items.append((cid, s, verifier_verdict(r), labels[cid]["errors"]))
    rows, n = _calibration_rows(items, uT)
    arows, an = _calibration_rows(att_items, uT)
    summary = {"benchmark": n, "attacks": an}
    if not rows and not arows:
        return [], summary
    head = ["| case | system | quantity | error vs reference | verifier U | verdict | covered |",
            "|---|---|---|---|---|---|---|"]
    out = ["", "### Calibration: the verifier's uncertainty estimate vs the error against the reference", "",
           "_Cases where mesh, time and domain all carry an estimate. U = averaging bias + RSS(components). "
           "'within U(T)': not covered by U alone, but by U combined with the reference's own uncertainty._", "",
           *head, *rows, "",
           f"Benchmark cases only: covered by U: {n['covered']}/{n['total']}; by U combined with U(T): "
           f"{n['covered_within_truth_unc']}/{n['total']}."]
    out += ["", "Attack cases (results/attacks/, same definition; errors of the attack roots against the same "
                "reference; results counted as in the attack section below):", ""]
    if arows:
        out += [*head, *arows, "",
                f"Attack cases only: covered by U: {an['covered']}/{an['total']}; by U combined with U(T): "
                f"{an['covered_within_truth_unc']}/{an['total']}."]
    else:
        out.append("No attack result has an estimate for all of mesh, time and domain.")
    return out, summary


def _rate(num: int, den: int):
    return None if den == 0 else num / den


def attack_labels(store: RunStore, T: dict, uT: dict, tau: dict) -> dict:
    """Labels of the attack roots against the benchmark reference, under both readings of the set-up clause.

    strict reading: set-up problems are those the benchmark labels use (wrong Re or steady formulation, from the
    evidence); set-up reading: the attack's departures from the problem statement count as well."""
    out = {}
    for f in sorted((REPO / "cases" / "attacks").glob("*.yaml")):
        cid = f.stem
        root = current_root(store, REPO, {"id": cid, "definition": str(f.relative_to(REPO))})
        if root is None:
            out[cid] = {"label": "unrun"}
            continue
        ev = store.load(root).evidence or {}
        rep = (ev.get("qoi") or {}).get("reported") or {}
        sp, dep = setup_problems(ev), ATTACK_SETUP_DEPARTURES.get(cid, [])
        lab = label_case(rep, T, tau, sp, truth_uncertainty=uT)
        conf = ev.get("configuration") or {}
        lab.update(label_point_estimate=label_case(rep, T, tau, sp)["label"],
                   label_setup_reading=label_case(rep, T, tau, sp + dep, truth_uncertainty=uT)["label"],
                   setup_departures=dep, root_run=root, reported={q: rep.get(q) for q in tau},
                   signed_errors={q: (rep[q] - T[q]) / T[q] for q in tau if rep.get(q) is not None},
                   configured_reynolds=conf.get("configured_reynolds"), solver=conf.get("solver"))
        out[cid] = lab
    return out


def attack_results(store: RunStore, alabels: dict) -> tuple[dict, list[str]]:
    """{(system, case): entry} for every attack system and labelled attack case.

    Attack results carry no decision-code stamp; scripts/replay_verdicts.py is their currency check
    (methodology E11).  A result with another root, a replay mismatch or an infrastructure error is shown but not
    counted; a result not covered by the last replay is counted and flagged."""
    att = REPO / "results" / "attacks"
    rp = REPO / "results" / "analysis" / "replay.json"
    replay, t_replay = {}, None
    if rp.exists():
        replay = {(x["system"], x["case"]): x["status"] for x in json.loads(rp.read_text()) if x.get("group") == "attacks"}
        t_replay = rp.stat().st_mtime
    out, notes = {}, []
    for s in ATT_SYSTEMS:
        for cid, lab in alabels.items():
            if lab["label"] == "unrun":
                continue
            f = att / s / f"{cid}.json"
            if not f.exists():
                out[(s, cid)] = {"verdict": "—", "counted": False, "status": "missing", "result": None}
                notes.append(f"{s}/{cid}: missing")
                continue
            r = json.loads(f.read_text())
            v = "ERROR" if is_infrastructure_error(r) else (r.get("final_verdict") or r.get("verdict"))
            if verifier_verdict(r) is None:
                rs = "not applicable (no deterministic verdict)"
            elif t_replay is not None and f.stat().st_mtime > t_replay:
                rs = "written after the last replay"
            elif (s, cid) not in replay:
                rs = "not replayed"
            else:
                rs = replay[(s, cid)]
            why = None
            if r.get("root_run") != lab["root_run"]:
                why = f"root {r.get('root_run')} != current root {lab['root_run']}"
            elif v == "ERROR":
                why = "infrastructure error"
            elif rs.startswith(("MISMATCH", "replay error")):
                why = f"replay: {rs}"
            if why:
                notes.append(f"{s}/{cid}: not counted ({why})")
            elif rs in ("written after the last replay", "not replayed"):
                notes.append(f"{s}/{cid}: counted, {rs} (run scripts/replay_verdicts.py to check it)")
            out[(s, cid)] = {"verdict": v, "counted": why is None, "status": why or "current", "replay": rs,
                             "result": r if why is None else None,
                             **{k: outcome(lab[k], v) for k, _ in READINGS}}
    return out, notes


def attack_section(alabels: dict, ares: dict, anotes: list[str], tau: dict) -> tuple[list[str], dict]:
    qs = list(tau)
    L = ["", "### Attack cases against the reference", "",
         "_Attack roots (cases/attacks/) labelled with the benchmark rule (orchestration/truth.label_case) against "
         "the same reference T. Errors are signed, (reported − T)/T. Strict reading: only the set-up problems the "
         "benchmark labels use (wrong Re or steady formulation, read from the evidence) count; set-up reading: the "
         "attack's departure from the problem statement (case definition) counts as well._", ""]
    if SETUP_CLAUSE not in (REPO / "docs" / "design.md").read_text():
        L += ["**The quoted set-up clause is no longer found verbatim in docs/design.md: update SETUP_CLAUSE before "
              "using this section.**", ""]
    L += ["| attack | reported Cd | reported St | err Cd | err St | max err / τ | set-up departure (case definition) | "
         "label: strict, point estimates | label: strict, with mitigation | label: set-up reading |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for cid, lab in alabels.items():
        if lab["label"] == "unrun":
            L.append(f"| {cid} | root run does not exist |||||||||")
            continue
        rep, se = lab["reported"], lab["signed_errors"]
        L.append(f"| {cid} | " + " | ".join("—" if rep.get(q) is None else f"{rep[q]:.4f}" for q in qs) + " | "
                 + " | ".join("—" if q not in se else f"{se[q]:+.2%}" for q in qs)
                 + f" | {lab['max_error_over_tolerance']:.2f} | {'; '.join(lab['setup_departures']) or 'none'} | "
                 f"{lab['label_point_estimate']} | {lab['label']} | {lab['label_setup_reading']} |")
    for cid, lab in alabels.items():
        if lab["label"] == "unrun" or lab["label_setup_reading"] == lab["label_point_estimate"]:
            continue
        errs = lab["errors"]
        within_half = all(errs[q] <= 0.5 * tau[q] for q in errs)
        bounds = []
        for q in lab["threshold_straddled"]:
            u = lab["truth_uncertainty"].get(q, 0.0)
            thr = "τ" if errs[q] - u < tau[q] < errs[q] + u else "τ/2"
            bounds.append(f"{SHORT.get(q, q)} {errs[q]:.2%} ± {u:.2%} straddles {thr}")
        re = lab["configured_reynolds"]
        re = "not recorded" if re is None else f"{re:.4g}"
        L += ["", f"**{cid}:** the point-estimate errors ("
              + ", ".join(f"{SHORT.get(q, q)} {errs[q]:.2%}" for q in qs if q in errs) + ") are "
              + (f"within τ/2 = {0.5 * max(tau.values()):.1%} for every quantity" if within_half
                 else f"at most {lab['max_error_over_tolerance']:.2f} τ")
              + f", so {cid} is flawed only if the §19 set-up clause applies. The clause (docs/design.md §19, "
              f"pre-registered evaluation protocol): a case is flawed \"{SETUP_CLAUSE}\". The evidence shows neither "
              f"(configured Re = {re}, solver {lab['solver']}). Strict reading (the "
              f"parenthesis is exhaustive): {cid} is labelled by its error, {lab['label_point_estimate']} on point "
              f"estimates and {lab['label']} with the truth-uncertainty mitigation"
              + (f" ({'; '.join(bounds)})" if bounds else "") + ". Set-up reading (the parenthesis gives examples; "
              f"here: {'; '.join(lab['setup_departures'])}): flawed."]
    systems = [s for s in ATT_SYSTEMS if any(k[0] == s for k in ares)]
    L += ["", "Attack verdicts. Where the readings disagree the cell shows the outcome under the set-up reading / "
              "under the strict reading on point estimates (with the mitigation the strict label of such a case may "
              "be ambiguous, and its verdict is then not scored; see the labels above).", "",
          "| attack | label: set-up / strict (point) | " + " | ".join(systems) + " |",
          "|---|---|" + "---|" * len(systems)]
    for cid, lab in alabels.items():
        if lab["label"] == "unrun":
            continue
        cells = []
        for s in systems:
            e = ares.get((s, cid))
            if e is None or not e["counted"]:
                cells.append(f"{'—' if e is None else e['verdict']} {MARKS['missing' if e is None or e['status'] == 'missing' else 'stale']}")
                continue
            a, b = MARKS[e["label_setup_reading"]], MARKS[e["label_point_estimate"]]
            cells.append(f"{e['verdict']} {a}" if a == b else f"{e['verdict']} {a} / {b}")
        L.append(f"| {cid} | {lab['label_setup_reading']} / {lab['label_point_estimate']} | " + " | ".join(cells) + " |")
    L += ["", "✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE · `~` / `~·` ambiguous "
              "label, not scored · ? missing · S not counted (see notes)", "",
          "| reading | " + " | ".join(systems) + " |", "|---|" + "---|" * len(systems)]
    summary = {}
    for key, name in READINGS:
        cells = []
        for s in systems:
            es = [e for (s2, _), e in ares.items() if s2 == s and e["counted"]]
            c = {o: sum(1 for e in es if e[key] == o) for o in ("correct", "false_accept", "false_reject")}
            c["n"] = len(es)
            summary.setdefault(s, {})[key] = c
            cells.append(f"{c['correct']} / {c['false_accept']} / {c['false_reject']} (of {c['n']})")
        L.append(f"| {name}: correct / **false acc.** / false rej. | " + " | ".join(cells) + " |")
    if anotes:
        L += ["", "Notes on the attack results: " + "; ".join(anotes) + "."]
    return L, summary


def per_quantity_section(items: list, tau: dict, uT: dict) -> tuple[list[str], dict]:
    """items: (group, system, case, case verdict, verdict dict, |errors| of the root)."""
    counts, flagged = {}, []
    for g, s, cid, cv, v, errors in items:
        c = counts.setdefault((g, s), {"quantities": 0, "ACCEPT": 0, "accept_within_half_tau": 0,
                                       "accept_within_tau": 0, "accept_beyond_tau": 0, "REJECT": 0,
                                       "reject_within_half_tau": 0, "INCONCLUSIVE": 0})
        for q, pq in ((v or {}).get("per_qoi") or {}).items():
            e, pv = errors.get(q), pq.get("verdict")
            if e is None or q not in tau:
                continue
            c["quantities"] += 1
            if pv in ("ACCEPT", "REJECT", "INCONCLUSIVE"):
                c[pv] += 1
            u = uT.get(q, 0.0)
            row = {"group": g, "system": s, "case": cid, "quantity": q, "error": e, "truth_uncertainty": u,
                   "verifier_U": pq.get("combined_uncertainty"), "quantity_verdict": pv, "case_verdict": cv}
            if pv == "ACCEPT":
                if e <= 0.5 * tau[q]:
                    c["accept_within_half_tau"] += 1
                elif e <= tau[q]:
                    c["accept_within_tau"] += 1
                else:
                    c["accept_beyond_tau"] += 1
                    flagged.append({**row, "finding": "false acceptance (e > τ)",
                                    "holds_for_every_T_within_UT": e - u > tau[q]})
            elif pv == "REJECT" and e <= 0.5 * tau[q]:
                c["reject_within_half_tau"] += 1
                flagged.append({**row, "finding": "REJECT of an accurate quantity (e ≤ τ/2)",
                                "holds_for_every_T_within_UT": e + u <= 0.5 * tau[q]})
    L = ["", "### Per-quantity verdict accuracy", "",
         "_Per-quantity verdicts of the deterministic verifier (`per_qoi`) against the error e of the root's reported "
         "value. ACCEPT with e > τ is a false acceptance at quantity level; REJECT with e ≤ τ/2 rejects an accurate "
         "quantity (the case-level REJECT can still be right when another quantity is wrong). Benchmark: current, "
         "non-error results; attacks: results counted in the attack section. The ACCEPT columns partition the "
         "ACCEPTs._", "",
         "| group | system | quantity verdicts | ACCEPT | ACCEPT, e ≤ τ/2 | ACCEPT, τ/2 < e ≤ τ | **ACCEPT, e > τ** | "
         "REJECT | REJECT, e ≤ τ/2 | INCONCLUSIVE |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for (g, s), c in counts.items():
        L.append(f"| {g} | {s} | {c['quantities']} | {c['ACCEPT']} | {c['accept_within_half_tau']} | "
                 f"{c['accept_within_tau']} | {c['accept_beyond_tau']} | {c['REJECT']} | {c['reject_within_half_tau']} | "
                 f"{c['INCONCLUSIVE']} |")
    L += ["", "Quantity-level false acceptances and rejections of an accurate quantity "
              "(last column: the finding holds for every reference value within T ± U(T)):", ""]
    if flagged:
        L += ["| group | case | system | quantity | error | U(T) | verifier U | quantity verdict | case verdict | "
              "finding | holds within ± U(T) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for x in flagged:
            vu = "—" if x["verifier_U"] is None else f"{x['verifier_U']:.2%}"
            L.append(f"| {x['group']} | {x['case']} | {x['system']} | {x['quantity']} | {x['error']:.2%} | "
                     f"{x['truth_uncertainty']:.2%} | {vu} | {x['quantity_verdict']} | {x['case_verdict']} | "
                     f"{x['finding']} | {'yes' if x['holds_for_every_T_within_UT'] else 'no'} |")
    else:
        L.append("None.")
    return L, {"counts": {f"{g}/{s}": c for (g, s), c in counts.items()}, "flagged": flagged}


def sign_test_p(k: int, n: int) -> float | None:
    """Exact two-sided sign test (binomial, p = 0.5) for k successes in n non-tied pairs."""
    if n == 0:
        return None
    m = min(k, n - k)
    return min(1.0, 2.0 * sum(math.comb(n, i) for i in range(m + 1)) / 2**n)


def criterion_5b(metrics: dict, cases: list[str], labels: dict, matrix: dict) -> tuple[list[str], dict]:
    """The decision rule for success criterion 5b, as fixed in docs/methodology.md (section 'Decision rule for
    success criterion 5b'): C-llm (first run) vs C-rule over the cases where both have a current, non-error result."""
    L = ["", "### Criterion 5b decision rule (docs/methodology.md, 'Decision rule for success criterion 5b')", ""]
    if "C-llm" not in metrics or "C-rule" not in metrics:
        L.append("Not evaluated: C-llm or C-rule has no results.")
        return L, {"evaluated": False}
    pr, pl = metrics["C-rule"]["cases"], metrics["C-llm"]["cases"]
    paired, unpaired = [], []
    for cid in cases:
        why = [f"{s}: {matrix.get((s, cid), ('—', 'missing'))[1]}" for s, c in (("C-rule", pr.get(cid)), ("C-llm", pl.get(cid)))
               if c is None or c["outcome"] == "error"]
        (unpaired if why else paired).append((cid, why))
    views = [("label", "with mitigation"), ("label_point_estimate", "point estimates")]
    acc = {}
    for key, _ in views:
        for s, pc in (("C-rule", pr), ("C-llm", pl)):
            lv = [(labels[cid][key], pc[cid]["verdict"]) for cid, _ in paired]
            acc.setdefault(key, {})[s] = {
                "correct": sum(1 for lb, v in lv if (lb, v) in (("flawed", "REJECT"), ("credible", "ACCEPT"))),
                "false_accept": sum(1 for lb, v in lv if (lb, v) == ("flawed", "ACCEPT")),
                "false_reject": sum(1 for lb, v in lv if (lb, v) == ("credible", "REJECT"))}
    more_correct = any(acc[k]["C-llm"]["correct"] > acc[k]["C-rule"]["correct"] for k, _ in views)
    no_worse = all(acc[k]["C-llm"][m] <= acc[k]["C-rule"][m] for k, _ in views for m in ("false_accept", "false_reject"))
    beats_accuracy = more_correct and no_worse
    rows, n_diff, k_llm, k_rule = [], 0, 0, 0
    for cid, _ in paired:
        a, b = pr[cid]["relative_compute"], pl[cid]["relative_compute"]
        differ = abs(a - b) > 0.05 * max(a, b)
        n_diff += differ
        k_llm += differ and b < a
        k_rule += differ and a < b
        rows.append(f"| {cid} | {labels[cid]['label']} | {labels[cid]['label_point_estimate']} | {pr[cid]['verdict']} | "
                    f"{pl[cid]['verdict']} | {a:.2f} | {b:.2f} | {'yes' if differ else 'no'} | "
                    f"{('C-llm' if b < a else 'C-rule') if differ else '—'} |")
    tot_rule = sum(pr[cid]["relative_compute"] for cid, _ in paired)
    tot_llm = sum(pl[cid]["relative_compute"] for cid, _ in paired)
    usd = sum(pl[cid].get("planner_cost_usd") or 0.0 for cid, _ in paired)
    p = sign_test_p(k_llm, n_diff)
    beats_cost = tot_llm < tot_rule and p is not None and k_llm > k_rule and p < 0.05
    meets = beats_accuracy or beats_cost
    concl = "meets 5b" if meets else "does not meet 5b: the LLM planner adds no measurable value on this benchmark"
    L += ["_C-llm (first run) against C-rule over the cases where both have a current, non-error result; repeats "
          "(C-llm-r*) do not enter. Correct decisions: flawed → REJECT, credible → ACCEPT. Cost: experiment cell-steps "
          "relative to the root, per case (wall time excluded). Costs differ when |C-llm − C-rule| > 5 % of the larger "
          "of the two; the sign test is exact, two-sided, binomial with p = 0.5, over those cases._", "",
          "| case | label (with mitigation) | label (point estimates) | C-rule | C-llm | C-rule compute (× root) | "
          "C-llm compute (× root) | differ > 5 % | cheaper |", "|---|---|---|---|---|---|---|---|---|", *rows, "",
          f"Paired cases: {len(paired)} of {len(cases)}."
          + (" Not paired: " + "; ".join(f"{cid} ({', '.join(w)})" for cid, w in unpaired) + "." if unpaired else ""), "",
          "| label view | correct: C-rule | correct: C-llm | **false acc.**: C-rule | **false acc.**: C-llm | "
          "false rej.: C-rule | false rej.: C-llm |", "|---|---|---|---|---|---|---|"]
    for key, name in views:
        r_, l_ = acc[key]["C-rule"], acc[key]["C-llm"]
        L.append(f"| {name} | {r_['correct']} | {l_['correct']} | {r_['false_accept']} | {l_['false_accept']} | "
                 f"{r_['false_reject']} | {l_['false_reject']} |")
    L += ["", f"- Accuracy: more correct decisions in at least one view: {'yes' if more_correct else 'no'}; no more "
              f"false acceptances or false rejections in either view: {'yes' if no_worse else 'no'} → "
              f"LLM planner beats the rule planner on accuracy: **{'yes' if beats_accuracy else 'no'}**.",
          f"- Cost: total paired compute C-rule {tot_rule:.2f} × root, C-llm {tot_llm:.2f} × root (C-llm lower: "
          f"{'yes' if tot_llm < tot_rule else 'no'}); costs differ in {n_diff} cases, C-llm cheaper in {k_llm}, "
          f"C-rule cheaper in {k_rule}; sign test p = {'—' if p is None else f'{p:.3g}'} → LLM planner beats the "
          f"rule planner on cost: **{'yes' if beats_cost else 'no'}**.",
          f"- LLM cost on the paired cases (counts against the LLM): {usd:.2f} USD.", "",
          f"**Criterion 5b: {concl}.**"
          + (f" Provisional: the rule is applied to the {len(paired)} paired cases; the conclusion can change when "
             f"the {len(unpaired)} unpaired case(s) have current, non-error results in both systems." if unpaired else "")]
    return L, {"evaluated": True, "paired_cases": [c for c, _ in paired],
               "unpaired_cases": {c: w for c, w in unpaired}, "accuracy": acc,
               "more_correct_in_a_view": more_correct, "no_more_false_decisions": no_worse,
               "beats_on_accuracy": beats_accuracy, "total_relative_compute": {"C-rule": tot_rule, "C-llm": tot_llm},
               "n_cost_differs_gt_5pct": n_diff, "n_llm_cheaper": k_llm, "n_rule_cheaper": k_rule,
               "sign_test_p_two_sided": p, "beats_on_cost": beats_cost, "llm_cost_usd_paired": usd,
               "conclusion": concl, "provisional": bool(unpaired)}


def main() -> None:
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = ProblemSpec.from_yaml(REPO / man["problem_spec"])
    truth = json.loads((REPO / "results" / "baseline" / "truth.json").read_text())["truth"]
    T = {q: truth[q]["value"] for q in spec.requested_outputs}
    uT = {q: truth[q]["uncertainty_rel"] for q in spec.requested_outputs}
    store = RunStore(REPO / "results" / "runs")
    bench = REPO / "results" / "benchmark"
    fp = decision_code_fingerprint()

    labels, problems = {}, []
    for s in SYSTEMS:
        if not (bench / s).is_dir():
            problems.append(f"system {s}: no results")
    for case in man["cases"]:
        root = current_root(store, REPO, case)
        if root is None:
            labels[case["id"]] = {"label": "unrun", "intended": case["intended"]}
            problems.append(f"{case['id']}: root run of the manifest definition does not exist")
            continue
        ev = store.load(root).evidence or {}
        rep = (ev.get("qoi") or {}).get("reported") or {}
        lab = label_case(rep, T, spec.verification.requested_tolerance, setup_problems(ev), truth_uncertainty=uT)
        # the docs/design.md section-19 rule verbatim, on point estimates (without the truth-uncertainty mitigation)
        lab["label_point_estimate"] = label_case(rep, T, spec.verification.requested_tolerance, setup_problems(ev))["label"]
        lab.update(intended=case["intended"], expected=case["expected_expert_judgement"], root_run=root,
                   reported={q: rep.get(q) for q in spec.requested_outputs},
                   revealing_experiment=case.get("revealing_experiment"))
        labels[case["id"]] = lab
    (REPO / "benchmark" / "labels.json").write_text(json.dumps(
        {"truth": T, "truth_uncertainty_rel": uT, "rule": man["tolerance_rule"], "cases": labels}, indent=1))
    cases = [c for c, v in labels.items() if v["label"] != "unrun"]

    metrics, matrix = {}, {}
    for s in SYSTEMS:
        if not (bench / s).is_dir():
            continue
        per_case, n_exp, rel_cost, wall, llm_cost, viol, untraced = {}, [], [], [], 0.0, 0, 0
        hit = miss = n_stale = n_missing = 0
        for cid in cases:
            f = bench / s / f"{cid}.json"
            if not f.exists():
                problems.append(f"{s}/{cid}: missing")
                matrix[(s, cid)] = ("—", "missing")
                n_missing += 1
                continue
            r = json.loads(f.read_text())
            why = staleness(r, f, store, fp, labels[cid]["root_run"])
            if why:
                problems.append(f"{s}/{cid}: stale ({why})")
                matrix[(s, cid)] = ("stale", "stale")
                n_stale += 1
                continue
            v = "ERROR" if is_infrastructure_error(r) else (r.get("final_verdict") or r.get("verdict"))
            lab = labels[cid]["label"]
            o = outcome(lab, v)
            matrix[(s, cid)] = (v, o)
            per_case[cid] = {"verdict": v, "label": lab, "outcome": o}
            if o == "error":
                continue  # errors carry no verification outcome: excluded from experiment/cost/flaw-targeting tallies
            exps = [e for e in (r.get("experiments") or []) if e.get("run_id")]
            if s in ("C-rule", "C-llm", "Bexh"):
                n_exp.append(len(exps))
                root_cs = ((store.load(labels[cid]["root_run"]).evidence or {}).get("cost") or {}).get("cell_steps") or 1
                cs = sum((((store.load(e["run_id"]).evidence or {}).get("cost") or {}).get("cell_steps") or 0) for e in exps)
                rel_cost.append(cs / root_cs)
                per_case[cid]["relative_compute"] = cs / root_cs
                wall.append(sum(((store.load(e["run_id"]).provenance or {}).get("wall_seconds") or 0) for e in exps))
            if s in ("C-rule", "C-llm"):
                per_case[cid]["planner_cost_usd"] = (r.get("cost") or {}).get("planner_cost_usd") or 0.0
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
            "errors_by_label": errors_by_label, "n_stale_excluded": n_stale, "n_missing": n_missing,
            "false_acceptance_rate": _rate(count("flawed", {"ACCEPT"}), nf),
            "detection_rate": _rate(count("flawed", {"REJECT"}), nf),
            "missed_but_safe_rate": _rate(count("flawed", {"INCONCLUSIVE"}), nf),
            "correct_acceptance_rate": _rate(count("credible", {"ACCEPT"}), nc),
            "false_rejection_rate": _rate(count("credible", {"REJECT"}), nc),
            "inconclusive_rate": _rate(sum(1 for c in decided if c["verdict"] == "INCONCLUSIVE"), len(decided)),
            "ambiguous_verdicts": {v: count("ambiguous", {v}) for v in ("ACCEPT", "REJECT", "INCONCLUSIVE")},
            "ambiguous_accepts_above_best_estimate_tau": sum(
                1 for cid, c in per_case.items() if c["outcome"] == "ambiguous_accept"
                and labels[cid]["max_error_over_tolerance"] > 1.0),
            "mean_experiments": (sum(n_exp) / len(n_exp)) if n_exp else 0.0,
            "total_experiments": sum(n_exp),
            "mean_compute_relative_to_root": (sum(rel_cost) / len(rel_cost)) if rel_cost else 0.0,
            "total_experiment_wall_hours": sum(wall) / 3600.0,
            "llm_cost_usd": llm_cost,
            "authority_violations": viol,
            "untraced_numbers": untraced,
            "first_experiment_targets_flaw": f"{hit}/{hit + miss}" if (hit + miss) else None,
        }}
    systems = [s for s in SYSTEMS if s in metrics]
    for s in systems:  # same verdicts, labels from the section-19 rule without the truth-uncertainty mitigation
        pc = [(labels[cid]["label_point_estimate"], c["verdict"]) for cid, c in metrics[s]["cases"].items()
              if c["outcome"] != "error"]

        def cnt(label, verdicts, pc=pc):
            return sum(1 for lb, v in pc if lb == label and v in verdicts)

        nf2, nc2 = cnt("flawed", {"ACCEPT", "REJECT", "INCONCLUSIVE"}), cnt("credible", {"ACCEPT", "REJECT", "INCONCLUSIVE"})
        metrics[s]["summary_point_estimate_labels"] = {
            "n_flawed": nf2, "n_credible": nc2, "n_ambiguous": len(pc) - nf2 - nc2,
            "false_acceptance_rate": _rate(cnt("flawed", {"ACCEPT"}), nf2),
            "detection_rate": _rate(cnt("flawed", {"REJECT"}), nf2),
            "missed_but_safe_rate": _rate(cnt("flawed", {"INCONCLUSIVE"}), nf2),
            "correct_acceptance_rate": _rate(cnt("credible", {"ACCEPT"}), nc2),
            "false_rejection_rate": _rate(cnt("credible", {"REJECT"}), nc2),
        }

    # ---------------- attacks, per-quantity accuracy, criterion 5b ----------------
    tau = spec.verification.requested_tolerance
    alabels = attack_labels(store, T, uT, tau)
    ares, anotes = attack_results(store, alabels)
    att_lines, att_summary = attack_section(alabels, ares, anotes, tau)
    att_items = [(cid, s, verifier_verdict(e["result"]), alabels[cid]["errors"]) for (s, cid), e in ares.items()
                 if e["counted"] and verifier_verdict(e["result"]) is not None]
    pq_items = []
    for s in ["B", "C-rule", "C-llm", "Bexh"] + sorted(d.name for d in bench.glob("C-llm-r*") if d.is_dir()):
        for cid in cases:
            r = current_result(bench, s, cid, labels, store, fp)
            if r is not None:
                pq_items.append(("benchmark", s, cid, r.get("final_verdict") or r.get("verdict"), verifier_verdict(r),
                                 labels[cid]["errors"]))
    pq_items += [("attacks", s, cid, ares[(s, cid)]["verdict"], v, errs) for cid, s, v, errs in att_items]
    pq_lines, pq_summary = per_quantity_section(pq_items, tau, uT)
    c5b_lines, c5b = criterion_5b(metrics, cases, labels, matrix)
    cal_lines, cal_summary = calibration_table(bench, cases, labels, uT, store, fp, att_items)

    # ---------------- tables ----------------
    var_lines = variance_table(bench, cases, labels, store, fp, problems)
    (bench / "metrics.json").write_text(json.dumps({
        "problems": problems, "metrics": metrics,
        "attacks": {"labels": alabels, "notes": anotes, "summary": att_summary,
                    "results": {f"{s}/{cid}": {k: v for k, v in e.items() if k != "result"} for (s, cid), e in ares.items()}},
        "per_quantity": pq_summary, "criterion_5b": c5b, "calibration": cal_summary}, indent=1))
    L = []
    if problems:
        L += ["**Missing or stale results (NOT counted in the rates of the system concerned; recompute before "
              "drawing conclusions):** " + "; ".join(problems), ""]
    L += ["_Percentages: errors against the reference T are relative to T. Verifier sensitivity changes are relative "
          "to the finer (child) member of a study, |q_fine − q_root| / |q_fine| (checks/sensitivity.py; the finest "
          "member for a three-level chain). Observation lines in the case reports (reports/cases/) and the loop "
          "traces in benchmark_results.md are relative to the parent run, (q_child − q_parent) / q_parent._", ""]
    L += ["| case | label (with mitigation) | max err / τ | unstable | label without mitigation | " + " | ".join(systems) + " |",
          "|---|---|---|---|---|" + "---|" * len(systems)]
    for cid in cases:
        lab = labels[cid]
        cells = []
        for s in systems:
            v, o = matrix.get((s, cid), ("—", "missing"))
            cells.append(f"{v} {MARKS[o]}")
        L.append(f"| {cid} | {lab['label']} | {lab['max_error_over_tolerance']:.2f} | "
                 f"{','.join(lab['label_unstable']) or ''} | {lab['label_point_estimate']} | " + " | ".join(cells) + " |")
    L += ["", "✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · "
              "`~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · "
              "S stale (not counted)", ""]
    keys = [("n", "cases"), ("n_flawed", "flawed cases (decided)"), ("n_credible", "credible cases (decided)"),
            ("n_ambiguous", "ambiguous cases (decided)"),
            ("false_acceptance_rate", "**false acceptance** (flawed → ACCEPT)"), ("detection_rate", "detection (flawed → REJECT)"),
            ("missed_but_safe_rate", "missed but safe (flawed → INCONCLUSIVE)"),
            ("correct_acceptance_rate", "correct acceptance (credible → ACCEPT)"),
            ("false_rejection_rate", "false rejection (credible → REJECT)"), ("inconclusive_rate", "inconclusive (all decided)"),
            ("ambiguous_verdicts", "ambiguous cases: verdicts"),
            ("ambiguous_accepts_above_best_estimate_tau", "ambiguous cases ACCEPTed although best-estimate error > τ"),
            ("n_error", "errors (excluded from rates)"), ("n_stale_excluded", "stale results (excluded)"),
            ("n_missing", "missing results"),
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
    L += ["", "### Labels without the truth-uncertainty mitigation (design.md §19 rule verbatim, point estimates)", "",
          "_Same verdicts; only the labels change. Both label sets are pre-registered: the §19 rule, and the risk "
          "mitigation 'label near-boundary cases ambiguous' (design.md, major technical risks 2), operationalised in "
          "review R18 before any result as 'the interval e ± U(T) straddles τ or τ/2'. The table above uses the "
          "mitigation._", "",
          "| metric | " + " | ".join(systems) + " |", "|---|" + "---|" * len(systems)]
    for k, name in [("n_flawed", "flawed cases"), ("n_credible", "credible cases"), ("n_ambiguous", "ambiguous cases"),
                    ("false_acceptance_rate", "**false acceptance**"), ("detection_rate", "detection"),
                    ("missed_but_safe_rate", "missed but safe"), ("correct_acceptance_rate", "correct acceptance"),
                    ("false_rejection_rate", "false rejection")]:
        vals = [metrics[s]["summary_point_estimate_labels"].get(k) for s in systems]
        L.append(f"| {name} | " + " | ".join("—" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x))
                                              for x in vals) + " |")
    L += cal_lines
    L += var_lines
    L += att_lines
    L += pq_lines
    L += c5b_lines
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
    keys_l = ["correct", "false_accept", "false_reject", "undecided", "ambiguous_accept", "ambiguous_reject",
              "ambiguous_inconclusive", "error"]
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=STATUS_COLORS[k], ec="#b4b2ad", lw=0.4) for k in keys_l],
              ["correct", "false acceptance (dangerous)", "false rejection", "inconclusive (safe)",
               "ambiguous case: ACCEPT", "ambiguous case: REJECT", "ambiguous case: INCONCLUSIVE (expected)", "error"],
              loc="upper center", bbox_to_anchor=(0.5, -0.03), ncol=4, fontsize=7, frameon=False)
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
