"""Pore-scale RVE samples: random porous structures, their descriptors and their permeability.

One sample = one periodic unit cube (box length 1) with a random structure from one of the
families in :mod:`physis.geometry.porous`, voxelised at ``n^3``, flowed through with the
D3Q19 TRT solver in the Darcy regime. Rows carry the geometry spec (reproducible from the
seed), descriptors, the measured permeability, the Kozeny–Carman estimate and run
diagnostics, so a dataset can be audited and re-run sample by sample.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from physis.core.backend import Backend
from physis.core.grid import Grid
from physis.data.porous_features import describe, kozeny_carman
from physis.geometry import spheres_for_porosity
from physis.solvers.lbm import PeriodicFlow, PeriodicFlowSpec, lattice

FAMILIES = ("spheres", "voids", "gyroid")
BOX = 1.0


def random_structure(index: int, family: str | None = None, *, seed_offset: int = 0) -> dict[str, Any]:
    """Geometry spec of sample ``index`` (deterministic). Families rotate unless given."""
    rng = np.random.default_rng(10_007 * (index + 1) + seed_offset)
    fam = family or FAMILIES[index % len(FAMILIES)]
    box = [BOX, BOX, BOX]
    if fam in ("spheres", "voids"):
        voids = fam == "voids"
        porosity = rng.uniform(0.35, 0.85) if not voids else rng.uniform(0.35, 0.80)
        radius = rng.uniform(0.05, 0.12) * BOX
        spread = rng.uniform(0.0, 0.4)
        count = spheres_for_porosity(box, porosity, radius, voids)
        return {"type": "periodic_spheres", "box": box, "count": count, "radius": float(radius),
                "radius_spread": float(spread), "seed": int(rng.integers(1 << 31)), "voids": voids}
    if fam == "gyroid":
        return {"type": "gyroid", "box": box, "periods": int(rng.integers(1, 3)), "level": float(rng.uniform(-0.9, 0.9))}
    raise ValueError(f"unknown family {fam!r}")


def family_of(geometry: dict[str, Any]) -> str:
    if geometry["type"] == "gyroid":
        return "gyroid"
    return "voids" if geometry.get("voids") else "spheres"


def check_interval(n: int, nu: float) -> int:
    """Steps between convergence checks: about one pore-scale decay time (pores ~ n/10 cells),
    so a small change per window really means steady."""
    return max(100, int((n / 10) ** 2 / (math.pi**2 * nu) * 4))


def run_rve(geometry: dict[str, Any], n: int, backend: Backend, *, target_velocity: float = 2e-4,
            tau_plus: float = 1.5, tol: float = 1e-6, impl: str = "auto", max_steps: int = 400_000,
            force: float | None = None) -> dict[str, Any]:
    """Descriptors and Darcy permeability of one structure at ``n^3`` (box length 1)."""
    grid = Grid((n, n, n), BOX / n, (0.0, 0.0, 0.0))
    feats = describe(geometry, grid, backend)
    h = grid.spacing
    k_kc = kozeny_carman(feats["porosity"], feats["specific_surface"]) if feats["specific_surface"] > 0 else float("nan")
    nu = lattice.viscosity(tau_plus)
    if force is None:  # aim the superficial velocity at target_velocity using the KC estimate
        k_kc_lu = k_kc / (h * h) if math.isfinite(k_kc) and k_kc > 0 else 1.0
        force = min(1e-3, target_velocity * nu / k_kc_lu)
    row: dict[str, Any] = {"family": family_of(geometry), "n": n, "geometry": geometry, **feats,
                           "kozeny_carman": k_kc, "force_lu": force, "tau_plus": tau_plus}
    if feats["porosity"] < 0.05:
        return {**row, "status": "closed"}
    spec = PeriodicFlowSpec(grid=grid.to_dict(), geometry=geometry, force=(force, 0.0, 0.0), tau_plus=tau_plus,
                            tol=tol, check_every=check_interval(n, nu), max_steps=max_steps, impl=impl,
                            keep_fields=False)
    res = PeriodicFlow().run(spec, backend)
    k = res.scalars["permeability"]
    percolating = k > 1e-6 * (k_kc if math.isfinite(k_kc) and k_kc > 0 else 1e-12)
    return {**row,
            "status": "ok" if res.diagnostics["converged"] and percolating else
                      ("not_percolating" if not percolating else "not_converged"),
            "permeability": k, "permeability_lu": res.scalars["permeability_lu"],
            "tortuosity_hydraulic": res.scalars["tortuosity_hydraulic"], "mach_max": res.scalars["mach_max"],
            "reynolds_pore": res.scalars["intrinsic_velocity"] * feats["hydraulic_diameter"] / h / nu,
            "steps": res.diagnostics["steps"], "converged": res.diagnostics["converged"],
            "impl": res.diagnostics["impl"], "wall_time_s": res.diagnostics["wall_time_s"],
            "mlups": res.diagnostics["mlups"]}
