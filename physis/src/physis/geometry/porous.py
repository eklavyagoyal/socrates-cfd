"""Periodic porous micro-structures for representative volume elements (ADR-0008).

Three families, each a regular SDF node (so they voxelise, hash and serialise like any
other geometry) and each periodic in a box ``[0, L)^3``:

- ``periodic_spheres`` with ``voids=False``: overlapping solid spheres (a sintered
  particle bed in the Boolean model);
- ``periodic_spheres`` with ``voids=True``: overlapping spherical *pores* in a solid matrix
  (templated porosity, e.g. burnt-out polymer spheres);
- ``gyroid``: a gyroid network solid (TPMS lattice).

Sphere sets are generated from ``(count, radius, radius_spread, seed)`` so a spec stays small
and reproducible. Periodicity uses the minimum-image convention.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import torch

from physis.geometry.sdf import SDF, register_node

Tensor = torch.Tensor

_CENTER_CHUNK = 64


@register_node
class PeriodicSpheres(SDF):
    type_name = "periodic_spheres"

    def __init__(self, box: Sequence[float], count: int, radius: float, *, radius_spread: float = 0.0,
                 seed: int = 0, voids: bool = False):
        self.box = tuple(float(b) for b in box)
        if len(self.box) != 3 or any(b <= 0 for b in self.box):
            raise ValueError("box must be three positive lengths")
        if count < 1 or not radius > 0 or not 0 <= radius_spread < 1:
            raise ValueError("need count >= 1, radius > 0 and 0 <= radius_spread < 1")
        self.ndim = 3
        self.count, self.radius, self.radius_spread = int(count), float(radius), float(radius_spread)
        self.seed, self.voids = int(seed), bool(voids)
        rng = np.random.default_rng(self.seed)
        self.centers = rng.random((self.count, 3)) * np.asarray(self.box)
        self.radii = self.radius * (1.0 + self.radius_spread * (2.0 * rng.random(self.count) - 1.0))

    def eval(self, p: Tensor) -> Tensor:
        box = p.new_tensor(self.box)
        centers = p.new_tensor(self.centers)
        radii = p.new_tensor(self.radii)
        best = torch.full(p.shape[:-1], math.inf, dtype=p.dtype, device=p.device)
        for k in range(0, self.count, _CENTER_CHUNK):
            c, r = centers[k:k + _CENTER_CHUNK], radii[k:k + _CENTER_CHUNK]
            d2 = torch.zeros(*p.shape[:-1], c.shape[0], dtype=p.dtype, device=p.device)
            for a in range(3):
                da = p[..., a, None] - c[:, a]
                da = da - box[a] * torch.round(da / box[a])
                d2 = d2 + da * da
            best = torch.minimum(best, (torch.sqrt(d2) - r).amin(dim=-1))
        return -best if self.voids else best

    def to_spec(self):
        return {"type": self.type_name, "box": list(self.box), "count": self.count, "radius": self.radius,
                "radius_spread": self.radius_spread, "seed": self.seed, "voids": self.voids}

    @classmethod
    def from_spec(cls, s):
        return cls(s["box"], s["count"], s["radius"], radius_spread=s.get("radius_spread", 0.0),
                   seed=s.get("seed", 0), voids=s.get("voids", False))


@register_node
class Gyroid(SDF):
    """Gyroid network solid where ``f(p) > level``; ``periods`` unit cells across the box.

    The distance is the first-order estimate ``(level - f) / |grad f|``: exact sign, accurate
    near the surface, which is all voxelisation and surface estimates need.
    """

    type_name = "gyroid"

    def __init__(self, box: Sequence[float], periods: int = 1, level: float = 0.0):
        self.box = tuple(float(b) for b in box)
        if len(self.box) != 3 or periods < 1 or not -1.5 < level < 1.5:
            raise ValueError("need a 3D box, periods >= 1 and -1.5 < level < 1.5")
        self.ndim, self.periods, self.level = 3, int(periods), float(level)

    def eval(self, p: Tensor) -> Tensor:
        k = [2 * math.pi * self.periods / b for b in self.box]
        x, y, z = p[..., 0] * k[0], p[..., 1] * k[1], p[..., 2] * k[2]
        sx, cx, sy, cy, sz, cz = torch.sin(x), torch.cos(x), torch.sin(y), torch.cos(y), torch.sin(z), torch.cos(z)
        f = sx * cy + sy * cz + sz * cx
        gx = k[0] * (cx * cy - sz * sx)
        gy = k[1] * (-sx * sy + cy * cz)
        gz = k[2] * (-sy * sz + cz * cx)
        grad = torch.sqrt(gx * gx + gy * gy + gz * gz).clamp_min(1e-6 * max(k))
        return (self.level - f) / grad

    def to_spec(self):
        return {"type": self.type_name, "box": list(self.box), "periods": self.periods, "level": self.level}

    @classmethod
    def from_spec(cls, s):
        return cls(s["box"], s.get("periods", 1), s.get("level", 0.0))


def spheres_for_porosity(box: Sequence[float], porosity: float, radius: float, voids: bool) -> int:
    """Sphere count that gives ``porosity`` in expectation (Boolean model: the uncovered
    fraction is ``exp(-n v)``; for voids the uncovered fraction is the solid)."""
    v = 4.0 / 3.0 * math.pi * radius**3
    volume = math.prod(box)
    covered = porosity if voids else 1.0 - porosity
    return max(1, round(-math.log(1.0 - covered) * volume / v))
