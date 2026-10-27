# ADR-0002: SDF geometry, simulation on the same Cartesian grid

**Status:** accepted (2026-10-27)

## Context
Body-fitted meshing is the most fragile step of classic CAE pipelines and the hardest to
automate. Volyra (the geometry kernel) is SDF/implicit-first.

## Decision
Geometry is a signed distance field. Solvers run on uniform Cartesian grids sampled from
it (`geometry/voxelize.py`). Boundary accuracy comes from the SDF itself: link fractions
for interpolated bounce-back (LBM), cut-cell/finite-cell integration (FEM), harmonic
interface conductivities (thermal). No body-fitted mesh in the core.

## Consequences
- Geometry changes never break a mesher; thousands of variants can be generated and
  simulated unattended (data factory).
- Uniform grids cost memory at high resolution; a sparse/adaptive grid is a later step
  (mirrors Volyra's planned OpenVDB backend).
- Accuracy near walls depends on using the SDF (not the staircase mask); every solver
  gate measures it.
