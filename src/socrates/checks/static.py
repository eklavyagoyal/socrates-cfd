"""Single-run deterministic checks.

Each function takes the evidence dict of one run (plus the problem spec and
the verification config) and returns CheckResult(s).  Missing evidence is
always INCONCLUSIVE, never PASS.
"""

from __future__ import annotations

from ..case_generation.spec import ProblemSpec
from .base import CheckResult, Status, thr

P, F, I = Status.PASS, Status.FAIL, Status.INCONCLUSIVE


def check_solver_completion(ev: dict) -> CheckResult:
    s = ev.get("solver", {})
    if not s.get("log_found"):
        return CheckResult("solver_completion", I, "no solver log found", source="solver log")
    if s.get("fatal_errors"):
        return CheckResult("solver_completion", F, "solver reported FOAM FATAL error(s)",
                           value=s["fatal_errors"][:2], source="solver log")
    if not s.get("completed"):
        return CheckResult("solver_completion", F, "solver log has no final 'End' (crashed or killed)",
                           value=s.get("final_time"), source="solver log")
    return CheckResult("solver_completion", P, "solver ran to its configured end and printed 'End'",
                       value=s.get("final_time"), source="solver log")


def check_mesh_quality(ev: dict, cfg: dict) -> CheckResult:
    cm = (ev.get("mesh") or {}).get("checkMesh")
    if not cm:
        return CheckResult("mesh_quality", I, "checkMesh output missing", source="checkMesh")
    limits = {
        "max_non_orthogonality": thr(cfg, "mesh_quality", "max_non_orthogonality_deg"),
        "max_skewness": thr(cfg, "mesh_quality", "max_skewness"),
        "max_aspect_ratio": thr(cfg, "mesh_quality", "max_aspect_ratio"),
    }
    vals = {k: cm.get(k) for k in limits}
    if any(v is None for v in vals.values()):
        return CheckResult("mesh_quality", I, f"checkMesh statistics missing: {vals}", value=vals, source="checkMesh")
    bad = {k: v for k, v in vals.items() if v > limits[k][0]}
    src = "; ".join(f"{k}: {s}" for k, (_, s) in limits.items())
    thr_vals = {k: v for k, (v, _) in limits.items()}
    if not cm.get("mesh_ok") or bad:
        return CheckResult("mesh_quality", F,
                           f"checkMesh failed ({cm.get('failed_checks')} failed checks) or limits exceeded: {bad}",
                           value=vals, threshold=thr_vals, source=src)
    return CheckResult("mesh_quality", P,
                       "checkMesh reports 'Mesh OK' and non-orthogonality, skewness, aspect ratio are within OpenFOAM's own limits. "
                       "This says the mesh is valid, NOT that it resolves the flow.",
                       value=vals, threshold=thr_vals, source=src)


def check_mass_conservation(ev: dict, spec: ProblemSpec, cfg: dict) -> CheckResult:
    c = ev.get("conservation", {})
    if not c.get("patch_fluxes_found"):
        return CheckResult("mass_conservation", I, "boundary flux records missing", source="surfaceFieldValue sum(phi)")
    tau = min(spec.verification.requested_tolerance.values())
    frac = cfg["conservation"]["imbalance_fraction_of_tolerance"]
    limit = frac * tau
    v = c["relative_imbalance_max"]
    cont = (ev.get("solver") or {}).get("continuity_sum_local_max")
    detail = {"continuity_sum_local_max": cont}
    src = "postProcessing/flux_*/surfaceFieldValue.dat; threshold = tau/20 (2*eps <= tau/10 bound on induced Cd error)"
    if v > limit:
        return CheckResult("mass_conservation", F, f"global mass imbalance {v:.2e} of inflow exceeds {limit:.2e}",
                           value=v, threshold=limit, source=src, details=detail)
    return CheckResult("mass_conservation", P,
                       f"max relative boundary-flux imbalance {v:.2e} <= {limit:.2e}; cannot bias the requested quantities beyond tau/10",
                       value=v, threshold=limit, source=src, details=detail)


