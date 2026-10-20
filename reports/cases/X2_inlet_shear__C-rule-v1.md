# Verification report: X2_inlet_shear (C-rule-v1)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3312
- strouhal_number: 0.16312

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.047% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.035% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.27e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.50e-03 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.76% <= 1.50% (root-to-finest change 0.254%) [differences within 2x statistical noise (2.3e-03); range-based U with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.18% <= 1.50% (root-to-finest change 0.828%) [three-level Celik procedure, observed order p=3.01, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.14% <= 1.50% (root-to-finest change 0.285%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.3e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.75% <= 1.50% (root-to-finest change 0.085%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.5e-03)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — family member(s) not statistically reliable for mean_drag_coefficient (run, cycles, uncertainty): [('X2_inlet_shear.long280-a5bb8f1a8800', 24, 0.007824449618541073)]; run them longer first
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — family member(s) not statistically reliable for strouhal_number (run, cycles, uncertainty): [('X2_inlet_shear.long280-a5bb8f1a8800', 24, 0.006186083008221495)]; run them longer first

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000473
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.00227
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): PASS U=0.00761
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.m1.41-ca5c50f2e498
│   └── X2_inlet_shear.m2-3f2d80a2a02e
├── Temporal discretisation (time-step sensitivity): PASS U=0.0114
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.dt0.005-2ef6d66a694b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── X2_inlet_shear-32168bfbca6b
    └── X2_inlet_shear.long280-a5bb8f1a8800

CLAIM: strouhal_number of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000352
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.0025
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): PASS U=0.0118
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.m1.41-ca5c50f2e498
│   └── X2_inlet_shear.m2-3f2d80a2a02e
├── Temporal discretisation (time-step sensitivity): PASS U=0.00749
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.dt0.005-2ef6d66a694b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── X2_inlet_shear-32168bfbca6b
    └── X2_inlet_shear.long280-a5bb8f1a8800

```

## EXPERIMENT HISTORY

Run X2_inlet_shear-32168bfbca6b: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on X2_inlet_shear-32168bfbca6b — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X2_inlet_shear.m1.41-ca5c50f2e498 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on X2_inlet_shear.m1.41-ca5c50f2e498 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X2_inlet_shear.m2-3f2d80a2a02e (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on X2_inlet_shear-32168bfbca6b — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X2_inlet_shear.dt0.005-2ef6d66a694b (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on X2_inlet_shear-32168bfbca6b — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> X2_inlet_shear.D2x-8d92db3cbed0 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on X2_inlet_shear.D2x-8d92db3cbed0 — refinement-family member X2_inlet_shear.D2x-8d92db3cbed0 is not statistically reliable
  - Outcome: executed -> X2_inlet_shear.long180-79490e8e4d8c (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on X2_inlet_shear.long180-79490e8e4d8c — refinement-family member X2_inlet_shear.long180-79490e8e4d8c is not statistically reliable
  - Outcome: executed -> X2_inlet_shear.long280-a5bb8f1a8800 (completed)

Run X2_inlet_shear.m1.41-ca5c50f2e498: REFINE_MESH from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.00869, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3338 (+0.24%).
  - Observation: strouhal_number 0.16318 → 0.16419 (+0.62%).

Run X2_inlet_shear.m2-3f2d80a2a02e: REFINE_MESH from X2_inlet_shear.m1.41-ca5c50f2e498 (mesh.refinement: 1.414→2, time.delta_t: 0.00869→0.007432).
  - Observation: mean_drag_coefficient 1.3338 → 1.334 (+0.01%).
  - Observation: strouhal_number 0.16419 → 0.16454 (+0.21%).

Run X2_inlet_shear.dt0.005-2ef6d66a694b: REDUCE_TIME_STEP from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3268 (-0.28%).
  - Observation: strouhal_number 0.16318 → 0.16332 (+0.08%).

Run X2_inlet_shear.D2x-8d92db3cbed0: EXPAND_DOMAIN from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.4857 (+11.66%).
  - Observation: strouhal_number 0.16318 → 0.17529 (+7.42%).

Run X2_inlet_shear.long180-79490e8e4d8c: RUN_LONGER from X2_inlet_shear.D2x-8d92db3cbed0 (time.end_time: 80→180).
  - Observation: mean_drag_coefficient 1.4857 → 1.3548 (-8.81%).
  - Observation: strouhal_number 0.17529 → 0.16578 (-5.42%).

Run X2_inlet_shear.long280-a5bb8f1a8800: RUN_LONGER from X2_inlet_shear.long180-79490e8e4d8c (time.end_time: 180→280).
  - Observation: mean_drag_coefficient 1.3548 → 1.323 (-2.34%).
  - Observation: strouhal_number 0.16578 → 0.16269 (-1.87%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X2_inlet_shear-32168bfbca6b` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=1984 s; record: results/runs/X2_inlet_shear-32168bfbca6b/run.json
- `X2_inlet_shear.m1.41-ca5c50f2e498` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T10:06:49+00:00 wall=2448 s; record: results/runs/X2_inlet_shear.m1.41-ca5c50f2e498/run.json
- `X2_inlet_shear.m2-3f2d80a2a02e` status=completed parent=X2_inlet_shear.m1.41-ca5c50f2e498 created=2026-10-19T11:25:18+00:00 wall=7000 s; record: results/runs/X2_inlet_shear.m2-3f2d80a2a02e/run.json
- `X2_inlet_shear.dt0.005-2ef6d66a694b` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T18:29:05+00:00 wall=1343 s; record: results/runs/X2_inlet_shear.dt0.005-2ef6d66a694b/run.json
- `X2_inlet_shear.D2x-8d92db3cbed0` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T10:07:14+00:00 wall=1191 s; record: results/runs/X2_inlet_shear.D2x-8d92db3cbed0/run.json
- `X2_inlet_shear.long180-79490e8e4d8c` status=completed parent=X2_inlet_shear.D2x-8d92db3cbed0 created=2026-10-19T21:36:42+00:00 wall=1367 s; record: results/runs/X2_inlet_shear.long180-79490e8e4d8c/run.json
- `X2_inlet_shear.long280-a5bb8f1a8800` status=completed parent=X2_inlet_shear.long180-79490e8e4d8c created=2026-10-20T03:41:01+00:00 wall=1759 s; record: results/runs/X2_inlet_shear.long280-a5bb8f1a8800/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3507667876.0, "relative_to_root": 7.646975966862874, "experiment_wall_seconds": 15108.475957746003, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0, "loop_wall_seconds": 11248.472000612}
