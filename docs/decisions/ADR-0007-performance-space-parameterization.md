# ADR-0007: Parameterise design spaces in performance space, not geometry space

**Status:** accepted (2026-10-28)

## Context
The data factory (`physis.data`) and the surrogates are only as cheap and as trustworthy as the
design space they sample. Sampling free-form geometry parameters (radii, offsets, lattice cell
sizes chosen independently) has three problems:

- most samples are physically poor or infeasible, so simulation budget is spent on designs nobody
  would build;
- the space is high-dimensional, so surrogates need tens of thousands of samples;
- a model trained on such data can propose geometries that look plausible but violate the physics
  ("hallucinated" designs).

Turbomachinery 3D inverse design shows the alternative. Advanced Design Technology (TURBOdesign)
describes a rocket-turbopump redesign driven by 13 blade-loading parameters and 57 candidate designs
(171 CFD runs in about 12.5 hours, LinkedIn post, October 2026): the inputs are target flow
behaviour (blade loading, pressure distribution), an inverse solver produces the geometry, and every
candidate is physically meaningful by construction. Socrates (eklavyagoyal/socrates-cfd) reached the
compatible conclusion from the verification side: trust comes from physics in the loop, not from more
data.

## Decision
Every design family in `physis.geometry.families` exposes two parameter sets:

1. **Performance parameters** (the default sampling space of the data factory): targets a design
   should meet, e.g. heat-flux or temperature distribution along a heat exchanger, allowed pressure
   drop, flow split, mass or volume budget, wall-temperature limits, loading distributions.
2. **Geometry parameters** (still available for exploration and debugging): the SDF parameters
   themselves.

Each family provides a **mapping from performance to geometry parameters**, in increasing fidelity:

- **Sizing models:** closed-form or reduced-order relations (correlations, 1D network models) that
  turn targets into an initial geometry.
- **Field-driven mapping:** target fields drive SDF fields directly on the shared grid (ADR-0002),
  e.g. TPMS wall thickness and cell size graded by a target heat-flux or stress field.
- **Inverse solve:** optimisation or adjoint/gradient methods through the differentiable solvers
  (ADR-0001) that adjust geometry until the simulated behaviour matches the targets.

Every family documents its feasibility constraints so that sampled performance points map to buildable
geometry (wall thickness ≥ manufacturing minimum, connectivity of flow domains, envelope limits).

Datasets record both parameter sets per sample, plus the **target error**: the deviation between
the requested performance and the performance the solver measured for the generated geometry. The
target error is a deterministic, verifiable quantity (ADR-0003, ADR-0006) and is the primary
validation metric of a mapping.

## Consequences
- Orders of magnitude fewer simulations per useful dataset; surrogates learn in a low-dimensional,
  physically meaningful space.
- Every family needs a sizing model or mapping before it can feed the data factory; this is real
  engineering work per product class (heat exchanger first).
- A mapping can bias the dataset towards what the sizing model believes; the target error and
  occasional geometry-space samples keep that bias visible.
- Inverse design via gradients becomes possible once the solvers are differentiable and validated;
  until then mappings are sizing models plus field-driven grading.
