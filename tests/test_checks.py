"""Deterministic checks: status logic, missing evidence -> INCONCLUSIVE, sensitivity math."""

import math

import pytest

from socrates.case_generation.spec import CaseConfig, PhysicalConfig, ProblemSpec
from socrates.checks.base import Status, load_config
from socrates.checks.sensitivity import assess_sequence, observed_order
from socrates.checks.static import (
    check_courant,
    check_force_reference,
    check_linear_solvers,
    check_mass_conservation,
    check_physics_regime,
    check_reynolds_consistency,
    check_solver_completion,
    run_static_checks,
)
from socrates.checks.verifier import RunGraph, RunNode, aggregate, verify

CFG = load_config()
SPEC = ProblemSpec.from_yaml("configs/problem_cylinder_re100.yaml")


def test_missing_evidence_is_never_pass():
    res = run_static_checks({}, SPEC, CFG)
    assert all(r.status != Status.PASS for r in res), [r.check for r in res if r.status == Status.PASS]


def test_empty_graph_verdict_inconclusive_not_accept():
    cfg = CaseConfig(name="x", physical=PhysicalConfig(diameter=0.01, inlet_velocity=0.15, kinematic_viscosity=1.5e-5, density=1.2))
    v = verify(RunGraph([RunNode("r", cfg, {})], "r"), SPEC, CFG)
    assert v.verdict in ("INCONCLUSIVE", "REJECT")
    assert v.verdict != "ACCEPT"


def test_solver_completion():
    assert check_solver_completion({"solver": {"log_found": True, "completed": True, "fatal_errors": []}}).status == Status.PASS
    assert check_solver_completion({"solver": {"log_found": True, "completed": False, "fatal_errors": []}}).status == Status.FAIL


def test_reynolds_mismatch_fails():
    ev = {"configuration": {"configured_reynolds": 83.33, "spec_reynolds": 100.0, "spec_reynolds_from_parameters": 100.0}}
    assert check_reynolds_consistency(ev, CFG).status == Status.FAIL
    ev["configuration"]["configured_reynolds"] = 100.0
    assert check_reynolds_consistency(ev, CFG).status == Status.PASS


def test_force_reference_uses_mesh_span():
    ev = {"configuration": {"force_reference": {"magUInf": 0.15, "Aref": 1e-4},
                            "force_reference_consistent_values": {"magUInf": 0.15, "Aref": 1e-4},
                            "physical_configured": {"diameter": 0.01}},
          "mesh": {"checkMesh": {"bounding_box": [[0, 0, 0], [1, 1, 0.01]]}}}
    assert check_force_reference(ev, CFG).status == Status.PASS
    ev["configuration"]["force_reference"]["magUInf"] = 0.16
    assert check_force_reference(ev, CFG).status == Status.FAIL
    ev["configuration"]["force_reference"]["magUInf"] = 0.15
    ev["mesh"]["checkMesh"]["bounding_box"][1][2] = 0.02  # mesh thicker than Aref assumes
    assert check_force_reference(ev, CFG).status == Status.FAIL


def test_courant_piso_vs_pimple():
    ev = {"configuration": {"solver": "pimpleFoam", "pimple": {"nOuterCorrectors": 1}}, "solver": {"courant_max": 1.4}}
    assert check_courant(ev, CFG).status == Status.FAIL
    ev["configuration"]["pimple"]["nOuterCorrectors"] = 3
    assert check_courant(ev, CFG).status == Status.INCONCLUSIVE
    ev["solver"]["courant_max"] = 0.7
    ev["configuration"]["pimple"]["nOuterCorrectors"] = 1
    assert check_courant(ev, CFG).status == Status.PASS


def test_mass_conservation_threshold_derived_from_tolerance():
    ev = {"conservation": {"patch_fluxes_found": True, "relative_imbalance_max": 1e-6}}
    r = check_mass_conservation(ev, SPEC, CFG)
    assert r.status == Status.PASS and math.isclose(r.threshold, 0.03 / 20)
    ev["conservation"]["relative_imbalance_max"] = 0.01
    assert check_mass_conservation(ev, SPEC, CFG).status == Status.FAIL


def test_linear_solver_uses_last_solve_from_log():
    ev = {"configuration": {"solver": "pimpleFoam"},
          "solver": {"p_last_solve_unconverged_fraction_1e-7": 0.0, "p_last_solve_final_residual_max": 9e-8,
                     "max_linear_solver_iteration_hits": 0}}
    assert check_linear_solvers(ev, CFG).status == Status.PASS
    ev["solver"]["p_last_solve_unconverged_fraction_1e-7"] = 0.2
    assert check_linear_solvers(ev, CFG).status == Status.FAIL


