"""Structure descriptors of a porous RVE, computed from its SDF on the solver grid.

- ``porosity``: fluid fraction of the voxelised cell (what the solver actually sees);
- ``specific_surface``: pore-solid interface area per bulk volume, from the SDF band
  estimate ``A ~ (h^2 / 2) * #{cells with |d| < h}`` (smoothed-delta integral of the surface;
  checked against 4 pi r^2 in the tests);
- ``hydraulic_diameter``: ``4 * porosity / specific_surface``;
- ``kozeny_carman``: ``porosity^3 / (c * S^2)`` with the Kozeny constant ``c`` (5 for packed
  beds) — the classical baseline the learned models have to beat.
"""

from __future__ import annotations

import torch

from physis.core.backend import Backend
from physis.core.grid import Grid
from physis.geometry import from_spec, sample


def describe(geometry: dict, grid: Grid, backend: Backend) -> dict[str, float]:
    d = sample(from_spec(geometry), grid, backend)
    h = grid.spacing
    porosity = float((d >= 0).sum()) / grid.size
    band = int((d.abs() < h).sum())
    area = 0.5 * h * h * band
    volume = grid.size * grid.cell_volume
    s = area / volume
    return {
        "porosity": porosity,
        "specific_surface": s,
        "hydraulic_diameter": 4.0 * porosity / s if s > 0 else float("inf"),
    }


def kozeny_carman(porosity: float, specific_surface: float, constant: float = 5.0) -> float:
    return porosity**3 / (constant * specific_surface**2)


def solid_fraction_field(geometry: dict, grid: Grid, backend: Backend, factor: int) -> torch.Tensor:
    """Solid fraction averaged over ``factor^3`` blocks: the input of the 3D-CNN surrogate."""
    solid = (sample(from_spec(geometry), grid, backend) < 0).to(backend.dtype)
    return torch.nn.functional.avg_pool3d(solid[None, None], factor)[0, 0]
