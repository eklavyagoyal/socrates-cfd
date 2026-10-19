"""Is the baseline's domain chain confounded by far-field coarsening?

EXPAND_DOMAIN keeps the near-field mesh and the per-cell growth rate, so the far field coarsens as the domain grows
(last wake cell ~1 D at x1, ~3.9 D at x4). The four-level domain chain (half-height 40/80/120/160 D) does not
converge like a power law, which this coarsening could explain. This test re-runs the x4 domain with the far-field
cell counts x1.5 (same domain, finer far field), mapped from the settled x4 run, and compares the stationary values.

    python scripts/farfield_resolution_test.py                      # x4 domain (stage 4)
    python scripts/farfield_resolution_test.py --level x1           # same refinement on the baseline-size domain

The x1 variant separates far-field coarsening from wake resolution: the x1.5 counts refine every block outside the
near-field square, i.e. also the wake inside the baseline's own extent. If drag moves by a similar amount on the
x1 domain, the stage-4 change is mostly wake resolution (already in the mesh chain), not a domain confound.

Writes results/baseline/farfield_test.json (x4) or farfield_test_x1.json. Not part of the pre-registered study;
used for the reference's uncertainty and reported in reports/baseline_validation.md.
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.blockmesh import resolve_layout  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.orchestration.store import Initialisation, RunStore  # noqa: E402

LEVELS = {  # settled source run, name, end time, averaging start, consistent mapping, output file
    "x4": ("baseline.long280-3b986ef1d905", "baseline.D4x.ff1.5", 200.0, 120.0, False, "farfield_test.json"),
    "x1": ("baseline.long250-8b585d987e4c", "baseline.ff1.5", 120.0, 60.0, True, "farfield_test_x1.json"),
}
FACTOR = 1.5


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", choices=sorted(LEVELS), default="x4")
    a = ap.parse_args()
    SOURCE, name, end, avg, consistent, out_name = LEVELS[a.level]
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    src = store.load(SOURCE)
    cfg = src.config
    m = cfg.mesh
    mesh = m.model_copy(update={k: round(getattr(m, k) * FACTOR) for k in ("n_upstream", "n_downstream", "n_lateral")})
    time = cfg.time.model_copy(update={"end_time": end})
    child = cfg.model_copy(update={"name": name, "mesh": mesh, "time": time,
                                   "averaging": cfg.averaging.model_copy(update={"start_time": avg}),
                                   "description": f"{a.level} domain with outer-block counts x{FACTOR} (resolution test)"})
    print("cells", resolve_layout(cfg).n_cells, "->", resolve_layout(child).n_cells, flush=True)
    res = store.get_or_run(child, spec, init=Initialisation("map", SOURCE, consistent=consistent), parent_run=SOURCE,
                           reason="far-field resolution test of the domain chain", launched_by="farfield_test")
    out = {"source": SOURCE, "test": res.run_id, "status": res.status, "factor": FACTOR}
    if res.ok:
        sa = (src.evidence or {})["qoi"]["stationary"]
        sb = (res.evidence or {})["qoi"]["stationary"]
        key = a.level
        out["values"] = {q: {key: sa[q], f"{key}_farfield_refined": sb[q], "relative_change": (sb[q] - sa[q]) / sa[q]}
                         for q in ("mean_drag_coefficient", "strouhal_number", "rms_lift_coefficient")}
    (REPO / "results" / "baseline" / out_name).write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1), flush=True)


if __name__ == "__main__":
    main()
