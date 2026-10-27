# ADR-0001: PyTorch as the compute backend

**Status:** accepted (2026-10-27)

## Context
physis builds its own solvers (flow, heat, structure) and its own physics-AI models. They
must run on Apple Silicon (development), NVIDIA (the GPU desktop, later cloud) and CPU, and
the long-term goal includes gradient-based shape optimisation.

## Decision
All numerics are written against `torch` tensors and take a `Backend` (device + dtype).
Two precisions: `validation` (float64, CPU/CUDA) for gates and convergence studies;
`fast` (float32, CUDA/MPS/CPU) for data generation and optimisation. No hard-coded
device or dtype in solver code. Hot kernels may later be ported to custom CUDA/Metal
behind the same interfaces.

## Consequences
- One array library for solvers and surrogates; GPU-portable; autograd available for
  differentiable solvers.
- MPS lacks float64, so validation never runs on MPS; each solver documents a
  float32-vs-float64 comparison before float32 data is trusted.
- Peak performance below hand-written CUDA; acceptable until profiling says otherwise.
