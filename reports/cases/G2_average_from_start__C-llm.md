# Verification report: G2_average_from_start (C-llm)

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
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.14% > 1.50% but the demonstrated change 0.46% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 3.3e-04)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.84% > 1.50% but the demonstrated change 0.32% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 3.5e-04)]

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0414
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D1.5x-b31588b6c8c7

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0284
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D1.5x-b31588b6c8c7

```

## EXPERIMENT HISTORY

Run G2_average_from_start-e7384e5a2c24: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and there are no failed checks, so I can't ACCEPT or REJECT. Mesh, time and domain uncertainty are all unmeasured for both Cd and St (no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists).
  - The physics_regime check for R0 is INCONCLUSIVE. The lift amplitude changes by +6.7% across the analysed window, so the oscillation is not yet a sustained limit cycle.
  - The stationary window starts at 27.88 convective units, and stationary_window_start_is_mser_cap is true. Only 5 stationary cycles are available, out of a 59.99 record.
  - The submitted-setup values differ from the stationary-window values. Cd is 1.3196 against 1.3266, a 0.523% bias. St is 0.16144 against 0.163, a 0.953% bias. Cd drift is 0.010388 and the Cd 95% CI is 0.0058205.
  - Averaging and statistics components already use part of the 0.03 tolerance. For Cd they are 0.005234 and 0.01039. For St they are 0.009529 and 0.008104. Any mesh, time or domain term would have to fit in the remaining margin.
  - A transient that may still be developing would confound every later comparison against R0. Mesh, time and domain deltas would mix discretisation effects with unsteady-growth effects. A longer record is the cheapest way to settle this first. It is estimated at 1060 s, against 1126 to 1963 s for the other experiments.
  - Time resolution looks adequate on the recorded values: 613.51 steps per shedding period and max Courant 0.73373. Domain extents are generous: upstream 30 D, downstream 50 D, half height 40 D, blockage 0.0125. The coarse mesh (representative cell size 0.45745 D, wake last cell 1.0209 D) is the next most likely error source after the transient question is closed.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on G2_average_from_start-e7384e5a2c24 — The physics_regime check is INCONCLUSIVE because the lift amplitude changes by +6.7% across the window. The stationary window starts at the MSER cap with only 5 cycles. A developed limit cycle is needed before mesh, time and domain comparisons mean anything, and this is the cheapest primitive.
  - Outcome: executed -> G2_average_from_start.long160-24e243b2227c (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. I cannot ACCEPT, and I have no FAIL to support REJECT.
  - Mesh, time and domain uncertainty are still unmeasured for both mean_drag_coefficient and strouhal_number. No REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists.
  - RUN_LONGER (R1, 160 convective units, 13 stationary cycles) fixed the averaging and statistics components. For Cd, averaging is 0.008643 and statistics 5.59e-05. For St, averaging is 0.01219 and statistics 4.525e-05. All are within the 0.5*0.03 component limit.
  - R1 stationary-window values are Cd 1.3311 and St 0.16344. R0 stationary values were 1.3266 and 0.163, so the earlier window was only slightly off. R1 drift is 5.59e-05 and the Cd CI95 is 1.5832e-05, so the record is stationary.
  - Averaging bias already uses 0.864% (Cd) and 1.219% (St) of the 3% tolerance. The root-sum-square of mesh, time and domain must fit in about 2.1% (Cd) and 1.8% (St). Any large discretisation error would break the budget.
  - The physics_regime check is still INCONCLUSIVE in the package. It cites a +6.7% lift-amplitude change for R0. The package has no explicit re-evaluation for R1. R1 shows rms Cl 0.22857, and stationary_window_start_is_mser_cap is still true.
  - The mesh is the most likely source of an error larger than the tolerance. The representative cell size is 0.45745 D, the wake last cell is 1.0209 D, and the cylinder has 160 cells around it with a first cell of 0.005 D.
  - Time resolution looks adequate: 611.86 steps per shedding period and max Courant 0.73373.
  - Domain extents are large: 30 D upstream, 50 D downstream, 40 D half height, blockage 0.0125. The domain is therefore the least likely dominant error.
  - Budget is available: 1 of 6 experiments and 1.67 of 12 compute units used. The mesh refinement costs about 1963 s, roughly 3.1 root runs, which fits.
  - Requested: REFINE_MESH {'factor': 2.0} on G2_average_from_start.long160-24e243b2227c — R1 gives a long, stationary baseline (13 cycles, drift 5.59e-05), so a difference against it reflects spatial discretisation and not transient or statistical noise. The mesh is the coarsest recorded resolution and the most likely source of an error above 3%. A factor of 2.0 gives the largest signal-to-noise for the mesh error estimate at the same listed cost (1963 s).
  - Outcome: executed -> G2_average_from_start.m2-6c5d2e554b4f (completed)
  - Numeric audit: 6 number(s) not traceable to evidence: 2.1%, 1.8%, 3.1, 1.8%, 2.1%

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. I can't ACCEPT, and there is no FAIL to support REJECT.
  - Mean drag coefficient (Cd): averaging 0.008643, statistics 5.59e-05 and mesh 0.01134 all pass. The time and domain components are unmeasured, so there is no combined uncertainty.
  - Strouhal number (St): averaging 0.01219 and statistics 4.525e-05 pass. The mesh component is 0.03459, which is above 0.5*tolerance (0.015), so it is INCONCLUSIVE. Time and domain are unmeasured.
  - R1 and R2 give Cd 1.3311 and 1.3349 (stationary windows). St is 0.16344 and 0.16486. The demonstrated mesh change in St is 0.86%, which is below the 3% tolerance, so there is no FAIL.
  - Budget: 10.36 of 12.0 root-relative compute units are used, leaving about 1.64. R2 consumed most of it.
  - REFINE_MESH from R1 is not affordable. R2 is the finest run allowed (cumulative refinement limit 2.0), so the St mesh question can't be settled further.
  - REDUCE_TIME_STEP from R0 or R1 is listed at 1697 s, about 2.7 root units. That exceeds the remaining budget.
  - RUN_LONGER (1060 s) would add nothing. R1 has 13 cycles with drift 5.59e-05, and R2 has drift 5.7347e-06.
  - EXPAND_DOMAIN from R1 is listed at 1126 s at the default factor 2.0, which is marginal against the 1.64 units left. The 1.5 minimum factor adds fewer far-field cells and should be the cheapest version. Its cost is not stated, so affordability is uncertain.
  - EXPAND_DOMAIN is the only experiment that might fit the budget. It could expose a domain-truncation error above the tolerance, which would give a deterministic FAIL. Time and domain are not demonstrated to be negligible, so they can't be assumed small.
  - Even a pass would leave the St mesh and time components unresolved, so ACCEPT is unlikely and the final outcome will probably be INCONCLUSIVE.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on G2_average_from_start.long160-24e243b2227c — Only EXPAND_DOMAIN may fit the remaining budget of about 1.64 root units. R1 is the long stationary baseline with 13 cycles and drift 5.59e-05, so any change relative to it reflects boundary effects. It is the one experiment that can still expose a flaw larger than the 3% tolerance. The minimum factor 1.5 is chosen to keep cost lowest, since the listed 1126 s at factor 2.0 is already marginal. The cost at 1.5 is not stated.
  - Outcome: executed -> G2_average_from_start.D1.5x-b31588b6c8c7 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 1.64, 2.7, 1.64, 1.64

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed because components are unmeasured. REJECT is not supported because there is no FAIL.
  - Cd: averaging 0.008643, statistics 5.59e-05 and mesh 0.01134 are measured and pass. Domain is 0.04139, which is above 0.5*tolerance (0.015) and therefore INCONCLUSIVE. Time is unmeasured.
  - St: averaging 0.01219 and statistics 4.525e-05 pass. Mesh is 0.03459, domain is 0.02843 and time is unmeasured. All three are INCONCLUSIVE, so the St mesh and domain terms alone already exceed 0.5*tolerance (0.015).
  - The demonstrated changes are small and below the 3% tolerance, so there is no FAIL. Domain R1 to R3: Cd 0.46%, St 0.32%. Mesh R1 to R2: Cd 0.284% (root-to-finest), St 0.86%. The large uncertainty estimates come from the conservative Richardson assumptions (p=1 for domain, p=2 for mesh, Fs=3), not from measured large changes.
  - Budget: compute_used_relative_to_root is 11.95 of 12.0, leaving 0.05 root units. R0 costs 636.22 s, so 0.05 units is far below any menu entry. The cheapest listed option is RUN_LONGER from R1 at 1060 s, about 1.67 root units. REDUCE_TIME_STEP from R1 is 1697 s and REFINE_MESH from R1 is 1963 s. None is affordable.
  - REFINE_MESH from R2 is not allowed (cumulative refinement limit). EXPAND_DOMAIN from R2 is not allowed (cell count limit). So no useful experiment fits, and the system should report INCONCLUSIVE. Time-step sensitivity is unmeasured: R0 has 613.51 steps per shedding period and max Courant 0.73373, but that is only a guideline, not a measured temporal error.
  - The physics_regime check is still INCONCLUSIVE. It cites a +6.7% lift-amplitude change for R0, and the package has no explicit re-evaluation for R1, R2 or R3. This is unresolved evidence. Every recorded stationary window also starts at the MSER cap.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 3 number(s) not traceable to evidence: 0.05, 0.05, 1.67

Run G2_average_from_start.long160-24e243b2227c: RUN_LONGER from G2_average_from_start-e7384e5a2c24 (time.end_time: 60→160).
  - Observation: mean_drag_coefficient 1.3266 → 1.3311 (+0.34%).
  - Observation: strouhal_number 0.163 → 0.16344 (+0.27%).

Run G2_average_from_start.m2-6c5d2e554b4f: REFINE_MESH from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16344 → 0.16486 (+0.87%).

Run G2_average_from_start.D1.5x-b31588b6c8c7: EXPAND_DOMAIN from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3251 (-0.46%).
  - Observation: strouhal_number 0.16344 → 0.16292 (-0.31%).

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
- `G2_average_from_start.D1.5x-b31588b6c8c7` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-19T16:42:03+00:00 wall=984.8 s; record: results/runs/G2_average_from_start.D1.5x-b31588b6c8c7/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 2192238080.0, "relative_to_root": 11.948103771528231, "experiment_wall_seconds": 13643.260280337012, "n_experiments": 3, "planner_calls": 4, "planner_cost_usd": 0.30922873500000003, "loop_wall_seconds": 32400.724822612996}
