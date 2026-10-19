"""Case generation, systematic refinement and experiment primitives (no solver runs)."""

import math

import pytest

from socrates.case_generation.blockmesh import (
    first_cell_from_ratio,
    ratio_from_first_cell,
    render_blockmesh_dict,
    resolve_layout,
)
from socrates.case_generation.catalog import list_adversarial, load_baseline, load_case_definition
from socrates.case_generation.spec import diff_configs
from socrates.case_generation.writer import write_case
from socrates.experiments.primitives import ActionRejected, plan_experiment

BASE = load_baseline()
PERIODIC_EV = {"solver": {"log_found": True, "completed": True, "courant_max": 0.75},
               "temporal_behavior": {"oscillating": True},
               "forces": {"stationary_window": {"n_cycles": 10}}}


def test_grading_roundtrip():
    E = ratio_from_first_cell(0.5, 30, 0.005)
    assert math.isclose(first_cell_from_ratio(0.5, 30, E), 0.005, rel_tol=1e-9)


def test_systematic_refinement_scales_cells_and_keeps_grading():
    L1 = resolve_layout(BASE)
    L2 = resolve_layout(BASE.with_changes({"mesh.refinement": 2.0}))
    assert L2.nq == 2 * L1.nq and L2.nra == 2 * L1.nra
    assert L2.E_ra == L1.E_ra and L2.E_dn == L1.E_dn
    # first wall cell roughly halves
    f1 = first_cell_from_ratio(L1.r_mid - L1.R, L1.nra, L1.E_ra)
    f2 = first_cell_from_ratio(L2.r_mid - L2.R, L2.nra, L2.E_ra)
    assert 0.45 < f2 / f1 < 0.55
    assert 3.8 < L2.n_cells / L1.n_cells < 4.2


def test_blockmesh_dict_has_all_patches():
    txt, _ = render_blockmesh_dict(BASE)
    for p in ("cylinder", "inlet", "outlet", "top", "bottom", "frontAndBack"):
        assert p in txt
    assert txt.count("hex (") == 16
    assert txt.count("arc ") == 16


def test_write_case_files(tmp_path):
    write_case(BASE, tmp_path / "c")
    for f in ("system/controlDict", "system/fvSchemes", "system/fvSolution", "0/U", "0/p",
              "constant/transportProperties", "case_config.json"):
        assert (tmp_path / "c" / f).exists()
    cd = (tmp_path / "c/system/controlDict").read_text()
    assert "forceCoeffs" in cd and "magUInf         0.15" in cd and "Aref            0.0001" in cd


def test_adversarial_definitions_load_and_differ_from_baseline():
    paths = list_adversarial()
    assert len(paths) >= 5
    for p in paths:
        cfg, meta = load_case_definition(p)
        assert diff_configs(BASE, cfg), meta["id"]


def test_domain_change_preserves_near_field_mesh():
    cfg, _ = load_case_definition([p for p in list_adversarial() if "B1" in p.name][0])
    a, b = resolve_layout(BASE), resolve_layout(cfg)
    assert (a.nq, a.nra, a.nrb, a.E_ra, a.E_rb) == (b.nq, b.nra, b.nrb, b.E_ra, b.E_rb)


def _plan(action, params=None, ev=PERIODIC_EV, parent=BASE):
    return plan_experiment(action, params, parent_run="root", parent_cfg=parent, parent_ev=ev, root_cfg=BASE)


def test_refine_mesh_records_changes_and_controls_courant():
    p = _plan("REFINE_MESH", {"factor": math.sqrt(2)})
    assert math.isclose(p.child_config.mesh.refinement, math.sqrt(2))
    assert p.child_config.time.delta_t < BASE.time.delta_t  # 0.75*1.414 > 0.9 -> dt reduced
    assert "mesh.refinement" in p.changes and p.init.kind == "map" and p.init.consistent


