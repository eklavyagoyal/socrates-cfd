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


def test_averaging_check_needs_reliable_reference():
    """Regression (found on case G1): a small reported-vs-stationary difference must not PASS
    when the stationary estimate itself comes from too few cycles / a drifting record."""
    from socrates.checks.static import check_averaging_window
    ev = {"configuration": {"solver": "pimpleFoam"},
          "qoi": {"reported": {"mean_drag_coefficient": 1.296, "strouhal_number": 0.1613},
                  "stationary": {"mean_drag_coefficient": 1.304, "strouhal_number": 0.1606,
                                 "strouhal_number_fft": 0.1607}},
          "forces": {"stationary_window": {"n_cycles": 3, "mean_cd_ci95_halfwidth": 0.04,
                                           "mean_cd_relative_drift": 0.04, "frequency_zero_crossing": 2.4,
                                           "period_ci95_halfwidth": 0.01}},
          "temporal_behavior": {}}
    res = check_averaging_window(ev, SPEC, CFG)
    assert all(r.status == Status.INCONCLUSIVE for r in res)
    ev["forces"]["stationary_window"].update(n_cycles=12, mean_cd_ci95_halfwidth=1e-4, mean_cd_relative_drift=1e-4,
                                             period_ci95_halfwidth=1e-5, mean_cd_half_difference_rel=1e-4)
    ev["qoi"]["stationary"]["strouhal_number_fft"] = 0.1606
    res = check_averaging_window(ev, SPEC, CFG)
    assert all(r.status == Status.PASS for r in res)


def test_geometry_consistency_extension():
    from socrates.checks.static import check_geometry_consistency
    cfg2 = load_config("configs/verification_v2.yaml")
    ev = {"mesh": {"measured_geometry": {"cylinder_diameter_x_m": 0.0105, "cylinder_diameter_y_m": 0.0105}}}
    assert check_geometry_consistency(ev, SPEC, cfg2).status == Status.FAIL
    ev["mesh"]["measured_geometry"].update(cylinder_diameter_x_m=0.01, cylinder_diameter_y_m=0.01)
    assert check_geometry_consistency(ev, SPEC, cfg2).status == Status.PASS
    assert check_geometry_consistency({}, SPEC, cfg2).status == Status.INCONCLUSIVE
    # v1 (pre-registered) configuration does not run it
    assert "geometry_consistency" not in [c.check for c in run_static_checks(ev, SPEC, CFG)]
    assert "geometry_consistency" in [c.check for c in run_static_checks(ev, SPEC, cfg2)]


# ---- regressions from the adversarial review (findings #2, #3, #4, #5/#13) ----

def test_slow_convergence_not_extrapolated_with_formal_order():
    # eps32/eps21 = 1.1 -> p_obs ~ 0.28; the old fallback to p=2 gave U ~1.4 % (PASS)
    r = 2 ** 0.5
    res = _seq([1.2958, 1.298, 1.300], [1.0, 1 / r, 0.5])
    assert res.details["observed_order"] < 0.5
    assert res.status == Status.INCONCLUSIVE and res.uncertainty > 0.03


def test_no_positive_order_is_inconclusive():
    res = assess_sequence(check="time_sensitivity", component="time", qoi="q", values=[1.2944, 1.298, 1.300],
                          sizes=[0.01, 0.004, 0.01 / 2.5 / 1.5], run_ids=["a", "b", "c"], formal_order=2.0,
                          tau=0.03, cfg=CFG)
    assert res.status == Status.INCONCLUSIVE


def test_observed_order_never_returns_unconverged_value():
    # r32 > r21^2 makes the plain fixed-point map oscillate; the bracketed solve must be exact or None
    for p_true in (0.7, 1.0, 1.5, 2.0, 3.0):
        h3, h2, h1 = 4.0, 1.6, 1.0
        f = lambda h: 1.0 + 0.05 * h ** p_true
        p, _ = observed_order(f(h3) - f(h2), f(h2) - f(h1), h2 / h1, h3 / h2, 2.0)
        assert p is not None and abs(p - p_true) < 1e-6


def test_degenerate_family_does_not_crash():
    res = _seq([1.30, 1.31, 1.312], [1.0, 0.5, 0.5])
    assert res.status == Status.INCONCLUSIVE


def test_two_level_noise_floor():
    res = assess_sequence(check="mesh_sensitivity", component="mesh", qoi="q", values=[1.30, 1.3002],
                          sizes=[1.0, 0.7], run_ids=["a", "b"], formal_order=2.0, tau=0.03, cfg=CFG, noise=0.014)
    assert res.status == Status.INCONCLUSIVE


def test_fail_needs_change_beyond_noise():
    res = assess_sequence(check="mesh_sensitivity", component="mesh", qoi="q", values=[1.0, 1.035],
                          sizes=[1.0, 0.7], run_ids=["a", "b"], formal_order=2.0, tau=0.03, cfg=CFG, noise=0.01)
    assert res.status != Status.FAIL
    res = assess_sequence(check="mesh_sensitivity", component="mesh", qoi="q", values=[1.0, 1.035],
                          sizes=[1.0, 0.7], run_ids=["a", "b"], formal_order=2.0, tau=0.03, cfg=CFG, noise=0.0)
    assert res.status == Status.FAIL


