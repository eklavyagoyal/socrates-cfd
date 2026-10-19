"""End-to-end test of the run store and every experiment primitive on a tiny real OpenFOAM case.

Slow (a few minutes on one core); skipped when OpenFOAM is not installed.
Run with:  pytest -m openfoam
These tests check the *software* (generation, execution, restart, mapping,
provenance); the tiny mesh is far too coarse to be physically meaningful.
"""

import os

import pytest

from socrates.case_generation.catalog import load_baseline
from socrates.case_generation.spec import ProblemSpec
from socrates.experiments.primitives import Limits, plan_experiment
from socrates.openfoam.runner import openfoam_available
from socrates.orchestration.store import RunStore

pytestmark = [pytest.mark.openfoam,
              pytest.mark.skipif(not openfoam_available(), reason="OpenFOAM not installed")]

SPEC = ProblemSpec.from_yaml("configs/problem_cylinder_re100.yaml")


@pytest.fixture(scope="module")
def tiny(tmp_path_factory):
    store = RunStore(tmp_path_factory.mktemp("store"), cpu_slots=1)
    base = load_baseline().with_changes({"mesh.refinement": 0.3, "time.end_time": 40.0, "time.delta_t": 0.02,
                                         "averaging.start_time": 20.0}, name="tiny")
    root = store.get_or_run(base, SPEC, reason="integration test")
    return store, base, root


def test_root_run_completes_with_provenance(tiny):
    store, base, root = tiny
    assert root.ok
    prov = root.provenance
    for key in ("problem_spec", "case_config", "config_hash", "software", "commands", "raw_output_sha256", "started"):
        assert key in prov
    times = sorted(float(d) for d in os.listdir(root.run_dir / "case") if d[0].isdigit())
    assert times[-1] == pytest.approx(40.0 * base.convective_time, rel=1e-6)  # final state written
    assert root.evidence["solver"]["completed"]
    assert root.evidence["mesh"]["measured_geometry"]["cylinder_diameter_x_m"] == pytest.approx(0.01, rel=1e-6)


def test_cache_returns_same_run(tiny):
    store, base, root = tiny
    again = store.get_or_run(base.with_changes({}, name="renamed"), SPEC, reason="cache test")
    assert again.run_id == root.run_id


@pytest.mark.parametrize("action,params,kind", [
    ("RUN_LONGER", {"additional_convective_times": 25}, "restart"),
    ("REFINE_MESH", {"factor": 1.5}, "map"),
    ("REDUCE_TIME_STEP", {"factor": 2}, "map"),
    ("EXPAND_DOMAIN", {"factor": 2}, "map"),
])
def test_primitive_executes_and_records_parent(tiny, action, params, kind):
    store, base, root = tiny
    lim = Limits(mapped_run_length=20.0, mapped_averaging_start=10.0)
    plan = plan_experiment(action, params, parent_run=root.run_id, parent_cfg=root.config,
                           parent_ev=root.evidence, root_cfg=base, limits=lim)
    assert plan.init.kind == kind
    child = store.get_or_run(plan.child_config, SPEC, init=plan.init, parent_run=root.run_id,
                             reason="integration test", experiment=plan.to_dict())
    assert child.ok, child.provenance.get("failure")
    assert child.provenance["parent_run"] == root.run_id
    assert child.provenance["config_changes_from_parent"]
    ev = child.evidence
    if action == "RUN_LONGER":
        # continues from the true final state: exactly the additional steps
        assert ev["solver"]["n_steps"] == root.evidence["solver"]["n_steps"] + 1250
        assert ev["temporal_behavior"]["record_length_convective"] == pytest.approx(65.0, abs=0.1)
    else:
        assert "log.mapFields" in [s["log_file"] for s in child.provenance["commands"]]
        # mapped from a shedding state: lift oscillates from the first convective unit
        import numpy as np
        s = child.series()
        early = s["t"] < 5 * base.convective_time
        assert np.std(s["cl"][early]) > 0.01
