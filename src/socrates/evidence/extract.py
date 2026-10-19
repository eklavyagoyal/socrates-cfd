"""Build the machine-readable evidence record for one completed run.

Evidence is *measured* -- every number comes from a solver output file, a
mesh utility, or the generated configuration.  Nothing here makes a
judgement; judgements live in ``socrates.checks``.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from ..case_generation.blockmesh import first_cell_from_ratio, resolve_layout
from ..case_generation.spec import CaseConfig, ProblemSpec
from ..openfoam.parsers import concat_time_dirs, parse_checkmesh, parse_solver_log
from .signals import analyze_steady, analyze_unsteady


def _finite(x) -> float | None:
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def mesh_evidence(case_dir: Path, cfg: CaseConfig) -> dict:
    log = case_dir / "log.checkMesh"
    cm = parse_checkmesh(log.read_text()) if log.exists() else None
    L = resolve_layout(cfg)
    first_wall = first_cell_from_ratio(L.r_mid - L.R, L.nra, L.E_ra)
    first_wake = first_cell_from_ratio(L.Ld - L.a, L.ndn, L.E_dn)
    last_wake = first_wake * L.E_dn
    D = cfg.physical.diameter
    out = {
        "checkMesh": cm,
        "n_cells": cm["cells"] if cm else L.n_cells,
        "design": {
            "refinement_factor": cfg.mesh.refinement,
            "cells_around_cylinder": 4 * L.nq,
            "wall_normal_first_cell_D": first_wall,
            "radial_cells_inner_ring": L.nra,
            "wake_cells_streamwise": L.ndn,
            "wake_first_cell_D": first_wake,
            "wake_last_cell_D": last_wake,
            "wake_cells_across_near_wake": L.nq,
            "wake_factor": cfg.mesh.wake_factor,
        },
    }
    if cm and cm.get("total_volume") and cm.get("cells"):
        area_D2 = cm["total_volume"] / (cfg.mesh.span * D) / D**2
        out["representative_cell_size_D"] = math.sqrt(area_D2 / cm["cells"])
        out["domain_area_D2"] = area_D2
    return out


def domain_evidence(cfg: CaseConfig) -> dict:
    d = cfg.domain
    return {
        "upstream_D": d.upstream,
        "downstream_D": d.downstream,
        "half_height_D": d.half_height,
        "blockage_ratio": 1.0 / (2.0 * d.half_height),
        "lateral_boundary": cfg.boundaries.lateral,
        "outlet_velocity_bc": cfg.boundaries.outlet_velocity,
        "outlet_pressure_bc": cfg.boundaries.outlet_pressure,
        "inlet_pressure_bc": cfg.boundaries.inlet_pressure,
        "cylinder_velocity_bc": cfg.boundaries.cylinder_velocity,
    }


def configuration_evidence(cfg: CaseConfig, spec: ProblemSpec) -> dict:
    p = cfg.physical
    ref = cfg.resolved_force_reference()
    span_m = cfg.mesh.span * p.diameter
    return {
        "solver": cfg.numerics.solver,
        "ddt_scheme": cfg.numerics.ddt if cfg.numerics.solver != "simpleFoam" else "steadyState",
        "convection_scheme": cfg.numerics.div_U,
        "grad_scheme": cfg.numerics.grad,
        "pimple": {
            "nOuterCorrectors": cfg.numerics.n_outer_correctors,
            "nCorrectors": cfg.numerics.n_correctors,
            "nNonOrthogonalCorrectors": cfg.numerics.n_nonorth_correctors,
        },
        "time_step_convective": cfg.time.delta_t if cfg.numerics.solver != "simpleFoam" else None,
        "end_time_convective": cfg.time.end_time if cfg.numerics.solver != "simpleFoam" else None,
        "declared_averaging_start_convective": cfg.averaging.start_time if cfg.numerics.solver != "simpleFoam" else None,
        "adjust_time_step": cfg.time.adjust_time_step,
        "physical_configured": p.model_dump(),
        "configured_reynolds": cfg.configured_reynolds(),
        "spec_reynolds": spec.operating_conditions.reynolds_number,
        "spec_reynolds_from_parameters": spec.reynolds_from_parameters(),
        "force_reference": ref,
        "force_reference_consistent_values": {
            "magUInf": p.inlet_velocity,
            "lRef": p.diameter,
            "Aref": p.diameter * span_m,
        },
        "mesh_span_m": span_m,
        "initial_perturbation": cfg.perturbation.enabled,
    }


def solver_evidence(case_dir: Path, cfg: CaseConfig) -> dict:
    logs = sorted(case_dir.glob(f"log.{cfg.numerics.solver}*"))
    if not logs:
        return {"log_found": False}
    parsed = [parse_solver_log(lp.read_text(errors="replace")) for lp in logs]
    last = parsed[-1]
    co_max = np.concatenate([p.courant_max for p in parsed]) if parsed else np.empty(0)
    co_mean = np.concatenate([p.courant_mean for p in parsed]) if parsed else np.empty(0)
    c_loc = np.concatenate([p.cont_sum_local for p in parsed])
    c_cum = np.concatenate([p.cont_cumulative for p in parsed])
    p_last = np.concatenate([p.p_last_final for p in parsed])
    # skip first steps: the impulsive start / setFields perturbation produce
    # a non-representative Courant spike that the solver immediately damps
    skip = min(10, max(len(co_max) - 1, 0))
    return {
        "log_found": True,
        "logs": [lp.name for lp in logs],
        "application": last.application,
        "build": last.build,
        "n_procs": last.n_procs,
        "completed": all(p.completed for p in parsed),
        "fatal_errors": [e for p in parsed for e in p.fatal_errors],
        "warnings": [w for p in parsed for w in p.warnings][:20],
        "n_warnings": sum(len(p.warnings) for p in parsed),
        "n_steps": int(sum(p.n_steps for p in parsed)),
        "final_time": _finite(last.times[-1]) if last.n_steps else None,
        "execution_time_s": sum(p.execution_time or 0.0 for p in parsed),
        "courant_max": _finite(np.nanmax(co_max[skip:])) if co_max.size > skip else None,
        "courant_max_including_startup": _finite(np.nanmax(co_max)) if co_max.size else None,
        "courant_mean_avg": _finite(np.nanmean(co_mean[skip:])) if co_mean.size > skip else None,
        "courant_startup_steps_skipped": int(skip),
        "continuity_sum_local_max": _finite(np.nanmax(c_loc[skip:])) if c_loc.size > skip else None,
        "continuity_sum_local_median": _finite(np.nanmedian(c_loc[skip:])) if c_loc.size > skip else None,
        "continuity_cumulative_final": _finite(c_cum[-1]) if c_cum.size else None,
        "max_linear_solver_iteration_hits": int(sum(p.max_solver_iterations_hit for p in parsed)),
        "p_last_solve_final_residual_max": _finite(np.nanmax(p_last[skip:])) if p_last.size > skip else None,
        "p_last_solve_final_residual_p99": _finite(np.nanpercentile(p_last[skip:], 99)) if p_last.size > skip else None,
        "p_last_solve_unconverged_fraction_1e-7": _finite(np.mean(p_last[skip:] > 1.0001e-7)) if p_last.size > skip else None,
        "steady_converged_iteration": last.steady_converged_iteration,
    }


def residual_evidence(case_dir: Path, cfg: CaseConfig) -> dict:
    si = concat_time_dirs(case_dir / "postProcessing" / "solverInfo1", "solverInfo.dat")
    if not si:
        return {"found": False}
    out: dict = {"found": True}
    n = len(si["Time"])
    tail = slice(int(0.9 * n), n)
    for name in ("Ux_initial", "Uy_initial", "p_initial"):
        if name in si:
            v = si[name].astype(float)
            out[name] = {
                "final": float(v[-1]),
                "max_last_10pct": float(np.max(v[tail])),
                "median_last_10pct": float(np.median(v[tail])),
            }
    for name in ("Ux_final", "Uy_final", "p_final"):
        if name in si:
            out[name + "_max_last_10pct"] = float(np.max(si[name][tail].astype(float)))
    return out


def conservation_evidence(case_dir: Path) -> dict:
    flux = {}
    for patch in ("inlet", "outlet", "top", "bottom"):
        c = concat_time_dirs(case_dir / "postProcessing" / f"flux_{patch}", "surfaceFieldValue.dat")
        if c and "sum(phi)" in c:
            flux[patch] = c
    if "inlet" not in flux or "outlet" not in flux:
        return {"patch_fluxes_found": False}
    t = flux["inlet"]["Time"]
    total = np.zeros_like(t)
    for patch, c in flux.items():
        total = total + np.interp(t, c["Time"], c["sum(phi)"])
    q_in = np.abs(flux["inlet"]["sum(phi)"])
    rel = np.abs(total) / np.maximum(q_in, 1e-300)
    skip = min(5, len(rel) - 1)
    return {
        "patch_fluxes_found": True,
        "patches": sorted(flux),
        "relative_imbalance_max": float(np.max(rel[skip:])),
        "relative_imbalance_final": float(rel[-1]),
        "lateral_flux_fraction_max": float(
            max((np.max(np.abs(flux[p]["sum(phi)"])) for p in ("top", "bottom") if p in flux), default=0.0)
            / max(float(np.max(q_in)), 1e-300)
        ),
    }


def force_series(case_dir: Path) -> dict[str, np.ndarray]:
    c = concat_time_dirs(case_dir / "postProcessing" / "forceCoeffs1", "coefficient.dat")
    if not c:
        return {}
    return {"t": c["Time"], "cd": c["Cd"], "cl": c["Cl"]}


def extract_evidence(case_dir: str | Path, cfg: CaseConfig, spec: ProblemSpec) -> tuple[dict, dict[str, np.ndarray]]:
    """Return (evidence dict, raw force series)."""
    case_dir = Path(case_dir)
    series = force_series(case_dir)
    ev: dict = {
        "mesh": mesh_evidence(case_dir, cfg),
        "domain": domain_evidence(cfg),
        "configuration": configuration_evidence(cfg, spec),
        "solver": solver_evidence(case_dir, cfg),
        "residuals": residual_evidence(case_dir, cfg),
        "conservation": conservation_evidence(case_dir),
    }
    tc = cfg.convective_time
    D, U = cfg.physical.diameter, cfg.physical.inlet_velocity
    if not series:
        ev["forces"] = {"found": False}
        ev["qoi"] = {}
        return ev, series
    if cfg.numerics.solver == "simpleFoam":
        fa = analyze_steady(series["t"], series["cd"], series["cl"])
        ev["forces"] = {"found": True, "steady": True, **fa}
        ev["temporal_behavior"] = {"steady_solver": True, "oscillating": None}
        ev["qoi"] = {
            "reported": {
                "mean_drag_coefficient": fa.get("final_cd"),
                "rms_lift_coefficient": 0.0 if fa.get("final_cd") is not None else None,
                "strouhal_number": None,
            },
            "stationary": None,
        }
        return ev, series

    fa = analyze_unsteady(
        series["t"], series["cd"], series["cl"],
        convective_time=tc, declared_start=cfg.averaging.start_time * tc,
    )
    cycle_table = fa.pop("cycle_table", None)
    ev["forces"] = {"found": True, "steady": False, **fa}
    if cycle_table is not None:
        ev["forces"]["cycle_table"] = cycle_table
    sw = fa.get("stationary_window") or {}
    dw = fa.get("declared_window") or {}

    def st(f):
        return f * D / U if f is not None else None

    f_st = sw.get("frequency_zero_crossing")
    period = 1.0 / f_st if f_st else None
    dt = cfg.time.delta_t * tc
    ev["temporal_behavior"] = {
        "steady_solver": False,
        "oscillating": fa.get("oscillating"),
        "record_length_convective": fa.get("record_length_convective"),
        "transient_end_time_convective": (sw["start"] / tc) if "start" in sw else None,
        "declared_averaging_start_convective": cfg.averaging.start_time,
        "stationary_cycles": sw.get("n_cycles"),
        "declared_window_cycles": dw.get("complete_cycles"),
        "mser_truncated_cycles": sw.get("truncated_cycles"),
        "mser_hit_cap": (sw.get("truncated_cycles") is not None and fa.get("n_cycles_total")
                         and sw["truncated_cycles"] >= fa["n_cycles_total"] // 2),
        "steps_per_period": (period / dt) if period else None,
        "shedding_period_convective": (period / tc) if period else None,
    }
    stationary_qoi = None
    if "mean_cd" in sw and fa.get("oscillating"):
        stationary_qoi = {
            "mean_drag_coefficient": sw["mean_cd"],
            "rms_lift_coefficient": sw["cl_rms"],
            "strouhal_number": st(sw.get("frequency_zero_crossing")),
            "strouhal_number_fft": st(sw.get("frequency_fft")),
            "mean_drag_coefficient_ci95": sw.get("mean_cd_ci95_halfwidth"),
            "mean_drag_coefficient_drift_rel": sw.get("mean_cd_relative_drift"),
            "mean_drag_coefficient_half_diff_rel": sw.get("mean_cd_half_difference_rel"),
            "n_cycles": sw.get("n_cycles"),
        }
    elif "mean_cd" in sw:
        stationary_qoi = {
            "mean_drag_coefficient": sw["mean_cd"],
            "rms_lift_coefficient": sw["cl_rms"],
            "strouhal_number": None,
        }
    ev["qoi"] = {
        "reported": {
            "mean_drag_coefficient": dw.get("mean_cd"),
            "rms_lift_coefficient": dw.get("cl_rms"),
            "strouhal_number": st(dw.get("frequency_fft")) if fa.get("oscillating") else None,
            "strouhal_frequency_resolution": st(dw.get("frequency_resolution")),
            "basis": "declared averaging window; time-weighted mean; St from FFT peak of Cl",
        },
        "stationary": stationary_qoi,
    }
    return ev, series
