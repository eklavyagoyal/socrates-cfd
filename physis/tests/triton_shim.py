"""A tiny CPU emulation of the Triton subset used by ``physis.solvers.lbm.triton_kernel``.

It checks the generated kernel's *logic* (indexing, periodic wrap, bounce-back, moments,
TRT pair update) on machines without an NVIDIA GPU. It does not check Triton compilation
or GPU behaviour; on CUDA machines ``triton_kernel.selfcheck`` does that.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import torch


class _Ptr:
    def __init__(self, base: torch.Tensor, off=0):
        self.base, self.off = base, off

    def __add__(self, other):
        return _Ptr(self.base, self.off + other)

    __radd__ = __add__


class _Scalar(int):
    def to(self, _dtype):
        return torch.tensor(int(self), dtype=torch.int64)


def _make_tl():
    tl = types.ModuleType("triton.language")
    tl.constexpr = object
    tl.int64 = torch.int64
    state = {"pid": 0}

    def program_id(_axis):
        return torch.tensor(state["pid"], dtype=torch.int64)

    def arange(lo, hi):
        return torch.arange(lo, hi, dtype=torch.int64)

    def load(ptr: _Ptr, mask=None, other=0.0):
        flat = ptr.base.reshape(-1)
        off = ptr.off
        safe = torch.where(mask, off, torch.zeros_like(off)) if mask is not None else off
        val = flat[safe]
        if mask is not None:
            val = torch.where(mask, val, torch.as_tensor(other, dtype=val.dtype))
        return val

    def store(ptr: _Ptr, val, mask=None):
        flat = ptr.base.reshape(-1)
        val = torch.as_tensor(val, dtype=flat.dtype).expand_as(ptr.off)
        flat[ptr.off[mask]] = val[mask]

    def where(c, a, b):
        return torch.where(c, torch.as_tensor(a, dtype=torch.float32), torch.as_tensor(b, dtype=torch.float32))

    tl.program_id, tl.arange, tl.load, tl.store, tl.where = program_id, arange, load, store, where
    return tl, state


def load_emulated_kernel_module():
    """Import the generated kernel module with a fake ``triton`` that runs on the CPU."""
    tl, state = _make_tl()

    class _Launcher:
        def __init__(self, fn):
            self.fn = fn

        def __call__(self, *a, **k):
            return self.fn(*a, **k)

        def __getitem__(self, grid):
            def run(*args, **kwargs):
                args = [_Ptr(a) if isinstance(a, torch.Tensor) else (_Scalar(a) if isinstance(a, int) else a)
                        for a in args]
                for pid in range(grid[0]):
                    state["pid"] = pid
                    self.fn(*args, **kwargs)
            return run

    triton = types.ModuleType("triton")
    triton.jit = _Launcher
    triton.cdiv = lambda a, b: (a + b - 1) // b
    triton.language = tl
    saved = {k: sys.modules.get(k) for k in ("triton", "triton.language")}
    sys.modules["triton"], sys.modules["triton.language"] = triton, tl
    try:
        path = Path(__file__).resolve().parents[1] / "src" / "physis" / "solvers" / "lbm" / "triton_kernel.py"
        spec = importlib.util.spec_from_file_location("physis_triton_emulated", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    mod.available = lambda: True
    return mod
