# Verification report: A2_moderate_mesh (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3221
- strouhal_number: 0.16157

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.56 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.004% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 7.17e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 5.21e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.60% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.50, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.58% > 1.50% but the demonstrated change 1.76% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.71, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.17% <= 1.50% (root-to-finest change 0.292%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.36% <= 1.50% (root-to-finest change 0.090%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.4e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.35% <= 1.50% (root-to-finest change 0.941%) [three-level Celik procedure, observed order p=1.48, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.84% <= 1.50% (root-to-finest change 0.611%) [three-level Celik procedure, observed order p=1.71, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=4.43e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Temporal statistics (stationarity, cycles): PASS U=7.17e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.016
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-69c39fb43565
├── Temporal discretisation (time-step sensitivity): PASS U=0.0117
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): PASS U=0.0135
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D2x-b76a220ade27

CLAIM: strouhal_number of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=8.52e-06
│   └── A2_moderate_mesh-1c5ea01594aa
├── Temporal statistics (stationarity, cycles): PASS U=5.21e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0258
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-69c39fb43565
├── Temporal discretisation (time-step sensitivity): PASS U=0.00362
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): PASS U=0.00843
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D2x-b76a220ade27

```

## EXPERIMENT HISTORY

Run A2_moderate_mesh-1c5ea01594aa: submitted simulation (17162 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on A2_moderate_mesh-1c5ea01594aa — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> A2_moderate_mesh.m1.06-c5d153eb41a5 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on A2_moderate_mesh.m1.06-c5d153eb41a5 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> A2_moderate_mesh.m1.5-69c39fb43565 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on A2_moderate_mesh.m1.5-69c39fb43565 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative refinement 2.83 exceeds limit 2.0

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on A2_moderate_mesh-1c5ea01594aa — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> A2_moderate_mesh.dt0.005-4720e4eddcde (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on A2_moderate_mesh-1c5ea01594aa — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> A2_moderate_mesh.D2x-4a8a18327a27 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on A2_moderate_mesh.D2x-4a8a18327a27 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> A2_moderate_mesh.D2x-b76a220ade27 (completed)

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run A2_moderate_mesh.m1.06-c5d153eb41a5: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.061, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3321 (+0.75%).
  - Observation: strouhal_number 0.16157 → 0.16364 (+1.28%).

Run A2_moderate_mesh.m1.5-69c39fb43565: REFINE_MESH from A2_moderate_mesh.m1.06-c5d153eb41a5 (mesh.refinement: 1.061→1.5).
  - Observation: mean_drag_coefficient 1.3321 → 1.3363 (+0.32%).
  - Observation: strouhal_number 0.16364 → 0.16446 (+0.50%).

Run A2_moderate_mesh.dt0.005-4720e4eddcde: REDUCE_TIME_STEP from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3183 (-0.29%).
  - Observation: strouhal_number 0.16157 → 0.16172 (+0.09%).

Run A2_moderate_mesh.D2x-4a8a18327a27: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3131 (-0.69%).
  - Observation: strouhal_number 0.16157 → 0.16082 (-0.46%).

Run A2_moderate_mesh.D2x-b76a220ade27: EXPAND_DOMAIN from A2_moderate_mesh.D2x-4a8a18327a27 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3131 → 1.3099 (-0.25%).
  - Observation: strouhal_number 0.16082 → 0.16059 (-0.14%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A2_moderate_mesh-1c5ea01594aa` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=2124 s; record: results/runs/A2_moderate_mesh-1c5ea01594aa/run.json
- `A2_moderate_mesh.m1.06-c5d153eb41a5` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T09:43:44+00:00 wall=1223 s; record: results/runs/A2_moderate_mesh.m1.06-c5d153eb41a5/run.json
- `A2_moderate_mesh.m1.5-69c39fb43565` status=completed parent=A2_moderate_mesh.m1.06-c5d153eb41a5 created=2026-10-19T10:04:58+00:00 wall=2428 s; record: results/runs/A2_moderate_mesh.m1.5-69c39fb43565/run.json
- `A2_moderate_mesh.dt0.005-4720e4eddcde` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:07:48+00:00 wall=764.5 s; record: results/runs/A2_moderate_mesh.dt0.005-4720e4eddcde/run.json
- `A2_moderate_mesh.D2x-4a8a18327a27` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:38:04+00:00 wall=438.6 s; record: results/runs/A2_moderate_mesh.D2x-4a8a18327a27/run.json
- `A2_moderate_mesh.D2x-b76a220ade27` status=completed parent=A2_moderate_mesh.D2x-4a8a18327a27 created=2026-10-20T01:15:35+00:00 wall=611.5 s; record: results/runs/A2_moderate_mesh.D2x-b76a220ade27/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1521168000.0, "relative_to_root": 5.90905488870761, "experiment_wall_seconds": 5466.021279772987, "n_experiments": 5, "planner_calls": 7, "planner_cost_usd": 0, "loop_wall_seconds": 617.7800807790001}
