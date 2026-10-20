"""Post-hoc analysis, NOT pre-registered: what blocks acceptance, and what would a looser acceptance rule accept?

No new simulation and no change to decision code.  For every stored result that has a run graph (benchmark: B,
C-rule, C-llm, Bexh, C-llm-r*; attacks: B-v1, B-v2, C-rule-v1, C-rule-v2, C-llm-v1, C-llm-v1+review) the current
verifier is replayed on that graph (graph reconstruction of scripts/replay_verdicts.py) and its component checks
are re-aggregated under three acceptance rules:

  V0  pre-registered (checks/verifier.aggregate).  Per quantity, each of the five components (averaging,
      statistics, mesh, time, domain) has one check.  A component PASSes when its estimated relative uncertainty
      U <= component_pass_fraction * tau = tau/2 (sensitivity.assess_sequence, static.check_statistics); the
      averaging bias b PASSes when b <= tau and FAILs above.  A quantity is REJECT if any component FAILs, ACCEPT
      if every component PASSes and U_total = bias + RSS(other components) <= tau, otherwise INCONCLUSIVE.  The case
      is REJECT if any check FAILs, ACCEPT if every gate check passes (courant_number INCONCLUSIVE is discharged by
      a time PASS, convection_scheme_order INCONCLUSIVE by a mesh PASS, for every quantity) and every quantity is
      ACCEPT, otherwise INCONCLUSIVE.
  V1  'combined only': a component that is INCONCLUSIVE only because its U exceeds tau/2 counts as measured;
      ACCEPT if no component is FAIL, missing or unresolved for another reason, and bias + RSS <= tau.
  V2  'domain relaxed': as V0, but the tau/2 limit of the domain component (only) is dropped in the same way.

Criterion for 'INCONCLUSIVE only because U > tau/2': status INCONCLUSIVE with a numerical uncertainty attached
(CheckResult.uncertainty is not None).  In the current decision code exactly two branches return such a result:
the last branch of sensitivity.assess_sequence (U_root > tau/2 and the demonstrated change does not exceed tau by
more than twice the statistical noise) and the u > tau/2 branch of static.check_statistics.  Every other INCONCLUSIVE component result (no experiment, family
member not statistically reliable, unknown temporal order, value missing, degenerate family, divergent sequence,
no positive observed order, steady solver, too few cycles, unreliable averaging reference) carries no
uncertainty.  The script checks U > threshold for every result it treats this way and reports any exception.

The variants are applied by running the decision code's own aggregate() on copies of the checks in which the
relaxed component results are marked PASS; their U still enters bias + RSS.  Gate checks and their discharge are
kept exactly as pre-registered (computed from the unmodified component statuses).  V0 must reproduce the stored
verdict, per quantity and per case; mismatches are reported and make the script exit 1.

An adaptive loop stops at the first decisive verifier verdict.  For C-* results the script therefore also evaluates
every intermediate state of the recorded loop (root plus the first k experiments) and reports the first state at
which each rule is decisive.  This assumes the planner would have chosen the same experiments under the looser
rule, which is not guaranteed (the planner sees the verifier's missing components); for C-llm-v1+review an ACCEPT
would further go to the acceptance review, whose outcome is unknown.

Labels.  Benchmark cases take both label views of benchmark/labels.json, which apply the narrow reading of the
docs/design.md section-19 set-up clause: only set-up problems detected from the evidence (wrong Re, steady
formulation) and missing quantities count; every other departure is judged by its error.  Attack labels are
computed as scripts/analyze_benchmark.py (attack_labels) computes them, in three readings: narrow (`label` with
the truth-uncertainty mitigation, `label_point_estimate` without), literal (`label_literal`: credible needs a
consistent set-up, flawed needs e > tau or a wrong Re or regime, so a departure leaves a within-tau/2 case
ambiguous) and set-up (`label_setup_reading`: any departure from the problem statement makes the case flawed).
Counts are reported in the narrow views, with false acceptances under the set-up reading as an extra column.

    python scripts/posthoc_acceptance_rule.py      # writes results/posthoc/acceptance_rule.{json,md}
                                                   # exit 1 on a V0 mismatch, criterion exception or label mismatch
"""

import copy
import datetime as dt
import json
import math
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

from analyze_benchmark import setup_problems  # noqa: E402  (narrow set-up problems, as in benchmark/labels.json)
from replay_verdicts import GROUPS, V1, V2, stored  # noqa: E402

from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.base import Status  # noqa: E402
from socrates.checks.verifier import COMPONENTS, aggregate, verify  # noqa: E402
from socrates.orchestration.evaluation import is_infrastructure_error, staleness  # noqa: E402
from socrates.orchestration.loop import graph_for  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.systems import decision_code_fingerprint  # noqa: E402
from socrates.orchestration.truth import label_case  # noqa: E402

TAG = "post-hoc analysis, NOT pre-registered: acceptance-rule variants re-evaluated on stored run graphs"
OUT = REPO / "results" / "posthoc"
SPEC = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
STORE = RunStore(REPO / "results" / "runs")
LABELS = json.loads((REPO / "benchmark" / "labels.json").read_text())
T, UT = LABELS["truth"], LABELS["truth_uncertainty_rel"]
TAU = dict(SPEC.verification.requested_tolerance)
QS = list(SPEC.requested_outputs)
SHORT = {"mean_drag_coefficient": "Cd", "strouhal_number": "St"}
ADAPTIVE = ("C-rule", "C-llm")  # system-name prefixes of results produced by the adaptive loop
# Attacks that depart from the problem statement itself, not its numerics (cases/attacks/<id>.yaml 'flaw'; same
# cases as scripts/analyze_benchmark.py).  They decide the label only under the set-up reading of the section-19
# clause (and prevent 'credible' under the literal reading); X3 changes mesh and domain size only and is judged by
# its error in every reading.
ATTACK_SETUP_DEPARTURES = {
    "X1_cylinder_geometry": ["cylinder diameter 1.05 D where the problem specifies D = 10 mm"],
    "X2_inlet_shear": ["sheared inlet profile where the problem specifies a uniform stream"],
}
# label fields of every case: (field, description); the attack-only readings are None for benchmark cases
VIEWS = {"label": "narrow, with mitigation", "label_point_estimate": "narrow, point estimate",
         "label_literal": "literal", "label_setup_reading": "set-up reading"}
REVIEW_SYSTEMS = ("C-llm-v1+review",)  # a verifier ACCEPT goes to the acceptance review, which was not replayed


