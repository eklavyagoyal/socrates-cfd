"""Porous RVE geometry: periodicity, porosity targets, structure descriptors."""

from __future__ import annotations

import math

import torch

from physis.core.grid import Grid
from physis.data.porous_features import describe, kozeny_carman
from physis.geometry import Gyroid, PeriodicSpheres, from_spec, sample, spheres_for_porosity


def test_periodic_spheres_wrap_and_roundtrip(cpu64):
    s = PeriodicSpheres((10.0, 10.0, 10.0), 1, 2.0, seed=3)
    c = torch.tensor(s.centers[0])
    p = torch.stack([c, c + torch.tensor([10.0, 0.0, 0.0]), c - torch.tensor([0.0, 10.0, 10.0])])
    d = s(p)
    assert torch.allclose(d, torch.full((3,), -2.0, dtype=torch.float64))  # same point under periodic images
    again = from_spec(s.to_spec())
    assert torch.allclose(again(p), d)
    voids = PeriodicSpheres((10.0, 10.0, 10.0), 1, 2.0, seed=3, voids=True)
    assert torch.allclose(voids(p), -d)


def test_specific_surface_of_a_sphere(cpu64):
    L, r = 48, 12.0
    grid = Grid((L, L, L), 1.0, (0.0, 0.0, 0.0))
    geom = {"type": "ball", "center": [L / 2] * 3, "radius": r}
    f = describe(geom, grid, cpu64)
    area = f["specific_surface"] * L**3
    assert abs(area / (4 * math.pi * r * r) - 1) < 0.03
    assert abs((1 - f["porosity"]) / (4 / 3 * math.pi * r**3 / L**3) - 1) < 0.02


def test_boolean_model_hits_target_porosity(cpu64):
    L = 64
    grid = Grid((L, L, L), 1.0, (0.0, 0.0, 0.0))
    for voids in (False, True):
        n = spheres_for_porosity((L, L, L), 0.6, 6.0, voids)
        geom = {"type": "periodic_spheres", "box": [L, L, L], "count": n, "radius": 6.0, "seed": 1, "voids": voids}
        phi = describe(geom, grid, cpu64)["porosity"]
        assert abs(phi - 0.6) < 0.06


def test_gyroid_level_controls_porosity(cpu64):
    grid = Grid((32, 32, 32), 1.0, (0.0, 0.0, 0.0))
    phis = [float((sample(Gyroid((32.0, 32.0, 32.0), 1, t), grid, cpu64) >= 0).double().mean()) for t in (-0.6, 0.0, 0.6)]
    assert phis[0] < phis[1] < phis[2]
    assert abs(phis[1] - 0.5) < 0.03


def test_kozeny_carman_formula():
    d, phi = 1.0, 0.4
    s = 6 * (1 - phi) / d  # spheres of diameter d
    assert abs(kozeny_carman(phi, s) - phi**3 * d**2 / (180 * (1 - phi) ** 2)) < 1e-15
