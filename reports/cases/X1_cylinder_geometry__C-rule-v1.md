# Verification report: X1_cylinder_geometry (C-rule-v1)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3941
- strouhal_number: 0.15804

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.70 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 9.23e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 7.54e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.57% <= 1.50% (root-to-finest change 0.426%) [three-level Celik procedure, observed order p=3.94, Fs=1.25]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.35% <= 1.50% (root-to-finest change 0.871%) [three-level Celik procedure, observed order p=2.37, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.09% <= 1.50% (root-to-finest change 0.272%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.33% <= 1.50% (root-to-finest change 0.083%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.92% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.85, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.84% <= 1.50% (root-to-finest change 0.602%) [three-level Celik procedure, observed order p=1.60, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X1_cylinder_geometry-53f173b2191e is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mesh_quality: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mass_conservation: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── linear_solver_convergence: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── courant_number: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── reynolds_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── force_reference_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── physics_regime: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── convection_scheme_order: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── Averaging window (reported vs stationary value): PASS U=2.15e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Temporal statistics (stationarity, cycles): PASS U=9.23e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Spatial discretisation (mesh sensitivity): PASS U=0.0057
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.m1.41-fd9653d19a94
│   └── X1_cylinder_geometry.m2-64b56619fbe8
├── Temporal discretisation (time-step sensitivity): PASS U=0.0109
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.dt0.005-e8d467b210a1
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0192
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D2x-077be73cf4dd

CLAIM: strouhal_number of run X1_cylinder_geometry-53f173b2191e is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mesh_quality: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mass_conservation: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── linear_solver_convergence: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── courant_number: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── reynolds_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── force_reference_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── physics_regime: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── convection_scheme_order: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── Averaging window (reported vs stationary value): PASS U=4.79e-06
│   └── X1_cylinder_geometry-53f173b2191e
├── Temporal statistics (stationarity, cycles): PASS U=7.54e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Spatial discretisation (mesh sensitivity): PASS U=0.0135
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.m1.41-fd9653d19a94
│   └── X1_cylinder_geometry.m2-64b56619fbe8
├── Temporal discretisation (time-step sensitivity): PASS U=0.00333
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.dt0.005-e8d467b210a1
└── Artificial boundaries (domain sensitivity): PASS U=0.00845
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D2x-077be73cf4dd

```

## EXPERIMENT HISTORY

Run X1_cylinder_geometry-53f173b2191e: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on X1_cylinder_geometry-53f173b2191e — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X1_cylinder_geometry.m1.41-fd9653d19a94 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on X1_cylinder_geometry.m1.41-fd9653d19a94 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X1_cylinder_geometry.m2-64b56619fbe8 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on X1_cylinder_geometry-53f173b2191e — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X1_cylinder_geometry.dt0.005-e8d467b210a1 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on X1_cylinder_geometry-53f173b2191e — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X1_cylinder_geometry.D2x-bfc063153665 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on X1_cylinder_geometry.D2x-bfc063153665 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X1_cylinder_geometry.D2x-077be73cf4dd (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on X1_cylinder_geometry.D2x-077be73cf4dd — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative domain factor exceeds limit 4.0

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run X1_cylinder_geometry.m1.41-fd9653d19a94: REFINE_MESH from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.009039, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3988 (+0.34%).
  - Observation: strouhal_number 0.15804 → 0.159 (+0.61%).

Run X1_cylinder_geometry.m2-64b56619fbe8: REFINE_MESH from X1_cylinder_geometry.m1.41-fd9653d19a94 (mesh.refinement: 1.414→2, time.delta_t: 0.009039→0.007735).
  - Observation: mean_drag_coefficient 1.3988 → 1.4 (+0.09%).
  - Observation: strouhal_number 0.159 → 0.15943 (+0.26%).

Run X1_cylinder_geometry.dt0.005-e8d467b210a1: REDUCE_TIME_STEP from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3903 (-0.27%).
  - Observation: strouhal_number 0.15804 → 0.15817 (+0.08%).

Run X1_cylinder_geometry.D2x-bfc063153665: EXPAND_DOMAIN from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3847 (-0.67%).
  - Observation: strouhal_number 0.15804 → 0.15732 (-0.45%).

Run X1_cylinder_geometry.D2x-077be73cf4dd: EXPAND_DOMAIN from X1_cylinder_geometry.D2x-bfc063153665 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3847 → 1.3795 (-0.38%).
  - Observation: strouhal_number 0.15732 → 0.15709 (-0.15%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0162 vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X1_cylinder_geometry-53f173b2191e` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=1421 s; record: results/runs/X1_cylinder_geometry-53f173b2191e/run.json
- `X1_cylinder_geometry.m1.41-fd9653d19a94` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T18:32:11+00:00 wall=2137 s; record: results/runs/X1_cylinder_geometry.m1.41-fd9653d19a94/run.json
- `X1_cylinder_geometry.m2-64b56619fbe8` status=completed parent=X1_cylinder_geometry.m1.41-fd9653d19a94 created=2026-10-19T21:32:11+00:00 wall=5933 s; record: results/runs/X1_cylinder_geometry.m2-64b56619fbe8/run.json
- `X1_cylinder_geometry.dt0.005-e8d467b210a1` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-20T01:15:35+00:00 wall=1156 s; record: results/runs/X1_cylinder_geometry.dt0.005-e8d467b210a1/run.json
- `X1_cylinder_geometry.D2x-bfc063153665` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T22:11:23+00:00 wall=1034 s; record: results/runs/X1_cylinder_geometry.D2x-bfc063153665/run.json
- `X1_cylinder_geometry.D2x-077be73cf4dd` status=completed parent=X1_cylinder_geometry.D2x-bfc063153665 created=2026-10-20T03:41:01+00:00 wall=1891 s; record: results/runs/X1_cylinder_geometry.D2x-077be73cf4dd/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3042146226.0, "relative_to_root": 6.632104264224983, "experiment_wall_seconds": 12151.501045441004, "n_experiments": 5, "planner_calls": 7, "planner_cost_usd": 0, "loop_wall_seconds": 1895.133197388}
