# Verification report: F1_upwind_convection (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2687
- strouhal_number: 0.12614

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +11.3% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **INCONCLUSIVE** convection_scheme_order — convection scheme 'Gauss upwind' is formally first order; numerical diffusion must be shown negligible by mesh refinement before the result can be trusted
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.168% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.103% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.37e-07 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 3.89e-07 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 10.75% > 1.50% but the demonstrated change 1.05% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 8.2e-04)]
- **FAIL** mesh_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 6.74% under mesh refinement (> tau=3%); its value is not converged to the requested tolerance
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

### Evidence graph

```
CLAIM: mean_drag_coefficient of run F1_upwind_convection-e460c39ac86c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mesh_quality: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mass_conservation: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── linear_solver_convergence: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── courant_number: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── reynolds_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── force_reference_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── physics_regime: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── convection_scheme_order: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── Averaging window (reported vs stationary value): PASS U=0.00168
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long550-0c1a1cefdb26
├── Temporal statistics (stationarity, cycles): PASS U=1.37e-07
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long550-0c1a1cefdb26
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.108
│   └── F1_upwind_convection.long550-0c1a1cefdb26
│   └── F1_upwind_convection.m1.41-ad07dfae9c95
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── F1_upwind_convection-e460c39ac86c

CLAIM: strouhal_number of run F1_upwind_convection-e460c39ac86c is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mesh_quality: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mass_conservation: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── linear_solver_convergence: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── courant_number: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── reynolds_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── force_reference_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── physics_regime: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── convection_scheme_order: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── Averaging window (reported vs stationary value): PASS U=0.00103
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long550-0c1a1cefdb26
├── Temporal statistics (stationarity, cycles): PASS U=3.89e-07
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long550-0c1a1cefdb26
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── F1_upwind_convection.long550-0c1a1cefdb26
│   └── F1_upwind_convection.m1.41-ad07dfae9c95
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── F1_upwind_convection-e460c39ac86c

```

## EXPERIMENT HISTORY

Run F1_upwind_convection-e460c39ac86c: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on F1_upwind_convection-e460c39ac86c — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> F1_upwind_convection.long250-0dc1edea9982 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on F1_upwind_convection.long250-0dc1edea9982 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> F1_upwind_convection.long350-5250370f1da9 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on F1_upwind_convection.long350-5250370f1da9 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> F1_upwind_convection.long450-1cccde0d6ce6 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on F1_upwind_convection.long450-1cccde0d6ce6 — lift oscillation not yet a sustained limit cycle
  - Outcome: executed -> F1_upwind_convection.long550-0c1a1cefdb26 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: RUN_LONGER  on F1_upwind_convection.long550-0c1a1cefdb26 — lift oscillation not yet a sustained limit cycle
  - Outcome: rejected by validator: end time 650.0 exceeds limit 600.0

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - deterministic verdict INCONCLUSIVE
  - Requested: REFINE_MESH  on F1_upwind_convection.long550-0c1a1cefdb26 — mesh uncertainty component is unmeasured or not yet within budget
  - Outcome: executed -> F1_upwind_convection.m1.41-ad07dfae9c95 (completed)

Run F1_upwind_convection.long250-0dc1edea9982: RUN_LONGER from F1_upwind_convection-e460c39ac86c (time.end_time: 150→250).
  - Observation: mean_drag_coefficient 1.2674 → 1.2708 (+0.27%).
  - Observation: strouhal_number 0.12581 → 0.12626 (+0.36%).

Run F1_upwind_convection.long350-5250370f1da9: RUN_LONGER from F1_upwind_convection.long250-0dc1edea9982 (time.end_time: 250→350).
  - Observation: mean_drag_coefficient 1.2708 → 1.2708 (+0.00%).
  - Observation: strouhal_number 0.12626 → 0.12627 (+0.00%).

Run F1_upwind_convection.long450-1cccde0d6ce6: RUN_LONGER from F1_upwind_convection.long350-5250370f1da9 (time.end_time: 350→450).
  - Observation: mean_drag_coefficient 1.2708 → 1.2708 (+0.00%).
  - Observation: strouhal_number 0.12627 → 0.12627 (+0.00%).

Run F1_upwind_convection.long550-0c1a1cefdb26: RUN_LONGER from F1_upwind_convection.long450-1cccde0d6ce6 (time.end_time: 450→550).
  - Observation: mean_drag_coefficient 1.2708 → 1.2708 (+0.00%).
  - Observation: strouhal_number 0.12627 → 0.12627 (-0.00%).

Run F1_upwind_convection.m1.41-ad07dfae9c95: REFINE_MESH from F1_upwind_convection.long550-0c1a1cefdb26 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008694, time.end_time: 550→80).
  - Observation: mean_drag_coefficient 1.2708 → 1.2844 (+1.07%).
  - Observation: strouhal_number 0.12627 → 0.13539 (+7.22%).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_sensitivity[strouhal_number].
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=FAIL, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `F1_upwind_convection-e460c39ac86c` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1374 s; record: results/runs/F1_upwind_convection-e460c39ac86c/run.json
- `F1_upwind_convection.long250-0dc1edea9982` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-19T09:08:42+00:00 wall=1220 s; record: results/runs/F1_upwind_convection.long250-0dc1edea9982/run.json
- `F1_upwind_convection.long350-5250370f1da9` status=completed parent=F1_upwind_convection.long250-0dc1edea9982 created=2026-10-19T10:27:13+00:00 wall=866.8 s; record: results/runs/F1_upwind_convection.long350-5250370f1da9/run.json
- `F1_upwind_convection.long450-1cccde0d6ce6` status=completed parent=F1_upwind_convection.long350-5250370f1da9 created=2026-10-19T18:43:35+00:00 wall=747.2 s; record: results/runs/F1_upwind_convection.long450-1cccde0d6ce6/run.json
- `F1_upwind_convection.long550-0c1a1cefdb26` status=completed parent=F1_upwind_convection.long450-1cccde0d6ce6 created=2026-10-20T01:15:35+00:00 wall=724.4 s; record: results/runs/F1_upwind_convection.long550-0c1a1cefdb26/run.json
- `F1_upwind_convection.m1.41-ad07dfae9c95` status=completed parent=F1_upwind_convection.long550-0c1a1cefdb26 created=2026-10-20T03:41:02+00:00 wall=2505 s; record: results/runs/F1_upwind_convection.m1.41-ad07dfae9c95/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1787889932.0, "relative_to_root": 3.897732574667539, "experiment_wall_seconds": 6063.421056986995, "n_experiments": 5, "planner_calls": 6, "planner_cost_usd": 0, "loop_wall_seconds": 6844.857922661}
