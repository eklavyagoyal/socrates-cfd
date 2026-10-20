# Verification report: G2_average_from_start (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3196
- strouhal_number: 0.16144

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
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +6.7% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.866% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.220% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.77e-07 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.56e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.68% > 1.50% but the demonstrated change 0.28% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.8e-05)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 3.61% > 1.50% but the demonstrated change 0.60% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 4.3e-05)]
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.00866
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long560-8405e4f070b4
├── Temporal statistics (stationarity, cycles): PASS U=5.77e-07
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long560-8405e4f070b4
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0168
│   └── G2_average_from_start.long560-8405e4f070b4
│   └── G2_average_from_start.m1.41-bcf7a2407283
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── G2_average_from_start-e7384e5a2c24

CLAIM: strouhal_number of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.0122
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long560-8405e4f070b4
├── Temporal statistics (stationarity, cycles): PASS U=1.56e-06
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long560-8405e4f070b4
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0361
│   └── G2_average_from_start.long560-8405e4f070b4
│   └── G2_average_from_start.m1.41-bcf7a2407283
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── G2_average_from_start-e7384e5a2c24

```

## EXPERIMENT HISTORY

Run G2_average_from_start-e7384e5a2c24: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start-e7384e5a2c24 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G2_average_from_start.long160-24e243b2227c (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start.long160-24e243b2227c — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G2_average_from_start.long260-18ba4267ecae (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start.long260-18ba4267ecae — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G2_average_from_start.long360-ec6888d21be5 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start.long360-ec6888d21be5 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G2_average_from_start.long460-80fd951e7902 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start.long460-80fd951e7902 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> G2_average_from_start.long560-8405e4f070b4 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on G2_average_from_start.long560-8405e4f070b4 — lift oscillation not yet a sustained limit cycle
  - Outcome: rejected by validator: end time 660.0 exceeds limit 600.0

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on G2_average_from_start.long560-8405e4f070b4 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> G2_average_from_start.m1.41-bcf7a2407283 (completed)

Run G2_average_from_start.long160-24e243b2227c: RUN_LONGER from G2_average_from_start-e7384e5a2c24 (time.end_time: 60→160).
  - Observation: mean_drag_coefficient 1.3266 → 1.3311 (+0.34%).
  - Observation: strouhal_number 0.163 → 0.16344 (+0.27%).

Run G2_average_from_start.long260-18ba4267ecae: RUN_LONGER from G2_average_from_start.long160-24e243b2227c (time.end_time: 160→260).
  - Observation: mean_drag_coefficient 1.3311 → 1.3312 (+0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (+0.00%).

Run G2_average_from_start.long360-ec6888d21be5: RUN_LONGER from G2_average_from_start.long260-18ba4267ecae (time.end_time: 260→360).
  - Observation: mean_drag_coefficient 1.3312 → 1.3312 (+0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (-0.00%).

Run G2_average_from_start.long460-80fd951e7902: RUN_LONGER from G2_average_from_start.long360-ec6888d21be5 (time.end_time: 360→460).
  - Observation: mean_drag_coefficient 1.3312 → 1.3312 (-0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (-0.00%).

Run G2_average_from_start.long560-8405e4f070b4: RUN_LONGER from G2_average_from_start.long460-80fd951e7902 (time.end_time: 460→560).
  - Observation: mean_drag_coefficient 1.3312 → 1.3312 (-0.00%).
  - Observation: strouhal_number 0.16344 → 0.16344 (+0.00%).

Run G2_average_from_start.m1.41-bcf7a2407283: REFINE_MESH from G2_average_from_start.long560-8405e4f070b4 (averaging.start_time: 0→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 560→80).
  - Observation: mean_drag_coefficient 1.3312 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16344 → 0.16443 (+0.61%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G2_average_from_start-e7384e5a2c24` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=636.2 s; record: results/runs/G2_average_from_start-e7384e5a2c24/run.json
- `G2_average_from_start.long160-24e243b2227c` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T09:08:43+00:00 wall=1041 s; record: results/runs/G2_average_from_start.long160-24e243b2227c/run.json
- `G2_average_from_start.long260-18ba4267ecae` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-19T10:44:31+00:00 wall=1337 s; record: results/runs/G2_average_from_start.long260-18ba4267ecae/run.json
- `G2_average_from_start.long360-ec6888d21be5` status=completed parent=G2_average_from_start.long260-18ba4267ecae created=2026-10-19T16:30:05+00:00 wall=956.2 s; record: results/runs/G2_average_from_start.long360-ec6888d21be5/run.json
- `G2_average_from_start.long460-80fd951e7902` status=completed parent=G2_average_from_start.long360-ec6888d21be5 created=2026-10-19T17:33:55+00:00 wall=884.3 s; record: results/runs/G2_average_from_start.long460-80fd951e7902/run.json
- `G2_average_from_start.long560-8405e4f070b4` status=completed parent=G2_average_from_start.long460-80fd951e7902 created=2026-10-20T01:15:35+00:00 wall=827.6 s; record: results/runs/G2_average_from_start.long560-8405e4f070b4/run.json
- `G2_average_from_start.m1.41-bcf7a2407283` status=completed parent=G2_average_from_start.long560-8405e4f070b4 created=2026-10-20T03:41:03+00:00 wall=2765 s; record: results/runs/G2_average_from_start.m1.41-bcf7a2407283/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 2095039984.0, "relative_to_root": 11.418356136908654, "experiment_wall_seconds": 7810.687375180002, "n_experiments": 6, "planner_calls": 7, "planner_cost_usd": 0, "loop_wall_seconds": 7419.815203322}
