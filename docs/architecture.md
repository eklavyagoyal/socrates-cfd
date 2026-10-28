# physis architecture

physis is a self-built engineering physics platform: parametric SDF geometry, GPU-capable
solvers for flow, heat and structure on the same Cartesian grids, a deterministic
verification layer, a data factory that produces *verified* training data, physics-AI
surrogates trained on it, design optimisation, and a platform surface (CLI, REST, MCP).

## Layers and data flow

```
                ┌──────────────────────────── platform ────────────────────────────┐
                │  CLI · REST API · MCP server (agents propose, code decides)      │
                └───────────────┬───────────────────────────────┬──────────────────┘
                                │                               │
   design space ──▶ geometry ──▶ voxelize ──▶ solvers ──▶ verification ──▶ data ──▶ surrogates
   (params)        (SDF, torch;  (sample,     lbm/thermal/  (gates, GCI,     (verified   (U-Net/FNO,
                    Volyra        mask, link   fem on the    evidence,        datasets)   ensembles)
                    parity)       fractions)   same grid)    verdicts)                       │
                                                                                             ▼
                                                                         optimize (direct, surrogate,
                                                                         gradient) ──▶ back to geometry
```

Every solver run goes through the content-addressed **run store** with provenance
(`core/store.py`); every capability claim goes through a **validation gate**
(`verification/gates.py`, report in `docs/validation.md`).

## Packages

| Package | Responsibility | Contract |
|---|---|---|
| `physis.core` | backend (device/dtype), `Grid`, `Spec`, `SolverResult`, provenance, `RunStore` | everything depends on it; it depends on nothing in physis |
| `physis.geometry` | SDF nodes in torch (differentiable), Volyra model import and parity, parametric families, voxelization (`sample`, `solid_mask`, `link_fractions`) | geometry ⇄ solvers only through `voxelize` |
| `physis.solvers.lbm` | lattice Boltzmann flow (D2Q9/D3Q19, BGK/TRT, Bouzidi walls, inlets/outlets, forces, LES) | `Solver` protocol in `solvers/base.py` |
| `physis.solvers.thermal` | heat conduction (conjugate solid/fluid), thermal LBM (advection–diffusion, Boussinesq) | same |
| `physis.solvers.fem` | voxel finite elements: linear elasticity (2D/3D), thermal stress | same |
| `physis.verification` | observed order, Richardson/GCI (Celik), transient removal, cycle statistics, Strouhal, checks and verdicts, gates | reads `SolverResult`s; never edits them |
| `physis.data` | design spaces sampled in performance space (ADR-0007), samplers, batch execution, verified datasets with cards and target error | writes through `RunStore` |
| `physis.surrogates` | models on SDF grids → fields and scalars, training, uncertainty, active learning | trains only on verified samples |
| `physis.optimize` | Nelder–Mead/CMA-ES, surrogate-assisted and gradient-based design optimisation | evaluates through solvers or surrogates |
| `physis.platform` | CLI, REST API, MCP server, job queue | thin; no physics |

## Grid convention

Cell-centred, `indexing="ij"`, arrays shaped `(nx, ny[, nz])`, uniform spacing `h`; node
`i` sits at `origin + (i + 0.5) h`. LBM lattice nodes, thermal cells and voxel-FEM
elements all use this grid, so fields from different physics live on the same index
space and couple without interpolation.

## Precision

`validation` = float64 on CPU (or CUDA); `fast` = float32 on CUDA/MPS/CPU. Gates run in
`validation`; data generation in `fast`, with a documented float32-vs-float64 check per
solver (ADR-0001).

## Authority

Agents and LLMs may propose geometry, parameters and experiments. Numbers, verdicts and
dataset labels come only from deterministic code (ADR-0006, from Socrates' finding that
LLM verdicts and LLM reviews failed as safety gates).