def u_only(c) -> bool:
    """INCONCLUSIVE solely because the estimated U exceeds the component's pass limit (see module docstring)."""
    return c is not None and c.status == Status.INCONCLUSIVE and c.uncertainty is not None


VARIANTS = {
    "V0": lambda comp, c: False,
    "V1": lambda comp, c: u_only(c),
    "V2": lambda comp, c: comp == "domain" and u_only(c),
}
VARIANT_NAMES = {"V0": "pre-registered", "V1": "combined only", "V2": "domain relaxed"}


def reason_class(c) -> str:
    """Short reason for a non-PASS component result (display only; V1/V2 use u_only())."""
    if c is None:
        return "no check"
    if c.status == Status.FAIL:
        return "FAIL"
    if u_only(c):
        return "U>tau/2"
    r = c.reason
    for key, label in (("experiment has been run", "no experiment"), ("not statistically reliable", "member unreliable"),
                       ("diverges under refinement", "divergent"), ("no positive observed order", "no observed order"),
                       ("degenerate", "degenerate family"), ("no known formal order", "no formal order"),
                       ("not available for runs", "value missing"), ("steady solver", "steady solver"),
                       ("cycles (<", "too few cycles"), ("itself unreliable", "unreliable reference"),
                       ("no stationary estimate", "no stationary estimate")):
        if key in r:
            return label
    return "other: " + r[:60]


def components(v, q: str) -> dict:
    """The check aggregate() uses for each component of q (the last one), or None."""
    out = {}
    for comp in COMPONENTS:
        cs = [c for c in v.checks if c.qoi == q and c.component == comp]
        out[comp] = cs[-1] if cs else None
    return out


def gates(v) -> list[str]:
    """Gate checks that block a case ACCEPT under the pre-registered discharge rule (empty = gates pass)."""
    mesh_ok_all = all(d["component_status"].get("mesh") == "PASS" for d in v.per_qoi.values())
    time_ok_all = all(d["component_status"].get("time") == "PASS" for d in v.per_qoi.values())
    block = []
    for c in v.checks:
        if c.component is not None or c.status == Status.PASS:
            continue
        if c.status == Status.INCONCLUSIVE and ((c.check == "courant_number" and time_ok_all)
                                                or (c.check == "convection_scheme_order" and mesh_ok_all)):
            continue
        block.append(f"{c.check} {c.status.value}")
    return block


def evaluate(v) -> dict:
    """Case and per-quantity verdicts of every variant on one replayed Verdict ``v``."""
    gate_block = gates(v)
    out = {}
    for name, relax in VARIANTS.items():
        checks = [copy.copy(c) for c in v.checks]  # shallow copies: only .status is changed
        for c in checks:
            if c.component is not None and relax(c.component, c):
                c.status = Status.PASS
        pq = aggregate(checks, SPEC).per_qoi
        if v.failed_checks:
            case = "REJECT"
        elif not gate_block and all(d["verdict"] == "ACCEPT" for d in pq.values()):
            case = "ACCEPT"
        else:
            case = "INCONCLUSIVE"
        out[name] = {"case": case, "per_qoi": {q: {"verdict": d["verdict"], "combined_uncertainty": d["combined_uncertainty"]}
                                               for q, d in pq.items()}}
    return {"variants": out, "gates_blocking": gate_block}


def criterion_anomalies(v, where: str) -> list[str]:
    bad = []
    for c in v.checks:
        if c.component is not None and u_only(c) and not (c.threshold is not None and c.uncertainty > c.threshold):
            bad.append(f"{where}: {c.check}[{c.qoi}] INCONCLUSIVE with U={c.uncertainty} not above threshold {c.threshold}")
    return bad


def literal_label(narrow: str, departures: list[str]) -> str:
    """Literal reading of section 19: 'credible' needs 'the set-up is consistent'; 'flawed' needs e > tau or a set-up
    that 'answers a different problem (wrong Re or regime)', which the narrow label already covers.  So a departure
    from the problem statement turns a narrow 'credible' into 'ambiguous' and changes nothing else."""
    return "ambiguous" if departures and narrow == "credible" else narrow


def truth_view(group: str, case: str, root: str) -> dict:
    """Signed true errors vs the reference T and the case labels (VIEWS).  `notes` lists disagreements with
    benchmark/labels.json; they are reported and make the script exit 1."""
    if group == "benchmark":
        lab = LABELS["cases"][case]
        rep = lab["reported"]
        err = {q: None if rep.get(q) is None else (rep[q] - T[q]) / abs(T[q]) for q in QS}
        notes = [f"{q}: |signed error| {abs(e)} != labels.json {lab['errors'].get(q)}" for q, e in err.items()
                 if e is not None and abs(abs(e) - lab["errors"].get(q, math.nan)) > 1e-12]
        if lab["root_run"] != root:
            notes.append(f"stored root {root} != labels.json root {lab['root_run']}")
        return {"errors": err, "label": lab["label"], "label_point_estimate": lab["label_point_estimate"],
                "label_literal": None, "label_setup_reading": None, "setup_problems": lab.get("setup_problems"),
                "setup_departures": None, "error_source": "benchmark/labels.json", "notes": notes}
    ev = json.loads((STORE.root / root / "evidence.json").read_text())
    rep = (ev.get("qoi") or {}).get("reported") or {}
    err = {q: None if rep.get(q) is None else (rep[q] - T[q]) / abs(T[q]) for q in QS}
    sp, dep = setup_problems(ev), ATTACK_SETUP_DEPARTURES.get(case, [])
    narrow = label_case(rep, T, TAU, sp, truth_uncertainty=UT)["label"]
    return {"errors": err, "label": narrow, "label_point_estimate": label_case(rep, T, TAU, sp)["label"],
            "label_literal": literal_label(narrow, dep),
            "label_setup_reading": label_case(rep, T, TAU, sp + dep, truth_uncertainty=UT)["label"],
            "setup_problems": sp, "setup_departures": dep,
            "error_source": f"results/runs/{root}/evidence.json qoi.reported vs benchmark/labels.json truth", "notes": []}


def first_decisive(states: list[dict]) -> dict:
    """Per variant: the first loop state (number of experiments) with a decisive case verdict."""
    out = {}
    for name in VARIANTS:
        hit = next(((k, s["variants"][name]["case"]) for k, s in enumerate(states)
                    if s["variants"][name]["case"] in ("ACCEPT", "REJECT")), None)
        out[name] = {"n_experiments": None if hit is None else hit[0], "verdict": "INCONCLUSIVE" if hit is None else hit[1]}
    return out


