"""Steady flow through a periodic cell driven by a body force: the pore-scale solver.

A periodic box (an RVE of a porous structure, a channel between solid walls, an array of
spheres) holds a solid given as SDF geometry. A uniform body acceleration drives the fluid;
the run stops when the superficial velocity is steady. Main output: the permeability
along the driving direction,

    K = nu * U_D / |g|      (Darcy, lattice units; times h^2 for physical units)

where ``U_D`` is the superficial (Darcy) velocity, the mean over the whole cell with
zero in the solid. With TRT at the magic parameter the steady solution, and therefore K,
does not depend on the viscosity chosen (ADR-0008 uses this to pick a fast-converging
``tau_plus``).

Everything is in lattice units (dx = dt = 1) except ``permeability``, which is scaled by
the grid spacing squared.
"""

from __future__ import annotations

import math
import time
from typing import Any, Literal

import torch
from pydantic import Field, field_validator

from physis.core.backend import Backend
from physis.core.grid import Grid
from physis.core.result import SolverResult
from physis.core.spec import Spec
from physis.geometry import from_spec, solid_mask
from physis.solvers.base import SolverDivergence, register
from physis.solvers.lbm import lattice, metal, trt

MACH_LIMIT = 0.3


class PeriodicFlowSpec(Spec):
    grid: dict[str, Any]
    geometry: dict[str, Any] | None = None  # SDF spec of the solid; None = no solid
    force: tuple[float, float, float]  # body acceleration, lattice units
    tau_plus: float = 1.0
    magic: float = lattice.MAGIC
    max_steps: int = Field(200_000, ge=1)
    check_every: int = Field(200, ge=1)
    tol: float = Field(1e-9, gt=0)  # relative change of U_D between checks
    impl: Literal["auto", "torch", "metal"] = "auto"
    keep_fields: bool = True

    @field_validator("tau_plus")
    @classmethod
    def _tau(cls, v: float) -> float:
        if not v > 0.5:
            raise ValueError("tau_plus must exceed 1/2")
        return v

    @field_validator("force")
    @classmethod
    def _force(cls, v: tuple[float, float, float]) -> tuple[float, float, float]:
        if not any(abs(x) > 0 for x in v):
            raise ValueError("force must be non-zero")
        return v


def _use_metal(spec: PeriodicFlowSpec, backend: Backend) -> bool:
    if spec.impl == "torch":
        return False
    fast_ok = backend.device.type == "mps" and backend.dtype == torch.float32 and metal.available()
    if spec.impl == "metal" and not fast_ok:
        raise ValueError("impl='metal' needs the fast backend on an Apple GPU (MPS, float32)")
    return fast_ok


@register
class PeriodicFlow:
    kind = "lbm.periodic_flow3d"
    spec_type = PeriodicFlowSpec

    def run(self, spec: PeriodicFlowSpec, backend: Backend) -> SolverResult:
        grid = Grid.from_dict(spec.grid)
        if grid.ndim != 3:
            raise ValueError("periodic_flow3d needs a 3D grid")
        if spec.geometry is None:
            solid = torch.zeros(grid.shape, dtype=torch.bool, device=backend.device)
        else:
            solid = solid_mask(from_spec(spec.geometry), grid, backend)
        if bool(solid.all()):
            raise ValueError("the geometry fills the whole cell")

        omega_p = 1.0 / spec.tau_plus
        omega_m = 1.0 / lattice.tau_minus(spec.tau_plus, spec.magic)
        nu = lattice.viscosity(spec.tau_plus)
        g = backend.tensor(spec.force)
        g_norm = float(torch.linalg.vector_norm(g))
        direction = g / g_norm

        ref = trt.Lattice(solid, backend)  # macroscopic moments (and the stepper on the torch path)
        use_metal = _use_metal(spec, backend)
        stepper = metal.MetalStepper(solid) if use_metal else None
        h = ref.rest()

        def advance(state: torch.Tensor, n: int) -> torch.Tensor:
            if stepper is not None:
                return stepper.run(state, n, g, omega_p, omega_m)
            for _ in range(n):
                state = ref.step(state, g, omega_p, omega_m)
            return state

        def superficial(state: torch.Tensor) -> tuple[float, float]:
            _, u = ref.macroscopic(state, g)
            ud = float((u * direction.view(3, 1, 1, 1)).sum(0).mean())
            umax = float(torch.linalg.vector_norm(u, dim=0).max())
            return ud, umax

        t0 = time.perf_counter()
        steps, history, converged, previous = 0, [], False, None
        while steps < spec.max_steps:
            n = min(spec.check_every, spec.max_steps - steps)
            h = advance(h, n)
            steps += n
            ud, umax = superficial(h)
            if not (math.isfinite(ud) and math.isfinite(umax)):
                raise SolverDivergence(f"non-finite state after {steps} steps")
            mach = umax / math.sqrt(lattice.CS2)
            if mach > MACH_LIMIT:
                raise SolverDivergence(f"Mach {mach:.3f} exceeds {MACH_LIMIT} after {steps} steps")
            history.append((steps, ud))
            if previous is not None and ud != 0 and abs(ud - previous) <= spec.tol * abs(ud):
                converged = True
                break
            previous = ud
        if backend.device.type == "mps":
            torch.mps.synchronize()
        wall = time.perf_counter() - t0

        rho, u = ref.macroscopic(h, g)
        n_fluid = int(ref.fluid.sum())
        porosity = n_fluid / grid.size
        ud, umax = superficial(h)
        k_lu = nu * ud / g_norm
        fields = {}
        if spec.keep_fields:
            fields = {"ux": u[0], "uy": u[1], "uz": u[2], "rho": rho, "solid": solid.to(backend.dtype)}
        return SolverResult(
            kind=self.kind,
            grid=grid,
            fields=fields,
            scalars={
                "porosity": porosity,
                "superficial_velocity": ud,
                "intrinsic_velocity": ud / porosity,
                "permeability_lu": k_lu,
                "permeability": k_lu * grid.spacing**2,
                "viscosity_lu": nu,
                "mach_max": umax / math.sqrt(lattice.CS2),
            },
            series={
                "step": torch.tensor([s for s, _ in history], dtype=torch.float64),
                "superficial_velocity": torch.tensor([v for _, v in history], dtype=torch.float64),
            },
            diagnostics={
                "steps": steps,
                "converged": converged,
                "impl": "metal" if use_metal else "torch",
                "wall_time_s": wall,
                "mlups": grid.size * steps / wall / 1e6 if wall > 0 else None,
                "fluid_nodes": n_fluid,
                "tau_minus": lattice.tau_minus(spec.tau_plus, spec.magic),
            },
            units={
                "porosity": "1", "superficial_velocity": "lu", "intrinsic_velocity": "lu",
                "permeability_lu": "lu^2", "permeability": "length^2", "viscosity_lu": "lu",
                "mach_max": "1", "ux": "lu", "uy": "lu", "uz": "lu", "rho": "lu", "solid": "1",
            },
        )
