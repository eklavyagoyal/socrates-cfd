# ADR-0008: First design family — transpiration-cooled porous walls for thrust chambers

**Status:** accepted (2026-10-29)

## Context
physis needs one narrow first design family to build depth instead of breadth: every family needs
its own sizing model and mapping before it can feed the data factory (ADR-0007), and a validated
end-to-end chain on one family is worth more than shallow coverage of many.

Transpiration cooling forces a coolant through a porous wall into the hot-gas boundary layer. The
coolant takes up heat inside the wall, and the injected layer lowers the convective load on the hot
side, which gives more uniform wall temperatures than regenerative or film cooling and suppresses the
hot spots that brittle ceramics cannot tolerate. A design has to satisfy conflicting requirements at
once: high permeability for the coolant, enough strength under pressure and thermal gradients, and
thermal-shock tolerance under cyclic firing. Additive manufacturing (lithography-based ceramics,
laser powder bed fusion) now makes graded porosity and engineered pore architectures possible, but
the design chain from pore structure to effective properties to wall performance is split across
disciplines and rarely available in one tool.

The team has domain background here from earlier research on additively manufactured porous ceramics
for small-satellite thrusters. **Data from that work is not used**: it belongs to the institute. physis
builds on public literature and its own verified simulations only.

## Decision
The first family is a **transpiration-cooled porous wall segment** (liner or inlay) of a thrust
chamber, simulated on two scales and learned on top:

1. **Pore scale (LBM, D3Q19).** Representative volume elements of synthetic porous structures — random
   sphere and particle packings, bimodal templated pores (spherical macropores in a fine matrix), TPMS
   lattices — generated as SDF and voxelised on the shared grid (ADR-0002), solid as bounce-back.
   Outputs are the closure properties of the wall: porosity ε, permeability K, Forchheimer coefficient β
   (from a Reynolds sweep), effective solid and fluid conductivities, interfacial heat-transfer
   coefficient and specific surface.
2. **Wall scale (porous-medium model).** Darcy–Forchheimer flow and two-temperature (local thermal
   non-equilibrium) energy equations through the wall thickness and along the chamber. Hot-gas side
   first through the classical blowing reduction of heat transfer (St/St₀ = b/(eᵇ − 1), b = F/St₀,
   blowing ratio F = (ρv)_coolant / (ρu)_gas); a coupled hot-gas channel later. Outputs: hot-wall
   temperature, cooling efficiency θ = (T_g − T_w)/(T_g − T_c), coolant mass-flux distribution and
   pressure drop.
3. **Structure.** Thermo-elastic voxel FEM on the same grid: thermal stress and a thermal-shock margin
   for the wall.
4. **Data factory.** Designs are sampled in performance space (ADR-0007): maximum wall temperature,
   available coolant mass flux, allowed pressure drop and stress margin are the targets, and the
   mapping produces graded porous architectures. Only samples whose gates pass enter a dataset.
5. **Surrogates.** Two learned maps: (a) structure → effective properties, trained on pore-scale runs,
   which replaces the expensive RVE simulation inside loops; (b) wall design and operating point → wall
   fields and scalars. Ensembles give uncertainty; active learning adds samples where it is high.
6. **Exploration.** With the surrogates, sweep the full variant space — porosity grading along the
   wall, thickness, pore architecture, coolant and mass flux — into Pareto fronts of coolant mass, wall
   temperature and stress margin, then confirm the chosen points with the solvers.

Out of scope at first: combustion chemistry, coolant phase change inside the wall, and modelling the
manufacturing process itself (sintering to microstructure). Pore architectures are parametric.

## Verification gates (first set)
- Permeability of periodic sphere arrays against the classical analytic and numerical results
  (Sangani & Acrivos 1982; Zick & Homsy 1982), with grid-convergence (GCI) evidence.
- Random packings against Kozeny–Carman / Ergun within a stated tolerance band.
- Forchheimer onset and β from a Reynolds sweep, checked for consistency with the Ergun inertial term.
- Wall model against closed-form one-dimensional solutions for a slab with throughflow (equilibrium and
  non-equilibrium), then against published transpiration-cooling experiments from the open literature.

## Consequences
- Solver priorities follow from this: LBM with solid voxels for the pore scale, the porous-medium wall
  model with two-temperature thermal coupling, then the voxel FEM.
- The wall model is small (1D/2D) and fast, so it can generate many samples; the pore-scale RVEs are the
  expensive part and are what the GPU budget is for.
- Known risks: high-temperature gas properties in the closures, validity of the blowing correlation at
  strong injection, and the low-Mach limit of LBM (fine inside pores, not for the hot-gas channel).

## First four weeks
1. Pore-scale LBM on periodic sphere arrays; permeability gate with GCI.
2. Random, bimodal and TPMS structures: K, β and conductivities; first RVE dataset.
3. Wall model with Darcy–Forchheimer, two-temperature coupling and blowing reduction; gates against
   the closed-form slab solutions; first parametric sweeps.
4. Surrogates v0 for both maps with uncertainty, and a first exploration of the variant space for a
   reference load case.
