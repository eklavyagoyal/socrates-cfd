"""D3Q19 two-relaxation-time (TRT) step in plain torch: the reference implementation.

State convention, shared with the fused Metal kernel:

- populations are stored *shifted*, ``h_i = f_i - w_i`` (so the rest state is zero and the
  small velocity-carrying part keeps its precision in float32);
- the stored state is *post-collision*; one step is pull streaming with half-way
  bounce-back on solid nodes, then collision at every fluid node;
- solid nodes hold the rest state (``h = 0``) and are never read as fluid.

Collision is TRT with Guo forcing for a uniform body acceleration ``g`` on fluid nodes:

    u   = (sum_i c_i f_i + F/2) / rho,        F = rho * g
    S_i = w_i [3 c_i.F + 9 (c_i.u)(c_i.F) - 3 u.F]
    f*_i = f_i - w+ (f+_i - feq+_i) - w- (f-_i - feq-_i) + (1 - w+/2) S+_i + (1 - w-/2) S-_i

where ``+``/``-`` are the parts symmetric/antisymmetric under ``i -> opp(i)``.
"""

from __future__ import annotations

import torch

from physis.core.backend import Backend
from physis.solvers.lbm import lattice

Tensor = torch.Tensor


class Lattice:
    """Precomputed constants and bounce-back masks for one solid mask on one backend."""

    def __init__(self, solid: Tensor, backend: Backend):
        if solid.ndim != 3:
            raise ValueError(f"solid mask must be 3D, got shape {tuple(solid.shape)}")
        self.backend = backend
        self.solid = solid.to(device=backend.device, dtype=torch.bool)
        self.fluid = ~self.solid
        self.c, self.w, self.opp = lattice.tensors(backend)
        self.w_b = self.w.view(-1, 1, 1, 1)
        # bb[i] is True at fluid nodes whose upstream neighbour x - c_i is solid
        self.bb = torch.stack([
            torch.roll(self.solid, shifts=ci, dims=(0, 1, 2)) & self.fluid for ci in lattice.C
        ])

    @property
    def shape(self) -> tuple[int, int, int]:
        return tuple(self.solid.shape)

    def rest(self) -> Tensor:
        return self.backend.zeros(lattice.Q, *self.shape)

    def stream(self, h: Tensor) -> Tensor:
        """Pull streaming with half-way bounce-back: pre-collision populations at every node."""
        out = torch.empty_like(h)
        for i, ci in enumerate(lattice.C):
            pulled = torch.roll(h[i], shifts=ci, dims=(0, 1, 2))
            out[i] = torch.where(self.bb[i], h[lattice.OPP[i]], pulled)
        return out

    def collide(self, hs: Tensor, g: Tensor, omega_p: float, omega_m: float) -> Tensor:
        """TRT collision with Guo forcing at fluid nodes; solid nodes return to rest."""
        c, opp, w = self.c, self.opp, self.w_b
        drho = hs.sum(0)
        rho = 1.0 + drho
        j = torch.einsum("qa,q...->a...", c, hs)
        force = rho.unsqueeze(0) * g.view(3, 1, 1, 1)
        u = (j + 0.5 * force) / rho
        cu = torch.einsum("qa,a...->q...", c, u)
        cf = torch.einsum("qa,a...->q...", c, force)
        usq = (u * u).sum(0)
        uf = (u * force).sum(0)
        heq = w * (drho + rho * (3.0 * cu + 4.5 * cu * cu - 1.5 * usq))
        src = w * (3.0 * cf + 9.0 * cu * cf - 3.0 * uf)
        hs_o, heq_o, src_o = hs[opp], heq[opp], src[opp]
        out = (hs
               - omega_p * 0.5 * ((hs + hs_o) - (heq + heq_o))
               - omega_m * 0.5 * ((hs - hs_o) - (heq - heq_o))
               + (1.0 - 0.5 * omega_p) * 0.5 * (src + src_o)
               + (1.0 - 0.5 * omega_m) * 0.5 * (src - src_o))
        return torch.where(self.solid.unsqueeze(0), torch.zeros_like(out), out)

    def step(self, h: Tensor, g: Tensor, omega_p: float, omega_m: float) -> Tensor:
        return self.collide(self.stream(h), g, omega_p, omega_m)

    def macroscopic(self, h: Tensor, g: Tensor) -> tuple[Tensor, Tensor]:
        """Density and velocity from a *post-collision* state.

        Collision adds exactly ``F`` to the momentum, so ``u = (j* - F/2) / rho`` equals the
        velocity of the step that produced ``h``. Solid nodes report ``rho = 1``, ``u = 0``.
        """
        drho = h.sum(0)
        rho = 1.0 + drho
        j = torch.einsum("qa,q...->a...", self.c, h)
        u = (j - 0.5 * rho.unsqueeze(0) * g.view(3, 1, 1, 1)) / rho
        u = torch.where(self.solid.unsqueeze(0), torch.zeros_like(u), u)
        rho = torch.where(self.solid, torch.ones_like(rho), rho)
        return rho, u