def flag(verdict: str, e: float | None, tau: float) -> str:
    if verdict != "ACCEPT" or e is None:
        return ""
    if abs(e) > tau:
        return "FALSE ACCEPT (abs. error > tau)"
    if abs(e) > 0.5 * tau:
        return "abs. error > tau/2"
    return ""


def results():
    """(group, system, case, result dict | None, skip reason | None) for every stored final result."""
    for group, systems in GROUPS.items():
        base = REPO / "results" / group
        extra = sorted(p.name for p in base.glob("C-llm-r*") if p.is_dir()) if group == "benchmark" else []
        for system in systems + extra:
            for f in sorted((base / system).glob("*.json")) if (base / system).is_dir() else []:
                if f.name.endswith(".partial.json"):
                    continue
                try:
                    r = json.loads(f.read_text())
                except (OSError, json.JSONDecodeError) as e:
                    yield group, system, f.stem, None, f"unreadable: {e!r}"
                    continue
                if is_infrastructure_error(r):
                    yield group, system, f.stem, None, "infrastructure error"
                    continue
                yield group, system, f.stem, (r, f), None


def main() -> int:
    fp = decision_code_fingerprint()
    frac = V1["error_budget"]["component_pass_fraction"]
    assert V2["error_budget"]["component_pass_fraction"] == frac
    rows, cases, skipped, mismatches, anomalies, truth_mismatches = [], [], [], [], [], []
    for group, system, case, item, why in results():
        if item is None:
            skipped.append({"group": group, "system": system, "case": case, "reason": why})
            continue
        r, f = item
        old, runs = stored(system, r)
        vcfg = V2 if system.endswith("v2") else V1
        where = f"{group}/{system}/{case}"
        try:
            v = verify(graph_for(STORE, r["root_run"], runs), SPEC, vcfg)
        except Exception as e:  # noqa: BLE001 -- a replay failure is itself a finding
            mismatches.append(f"{where}: replay error {e!r}")
            continue
        anomalies += criterion_anomalies(v, where)
        ev = evaluate(v)
        stale = (staleness(r, f, STORE, fp, LABELS["cases"].get(case, {}).get("root_run"))
                 if group == "benchmark" else None)
        # V0 must reproduce the stored verdict and the stored per-quantity verdicts and combined U
        v0 = ev["variants"]["V0"]
        if v0["case"] != old.get("verdict") or v0["case"] != v.verdict:
            mismatches.append(f"{where}: case V0 {v0['case']} / replay {v.verdict} / stored {old.get('verdict')}")
        for q in QS:
            so = (old.get("per_qoi") or {}).get(q) or {}
            a, b = v0["per_qoi"][q]["combined_uncertainty"], so.get("combined_uncertainty")
            if v0["per_qoi"][q]["verdict"] != so.get("verdict") or (a is None) != (b is None) or (
                    a is not None and abs(a - b) > 1e-9 * max(abs(a), 1e-12)):
                mismatches.append(f"{where} {q}: V0 {v0['per_qoi'][q]} / stored {so.get('verdict')} U={b}")
        tv = truth_view(group, case, r["root_run"])
        truth_mismatches += [f"{where}: {n}" for n in tv["notes"]]
        # intermediate loop states (adaptive systems only)
        loop = None
        if system.startswith(ADAPTIVE) and len(runs) > 1:
            states = [evaluate(verify(graph_for(STORE, r["root_run"], runs[:k]), SPEC, vcfg)) for k in range(1, len(runs))]
            states.append(ev)
            loop = {"n_states": len(states), "first_decisive": first_decisive(states),
                    "cases_per_state": {n: [s["variants"][n]["case"] for s in states] for n in VARIANTS}}
            # the recorded loop continued, so V0 must have been INCONCLUSIVE at every state before the last
            early = [k for k, s in enumerate(states[:-1]) if s["variants"]["V0"]["case"] != "INCONCLUSIVE"]
            if early:
                mismatches.append(f"{where}: V0 decisive at intermediate state(s) {early} although the loop continued")
        cases.append({"group": group, "system": system, "case": case, "root_run": r["root_run"], "n_runs": len(runs),
                      "stored_verdict": old.get("verdict"), "final_verdict": r.get("final_verdict"),
                      "stale": stale, **{view: tv[view] for view in VIEWS},
                      "setup_problems": tv["setup_problems"], "setup_departures": tv["setup_departures"],
                      "true_errors": tv["errors"], "truth_notes": tv["notes"],
                      "failed_checks": v.failed_checks, "gates_blocking": ev["gates_blocking"],
                      **{n: ev["variants"][n]["case"] for n in VARIANTS}, "loop": loop})
        for q in QS:
            comp = components(v, q)
            us = [(k, c.uncertainty, (c.details or {}).get("kind")) for k, c in comp.items()
                  if c is not None and c.uncertainty is not None]
            bias = sum(u for _, u, kind in us if kind == "bias")
            rss = math.sqrt(sum(u * u for _, u, kind in us if kind != "bias"))
            e = tv["errors"][q]
            row = {"group": group, "system": system, "case": case, "quantity": q, "tau": TAU[q],
                   "component_status": {k: (c.status.value if c else "MISSING") for k, c in comp.items()},
                   "component_uncertainty": {k: c.uncertainty for k, c in comp.items() if c and c.uncertainty is not None},
                   "blocking_V0": {k: reason_class(c) for k, c in comp.items() if c is None or c.status != Status.PASS},
                   "u_available": bias + rss, "components_without_estimate": [k for k, c in comp.items()
                                                                              if c is None or c.uncertainty is None],
                   "true_error": e, "error_source": tv["error_source"]}
            for n in VARIANTS:
                d = ev["variants"][n]["per_qoi"][q]
                row[n] = d["verdict"]
                row[f"combined_{n}"] = d["combined_uncertainty"]
                row[f"flag_{n}"] = flag(d["verdict"], e, TAU[q])
            rows.append(row)

    roots = {}
    for c in cases:
        if c["group"] == "attacks":
            roots.setdefault(c["case"], set()).add(c["root_run"])
    truth_mismatches += [f"attacks/{cid}: root runs differ between systems: {sorted(rs)}" for cid, rs in roots.items()
                         if len(rs) > 1]
    summary = summarize(rows, cases)
    blockers = blocking_table(rows, cases)
    present = {(c["system"], c["case"]) for c in cases if c["group"] == "benchmark"}
    present |= {(s["system"], s["case"]) for s in skipped if s["group"] == "benchmark"}
    missing = {s: [cid for cid in LABELS["cases"] if (s, cid) not in present]
               for s in dict.fromkeys(c["system"] for c in cases if c["group"] == "benchmark")}
    doc = {"status": TAG, "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "decision_code": fp, "tau": TAU, "component_pass_fraction": frac,
           "rule_V0": "component PASS: U <= component_pass_fraction*tau (averaging bias: b <= tau); quantity ACCEPT: "
                      "all five components PASS and bias + RSS(others) <= tau; quantity REJECT: any component FAIL; "
                      "case ACCEPT: no FAIL, gates pass or are discharged, every quantity ACCEPT",
           "criterion_u_only": "component status INCONCLUSIVE with CheckResult.uncertainty not None "
                               "(sensitivity.assess_sequence last branch; static.check_statistics u > tau/2 branch)",
           "variants": {n: VARIANT_NAMES[n] for n in VARIANTS},
           "label_views": VIEWS,
           "label_views_note": "benchmark cases: narrow reading only (benchmark/labels.json), label_literal and "
                               "label_setup_reading are null and not counted; summary counts in those two views are "
                               "over attack cases only",
           "attack_setup_departures": ATTACK_SETUP_DEPARTURES,
           "v0_mismatches": mismatches, "criterion_anomalies": anomalies, "truth_mismatches": truth_mismatches,
           "skipped": skipped, "benchmark_results_not_stored": {s: m for s, m in missing.items() if m},
           "summary": summary, "blocking_V0": blockers, "gates_V0_inconclusive": gate_table(cases),
           "gate_only": gate_only(rows, cases), "cases": cases, "rows": rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "acceptance_rule.json").write_text(json.dumps(doc, indent=1, default=str))
    (OUT / "acceptance_rule.md").write_text(markdown(doc))
    print_summary(doc)
    return 1 if (mismatches or anomalies or truth_mismatches) else 0