def test_physics_regime_steady_solver_fails_in_shedding_regime():
    ev = {"configuration": {"solver": "simpleFoam"}}
    assert check_physics_regime(ev, SPEC, CFG).status == Status.FAIL
    ev = {"configuration": {"solver": "pimpleFoam"}, "temporal_behavior": {"oscillating": False},
          "forces": {"cl_rms_last_quarter": 1e-6}}
    assert check_physics_regime(ev, SPEC, CFG).status == Status.FAIL


def test_observed_order_recovers_second_order():
    # phi(h) = 1 + 0.5 h^2, h = 4, 2, 1  -> p = 2
    q3, q2, q1 = 1 + 0.5 * 16, 1 + 0.5 * 4, 1 + 0.5
    p, _ = observed_order(q3 - q2, q2 - q1, 2.0, 2.0, 1.0)
    assert abs(p - 2.0) < 1e-6


def test_observed_order_nonuniform_ratio():
    h3, h2, h1 = 3.0, 2.0, 1.3
    f = lambda h: 2.0 + 0.1 * h**1.5
    p, _ = observed_order(f(h3) - f(h2), f(h2) - f(h1), h2 / h1, h3 / h2, 2.0)
    assert abs(p - 1.5) < 1e-5


def _seq(values, sizes, tau=0.03, order=2.0):
    return assess_sequence(check="mesh_sensitivity", component="mesh", qoi="q", values=values, sizes=sizes,
                           run_ids=[f"r{i}" for i in range(len(values))], formal_order=order, tau=tau, cfg=CFG)


def test_sensitivity_fail_on_large_change():
    r = _seq([1.0, 1.06], [1.0, 0.7])
    assert r.status == Status.FAIL


def test_sensitivity_two_level_needs_small_change():
    # two-level: U_root = 3 * delta * r^2/(r^2-1); r = sqrt2 -> 6 delta; pass needs <= 1.5 %
    assert _seq([1.0, 1.002], [1.0, 1 / math.sqrt(2)]).status == Status.PASS
    assert _seq([1.0, 1.01], [1.0, 1 / math.sqrt(2)]).status == Status.INCONCLUSIVE


def test_sensitivity_three_level_monotone_second_order():
    f = lambda h: 1.3 * (1 + 0.01 * h**2)
    hs = [1.0, 1 / math.sqrt(2), 0.5]
    r = _seq([f(h) for h in hs], hs)
    assert r.status == Status.PASS
    assert abs(r.details["observed_order"] - 2.0) < 1e-6
    assert abs(r.details["extrapolated_value"] - 1.3) < 1e-9


def test_sensitivity_oscillatory_detected():
    r = _seq([1.0, 1.01, 1.005], [1.0, 0.7, 0.5])
    assert r.details.get("oscillatory")


def test_aggregate_fail_wins():
    from socrates.checks.base import CheckResult
    checks = [CheckResult("x", Status.FAIL, "bad"), CheckResult("y", Status.PASS, "ok")]
    assert aggregate(checks, SPEC).verdict == "REJECT"


@pytest.mark.parametrize("missing", ["mesh", "time", "domain", "statistics", "averaging"])
def test_accept_requires_every_component(missing):
    from socrates.checks.base import CheckResult
    checks = [CheckResult("gate", Status.PASS, "ok")]
    for q in SPEC.requested_outputs:
        for comp in ("averaging", "statistics", "mesh", "time", "domain"):
            if comp != missing:
                checks.append(CheckResult(f"{comp}_c", Status.PASS, "ok", qoi=q, component=comp, uncertainty=0.001))
    v = aggregate(checks, SPEC)
    assert v.verdict == "INCONCLUSIVE"
    checks += [CheckResult(f"{missing}_c", Status.PASS, "ok", qoi=q, component=missing, uncertainty=0.001)
               for q in SPEC.requested_outputs]
    assert aggregate(checks, SPEC).verdict == "ACCEPT"


def test_accept_requires_rss_within_tolerance():
    from socrates.checks.base import CheckResult
    checks = [CheckResult("gate", Status.PASS, "ok")]
    for q in SPEC.requested_outputs:
        for comp in ("averaging", "statistics", "mesh", "time", "domain"):
            checks.append(CheckResult(f"{comp}_c", Status.PASS, "ok", qoi=q, component=comp, uncertainty=0.014))
    # each component 1.4 % <= 1.5 %, but RSS = 3.1 % > 3 %
    assert aggregate(checks, SPEC).verdict == "INCONCLUSIVE"
