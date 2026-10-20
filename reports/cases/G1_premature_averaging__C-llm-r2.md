# Verification report: G1_premature_averaging (C-llm-r2)

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
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is also not justified, because no measured FAIL invalidates R0.
  - R0 passes the basic sanity checks: solver_completion, mesh_quality, mass_conservation (8.333e-11), linear_solver_convergence, courant_number (max 0.7337), reynolds_consistency, force_reference_consistency and convection_scheme_order.
  - physics_regime is INCONCLUSIVE: the lift amplitude changes by +25.8% across the analysed window, so R0 is not yet a sustained limit cycle. The record is only 39.99 convective units.
  - The stationary window start (15.276) is the MSER cap (stationary_window_start_is_mser_cap = true). Only 3 stationary cycles are available, below the minimum of 4.
  - Drag statistical uncertainty is too large for the 3% tolerance: CI95 is 0.044509 and the drift is 0.040105 relative, both above the 3% tolerance. The Strouhal statistical/stationarity uncertainty is 3.58%.
  - The submitted-setup and stationary-window values differ. Mean drag is 1.2961 vs 1.3039, and Strouhal is 0.16129 vs 0.16058 (FFT 0.16169). The Strouhal frequency resolution of 0.033333 is coarse relative to a 3% tolerance.
  - The averaging, statistics, mesh, time and domain components are all unmeasured. Every other experiment would be compared against a non-stationary, under-sampled baseline, so its effect could not be separated from transient and sampling noise. Establishing the limit cycle first is the most informative step.
  - RUN_LONGER on R0 costs an estimated 979 s, the cheapest of the four options except EXPAND_DOMAIN (1040 s). It fits well within the budget (0 of 6 experiments used, 0 of 12 relative compute used).
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on G1_premature_averaging-17c0143468d7 — R0 is not a demonstrated stationary limit cycle. The lift amplitude changes by +25.8% across the window, the window start is the MSER cap, and only 3 cycles are available (below 4). The averaging and statistics components are INCONCLUSIVE for both quantities. A longer record is required before any mesh, time or domain comparison is meaningful, and it is among the cheapest experiments.
  - Outcome: executed -> G1_premature_averaging.long140-34c6cca905d9 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and there are no failed checks. ACCEPT is not allowed, and REJECT is not justified because no measured FAIL invalidates R0.
  - The R1 RUN_LONGER experiment resolved the averaging and statistics components. R1 has 12 stationary cycles, a drag CI95 of 3.4541e-05, drift of 0.0001195 and a Strouhal FFT value of 0.16343. Statistics PASS for both quantities.
  - R0's submitted-setup values are biased relative to the R1 stationary window. Mean drag is biased by 2.631% (R0 1.2961 vs R1 1.3311). Strouhal is biased by 1.312% (R0 0.16129 vs R1 0.16343). These biases use most of the 3% tolerance, and the verifier adds them linearly. Mesh, time and domain errors must therefore be very small.
  - The mesh, time and domain components are all unmeasured for both quantities: mesh_sensitivity, time_sensitivity and domain_sensitivity are INCONCLUSIVE. No ACCEPT is possible until all three are measured.
  - The physics_regime check is still INCONCLUSIVE. It carries the +25.8% lift-amplitude change measured on R0's 39.99-unit record. R1 has not been re-evaluated on this check.
  - Mesh resolution is the most likely source of an error larger than the tolerance. The 30580 cells give a representative cell size of 0.45745 D with 160 cells around the cylinder, the wake cells stretch to 1.0209 D at the last cell, and the wall-first cell is 0.005 D. The scheme is only nominally second order (linearUpwind), and a coarse wake can shift both the drag and the shedding frequency.
  - Time-step evidence is weaker as a concern: dt is 0.01 convective units, max Courant is 0.7337 and there are about 612 steps per shedding period on R1. The domain is large (30D upstream, 50D downstream, 40D half height, blockage 0.0125), so these are less likely to cause a shift above 3%.
  - Budget: 1 of 6 experiments is used and 2.5 of 12 compute units (relative to root) are used. The menu costs relative to R0's 391.64 s are about 4.63 for REFINE_MESH, 4.0 for REDUCE_TIME_STEP and 2.66 for EXPAND_DOMAIN. This is derived from the menu costs and is not a recorded quantity. The three together would exceed the remaining budget, so the most informative experiment must go first.
  - The parent is R1 because it is the only stationary, well-sampled baseline (12 cycles). Refining from R1 compares like with like, and the cost is the same as from R0 (1812 s).
  - Requested: REFINE_MESH {'factor': 1.4142} on G1_premature_averaging.long140-34c6cca905d9 — Mesh error is the most likely unmeasured source of a shift larger than the tolerance (cell size 0.45745 D, wake last cell 1.0209 D, 160 cells around the cylinder). The R0-to-R1 averaging bias already uses 2.631% of the 3% drag budget and 1.312% of the Strouhal budget. R1 is the stationary 12-cycle baseline. Remaining budget cannot cover all three sensitivity experiments, so the most informative one runs first.
  - Outcome: executed -> G1_premature_averaging.m1.41-5d1d1becf814 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 4.63, 2.66

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not justified because no measured FAIL invalidates R0.
  - R1 (RUN_LONGER) resolved averaging and statistics. R1 has 12 stationary cycles, drag CI95 3.4541e-05, drag drift 0.0001195 and Strouhal FFT 0.16343. Statistics PASS for both quantities. R0's submitted values are biased by 2.631% (drag) and 1.312% (Strouhal) against the R1 stationary window.
  - R2 (REFINE_MESH from R1) changes the stationary-window values little. Drag goes 1.3311 -> 1.3349 (demonstrated change 0.28%). Strouhal goes 0.16343 -> 0.16443 (0.61%). Both are below tolerance, so the verifier records mesh as INCONCLUSIVE (drag 1.698%, Strouhal 3.63%), not as a FAIL.
  - Time and domain components are still unmeasured for both quantities: no REDUCE_TIME_STEP or EXPAND_DOMAIN run exists. Absence of evidence is not a pass.
  - physics_regime is still INCONCLUSIVE. It carries R0's +25.8% lift-amplitude change on its 39.99-unit record. R1 (record 139.99, 12 cycles) is the sustained-limit-cycle evidence, but the check was not re-evaluated on it.
  - Budget used is 7.13 of 12 relative compute units, and 2 of 6 experiments. Menu costs from R1 are 1812 s (REFINE_MESH), 1567 s (REDUCE_TIME_STEP), 1040 s (EXPAND_DOMAIN) and 979 s (RUN_LONGER). Relative to R0's 391.64 s, these are about 4.63, 4.0, 2.66 and 2.5 units. These ratios are derived, not recorded. Only one more experiment fits in the remaining ~4.87 units. Experiments from R2 (2265-4164 s) do not fit.
  - EXPAND_DOMAIN from R1 is chosen because it fits the budget and tests the largest untested modelling assumption. The lateral boundaries are symmetryPlane at 40 D half height (blockage_ratio 0.0125), inlet is 30 D, outlet is 50 D, and inlet pressure is zeroGradient. A shift above 3% would let the verifier record a FAIL. REDUCE_TIME_STEP is less likely to expose a large flaw: Courant is 0.73, backward scheme, about 612 steps per shedding period on R1.
  - Caveat: after this run, the remaining budget (about 2.2 units) cannot cover REDUCE_TIME_STEP. The mesh and Strouhal mesh uncertainty (3.63% > 1.5%) is also unresolved. The final outcome is therefore likely INCONCLUSIVE unless the domain run exposes a FAIL.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on G1_premature_averaging.long140-34c6cca905d9 — It is the only untested modelling assumption that fits the remaining budget and has a plausible effect above the tolerance. Lateral symmetry planes at 40 D (blockage 0.0125), 30 D inlet, 50 D outlet and zeroGradient inlet pressure could shift drag and Strouhal number. R1 is the stationary 12-cycle baseline, and the cost from R1 is 1040 s, the cheapest affordable option.
  - Outcome: executed -> G1_premature_averaging.D2x-0c05c8ab28fb (completed)
  - Numeric audit: 5 number(s) not traceable to evidence: 4.63, 2.66, 2.5, 4.87, 2.2

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not justified, because no measured FAIL invalidates R0.
  - Averaging and statistics PASS for both quantities, using R1 (12 cycles, drag CI95 3.4541e-05). R0's submitted values are biased against R1 by 2.631% (drag) and 1.312% (Strouhal). The verifier adds these linearly to the budget.
  - Mesh is INCONCLUSIVE (R1->R2). Drag changes 1.3311 -> 1.3349 (0.28%) and Strouhal 0.16343 -> 0.16443 (0.61%). The extrapolated mesh uncertainty is 1.698% for drag and 3.63% for Strouhal. Both are above 0.5*tolerance (1.5%), and the Strouhal value is above the full 3% tolerance. These come from a two-level Richardson estimate with an assumed order p=2 and Fs=3.
  - Domain is INCONCLUSIVE (R1->R3). Drag changes 1.3311 -> 1.3224 (0.66%) and Strouhal 0.16343 -> 0.16269 (0.45%). The extrapolated domain uncertainty is 3.97% for drag and 2.71% for Strouhal, with an assumed order p=1. The demonstrated changes are within tolerance, so there is no FAIL. R3 has checkMesh_ok=false and a different far-field mesh (cell size 0.79405 D, wake last cell 1.9729 D), so its comparison with R1 is partly confounded.
  - Time is unmeasured for both quantities. No REDUCE_TIME_STEP run exists. R2 also changed dt (0.0086734), so its mesh and time effects are confounded. Absence of evidence is not a pass.
  - physics_regime is still INCONCLUSIVE. It carries R0's +25.8% lift-amplitude change on a 39.99-unit record. R1 (record 139.99, 12 cycles) has not been re-evaluated on this check.
  - Budget: 3 of 6 experiments used and 9.78 of 12 compute units used, so about 2.22 units remain. At R0's 391.64 s that is about 869 s. This is derived from the recorded budget and is not itself recorded. The cheapest menu entry is 979 s (RUN_LONGER from R1) and every other entry costs more. No experiment fits, so next_experiment is null and the system will report INCONCLUSIVE.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 2 number(s) not traceable to evidence: 2.22, 869

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
- Experiment cost: {"experiment_cell_steps": 1196639984.0, "relative_to_root": 9.782864486592544, "experiment_wall_seconds": 4537.419368196994, "n_experiments": 3, "planner_calls": 4, "planner_cost_usd": 0.32542164, "loop_wall_seconds": 108.32358546599971}
