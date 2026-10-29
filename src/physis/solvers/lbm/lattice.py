"""D3Q19 velocity set.

Order: rest, the six axis directions, then the twelve edge diagonals, arranged so that
every direction ``i >= 1`` and its opposite are neighbours (``OPP[1] == 2``,
``OPP[2] == 1``...). The Metal kernel in :mod:`physis.solvers.lbm.metal` uses the same
order; ``tests/test_lbm.py`` checks both.
"""

from __future__ import annotations

import torch

from physis.core.backend import Backend

C = (
    (0, 0, 0),
    (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
    (1, 1, 0), (-1, -1, 0), (1, -1, 0), (-1, 1, 0),
    (1, 0, 1), (-1, 0, -1), (1, 0, -1), (-1, 0, 1),
    (0, 1, 1), (0, -1, -1), (0, 1, -1), (0, -1, 1),
)
Q = len(C)
W = (1.0 / 3.0,) + (1.0 / 18.0,) * 6 + (1.0 / 36.0,) * 12
OPP = tuple(C.index(tuple(-c for c in ci)) for ci in C)
CS2 = 1.0 / 3.0  # lattice speed of sound squared

MAGIC = 3.0 / 16.0
"""TRT magic parameter: with half-way bounce-back the wall sits exactly midway between
nodes for Poiseuille-type flows, and steady solutions do not depend on viscosity."""


def tau_minus(tau_plus: float, magic: float = MAGIC) -> float:
    """Antisymmetric relaxation time from ``(tau+ - 1/2)(tau- - 1/2) = magic``."""
    if tau_plus <= 0.5:
        raise ValueError(f"tau_plus must exceed 1/2, got {tau_plus}")
    return 0.5 + magic / (tau_plus - 0.5)


def viscosity(tau_plus: float) -> float:
    """Kinematic viscosity in lattice units."""
    return CS2 * (tau_plus - 0.5)


def tensors(backend: Backend) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """``(c, w, opp)`` on the backend: c is (19, 3) in the working dtype, w is (19,), opp is long."""
    c = backend.tensor(C)
    w = backend.tensor(W)
    opp = torch.tensor(OPP, dtype=torch.long, device=backend.device)
    return c, w, opp
