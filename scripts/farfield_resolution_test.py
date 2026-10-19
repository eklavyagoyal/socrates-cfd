"""Is the baseline's domain chain confounded by far-field coarsening?

EXPAND_DOMAIN keeps the near-field mesh and the per-cell growth rate, so the far field coarsens as the domain grows
(last wake cell ~1 D at x1, ~3.9 D at x4). The four-level domain chain (half-height 40/80/120/160 D) does not
converge like a power law, which this coarsening could explain. This test re-runs the x4 domain with the far-field
cell counts x1.5 (same domain, finer far field), mapped from the settled x4 run, and compares the stationary values.

    python scripts/farfield_resolution_test.py

Writes results/baseline/farfield_test.json. Not part of the pre-registered study; used for the reference's
uncertainty and reported in reports/baseline_validation.md.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.blockmesh import resolve_layout  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.orchestration.store import Initialisation, RunStore  # noqa: E402

SOURCE = "baseline.long280-3b986ef1d905"  # x4 domain (half-height 160 D), settled limit cycle
FACTOR = 1.5


def main() -> None:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    src = store.load(SOURCE)
    cfg = src.config
    m = cfg.mesh
    mesh = m.model_copy(update={k: round(getattr(m, k) * FACTOR) for k in ("n_upstream", "n_downstream", "n_lateral")})
    time = cfg.time.model_copy(update={"end_time": 200.0})
    child = cfg.model_copy(update={"name": "baseline.D4x.ff1.5", "mesh": mesh, "time": time,
                                   "averaging": cfg.averaging.model_copy(update={"start_time": 120.0}),
                                   "description": f"x4 domain with far-field counts x{FACTOR} (resolution test)"})
    print("cells", resolve_layout(cfg).n_cells, "->", resolve_layout(child).n_cells, flush=True)
    res = store.get_or_run(child, spec, init=Initialisation("map", SOURCE, consistent=False), parent_run=SOURCE,
                           reason="far-field resolution test of the domain chain", launched_by="farfield_test")
    out = {"source": SOURCE, "test": res.run_id, "status": res.status, "factor": FACTOR}
    if res.ok:
        a = (src.evidence or {})["qoi"]["stationary"]
        b = (res.evidence or {})["qoi"]["stationary"]
        out["values"] = {q: {"x4": a[q], "x4_farfield_refined": b[q], "relative_change": (b[q] - a[q]) / a[q]}
                         for q in ("mean_drag_coefficient", "strouhal_number", "rms_lift_coefficient")}
    (REPO / "results" / "baseline" / "farfield_test.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1), flush=True)


if __name__ == "__main__":
    main()