def check_linear_solvers(ev: dict, cfg: dict) -> CheckResult:
    r = ev.get("residuals", {})
    s = ev.get("solver", {})
    if not r.get("found"):
        return CheckResult("linear_solver_convergence", I, "solverInfo output missing", source="solverInfo")
    if ev.get("configuration", {}).get("solver") == "simpleFoam":
        return check_steady_convergence(ev)
    lim = cfg["linear_solvers"]
    pf = r.get("p_final_max_last_10pct")
    hits = s.get("max_linear_solver_iteration_hits", 0)
    if pf is None:
        return CheckResult("linear_solver_convergence", I, "final pressure residual not recorded", source="solverInfo")
    # last p solve of each step uses relTol 0: it must reach the absolute tolerance
    ok = pf <= lim["p_tolerance"] * 1.0001 and hits == 0
    return CheckResult(
        "linear_solver_convergence", P if ok else F,
        ("final pressure solve of every recorded step reached the configured tolerance"
         if ok else f"pressure solves did not reach the configured tolerance (max final residual {pf:.2e}; iteration-limit hits {hits})"),
        value={"p_final_max_last_10pct": pf, "iteration_limit_hits": hits},
        threshold=lim["p_tolerance"], source="solverInfo.dat p_final; threshold = configured solver tolerance",
    )


def check_steady_convergence(ev: dict) -> CheckResult:
    s = ev.get("solver", {})
    it = s.get("steady_converged_iteration")
    if it is None:
        return CheckResult("linear_solver_convergence", F,
                           "steady solver did not satisfy its residualControl before the iteration limit",
                           source="simpleFoam log 'SIMPLE solution converged'")
    return CheckResult("linear_solver_convergence", P,
                       f"steady solver satisfied residualControl after {it} iterations. Residual convergence "
                       "shows the discrete steady equations were solved; it does not show the steady model is appropriate.",
                       value=it, source="simpleFoam log")


def check_courant(ev: dict, cfg: dict) -> CheckResult:
    conf = ev.get("configuration", {})
    if conf.get("solver") == "simpleFoam":
        return CheckResult("courant_number", I, "not applicable to a steady pseudo-time solver; temporal behaviour unverifiable",
                           source="configuration")
    co = (ev.get("solver") or {}).get("courant_max")
    limit, src = thr(cfg, "courant", "piso_max_co")
    if co is None:
        return CheckResult("courant_number", I, "Courant number not found in log", source="solver log")
    n_outer = conf.get("pimple", {}).get("nOuterCorrectors", 1)
    if n_outer <= 1:
        if co > limit:
            return CheckResult("courant_number", F,
                               f"max Courant number {co:.2f} exceeds {limit} while running in PISO mode (nOuterCorrectors=1)",
                               value=co, threshold=limit, source=src)
        return CheckResult("courant_number", P, f"max Courant number {co:.2f} < {limit} (PISO mode). "
                           "Stability/accuracy guideline only; temporal discretisation error is not quantified by this.",
                           value=co, threshold=limit, source=src)
    return CheckResult("courant_number", I,
                       f"max Courant number {co:.2f} with {n_outer} PIMPLE outer correctors: stable large-Co operation is possible "
                       "but temporal accuracy is unproven without time-step refinement",
                       value=co, threshold=limit, source=src)


def check_reynolds_consistency(ev: dict, cfg: dict) -> CheckResult:
    conf = ev.get("configuration", {})
    re_case = conf.get("configured_reynolds")
    re_spec = conf.get("spec_reynolds")
    re_spec_params = conf.get("spec_reynolds_from_parameters")
    tol = cfg["consistency"]["reynolds_relative"]
    vals = {"case": re_case, "spec": re_spec, "spec_from_parameters": re_spec_params}
    if None in vals.values():
        return CheckResult("reynolds_consistency", I, "Reynolds number inputs missing", value=vals)
    if abs(re_spec_params - re_spec) / re_spec > tol:
        return CheckResult("reynolds_consistency", F, "problem specification is internally inconsistent (U*D/nu != Re)",
                           value=vals, threshold=tol, source="spec")
    rel = abs(re_case - re_spec) / re_spec
    if rel > tol:
        return CheckResult("reynolds_consistency", F,
                           f"case solves Re={re_case:.4g} but the problem specifies Re={re_spec:.4g} (relative mismatch {rel:.2%}); "
                           "the simulation answers a different question",
                           value=vals, threshold=tol, source="case physical parameters vs spec")
    return CheckResult("reynolds_consistency", P, f"case Re={re_case:.4g} matches spec Re={re_spec:.4g}",
                       value=vals, threshold=tol, source="case physical parameters vs spec")


