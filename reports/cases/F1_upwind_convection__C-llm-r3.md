# Verification report: F1_upwind_convection (C-llm-r3)

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
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 3.29e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.68e-06 <= 1.50%
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
│   └── F1_upwind_convection.long350-3e56ac0814bc
├── Temporal statistics (stationarity, cycles): PASS U=3.29e-06
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long350-3e56ac0814bc
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.12
│   └── F1_upwind_convection.long350-3e56ac0814bc
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
│   └── F1_upwind_convection.long350-3e56ac0814bc
├── Temporal statistics (stationarity, cycles): PASS U=1.68e-06
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long350-3e56ac0814bc
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── F1_upwind_convection.long350-3e56ac0814bc
│   └── F1_upwind_convection.m2-a5b11786bf96
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── F1_upwind_convection-e460c39ac86c

```

## EXPERIMENT HISTORY

Run F1_upwind_convection-e460c39ac86c: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified because no FAIL has been measured.
  - Mesh, time and domain uncertainty components are all unmeasured for both quantities (mesh_sensitivity, time_sensitivity and domain_sensitivity are INCONCLUSIVE). No combined uncertainty can be formed.
  - R0 uses 'Gauss upwind', which is formally first order. The convection_scheme_order check is INCONCLUSIVE until mesh refinement shows numerical diffusion is negligible.
  - R0's mesh is coarse for resolving the wake: representative_cell_size_D is 0.45745, wake_last_cell_D is 1.0209, and the mesh has 30580 cells. This makes spatial/numerical-diffusion error the most likely effect to exceed the 0.03 tolerance on both mean_drag_coefficient and strouhal_number.
  - Time and domain look less suspect: max_courant is 0.73198, steps_per_shedding_period is 794.84, and blockage_ratio is 0.0125 with upstream_D 30, downstream_D 50 and half_height_D 40.
  - Physics_regime is INCONCLUSIVE because the lift amplitude changes by +11.3% across the window. The stationary window start (67.226) is the MSER cap, so the run may not be at a sustained limit cycle. This is a second concern, best examined once the mesh effect is known.
  - Statistical uncertainty is 0.01069 for drag and 0.01474 for Strouhal. The Strouhal value is close to its 1.5% limit (half of the 0.03 tolerance). The averaging bias is small (0.001038 and 0.002589).
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute used. REFINE_MESH is therefore affordable and is the most informative next step.
  - Requested: REFINE_MESH {'factor': 2.0} on F1_upwind_convection-e460c39ac86c — R0 combines a first-order upwind scheme with a coarse mesh (representative_cell_size_D 0.45745, wake_last_cell_D 1.0209). Numerical diffusion is the most likely flaw to shift drag or Strouhal by more than 3%. The largest allowed factor gives the clearest signal against the ~1% statistical noise, and the budget (0 of 6 experiments, 0 of 12 relative compute used) can afford it.
  - Outcome: executed -> F1_upwind_convection.m2-a5b11786bf96 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT is not allowed because no FAIL has been recorded.
  - R0 and R1 stationary-window values differ. Drag goes from 1.2674 to 1.2968 (about 2.3%). Strouhal goes from 0.12581 to 0.1426 (about 13%). The Strouhal shift is far above the 0.03 tolerance. The verifier has not turned it into a FAIL or a mesh uncertainty, because it treats R0 as statistically unreliable.
  - mesh_sensitivity is INCONCLUSIVE for both quantities. Its stated reason is that R0 (10 cycles, drag uncertainty 0.010692, Strouhal uncertainty 0.014742) is not statistically reliable, and it says to run it longer first. The mesh component stays unusable until R0 is extended.
  - physics_regime is INCONCLUSIVE for R0. The lift amplitude changes by +11.3% across the window, so it is not yet a sustained limit cycle. R0's stationary window start (67.226) is the MSER cap. R0 rms lift is 0.12493 against 0.19709 in R1, which fits a still-developing wake.
  - R0's Strouhal frequency resolution is 0.013333, about 10% of its Strouhal value (0.12581). R0's Strouhal statistical uncertainty (0.01474) is close to its 1.5% component limit. A longer record directly improves both.
  - R1 is not allowed to refine further (cumulative refinement limit) or to expand the domain (cell limit). R0 is therefore the only parent for the remaining experiments.
  - RUN_LONGER on R0 is the cheapest experiment (estimated 916 s at default length). It resolves the blocker named by the verifier. Budget used is 1 of 6 experiments and 3.47 of 12 relative compute, so there is room for time-step and domain runs afterwards.
  - Requested: RUN_LONGER {'additional_convective_times': 200.0} on F1_upwind_convection-e460c39ac86c — The mesh_sensitivity check names R0 as not statistically reliable (10 cycles, uncertainty 0.010692 for drag and 0.014742 for Strouhal) and says to run it longer first. physics_regime is also INCONCLUSIVE because of the +11.3% lift amplitude drift, and R0's stationary window start is the MSER cap. A longer R0 record tests whether the transient had ended and tightens the statistics. It also unblocks the R0-to-R1 mesh comparison, which currently shows a Strouhal shift of about 13% that the verifier cannot yet use. It is cheap compared with the other experiments.
  - Outcome: executed -> F1_upwind_convection.long350-3e56ac0814bc (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 2.3%

Run F1_upwind_convection.m2-a5b11786bf96: REFINE_MESH from F1_upwind_convection-e460c39ac86c (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006148, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2674 → 1.2968 (+2.32%).
  - Observation: strouhal_number 0.12581 → 0.1426 (+13.34%).

Run F1_upwind_convection.long350-3e56ac0814bc: RUN_LONGER from F1_upwind_convection-e460c39ac86c (time.end_time: 150→350).
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
- `F1_upwind_convection.long350-3e56ac0814bc` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-19T21:14:39+00:00 wall=1529 s; record: results/runs/F1_upwind_convection.long350-3e56ac0814bc/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 2203350160.0, "relative_to_root": 4.803466666666667, "experiment_wall_seconds": 8719.647413509985, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12752618500000001, "loop_wall_seconds": 40.58878954700049}
