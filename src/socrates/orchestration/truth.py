"""In-house converged reference ("truth") and ground-truth labelling.

Truth = baseline stationary value + sum over factors (mesh, time, domain) of
(three-level Richardson-extrapolated value - baseline value), i.e. the usual
assumption that small error contributions are additive.  Each factor's
extrapolation uses the Celik et al. (2008) procedure on that factor's
one-at-a-time refinement chain.  When a chain does not converge
monotonically, the finest value is used and the range is carried into the
truth uncertainty.  The truth is used ONLY for labelling and validation,
never by the verifier or the critic.
"""

from __future__ import annotations

import math

from ..checks.sensitivity import observed_order


def extrapolate_chain(values: list[float], sizes: list[float], formal_order: float) -> dict:
    """values/sizes ordered coarse -> fine (3 levels)."""
    q3, q2, q1 = values
    h3, h2, h1 = sizes
    r32, r21 = h3 / h2, h2 / h1
    e32, e21 = q3 - q2, q2 - q1
    out = {"values": values, "sizes": sizes}
    if e32 == 0 or e21 == 0 or e32 * e21 < 0 or abs(e21) >= abs(e32):
        out.update(method="non-monotone, divergent or exact: finest value", extrapolated=q1, order=None,
                   uncertainty=abs(max(values) - min(values)))
        return out
    p, _ = observed_order(e32, e21, r21, r32, formal_order)
    if p is None or not (0.5 * formal_order <= p <= 2.0 * formal_order):
        p_use, fs = formal_order, 3.0
        method = f"observed order {p} outside band; formal order {formal_order} with Fs=3"
    else:
        p_use, fs = p, 1.25
        method = f"Richardson with observed order {p:.2f}, Fs=1.25"
    q_ext = (r21**p_use * q1 - q2) / (r21**p_use - 1.0)
    out.update(method=method, extrapolated=q_ext, order=p, uncertainty=fs * abs(q_ext - q1))
    return out


def combine_truth(root_value: float, chains: dict[str, dict]) -> dict:
    corr = {k: c["extrapolated"] - root_value for k, c in chains.items()}
    value = root_value + sum(corr.values())
    unc = math.sqrt(sum(c["uncertainty"] ** 2 for c in chains.values()))
    return {"value": value, "uncertainty_abs": unc, "uncertainty_rel": unc / abs(value), "corrections": corr}


def label_case(reported: dict, truth: dict[str, float], tolerances: dict[str, float],
               setup_problems: list[str] | None = None, truth_uncertainty: dict[str, float] | None = None) -> dict:
    """Pre-registered rule, with the pre-registered mitigation for truth uncertainty.

    e_q = |reported_q - T_q| / T_q, ratio = max_q e_q / tau_q.
      flawed     ratio > 1, a requested quantity is missing, or the set-up solves a different problem
      credible   ratio <= 1/2
      ambiguous  otherwise
    If the interval [e - u_T, e + u_T] (u_T = relative truth uncertainty) straddles tau or tau/2 for any
    quantity, the label is not determined by the evidence: such a case is labelled 'ambiguous' and flagged
    label_unstable (setup problems still make it 'flawed').
    """
    u = truth_uncertainty or {}
    errs, missing, unstable = {}, [], []
    for q, tau in tolerances.items():
        v = reported.get(q)
        if v is None:
            missing.append(q)
            continue
        e = abs(v - truth[q]) / abs(truth[q])
        errs[q] = e
        uq = u.get(q, 0.0)
        for thr in (tau, 0.5 * tau):
            if e - uq < thr < e + uq:
                unstable.append(q)
                break
    ratio = max((errs[q] / tolerances[q] for q in errs), default=0.0)
    reasons = list(setup_problems or [])
    if missing:
        reasons.append(f"requested quantities not produced: {missing}")
    clearly_flawed = any(errs[q] - u.get(q, 0.0) > tolerances[q] for q in errs)
    if reasons or clearly_flawed:
        label = "flawed"
    elif unstable:
        label = "ambiguous"
    elif ratio > 1.0:
        label = "flawed"
    elif ratio <= 0.5:
        label = "credible"
    else:
        label = "ambiguous"
    return {"label": label, "errors": errs, "max_error_over_tolerance": ratio, "setup_problems": reasons,
            "label_unstable": sorted(set(unstable)), "truth_uncertainty": u}
