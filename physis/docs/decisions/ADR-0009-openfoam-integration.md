# ADR-0009: Where OpenFOAM fits — device scale, hot gas and independent cross-checks

**Status:** proposed (2026-10-29) — no installation yet

## Context
ADR-0008 splits the first family into a pore scale and a wall/device scale. Pore-scale work runs
on physis' own D3Q19 TRT solver (`physis.solvers.lbm`): voxel geometry straight from SDF, no
meshing, 540–810 MLUPS on an M4 GPU, validated against the Sangani–Acrivos sphere-array solution.
Three needs are outside what that solver should do:

1. **Hot gas.** The combustion-side flow is compressible, hot and, in the nozzle, transonic to
   supersonic. Lattice Boltzmann as built is a low-Mach method.
2. **Device scale.** Plenum, porous liner and hot-gas channel together, with the porous wall as a
   homogenised zone (Darcy–Forchheimer) and conjugate heat transfer into the structure.
3. **An independent second opinion.** A capability is more trustworthy when a different method
   (finite volume on a body-fitted mesh) reproduces it; socrates-cfd built its verification
   methodology on OpenFOAM v2412 for the same reason.

## Decision
OpenFOAM (ESI, pinned **v2412** as in socrates-cfd) is integrated as an **external solver behind
the physis solver contract**, in three places only:

- **Device scale and hot gas:** compressible solvers (`rhoPimpleFoam`; `rhoCentralFoam` for
  supersonic nozzle flow) with the porous liner as a porosity zone whose Darcy–Forchheimer
  coefficients come from physis' pore-scale closures (K, β). Conjugate heat transfer through
  `chtMultiRegionFoam`. Local thermal non-equilibrium inside the liner is not a standard model; the
  candidate is two overlapping regions coupled by inter-region heat transfer, as used for
  heat-exchanger models — to be confirmed in a spike before relying on it.
- **Cross-check gates:** at least one pore-scale case (the simple cubic sphere array, driven with
  `meanVelocityForce` on cyclic boundaries) is solved with `simpleFoam` on a snappyHexMesh mesh, and
  its permeability is compared with the LBM result. Disagreement beyond the stated tolerance fails
  the gate for both.
- **Data factory, device level:** OpenFOAM runs produce device-level samples (wall temperature,
  coolant distribution, pressure drop) for the second surrogate of ADR-0008 when the fast wall
  model is not trusted for a regime.

OpenFOAM is **not** used inside the pore-scale loop: meshing porous micro-structures is the slow,
fragile step it would add, and the GPU LBM is orders of magnitude faster on voxel geometry.

## How
- `physis.solvers.openfoam`: case writers (templates plus spec → dictionaries, deterministic),
  a runner that executes the OpenFOAM tools as a **separate process** with files in and out, and
  log/field parsers that return a normal `SolverResult`. Divergence, non-convergence and mesh
  failures raise `SolverDivergence` (solver contract), never a silent result.
- Provenance records the OpenFOAM version and the full case, so a stored run can be repeated.
- socrates-cfd already has a v2412 runner and log parsers. They are Eklavya's code: reuse only with
  his agreement and with attribution.

## Licensing boundary
OpenFOAM is GPL-3. physis calls it as a separate program and exchanges files; it does not link
against OpenFOAM, embed it, or ship a modified OpenFOAM. Distributing a bundle that contains
OpenFOAM would carry GPL obligations for that bundle, so OpenFOAM stays an external dependency
the user (or a worker image) installs.

## Runtime
- **Linux worker (preferred):** a pinned container (Ubuntu 24.04 + `openfoam2412`, as in
  socrates-cfd's Dockerfile) on the RTX/Linux machine or as a nexus worker. Reproducible and
  close to how results would be produced at scale.
- **Mac (optional, for quick looks):** a native macOS build of OpenFOAM exists as a community
  package; this Mac currently has no Docker. Installing either needs Luis' go-ahead first.

## Consequences
- The physis-owned core stays the pore-scale LBM, the wall model, verification, data and
  surrogates; OpenFOAM is a replaceable component behind the solver contract.
- One more toolchain to pin and keep reproducible; CI cannot run it on a Mac without the worker.
- First milestone (ADR-0008 weeks 3–4): the sphere-array cross-check gate, then a porous-zone
  device case fed by LBM closures.