def test_refine_from_non_periodic_parent_starts_fresh():
    ev = {"solver": {"log_found": True, "completed": True, "courant_max": 0.5}, "temporal_behavior": {"oscillating": False}}
    p = _plan("REFINE_MESH", None, ev)
    assert p.init.kind == "fresh"
    assert p.child_config.time.end_time == BASE.time.end_time


def test_reduce_time_step_and_expand_domain():
    p = _plan("REDUCE_TIME_STEP", {"factor": 2})
    assert math.isclose(p.child_config.time.delta_t, BASE.time.delta_t / 2)
    p = _plan("EXPAND_DOMAIN", {"factor": 2})
    assert p.child_config.domain.half_height == 2 * BASE.domain.half_height
    assert p.init.kind == "map" and not p.init.consistent
    a, b = resolve_layout(BASE), resolve_layout(p.child_config)
    assert (a.nq, a.nra, a.E_ra) == (b.nq, b.nra, b.E_ra)


def test_run_longer_is_restart():
    p = _plan("RUN_LONGER", {"additional_convective_times": 100})
    assert p.init.kind == "restart" and p.child_config.time.end_time == BASE.time.end_time + 100


@pytest.mark.parametrize("action,params", [
    ("DELETE_FILES", {}),
    ("REFINE_MESH", {"factor": 5.0}),
    ("REFINE_MESH", {"factor": "big"}),
    ("REFINE_MESH", {"factr": 1.5}),
    ("REDUCE_TIME_STEP", {"factor": 1.0}),
    ("RUN_LONGER", {"additional_convective_times": 10000}),
])
def test_invalid_actions_rejected(action, params):
    with pytest.raises(ActionRejected):
        _plan(action, params)


def test_cumulative_refinement_limit():
    parent = BASE.with_changes({"mesh.refinement": 2.0})
    with pytest.raises(ActionRejected):
        _plan("REFINE_MESH", {"factor": 1.5}, parent=parent)


def test_content_hash_ignores_name():
    assert BASE.content_hash() == BASE.with_changes({}, name="other").content_hash()
    assert BASE.content_hash() != BASE.with_changes({"time.delta_t": 0.02}).content_hash()


@pytest.mark.parametrize("changes", [{}, {"boundaries.inlet_shear": 0.1}, {"boundaries.lateral": "noSlipWall"},
                                     {"numerics.solver": "simpleFoam"}])
def test_each_patch_defined_exactly_once(tmp_path, changes):
    import re
    cfg = BASE.with_changes(changes)
    write_case(cfg, tmp_path / "c")
    for field in ("U", "p"):
        txt = (tmp_path / "c" / "0" / field).read_text()
        bf = txt[txt.index("boundaryField"):]
        blocks = re.findall(r"^    (\w+)\n    \{\n(.*?)\n    \}", bf, re.S | re.M)
        names = [b[0] for b in blocks]
        assert sorted(names) == sorted(["inlet", "outlet", "cylinder", "top", "bottom", "frontAndBack"]), names
        for name, body in blocks:
            assert body.count("type ") == 1, (field, name, body)


def test_cylinder_scale_only_changes_geometry():
    a, b = resolve_layout(BASE), resolve_layout(BASE.with_changes({"mesh.cylinder_scale": 1.05}))
    assert math.isclose(b.R, 0.525) and (a.nq, a.nra, a.E_ra) == (b.nq, b.nra, b.E_ra)
    assert BASE.with_changes({"mesh.cylinder_scale": 1.0}).content_hash() == BASE.content_hash()


def test_fields_written_exactly_at_end_time(tmp_path):
    """Regression: restarts and mapped children must start from the true final state."""
    import re
    cfg = BASE.with_changes({"time.end_time": 40.0})
    write_case(cfg, tmp_path / "c")
    cd = (tmp_path / "c/system/controlDict").read_text()
    end = float(re.search(r"^endTime\s+([\d.eE+-]+);", cd, re.M).group(1))
    wi = float(re.search(r"^writeInterval\s+([\d.eE+-]+);", cd, re.M).group(1))
    assert math.isclose(end, wi)
