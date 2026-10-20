# Verification report: G1_premature_averaging (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2961
- strouhal_number: 0.16129

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
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +25.8% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 2.631% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.312% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.01e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.70% > 1.50% but the demonstrated change 0.28% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 3.63% > 1.50% but the demonstrated change 0.61% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.0e-04)]
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.97% > 1.50% but the demonstrated change 0.66% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.1e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.71% > 1.50% but the demonstrated change 0.45% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 9.6e-04)]

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
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Temporal statistics (stationarity, cycles): PASS U=0.00012
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.017
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.m1.41-5d1d1becf814
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0397
    └── G1_premature_averaging.long140-34c6cca905d9
    └── G1_premature_averaging.D2x-0c05c8ab28fb

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
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Temporal statistics (stationarity, cycles): PASS U=0.000101
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0363
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.m1.41-5d1d1becf814
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0271
    └── G1_premature_averaging.long140-34c6cca905d9
    └── G1_premature_averaging.D2x-0c05c8ab28fb

```

## EXPERIMENT HISTORY

Run G1_premature_averaging-17c0143468d7: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified because no FAIL has been measured.
  - R0 physics_regime is INCONCLUSIVE. The lift amplitude changes by +25.8% across the analysed window, so this is not yet a sustained limit cycle (still growing or decaying).
  - The stationary window starts at 15.276 convective units, which is flagged as the MSER cap (stationary_window_start_is_mser_cap=true). It holds only 3 cycles (<4), so the transient may not have ended.
  - R0 drag drift is 0.040105 relative and the 95% CI is 0.044509. Both exceed the 0.03 tolerance. The Strouhal statistical uncertainty is 3.58%, also above 0.03. The averaging and statistics components are unusable for both quantities.
  - The reported Strouhal number is 0.16129 against a window value of 0.16058 (FFT 0.16169). The frequency resolution is 0.033333, which is coarse relative to the 3% tolerance. A longer record would improve it.
  - Mesh, time and domain sensitivity are unmeasured. Their results would be biased if run from R0, because R0 is not yet statistically stationary. Time and domain comparisons would be confounded by the unsettled transient.
  - RUN_LONGER on R0 costs an estimated 979 s, roughly 2.5x the root cost of 391.64 s. It is the cheapest experiment on the menu except EXPAND_DOMAIN, and it resolves the stationarity question that blocks every other component.
  - Other checks pass: Courant number 0.7337, mass imbalance 8.333e-11, Reynolds number and force reference consistent, and the convection scheme is nominally second order. Nothing in the setup is flagged as invalid at this stage.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on G1_premature_averaging-17c0143468d7 — R0 is not yet a sustained limit cycle (lift amplitude +25.8% across the window), and its stationary window has only 3 cycles at the MSER cap. Averaging and statistics are therefore INCONCLUSIVE for both quantities. Extending R0 tests whether the transient had ended, and gives enough stationary cycles to measure averaging bias and statistical uncertainty. It also gives a trustworthy baseline for later mesh, time and domain comparisons.
  - Outcome: executed -> G1_premature_averaging.long140-34c6cca905d9 (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 95%, 2.5, 0.015

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and REJECT is not justified because no FAIL has been measured.
  - R1 (RUN_LONGER from R0, 140 convective units) resolved the stationarity problem. It has 12 stationary cycles. Drag drift is 0.0001195 and the CI95 is 3.4541e-05. The Strouhal number is 0.16343 from both the window and the FFT, with a frequency resolution of 0.0076923.
  - The averaging bias of the R0-reported values is measured. Drag is biased by 2.631% (R0 1.2961 vs R1 stationary window 1.3311). Strouhal is biased by 1.312% (0.16129 vs 0.16343). Averaging and statistics both PASS.
  - The error-budget rule adds the averaging bias linearly. For drag, 0.02631 of the 0.03 tolerance is already used. Only about 0.0037 is left for the root-sum-square of the mesh, time and domain components. The remaining experiments may therefore not be able to produce an ACCEPT for drag. They can still produce a measured FAIL, or show the drag error is small.
  - Mesh, time and domain sensitivity are all unmeasured (INCONCLUSIVE). R0/R1 use a coarse mesh: 30580 cells, representative size 0.45745 D, 160 cells around the cylinder, and wake_last_cell_D 1.0209 over 111 streamwise wake cells. Spatial error is the most likely component to change drag or Strouhal number by more than 3%.
  - The time step is 0.01 D/U, with max Courant 0.73373 and about 612 steps per shedding period. The backward scheme is second order, so time error is less likely to be dominant. The domain is 30 D upstream, 50 D downstream and 40 D half-height, with blockage 0.0125. That is generous, and the domain experiment is cheaper (1040 s) if budget allows later.
  - Budget: 1 of 6 experiments used and 2.5x of 12x compute used, which leaves 9.5x, about 3720 s. REFINE_MESH from R1 costs 1812 s (about 4.6x), so it is affordable. Running mesh, time and domain together (4419 s) would exceed the remaining budget. The most informative experiment must therefore go first.
  - R1 is the parent because it is the stationary baseline. R0's window is short and biased, so comparing against it would confound the mesh effect with transient bias.
  - The R0 physics_regime INCONCLUSIVE (+25.8% lift amplitude drift) applies to the short R0 record only. R1 shows a drift of 1.2e-4 over 12 cycles and no longer flags non-stationarity.
  - Requested: REFINE_MESH {'factor': 1.4142} on G1_premature_averaging.long140-34c6cca905d9 — Mesh error is unmeasured and is the most likely flaw to move drag or Strouhal number by more than the 3% tolerance. The mesh is coarse, especially in the wake. R1 is the stationary baseline with 12 cycles and negligible drift, so a mesh comparison against it is not confounded by transient bias. This is the most informative use of the remaining budget, which cannot cover all three of mesh, time and domain.
  - Outcome: executed -> G1_premature_averaging.m1.41-5d1d1becf814 (completed)
  - Numeric audit: 5 number(s) not traceable to evidence: 0.0037, 9.5, 3720, 4.6, 4419

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE and failed_checks is empty, so ACCEPT is not allowed. REJECT is not justified because no FAIL has been measured.
  - R1 is a stationary baseline: 12 cycles, drag drift 0.0001195, drag CI95 3.4541e-05, Strouhal 0.16343 (window and FFT agree). Averaging and statistics PASS for both quantities.
  - R2 (REFINE_MESH from R1, 61366 cells vs 30580) gives drag 1.3349 vs 1.3311 and Strouhal 0.16443 vs 0.16343. The demonstrated changes are 0.28% and 0.61%, both below the 0.03 tolerance, so there is no FAIL. The Richardson estimate (assumed p=2) is still 1.70% for drag and 3.63% for Strouhal, above the 1.5% component limit. The mesh component stays INCONCLUSIVE.
  - R2 changed the time step (0.0086734 vs 0.01) together with the mesh, so the mesh estimate is partly confounded with temporal error. R2 has only 6 cycles.
  - The drag averaging bias of 0.02631 is added linearly and leaves only about 0.0037 of the 0.03 tolerance for the other components. An ACCEPT for drag is unlikely. The Strouhal mesh estimate of 3.63% also exceeds the tolerance as extrapolated. More evidence can only add a measured FAIL or shrink the uncertainties.
  - Budget: compute used is 7.13 of 12.0, so 4.87 root-cost units remain. Only EXPAND_DOMAIN on R1 (1040 s) or REDUCE_TIME_STEP on R1 (1567 s) is affordable, not both. Another REFINE_MESH from R2 (4164 s) or RUN_LONGER on R2 (2265 s) is not affordable.
  - Domain error is completely unmeasured. The request says to treat the stream as unbounded, but the domain has blockage ratio 0.0125, symmetryPlane lateral boundaries, a zeroGradient inlet pressure and a fixedValue outlet pressure. Truncation or blockage effects are a plausible cause of a shift larger than the tolerance. This is cheaper than the time-step test, and the time scheme is second-order backward with about 612 steps per period.
  - R1 is the parent because it is the stationary baseline and is affordable. R2 as parent costs 2407 s, which exceeds the remaining budget.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on G1_premature_averaging.long140-34c6cca905d9 — Domain truncation and blockage error is unmeasured and could move drag or Strouhal number by more than 3% in a problem that is meant to be unbounded. R1 is the stationary 12-cycle baseline, so the comparison is not confounded by transient bias. This is the cheapest affordable primitive (1040 s). After it, the 4.87 remaining cost units cannot cover another experiment on R1 (REDUCE_TIME_STEP at 1567 s) and the final budget decision will follow from this result.
  - Outcome: executed -> G1_premature_averaging.D2x-0c05c8ab28fb (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 0.0037, 4.87, 4.87

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not justified because no FAIL has been measured.
  - R1 is a stationary baseline: 12 cycles, drag drift 0.0001195, drag CI95 3.4541e-05, Strouhal 0.16343 (window and FFT agree). Averaging and statistics PASS for both quantities.
  - The averaging bias of the R0-reported values is measured: 2.631% for drag (1.2961 vs 1.3311) and 1.312% for Strouhal (0.16129 vs 0.16343). It is added linearly, so drag has about 0.0037 of the 0.03 tolerance left for mesh, time and domain combined.
  - Mesh (R1 to R2): drag 1.3311 to 1.3349 (0.28%), Strouhal 0.16343 to 0.16443 (0.61%). There is no FAIL, but the two-level Richardson estimate (assumed p=2) is 1.70% for drag and 3.63% for Strouhal, above the 1.5% component limit, so the mesh component stays INCONCLUSIVE. R2 also changed the time step (0.0086734 vs 0.01), so the mesh and time effects are confounded.
  - Domain (R1 to R3): drag 1.3311 to 1.3224 (0.66%), Strouhal 0.16343 to 0.1627 (0.45%). There is no FAIL, but the Richardson estimate (assumed p=1) is 3.97% for drag and 2.71% for Strouhal, so the domain component stays INCONCLUSIVE. R3 has checkMesh_ok=false and a much coarser wake (wake_last_cell_D 1.9729 vs 1.0209, representative size 0.79405 D vs 0.45745 D), so the domain comparison is also confounded with a mesh change.
  - Time-step error is entirely unmeasured. No REDUCE_TIME_STEP run exists, so the time component is INCONCLUSIVE for both quantities.
  - The recorded physics_regime check is still INCONCLUSIVE. It reports the +25.8% lift-amplitude change for the short R0 record. R1 has no separate physics_regime entry, so a sustained limit cycle is not confirmed by the verifier.
  - Budget: 9.78 of 12.0 root-cost units are used, so 2.22 units remain, which is about 869 s at the root cost of 391.64 s. The cheapest menu entries from any parent are RUN_LONGER on R1 (979 s) and EXPAND_DOMAIN on R1 (1040 s). REDUCE_TIME_STEP on R1 costs 1567 s and REFINE_MESH on R1 costs 1812 s. None of them is affordable, so no useful experiment can be run.
  - The system will report INCONCLUSIVE. This is not a pass: the mesh, time and domain components are unquantified or above their limits.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 5 number(s) not traceable to evidence: 0.0037, 2.22, 869, 2.22, 869

Run G1_premature_averaging.long140-34c6cca905d9: RUN_LONGER from G1_premature_averaging-17c0143468d7 (time.end_time: 40→140).
  - Observation: mean_drag_coefficient 1.3039 → 1.3311 (+2.09%).
  - Observation: strouhal_number 0.16058 → 0.16343 (+1.78%).

Run G1_premature_averaging.m1.41-5d1d1becf814: REFINE_MESH from G1_premature_averaging.long140-34c6cca905d9 (averaging.start_time: 10→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 140→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run G1_premature_averaging.D2x-0c05c8ab28fb: EXPAND_DOMAIN from G1_premature_averaging.long140-34c6cca905d9 (averaging.start_time: 10→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 140→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3224 (-0.66%).
  - Observation: strouhal_number 0.16343 → 0.1627 (-0.45%).

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
- `G1_premature_averaging.m1.41-5d1d1becf814` status=completed parent=G1_premature_averaging.long140-34c6cca905d9 created=2026-10-19T18:15:52+00:00 wall=2355 s; record: results/runs/G1_premature_averaging.m1.41-5d1d1becf814/run.json
- `G1_premature_averaging.D2x-0c05c8ab28fb` status=completed parent=G1_premature_averaging.long140-34c6cca905d9 created=2026-10-20T03:42:26+00:00 wall=1243 s; record: results/runs/G1_premature_averaging.D2x-0c05c8ab28fb/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1196639984.0, "relative_to_root": 9.782864486592544, "experiment_wall_seconds": 4537.419368196994, "n_experiments": 3, "planner_calls": 4, "planner_cost_usd": 0.329054505, "loop_wall_seconds": 4675.0673268069995}