def check_force_reference(ev: dict, cfg: dict) -> CheckResult:
    conf = ev.get("configuration", {})
    used = conf.get("force_reference", {})
    want = dict(conf.get("force_reference_consistent_values", {}))
    tol = cfg["consistency"]["force_reference_relative"]
    # independent geometric cross-check of the span from the mesh bounding box
    bb = ((ev.get("mesh") or {}).get("checkMesh") or {}).get("bounding_box")
    detail = {}
    if bb:
        span_mesh = bb[1][2] - bb[0][2]
        D = conf["physical_configured"]["diameter"]
        detail["Aref_from_mesh_bounding_box"] = D * span_mesh
        want["Aref"] = D * span_mesh
    bad = {}
    for k in ("magUInf", "Aref"):
        if k not in used or k not in want:
            return CheckResult("force_reference_consistency", I, f"missing {k}", value=used)
        if abs(used[k] - want[k]) / abs(want[k]) > tol:
            bad[k] = {"used": used[k], "consistent": want[k]}
    src = "forceCoeffs entries vs inlet BC velocity and mesh-measured projected area (D x span)"
    if bad:
        return CheckResult("force_reference_consistency", F,
                           f"force-coefficient normalisation inconsistent with the case: {bad}; coefficients are mis-scaled",
                           value=used, threshold=tol, source=src, details=detail)
    return CheckResult("force_reference_consistency", P,
                       "magUInf equals inlet velocity and Aref equals D x mesh span",
                       value=used, threshold=tol, source=src, details=detail)


def check_physics_regime(ev: dict, spec: ProblemSpec, cfg: dict) -> CheckResult:
    """Qualitative regime consistency (steady / periodic / 3D) from literature boundaries."""
    re = spec.operating_conditions.reynolds_number
    onset, s1 = thr(cfg, "physics_regime", "shedding_onset_re")
    three_d, s2 = thr(cfg, "physics_regime", "three_d_transition_re")
    src = f"{s1}; {s2}"
    conf = ev.get("configuration", {})
    tb = ev.get("temporal_behavior", {})
    if spec.problem.dimensionality == "2D" and re > three_d:
        return CheckResult("physics_regime", F,
                           f"Re={re} exceeds the 3D wake-transition Re~{three_d}; a 2D model is not representative",
                           value=re, threshold=three_d, source=src)
    if re <= onset:
        return CheckResult("physics_regime", I, "steady regime expected; no oscillation check applies", value=re, source=src)
    if conf.get("solver") == "simpleFoam":
        return CheckResult("physics_regime", F,
                           f"Re={re} lies in the periodic-shedding regime (onset Re~{onset}); a steady formulation can only "
                           "return the unstable symmetric branch, whose drag is not the time-mean drag of the physical flow",
                           value={"re": re, "solver": "simpleFoam"}, threshold=onset, source=src)
    osc = tb.get("oscillating")
    if osc is None:
        return CheckResult("physics_regime", I, "could not determine whether the lift oscillates", value=re, source=src)
    if not osc:
        return CheckResult("physics_regime", F,
                           f"Re={re} lies in the periodic-shedding regime but no sustained lift oscillation was found "
                           f"(Cl rms over last quarter {ev['forces'].get('cl_rms_last_quarter'):.2e}); the expected physics is absent "
                           "(typical causes: excessive numerical diffusion, damping time step, too short a run)",
                           value=ev["forces"].get("cl_rms_last_quarter"),
                           threshold=cfg["physics_regime"]["oscillation_cl_rms"], source=src)
    return CheckResult("physics_regime", P, f"sustained periodic lift oscillation present, as expected for {onset} < Re={re} < {three_d}",
                       value=re, source=src)


def _rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(b), 1e-30)


def check_averaging_window(ev: dict, spec: ProblemSpec, cfg: dict) -> list[CheckResult]:
    """Bias of the *reported* (declared-window) value vs the stationary estimate of the same run."""
    out = []
    frac = cfg["error_budget"]["component_pass_fraction"]
    rep = (ev.get("qoi") or {}).get("reported") or {}
    sta = (ev.get("qoi") or {}).get("stationary")
    tb = ev.get("temporal_behavior") or {}
    for q in spec.requested_outputs:
        tau = spec.verification.requested_tolerance.get(q)
        if tau is None:
            continue
        name = "averaging_window"
        if ev.get("configuration", {}).get("solver") == "simpleFoam":
            out.append(CheckResult(name, I, "steady solver: no time averaging performed", qoi=q, component="averaging"))
            continue
        if not sta or sta.get(q) is None or rep.get(q) is None:
            out.append(CheckResult(name, I, f"no stationary estimate of {q} available (record too short or no oscillation)",
                                   qoi=q, component="averaging"))
            continue
        b = _rel(rep[q], sta[q])
        detail = {"reported": rep[q], "stationary": sta[q],
                  "declared_start_convective": tb.get("declared_averaging_start_convective"),
                  "transient_end_convective": tb.get("transient_end_time_convective"),
                  "declared_window_cycles": tb.get("declared_window_cycles")}
        src = "declared-window value vs MSER-truncated integer-cycle value of the same run"
        if b > tau:
            out.append(CheckResult(name, F, f"reported {q} differs from the stationary-window value by {b:.2%} > tau={tau:.0%}: "
                                   "the declared averaging window is contaminated or too short",
                                   value=b, threshold=tau, source=src, qoi=q, component="averaging", uncertainty=b, details=detail))
        elif b <= frac * tau:
            out.append(CheckResult(name, P, f"reported {q} within {b:.3%} of the stationary-window value",
                                   value=b, threshold=frac * tau, source=src, qoi=q, component="averaging", uncertainty=b, details=detail))
        else:
            out.append(CheckResult(name, I, f"averaging bias {b:.2%} is between {frac*tau:.2%} and {tau:.0%}",
                                   value=b, threshold=frac * tau, source=src, qoi=q, component="averaging", uncertainty=b, details=detail))
    return out


