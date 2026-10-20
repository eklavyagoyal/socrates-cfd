# Verification report: C1_large_timestep (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3238
- strouhal_number: 0.16351

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 3.42 with 3 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.03e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 8.42e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.08% <= 1.50% (root-to-finest change 0.019%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.0e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.25% <= 1.50% (root-to-finest change 0.064%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.4e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.36% <= 1.50% (root-to-finest change 0.932%) [three-level Celik procedure, observed order p=1.40, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.86% <= 1.50% (root-to-finest change 0.600%) [three-level Celik procedure, observed order p=1.49, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=8.69e-05
│   └── C1_large_timestep-49d90ffccdac
├── Temporal statistics (stationarity, cycles): PASS U=0.000103
│   └── C1_large_timestep-49d90ffccdac
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.000765
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): PASS U=0.0136
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D2x-cd501a12fa84

CLAIM: strouhal_number of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=1.26e-05
│   └── C1_large_timestep-49d90ffccdac
├── Temporal statistics (stationarity, cycles): PASS U=8.42e-05
│   └── C1_large_timestep-49d90ffccdac
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.00254
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): PASS U=0.0086
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D2x-cd501a12fa84

```

## EXPERIMENT HISTORY

Run C1_large_timestep-49d90ffccdac: submitted simulation (30580 cells, dt=0.05 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on C1_large_timestep-49d90ffccdac — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C1_large_timestep.m1.41-c9c1535204d3 (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on C1_large_timestep-49d90ffccdac — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected: identical experiment already in the evidence graph as C1_large_timestep.m1.41-c9c1535204d3

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on C1_large_timestep-49d90ffccdac — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C1_large_timestep.dt0.025-610f857bd6ea (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on C1_large_timestep-49d90ffccdac — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C1_large_timestep.D2x-f2b47ea2de80 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on C1_large_timestep.D2x-f2b47ea2de80 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> C1_large_timestep.D2x-cd501a12fa84 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run C1_large_timestep.m1.41-c9c1535204d3: REFINE_MESH from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.end_time: 150→80).

Run C1_large_timestep.dt0.025-610f857bd6ea: REDUCE_TIME_STEP from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, time.delta_t: 0.05→0.025, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3237 → 1.3235 (-0.02%).
  - Observation: strouhal_number 0.16351 → 0.16361 (+0.06%).

Run C1_large_timestep.D2x-f2b47ea2de80: EXPAND_DOMAIN from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3237 → 1.3149 (-0.67%).
  - Observation: strouhal_number 0.16351 → 0.16279 (-0.44%).

Run C1_large_timestep.D2x-cd501a12fa84: EXPAND_DOMAIN from C1_large_timestep.D2x-f2b47ea2de80 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3149 → 1.3115 (-0.26%).
  - Observation: strouhal_number 0.16279 → 0.16254 (-0.16%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C1_large_timestep-49d90ffccdac` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1159 s; record: results/runs/C1_large_timestep-49d90ffccdac/run.json
- `C1_large_timestep.m1.41-c9c1535204d3` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T03:41:02+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.41-c9c1535204d3/run.json
- `C1_large_timestep.dt0.025-610f857bd6ea` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T16:55:27+00:00 wall=906.3 s; record: results/runs/C1_large_timestep.dt0.025-610f857bd6ea/run.json
- `C1_large_timestep.D2x-f2b47ea2de80` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T04:12:05+00:00 wall=885.8 s; record: results/runs/C1_large_timestep.D2x-f2b47ea2de80/run.json
- `C1_large_timestep.D2x-cd501a12fa84` status=completed parent=C1_large_timestep.D2x-f2b47ea2de80 created=2026-10-20T04:26:51+00:00 wall=1204 s; record: results/runs/C1_large_timestep.D2x-cd501a12fa84/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 249959032.0, "relative_to_root": 2.72464608676695, "experiment_wall_seconds": 2995.9767474300047, "n_experiments": 4, "planner_calls": 6, "planner_cost_usd": 0, "loop_wall_seconds": 6869.729700421}