def summarize(rows: list[dict], cases: list[dict]) -> dict:
    """Per (group, system), per group and overall, per variant: case-level and quantity-level acceptance counts
    (stale results excluded).  Label counts per view are over the cases labelled in that view (VIEWS)."""
    out = {}
    stale = {(c["group"], c["system"], c["case"]) for c in cases if c["stale"]}
    keys = list(dict.fromkeys((c["group"], c["system"]) for c in cases))
    keys += [(g, "all") for g in dict.fromkeys(c["group"] for c in cases)] + [("all", "all")]
    for g, s in keys:
        def sel(x, g=g, s=s):
            return g in ("all", x["group"]) and s in ("all", x["system"])
        cs = [c for c in cases if sel(c) and (c["group"], c["system"], c["case"]) not in stale]
        rs = [r for r in rows if sel(r) and (r["group"], r["system"], r["case"]) not in stale]
        d = {"n_results": len(cs), "n_stale_excluded": sum(1 for c in cases if sel(c) and c["stale"])}
        for view in VIEWS:
            d[f"n_labelled[{view}]"] = sum(1 for c in cs if c[view] is not None)
            d[f"n_credible[{view}]"] = sum(1 for c in cs if c[view] == "credible")
            d[f"n_flawed[{view}]"] = sum(1 for c in cs if c[view] == "flawed")
        for n in VARIANTS:
            acc = [c for c in cs if c[n] == "ACCEPT"]
            qa = [r for r in rs if r[n] == "ACCEPT"]
            d[n] = {"cases_accept": len(acc),
                    "cases_accept_review_not_run": sum(1 for c in acc if c["system"] in REVIEW_SYSTEMS),
                    **{f"correct_accept[{view}]": sum(1 for c in acc if c[view] == "credible") for view in VIEWS},
                    **{f"false_accept_case[{view}]": sum(1 for c in acc if c[view] == "flawed") for view in VIEWS},
                    **{f"ambiguous_accept[{view}]": sum(1 for c in acc if c[view] == "ambiguous") for view in VIEWS},
                    "quantities_accept": len(qa),
                    "quantities_accept_err_gt_tau": sum(1 for r in qa if r["true_error"] is not None and abs(r["true_error"]) > r["tau"]),
                    "quantities_accept_err_gt_half_tau": sum(1 for r in qa if r["true_error"] is not None
                                                             and abs(r["true_error"]) > 0.5 * r["tau"]),
                    "loop_first_decisive_accept": sum(1 for c in cs if c["loop"] and c["loop"]["first_decisive"][n]["verdict"] == "ACCEPT"),
                    "loop_first_decisive_accept_flawed[label]": sum(
                        1 for c in cs if c["loop"] and c["loop"]["first_decisive"][n]["verdict"] == "ACCEPT" and c["label"] == "flawed")}
        out[f"{g}/{s}"] = d
    return out


BLOCK_COLUMNS = [(g, k) for g in ("benchmark", "attacks") for k in ("single run", "with experiments")]


def blocking_table(rows: list[dict], cases: list[dict]) -> list[dict]:
    """Why quantities are not ACCEPTed under V0: INCONCLUSIVE quantities of INCONCLUSIVE cases (a REJECTed case
    is not blocked from acceptance by its components), by blocking pattern.  'single run' = B, B-v1, B-v2."""
    inconclusive = {(c["group"], c["system"], c["case"]) for c in cases if c["V0"] == "INCONCLUSIVE"}
    cnt = Counter()
    for r in rows:
        if r["V0"] != "INCONCLUSIVE" or (r["group"], r["system"], r["case"]) not in inconclusive:
            continue
        pat = " + ".join(f"{k}: {why}" for k, why in r["blocking_V0"].items()) or "all components PASS, U_total > tau"
        kind = "single run" if r["system"] in ("B", "B-v1", "B-v2") else "with experiments"
        cnt[(pat, r["group"], kind)] += 1
    pats = sorted({p for p, _, _ in cnt}, key=lambda p: (-sum(cnt[(p, g, k)] for g, k in BLOCK_COLUMNS
                                                              if k == "with experiments"),
                                                         -sum(cnt[(p, g, k)] for g, k in BLOCK_COLUMNS), p))
    return [{"pattern": p, **{f"{g}, {k}": cnt[(p, g, k)] for g, k in BLOCK_COLUMNS}} for p in pats]


def gate_table(cases: list[dict]) -> dict:
    """{gate result: [group/system/case]} over V0-INCONCLUSIVE cases whose gate checks are not passed or
    discharged (a case can hold more than one gate)."""
    out = {}
    for c in cases:
        if c["V0"] == "INCONCLUSIVE":
            for gt in c["gates_blocking"]:
                out.setdefault(gt, []).append(f"{c['group']}/{c['system']}/{c['case']}")
    return dict(sorted(out.items(), key=lambda kv: (-len(kv[1]), kv[0])))