def statistical_uncertainty(ev: dict, q: str) -> tuple[float | None, dict]:
    """Relative statistical/stationarity uncertainty of the stationary estimate of q."""
    sw = (ev.get("forces") or {}).get("stationary_window") or {}
    sta = (ev.get("qoi") or {}).get("stationary") or {}
    if not sta or sta.get(q) is None or "n_cycles" not in sw:
        return None, {"reason": "no stationary window"}
    if q == "mean_drag_coefficient":
        parts = {
            "ci95": (sw.get("mean_cd_ci95_halfwidth") or 0.0) / abs(sta[q]),
            "drift": abs(sw.get("mean_cd_relative_drift") or 0.0),
            "half_difference": abs(sw.get("mean_cd_half_difference_rel") or 0.0),
        }
    elif q == "strouhal_number":
        T = 1.0 / sw["frequency_zero_crossing"]
        st_fft = sta.get("strouhal_number_fft")
        parts = {
            "ci95_period": (sw.get("period_ci95_halfwidth") or 0.0) / T,
            "fft_vs_zero_crossing": _rel(st_fft, sta[q]) if st_fft else 0.0,
        }
    elif q == "rms_lift_coefficient":
        parts = {"amplitude_drift": abs(sw.get("cl_amplitude_relative_drift") or 0.0)}
    else:
        return None, {"reason": f"unknown quantity {q}"}
    return max(parts.values()), parts


def check_statistics(ev: dict, spec: ProblemSpec, cfg: dict) -> list[CheckResult]:
    out = []
    frac = cfg["error_budget"]["component_pass_fraction"]
    min_cyc = cfg["statistics"]["min_cycles"]
    sw = (ev.get("forces") or {}).get("stationary_window") or {}
    tb = ev.get("temporal_behavior") or {}
    for q in spec.requested_outputs:
        tau = spec.verification.requested_tolerance.get(q)
        if tau is None:
            continue
        if ev.get("configuration", {}).get("solver") == "simpleFoam":
            out.append(CheckResult("statistical_uncertainty", I, "steady solver: no statistics", qoi=q, component="statistics"))
            continue
        n = sw.get("n_cycles")
        if n is None or n < min_cyc:
            out.append(CheckResult("statistical_uncertainty", I, f"stationary window has {n} cycles (< {min_cyc})",
                                   value=n, threshold=min_cyc, qoi=q, component="statistics"))
            continue
        u, parts = statistical_uncertainty(ev, q)
        detail = {"components": parts, "n_cycles": n, "mser_hit_cap": tb.get("mser_hit_cap")}
        src = "per-cycle batch means (t-quantile CI95), linear drift and half-window difference; max taken"
        if u is None:
            out.append(CheckResult("statistical_uncertainty", I, parts.get("reason", "unavailable"), qoi=q, component="statistics"))
        elif u <= frac * tau:
            out.append(CheckResult("statistical_uncertainty", P, f"statistical/stationarity uncertainty {u:.2e} <= {frac*tau:.2%}",
                                   value=u, threshold=frac * tau, source=src, qoi=q, component="statistics", uncertainty=u, details=detail))
        else:
            out.append(CheckResult("statistical_uncertainty", I, f"statistical/stationarity uncertainty {u:.2%} > {frac*tau:.2%}; "
                                   "a longer record is needed", value=u, threshold=frac * tau, source=src, qoi=q,
                                   component="statistics", uncertainty=u, details=detail))
    return out


def run_static_checks(ev: dict, spec: ProblemSpec, cfg: dict) -> list[CheckResult]:
    res = [
        check_solver_completion(ev),
        check_mesh_quality(ev, cfg),
        check_mass_conservation(ev, spec, cfg),
        check_linear_solvers(ev, cfg),
        check_courant(ev, cfg),
        check_reynolds_consistency(ev, cfg),
        check_force_reference(ev, cfg),
        check_physics_regime(ev, spec, cfg),
    ]
    res += check_averaging_window(ev, spec, cfg)
    res += check_statistics(ev, spec, cfg)
    return res
