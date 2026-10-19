"""Baseline verification study + in-house converged reference ("truth").

One-factor-at-a-time refinement chains from the baseline, run in parallel:
    mesh:   f = 1 -> sqrt2 -> 2          (both levels mapped from the baseline)
    time:   dt = 0.01 -> 0.005 -> 0.0025 (both levels mapped from the baseline)
    domain: x1 -> x2 -> x4               (x4 mapped from x2: one EXPAND_DOMAIN step is limited to x3)
    run longer: +100 D/U
Levels mapped from the baseline run concurrently; the initialisation source does
not enter the statistic (every mapped level runs 80 D/U and averages the last 40).

Stage 2 (added after the first study, before any benchmark label was used; see
reports/baseline_validation.md): the x2 and x4 domain levels had not reached a limit
cycle in 80 D/U (the wake must first cross the enlarged domain), so both are continued
(RUN_LONGER) until the run length exceeds the wake transit time to the outlet plus
the averaging window; and a fourth time level (dt/8) tests the slow St convergence.
The report uses every member's longest continuation, as the verifier does.

Stage 3 (after a second fact-check): a fourth domain level (x3, half-height 120 D) continued to a limit cycle,
to test whether the three-level domain extrapolation is in its asymptotic range.
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

# (action, parameters, parent): parent "root" = the baseline, "prev" = the previous level of the chain
CHAINS = {
    "mesh": [("REFINE_MESH", {}, "root"), ("REFINE_MESH", {"factor": 2.0}, "root")],
    "time": [("REDUCE_TIME_STEP", {"factor": 2}, "root"), ("REDUCE_TIME_STEP", {"factor": 4}, "root")],
    "domain": [("EXPAND_DOMAIN", {"factor": 2}, "root"), ("EXPAND_DOMAIN", {"factor": 2}, "prev")],
    "longer": [("RUN_LONGER", {}, "root")],
}


def main() -> None:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    base_cfg = load_baseline()
    root = store.get_or_run(base_cfg, spec, reason="baseline", launched_by="baseline_study")
    print("root", root.run_id, root.status, flush=True)

    def step(name: str, action: str, params: dict, parent):
        plan = plan_experiment(action, params, parent_run=parent.run_id, parent_cfg=parent.config,
                               parent_ev=parent.evidence, root_cfg=base_cfg)
        res = store.get_or_run(plan.child_config, spec, init=plan.init, parent_run=parent.run_id,
                               reason=f"baseline verification study ({name} chain)", experiment=plan.to_dict(),
                               launched_by="baseline_study")
        print(name, action, params, res.run_id, res.status, flush=True)
        if not res.ok:
            raise RuntimeError(f"{name} chain: {res.run_id} {res.status}: {res.provenance.get('failure')}")
        return res

    def chain(name: str):
        levels = CHAINS[name]
        done = [None] * len(levels)
        with ThreadPoolExecutor(max_workers=len(levels)) as inner:
            futs = {i: inner.submit(step, name, a, p, root) for i, (a, p, par) in enumerate(levels) if par == "root"}
            for i, f in futs.items():
                done[i] = f.result()
        for i, (a, p, par) in enumerate(levels):
            if par == "prev":
                done[i] = step(name, a, p, done[i - 1])
        out = []
        for i, (a, p, par) in enumerate(levels):
            parent = root if par == "root" else done[i - 1]
            out.append({"action": a, "parameters": p, "run_id": done[i].run_id, "parent": parent.run_id,
                        "status": done[i].status})
        return name, out

    with ThreadPoolExecutor(max_workers=len(CHAINS)) as ex:
        results = dict(ex.map(chain, CHAINS))

    # ---- stage 2: continuations of the domain levels, fourth time level ----
    def extend(job):
        name, idx, action, params = job
        parent = store.load(results[name][idx]["run_id"])
        return name, idx, action, step(name, action, params, parent)

    jobs = [("domain", 0, "RUN_LONGER", {"additional_convective_times": 100.0}),   # x2: outlet 100 D, run 180 D/U
            ("domain", 1, "RUN_LONGER", {"additional_convective_times": 200.0}),   # x4: outlet 200 D, run 280 D/U
            ("time", 1, "REDUCE_TIME_STEP", {"factor": 2})]                         # dt/8 from dt/4
    extensions = {"continuations": {}, "time_level_4": None}
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        for name, idx, action, res in ex.map(extend, jobs):
            if action == "RUN_LONGER":
                extensions["continuations"][results[name][idx]["run_id"]] = res.run_id
            else:
                extensions["time_level_4"] = {"run_id": res.run_id, "parent": results[name][idx]["run_id"]}
    d = REPO / "results" / "baseline"
    d.mkdir(parents=True, exist_ok=True)
    # ---- stage 3: a fourth domain level, to test the conditioning of the domain extrapolation ----
    # The x3 level (half-height 120 D, EXPAND_DOMAIN 1.5 from x2) already exists in the store (requested by the
    # LLM critic for the baseline case); it is continued to a limit cycle like the other domain levels.
    x3 = store.load("baseline.D1.5x-ed421affd588")
    x3c = step("domain", "RUN_LONGER", {"additional_convective_times": 120.0}, x3)   # outlet 150 D, run 200 D/U
    extensions["domain_level_x3"] = {"run_id": x3.run_id, "continuation": x3c.run_id}
    extensions["continuations"][x3.run_id] = x3c.run_id
    (d / "study.json").write_text(json.dumps({"root": root.run_id, "chains": results, "stage2": extensions}, indent=2))


if __name__ == "__main__":
    main()
