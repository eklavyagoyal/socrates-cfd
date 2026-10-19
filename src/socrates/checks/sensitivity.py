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
    observed order p (bracketed root of Celik's equation), monotone/oscillatory
    test via sign(eps32/eps21), extrapolated value q_ext,
    U_root = Fs*|q_3-q_ext|/|q_ext| with Fs = 1.25 when p is within the band
    around the formal order, otherwise Fs = 3 with p = min(observed, formal)
    (never extrapolate slow convergence with a fast order).  No positive
    observed order -> INCONCLUSIVE.  Oscillatory or noise-level sequences use
    U_root = Fs2 * (range / |q_finest|).  Both estimates are floored at
    Fs2 * statistical noise, and a FAIL needs the change to exceed tau by more
    than twice the noise.  Degenerate families (equal sizes) -> INCONCLUSIVE.
Decision for the root at tolerance tau:
    FAIL         |q_root - q_finest| / |q_finest| > tau   (demonstrated change)
    PASS         U_root <= pass_fraction * tau
    INCONCLUSIVE otherwise
"""

from __future__ import annotations

import math

from .base import CheckResult, Status


def observed_order(eps32: float, eps21: float, r21: float, r32: float, p0: float,
                   p_max: float = 10.0) -> tuple[float | None, int]:
    """Apparent order from Celik et al. (2008):  p = |ln|eps32/eps21| + q(p)| / ln r21.

    Solved as a root of g(p) = p ln r21 - |ln|eps32/eps21| + q(p)| on (0, p_max]
    by sign-change bracketing + bisection, so an unconverged iterate is never
    returned (the plain fixed-point map oscillates when r32 > r21^2).  Returns
    (None, n) when no positive order solves the equation.
    """
    if eps21 == 0 or eps32 == 0 or r21 <= 1.0 or r32 <= 1.0:
        return None, 0
    s = 1.0 if eps32 / eps21 > 0 else -1.0
    lnr = math.log(abs(eps32 / eps21))

    def g(p: float) -> float | None:
        try:
            return p * math.log(r21) - abs(lnr + math.log((r21**p - s) / (r32**p - s)))
        except (ValueError, ZeroDivisionError, OverflowError):
            return None

    grid = [1e-3 * (p_max / 1e-3) ** (i / 400) for i in range(401)]  # log-spaced
    prev_p, prev_g = None, None
    for p in grid:
        gp = g(p)
        if gp is None:
            prev_p, prev_g = None, None
            continue
        if prev_g is not None and (prev_g == 0 or prev_g * gp < 0):
            a, b, ga = prev_p, p, prev_g
            for it in range(200):
                m = 0.5 * (a + b)
                gm = g(m)
                if gm is None:
                    return None, it
                if ga * gm <= 0:
                    b = m
                else:
                    a, ga = m, gm
                if b - a < 1e-10:
                    return 0.5 * (a + b), it
            return 0.5 * (a + b), 200
        prev_p, prev_g = p, gp
    return None, len(grid)


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
    if any(r <= 1.0 + 1e-6 for r in ratios):
        return CheckResult(check, Status.INCONCLUSIVE,
                           f"degenerate {component} family: two runs at the same refinement level ({ratios})",
                           qoi=qoi, component=component, runs=run_ids, details=details)
    if len(values) == 2:
        r = ratios[0]
        p = formal_order
        e_root = change * r**p / (r**p - 1.0)
        u_root = max(fs2 * e_root, fs2 * noise)  # a difference below the statistical noise proves nothing
        method = f"two-level Richardson, assumed order p={p:g}, Fs={fs2:g} (noise floor {noise:.1e})"
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
            if p_obs is None:
                return CheckResult(check, Status.INCONCLUSIVE,
                                   f"monotone {component} sequence but no positive observed order solves the Celik "
                                   f"equation: not in the asymptotic range", qoi=qoi, component=component,
                                   runs=run_ids, details=details)
            if lo * formal_order <= p_obs <= hi * formal_order:
                p, fs = p_obs, fs3
                method = f"three-level Celik procedure, observed order p={p_obs:.2f}, Fs={fs3:g}"
            else:
                # outside the asymptotic band: use the SMALLER of observed and formal order
                # (slow convergence must not be extrapolated with a fast order) and Fs=3
                p, fs = min(p_obs, formal_order), fs2
                method = (f"three-level, observed order {p_obs:.2f} outside [{lo}, {hi}]x formal; "
                          f"p=min(observed, formal)={p:.2f} with Fs={fs2:g}")
            q_ext = (r21**p * q1 - q2) / (r21**p - 1.0)
            e_root = abs(q3 - q_ext) / abs(q_ext)
            u_root = max(fs * e_root, fs2 * noise)
            details.update(extrapolated_value=q_ext, estimated_root_error=e_root)
    details["method"] = method
    src = "Roache (1998); Celik et al. (2008) J. Fluids Eng. 130:078001"
    details["noise"] = noise
    if change - 2.0 * noise > tau:  # demonstrated beyond the statistical noise of the two runs
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
