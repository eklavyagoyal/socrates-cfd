"""Compute backend: device and dtype policy (ADR-0001).

Every solver is written against torch and takes a :class:`Backend`. Two precisions:

- ``"validation"``: float64. Used by validation gates and convergence studies, where
  round-off must stay far below discretisation error. MPS has no float64, so validation
  runs on CPU (or CUDA when present).
- ``"fast"``: float32 on the best available device (CUDA > MPS > CPU). Used for data
  generation, optimisation loops and interactive work.

Solver code must never hard-code a device or dtype: allocate through the backend.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

import numpy as np
import torch

Precision = Literal["validation", "fast"]


def configure_threads(n: int | None = None) -> int:
    """Set torch intra-op threads from ``n`` or ``PHYSIS_THREADS`` (default: torch's choice).

    Parallel test or data-generation processes must each limit their threads, otherwise
    they oversubscribe the CPU and wall times become meaningless.
    """
    if n is None:
        env = os.environ.get("PHYSIS_THREADS")
        n = int(env) if env else None
    if n is not None and n > 0:
        torch.set_num_threads(n)
    return torch.get_num_threads()


def resolve_device(name: str = "auto") -> torch.device:
    """``"auto"`` picks CUDA, then MPS, then CPU; anything else is passed to ``torch.device``."""
    if name != "auto":
        return torch.device(name)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


@dataclass(frozen=True)
class Backend:
    device: torch.device
    dtype: torch.dtype

    @property
    def precision(self) -> Precision:
        return "validation" if self.dtype == torch.float64 else "fast"

    def tensor(self, data, dtype: torch.dtype | None = None) -> torch.Tensor:
        return torch.as_tensor(data, dtype=dtype or self.dtype, device=self.device)

    def zeros(self, *shape: int, dtype: torch.dtype | None = None) -> torch.Tensor:
        return torch.zeros(*shape, dtype=dtype or self.dtype, device=self.device)

    def ones(self, *shape: int, dtype: torch.dtype | None = None) -> torch.Tensor:
        return torch.ones(*shape, dtype=dtype or self.dtype, device=self.device)

    def full(self, shape: tuple[int, ...], value: float, dtype: torch.dtype | None = None) -> torch.Tensor:
        return torch.full(shape, value, dtype=dtype or self.dtype, device=self.device)

    def arange(self, *args, dtype: torch.dtype | None = None) -> torch.Tensor:
        return torch.arange(*args, dtype=dtype or self.dtype, device=self.device)

    @staticmethod
    def to_numpy(t: torch.Tensor) -> np.ndarray:
        return t.detach().to("cpu").numpy()

    def describe(self) -> dict:
        return {"device": str(self.device), "dtype": str(self.dtype).replace("torch.", "")}


def get_backend(precision: Precision = "validation", device: str = "auto") -> Backend:
    """Return the backend for a precision.

    ``validation`` on MPS is not possible (no float64); it falls back to CPU unless CUDA
    is available or a device is named explicitly.
    """
    if precision == "validation":
        dev = resolve_device(device)
        if dev.type == "mps":
            if device != "auto":
                raise ValueError("MPS does not support float64; use device='cpu' for validation precision")
            dev = torch.device("cpu")
        return Backend(dev, torch.float64)
    if precision == "fast":
        return Backend(resolve_device(device), torch.float32)
    raise ValueError(f"unknown precision {precision!r}")
