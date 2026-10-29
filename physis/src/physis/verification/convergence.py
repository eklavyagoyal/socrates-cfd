"""Minimal convergence helpers used by the solver gates.

The full Richardson/GCI machinery (Celik procedure, safety factors, oscillatory
convergence handling) lives in ``physis.verification.richardson``; this module only has
the two functions gate tests need everywhere.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def observed_order(spacings: Sequence[float], errors: Sequence[float]) -> float:
    """Least-squares slope of log(error) against log(spacing).

    With errors measured against an exact solution this is the observed order of
    accuracy. Needs at least two levels and positive errors.
    """
    h = np.asarray(spacings, dtype=float)
    e = np.asarray(errors, dtype=float)
    if h.size < 2 or h.size != e.size:
        raise ValueError("need >= 2 matching spacings and errors")
    if np.any(e <= 0) or np.any(h <= 0):
        raise ValueError("spacings and errors must be positive")
    slope, _ = np.polyfit(np.log(h), np.log(e), 1)
    return float(slope)


def relative_error(value: float, reference: float) -> float:
    return abs(value - reference) / abs(reference)
