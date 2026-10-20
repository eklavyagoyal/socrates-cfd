"""Post-hoc tests of the LLM acceptance review (veto-only; not part of the pre-registered protocol).

The review (orchestration/loop.py, LLMPlanner.review) is only invoked on a deterministic ACCEPT. None occurred in the
attack phase or in the first C-llm run, so it was never exercised there. This script tests it in two ways:

1. **Real ACCEPTs** (C-llm-r2 on K2_fine_large, C-llm-r3 on baseline): `systems.review_only` on the stored graph. A
   veto here would be a false veto (both acceptances are correct on point estimates).
2. **Counterfactual X1 ACCEPT** (C-llm-v1 and C-rule-v1 graphs of attack X1, cylinder 5 % too large): the verdict the
   post-hoc combined-only rule V1 (`scripts/posthoc_acceptance_rule.py`) would give, made self-consistent by setting
   every check that is INCONCLUSIVE only because its U exceeds tau/2 to PASS. A concur here is a false acceptance.

Default mode does not call the LLM: it rebuilds each review's evidence package exactly as `LLMPlanner.review` builds it
and writes it with its sha256 and, for X1, the number of occurrences of the measured cylinder extent (0.0105 m), so the
package the review saw can be inspected. `--call` asks the LLM again and writes the review results. The stored results
in results/posthoc/review-on-accepts/*.json (2026-10-20 ~14:35 UTC) were produced by the same code run inline before
this script existed; LLM outputs are not deterministic, so a new --call can differ.

    python scripts/posthoc_review_tests.py           # rebuild and save the packages (no LLM call)
    python scripts/posthoc_review_tests.py --call    # also re-run the reviews (LLM cost ~USD 0.3 each)
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

import replay_verdicts as rv  # noqa: E402  (stored(): the runs of a result; V1: verification.yaml)
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.base import Status  # noqa: E402
from socrates.checks.verifier import verify  # noqa: E402
from socrates.critic.prompt import alias_map, anonymize, build_package, render_user_prompt  # noqa: E402
from socrates.orchestration.loop import LLMPlanner, graph_for  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.systems import review_only  # noqa: E402

OUT = REPO / "results" / "posthoc" / "review-on-accepts"
REAL = [("benchmark", "C-llm-r2", "K2_fine_large"), ("benchmark", "C-llm-r3", "baseline")]
COUNTERFACTUAL = [("attacks", "C-llm-v1", "X1_cylinder_geometry"), ("attacks", "C-rule-v1", "X1_cylinder_geometry")]
MEASURED_EXTENT = "0.0105"


def review_package(spec, graph, verdict, history) -> str:
    """The user prompt LLMPlanner.review sends, built the same way (loop.py, LLMPlanner.review)."""
    package = anonymize(build_package(spec, graph, verdict, history, [], {"note": "review only; no experiments"}),
                        alias_map(graph))
    package.pop("experiment_menu", None)
    return render_user_prompt(package)


def counterfactual_accept(verdict):
    """The V1 (combined-only) verdict on the same graph, made self-consistent. Returns the relaxed checks."""
    relaxed = []
    for c in verdict.checks:
        if c.status == Status.INCONCLUSIVE and c.uncertainty is not None and c.component in ("mesh", "time", "domain", "statistics"):
            c.status = Status.PASS
            relaxed.append(f"{c.check}[{c.qoi}] U={c.uncertainty:.4f}")
    for d in verdict.per_qoi.values():
        d["verdict"] = "ACCEPT"
        d["component_status"] = {k: "PASS" for k in d["component_status"]}
        u = d["component_uncertainty"]
        d["combined_uncertainty"] = sum(x * x for k, x in u.items() if k != "averaging") ** 0.5 + u.get("averaging", 0.0)
    verdict.verdict, verdict.missing_components = "ACCEPT", {}
    blocking = [c.check for c in verdict.checks if c.status in (Status.FAIL, Status.INCONCLUSIVE)]
    if blocking:  # a FAIL or a gate is not relaxed by V1: then there is no counterfactual ACCEPT to review
        raise SystemExit(f"counterfactual ACCEPT impossible, blocking checks remain: {blocking}")
    return relaxed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--call", action="store_true", help="re-run the LLM reviews (costs money; nondeterministic)")
    a = ap.parse_args()
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    OUT.mkdir(parents=True, exist_ok=True)
    for kind, tests in (("real", REAL), ("counterfactual", COUNTERFACTUAL)):
        for group, system, case in tests:
            r = json.loads((REPO / "results" / group / system / f"{case}.json").read_text())
            _, runs = rv.stored(system, r)
            g = graph_for(store, r["root_run"], runs)
            v = verify(g, spec, rv.V1)
            relaxed = []
            if kind == "real" and v.verdict != "ACCEPT":
                raise SystemExit(f"{system}/{case}: stored graph no longer gives ACCEPT ({v.verdict})")
            if kind == "counterfactual":
                relaxed = counterfactual_accept(v)
            text = review_package(spec, g, v, r.get("history") or [])
            name = f"{system}__{case}" + ("__V1" if kind == "counterfactual" else "")
            meta = {"system": system, "case": case, "kind": kind, "package_sha256": hashlib.sha256(text.encode()).hexdigest(),
                    "package_chars": len(text), "relaxed_checks": relaxed,
                    "measured_extent_occurrences": text.count(MEASURED_EXTENT) if case.startswith("X1") else None}
            (OUT / f"{name}.package.txt").write_text(text)
            (OUT / f"{name}.package_meta.json").write_text(json.dumps(meta, indent=1))
            line = f"{name}: package {meta['package_sha256'][:12]} ({len(text)} chars)"
            if meta["measured_extent_occurrences"] is not None:
                line += f", '{MEASURED_EXTENT}' occurs {meta['measured_extent_occurrences']} times"
            if a.call:
                if kind == "real":
                    res = {"case": case, "system": system, "note": "post-hoc: LLM acceptance review applied to a stored "
                           "deterministic ACCEPT", **review_only(store, spec, r, rv.V1)}
                else:
                    rvw = LLMPlanner().review(spec, g, v, r.get("history") or [])
                    res = {"case": case, "system": system, "note": "post-hoc counterfactual: verdict as the combined-only "
                           "rule (V1) would give it", "relaxed_checks": relaxed,
                           "review_verdict": "INCONCLUSIVE" if rvw.get("failure") else ("ACCEPT" if rvw.get("concur") else "INCONCLUSIVE"),
                           "review": rvw}
                (OUT / f"{name}.json").write_text(json.dumps(res, indent=1, default=str))
                line += f" -> review {res.get('review_verdict') or res.get('verdict')}"
            elif not (OUT / f"{name}.json").exists():
                line += " (no stored review result; run with --call)"
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
