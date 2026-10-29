"""Validation gates for the D3Q19 TRT pore-scale solver (ADR-0003, ADR-0008).

Both gates run in validation precision (float64, CPU) as ADR-0001 requires; the Metal fast
path is tied to them by ``tests/test_lbm.py::test_metal_and_float64_reference_agree_on_permeability``.
Criteria were fixed before the first gate run.
"""

from __future__ import annotations

import math

import pytest
import torch

from physis.solvers.lbm import PeriodicFlow, PeriodicFlowSpec, lattice

pytestmark = pytest.mark.validation

SUB = "solvers.lbm"


def _channel(H: int, tau: float, g: float = 1e-6) -> PeriodicFlowSpec:
    walls = {"type": "union", "children": [
        {"type": "box", "center": [2.0, 2.0, 0.5], "half_extents": [100.0, 100.0, 0.5]},
        {"type": "box", "center": [2.0, 2.0, H + 1.5], "half_extents": [100.0, 100.0, 0.5]},
    ]}
    return PeriodicFlowSpec(grid={"shape": [4, 4, H + 2], "spacing": 1.0, "origin": [0.0, 0.0, 0.0]},
                            geometry=walls, force=(g, 0.0, 0.0), tau_plus=tau, tol=1e-13,
                            check_every=500, max_steps=500_000, impl="torch")


def test_gate_poiseuille_channel(gate, cpu64):
    """Plane Poiseuille between half-way bounce-back walls: TRT at the magic parameter is
    exact for the parabolic profile and independent of the relaxation time."""
    g = gate("lbm.poiseuille3d", capability="lbm.d3q19.trt.bounce_back_wall",
             reference={"source": "analytic plane Poiseuille, u(z) = g/(2 nu) (z - z0)(z1 - z), walls midway between nodes",
                        "criteria": "max relative profile error <= 1e-10 for H in {8, 16, 32} and tau+ in {0.8, 2.0}; "
                                    "flow rate identical across tau+ to 1e-10"},
             code_subpackage=SUB, backend=cpu64.describe())
    worst, spread = 0.0, 0.0
    for H in (8, 16, 32):
        rates = []
        for tau in (0.8, 2.0):
            r = PeriodicFlow().run(_channel(H, tau), cpu64)
            nu = lattice.viscosity(tau)
            z = torch.arange(H + 2, dtype=torch.float64) + 0.5
            exact = 1e-6 / (2 * nu) * (z - 1.0) * (H + 1.0 - z)
            ux = r.fields["ux"][0, 0, :]
            err = float((ux[1:-1] - exact[1:-1]).abs().max() / exact.max())
            g.metric(f"H{H}_tau{tau}_max_rel_err", err)
            g.metric(f"H{H}_tau{tau}_steps", r.diagnostics["steps"])
            worst = max(worst, err)
            rates.append(r.scalars["permeability_lu"])
        spread = max(spread, abs(rates[0] / rates[1] - 1))
    g.check("max_rel_profile_error", worst, "<=", 1e-10)
    g.check("tau_dependence_of_flow_rate", spread, "<=", 1e-10)
    g.finish()


# Sangani & Acrivos (1982) normalised drag K = F / (6 pi mu a U) for simple cubic arrays.
# The analytic values are back-computed from Table 1 of arXiv:1401.2025 ("Drag correlation
# for dilute and moderately dense fluid-particle systems using the lattice Boltzmann method"),
# which lists simulated drag C* and its error against the analytic C: C = C* / (1 + err),
# averaged over the L = 32 and L = 64 rows (they agree to < 0.1 %).
_TABLE = {0.5: [(2.93, 0.0293), (2.89, 0.0163)],
          0.7: [(6.15, 0.0249), (6.08, 0.0127)],
          0.9: [(20.06, 0.0469), (19.52, 0.0186)]}
SANGANI_ACRIVOS = {chi: sum(c / (1 + e) for c, e in rows) / len(rows) for chi, rows in _TABLE.items()}


def _sphere(L: int, chi: float, tau: float = 1.5, gval: float = 1e-6) -> PeriodicFlowSpec:
    return PeriodicFlowSpec(grid={"shape": [L, L, L], "spacing": 1.0, "origin": [0.0, 0.0, 0.0]},
                            geometry={"type": "ball", "center": [L / 2] * 3, "radius": chi * L / 2},
                            force=(gval, 0.0, 0.0), tau_plus=tau, tol=1e-10, check_every=100,
                            max_steps=200_000, impl="torch", keep_fields=False)


def _drag(L: int, chi: float, k: float) -> float:
    return L**3 / (6 * math.pi * (chi * L / 2) * k)


def test_gate_simple_cubic_sphere_array(gate, cpu64):
    """Stokes permeability of a simple cubic array of spheres (staircase bounce-back)."""
    g = gate("lbm.sc_sphere_array", capability="lbm.d3q19.trt.porous_permeability",
             reference={"source": "Sangani & Acrivos (1982), Int. J. Multiphase Flow 8:343-360, values via "
                                  "arXiv:1401.2025 Table 1 (C = C*/(1+err))",
                        "values": {str(k): v for k, v in SANGANI_ACRIVOS.items()},
                        "criteria": "relative drag error <= 6 % at L = 32 and <= 4 % at L = 48 for chi in "
                                    "{0.5, 0.7, 0.9}; permeability independent of tau+ (0.8 vs 2.5) to 1e-4 and "
                                    "of the force (Darcy regime, g vs 4g) to 1e-3 at L = 32, chi = 0.7"},
             code_subpackage=SUB, backend=cpu64.describe())
    g.note("Simple bounce-back on voxelised spheres converges non-monotonically (the voxel solid fraction "
           "jumps with L), so no observed order is required; voxel and nominal solid fractions are recorded.")
    worst = {32: 0.0, 48: 0.0}
    for L in (32, 48):
        for chi, ref in SANGANI_ACRIVOS.items():
            r = PeriodicFlow().run(_sphere(L, chi), cpu64)
            c = _drag(L, chi, r.scalars["permeability_lu"])
            err = abs(c / ref - 1)
            worst[L] = max(worst[L], err)
            g.metric(f"L{L}_chi{chi}", {"drag": c, "reference": ref, "rel_err": c / ref - 1,
                                         "solid_fraction_voxel": 1 - r.scalars["porosity"],
                                         "solid_fraction_nominal": math.pi / 6 * chi**3,
                                         "steps": r.diagnostics["steps"], "converged": r.diagnostics["converged"],
                                         "mach_max": r.scalars["mach_max"]})
    g.check("max_rel_drag_error_L32", worst[32], "<=", 0.06)
    g.check("max_rel_drag_error_L48", worst[48], "<=", 0.04)

    k_a = PeriodicFlow().run(_sphere(32, 0.7, tau=0.8), cpu64).scalars["permeability_lu"]
    k_b = PeriodicFlow().run(_sphere(32, 0.7, tau=2.5), cpu64).scalars["permeability_lu"]
    g.check("tau_dependence", abs(k_a / k_b - 1), "<=", 1e-4)
    k_1 = PeriodicFlow().run(_sphere(32, 0.7, gval=1e-6), cpu64)
    k_4 = PeriodicFlow().run(_sphere(32, 0.7, gval=4e-6), cpu64)
    g.metric("darcy_check_pore_mach", k_4.scalars["mach_max"])
    g.check("force_dependence", abs(k_1.scalars["permeability_lu"] / k_4.scalars["permeability_lu"] - 1), "<=", 1e-3)
    g.finish()
