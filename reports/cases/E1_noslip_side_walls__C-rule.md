# Verification report: E1_noslip_side_walls (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3403
- strouhal_number: 0.16429

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 9.70e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.96% > 1.50% but the demonstrated change 0.89% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.20, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.46% > 1.50% but the demonstrated change 1.28% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.50, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.83% <= 1.50% (root-to-finest change 0.209%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.55% <= 1.50% (root-to-finest change 0.137%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.7e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.71% > 1.50% but the demonstrated change 1.62% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.01, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.51% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.51, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=9.32e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.0012
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0196
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.00834
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0271
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D2x-6e1f5c2d9088

CLAIM: strouhal_number of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=6.51e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.00097
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0246
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.00547
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0151
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D2x-6e1f5c2d9088

```

## EXPERIMENT HISTORY

Run E1_noslip_side_walls-88a7cd5812e8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on E1_noslip_side_walls-88a7cd5812e8 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> E1_noslip_side_walls.m1.41-f15d7e2db685 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on E1_noslip_side_walls.m1.41-f15d7e2db685 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> E1_noslip_side_walls.m2-24c0dd986308 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on E1_noslip_side_walls.m2-24c0dd986308 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative refinement 2.83 exceeds limit 2.0

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on E1_noslip_side_walls-88a7cd5812e8 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> E1_noslip_side_walls.dt0.005-c41af2c90410 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on E1_noslip_side_walls-88a7cd5812e8 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> E1_noslip_side_walls.D2x-1620b1098386 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on E1_noslip_side_walls.D2x-1620b1098386 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> E1_noslip_side_walls.D2x-6e1f5c2d9088 (completed)

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on E1_noslip_side_walls.D2x-6e1f5c2d9088 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative domain factor exceeds limit 4.0

**Critic iteration 8** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run E1_noslip_side_walls.m1.41-f15d7e2db685: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3475 (+0.55%).
  - Observation: strouhal_number 0.16428 → 0.16562 (+0.82%).

Run E1_noslip_side_walls.m2-24c0dd986308: REFINE_MESH from E1_noslip_side_walls.m1.41-f15d7e2db685 (mesh.refinement: 1.414→2, time.delta_t: 0.008673→0.007478).
  - Observation: mean_drag_coefficient 1.3475 → 1.3523 (+0.35%).
  - Observation: strouhal_number 0.16562 → 0.16641 (+0.48%).

Run E1_noslip_side_walls.dt0.005-c41af2c90410: REDUCE_TIME_STEP from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3374 (-0.21%).
  - Observation: strouhal_number 0.16428 → 0.1645 (+0.14%).

Run E1_noslip_side_walls.D2x-1620b1098386: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3259 (-1.07%).
  - Observation: strouhal_number 0.16428 → 0.16301 (-0.77%).

Run E1_noslip_side_walls.D2x-6e1f5c2d9088: EXPAND_DOMAIN from E1_noslip_side_walls.D2x-1620b1098386 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3259 → 1.3188 (-0.54%).
  - Observation: strouhal_number 0.16301 → 0.16256 (-0.27%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `E1_noslip_side_walls-88a7cd5812e8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1851 s; record: results/runs/E1_noslip_side_walls-88a7cd5812e8/run.json
- `E1_noslip_side_walls.m1.41-f15d7e2db685` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:08:43+00:00 wall=2302 s; record: results/runs/E1_noslip_side_walls.m1.41-f15d7e2db685/run.json
- `E1_noslip_side_walls.m2-24c0dd986308` status=completed parent=E1_noslip_side_walls.m1.41-f15d7e2db685 created=2026-10-20T01:15:34+00:00 wall=5373 s; record: results/runs/E1_noslip_side_walls.m2-24c0dd986308/run.json
- `E1_noslip_side_walls.dt0.005-c41af2c90410` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T01:16:41+00:00 wall=1163 s; record: results/runs/E1_noslip_side_walls.dt0.005-c41af2c90410/run.json
- `E1_noslip_side_walls.D2x-1620b1098386` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T20:14:34+00:00 wall=1058 s; record: results/runs/E1_noslip_side_walls.D2x-1620b1098386/run.json
- `E1_noslip_side_walls.D2x-6e1f5c2d9088` status=completed parent=E1_noslip_side_walls.D2x-1620b1098386 created=2026-10-20T02:45:12+00:00 wall=1285 s; record: results/runs/E1_noslip_side_walls.D2x-6e1f5c2d9088/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3108581664.0, "relative_to_root": 6.776938443427077, "experiment_wall_seconds": 11180.323189259996, "n_experiments": 5, "planner_calls": 8, "planner_cost_usd": 0, "loop_wall_seconds": 7979.152034932999}
