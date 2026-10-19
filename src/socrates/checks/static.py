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
    """checkMesh validity.  checkMesh always exits 0, so its log verdict is parsed.

    '***' items (failed checks, e.g. skewness > 4, aspect ratio > 1000) -> FAIL.
    Non-orthogonality > 70 deg is only a '*' warning in OpenFOAM -> INCONCLUSIVE.
    """
    cm = (ev.get("mesh") or {}).get("checkMesh")
    if not cm or not cm.get("completed"):
        return CheckResult("mesh_quality", I, "checkMesh output missing or incomplete", source="checkMesh")
    limits = {
        "max_non_orthogonality": thr(cfg, "mesh_quality", "max_non_orthogonality_deg"),
        "max_skewness": thr(cfg, "mesh_quality", "max_skewness"),
        "max_aspect_ratio": thr(cfg, "mesh_quality", "max_aspect_ratio"),
    }
    vals = {k: cm.get(k) for k in limits}
    src = "checkMesh log ('Mesh OK' / 'Failed N mesh checks'); limits: " + "; ".join(f"{k}: {s}" for k, (_, s) in limits.items())
    thr_vals = {k: v for k, (v, _) in limits.items()}
    if not cm.get("mesh_ok"):
        return CheckResult("mesh_quality", F, f"checkMesh reports {cm.get('failed_checks')} failed check(s): {cm.get('error_lines')[:3]}",
                           value=vals, threshold=thr_vals, source=src)
    if any(v is None for v in vals.values()):
        return CheckResult("mesh_quality", I, f"checkMesh statistics missing: {vals}", value=vals, source=src)
    warn = {k: v for k, v in vals.items() if v > thr_vals[k]}
    if warn:
        return CheckResult("mesh_quality", I, f"checkMesh passes but reports warnings above OpenFOAM limits: {warn}",
                           value=vals, threshold=thr_vals, source=src)
    return CheckResult("mesh_quality", P,
                       "checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. "
                       "This shows the mesh is valid, NOT that it resolves the flow.",
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
    s = ev.get("solver", {})
    if ev.get("configuration", {}).get("solver") == "simpleFoam":
        return check_steady_convergence(ev)
    lim = cfg["linear_solvers"]
    frac = s.get("p_last_solve_unconverged_fraction_1e-7")
    pmax = s.get("p_last_solve_final_residual_max")
    hits = s.get("max_linear_solver_iteration_hits", 0)
    if frac is None:
        return CheckResult("linear_solver_convergence", I, "final pressure solves not found in the solver log",
                           source="solver log (last 'Solving for p' line of each step)")
    ok = frac <= lim["allowed_fraction_unconverged_steps"] and hits == 0
    src = ("solver log, last pressure solve of each time step (relTol 0, so it must reach the configured absolute "
           "tolerance); solverInfo is not used because it records only the first solve of a step")
    val = {"fraction_of_steps_above_tolerance": frac, "max_final_residual": pmax, "iteration_limit_hits": hits}
    if ok:
        return CheckResult("linear_solver_convergence", P,
                           f"final pressure solve reached the configured tolerance in {1 - frac:.1%} of steps",
                           value=val, threshold=lim["allowed_fraction_unconverged_steps"], source=src)
    return CheckResult("linear_solver_convergence", F,
                       f"final pressure solve missed the configured tolerance in {frac:.1%} of steps "
                       f"(max final residual {pmax:.2e}; iteration-limit hits {hits})",
                       value=val, threshold=lim["allowed_fraction_unconverged_steps"], source=src)


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
    sw = (ev.get("forces") or {}).get("stationary_window") or {}
    amp_drift = sw.get("cl_amplitude_relative_drift")
    tau = min(spec.verification.requested_tolerance.values())
    if amp_drift is not None and abs(amp_drift) > tau:
        return CheckResult("physics_regime", I,
                           f"lift oscillation present but its amplitude changes by {amp_drift:+.1%} across the analysed window: "
                           "not yet a sustained limit cycle (decaying or still growing); a longer record is needed",
                           value=amp_drift, threshold=tau, source=src)
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
        # the stationary estimate is only a valid reference if it is itself
        # statistically reliable (enough cycles, small drift)
        n_cyc = ((ev.get("forces") or {}).get("stationary_window") or {}).get("n_cycles")
        u_ref, _ = statistical_uncertainty(ev, q)
        min_cyc = cfg["statistics"]["min_cycles"]
        if n_cyc is None or n_cyc < min_cyc or u_ref is None or u_ref > frac * tau:
            out.append(CheckResult(name, I,
                                   f"reference (stationary-window) estimate of {q} is itself unreliable "
                                   f"({n_cyc} cycles, statistical/stationarity uncertainty "
                                   f"{'n/a' if u_ref is None else f'{u_ref:.2%}'}); averaging bias cannot be assessed",
                                   value=b, qoi=q, component="averaging",
                                   details={"reported": rep[q], "stationary": sta[q], "n_cycles": n_cyc,
                                            "reference_uncertainty": u_ref}))
            continue
        detail = {"reported": rep[q], "stationary": sta[q],
                  "declared_start_convective": tb.get("declared_averaging_start_convective"),
                  "transient_end_convective": tb.get("transient_end_time_convective"),
                  "declared_window_cycles": tb.get("declared_window_cycles")}
        src = "declared-window value vs MSER-truncated integer-cycle value of the same run"
        detail["kind"] = "bias"  # a measured, signed error of the reported value, not a random uncertainty
        if b > tau:
            out.append(CheckResult(name, F, f"reported {q} differs from the stationary-window value by {b:.2%} > tau={tau:.0%}: "
                                   "the declared averaging window is contaminated or too short",
                                   value=b, threshold=tau, source=src, qoi=q, component="averaging", uncertainty=b, details=detail))
        else:
            # no experiment can change the root's declared-window value, so this is not missing evidence:
            # it is a known bias that the aggregation adds linearly to the other components
            out.append(CheckResult(name, P, f"reported {q} is biased by {b:.3%} relative to the stationary-window value "
                                   "(measured bias, added linearly to the error budget)",
                                   value=b, threshold=tau, source=src, qoi=q, component="averaging", uncertainty=b, details=detail))
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
            "period_drift": abs(sw.get("period_relative_drift") or 0.0),
            "period_half_difference": abs(sw.get("period_half_difference_rel") or 0.0),
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


def check_scheme_order(ev: dict) -> CheckResult:
    conf = ev.get("configuration", {})
    conv = conf.get("convection_scheme")
    if not conv:
        return CheckResult("convection_scheme_order", I, "convection scheme not recorded", source="configuration")
    toks = conv.replace("bounded", "").split()
    src = ("J. Fluids Eng. editorial policy on numerical accuracy (published with Celik et al. 2008): at least "
           "second-order spatial schemes; first-order numerical diffusion called 'devastating'")
    if len(toks) >= 2 and toks[1] == "upwind":
        return CheckResult("convection_scheme_order", I,
                           f"convection scheme '{conv}' is formally first order; numerical diffusion must be shown "
                           "negligible by mesh refinement before the result can be trusted",
                           value=conv, source=src)
    return CheckResult("convection_scheme_order", P, f"convection scheme '{conv}' is nominally second order", value=conv, source=src)


def check_geometry_consistency(ev: dict, spec: ProblemSpec, cfg: dict) -> CheckResult:
    """Measured cylinder diameter (checkMesh patch bounding box) vs the specification.

    Added after attack X1: refinement studies cannot detect a geometry that is
    consistently wrong, so the solved geometry must be measured, not assumed.
    """
    tol = cfg["extensions"]["geometry_relative_tolerance"]
    mg = (ev.get("mesh") or {}).get("measured_geometry")
    if not mg:
        return CheckResult("geometry_consistency", I, "cylinder patch geometry not measured", source="checkMesh -allTopology")
    D = spec.geometry.cylinder_diameter
    dx, dy = mg["cylinder_diameter_x_m"], mg["cylinder_diameter_y_m"]
    rel = max(abs(dx - D), abs(dy - D)) / D
    src = "checkMesh patch bounding box of 'cylinder' vs problem specification"
    val = {"measured_x": dx, "measured_y": dy, "specified": D}
    if rel > tol:
        return CheckResult("geometry_consistency", F,
                           f"meshed cylinder is {dx * 1e3:.4g} x {dy * 1e3:.4g} mm but the problem specifies {D * 1e3:.4g} mm "
                           f"({rel:.2%} mismatch): the simulation solves a different geometry", value=val, threshold=tol, source=src)
    return CheckResult("geometry_consistency", P, f"meshed cylinder diameter matches the specification within {tol:.0e}",
                       value=val, threshold=tol, source=src)


def check_inlet_uniformity(ev: dict, spec: ProblemSpec, cfg: dict) -> CheckResult:
    """The spec asks for a uniform stream: the solved inlet profile must be uniform.

    Added after attack X2: no refinement primitive varies the inlet profile, so a
    wrong profile is invisible to sensitivity studies and must be measured.
    """
    tol = cfg["extensions"]["inlet_nonuniformity_tolerance"]
    inl = ev.get("inlet") or {}
    if not inl.get("measured"):
        return CheckResult("inlet_uniformity", I, "inlet velocity profile not measured", source="latest U field")
    nu = inl.get("ux_nonuniformity") or 0.0
    U = spec.operating_conditions.inlet_velocity
    mean_err = abs(inl["ux_mean_unweighted"] - U) / U
    val = {"nonuniformity": nu, "ux_min": inl["ux_min"], "ux_max": inl["ux_max"], "uy_max_abs": inl["uy_max_abs"]}
    src = "inlet patch values of the latest written U field vs the specified uniform free stream"
    if nu > tol or inl["uy_max_abs"] > tol * U or (inl["n_faces_or_uniform"] == 1 and mean_err > tol):
        return CheckResult("inlet_uniformity", F, f"inlet velocity is not the specified uniform stream "
                           f"(Ux {inl['ux_min']:.4g}..{inl['ux_max']:.4g} m/s, non-uniformity {nu:.2%})",
                           value=val, threshold=tol, source=src)
    return CheckResult("inlet_uniformity", P, "inlet velocity is uniform and equals the specified free stream",
                       value=val, threshold=tol, source=src)


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
        check_scheme_order(ev),
    ]
    if (cfg.get("extensions") or {}).get("geometry_consistency"):
        res.append(check_geometry_consistency(ev, spec, cfg))
    if (cfg.get("extensions") or {}).get("inlet_uniformity"):
        res.append(check_inlet_uniformity(ev, spec, cfg))
    res += check_averaging_window(ev, spec, cfg)
    res += check_statistics(ev, spec, cfg)
    return res
