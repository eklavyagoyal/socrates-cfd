"""Multi-run sensitivity checks (mesh, time step, domain size).

One generic routine assesses a sequence of runs that differ in a single
factor, ordered from the root (the run under verification, "coarsest") to
the most refined.  The estimate is always of the error/uncertainty of the
ROOT run's value -- that is what the user is asking us to trust.

Two levels (Roache 1998; Celik et al. 2008, J. Fluids Eng. 130:078001):
    delta   = |q_f - q_c| / |q_f|
    e_root  = delta * r^p / (r^p - 1)            (Richardson, assumed order p)
    U_root  = Fs2 * e_root,   Fs2 = 3
Three levels (Celik et al. 2008 procedure):
    observed order p by fixed-point iteration, monotone/oscillatory test
    via sign(eps32/eps21), extrapolated value q_ext, U_root = Fs3*|q_3-q_ext|/|q_ext|
    with Fs3 = 1.25 when p is consistent with the formal order, otherwise
    Fs2 with the formal order (more conservative).  Oscillatory or noisy
    sequences fall back to U_root = Fs2 * (range / |q_finest|).
Decision for the root at tolerance tau:
    FAIL         |q_root - q_finest| / |q_finest| > tau   (demonstrated change)
    PASS         U_root <= pass_fraction * tau
    INCONCLUSIVE otherwise
"""

from __future__ import annotations

import math

from .base import CheckResult, Status


def observed_order(eps32: float, eps21: float, r21: float, r32: float, p0: float) -> tuple[float | None, int]:
    """Celik et al. (2008) fixed-point iteration for the apparent order."""
    if eps21 == 0 or eps32 == 0:
        return None, 0
    s = 1.0 if eps32 / eps21 > 0 else -1.0
    p = p0
    for it in range(1, 101):
        try:
            qp = math.log((r21**p - s) / (r32**p - s))
            p_new = abs(math.log(abs(eps32 / eps21)) + qp) / math.log(r21)
        except (ValueError, ZeroDivisionError, OverflowError):
            return None, it
        if abs(p_new - p) < 1e-8:
            return p_new, it
        p = p_new
    return p, 100


def assess_sequence(
    *,
    check: str,
    component: str,
    qoi: str,
    values: list[float],
    sizes: list[float],
    run_ids: list[str],
    formal_order: float,
    tau: float,
    cfg: dict,
    noise: float = 0.0,
    notes: list[str] | None = None,
    factor_label: str = "h",
) -> CheckResult:
    """``sizes`` are the controlling length/time scale per run (coarse -> fine, decreasing).

    For a domain study pass the *inverse* domain size so that it decreases.
    """
    sens = cfg["sensitivity"]
    frac = cfg["error_budget"]["component_pass_fraction"]
    fs2, fs3 = sens["safety_factor_two_level"], sens["safety_factor_three_level"]
    lo, hi = sens["observed_order_band"]
    details: dict = {"values": values, factor_label: sizes, "formal_order": formal_order, "notes": notes or []}
    if len(values) < 2 or any(v is None for v in values):
        return CheckResult(check, Status.INCONCLUSIVE, f"need at least two completed runs with a value of {qoi}",
                           qoi=qoi, component=component, runs=run_ids, details=details)
    q_root, q_fine = values[0], values[-1]
    if q_fine == 0:
        return CheckResult(check, Status.INCONCLUSIVE, "finest value is zero; relative error undefined",
                           qoi=qoi, component=component, runs=run_ids, details=details)
    change = abs(q_fine - q_root) / abs(q_fine)
    details["root_to_finest_change"] = change
    ratios = [sizes[i] / sizes[i + 1] for i in range(len(sizes) - 1)]
    details["refinement_ratios"] = ratios
    if any(r < sens["min_refinement_ratio"] for r in ratios):
        details["notes"].append(f"refinement ratio below {sens['min_refinement_ratio']} (Celik et al. 2008)")

    method = ""
    if len(values) == 2:
        r = ratios[0]
        p = formal_order
        e_root = change * r**p / (r**p - 1.0)
        u_root = fs2 * e_root
        method = f"two-level Richardson, assumed order p={p:g}, Fs={fs2:g}"
        details.update(estimated_root_error=e_root)
    else:
        q3, q2, q1 = values[0], values[-2], values[-1]
        h3, h2, h1 = sizes[0], sizes[-2], sizes[-1]
        r32, r21 = h3 / h2, h2 / h1
        eps32, eps21 = q3 - q2, q2 - q1
        scale = abs(q1)
        if max(abs(eps32), abs(eps21)) / scale <= 2.0 * noise:
            u_root = fs2 * max(change, noise)
            method = f"differences within 2x statistical noise ({noise:.1e}); range-based U with Fs={fs2:g}"
        elif eps32 * eps21 < 0:
            rng = (max(values) - min(values)) / scale
            u_root = fs2 * rng
            method = f"oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs={fs2:g}"
            details["oscillatory"] = True
        else:
            p_obs, n_it = observed_order(eps32, eps21, r21, r32, formal_order)
            details.update(observed_order=p_obs, iterations=n_it)
            if p_obs is not None and lo * formal_order <= p_obs <= hi * formal_order:
                p, fs = p_obs, fs3
                method = f"three-level Celik procedure, observed order p={p_obs:.2f}, Fs={fs3:g}"
            else:
                p, fs = formal_order, fs2
                method = (f"three-level, observed order {p_obs if p_obs is None else round(p_obs, 2)} outside "
                          f"[{lo}, {hi}]x formal; formal order p={formal_order:g} with Fs={fs2:g}")
            q_ext = (r21**p * q1 - q2) / (r21**p - 1.0)
            e_root = abs(q3 - q_ext) / abs(q_ext)
            u_root = fs * e_root
            details.update(extrapolated_value=q_ext, estimated_root_error=e_root)
    details["method"] = method
    src = "Roache (1998); Celik et al. (2008) J. Fluids Eng. 130:078001"
    if change > tau:
        return CheckResult(check, Status.FAIL,
                           f"{qoi} of the run under verification changes by {change:.2%} under {component} refinement "
                           f"(> tau={tau:.0%}); its value is not converged to the requested tolerance [{method}]",
                           value=change, threshold=tau, source=src, qoi=qoi, component=component,
                           uncertainty=u_root, runs=run_ids, details=details)
    if u_root <= frac * tau:
        return CheckResult(check, Status.PASS,
                           f"estimated {component} uncertainty of {qoi} = {u_root:.2%} <= {frac*tau:.2%} "
                           f"(root-to-finest change {change:.3%}) [{method}]",
                           value=u_root, threshold=frac * tau, source=src, qoi=qoi, component=component,
                           uncertainty=u_root, runs=run_ids, details=details)
    return CheckResult(check, Status.INCONCLUSIVE,
                       f"estimated {component} uncertainty of {qoi} = {u_root:.2%} > {frac*tau:.2%} but the demonstrated "
                       f"change {change:.2%} <= tau; more refinement would be needed [{method}]",
                       value=u_root, threshold=frac * tau, source=src, qoi=qoi, component=component,
                       uncertainty=u_root, runs=run_ids, details=details)
