# Verification report: G2_average_from_start (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3196
- strouhal_number: 0.16144

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
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +6.7% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.864% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.219% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.59e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 4.53e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.13% <= 1.50% (root-to-finest change 0.284%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 5.6e-05)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 3.46% > 1.50% but the demonstrated change 0.86% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.7e-05)]
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
├── Averaging window (reported vs stationary value): PASS U=0.00864
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=5.59e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): PASS U=0.0113
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m2-6c5d2e554b4f
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
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=4.53e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0346
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m2-6c5d2e554b4f
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── G2_average_from_start-e7384e5a2c24

```

## EXPERIMENT HISTORY

Run G2_average_from_start-e7384e5a2c24: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - For both mean_drag_coefficient and strouhal_number, the mesh, time and domain components are unmeasured. No REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists, so no combined uncertainty can be formed.
  - The physics_regime check on R0 is INCONCLUSIVE. The lift amplitude changes by +6.7% across the analysed window, so the record is not yet shown to be a sustained limit cycle.
  - In R0 the stationary window start (27.88 convective units) is the MSER cap, and the record is 59.99 units long with only 5 stationary cycles.
  - R0 also shows a mean-drag drift of 0.010388 (relative) and a statistics uncertainty of 0.01039 for drag. That is about 69% of the 1.5% per-component limit (0.5*tol).
  - R0 reports Strouhal 0.16144 against 0.163 in the stationary window, a bias of 0.953%. Its frequency resolution is 0.016669, which is coarse.
  - Any sensitivity comparison (mesh, time or domain) against a parent that may still be in transient would mix a discretisation effect with transient or statistical differences. Settling the baseline first makes the later comparisons interpretable.
  - RUN_LONGER on R0 is the cheapest experiment (1060 s estimated). It directly tests the unresolved physics_regime check and reduces the statistics and averaging uncertainties.
  - Budget is ample (0 of 6 experiments used, 0 of 12.0 relative compute used). The mesh, time and domain experiments can follow, with REFINE_MESH likely first given R0's coarse wake (wake_last_cell_D 1.0209, representative cell size 0.45745 D).
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on G2_average_from_start-e7384e5a2c24 — The physics_regime check is INCONCLUSIVE (lift amplitude +6.7% across the window). The stationary window starts at the MSER cap and holds only 5 cycles. A longer record settles the baseline, so that later mesh, time and domain comparisons are not confounded by transient or statistical noise. It is the cheapest option.
  - Outcome: executed -> G2_average_from_start.long160-24e243b2227c (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 69%, 16

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - The RUN_LONGER experiment R1 (160 convective units, 13 stationary cycles) settled the averaging and statistics components. Drag statistics uncertainty is 5.59e-05 and Strouhal statistics uncertainty is 4.525e-05. R1 stationary-window values are Cd 1.3311 and St 0.16344. The R1 drag drift is 5.59e-05 and its CI95 is 1.5832e-05.
  - The averaging bias of the submitted setup is measured at 0.008643 for drag and 0.01219 for Strouhal. These are added linearly to the budget and use part of the 0.03 tolerance. The mesh, time and domain components are still unmeasured for both quantities.
  - R1 stationary-window values differ little from R0's (Cd 1.3266 and St 0.163), which supports a settled baseline. R1's window start is still flagged as the MSER cap, but its statistics are tight. The physics_regime INCONCLUSIVE flag was raised on R0, where the lift amplitude changed by +6.7%. R1 supplies the longer record that flag asked for.
  - The mesh looks like the most likely discretisation flaw. R0 and R1 share a mesh with representative cell size 0.45745 D, wake_last_cell_D 1.0209 and wake_cells_streamwise 111. Wake resolution is the likeliest driver of Strouhal and drag error. The max non-orthogonality of 43.313 deg and the 1-corrector-outer PIMPLE setup add some doubt.
  - The time step is 0.01 convective units with max Courant 0.73373 and 611.86 steps per shedding period. Backward time with second-order upwind convection is nominally adequate, so the time error is probably smaller than the mesh error. The time check is still unmeasured.
  - The domain has blockage_ratio 0.0125, 30 D upstream, 50 D downstream, 40 D half height and symmetry sides. This is generous, but pressure zeroGradient at the inlet and the symmetry sides are untested.
  - REFINE_MESH from R1 continues from the longest, best-averaged baseline. This means the mesh comparison is not confounded by averaging noise. It costs 1963 s, which the budget can cover: 1 of 6 experiments used and 1.67 of 12.0 relative compute used.
  - Requested: REFINE_MESH {'factor': 2.0} on G2_average_from_start.long160-24e243b2227c — Mesh error is unmeasured for both quantities, and the mesh is coarse in the wake (wake_last_cell_D 1.0209, representative cell size 0.45745 D). It is the most likely flaw to move St or Cd by more than the tolerance. R1 is the best-averaged baseline (13 cycles, drag CI95 1.5832e-05), so the comparison is not confounded by statistical noise. Factor 2.0 gives a clear refinement signal. The default 1.4142 would give a weaker one.
  - Outcome: executed -> G2_average_from_start.m2-6c5d2e554b4f (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - Drag: averaging (0.008643), statistics (5.59e-05) and mesh (0.01134) all PASS. The time and domain components are unmeasured, so no combined uncertainty exists.
  - Strouhal: averaging (0.01219) and statistics (4.525e-05) PASS. The mesh component is INCONCLUSIVE at 0.03459, above the 0.015 per-component limit. The R1 to R2 stationary St change is small (0.16344 to 0.16486), but the two-level Richardson estimate with assumed p=2 and Fs=3 is conservative. Time and domain are also unmeasured.
  - Resolving the Strouhal mesh uncertainty would need a third mesh level. R2 already has cumulative refinement 2.83 and further refinement is not allowed.
  - Closing the time and domain gaps would need REDUCE_TIME_STEP and EXPAND_DOMAIN runs on R1. Both would be needed for ACCEPT, plus a third mesh level for St.
  - Budget: compute used is 10.36 of 12.0, leaving 1.64 relative to the root. The cheapest menu entries from R1 are RUN_LONGER (1060 s) and EXPAND_DOMAIN (1126 s). The root R0 cost 636.22 s, so 1.64 root-equivalents is about 1043 s. By my reading, neither fits, and REDUCE_TIME_STEP (1697 s) and REFINE_MESH (1963 s) clearly do not. That reading assumes the compute budget scales with wall seconds, which the package does not state explicitly.
  - Even if one more run fit, the remaining uncertainty components could not all be closed within the budget. No single affordable experiment can turn the verdict into ACCEPT, so the system should report INCONCLUSIVE.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 3 number(s) not traceable to evidence: 1.64, 1.64, 1043

Run G2_average_from_start.long160-24e243b2227c: RUN_LONGER from G2_average_from_start-e7384e5a2c24 (time.end_time: 60→160).
  - Observation: mean_drag_coefficient 1.3266 → 1.3311 (+0.34%).
  - Observation: strouhal_number 0.163 → 0.16344 (+0.27%).

Run G2_average_from_start.m2-6c5d2e554b4f: REFINE_MESH from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16344 → 0.16486 (+0.87%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G2_average_from_start-e7384e5a2c24` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=636.2 s; record: results/runs/G2_average_from_start-e7384e5a2c24/run.json
- `G2_average_from_start.long160-24e243b2227c` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T09:08:43+00:00 wall=1041 s; record: results/runs/G2_average_from_start.long160-24e243b2227c/run.json
- `G2_average_from_start.m2-6c5d2e554b4f` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-19T10:44:53+00:00 wall=1.162e+04 s; record: results/runs/G2_average_from_start.m2-6c5d2e554b4f/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1901342080.0, "relative_to_root": 10.362666666666666, "experiment_wall_seconds": 12658.460272847, "n_experiments": 2, "planner_calls": 3, "planner_cost_usd": 0.216673395, "loop_wall_seconds": 68.28233009399992}
