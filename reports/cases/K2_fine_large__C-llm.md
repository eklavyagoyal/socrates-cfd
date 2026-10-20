# Verification report: K2_fine_large (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3278
- strouhal_number: 0.16382

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.65 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.91e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.01e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.34% <= 1.50% (root-to-finest change 0.088%) [oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 0.99% <= 1.50% (root-to-finest change 0.443%) [three-level Celik procedure, observed order p=1.74, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.79% <= 1.50% (root-to-finest change 0.198%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.068%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.38% > 1.50% but the demonstrated change 0.71% <= tau; more refinement would be needed [three-level, observed order 2.79 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.12% <= 1.50% (root-to-finest change 0.365%) [oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=7.06e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.91e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): PASS U=0.00337
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.62-fcd62f550c49
│   └── K2_fine_large.m2-e923e7640822
├── Temporal discretisation (time-step sensitivity): PASS U=0.00791
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0238
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.long180-dda8a9c17278
    └── K2_fine_large.D2x-18f27cb1204c

CLAIM: strouhal_number of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=4.99e-06
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.01e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): PASS U=0.00991
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.62-fcd62f550c49
│   └── K2_fine_large.m2-e923e7640822
├── Temporal discretisation (time-step sensitivity): PASS U=0.0027
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.0112
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.long180-dda8a9c17278
    └── K2_fine_large.D2x-18f27cb1204c

```

## EXPERIMENT HISTORY

Run K2_fine_large-2d999cd1eb7c: submitted simulation (54244 cells, dt=0.007 D/U, half-height 60 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. Mesh, time and domain components are unmeasured for both mean_drag_coefficient and strouhal_number.
  - Averaging and statistics components are measured and small. For drag they are 7.057e-05 and 2.908e-05. For Strouhal they are 4.994e-06 and 2.011e-05. They use almost none of the 0.03 tolerance. R0 has 13 stationary cycles and drag drift of -2.9076e-05, so the remaining risk is discretisation or domain error.
  - The mesh is the weakest-looking element in R0. The representative cell size is 0.47033 D and the last wake cell is 0.96749 D, with only 150 streamwise wake cells. The wake is therefore coarsely resolved far downstream, and this could shift shedding frequency and drag.
  - The time step looks adequate: max Courant is 0.64796, there are 872.03 steps per shedding period, and the scheme is backward. The domain also looks adequate: 40 D upstream, 60 D downstream, half-height 60 D and blockage 0.0083333. Both are lower-probability risks than the mesh, though neither is verified.
  - The recorded cost is 8041 s for R0, and the budget allows 12x root compute with 6 experiments. Mesh refinement is affordable at an estimated 8677 s (default factor), with room left for the time and domain checks afterward.
  - Requested: REFINE_MESH {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — The mesh is the most likely unmeasured source of error larger than the 3 % tolerance. The wake cells are coarse, up to 0.96749 D. Time step and domain look comparatively adequate. Statistical noise on R0 is about 1e-5, so a factor of 2.0 (about 1.41x linear) gives a clear signal and gives the best estimate of the mesh error. The budget allows it.
  - Outcome: rejected by validator: child mesh has 216220 cells > limit 160000

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not allowed. Mesh, time and domain components are unmeasured for both mean_drag_coefficient and strouhal_number.
  - Averaging and statistics components are tiny. For drag they are 7.057e-05 and 2.908e-05. For Strouhal they are 4.994e-06 and 2.011e-05. R0 has 13 stationary cycles. Remaining risk is discretisation or domain error.
  - The validator rejected factor 2.0 because the child mesh would have 216220 cells, over the 160000 limit. 216220 / 54244 is about 3.99, so the factor scales cell count roughly as factor^2 (per-direction refinement). The limit of 160000 cells therefore allows a factor of about 1.717 at most.
  - A factor of 1.6 gives about 2.56x the cells, roughly 139000 cells. That is under the 160000 limit with margin. It is still a clear refinement of the 0.47033 D representative cell size and the 0.96749 D last wake cell.
  - The mesh stays the most likely source of error. The wake is coarse, with 150 streamwise cells and a last wake cell of 0.96749 D. Max Courant is 0.64796 with 872.03 steps per shedding period, and the domain is 40 D upstream, 60 D downstream and 60 D half-height with blockage 0.0083333. Time and domain look less risky but are unverified.
  - Budget is unused: 0 of 6 experiments and 0.0 of 12.0 relative compute. The estimated cost for mesh refinement is about 8677 s against 8041 s for R0, so time and domain runs remain affordable afterwards.
  - Requested: REFINE_MESH {'factor': 1.6} on K2_fine_large-2d999cd1eb7c — The mesh is the most likely unmeasured error source. The earlier factor of 2.0 was rejected because it gave 216220 cells against a limit of 160000. Factor 1.6 gives about 2.56x cells, roughly 139000, which fits. Statistical noise on R0 is about 1e-5, so even a small mesh effect will be clearly visible.
  - Outcome: executed -> K2_fine_large.m2-e923e7640822 (completed)
  - Numeric audit: 8 number(s) not traceable to evidence: 3.99, 1.717, 1.6, 2.56, 139000

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not allowed.
  - Time and domain components are unmeasured for both Cd and St. The St mesh component is also INCONCLUSIVE.
  - Mesh, Cd: R0 gives 1.3277 and R1 gives 1.3289, a change of 0.088%. The mesh uncertainty is 0.004327, which passes.
  - Mesh, St: R0 gives 0.16382 and R1 gives 0.16455, a change of 0.44%. The two-level Richardson estimate is 0.02187, above 0.5*tol = 0.015, so the St mesh check is INCONCLUSIVE.
  - Another mesh refinement can't fix this. REFINE_MESH is not allowed from R1, because cumulative refinement would exceed 2.0. From R0, a factor of 2.0 was already rejected for exceeding the cell limit. A factor near 1.7 would only repeat R1's resolution and would add little to a Richardson estimate.
  - R0 has 872.03 steps per shedding period, max Courant 0.64796 and a backward scheme. Temporal error looks small, but it is unverified.
  - R0 has blockage 0.0083333 and symmetryPlane lateral boundaries at 60 D. The question requires an unbounded stream. Boundary truncation or blockage can shift both Cd and St, and neither has been measured.
  - EXPAND_DOMAIN from R0 is the cheapest remaining experiment, at 5621 s. Budget used is 1 of 6 experiments and 1.56 of 12.0 relative compute, so it is affordable. REDUCE_TIME_STEP from R0 can follow it.
  - The submitted setup reports Cd 1.3278 and St 0.16382 with a frequency resolution of 0.013334. That resolution is coarse compared with the 3% tolerance on St. The stationary-window FFT value matches it at 0.16382.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Domain truncation is the only unmeasured component that the stated requirement 'treat the stream as unbounded' directly targets, and it has not been tested. It is the cheapest option from R0 at 5621 s. Further mesh refinement is blocked by the cumulative factor limit and the cell limit. The time step looks adequate.
  - Outcome: executed -> K2_fine_large.D2x-bc527461f36d (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.7

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not allowed.
  - Drag: averaging is 7.057e-05, statistics is 2.908e-05 and mesh is 0.004327 (R0 1.3277 vs R1 1.3289), all PASS. The time component is unmeasured. The domain component is 0.03173, above 0.5*tol = 0.015, so it is INCONCLUSIVE.
  - Strouhal: the mesh component is 0.02187 (R0 0.16382 vs R1 0.16455, change 0.44%), the domain component is 0.01884, and the time component is unmeasured. All three are INCONCLUSIVE.
  - The time-step sensitivity is unmeasured for both quantities. R0 has time_step_convective_units 0.007, max Courant 0.64796 and 872.03 steps per shedding period. No REDUCE_TIME_STEP run exists, so every quantity stays INCONCLUSIVE whatever else is resolved. This is the only component with no measurement.
  - Domain: R2 (80 D upstream, 120 D downstream, 120 D half-height) changes Cd from 1.3277 to 1.3208 (0.53%) and St from 0.16382 to 0.16331 (0.31%). The shifts are small but the estimate is inflated by the assumed order p=1 and Fs=3.
  - R2 is a weak comparison run. Its checkMesh_ok is false. Its far-field mesh is coarser (last wake cell 1.8673 D). It has only 6 stationary cycles, a Cd ci95 of 0.00088885 against 1.0366e-05 for R0, and drift of -0.0019997. The domain estimate is therefore confounded and noisy, and will need a follow-up run.
  - Budget: 2 of 6 experiments and 2.26 of 12.0 relative compute are used. REDUCE_TIME_STEP from R0 costs 8577 s, so it is affordable and leaves room for domain follow-up (RUN_LONGER or EXPAND_DOMAIN on R2) and St mesh work.
  - REFINE_MESH is not allowed from R1 (cumulative refinement 2.26 exceeds the 2.0 limit). It cannot clear the St mesh component this iteration.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — The time component is the only one with no measurement for either quantity, so no ACCEPT is possible without it. R0 is the root, so the time-step comparison is made directly against the quantities being certified. R0 has the longest record (13 stationary cycles) and the lowest noise. The cost is 8577 s, which fits the remaining budget.
  - Outcome: executed -> K2_fine_large.dt0.0035-6a0f9a80f290 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not allowed.
  - Cd: averaging 7.057e-05, statistics 2.908e-05, mesh 0.004327 (R0 1.3277 vs R1 1.3289) and time 0.007908 (R0 vs R3 1.3251) all PASS. Domain is 0.03173, which is above 0.5*tol = 0.015 and is the only blocker for Cd.
  - St: averaging, statistics and time (0.0027, R0 0.16382 vs R3 0.16393) PASS. Mesh is 0.02187 (R0 0.16382 vs R1 0.16455, change 0.44%) and domain is 0.01884. Both are INCONCLUSIVE.
  - Domain is the largest open item. R2 (80 D upstream, 120 D downstream, 120 D half-height) gives Cd 1.3208 and St 0.16331, which are changes of 0.53% and 0.31% from R0. The assumed order is p=1 with Fs=3, and the noise floors are 2.0e-03 for Cd and 1.5e-03 for St. The estimate is therefore inflated by noise as well as by the assumed order.
  - R2 is a weak comparison run. It has only 6 stationary cycles, a Cd ci95 of 0.00088885 against 1.0366e-05 for R0, drift of -0.0019997, stationary_window_start_is_mser_cap true, checkMesh_ok false and a coarse far-field (last wake cell 1.8673 D). The 0.53% change may therefore be partly transient or noise.
  - The time check is now measured and small: R3 has half the time step, 1742.9 steps per period and max Courant 0.26056. R3 changes Cd by 0.198% and St by 0.068% from R0. The time component does not need more work.
  - RUN_LONGER on R2 attacks the noise and drift that inflate the domain estimate. It costs about 7027 s, which is the cheapest useful option. Budget is 3 of 6 experiments and 3.33 of 12.0 relative compute used, so it is affordable.
  - A further mesh level for the St mesh component is possible later. REFINE_MESH from R0 with a small factor could give a third level. REFINE_MESH from R1 is not allowed because the cumulative refinement limit is exceeded.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on K2_fine_large.D2x-bc527461f36d — Domain is the largest open component, with Cd at 0.03173 and St at 0.01884. R2 is the only domain comparison, and it is noisy and still drifting (6 cycles, drift -0.0019997, ci95 0.00088885, noise floor 2.0e-03). Extending R2 removes the noise and drift confounder cheaply, at about 7027 s, and shows whether the R0-to-R2 shift is real.
  - Outcome: executed -> K2_fine_large.long180-dda8a9c17278 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT and REJECT are therefore both unavailable.
  - Cd: averaging 7.057e-05, statistics 2.908e-05, mesh 0.004327 and time 0.007908 all PASS. Only the domain component blocks it, at 0.03693, against a limit of 0.5*tol = 0.015.
  - St: averaging 4.994e-06, statistics 2.011e-05 and time 0.0027 PASS. Mesh (0.02187) and domain (0.02237) are INCONCLUSIVE.
  - Domain evidence: R4 (R2 extended to 14 stationary cycles, ci95 2.2903e-05) has Cd 1.3196 and St 0.16321. R0 has Cd 1.3277 and St 0.16382. The changes are 0.62% for Cd and 0.37% for St, and both are far below the 3% tolerance. The inconclusive status comes from the assumed order p=1 with safety factor Fs=3 on a two-level comparison, which inflates the estimate.
  - The domain trend is not yet characterised. Cd moved from 1.3277 (R0, 60 D) to 1.3208 (R2, 120 D) and to 1.3196 (R4, same domain as R2, longer record). A third domain level would give an observed order and show whether the change is converging.
  - R4 is the best base for a third domain level. It has 14 cycles, drift of -9.4811e-05 and ci95 of 2.2903e-05, so noise will not mask the signal. EXPAND_DOMAIN from R4 is listed at 7234 s and is not marked as disallowed.
  - Caveat: R2 and R4 have checkMesh_ok false and a coarser far field (last wake cell 1.8673 D). A change between levels may therefore mix domain and far-field mesh effects. The near-field mesh is unchanged (200 cells around the cylinder), which limits this.
  - Time is measured and small. R3 changes Cd by 0.198% and St by 0.068% from R0. It needs no more work.
  - St mesh is the other open item. R0 to R1 changes St by 0.44% (0.16382 to 0.16455), but the estimate is 0.02187 under the assumed p=2. It affects only St, while domain blocks both quantities, so domain goes first.
  - Budget: 4 of 6 experiments and 4.2 of 12.0 relative compute are used. One experiment of about 7234 s fits and leaves one more for the St mesh component.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K2_fine_large.long180-dda8a9c17278 — Domain is the one component that blocks both Cd and St. Only two domain levels exist, so the order is assumed. R4 is the longest and lowest-noise domain run, with 14 cycles and ci95 2.2903e-05. Expanding it again by 2.0 gives a third level (R0, R4, child) and an observed convergence rate. The near-field mesh is unchanged. The cost of 7234 s fits the remaining budget.
  - Outcome: executed -> K2_fine_large.D2x-18f27cb1204c (completed)

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT and REJECT are both unavailable.
  - Mean Cd: averaging 7.057e-05, statistics 2.908e-05, mesh 0.004327 and time 0.007908 all PASS. Only the domain component blocks it, at 0.02385 against a limit of 0.5*tol = 0.015.
  - Strouhal: averaging 4.994e-06, statistics 2.011e-05, time 0.0027 and domain 0.01119 all PASS. Only the mesh component blocks it, at 0.02187 (R0 0.16382 vs R1 0.16455, change 0.44%).
  - The demonstrated changes are far below the 0.03 tolerance. Cd domain: R0 1.3277, R4 1.3196, R5 1.3185. Cd time: R0 1.3277 vs R3 1.3251. The INCONCLUSIVE status comes from conservative uncertainty estimates (Fs=3, order capped at p=1), not from a measured violation.
  - The domain Cd estimate is a three-level result (R0, R4, R5). The verifier reports observed order 2.79 outside [0.5, 2.0]x formal and uses p=min(observed, formal)=1.00. Cd moves 1.3277 to 1.3196 to 1.3185, so the change is shrinking quickly. Another domain run cannot lift the p=1 cap, so it is unlikely to bring 0.02385 under 0.015. EXPAND_DOMAIN is also disallowed from R5 (cumulative factor limit 4.0).
  - The St mesh estimate rests on only two levels (R0 and R1). One remaining experiment can add a third mesh level. A REFINE_MESH child of R0 at factor 1.3 gives an observed order for St and a Richardson estimate that is not assumed. This is the only blocker that a single run can plausibly clear.
  - REFINE_MESH from R1 is not allowed (cumulative refinement limit 2.0). From R0 the child must stay under 160000 cells. R0 has 54244 cells and R1 has 138064, so factor 1.3 (about 1.69x cells, roughly 92000) fits and sits between R0 and R1.
  - Budget: 5 of 6 experiments and 5.1 of 12.0 relative compute used. One experiment fits (R0 REFINE_MESH is listed at 8677 s at the default factor). Time is already measured and small (R3 changes Cd by 0.198% and St by 0.068%).
  - Even if this run clears the St mesh component, Cd domain remains INCONCLUSIVE. The final report is therefore likely to stay INCONCLUSIVE unless the verifier's domain estimate changes.
  - Requested: REFINE_MESH {'factor': 1.3} on K2_fine_large-2d999cd1eb7c — The St mesh component is the only blocker that one run can plausibly clear. It is a two-level estimate with no observed order. A factor of 1.3 gives an intermediate level (about 92000 cells, under the 160000 limit) between R0 (54244 cells) and R1 (138064 cells). That makes a three-level sequence for St and Cd.
  - Outcome: executed -> K2_fine_large.m1.62-fcd62f550c49 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 1.69, 92000, 0.62%, 92000

Run K2_fine_large.m2-e923e7640822: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→2, time.delta_t: 0.007→0.006077, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3289 (+0.09%).
  - Observation: strouhal_number 0.16382 → 0.16455 (+0.44%).

Run K2_fine_large.D2x-bc527461f36d: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→120, domain.half_height: 60→120, domain.upstream: 40→80, mesh.n_downstream: 120→155, mesh.n_lateral: 51→61, mesh.n_upstream: 38→46, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3208 (-0.53%).
  - Observation: strouhal_number 0.16382 → 0.16331 (-0.31%).

Run K2_fine_large.dt0.0035-6a0f9a80f290: REDUCE_TIME_STEP from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, time.delta_t: 0.007→0.0035, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3251 (-0.20%).
  - Observation: strouhal_number 0.16382 → 0.16393 (+0.07%).

Run K2_fine_large.long180-dda8a9c17278: RUN_LONGER from K2_fine_large.D2x-bc527461f36d (time.end_time: 80→180).
  - Observation: mean_drag_coefficient 1.3208 → 1.3196 (-0.09%).
  - Observation: strouhal_number 0.16331 → 0.16321 (-0.06%).

Run K2_fine_large.D2x-18f27cb1204c: EXPAND_DOMAIN from K2_fine_large.long180-dda8a9c17278 (domain.downstream: 120→240, domain.half_height: 120→240, domain.upstream: 80→160, mesh.n_downstream: 155→191, mesh.n_lateral: 61→71, mesh.n_upstream: 46→54, time.end_time: 180→80).
  - Observation: mean_drag_coefficient 1.3196 → 1.3185 (-0.09%).
  - Observation: strouhal_number 0.16321 → 0.16323 (+0.01%).

Run K2_fine_large.m1.62-fcd62f550c49: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→1.625, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3292 (+0.11%).
  - Observation: strouhal_number 0.16382 → 0.1643 (+0.29%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0152 vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K2_fine_large-2d999cd1eb7c` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=8041 s; record: results/runs/K2_fine_large-2d999cd1eb7c/run.json
- `K2_fine_large.m2-e923e7640822` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:39+00:00 wall=1.145e+04 s; record: results/runs/K2_fine_large.m2-e923e7640822/run.json
- `K2_fine_large.D2x-bc527461f36d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:02+00:00 wall=3765 s; record: results/runs/K2_fine_large.D2x-bc527461f36d/run.json
- `K2_fine_large.dt0.0035-6a0f9a80f290` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T01:15:34+00:00 wall=3507 s; record: results/runs/K2_fine_large.dt0.0035-6a0f9a80f290/run.json
- `K2_fine_large.long180-dda8a9c17278` status=completed parent=K2_fine_large.D2x-bc527461f36d created=2026-10-20T08:47:43+00:00 wall=4900 s; record: results/runs/K2_fine_large.long180-dda8a9c17278/run.json
- `K2_fine_large.D2x-18f27cb1204c` status=completed parent=K2_fine_large.long180-dda8a9c17278 created=2026-10-20T10:51:15+00:00 wall=5680 s; record: results/runs/K2_fine_large.D2x-18f27cb1204c/run.json
- `K2_fine_large.m1.62-fcd62f550c49` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T12:26:35+00:00 wall=6181 s; record: results/runs/K2_fine_large.m1.62-fcd62f550c49/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 6974062801.0, "relative_to_root": 5.999737391261073, "experiment_wall_seconds": 35481.88136101601, "n_experiments": 6, "planner_calls": 7, "planner_cost_usd": 0.6580210999999999, "loop_wall_seconds": 37717.039478823004}
