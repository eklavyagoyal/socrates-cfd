# Verification report: B1_small_domain (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.5089
- strouhal_number: 0.17963

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 6.67e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.12e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.62e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.36% <= 1.50% (root-to-finest change 0.256%) [three-level Celik procedure, observed order p=3.31, Fs=1.25]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.13% <= 1.50% (root-to-finest change 0.744%) [three-level Celik procedure, observed order p=2.52, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.05% <= 1.50% (root-to-finest change 0.263%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.3e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.69% <= 1.50% (root-to-finest change 0.173%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.7e-05)]
- **FAIL** domain_sensitivity [mean_drag_coefficient] — mean_drag_coefficient of the run under verification changes by 8.86% under domain refinement (> tau=3%); its value is not converged to the requested tolerance
- **FAIL** domain_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 6.65% under domain refinement (> tau=3%); its value is not converged to the requested tolerance

### Evidence graph

```
CLAIM: mean_drag_coefficient of run B1_small_domain-a69ffb97a2e6 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mesh_quality: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mass_conservation: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── linear_solver_convergence: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── courant_number: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── reynolds_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── force_reference_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── physics_regime: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── convection_scheme_order: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── Averaging window (reported vs stationary value): PASS U=1.31e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal statistics (stationarity, cycles): PASS U=1.12e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Spatial discretisation (mesh sensitivity): PASS U=0.00356
│   └── B1_small_domain-a69ffb97a2e6
│   └── B1_small_domain.m1.41-21ba2b6971bf
│   └── B1_small_domain.m2-9feee10e9fa6
├── Temporal discretisation (time-step sensitivity): PASS U=0.0105
│   └── B1_small_domain-a69ffb97a2e6
│   └── B1_small_domain.dt0.005-61f238fa3616
└── Artificial boundaries (domain sensitivity): FAIL
    └── B1_small_domain-a69ffb97a2e6
    └── B1_small_domain.D2x-1e192fc39a3e

CLAIM: strouhal_number of run B1_small_domain-a69ffb97a2e6 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mesh_quality: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mass_conservation: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── linear_solver_convergence: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── courant_number: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── reynolds_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── force_reference_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── physics_regime: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── convection_scheme_order: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── Averaging window (reported vs stationary value): PASS U=9.75e-08
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal statistics (stationarity, cycles): PASS U=1.62e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Spatial discretisation (mesh sensitivity): PASS U=0.0113
│   └── B1_small_domain-a69ffb97a2e6
│   └── B1_small_domain.m1.41-21ba2b6971bf
│   └── B1_small_domain.m2-9feee10e9fa6
├── Temporal discretisation (time-step sensitivity): PASS U=0.00694
│   └── B1_small_domain-a69ffb97a2e6
│   └── B1_small_domain.dt0.005-61f238fa3616
└── Artificial boundaries (domain sensitivity): FAIL
    └── B1_small_domain-a69ffb97a2e6
    └── B1_small_domain.D2x-1e192fc39a3e

```

## EXPERIMENT HISTORY

Run B1_small_domain-a69ffb97a2e6: submitted simulation (13070 cells, dt=0.01 D/U, half-height 4 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on B1_small_domain-a69ffb97a2e6 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> B1_small_domain.m1.41-21ba2b6971bf (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on B1_small_domain.m1.41-21ba2b6971bf — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> B1_small_domain.m2-9feee10e9fa6 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on B1_small_domain-a69ffb97a2e6 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> B1_small_domain.dt0.005-61f238fa3616 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on B1_small_domain-a69ffb97a2e6 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> B1_small_domain.D2x-1e192fc39a3e (completed)

Run B1_small_domain.m1.41-21ba2b6971bf: REFINE_MESH from B1_small_domain-a69ffb97a2e6 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008552, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.5089 → 1.5119 (+0.20%).
  - Observation: strouhal_number 0.17963 → 0.18058 (+0.53%).

Run B1_small_domain.m2-9feee10e9fa6: REFINE_MESH from B1_small_domain.m1.41-21ba2b6971bf (mesh.refinement: 1.414→2, time.delta_t: 0.008552→0.006971).
  - Observation: mean_drag_coefficient 1.5119 → 1.5128 (+0.06%).
  - Observation: strouhal_number 0.18058 → 0.18098 (+0.22%).

Run B1_small_domain.dt0.005-61f238fa3616: REDUCE_TIME_STEP from B1_small_domain-a69ffb97a2e6 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.5089 → 1.505 (-0.26%).
  - Observation: strouhal_number 0.17963 → 0.17994 (+0.17%).

Run B1_small_domain.D2x-1e192fc39a3e: EXPAND_DOMAIN from B1_small_domain-a69ffb97a2e6 (averaging.start_time: 75→40, domain.downstream: 15→30, domain.half_height: 4→8, domain.upstream: 8→16, mesh.n_downstream: 56→86, mesh.n_lateral: 9→21, mesh.n_upstream: 19→28, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.5089 → 1.3862 (-8.13%).
  - Observation: strouhal_number 0.17963 → 0.16844 (-6.23%).

## FINAL JUSTIFICATION

Failed checks (measured): domain_sensitivity[mean_drag_coefficient], domain_sensitivity[strouhal_number].
- mean_drag_coefficient: REJECT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=FAIL; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=FAIL; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `B1_small_domain-a69ffb97a2e6` status=completed parent=None created=2026-10-19T07:02:08+00:00 wall=511 s; record: results/runs/B1_small_domain-a69ffb97a2e6/run.json
- `B1_small_domain.m1.41-21ba2b6971bf` status=completed parent=B1_small_domain-a69ffb97a2e6 created=2026-10-19T09:08:42+00:00 wall=1144 s; record: results/runs/B1_small_domain.m1.41-21ba2b6971bf/run.json
- `B1_small_domain.m2-9feee10e9fa6` status=completed parent=B1_small_domain.m1.41-21ba2b6971bf created=2026-10-19T10:24:04+00:00 wall=4760 s; record: results/runs/B1_small_domain.m2-9feee10e9fa6/run.json
- `B1_small_domain.dt0.005-61f238fa3616` status=completed parent=B1_small_domain-a69ffb97a2e6 created=2026-10-19T13:25:17+00:00 wall=1082 s; record: results/runs/B1_small_domain.dt0.005-61f238fa3616/run.json
- `B1_small_domain.D2x-1e192fc39a3e` status=completed parent=B1_small_domain-a69ffb97a2e6 created=2026-10-19T09:09:23+00:00 wall=695.4 s; record: results/runs/B1_small_domain.D2x-1e192fc39a3e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1206836760.0, "relative_to_root": 6.155760061208875, "experiment_wall_seconds": 7682.172272881, "n_experiments": 4, "planner_calls": 4, "planner_cost_usd": 0, "loop_wall_seconds": 16639.31266296}
