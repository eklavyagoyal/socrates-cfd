# Verification report: F1_upwind_convection (C-llm)

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
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed, and there is no measured FAIL to justify REJECT.
  - Mesh, time and domain uncertainty components are unmeasured for both mean_drag_coefficient and strouhal_number. Absence of evidence is not a pass.
  - R0 uses 'Gauss upwind', which is formally first order. The convection_scheme_order check is INCONCLUSIVE and says diffusion must be shown negligible by mesh refinement.
  - The mesh is coarse for a first-order scheme: representative_cell_size_D 0.45745, 30580 cells, wall_first_cell_D 0.005, wake_last_cell_D 1.0209. Numerical diffusion could shift Strouhal and drag by more than the 0.03 tolerance.
  - R0 statistics are acceptable: drag ci95 0.0034414, Strouhal 0.12581 (window) vs 0.12605 (FFT). Statistical uncertainty is 0.01069 (drag) and 0.01474 (Strouhal), and the latter is already near the 1.50% limit.
  - The Strouhal frequency resolution is 0.013333. This is large compared with the 3% tolerance on a value of about 0.126, so the refinement comparison must be read with that noise in mind.
  - physics_regime is INCONCLUSIVE: lift amplitude changes +11.3% across the analysed window. stationary_window_start_is_mser_cap is true (67.226). The record may not be a sustained limit cycle, so RUN_LONGER is a likely follow-up.
  - Mesh refinement is chosen first because the first-order scheme on a coarse mesh is the most likely flaw to move both quantities by more than tolerance. It is also the only experiment that can resolve the convection_scheme_order check.
  - Budget is ample: 0 of 6 experiments used and 0.0 of 12.0 relative compute used. The REFINE_MESH estimate from R0 is 1691 s, against a root cost of 1373.7 s.
  - Requested: REFINE_MESH {'factor': 2.0} on F1_upwind_convection-e460c39ac86c — R0 uses first-order Gauss upwind on a coarse mesh (representative_cell_size_D 0.45745), and the mesh error is entirely unmeasured. This is the flaw most likely to change drag or Strouhal number by more than 3%. The largest allowed factor gives the clearest signal for a first-order scheme, and the budget allows it (0 of 6 experiments and 0.0 of 12.0 relative compute used).
  - Outcome: executed -> F1_upwind_convection.m2-a5b11786bf96 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with failed_checks empty. ACCEPT is not allowed. REJECT is also not allowed, because no deterministic FAIL is recorded.
  - R0 and R1 differ by more than the 0.03 tolerance in the recorded stationary-window Strouhal number: R0 0.12581, R1 0.1426. Drag differs by less: R0 1.2674, R1 1.2968. I cannot call this a FAIL myself. The verifier withheld the mesh verdict because R0 is 'not statistically reliable' (10 cycles, uncertainty 0.010692 for drag, 0.014742 for Strouhal).
  - R0 has a physics_regime INCONCLUSIVE: lift amplitude changes +11.3% across the window, and stationary_window_start_is_mser_cap is true (67.226). R0 rms lift is 0.12493 against R1's 0.19709, and cl_amplitude_mean is 0.17669 against 0.27874. This is consistent with R0 not yet being in a saturated limit cycle, or with strong numerical damping from first-order upwind on the coarse mesh.
  - R0 Strouhal frequency resolution is 0.013333, and R1's is 0.025002. Both are large next to a 3% tolerance on values of about 0.126 and 0.143. Part of the R0-R1 gap may be spectral and record-length noise, so a longer record is needed to resolve it.
  - R1 is also short: 80.0 convective times and 5 stationary cycles. The R1 family check will still need a longer run. RUN_LONGER on R1 costs 5959 s, so I am doing R0 first because it is the member the verifier flagged.
  - The time and domain components are still unmeasured. Budget remains: 1 of 6 experiments used and 3.47 of 12.0 relative compute used. REFINE_MESH from R1 is not allowed, and EXPAND_DOMAIN from R1 is not allowed.
  - Requested: RUN_LONGER {'additional_convective_times': 200.0} on F1_upwind_convection-e460c39ac86c — The verifier blocks mesh_sensitivity because R0 is not statistically reliable. R0 also has an INCONCLUSIVE physics_regime (+11.3% lift-amplitude change, MSER cap hit). R0 is the cheapest run to extend (916 s estimated at the default length, against 5959 s for R1). It tests the most likely benign explanation for the large R0-R1 Strouhal difference, which is a transient and a coarse frequency resolution (0.013333). It also tests whether the difference is real numerical diffusion.
  - Outcome: executed -> F1_upwind_convection.long350-3e56ac0814bc (completed)

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
- Experiment cost: {"experiment_cell_steps": 2203350160.0, "relative_to_root": 4.803466666666667, "experiment_wall_seconds": 8719.647413509985, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12549808499999998, "loop_wall_seconds": 55639.212479744}