def gate_only(rows: list[dict], cases: list[dict]) -> dict:
    """Per variant: cases without a FAIL whose quantities are all ACCEPT but whose case verdict is held by a gate."""
    out = {}
    for n in VARIANTS:
        out[n] = [f"{c['group']}/{c['system']}/{c['case']} ({', '.join(c['gates_blocking'])})" for c in cases
                  if c[n] != "ACCEPT" and not c["failed_checks"] and c["gates_blocking"]
                  and all(r[n] == "ACCEPT" for r in rows if (r["group"], r["system"], r["case"])
                          == (c["group"], c["system"], c["case"]))]
    return out


def findings(doc: dict) -> list[str]:
    """One line per variant, generated from the rows (final graphs, stale results excluded)."""
    out = []
    stale = {(c["group"], c["system"], c["case"]) for c in doc["cases"] if c["stale"]}
    for n in VARIANTS:
        acc = [c for c in doc["cases"] if c[n] == "ACCEPT" and (c["group"], c["system"], c["case"]) not in stale]
        by_label = Counter(f"{c['label']} / {c['label_point_estimate']}" for c in acc)
        bad = [r for r in doc["rows"] if r[n] == "ACCEPT" and r["true_error"] is not None and abs(r["true_error"]) > r["tau"]
               and (r["group"], r["system"], r["case"]) not in stale]
        early = [c for c in doc["cases"] if c["loop"] and c["loop"]["first_decisive"][n]["verdict"] == "ACCEPT"
                 and c["loop"]["first_decisive"][n]["n_experiments"] < c["loop"]["n_states"] - 1]
        s = (f"- **{n} ({VARIANT_NAMES[n]})**: {len(acc)} case ACCEPT"
             + (" (" + "; ".join(f"{c['system']}/{c['case']}" for c in acc) + "; narrow labels with mitigation / "
                "point estimate: " + ", ".join(f"{k} ×{v}" for k, v in by_label.items()) + ")" if acc else "")
             + f". Quantity ACCEPTs with |e| > τ: {len(bad)}"
             + (" (" + "; ".join(f"{r['system']}/{r['case']} {SHORT[r['quantity']]} {pct(r['true_error'], True)}"
                                 for r in bad) + ")" if bad else "")
             + ".")
        if early:
            s += (" In " + ", ".join(f"{c['system']}/{c['case']}" for c in early)
                  + " the recorded loop passes a state this rule ACCEPTs before its last experiment.")
        review = sorted({c["case"] for c in acc if c["system"] in REVIEW_SYSTEMS})
        if review:
            s += (f" For {', '.join(REVIEW_SYSTEMS)} ({', '.join(review)}) the ACCEPT is the verifier's; the acceptance "
                  "review was not run on it, so that system's final verdict under this rule is unknown.")
        out.append(s)
    return out + config_lines(doc, stale)


def config_lines(doc: dict, stale: set) -> list[str]:
    """Which verification configuration the false case acceptances come from, and what v2 does on the same cases
    (FAILs and gates are the same in every variant)."""
    false = [c for c in doc["cases"] if (c["group"], c["system"], c["case"]) not in stale
             and any(c[n] == "ACCEPT" for n in VARIANTS) and "flawed" in (c["label"], c["label_setup_reading"])]
    if not false:
        return []
    v2 = [c for c in doc["cases"] if c["group"] == "attacks" and c["system"].endswith("v2") and c["setup_departures"]]
    v1_only = all(not c["system"].endswith("v2") for c in false)
    s = ("- All false case acceptances occur with verification v1 (`configs/verification.yaml`)" if v1_only
         else "- False case acceptances occur with verification v2 as well: "
         + "; ".join(f"{c['system']}/{c['case']}" for c in false if c["system"].endswith("v2")))
    if v2 and all(c[n] == "REJECT" for c in v2 for n in VARIANTS):
        by_case = {}
        for c in v2:
            by_case.setdefault(c["case"], set()).update(c["failed_checks"])
        s += (". With v2 the static " + " and ".join(f"{', '.join(sorted(f))} ({cid.split('_')[0]})"
                                                    for cid, f in by_case.items())
              + " checks FAIL, so " + " and ".join(sorted({c["system"] for c in v2})) + " REJECT "
              + " and ".join(cid.split("_")[0] for cid in by_case) + " under every variant. These v2 checks were "
              "committed in 8161f5c (2026-10-19 07:40) before the attacks ran, but are post-hoc extensions of the "
              "pre-registered verifier (`configs/verification_v2.yaml` line 1): their detections of "
              + " and ".join(cid.split("_")[0] for cid in by_case) + " are not blind tests")
        # a REJECT is correct only where the case is flawed; for a case flawed only under the set-up reading say so
        not_flawed = sorted({c["case"].split("_")[0] for c in v2 if c["label"] != "flawed"})
        if not_flawed:
            s += (". The " + " and ".join(not_flawed) + " REJECTs are correct only under the set-up reading: under the "
                  "narrow reading they are false rejections on point estimates and not scored with the mitigation "
                  "(ambiguous under the literal reading too)")
    elif v2:
        s += (". With v2: " + "; ".join(f"{c['system']}/{c['case']} " + " / ".join(c[n] for n in VARIANTS)
                                         for c in v2))
    return [s + "."]


def pct(x, signed: bool = False) -> str:
    return "—" if x is None else (f"{x:+.2%}" if signed else f"{x:.2%}")


