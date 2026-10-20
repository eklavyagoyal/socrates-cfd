# Verification report: K1_central_scheme (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3404
- strouhal_number: 0.16329

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linear' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.33e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.22e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 6.48% > 1.50% but the demonstrated change 0.23% <= tau; more refinement would be needed [three-level, observed order 0.16 outside [0.5, 2.0]x formal; p=min(observed, formal)=0.16 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.26% <= 1.50% (root-to-finest change 0.817%) [three-level Celik procedure, observed order p=2.37, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.91% <= 1.50% (root-to-finest change 0.228%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.3e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.48% <= 1.50% (root-to-finest change 0.120%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.57% > 1.50% but the demonstrated change 1.01% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.17, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.14% > 1.50% but the demonstrated change 0.59% <= tau; more refinement would be needed [three-level, observed order 2.01 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=7.04e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000133
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0648
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-f0705353471c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00913
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0157
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D2x-0c7e73f08a9e

CLAIM: strouhal_number of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=1.32e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000122
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): PASS U=0.0126
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-f0705353471c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00478
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0214
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D2x-0c7e73f08a9e

```

## EXPERIMENT HISTORY

Run K1_central_scheme-e4e5fb66bdca: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on K1_central_scheme-e4e5fb66bdca — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K1_central_scheme.m1.41-9a011a4052fe (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on K1_central_scheme.m1.41-9a011a4052fe — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K1_central_scheme.m2-f0705353471c (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on K1_central_scheme.m2-f0705353471c — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative refinement 2.83 exceeds limit 2.0

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on K1_central_scheme-e4e5fb66bdca — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K1_central_scheme.dt0.005-4f460bac38b7 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on K1_central_scheme-e4e5fb66bdca — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K1_central_scheme.D2x-b0a7ed20bbb5 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on K1_central_scheme.D2x-b0a7ed20bbb5 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> K1_central_scheme.D2x-0c7e73f08a9e (completed)

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on K1_central_scheme.D2x-0c7e73f08a9e — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative domain factor exceeds limit 4.0

**Critic iteration 8** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run K1_central_scheme.m1.41-9a011a4052fe: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008642, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3388 (-0.12%).
  - Observation: strouhal_number 0.1633 → 0.16423 (+0.57%).

Run K1_central_scheme.m2-f0705353471c: REFINE_MESH from K1_central_scheme.m1.41-9a011a4052fe (mesh.refinement: 1.414→2, time.delta_t: 0.008642→0.007502).
  - Observation: mean_drag_coefficient 1.3388 → 1.3373 (-0.11%).
  - Observation: strouhal_number 0.16423 → 0.16464 (+0.25%).

Run K1_central_scheme.dt0.005-4f460bac38b7: REDUCE_TIME_STEP from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3373 (-0.23%).
  - Observation: strouhal_number 0.1633 → 0.16349 (+0.12%).

Run K1_central_scheme.D2x-b0a7ed20bbb5: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3311 (-0.69%).
  - Observation: strouhal_number 0.1633 → 0.16252 (-0.47%).

Run K1_central_scheme.D2x-0c7e73f08a9e: EXPAND_DOMAIN from K1_central_scheme.D2x-b0a7ed20bbb5 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3311 → 1.327 (-0.31%).
  - Observation: strouhal_number 0.16252 → 0.16233 (-0.12%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K1_central_scheme-e4e5fb66bdca` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=4094 s; record: results/runs/K1_central_scheme-e4e5fb66bdca/run.json
- `K1_central_scheme.m1.41-9a011a4052fe` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T09:33:11+00:00 wall=3361 s; record: results/runs/K1_central_scheme.m1.41-9a011a4052fe/run.json
- `K1_central_scheme.m2-f0705353471c` status=completed parent=K1_central_scheme.m1.41-9a011a4052fe created=2026-10-20T01:15:34+00:00 wall=4868 s; record: results/runs/K1_central_scheme.m2-f0705353471c/run.json
- `K1_central_scheme.dt0.005-4f460bac38b7` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T03:41:02+00:00 wall=1455 s; record: results/runs/K1_central_scheme.dt0.005-4f460bac38b7/run.json
- `K1_central_scheme.D2x-b0a7ed20bbb5` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T16:16:09+00:00 wall=988.1 s; record: results/runs/K1_central_scheme.D2x-b0a7ed20bbb5/run.json
- `K1_central_scheme.D2x-0c7e73f08a9e` status=completed parent=K1_central_scheme.D2x-b0a7ed20bbb5 created=2026-10-20T04:05:21+00:00 wall=1867 s; record: results/runs/K1_central_scheme.D2x-0c7e73f08a9e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3106325542.0, "relative_to_root": 6.7720199302376285, "experiment_wall_seconds": 12539.277286243998, "n_experiments": 5, "planner_calls": 8, "planner_cost_usd": 0, "loop_wall_seconds": 13114.58379044}
