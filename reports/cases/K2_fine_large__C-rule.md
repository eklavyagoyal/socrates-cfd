# Verification report: K2_fine_large (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3278
- strouhal_number: 0.16382

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.65 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.91e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.01e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.68% <= 1.50% (root-to-finest change 0.113%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.17% > 1.50% but the demonstrated change 0.36% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 4.3e-05)]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.79% <= 1.50% (root-to-finest change 0.198%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.068%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.02% <= 1.50% (root-to-finest change 0.715%) [three-level Celik procedure, observed order p=1.51, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.29% <= 1.50% (root-to-finest change 0.372%) [three-level, observed order 2.45 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=7.06e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.91e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): PASS U=0.00684
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
├── Temporal discretisation (time-step sensitivity): PASS U=0.00791
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.0102
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D2x-bc527461f36d
    └── K2_fine_large.D2x-4555577439db

CLAIM: strouhal_number of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=4.99e-06
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.01e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0217
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
├── Temporal discretisation (time-step sensitivity): PASS U=0.0027
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.0129
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D2x-bc527461f36d
    └── K2_fine_large.D2x-4555577439db

```

## EXPERIMENT HISTORY

Run K2_fine_large-2d999cd1eb7c: submitted simulation (54244 cells, dt=0.007 D/U, half-height 60 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on K2_fine_large-2d999cd1eb7c — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K2_fine_large.m1.77-e5d0ad1d73b4 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on K2_fine_large.m1.77-e5d0ad1d73b4 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: child mesh has 216220 cells > limit 160000

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on K2_fine_large-2d999cd1eb7c — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K2_fine_large.dt0.0035-6a0f9a80f290 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on K2_fine_large-2d999cd1eb7c — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K2_fine_large.D2x-bc527461f36d (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on K2_fine_large.D2x-bc527461f36d — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K2_fine_large.D2x-4555577439db (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run K2_fine_large.m1.77-e5d0ad1d73b4: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→1.768, time.delta_t: 0.007→0.006875, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3293 (+0.11%).
  - Observation: strouhal_number 0.16382 → 0.16441 (+0.36%).

Run K2_fine_large.dt0.0035-6a0f9a80f290: REDUCE_TIME_STEP from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, time.delta_t: 0.007→0.0035, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3251 (-0.20%).
  - Observation: strouhal_number 0.16382 → 0.16393 (+0.07%).

Run K2_fine_large.D2x-bc527461f36d: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→120, domain.half_height: 60→120, domain.upstream: 40→80, mesh.n_downstream: 120→155, mesh.n_lateral: 51→61, mesh.n_upstream: 38→46, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3208 (-0.53%).
  - Observation: strouhal_number 0.16382 → 0.16331 (-0.31%).

Run K2_fine_large.D2x-4555577439db: EXPAND_DOMAIN from K2_fine_large.D2x-bc527461f36d (domain.downstream: 120→240, domain.half_height: 120→240, domain.upstream: 80→160, mesh.n_downstream: 155→191, mesh.n_lateral: 61→71, mesh.n_upstream: 46→54).
  - Observation: mean_drag_coefficient 1.3208 → 1.3183 (-0.19%).
  - Observation: strouhal_number 0.16331 → 0.16321 (-0.06%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0147 vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K2_fine_large-2d999cd1eb7c` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=8041 s; record: results/runs/K2_fine_large-2d999cd1eb7c/run.json
- `K2_fine_large.m1.77-e5d0ad1d73b4` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-19T10:01:45+00:00 wall=4914 s; record: results/runs/K2_fine_large.m1.77-e5d0ad1d73b4/run.json
- `K2_fine_large.dt0.0035-6a0f9a80f290` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T01:15:34+00:00 wall=3507 s; record: results/runs/K2_fine_large.dt0.0035-6a0f9a80f290/run.json
- `K2_fine_large.D2x-bc527461f36d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:02+00:00 wall=3765 s; record: results/runs/K2_fine_large.D2x-bc527461f36d/run.json
- `K2_fine_large.D2x-4555577439db` status=completed parent=K2_fine_large.D2x-bc527461f36d created=2026-10-20T05:15:20+00:00 wall=5619 s; record: results/runs/K2_fine_large.D2x-4555577439db/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 4352582944.0, "relative_to_root": 3.7444966274088474, "experiment_wall_seconds": 17804.939727208002, "n_experiments": 4, "planner_calls": 6, "planner_cost_usd": 0, "loop_wall_seconds": 12464.868740948}