def markdown(doc: dict) -> str:
    tau = doc["tau"]
    L = ["# Acceptance rule: what blocks acceptance, and what a looser rule would accept",
         "",
         f"**{doc['status']}.** No new simulation; decision code unchanged (fingerprint `{doc['decision_code']}`). "
         f"Generated by `scripts/posthoc_acceptance_rule.py` on {doc['created']}.",
         "",
         "## Rules compared",
         "",
         f"Tolerance τ = {', '.join(f'{SHORT[q]} {t:.0%}' for q, t in tau.items())}; component pass limit "
         f"{doc['component_pass_fraction']:g} τ = τ/2.",
         "",
         "- **V0, pre-registered** (`checks/verifier.aggregate`). Per quantity, each component (averaging, statistics, "
         "mesh, time, domain) must PASS: a mesh, time, domain or statistics component passes when its estimated "
         "relative uncertainty U ≤ τ/2; the averaging bias b passes when b ≤ τ (and FAILs above). The quantity is "
         "ACCEPT when every component passes and U_total = bias + RSS(other components) ≤ τ, REJECT when any component "
         "FAILs, INCONCLUSIVE otherwise. The case is ACCEPT when no check FAILs, every gate check passes or is "
         "discharged (Courant concern by a time PASS, first-order-scheme concern by a mesh PASS, for every quantity), "
         "and every quantity is ACCEPT.",
         "- **V1, combined only.** A component that is INCONCLUSIVE only because U > τ/2 counts as measured; its U "
         "enters bias + RSS. ACCEPT when no component is FAIL, missing or unresolved for another reason, and "
         "bias + RSS ≤ τ.",
         "- **V2, domain relaxed.** As V0, but the τ/2 limit is dropped for the domain component only.",
         "",
         "Gate checks, FAIL criteria and the gate discharge rule are the same in all three; the variants change only "
         "which component results count as measured. Each variant is computed by the decision code's own `aggregate()` "
         "on copies of the replayed checks in which the relaxed component results are marked PASS.",
         "",
         "**Criterion for 'INCONCLUSIVE only because U > τ/2'**: status INCONCLUSIVE with a numerical uncertainty "
         "attached. In the current decision code only two branches return that: the last branch of "
         "`sensitivity.assess_sequence` (U_root > τ/2 and the demonstrated change does not exceed τ by more than twice "
         "the statistical noise) and the u > τ/2 branch of `static.check_statistics`. Every other INCONCLUSIVE component result carries no uncertainty (no experiment, "
         "family member not statistically reliable, divergent sequence, no positive observed order, degenerate family, "
         "unknown temporal order, value missing, steady solver, too few cycles, unreliable averaging reference) and "
         "still blocks under V1 and V2. "
         + (f"Exceptions found: {len(doc['criterion_anomalies'])} (listed below)." if doc["criterion_anomalies"]
            else "Every result treated this way has U above its threshold (checked)."),
         "",
         "True error e = (reported − T)/T against the in-house reference T (benchmark: `benchmark/labels.json`; "
         "attacks: the root run's `qoi.reported` against the same T).",
         "",
         "**Labels.** Benchmark cases use both label views of `benchmark/labels.json` (with the truth-uncertainty "
         "mitigation / point estimates). These apply the narrow reading of the set-up clause of `docs/design.md` "
         "section 19: only set-up problems detected from the evidence (wrong Re, steady formulation) and missing "
         "quantities count; every other departure is judged by its error. Attack labels are computed as "
         "`scripts/analyze_benchmark.py` computes them for `results/benchmark/metrics.json`, in three readings: "
         "narrow (as the benchmark), literal (credible needs 'the set-up is consistent'; flawed needs e > τ or a "
         "set-up that 'answers a different problem (wrong Re or regime)') and set-up (any departure from the problem "
         "statement makes the case flawed). The counts below use the narrow views; false acceptances under the "
         "set-up reading are an extra column.",
         "",
         "| attack | Cd error | St error | departure from the problem statement | narrow, with mitigation | "
         "narrow, point estimate | literal | set-up reading |",
         "|---|---|---|---|---|---|---|---|"]
    att = list({c["case"]: c for c in doc["cases"] if c["group"] == "attacks"}.values())
    L += [f"| {c['case']} | {pct(c['true_errors'][QS[0]], True)} | {pct(c['true_errors'][QS[1]], True)} | "
          f"{'; '.join(c['setup_departures']) or '— (mesh and domain size only)'} | "
          + " | ".join(c[view] for view in VIEWS) + " |" for c in att]
    by_err = [c["case"].split("_")[0] for c in att if c["label"] == "flawed" and not c["setup_problems"]]
    setup_only = [c for c in att if c["label_setup_reading"] == "flawed" and c["label"] != "flawed"]
    acc_setup_only = [f"{c['system']}/{c['case']}" for c in doc["cases"] if c["group"] == "attacks"
                      and c["case"] in {x["case"] for x in setup_only} and any(c[n] == "ACCEPT" for n in VARIANTS)]
    L += ["", f"{' and '.join(by_err)} {'is' if len(by_err) == 1 else 'are'} flawed by {'its' if len(by_err) == 1 else 'their'} "
          "error in every reading (no set-up problem is detected from the evidence), so an acceptance of "
          f"{'it' if len(by_err) == 1 else 'either'} is a false acceptance in every reading."
          + "".join(f" {c['case'].split('_')[0]} is flawed only under the set-up reading ({c['setup_departures'][0]}); "
                    f"under the narrow reading used by `benchmark/labels.json` and `metrics.json` it is {c['label']} with "
                    f"mitigation and {c['label_point_estimate']} on point estimates, and {c['label_literal']} under the "
                    "literal reading." for c in setup_only)
          + (" No variant accepts " + " or ".join(f"the {c['case'].split('_')[0]} case" for c in setup_only) + "."
             if setup_only and not acc_setup_only else
             (" Accepted under some variant: " + "; ".join(acc_setup_only) + "." if acc_setup_only else "")),
          "",
          "## Findings",
          "",
          *findings(doc),
          "",
          "## Reproduction of the stored verdicts (V0)",
          ""]
    n_res = len(doc["cases"])
    if doc["v0_mismatches"]:
        L += [f"**{len(doc['v0_mismatches'])} mismatch(es)** between V0 and the stored verdicts:", ""]
        L += [f"- {m}" for m in doc["v0_mismatches"]]
    else:
        L += [f"V0 reproduces the stored case verdict, per-quantity verdict and combined U of all {n_res} results. "
              "For adaptive results V0 is INCONCLUSIVE at every intermediate state of the recorded loop, as it must be "
              "for the loop to have continued."]
    if doc["truth_mismatches"]:
        L += ["", f"**{len(doc['truth_mismatches'])} disagreement(s) with `benchmark/labels.json`** (true errors or "
              "root runs):", ""] + [f"- {m}" for m in doc["truth_mismatches"]]
    else:
        L += ["", "True errors and root runs of the benchmark results agree with `benchmark/labels.json` (checked)."]
    stale = [c for c in doc["cases"] if c["stale"]]
    if stale:
        L += ["", "Stale benchmark results (excluded from the counts): "
              + "; ".join(f"{c['system']}/{c['case']} ({c['stale']})" for c in stale)]
    if doc["skipped"]:
        L += ["", "Not evaluated: " + "; ".join(f"{s['group']}/{s['system']}/{s['case']} ({s['reason']})"
                                               for s in doc["skipped"])]
    if doc["benchmark_results_not_stored"]:
        L += ["", "Benchmark cases without a stored final result at the time of this run (not counted): "
              + "; ".join(f"{s}: {', '.join(m)}" for s, m in doc["benchmark_results_not_stored"].items()) + "."]
    if doc["criterion_anomalies"]:
        L += ["", "Criterion exceptions:", ""] + [f"- {a}" for a in doc["criterion_anomalies"]]

    L += ["", "## Summary per variant", "",
          "Counts over the final evidence graph of each stored result. 'correct' = credible case ACCEPTed; "
          "'false' = flawed case ACCEPTed; 'ambig.' = ambiguous case ACCEPTed (not scored). Each correct/false cell "
          "gives 'with mitigation · point estimate' in the narrow reading, each as ACCEPTed/labelled; 'ambig.' gives "
          "'with mitigation · point estimate'. 'false, set-up reading' counts flawed cases ACCEPTed under the set-up "
          "reading, over attack cases only (benchmark labels use the narrow reading: —). Quantity columns count "
          "quantity-level ACCEPTs and those whose true error exceeds τ or τ/2 (the τ/2 count includes the τ count). "
          "'loop ACCEPT' counts adaptive results whose recorded loop passes through a state the variant ACCEPTs (see "
          "the last section); '(flawed)' uses the narrow label with mitigation. All verdicts here are the "
          "deterministic verifier's. ¹ " + ", ".join(REVIEW_SYSTEMS) + ": a verifier ACCEPT would go to the acceptance "
          "review, which was not run on these states, so the system's final verdict under V1 or V2 is unknown; its "
          "case ACCEPTs are counted as verifier ACCEPTs.", ""]
    for n in VARIANTS:
        L += [f"### {n}: {VARIANT_NAMES[n]}", "",
              "| group / system | results | cases ACCEPT | correct | false (verifier) | false, set-up reading | ambig. | "
              "quantities ACCEPT | of which abs. error > τ | abs. error > τ/2 | loop ACCEPT (flawed) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for key, d in doc["summary"].items():
            x = d[n]
            g, s = key.split("/", 1)
            name = ("**all**" if key == "all/all" else f"**{g}, all**" if s == "all"
                    else key + (" ¹" if s in REVIEW_SYSTEMS else ""))
            sv = "label_setup_reading"
            setup = (f"{x[f'false_accept_case[{sv}]']}/{d[f'n_flawed[{sv}]']}" if d[f"n_labelled[{sv}]"] else "—")
            L.append(f"| {name} | {d['n_results']} | {x['cases_accept']} | "
                     f"{x['correct_accept[label]']}/{d['n_credible[label]']} · "
                     f"{x['correct_accept[label_point_estimate]']}/{d['n_credible[label_point_estimate]']} | "
                     f"{x['false_accept_case[label]']}/{d['n_flawed[label]']} · "
                     f"{x['false_accept_case[label_point_estimate]']}/{d['n_flawed[label_point_estimate]']} | {setup} | "
                     f"{x['ambiguous_accept[label]']} · {x['ambiguous_accept[label_point_estimate]']} | "
                     f"{x['quantities_accept']} | {x['quantities_accept_err_gt_tau']} | "
                     f"{x['quantities_accept_err_gt_half_tau']} | {x['loop_first_decisive_accept']} "
                     f"({x['loop_first_decisive_accept_flawed[label]']}) |")
        L.append("")
    if doc["summary"]["all/all"]["n_credible[label]"] == 0:
        L += ["With the truth-uncertainty mitigation no evaluated case is labelled credible, so 'correct' is 0/0 in "
              "that view; the point-estimate view has credible cases.", ""]

    L += ["## What blocks acceptance under V0", "",
          "INCONCLUSIVE quantities of cases whose V0 verdict is INCONCLUSIVE (in a REJECTed case the components do not "
          "decide the outcome), by the set of components that do not PASS. 'U>tau/2' = INCONCLUSIVE only because U "
          "exceeds τ/2. 'single run' = B, B-v1, B-v2 (no experiments by design); 'with experiments' = C-*, Bexh.", "",
          "| blocking components | " + " | ".join(f"{g}, {k}" for g, k in BLOCK_COLUMNS) + " |",
          "|---|" + "---|" * len(BLOCK_COLUMNS)]
    L += [f"| {b['pattern']} | " + " | ".join(str(b[f'{g}, {k}']) for g, k in BLOCK_COLUMNS) + " |"
          for b in doc["blocking_V0"]]
    incl = {(c["group"], c["system"], c["case"]) for c in doc["cases"] if c["V0"] == "INCONCLUSIVE"}
    only_u = [r for r in doc["rows"] if r["V0"] == "INCONCLUSIVE" and r["blocking_V0"]
              and all(w == "U>tau/2" for w in r["blocking_V0"].values())]
    only_dom = [r for r in only_u if list(r["blocking_V0"]) == ["domain"]]
    L += ["", f"Over all results, {len(only_u)} V0-INCONCLUSIVE quantities are blocked only by components with U > τ/2 "
              f"({sum((r['group'], r['system'], r['case']) in incl for r in only_u)} of them in INCONCLUSIVE cases); "
              f"{sum(r['V1'] == 'ACCEPT' for r in only_u)} of these become ACCEPT under V1, the others have "
              f"bias + RSS > τ. {len(only_dom)} are blocked only by the domain component; "
              f"{sum(r['V2'] == 'ACCEPT' for r in only_dom)} of these become ACCEPT under V2.", ""]
    gt = doc["gates_V0_inconclusive"]
    held = {x for v in gt.values() for x in v}
    L += [f"**Gates.** {len(held)} V0-INCONCLUSIVE cases also hold a gate check that is neither passed nor "
          "discharged" + (": " + "; ".join(f"{g} {len(v)} ({', '.join(x.split('/', 1)[1] for x in v)})"
                                          for g, v in gt.items()) + ". A case can hold more than one gate" if gt else "")
          + ". "
          + ("No case has all quantities ACCEPT under " + ", ".join(list(VARIANTS)[:-1]) + " or " + list(VARIANTS)[-1]
             + " while held by a gate: every gate-held case also has a quantity that is not ACCEPT under each variant, "
             "so it has component blockers as well."
             if not any(doc["gate_only"].values()) else
             "Cases whose quantities are all ACCEPT but whose case verdict is held by a gate: "
             + "; ".join(f"{n}: {', '.join(v)}" for n, v in doc["gate_only"].items() if v) + "."), ""]

    case_of = {(c["group"], c["system"], c["case"]): c for c in doc["cases"]}
    L += ["## Quantity rows that change", "",
          "'case V0 / V1 / V2' is the case verdict; a quantity ACCEPT in a REJECTed or INCONCLUSIVE case is counted in "
          "the quantity columns of the summary but does not accept the case.", "",
          "| group | system | case | qty | V0 | V1 | V2 | U_total (V1) | V0 blocking (U) | true error | flag | "
          "case V0 / V1 / V2 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in doc["rows"]:
        if r["V1"] == r["V0"] and r["V2"] == r["V0"]:
            continue
        blk = ", ".join(f"{k} {why}" + (f" {pct(r['component_uncertainty'][k])}" if k in r["component_uncertainty"] else "")
                        for k, why in r["blocking_V0"].items())
        fl = r["flag_V1"] or r["flag_V2"]
        c = case_of[(r["group"], r["system"], r["case"])]
        L.append(f"| {r['group']} | {r['system']} | {r['case']} | {SHORT[r['quantity']]} | {r['V0']} | {r['V1']} | "
                 f"{r['V2']} | {pct(r['combined_V1'])} | {blk} | {pct(r['true_error'], True)} | "
                 f"{'**' + fl + '**' if fl else ''} | {c['V0']} / {c['V1']} / {c['V2']} |")

    L += ["", "## Case rows that change", "",
          "| group | system | case | label (narrow: mitig. / point; set-up reading) | V0 | V1 | V2 | gates blocking | "
          "failed checks |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c in doc["cases"]:
        if c["V1"] == c["V0"] and c["V2"] == c["V0"]:
            continue
        lab = f"{c['label']} / {c['label_point_estimate']}" + (f"; {c['label_setup_reading']}"
                                                               if c["label_setup_reading"] else "")
        L.append(f"| {c['group']} | {c['system']} | {c['case']} | {lab} | {c['V0']} | "
                 f"{c['V1']} | {c['V2']} | {', '.join(c['gates_blocking']) or '—'} | {', '.join(c['failed_checks']) or '—'} |")

    L += ["", "## ACCEPTs with true error above τ/2 (all variants, final graphs)", "",
          "| group | system | case | qty | V0 | V1 | V2 | true error | case V0 / V1 / V2 |", "|---|---|---|---|---|---|---|---|---|"]
    for r in doc["rows"]:
        if any(r[f"flag_{n}"] for n in VARIANTS):
            c = case_of[(r["group"], r["system"], r["case"])]
            L.append(f"| {r['group']} | {r['system']} | {r['case']} | {SHORT[r['quantity']]} | {r['V0']} | {r['V1']} | "
                     f"{r['V2']} | {pct(r['true_error'], True)} | {c['V0']} / {c['V1']} / {c['V2']} |")

    L += ["", "## Adaptive loops: first state at which each rule is decisive", "",
          "An adaptive loop stops at the first decisive verdict. The table lists adaptive results in which a variant is "
          "decisive at an earlier state of the recorded loop than V0, or with a different verdict ('state k' = root "
          "plus the first k experiments; the recorded loop ran to state n). This assumes the planner would have chosen "
          "the same experiments under the variant, which is not guaranteed. For C-llm-v1+review an ACCEPT would go to "
          "the acceptance review.", "",
          "| group | system | case | label (narrow, mitig.) | n | V0 | V1 | V2 |", "|---|---|---|---|---|---|---|---|"]
    for c in doc["cases"]:
        lp = c["loop"]
        if not lp:
            continue
        fd = lp["first_decisive"]
        if all(fd[n] == fd["V0"] for n in VARIANTS):
            continue
        cell = {n: fd[n]["verdict"] + ("" if fd[n]["n_experiments"] is None else f" at state {fd[n]['n_experiments']}")
                for n in VARIANTS}
        L.append(f"| {c['group']} | {c['system']} | {c['case']} | {c['label']} | {lp['n_states'] - 1} | {cell['V0']} | "
                 f"{cell['V1']} | {cell['V2']} |")

    L += ["", "## Examples", ""]
    for g, s, cid in (("attacks", "C-rule-v1", "X1_cylinder_geometry"), ("benchmark", "C-rule", "baseline")):
        rs = [r for r in doc["rows"] if (r["group"], r["system"], r["case"]) == (g, s, cid)]
        if not rs:
            continue
        parts = []
        for r in rs:
            blk = ", ".join(f"{k} {why}" + (f" (U = {pct(r['component_uncertainty'][k])})" if k in r["component_uncertainty"] else "")
                            for k, why in r["blocking_V0"].items())
            parts.append(f"{SHORT[r['quantity']]}: V0 {r['V0']}" + (f", U_total {pct(r['combined_V0'])}" if r["combined_V0"] is not None else "")
                         + (f", blocked by {blk}" if blk else "") + f"; V1 {r['V1']}"
                         + (f" (U_total {pct(r['combined_V1'])})" if r["combined_V1"] is not None else "")
                         + f"; V2 {r['V2']}; true error {pct(r['true_error'], True)}")
        c = case_of[(g, s, cid)]
        L.append(f"- **{s} / {cid}** ({c['label']}): " + ". ".join(parts) + f". Case: V0 {c['V0']}, V1 {c['V1']}, V2 {c['V2']}.")
    L.append("")
    return "\n".join(L)


def print_summary(doc: dict) -> None:
    print(f"{len(doc['cases'])} results, {len(doc['rows'])} quantity rows; {len(doc['v0_mismatches'])} V0 mismatch(es), "
          f"{len(doc['criterion_anomalies'])} criterion exception(s), {len(doc['truth_mismatches'])} label mismatch(es), "
          f"{len(doc['skipped'])} skipped")
    for m in doc["v0_mismatches"] + doc["criterion_anomalies"] + doc["truth_mismatches"]:
        print("  ", m)
    for n in VARIANTS:
        a, d = doc["summary"]["all/all"][n], doc["summary"]["all/all"]
        sv = "label_setup_reading"
        print(f"{n} ({VARIANT_NAMES[n]}): cases ACCEPT {a['cases_accept']}; narrow mitigation / point: correct "
              f"{a['correct_accept[label]']}/{d['n_credible[label]']} / "
              f"{a['correct_accept[label_point_estimate]']}/{d['n_credible[label_point_estimate]']}, false "
              f"{a['false_accept_case[label]']}/{d['n_flawed[label]']} / "
              f"{a['false_accept_case[label_point_estimate]']}/{d['n_flawed[label_point_estimate]']}; set-up reading "
              f"(attacks) false {a[f'false_accept_case[{sv}]']}/{d[f'n_flawed[{sv}]']}; quantities ACCEPT "
              f"{a['quantities_accept']}, |e|>tau {a['quantities_accept_err_gt_tau']}, |e|>tau/2 "
              f"{a['quantities_accept_err_gt_half_tau']}; loop ACCEPT {a['loop_first_decisive_accept']}")


if __name__ == "__main__":
    sys.exit(main())
