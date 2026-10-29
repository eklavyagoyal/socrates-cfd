"""Uniform Cartesian grids (2D or 3D), cell-centred.

Convention used by every solver and by geometry sampling:

- Arrays on a grid have shape ``grid.shape`` = ``(nx, ny)`` or ``(nx, ny, nz)``, x first
  (``indexing="ij"``).
- Cell ``i`` along an axis spans ``[origin + i*h, origin + (i+1)*h]``; its node (the point
  where values live, and the lattice node for LBM) is the cell centre
  ``origin + (i + 0.5) * h``.
- Spacing ``h`` is the same on all axes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch

from physis.core.backend import Backend


@dataclass(frozen=True)
class Grid:
    shape: tuple[int, ...]
    spacing: float
    origin: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.shape) not in (2, 3):
            raise ValueError(f"grid must be 2D or 3D, got shape {self.shape}")
        if len(self.origin) != len(self.shape):
            raise ValueError("origin and shape must have the same length")
        if any(n < 1 for n in self.shape):
            raise ValueError(f"every axis needs at least one cell, got {self.shape}")
        if not (self.spacing > 0 and math.isfinite(self.spacing)):
            raise ValueError(f"spacing must be positive and finite, got {self.spacing}")
        object.__setattr__(self, "shape", tuple(int(n) for n in self.shape))
        object.__setattr__(self, "origin", tuple(float(o) for o in self.origin))
        object.__setattr__(self, "spacing", float(self.spacing))

    # --- construction -------------------------------------------------------------

    @classmethod
    def from_bounds(cls, lo: tuple[float, ...], hi: tuple[float, ...], spacing: float) -> Grid:
        """Grid covering ``[lo, hi]`` with ``round((hi-lo)/h)`` cells per axis.

        Raises if an extent is not an integer multiple of ``spacing`` (to 1e-9 relative),
        because silently stretching the domain changes the problem being solved.
        """
        shape = []
        for a, b in zip(lo, hi, strict=True):
            n_float = (b - a) / spacing
            n = round(n_float)
            if n < 1 or abs(n_float - n) > 1e-9 * max(1.0, abs(n_float)):
                raise ValueError(f"extent {b - a} is not a multiple of spacing {spacing}")
            shape.append(n)
        return cls(tuple(shape), spacing, tuple(lo))

    @classmethod
    def from_dict(cls, d: dict) -> Grid:
        return cls(tuple(d["shape"]), d["spacing"], tuple(d["origin"]))

    def to_dict(self) -> dict:
        return {"shape": list(self.shape), "spacing": self.spacing, "origin": list(self.origin)}

    def refined(self, ratio: int) -> Grid:
        """Same domain, ``ratio`` times as many cells per axis."""
        if ratio < 1:
            raise ValueError("ratio must be >= 1")
        return Grid(tuple(n * ratio for n in self.shape), self.spacing / ratio, self.origin)

    # --- geometry -----------------------------------------------------------------

    @property
    def ndim(self) -> int:
        return len(self.shape)

    @property
    def size(self) -> int:
        return math.prod(self.shape)

    @property
    def lower(self) -> tuple[float, ...]:
        return self.origin

    @property
    def upper(self) -> tuple[float, ...]:
        return tuple(o + n * self.spacing for o, n in zip(self.origin, self.shape))

    @property
    def extent(self) -> tuple[float, ...]:
        return tuple(n * self.spacing for n in self.shape)

    @property
    def cell_volume(self) -> float:
        return self.spacing**self.ndim

    def axes(self, backend: Backend) -> list[torch.Tensor]:
        """1D tensors of cell-centre coordinates per axis."""
        h = self.spacing
        return [
            backend.tensor(o) + (backend.arange(n) + 0.5) * h
            for o, n in zip(self.origin, self.shape)
        ]

    def centers(self, backend: Backend) -> torch.Tensor:
        """Cell-centre coordinates, shape ``(*shape, ndim)``."""
        mesh = torch.meshgrid(*self.axes(backend), indexing="ij")
        return torch.stack(mesh, dim=-1)

    def index_of(self, point: tuple[float, ...]) -> tuple[int, ...]:
        """Index of the cell containing ``point`` (clamped to the grid)."""
        idx = []
        for p, o, n in zip(point, self.origin, self.shape):
            i = int(math.floor((p - o) / self.spacing))
            idx.append(min(max(i, 0), n - 1))
        return tuple(idx)
