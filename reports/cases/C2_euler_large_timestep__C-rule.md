# Verification report: C2_euler_large_timestep (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2901
- strouhal_number: 0.15849

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 2.92 with 2 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.66e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.27e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 3.32% > 1.50% but the demonstrated change 2.17% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.81, Fs=1.25]
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 4.02% > 1.50% but the demonstrated change 2.77% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.93, Fs=1.25]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.41% <= 1.50% (root-to-finest change 0.975%) [three-level Celik procedure, observed order p=1.44, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.84% <= 1.50% (root-to-finest change 0.602%) [three-level Celik procedure, observed order p=1.62, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=9.49e-07
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal statistics (stationarity, cycles): PASS U=0.000166
│   └── C2_euler_large_timestep-268eddd71f94
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0332
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
│   └── C2_euler_large_timestep.dt0.005-752b3af02251
└── Artificial boundaries (domain sensitivity): PASS U=0.0141
    └── C2_euler_large_timestep-268eddd71f94
    └── C2_euler_large_timestep.D2x-a912f88e2d43
    └── C2_euler_large_timestep.D2x-fa5f34107d8d

CLAIM: strouhal_number of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=1.57e-05
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal statistics (stationarity, cycles): PASS U=0.000127
│   └── C2_euler_large_timestep-268eddd71f94
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0402
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
│   └── C2_euler_large_timestep.dt0.005-752b3af02251
└── Artificial boundaries (domain sensitivity): PASS U=0.00842
    └── C2_euler_large_timestep-268eddd71f94
    └── C2_euler_large_timestep.D2x-a912f88e2d43
    └── C2_euler_large_timestep.D2x-fa5f34107d8d

```

## EXPERIMENT HISTORY

Run C2_euler_large_timestep-268eddd71f94: submitted simulation (30580 cells, dt=0.04 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on C2_euler_large_timestep-268eddd71f94 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.m1.41-eb9ef468444b (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on C2_euler_large_timestep-268eddd71f94 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected: identical experiment already in the evidence graph as C2_euler_large_timestep.m1.41-eb9ef468444b

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on C2_euler_large_timestep-268eddd71f94 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.dt0.01-f9cf9b35455e (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on C2_euler_large_timestep.dt0.01-f9cf9b35455e — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.dt0.005-752b3af02251 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on C2_euler_large_timestep.dt0.005-752b3af02251 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: time step 0.0025 below limit 0.005

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on C2_euler_large_timestep-268eddd71f94 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.D2x-a912f88e2d43 (completed)

**Critic iteration 8** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on C2_euler_large_timestep.D2x-a912f88e2d43 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C2_euler_large_timestep.D2x-fa5f34107d8d (completed)

Run C2_euler_large_timestep.m1.41-eb9ef468444b: REFINE_MESH from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.end_time: 150→80).

Run C2_euler_large_timestep.dt0.02-2f2ce6b4d241: REDUCE_TIME_STEP from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, time.delta_t: 0.04→0.02, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.3047 (+1.13%).
  - Observation: strouhal_number 0.15848 → 0.16096 (+1.56%).

Run C2_euler_large_timestep.dt0.01-f9cf9b35455e: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (time.delta_t: 0.02→0.01).
  - Observation: mean_drag_coefficient 1.3047 → 1.3139 (+0.70%).
  - Observation: strouhal_number 0.16096 → 0.16231 (+0.84%).

Run C2_euler_large_timestep.dt0.005-752b3af02251: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.01-f9cf9b35455e (time.delta_t: 0.01→0.005).
  - Observation: mean_drag_coefficient 1.3139 → 1.3188 (+0.37%).
  - Observation: strouhal_number 0.16231 → 0.163 (+0.42%).

Run C2_euler_large_timestep.D2x-a912f88e2d43: EXPAND_DOMAIN from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.281 (-0.71%).
  - Observation: strouhal_number 0.15848 → 0.15777 (-0.45%).

Run C2_euler_large_timestep.D2x-fa5f34107d8d: EXPAND_DOMAIN from C2_euler_large_timestep.D2x-a912f88e2d43 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.281 → 1.2777 (-0.26%).
  - Observation: strouhal_number 0.15777 → 0.15754 (-0.15%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=PASS; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time.
- strouhal_number: not established — mesh, time.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C2_euler_large_timestep-268eddd71f94` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1056 s; record: results/runs/C2_euler_large_timestep-268eddd71f94/run.json
- `C2_euler_large_timestep.m1.41-eb9ef468444b` status=failed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T09:08:42+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m1.41-eb9ef468444b/run.json
- `C2_euler_large_timestep.dt0.02-2f2ce6b4d241` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T17:02:32+00:00 wall=818.4 s; record: results/runs/C2_euler_large_timestep.dt0.02-2f2ce6b4d241/run.json
- `C2_euler_large_timestep.dt0.01-f9cf9b35455e` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-19T19:14:28+00:00 wall=1418 s; record: results/runs/C2_euler_large_timestep.dt0.01-f9cf9b35455e/run.json
- `C2_euler_large_timestep.dt0.005-752b3af02251` status=completed parent=C2_euler_large_timestep.dt0.01-f9cf9b35455e created=2026-10-19T19:42:57+00:00 wall=2541 s; record: results/runs/C2_euler_large_timestep.dt0.005-752b3af02251/run.json
- `C2_euler_large_timestep.D2x-a912f88e2d43` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T19:14:28+00:00 wall=643.5 s; record: results/runs/C2_euler_large_timestep.D2x-a912f88e2d43/run.json
- `C2_euler_large_timestep.D2x-fa5f34107d8d` status=completed parent=C2_euler_large_timestep.D2x-a912f88e2d43 created=2026-10-19T20:56:36+00:00 wall=798.5 s; record: results/runs/C2_euler_large_timestep.D2x-fa5f34107d8d/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1046859718.0, "relative_to_root": 9.128927124482232, "experiment_wall_seconds": 6219.248803382019, "n_experiments": 6, "planner_calls": 8, "planner_cost_usd": 0, "loop_wall_seconds": 52589.600216932005}
