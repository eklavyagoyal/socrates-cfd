"""From SDF geometry to solver grids: sampling, solid masks and wall-link fractions.

This is the single bridge between geometry and every grid solver (ADR-0002). No
body-fitted mesh is ever built: solvers see

- ``sample``: the signed distance at each cell centre;
- ``solid_mask``: ``d < 0`` per cell;
- ``link_fractions``: for each fluid node and lattice direction whose neighbour is solid,
  the fraction ``q`` in (0, 1] of the link at which the wall lies (root of the SDF along
  the link). Interpolated bounce-back (Bouzidi), immersed boundaries and cut-cell
  methods all need exactly this.
"""

from __future__ import annotations

import torch

from physis.core.backend import Backend
from physis.core.grid import Grid
from physis.geometry.sdf import SDF

Tensor = torch.Tensor

_CHUNK = 1 << 20  # points per evaluation chunk (bounds peak memory on large 3D grids)


def evaluate_points(sdf: SDF, points: Tensor) -> Tensor:
    """Evaluate ``sdf`` on ``points`` (..., ndim) in chunks."""
    flat = points.reshape(-1, points.shape[-1])
    if flat.shape[0] <= _CHUNK:
        return sdf(flat).reshape(points.shape[:-1])
    out = torch.empty(flat.shape[0], dtype=points.dtype, device=points.device)
    for i in range(0, flat.shape[0], _CHUNK):
        out[i : i + _CHUNK] = sdf(flat[i : i + _CHUNK])
    return out.reshape(points.shape[:-1])


def sample(sdf: SDF, grid: Grid, backend: Backend) -> Tensor:
    """Signed distance at every cell centre, shape ``grid.shape``."""
    if sdf.ndim != grid.ndim:
        raise ValueError(f"geometry is {sdf.ndim}D but grid is {grid.ndim}D")
    return evaluate_points(sdf, grid.centers(backend))


def solid_mask(sdf: SDF, grid: Grid, backend: Backend) -> Tensor:
    """Boolean mask of cells whose centre lies inside the solid (``d < 0``)."""
    return sample(sdf, grid, backend) < 0


def link_fractions(
    sdf: SDF,
    grid: Grid,
    velocities: Tensor,
    backend: Backend,
    *,
    solid: Tensor | None = None,
    iterations: int = 48,
) -> Tensor:
    """Wall position along every fluid→solid lattice link.

    Args:
        velocities: integer lattice directions, shape ``(Q, ndim)``.
        solid: precomputed ``solid_mask`` (computed if None).
        iterations: bisection steps (48 halvings resolve q to ~1e-14 of a link).

    Returns:
        Tensor ``(Q, *grid.shape)``: ``q`` in (0, 1] where node ``x`` is fluid and
        ``x + c_i`` is a solid node inside the grid, ``NaN`` everywhere else. ``q`` is the
        distance from the fluid node to the wall in units of the link length
        ``|c_i| * h`` (Bouzidi convention).

    Neighbours outside the grid are not links to geometry (domain boundaries belong to
    the solver's boundary conditions).
    """
    if solid is None:
        solid = solid_mask(sdf, grid, backend)
    c = velocities.to(device=backend.device, dtype=torch.long)
    q_out = backend.full((c.shape[0], *grid.shape), float("nan"))
    centers = grid.centers(backend)
    fluid = ~solid
    shape = torch.tensor(grid.shape, device=backend.device)
    idx = torch.nonzero(fluid)  # (N, ndim)
    for i in range(c.shape[0]):
        ci = c[i]
        if torch.all(ci == 0):
            continue
        nb = idx + ci
        inside = torch.all((nb >= 0) & (nb < shape), dim=1)
        src, nbi = idx[inside], nb[inside]
        hits = solid[tuple(nbi.T)]
        if not torch.any(hits):
            continue
        src = src[hits]
        x0 = centers[tuple(src.T)]  # fluid node, d >= 0
        step = ci.to(backend.dtype) * grid.spacing
        lo = torch.zeros(src.shape[0], dtype=backend.dtype, device=backend.device)
        hi = torch.ones_like(lo)
        for _ in range(iterations):
            mid = 0.5 * (lo + hi)
            d = sdf(x0 + mid[:, None] * step)
            inside_mid = d < 0
            hi = torch.where(inside_mid, mid, hi)
            lo = torch.where(inside_mid, lo, mid)
        q = 0.5 * (lo + hi)
        q_out[i][tuple(src.T)] = q
    return q_out
