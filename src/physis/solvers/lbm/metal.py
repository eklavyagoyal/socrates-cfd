"""Fused D3Q19 TRT step as one Metal kernel (Apple GPUs, float32): the fast path on Macs.

Same algorithm, state convention and direction order as :mod:`physis.solvers.lbm.trt`
(shifted post-collision populations, pull streaming with half-way bounce-back, TRT with
Guo forcing). One thread per node reads 19 populations and writes 19 (152 bytes), so the
kernel is bandwidth-bound like the hardware benchmark it grew out of. ``tests/test_lbm.py``
checks it step by step against the float64 torch reference.
"""

from __future__ import annotations

import functools

import torch

from physis.solvers.lbm import lattice

Tensor = torch.Tensor


def _source() -> str:
    cx = ", ".join(str(c[0]) for c in lattice.C)
    cy = ", ".join(str(c[1]) for c in lattice.C)
    cz = ", ".join(str(c[2]) for c in lattice.C)
    opp = ", ".join(str(o) for o in lattice.OPP)
    return r"""
#include <metal_stdlib>
using namespace metal;

constant int CX[19] = {%s};
constant int CY[19] = {%s};
constant int CZ[19] = {%s};
constant int OPP[19] = {%s};
constant float W[19] = {1.0f/3.0f,
    1.0f/18.0f, 1.0f/18.0f, 1.0f/18.0f, 1.0f/18.0f, 1.0f/18.0f, 1.0f/18.0f,
    1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f,
    1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f, 1.0f/36.0f};

// Layout: h[q][x][y][z], z fastest (torch's (19, nx, ny, nz) contiguous order).
// prm = {omega+, omega-, gx, gy, gz}; dims = {nx, ny, nz}.
kernel void trt_step(device const float* hin   [[buffer(0)]],
                     device float* hout        [[buffer(1)]],
                     device const uchar* solid [[buffer(2)]],
                     device const float* prm   [[buffer(3)]],
                     device const int* dims    [[buffer(4)]],
                     uint idx [[thread_position_in_grid]]) {
    const int nx = dims[0], ny = dims[1], nz = dims[2];
    const uint n = uint(nx * ny * nz);
    if (idx >= n) return;
    if (solid[idx]) {
        for (int q = 0; q < 19; ++q) hout[q * n + idx] = 0.0f;
        return;
    }
    const int z = int(idx %% uint(nz));
    const int y = int((idx / uint(nz)) %% uint(ny));
    const int x = int(idx / uint(ny * nz));

    float h[19];
    for (int q = 0; q < 19; ++q) {
        int xs = x - CX[q]; xs += (xs < 0) ? nx : 0; xs -= (xs >= nx) ? nx : 0;
        int ys = y - CY[q]; ys += (ys < 0) ? ny : 0; ys -= (ys >= ny) ? ny : 0;
        int zs = z - CZ[q]; zs += (zs < 0) ? nz : 0; zs -= (zs >= nz) ? nz : 0;
        const uint s = uint((xs * ny + ys) * nz + zs);
        h[q] = solid[s] ? hin[uint(OPP[q]) * n + idx] : hin[uint(q) * n + s];
    }

    float drho = 0.0f, jx = 0.0f, jy = 0.0f, jz = 0.0f;
    for (int q = 0; q < 19; ++q) {
        drho += h[q];
        jx += float(CX[q]) * h[q]; jy += float(CY[q]) * h[q]; jz += float(CZ[q]) * h[q];
    }
    const float rho = 1.0f + drho;
    const float wp = prm[0], wm = prm[1];
    const float fx = rho * prm[2], fy = rho * prm[3], fz = rho * prm[4];
    const float ux = (jx + 0.5f * fx) / rho, uy = (jy + 0.5f * fy) / rho, uz = (jz + 0.5f * fz) / rho;
    const float usq = ux * ux + uy * uy + uz * uz;
    const float uf = ux * fx + uy * fy + uz * fz;

    float heq[19], src[19];
    for (int q = 0; q < 19; ++q) {
        const float cu = float(CX[q]) * ux + float(CY[q]) * uy + float(CZ[q]) * uz;
        const float cf = float(CX[q]) * fx + float(CY[q]) * fy + float(CZ[q]) * fz;
        heq[q] = W[q] * (drho + rho * (3.0f * cu + 4.5f * cu * cu - 1.5f * usq));
        src[q] = W[q] * (3.0f * cf + 9.0f * cu * cf - 3.0f * uf);
    }
    for (int q = 0; q < 19; ++q) {
        const int o = OPP[q];
        const float hp = 0.5f * (h[q] + h[o]), hm = 0.5f * (h[q] - h[o]);
        const float ep = 0.5f * (heq[q] + heq[o]), em = 0.5f * (heq[q] - heq[o]);
        const float sp = 0.5f * (src[q] + src[o]), sm = 0.5f * (src[q] - src[o]);
        hout[uint(q) * n + idx] = h[q] - wp * (hp - ep) - wm * (hm - em)
                                + (1.0f - 0.5f * wp) * sp + (1.0f - 0.5f * wm) * sm;
    }
}
""" % (cx, cy, cz, opp)


def available() -> bool:
    return torch.backends.mps.is_available() and hasattr(torch.mps, "compile_shader")


@functools.lru_cache(maxsize=1)
def _library():
    return torch.mps.compile_shader(_source())


class MetalStepper:
    """Owns the double buffer and the device constants for one solid mask."""

    def __init__(self, solid: Tensor):
        if not available():
            raise RuntimeError("Metal fast path needs an Apple GPU and torch.mps.compile_shader")
        dev = torch.device("mps")
        self.solid = solid.to(device=dev, dtype=torch.uint8).contiguous()
        self.shape = tuple(int(n) for n in solid.shape)
        self.n = self.solid.numel()
        self.dims = torch.tensor(self.shape, dtype=torch.int32, device=dev)
        self.lib = _library()

    def run(self, h: Tensor, steps: int, g: Tensor, omega_p: float, omega_m: float) -> Tensor:
        """Advance ``h`` (float32 on MPS, shape (19, *shape)) by ``steps`` and return the new state."""
        prm = torch.tensor([omega_p, omega_m, *[float(v) for v in g.tolist()]],
                           dtype=torch.float32, device=h.device)
        a = h.contiguous()
        b = torch.empty_like(a)
        for _ in range(steps):
            self.lib.trt_step(a, b, self.solid, prm, self.dims, threads=self.n)
            a, b = b, a
        return a
