"""The rule-based planner exactly as pre-registered (sensitivity analysis for criterion 5b; not part of the §19 protocol).

design.md §19 fixes the C-rule policy as: statistics/averaging -> mesh -> time -> domain, default parameters,
refinement families continued from their finest member. The planner that ran as C-rule also requests RUN_LONGER, before
that order, for a statistically unreliable family member (1df98b8) and for an INCONCLUSIVE physics_regime check
(10f8b80), both added after the first results existed (docs/methodology.md §6, "Deviations from pre-registration",
item 2). Criterion 5b compares the LLM planner with "the pre-registered rule-based planner", so this script runs that
planner: the same loop, validator and budgets, with `candidate_actions` reduced to the fixed order. The decision code is
not edited; the variant is applied by replacing one function here (as scripts/posthoc_allgeometry.py does).

    SOCRATES_CPU_SLOTS=1 python scripts/run_rule_prereg.py [--cases all] [--workers 17]

Writes results/benchmark/C-rule-prereg/<case>.json (stamped like benchmark results, plus the planner variant).
Simulations that the variant requests and another system already ran are reused from the run store.
"""

import argparse
import json
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

import socrates.critic.rule_based as rule_based  # noqa: E402
from socrates.checks.verifier import COMPONENT_TO_ACTION  # noqa: E402
from socrates.critic.schema import NextExperiment  # noqa: E402
from socrates.orchestration.evaluation import is_infrastructure_error, staleness  # noqa: E402
from socrates.orchestration.loop import Budget, RuleBasedPlanner, run_adaptive  # noqa: E402

import run_benchmark as rb  # noqa: E402  (root_for, stamp, FINGERPRINT: identical bookkeeping)

SYSTEM = "C-rule-prereg"
VARIANT = "pre-registered order only (no unreliable-member or physics-regime RUN_LONGER rules)"


def candidate_actions_prereg(graph, verdict):
    """The §19 policy: the first missing component in the fixed order, its primitive with default parameters, from the
    finest member of its family (RUN_LONGER from the longest run of the root's configuration)."""
    missing: set[str] = set()
    for comps in verdict.missing_components.values():
        missing.update(comps)
    out, seen = [], set()
    for comp in rule_based.ORDER:
        if comp not in missing:
            continue
        action = COMPONENT_TO_ACTION[comp]
        if action in seen:
            continue
        seen.add(action)
        if action == "RUN_LONGER":
            parent = graph.longest_same_config(graph.root).run_id
        else:
            fam = graph.factor_family({"REFINE_MESH": "mesh", "REDUCE_TIME_STEP": "time", "EXPAND_DOMAIN": "domain"}[action])
            parent = fam[-1].run_id
        out.append(NextExperiment(action=action, parameters={}, parent_run=parent,
                                  reason=f"{comp} uncertainty component is unmeasured or not yet within budget",
                                  expected_outcome="quantifies the missing component"))
    return out


def run_case(case: dict, store, spec) -> str:
    f = rb.OUT / SYSTEM / f"{case['id']}.json"
    root = rb.root_for(store, spec, case)
    if f.exists():
        old = json.loads(f.read_text())
        if not is_infrastructure_error(old) and staleness(old, f, store, rb.FINGERPRINT, root.run_id) is None:
            return f"{SYSTEM:14s} {case['id']:24s} -> {old.get('final_verdict')} (current)"
    res = run_adaptive(root.run_id, store, spec, RuleBasedPlanner(), budget=Budget(),
                       log_path=rb.OUT / SYSTEM / f"{case['id']}.partial.json").to_dict()
    res["case"], res["root_run"], res["planner_variant"] = case["id"], root.run_id, VARIANT
    res["stamp"] = rb.stamp(store, res, root)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(res, indent=1, default=str))
    return f"{SYSTEM:14s} {case['id']:24s} -> {res.get('final_verdict')}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="all")
    ap.add_argument("--workers", type=int, default=17)
    a = ap.parse_args()
    rule_based.candidate_actions = candidate_actions_prereg  # read at call time by rule_based_decision and the planner
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = rb.ProblemSpec.from_yaml(REPO / man["problem_spec"])
    store = rb.RunStore(REPO / "results" / "runs")
    cases = man["cases"] if a.cases == "all" else [c for c in man["cases"] if c["id"] in a.cases.split(",")]
    print(f"{SYSTEM}: {VARIANT}; decision code {rb.FINGERPRINT}", flush=True)

    def go(c):
        try:
            print(run_case(c, store, spec), flush=True)
        except Exception:  # noqa: BLE001 -- recorded and visible; the other cases continue
            print(f"{SYSTEM:14s} {c['id']:24s} -> ERROR\n{traceback.format_exc()}", flush=True)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(go, cases))
    print("done", flush=True)


if __name__ == "__main__":
    main()
