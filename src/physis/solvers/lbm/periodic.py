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

Three implementations of the same step: the torch reference (any device, the only one in
float64), a fused Metal kernel (Apple GPUs) and a fused Triton kernel (NVIDIA GPUs, used
only after its self-check against the reference passes). The fast paths keep just the
double buffer and the solid mask on the device and reduce moments one component at a
time, so a 512^3 cell fits in 32 GB.

Everything is in lattice units (dx = dt = 1) except ``permeability``, which is scaled by
the grid spacing squared.
"""

from __future__ import annotations

import math
import time
import warnings
from typing import Any, Literal

import torch
from pydantic import Field, field_validator

from physis.core.backend import Backend
from physis.core.grid import Grid
from physis.core.result import SolverResult
from physis.core.spec import Spec
from physis.geometry import from_spec, solid_mask
from physis.solvers.base import SolverDivergence, register
from physis.solvers.lbm import lattice, metal, triton_kernel, trt

MACH_LIMIT = 0.3

Impl = Literal["auto", "torch", "metal", "triton"]


class PeriodicFlowSpec(Spec):
    grid: dict[str, Any]
    geometry: dict[str, Any] | None = None  # SDF spec of the solid; None = no solid
    force: tuple[float, float, float]  # body acceleration, lattice units
    tau_plus: float = 1.0
    magic: float = lattice.MAGIC
    max_steps: int = Field(200_000, ge=1)
    check_every: int = Field(200, ge=1)
    tol: float = Field(1e-9, gt=0)  # relative change of U_D between two full check windows (needed twice in a row)
    impl: Impl = "auto"
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


def choose_impl(requested: Impl, backend: Backend) -> str:
    """The implementation that will actually run for ``requested`` on ``backend``."""
    fast = backend.dtype == torch.float32
    if requested == "torch":
        return "torch"
    if requested in ("auto", "metal") and fast and backend.device.type == "mps" and metal.available():
        return "metal"
    if requested in ("auto", "triton") and fast and backend.device.type == "cuda" and triton_kernel.available():
        ok, detail = triton_kernel.selfcheck(str(backend.device))
        if ok:
            return "triton"
        if requested == "triton":
            raise RuntimeError(f"Triton kernel failed its self-check: {detail}")
        warnings.warn(f"Triton kernel failed its self-check ({detail}); using the torch reference path", stacklevel=2)
    if requested in ("metal", "triton"):
        raise ValueError(f"impl={requested!r} is not available on {backend.describe()}")
    return "torch"


def bytes_needed(shape: tuple[int, ...], impl: str, itemsize: int = 4) -> int:
    """Device memory a run needs, as a guard before allocating (estimate, not a bound)."""
    n = math.prod(shape)
    if impl in ("metal", "triton"):
        return n * (2 * 19 * itemsize + 1 + 6 * itemsize)  # double buffer, mask, reduction temporaries
    return n * (19 * (1 + 6 * itemsize) + 8 * itemsize)  # bounce-back masks, stream/collide temporaries


def _reductions(h: torch.Tensor, c: torch.Tensor, g: tuple[float, float, float], direction: tuple[float, float, float],
                fluid: torch.Tensor, *, speed: bool) -> dict[str, float]:
    """Superficial velocity along ``direction``, max |u| and mean fluid speed, one component at a time."""
    rho = 1.0 + h.sum(0)
    usq = torch.zeros_like(rho) if speed else None
    ud = torch.zeros_like(rho)
    for a in range(3):
        ua = (torch.tensordot(c[:, a], h, dims=1) - 0.5 * rho * g[a]) / rho
        ua = torch.where(fluid, ua, torch.zeros_like(ua))
        if direction[a] != 0.0:
            ud = ud + direction[a] * ua
        if speed:
            usq = usq + ua * ua
        del ua
    out = {"ud": float(ud.mean())}
    n_fluid = int(fluid.sum())
    if speed:
        mag = torch.sqrt(usq)
        out["umax"] = float(mag.max())
        out["mean_speed_fluid"] = float(mag.sum()) / max(n_fluid, 1)
    out["ud_fluid"] = float(ud.sum()) / max(n_fluid, 1)
    return out


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
        fluid = ~solid

        impl = choose_impl(spec.impl, backend)
        omega_p = 1.0 / spec.tau_plus
        omega_m = 1.0 / lattice.tau_minus(spec.tau_plus, spec.magic)
        nu = lattice.viscosity(spec.tau_plus)
        g = tuple(float(v) for v in spec.force)
        g_norm = math.sqrt(sum(v * v for v in g))
        direction = tuple(v / g_norm for v in g)
        c = backend.tensor(lattice.C)

        if impl == "torch":
            ref = trt.Lattice(solid, backend)
            g_t = backend.tensor(g)
            state = {"h": ref.rest()}

            def advance(n: int) -> torch.Tensor:
                for _ in range(n):
                    state["h"] = ref.step(state["h"], g_t, omega_p, omega_m)
                return state["h"]
        else:
            h0 = torch.zeros(lattice.Q, *grid.shape, dtype=torch.float32, device=backend.device)
            stepper = (metal.MetalStepper(solid, h0) if impl == "metal" else triton_kernel.TritonStepper(solid, h0))
            del h0

            def advance(n: int) -> torch.Tensor:
                return stepper.run(n, g, omega_p, omega_m)

        t0 = time.perf_counter()
        steps, history, converged, previous, calm = 0, [], False, None, 0
        h = None
        # Periodic lattices carry a small undamped period-2 oscillation (a staggered mode excited by
        # the impulsive start); a single-step sample alternates between its two levels forever. Every
        # check therefore averages the last two time steps.
        while steps < spec.max_steps:
            n = min(spec.check_every, spec.max_steps - steps)
            if n >= 2:
                r1 = _reductions(advance(n - 1), c, g, direction, fluid, speed=False)
                h = advance(1)
                r = _reductions(h, c, g, direction, fluid, speed=True)
                ud, umax = 0.5 * (r1["ud"] + r["ud"]), r["umax"]
            else:
                h = advance(n)
                r = _reductions(h, c, g, direction, fluid, speed=True)
                ud, umax = r["ud"], r["umax"]
            steps += n
            if not (math.isfinite(ud) and math.isfinite(umax)):
                raise SolverDivergence(f"non-finite state after {steps} steps")
            mach = umax / math.sqrt(lattice.CS2)
            if mach > MACH_LIMIT:
                raise SolverDivergence(f"Mach {mach:.3f} exceeds {MACH_LIMIT} after {steps} steps")
            history.append((steps, ud))
            if n < spec.check_every:  # a short last window before max_steps changes little: never evidence
                break
            if previous is not None and ud != 0 and abs(ud - previous) <= spec.tol * abs(ud):
                calm += 1
                if calm >= 2:  # twice in a row, so one quiet window inside an oscillation does not count
                    converged = True
                    break
            else:
                calm = 0
            previous = ud
        if backend.device.type == "mps":
            torch.mps.synchronize()
        elif backend.device.type == "cuda":
            torch.cuda.synchronize()
        wall = time.perf_counter() - t0

        final = _reductions(h, c, g, direction, fluid, speed=True)
        n_fluid = int(fluid.sum())
        porosity = n_fluid / grid.size
        ud = history[-1][1] if history else final["ud"]  # two-step average of the last check
        k_lu = nu * ud / g_norm
        fields = {}
        if spec.keep_fields:
            rho = 1.0 + h.sum(0)
            comps = []
            for a in range(3):
                ua = (torch.tensordot(c[:, a], h, dims=1) - 0.5 * rho * g[a]) / rho
                comps.append(torch.where(fluid, ua, torch.zeros_like(ua)))
            fields = {"ux": comps[0], "uy": comps[1], "uz": comps[2],
                      "rho": torch.where(fluid, rho, torch.ones_like(rho)), "solid": solid.to(backend.dtype)}
        tortuosity = final["mean_speed_fluid"] / final["ud_fluid"] if final["ud_fluid"] > 0 else float("nan")
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
                "mach_max": final["umax"] / math.sqrt(lattice.CS2),
                "tortuosity_hydraulic": tortuosity,
            },
            series={
                "step": torch.tensor([s for s, _ in history], dtype=torch.float64),
                "superficial_velocity": torch.tensor([v for _, v in history], dtype=torch.float64),
            },
            diagnostics={
                "steps": steps,
                "converged": converged,
                "impl": impl,
                "wall_time_s": wall,
                "mlups": grid.size * steps / wall / 1e6 if wall > 0 else None,
                "fluid_nodes": n_fluid,
                "tau_minus": lattice.tau_minus(spec.tau_plus, spec.magic),
            },
            units={
                "porosity": "1", "superficial_velocity": "lu", "intrinsic_velocity": "lu",
                "permeability_lu": "lu^2", "permeability": "length^2", "viscosity_lu": "lu",
                "mach_max": "1", "tortuosity_hydraulic": "1",
                "ux": "lu", "uy": "lu", "uz": "lu", "rho": "lu", "solid": "1",
            },
        )
