# Verification report: G1_premature_averaging (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2961
- strouhal_number: 0.16129

## VERDICT: **INCONCLUSIVE**

Stop reason: compute budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +25.8% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 2.635% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.315% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 8.05e-07 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.13e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0263
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long440-c4155f5b634a
├── Temporal statistics (stationarity, cycles): PASS U=8.05e-07
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long440-c4155f5b634a
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── G1_premature_averaging-17c0143468d7

CLAIM: strouhal_number of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0131
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long440-c4155f5b634a
├── Temporal statistics (stationarity, cycles): PASS U=2.13e-06
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long440-c4155f5b634a
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── G1_premature_averaging-17c0143468d7

```

## EXPERIMENT HISTORY

Run G1_premature_averaging-17c0143468d7: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G1_premature_averaging-17c0143468d7 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G1_premature_averaging.long140-34c6cca905d9 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G1_premature_averaging.long140-34c6cca905d9 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G1_premature_averaging.long240-ddb0109abd94 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G1_premature_averaging.long240-ddb0109abd94 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G1_premature_averaging.long340-807cb251d414 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G1_premature_averaging.long340-807cb251d414 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G1_premature_averaging.long440-c4155f5b634a (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G1_premature_averaging.long440-c4155f5b634a — lift oscillation not yet a sustained limit cycle
  - Outcome: rejected: estimated cost 2.5x root exceeds remaining budget 2.0x

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on G1_premature_averaging.long440-c4155f5b634a — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected: estimated cost 4.6x root exceeds remaining budget 2.0x

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REDUCE_TIME_STEP  on G1_premature_averaging.long440-c4155f5b634a — time uncertainty component is unmeasured or not yet within budget
  - Outcome: rejected: estimated cost 4.0x root exceeds remaining budget 2.0x

Run G1_premature_averaging.long140-34c6cca905d9: RUN_LONGER from G1_premature_averaging-17c0143468d7 (time.end_time: 40→140).
  - Observation: mean_drag_coefficient 1.3039 → 1.3311 (+2.09%).
  - Observation: strouhal_number 0.16058 → 0.16343 (+1.78%).

Run G1_premature_averaging.long240-ddb0109abd94: RUN_LONGER from G1_premature_averaging.long140-34c6cca905d9 (time.end_time: 140→240).
  - Observation: mean_drag_coefficient 1.3311 → 1.3312 (+0.00%).
  - Observation: strouhal_number 0.16343 → 0.16344 (+0.00%).

Run G1_premature_averaging.long340-807cb251d414: RUN_LONGER from G1_premature_averaging.long240-ddb0109abd94 (time.end_time: 240→340).
  - Observation: mean_drag_coefficient 1.3312 → 1.3312 (+0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (+0.00%).

Run G1_premature_averaging.long440-c4155f5b634a: RUN_LONGER from G1_premature_averaging.long340-807cb251d414 (time.end_time: 340→440).
  - Observation: mean_drag_coefficient 1.3312 → 1.3312 (-0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (+0.00%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G1_premature_averaging-17c0143468d7` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=391.6 s; record: results/runs/G1_premature_averaging-17c0143468d7/run.json
- `G1_premature_averaging.long140-34c6cca905d9` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-19T09:08:45+00:00 wall=939.3 s; record: results/runs/G1_premature_averaging.long140-34c6cca905d9/run.json
- `G1_premature_averaging.long240-ddb0109abd94` status=completed parent=G1_premature_averaging.long140-34c6cca905d9 created=2026-10-20T01:15:35+00:00 wall=720.9 s; record: results/runs/G1_premature_averaging.long240-ddb0109abd94/run.json
- `G1_premature_averaging.long340-807cb251d414` status=completed parent=G1_premature_averaging.long240-ddb0109abd94 created=2026-10-20T03:41:03+00:00 wall=1266 s; record: results/runs/G1_premature_averaging.long340-807cb251d414/run.json
- `G1_premature_averaging.long440-c4155f5b634a` status=completed parent=G1_premature_averaging.long340-807cb251d414 created=2026-10-20T07:29:58+00:00 wall=1168 s; record: results/runs/G1_premature_averaging.long440-c4155f5b634a/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1223200000.0, "relative_to_root": 10.0, "experiment_wall_seconds": 4094.0049051409987, "n_experiments": 4, "planner_calls": 7, "planner_cost_usd": 0, "loop_wall_seconds": 14908.899337623001}
