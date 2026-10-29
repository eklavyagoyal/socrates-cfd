# physis

Self-built engineering physics platform (working name): parametric SDF geometry, our own
solvers for flow, heat and structure on GPU-capable Cartesian grids, a deterministic
verification layer, a data factory for *verified* training data, physics-AI surrogates,
design optimisation, and a CLI/REST/MCP surface.

Built for the TUM.ai E-Lab 6.0 by Luis Dehlwes and Eklavya Goyal. Geometry semantics follow
[Volyra](../../01_Projects/volyra); verification methodology builds on
[socrates-cfd](../socrates-cfd).

> **Status:** under construction. What is validated and what is prototype is listed per
> capability in [`docs/validation.md`](docs/validation.md), generated from the gate records.

## Start here

- [`docs/architecture.md`](docs/architecture.md): layers, data flow, grid and precision conventions
- [`docs/decisions/`](docs/decisions/): ADR-0001 … ADR-0009 (why torch, why SDF-native grids, gates,
  Volyra parity, run store, authority boundaries, performance-space parameterisation, first family:
  transpiration-cooled porous walls, where OpenFOAM fits)
- [`docs/validation.md`](docs/validation.md): gate status per capability

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest                       # unit tests (fast)
.venv/bin/python -m pytest -m validation         # validation gates (slow, write validation/results/)
.venv/bin/python scripts/validation_report.py    # regenerate docs/validation.md
```

`PHYSIS_THREADS` limits torch threads per process (default 3 in tests);
`PHYSIS_STORE` sets the run-store location (default `var/store`, not in git).

## Weekend run on an NVIDIA GPU

[`docs/weekend-5090.md`](docs/weekend-5090.md): `scripts/weekend_5090.py` computes a pore-scale
permeability dataset and trains the first learned closure; `--quick` smoke-tests every stage.

## Layout

| Path | Contents |
|---|---|
| `src/physis/core` | backend (device/dtype policy), `Grid`, `Spec`, `SolverResult`, provenance, `RunStore` |
| `src/physis/geometry` | SDF nodes in torch, porous RVE families (sphere beds, templated pores, gyroids), Volyra import/parity, voxelization |
| `src/physis/solvers` | `lbm` (flow: D3Q19 TRT; torch reference, fused Metal and Triton kernels), `thermal` (heat), `fem` (structure); contract in `solvers/base.py` |
| `src/physis/verification` | convergence/GCI, evidence extraction, gates |
| `src/physis/data` | structure descriptors, pore-scale RVE samples, design spaces, verified datasets |
| `src/physis/surrogates` | learned closures (Kozeny–Carman baseline, MLP ensemble, 3D CNN), uncertainty |
| `src/physis/optimize` | design optimisation |
| `src/physis/platform` | CLI, REST API, MCP server |
| `tests/` | unit tests and validation gates |
| `validation/results/` | gate records (JSON, committed) |
