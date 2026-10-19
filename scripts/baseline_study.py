"""Baseline verification study + in-house converged reference ("truth").

One-factor-at-a-time refinement chains from the baseline, run in parallel:
    mesh:   f = 1 -> sqrt2 -> 2
    time:   dt = 0.01 -> 0.005 -> 0.0025
    domain: x1 -> x2 -> x4
    run longer: +100 D/U
Results: results/baseline/study.json (consumed by scripts/make_baseline_report.py).
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.catalog import load_baseline  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.experiments.primitives import plan_experiment  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402

CHAINS = {
    "mesh": [("REFINE_MESH", {}), ("REFINE_MESH", {})],
    "time": [("REDUCE_TIME_STEP", {"factor": 2}), ("REDUCE_TIME_STEP", {"factor": 2})],
    "domain": [("EXPAND_DOMAIN", {"factor": 2}), ("EXPAND_DOMAIN", {"factor": 2})],
    "longer": [("RUN_LONGER", {})],
}


def main() -> None:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    base_cfg = load_baseline()
    root = store.get_or_run(base_cfg, spec, reason="baseline", launched_by="baseline_study")
    print("root", root.run_id, root.status, flush=True)

    def chain(name: str):
        out, parent = [], root
        for action, params in CHAINS[name]:
            plan = plan_experiment(action, params, parent_run=parent.run_id, parent_cfg=parent.config,
                                   parent_ev=parent.evidence, root_cfg=base_cfg)
            res = store.get_or_run(plan.child_config, spec, init=plan.init, parent_run=parent.run_id,
                                   reason=f"baseline verification study ({name} chain)", experiment=plan.to_dict(),
                                   launched_by="baseline_study")
            print(name, action, res.run_id, res.status, flush=True)
            out.append({"action": action, "run_id": res.run_id, "parent": parent.run_id, "status": res.status})
            parent = res
        return name, out

    with ThreadPoolExecutor(max_workers=len(CHAINS)) as ex:
        results = dict(ex.map(chain, CHAINS))
    d = REPO / "results" / "baseline"
    d.mkdir(parents=True, exist_ok=True)
    (d / "study.json").write_text(json.dumps({"root": root.run_id, "chains": results}, indent=2))


if __name__ == "__main__":
    main()
