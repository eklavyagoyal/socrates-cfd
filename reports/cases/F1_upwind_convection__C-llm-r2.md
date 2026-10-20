# Verification report: F1_upwind_convection (C-llm-r2)

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
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.99e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.88e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 11.99% > 1.50% but the demonstrated change 2.00% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 9.6e-04)]
- **FAIL** mesh_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 11.45% under mesh refinement (> tau=3%); its value is not converged to the requested tolerance
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
│   └── F1_upwind_convection.long300-881ab970472f
├── Temporal statistics (stationarity, cycles): PASS U=1.99e-05
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long300-881ab970472f
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.12
│   └── F1_upwind_convection.long300-881ab970472f
│   └── F1_upwind_convection.m2-a5b11786bf96
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
│   └── F1_upwind_convection.long300-881ab970472f
├── Temporal statistics (stationarity, cycles): PASS U=1.88e-05
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long300-881ab970472f
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── F1_upwind_convection.long300-881ab970472f
│   └── F1_upwind_convection.m2-a5b11786bf96
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── F1_upwind_convection-e460c39ac86c

```

## EXPERIMENT HISTORY

Run F1_upwind_convection-e460c39ac86c: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT is not justified because no FAIL has been measured.
  - Three uncertainty components are unmeasured for both Cd and St: mesh, time and domain. There are 0 of 6 experiments used and 0.0 of 12.0 compute used, so there is budget for experiments.
  - R0 uses 'Gauss upwind', which is first order. The convection_scheme_order check is INCONCLUSIVE because numerical diffusion must be shown negligible by mesh refinement.
  - R0 is coarse: representative_cell_size_D is 0.45745, wake_last_cell_D is 1.0209, and there are 30580 cells. Numerical diffusion on this mesh could shift the Cd and St results by more than the 0.03 tolerance. This is a hypothesis, not a measurement.
  - The time-step evidence is weaker: backward (second-order) time scheme, 794.84 steps per shedding period, max Courant 0.73198. The domain is large (upstream_D 30, downstream_D 50, half_height_D 40, blockage_ratio 0.0125), so a domain effect is less likely to dominate.
  - Statistical margins are thin. St statistics uncertainty is 0.01474 against a 0.015 limit. Cd drift_rel is 0.010692. The stationary window start is the MSER cap (67.226), and the physics_regime check is INCONCLUSIVE because lift amplitude changes by +11.3%. RUN_LONGER is the next candidate after the mesh result.
  - REFINE_MESH on R0 targets the largest likely error source. It also clears the convection_scheme_order check if the change is small. Factor 2.0 gives the most discriminating signal for a first-order scheme. Its estimated cost is about 1691 s (R0 took 1373.7 s), which fits the budget.
  - Requested: REFINE_MESH {'factor': 2.0} on F1_upwind_convection-e460c39ac86c — R0 uses first-order upwind convection on a coarse mesh. Mesh error is unmeasured for both Cd and St, and it is the component most likely to change the answer by more than 3%.
  - Outcome: executed -> F1_upwind_convection.m2-a5b11786bf96 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed either, because no FAIL has been recorded. The mesh check is INCONCLUSIVE, not FAIL.
  - R0 and R1 differ a lot in the stationary-window values. Strouhal number is 0.12581 on R0 and 0.1426 on R1. Mean Cd is 1.2674 on R0 and 1.2968 on R1. The St shift looks much larger than the 0.03 tolerance. This is only a hint, because the verifier has not turned it into a mesh uncertainty.
  - The verifier says it cannot compute the mesh component because R0 is not statistically reliable: 10 cycles, Cd uncertainty 0.010692, St uncertainty 0.014742. Its instruction is 'run them longer first'. RUN_LONGER on R0 therefore unblocks the mesh check.
  - The R0 stationary window start is 67.226, which is the MSER cap (stationary_window_start_is_mser_cap true). The physics_regime check is INCONCLUSIVE because lift amplitude changes by +11.3% across the window. R0's St frequency resolution is 0.013333, which is coarse against the 0.03 tolerance. A longer R0 record addresses all three problems.
  - R1 has a small Cd ci95 (0.00051916) and drift (0.00095919) over 5 cycles. Its St FFT value, 0.14263, matches its window value, 0.1426. The weak member of the pair is R0, not R1. RUN_LONGER on R1 would cost 5959 s, versus 916 s at default length on R0.
  - Time and domain components are still unmeasured. They are lower priority because the mesh check is blocked by R0 reliability. Budget is 1 of 6 experiments and 3.47 of 12.0 compute, so there is room for a longer R0 run and later time and domain runs.
  - The R0 run is the root run, so extending it also improves the evidence for the requested quantities directly.
  - Requested: RUN_LONGER {'additional_convective_times': 150.0} on F1_upwind_convection-e460c39ac86c — The mesh check for both quantities is blocked because R0 is not statistically reliable. R0 also has a stationary window start at the MSER cap, a +11.3% lift amplitude change, and a coarse St frequency resolution of 0.013333. Extending R0 is the cheapest way to unblock the mesh comparison against R1 and to test whether the transient had ended.
  - Outcome: executed -> F1_upwind_convection.long300-881ab970472f (completed)

Run F1_upwind_convection.m2-a5b11786bf96: REFINE_MESH from F1_upwind_convection-e460c39ac86c (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006148, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2674 → 1.2968 (+2.32%).
  - Observation: strouhal_number 0.12581 → 0.1426 (+13.34%).

Run F1_upwind_convection.long300-881ab970472f: RUN_LONGER from F1_upwind_convection-e460c39ac86c (time.end_time: 150→300).
  - Observation: mean_drag_coefficient 1.2674 → 1.2708 (+0.27%).
  - Observation: strouhal_number 0.12581 → 0.12627 (+0.36%).

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
- `F1_upwind_convection.m2-a5b11786bf96` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-19T09:09:23+00:00 wall=7191 s; record: results/runs/F1_upwind_convection.m2-a5b11786bf96/run.json
- `F1_upwind_convection.long300-881ab970472f` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-20T07:51:06+00:00 wall=1671 s; record: results/runs/F1_upwind_convection.long300-881ab970472f/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 2050450160.0, "relative_to_root": 4.470133333333333, "experiment_wall_seconds": 8861.611396041983, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12612362, "loop_wall_seconds": 16413.524408732}