def test_label_uses_truth_uncertainty():
    from socrates.orchestration.truth import label_case
    T = {"mean_drag_coefficient": 1.33, "strouhal_number": 0.165}
    tol = {"mean_drag_coefficient": 0.03, "strouhal_number": 0.03}
    rep = {"mean_drag_coefficient": 1.33 * 1.0302, "strouhal_number": 0.165}
    assert label_case(rep, T, tol)["label"] == "flawed"
    lab = label_case(rep, T, tol, truth_uncertainty={"mean_drag_coefficient": 0.005, "strouhal_number": 0.005})
    assert lab["label"] == "ambiguous" and lab["label_unstable"] == ["mean_drag_coefficient"]
    rep["mean_drag_coefficient"] = 1.33 * 1.10
    assert label_case(rep, T, tol, truth_uncertainty={"mean_drag_coefficient": 0.005})["label"] == "flawed"
    assert label_case({"mean_drag_coefficient": 1.0}, T, tol)["label"] == "flawed"  # St missing
    # one quantity borderline at tau/2, the other clearly beyond tau -> still flawed
    rep = {"mean_drag_coefficient": 1.33 * 1.015, "strouhal_number": 0.165 * 1.08}
    assert label_case(rep, T, tol, truth_uncertainty={"mean_drag_coefficient": 0.005,
                                                      "strouhal_number": 0.005})["label"] == "flawed"


# ---- second review round: divergence, bias aggregation, decaying oscillation ----

def test_monotone_divergence_is_not_a_pass():
    r = 2 ** 0.5
    res = _seq([1.000, 1.002, 1.008], [1.0, 1 / r, 0.5])
    assert res.status == Status.INCONCLUSIVE and res.details.get("divergent")
    res = _seq([1.000, 1.010, 1.040], [1.0, 1 / r, 0.5])
    assert res.status == Status.FAIL


def test_truth_extrapolation_refuses_divergent_chain():
    from socrates.orchestration.truth import extrapolate_chain
    out = extrapolate_chain([1.000, 1.002, 1.008], [1.0, 2 ** -0.5, 0.5], 2.0)
    assert out["order"] is None and out["extrapolated"] == 1.008


def test_bias_adds_linearly_to_rss():
    from socrates.checks.base import CheckResult
    checks = [CheckResult("gate", Status.PASS, "ok")]
    for q in SPEC.requested_outputs:
        checks.append(CheckResult("averaging_window", Status.PASS, "b", qoi=q, component="averaging",
                                  uncertainty=0.02, details={"kind": "bias"}))
        for comp in ("statistics", "mesh", "time", "domain"):
            checks.append(CheckResult(f"{comp}_c", Status.PASS, "ok", qoi=q, component=comp, uncertainty=0.006))
    v = aggregate(checks, SPEC)
    # 0.02 + sqrt(4 * 0.006^2) = 0.032 > 0.03 (RSS alone would give 0.0228 and ACCEPT)
    assert v.verdict == "INCONCLUSIVE"
    assert abs(v.per_qoi["mean_drag_coefficient"]["combined_uncertainty"] - 0.032) < 1e-9


def test_decaying_oscillation_is_not_sustained_shedding():
    ev = {"configuration": {"solver": "pimpleFoam"}, "temporal_behavior": {"oscillating": True},
          "forces": {"stationary_window": {"cl_amplitude_relative_drift": -0.2}}}
    assert check_physics_regime(ev, SPEC, CFG).status == Status.INCONCLUSIVE
    ev["forces"]["stationary_window"]["cl_amplitude_relative_drift"] = -0.001
    assert check_physics_regime(ev, SPEC, CFG).status == Status.PASS


# ---- fix-verification round ----

def test_fail_not_hidden_by_missing_order_or_divergence():
    r = 2 ** 0.5
    for vals in ([1.40, 1.330, 1.329], [1.40, 1.401, 1.450]):
        res = assess_sequence(check="m", component="mesh", qoi="q", values=vals, sizes=[1.0, 1 / r, 0.5],
                              run_ids=["a", "b", "c"], formal_order=2.0, tau=0.03, cfg=CFG, noise=1e-4)
        assert res.status == Status.FAIL, vals


def test_very_fast_convergence_uses_above_band_rule():
    r = 2 ** 0.5
    res = assess_sequence(check="m", component="mesh", qoi="q", values=[1.3400, 1.3346, 1.33447],
                          sizes=[1.0, 1 / r, 0.5], run_ids=["a", "b", "c"], formal_order=2.0, tau=0.03, cfg=CFG, noise=2e-5)
    assert res.status == Status.PASS and "outside" in res.details["method"]


def test_truth_extrapolation_never_uses_a_faster_order_than_observed():
    from socrates.orchestration.truth import extrapolate_chain

    h = [1.0, 2 ** -0.5, 0.5]
    vals = [1.0 + 0.01 * x**0.6 for x in h]  # slow, pre-asymptotic convergence to 1.0 (p = 0.6 < band)
    out = extrapolate_chain(vals, h, 2.0)
    assert abs(out["order_used"] - 0.6) < 1e-6 and abs(out["extrapolated"] - 1.0) < 1e-9
    assert out["uncertainty"] >= abs(out["extrapolated"] - vals[-1]) * 2.9  # Fs = 3 outside the band


def test_label_unstable_only_when_the_truth_interval_can_change_the_label():
    from socrates.orchestration.truth import label_case

    tol = {"cd": 0.03, "st": 0.03}
    T = {"cd": 1.0, "st": 1.0}
    u = {"cd": 0.005, "st": 0.005}
    # st straddles tau/2 but cd is clearly beyond tau: flawed whatever the truth, so not 'unstable'
    lab = label_case({"cd": 1.06, "st": 1.015}, T, tol, truth_uncertainty=u)
    assert lab["label"] == "flawed" and lab["label_unstable"] == [] and lab["threshold_straddled"] == ["st"]
    lab = label_case({"cd": 1.0, "st": 1.015}, T, tol, truth_uncertainty=u)
    assert lab["label"] == "ambiguous" and lab["label_unstable"] == ["st"]
