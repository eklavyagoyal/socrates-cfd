# Verification report: baseline (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3313
- strouhal_number: 0.16344

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
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 8.23e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 6.60e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.15% <= 1.50% (root-to-finest change 0.333%) [three-level, observed order 4.93 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.32% <= 1.50% (root-to-finest change 0.862%) [three-level Celik procedure, observed order p=2.43, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.10% <= 1.50% (root-to-finest change 0.276%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.31% <= 1.50% (root-to-finest change 0.077%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.6e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.81% > 1.50% but the demonstrated change 1.01% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.86, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.83% <= 1.50% (root-to-finest change 0.586%) [three-level Celik procedure, observed order p=1.55, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run baseline-408129116207 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── baseline-408129116207
├── mesh_quality: PASS
│   └── baseline-408129116207
├── mass_conservation: PASS
│   └── baseline-408129116207
├── linear_solver_convergence: PASS
│   └── baseline-408129116207
├── courant_number: PASS
│   └── baseline-408129116207
├── reynolds_consistency: PASS
│   └── baseline-408129116207
├── force_reference_consistency: PASS
│   └── baseline-408129116207
├── physics_regime: PASS
│   └── baseline-408129116207
├── convection_scheme_order: PASS
│   └── baseline-408129116207
├── Averaging window (reported vs stationary value): PASS U=9.37e-05
│   └── baseline-408129116207
├── Temporal statistics (stationarity, cycles): PASS U=8.23e-05
│   └── baseline-408129116207
├── Spatial discretisation (mesh sensitivity): PASS U=0.0115
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.011
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0181
    └── baseline-408129116207
    └── baseline.D2x-efba395f6c27
    └── baseline.D2x-4312d7d8fec3

CLAIM: strouhal_number of run baseline-408129116207 is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── baseline-408129116207
├── mesh_quality: PASS
│   └── baseline-408129116207
├── mass_conservation: PASS
│   └── baseline-408129116207
├── linear_solver_convergence: PASS
│   └── baseline-408129116207
├── courant_number: PASS
│   └── baseline-408129116207
├── reynolds_consistency: PASS
│   └── baseline-408129116207
├── force_reference_consistency: PASS
│   └── baseline-408129116207
├── physics_regime: PASS
│   └── baseline-408129116207
├── convection_scheme_order: PASS
│   └── baseline-408129116207
├── Averaging window (reported vs stationary value): PASS U=1.55e-05
│   └── baseline-408129116207
├── Temporal statistics (stationarity, cycles): PASS U=6.6e-05
│   └── baseline-408129116207
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.00309
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): PASS U=0.00829
    └── baseline-408129116207
    └── baseline.D2x-efba395f6c27
    └── baseline.D2x-4312d7d8fec3

```

## EXPERIMENT HISTORY

Run baseline-408129116207: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on baseline-408129116207 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> baseline.m1.41-807cdf343a51 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on baseline.m1.41-807cdf343a51 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> baseline.m2-476115cbbf20 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on baseline-408129116207 — time uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> baseline.dt0.005-693742b868bc (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on baseline-408129116207 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> baseline.D2x-efba395f6c27 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on baseline.D2x-efba395f6c27 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> baseline.D2x-4312d7d8fec3 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: EXPAND_DOMAIN  on baseline.D2x-4312d7d8fec3 — domain uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected by validator: cumulative domain factor exceeds limit 4.0

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Outcome: planner chose to stop (no useful affordable experiment)

Run baseline.m1.41-807cdf343a51: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run baseline.m2-476115cbbf20: REFINE_MESH from baseline.m1.41-807cdf343a51 (mesh.refinement: 1.414→2, time.delta_t: 0.008673→0.007524).
  - Observation: mean_drag_coefficient 1.3349 → 1.3356 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run baseline.dt0.005-693742b868bc: REDUCE_TIME_STEP from baseline-408129116207 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run baseline.D2x-efba395f6c27: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3226 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

Run baseline.D2x-4312d7d8fec3: EXPAND_DOMAIN from baseline.D2x-efba395f6c27 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3226 → 1.3179 (-0.36%).
  - Observation: strouhal_number 0.16272 → 0.16248 (-0.15%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0159 vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `baseline-408129116207` status=completed parent=None created=2026-10-19T07:00:06+00:00 wall=1442 s; record: results/runs/baseline-408129116207/run.json
- `baseline.m1.41-807cdf343a51` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=5234 s; record: results/runs/baseline.m1.41-807cdf343a51/run.json
- `baseline.m2-476115cbbf20` status=completed parent=baseline.m1.41-807cdf343a51 created=2026-10-19T09:41:41+00:00 wall=6871 s; record: results/runs/baseline.m2-476115cbbf20/run.json
- `baseline.dt0.005-693742b868bc` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=4058 s; record: results/runs/baseline.dt0.005-693742b868bc/run.json
- `baseline.D2x-efba395f6c27` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=3659 s; record: results/runs/baseline.D2x-efba395f6c27/run.json
- `baseline.D2x-4312d7d8fec3` status=completed parent=baseline.D2x-efba395f6c27 created=2026-10-19T09:15:09+00:00 wall=3214 s; record: results/runs/baseline.D2x-4312d7d8fec3/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3100386224.0, "relative_to_root": 6.75907177676041, "experiment_wall_seconds": 23036.304041032, "n_experiments": 5, "planner_calls": 7, "planner_cost_usd": 0, "loop_wall_seconds": 11395.247138723}
