# Verification report: X2_inlet_shear (C-llm-v1+review)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3312
- strouhal_number: 0.16312

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
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.047% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.035% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.27e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.50e-03 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.76% <= 1.50% (root-to-finest change 0.254%) [differences within 2x statistical noise (2.3e-03); range-based U with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.18% <= 1.50% (root-to-finest change 0.828%) [three-level Celik procedure, observed order p=3.01, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.14% <= 1.50% (root-to-finest change 0.285%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.3e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.75% <= 1.50% (root-to-finest change 0.085%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.5e-03)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.07% > 1.50% but the demonstrated change 0.68% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 2.3e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.35% > 1.50% but the demonstrated change 0.39% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 2.5e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000473
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.00227
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): PASS U=0.00761
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.m1.41-ca5c50f2e498
│   └── X2_inlet_shear.m2-3f2d80a2a02e
├── Temporal discretisation (time-step sensitivity): PASS U=0.0114
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.dt0.005-2ef6d66a694b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0407
    └── X2_inlet_shear-32168bfbca6b
    └── X2_inlet_shear.long430-1e25bc8ea220

CLAIM: strouhal_number of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000352
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.0025
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): PASS U=0.0118
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.m1.41-ca5c50f2e498
│   └── X2_inlet_shear.m2-3f2d80a2a02e
├── Temporal discretisation (time-step sensitivity): PASS U=0.00749
│   └── X2_inlet_shear-32168bfbca6b
│   └── X2_inlet_shear.dt0.005-2ef6d66a694b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0235
    └── X2_inlet_shear-32168bfbca6b
    └── X2_inlet_shear.long430-1e25bc8ea220

```

## EXPERIMENT HISTORY

Run X2_inlet_shear-32168bfbca6b: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so I cannot REJECT or ACCEPT. Mesh, time and domain uncertainty are all unmeasured for both mean_drag_coefficient and strouhal_number.
  - R0 shedding is well sampled. It has 11 stationary cycles, a drag CI95 of 0.00097218 and an averaging bias of 0.0004734 (Cd) and 0.000352 (St). Statistics are 0.002267 (Cd) and 0.002498 (St). All are far below the 0.03 tolerance, so RUN_LONGER would add little.
  - Anomaly in R0 inlet_velocity_measured: ux_min is 0.1125 and ux_max is 0.1875 (ux_nonuniformity 0.5), with a mean of 0.15. The question specifies a uniform stream, and the force reference uses magUInf 0.15. A non-uniform inlet could bias Cd and St by an unknown amount. The verifier has no check for this, so it is not a FAIL. It is still a flag.
  - The domain check is the only one touching the inlet and outer boundaries. R0 has upstream_D 30, downstream_D 50 and half_height_D 40, with symmetryPlane sides and a blockage ratio of 0.0125. Expanding the domain tests boundary truncation. It may also expose the inlet non-uniformity, depending on how the profile scales.
  - Time resolution looks adequate: time step 0.01 convective units, max Courant 0.7323, 612.82 steps per shedding period, backward scheme. Temporal error is less likely to exceed tolerance than mesh or domain error.
  - Mesh is a concern. It has 30580 cells, a representative size of 0.45745 D and a last wake cell of 1.0209 D. Mesh refinement is still needed, but EXPAND_DOMAIN is cheaper (1405 s vs 2443 s) and addresses the inlet anomaly first. Mesh and time experiments can follow within the budget (0 of 6 experiments used).
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X2_inlet_shear-32168bfbca6b — R0 recorded a non-uniform inlet (ux 0.1125 to 0.1875, nonuniformity 0.5) although the stream is specified as uniform. This is the most conspicuous departure from the problem statement and the most likely flaw to move Cd or St by more than 3%. EXPAND_DOMAIN is the primitive that probes the boundaries and inlet, and it is the cheapest informative experiment (1405 s). The domain component is also unmeasured, with a 0.0125 blockage and symmetry side walls.
  - Outcome: executed -> X2_inlet_shear.D2x-8d92db3cbed0 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I cannot ACCEPT. I cannot REJECT either, because no FAIL has been measured. Mesh, time and domain components are still INCONCLUSIVE for both Cd and St.
  - R0 is well sampled. It has 11 stationary cycles, a Cd CI95 of 0.00097218, a Cd statistics uncertainty of 0.002267 and an St statistics uncertainty of 0.002498. RUN_LONGER on R0 would add little.
  - R1 (EXPAND_DOMAIN x2 of R0) gives a stationary-window Cd of 1.4857 against 1.3306 for R0, and St of 0.17529 (FFT 0.16948) against 0.16318 for R0. This must not be read as a domain effect, because R1 is not statistically reliable.
  - R1's Cd drift_rel is 0.27794, its half_diff_rel is 0.11656 and its Cd CI95 is 0.10446. Its stationary window starts at 4.0695 convective units, with stationary_window_start_is_mser_cap false. The window therefore still contains the start-up transient. R1's own reported-setup values (Cd 1.5627, St 0.18326) differ from its window values. The verifier states that R1 must be run longer first.
  - R1 is also confounded. Its checkMesh_ok is false, although max non-orthogonality 43.313 and max skewness 0.53384 are identical to R0. Its representative cell size is 0.79405 D against 0.45745 D for R0, and its wake_last_cell_D is 1.9729 against 1.0209. EXPAND_DOMAIN was meant to leave the near field unchanged, so R1 may mix mesh and domain effects.
  - R1 has a long downstream length (100 D) and was run only to 80 convective units. Transient length probably scales with domain size, so a longer R1 is the most direct way to get a usable domain comparison.
  - Both R0 and R1 record a non-uniform inlet: ux_min 0.1125, ux_max 0.1875, mean 0.15, ux_nonuniformity 0.5. The question specifies a uniform stream. Expanding the domain did not remove this, and no menu primitive can change it. The verifier has no check for it, so it is not a FAIL, but it remains an unquantified risk to the requested Cd and St. It must be flagged to the submitter.
  - Time-step error (0.01 convective units, max Courant 0.7323, 612.82 steps per period) and mesh error (0.45745 D representative cell size) are still unmeasured. They are lower priority than making the domain comparison valid. Budget is ample: 1 of 6 experiments used and 0.71 of 12.0 compute.
  - Requested: RUN_LONGER {'additional_convective_times': 150.0} on X2_inlet_shear.D2x-8d92db3cbed0 — The domain-sensitivity check for both quantities is INCONCLUSIVE because R1 is not statistically reliable (Cd drift_rel 0.27794, CI95 0.10446, window start 4.0695, not an MSER cap). The verifier says to run it longer first. R1's record of 79.99 convective units is too short for its larger domain (100 D downstream). Extending R1 gives a valid R0 vs R1 comparison. That comparison is the only available handle on the boundary and blockage error, and a demonstrated change above tolerance would be a FAIL. RUN_LONGER on R1 is cheaper than REFINE_MESH or REDUCE_TIME_STEP on any parent, and it unblocks the verdict.
  - Outcome: executed -> X2_inlet_shear.long230-1a1e9e99a483 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, because the mesh, time and domain components are unmeasured for both Cd and St. I can't REJECT, because no FAIL has been measured.
  - R0 is well sampled. It has 11 stationary cycles, a Cd CI95 of 0.00097218, and statistics uncertainty of 0.002267 (Cd) and 0.002498 (St). Averaging bias is 0.0004734 (Cd) and 0.000352 (St). More run time on R0 would add little.
  - R2 (R1 run to 230 convective units, 20 cycles) gives a stationary-window Cd of 1.329 and St of 0.16325. R0 gives Cd 1.3306 and St 0.16318. The two domains agree closely, which is encouraging for the domain component.
  - The verifier still marks the domain check INCONCLUSIVE. R2 is not statistically reliable: Cd drift_rel is -0.02625, the Cd uncertainty is 0.026250161373716333, and the St uncertainty is 0.019654541917742144. R2's reported-setup Cd of 1.3922 differs from its window Cd of 1.329, so its transient is slow. The R2 agreement is therefore indicative only, not a certified domain uncertainty.
  - R1 and R2 are confounded. Their representative cell size is 0.79405 D against 0.45745 D for R0, wake_last_cell_D is 1.9729 against 1.0209, and checkMesh_ok is false. Near-field settings are identical to R0: 160 cells around the cylinder and wall_first_cell_D 0.005. Even so, the domain comparison mixes in far-field mesh differences.
  - Mesh error is the largest unmeasured risk to the 0.03 tolerance. R0 has only 30580 cells and a wake_last_cell_D of 1.0209. REFINE_MESH from R0 has not been run. It is the experiment most likely to expose an error larger than the tolerance, and it also gives a clean same-domain comparison.
  - Time resolution looks adequate on paper: time step 0.01, max Courant 0.7323, 612.82 steps per shedding period, backward scheme. It is still unmeasured, so REDUCE_TIME_STEP stays in the plan.
  - All runs record a non-uniform inlet: ux_min 0.1125, ux_max 0.1875, mean 0.15, ux_nonuniformity 0.5. The question specifies a uniform stream. No menu primitive can change or measure this, and the verifier has no check for it. It is not a FAIL, but it is an unquantified risk and should be flagged to the submitter.
  - Budget is sufficient. 2 of 6 experiments are used and compute is 2.04 of 12.0. Mesh, time and a longer R2 can all still be afforded.
  - Requested: REFINE_MESH {'factor': 1.4142} on X2_inlet_shear-32168bfbca6b — Mesh error is unmeasured and is the most likely remaining flaw to move Cd or St by more than the 0.03 tolerance. R0 is coarse (0.45745 D representative size, last wake cell 1.0209 D). The domain evidence from R2 already looks consistent with R0, though it is not yet certified. Refining R0 isolates mesh effects on the same domain, avoiding the confounding in R1 and R2.
  - Outcome: executed -> X2_inlet_shear.m1.41-ca5c50f2e498 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. I can't ACCEPT, because the time and domain components are unmeasured for both quantities and the mesh component is unmeasured for St. I can't REJECT, because no FAIL was measured.
  - R3 (REFINE_MESH of R0, 61366 cells vs 30580) gives stationary-window Cd 1.3338 and St 0.16419. R0 gives Cd 1.3306 and St 0.16318. The root-to-finest change is 0.240% for Cd and 0.62% for St, both far below the 3% tolerance.
  - Mesh component for Cd passes at 1.44% (limit 1.5%), only just inside the budget. St mesh uncertainty is 3.68% and INCONCLUSIVE. This comes from a two-level Richardson estimate with an assumed order p=2 and Fs=3. The observed order is not measured, so the estimate is conservative and can't be certified.
  - R3 has only 6 stationary cycles, with its window start at the MSER cap (40.921). Its Cd CI95 is 2.576e-05, so the statistics are not the limiting factor. R3 also uses a smaller time step (0.0086903 vs 0.01), so the R0-to-R3 change mixes spatial and temporal effects slightly.
  - Domain check is INCONCLUSIVE because R2 is not statistically reliable. R2 has Cd drift_rel -0.02625, Cd uncertainty 0.02625 and St uncertainty 0.019654. R2 (Cd 1.329, St 0.16325) agrees with R0 (Cd 1.3306, St 0.16318) but that agreement is indicative only. R1 and R2 also have checkMesh_ok false and a coarser far-field mesh (0.79405 D vs 0.45745 D).
  - Time sensitivity is unmeasured. R0 has dt 0.01, max Courant 0.7323 and 612.82 steps per period, so a large error is unlikely. Unmeasured is still not a pass.
  - All runs record a non-uniform inlet (ux 0.1125 to 0.1875, mean 0.15, nonuniformity 0.5), although the question specifies a uniform stream. The verifier has no check for it and no menu primitive can change or measure it. It is an unquantified risk and must be flagged to the submitter.
  - Budget: 3 of 6 experiments used and 3.27 of 12.0 compute. REFINE_MESH from R3 costs about 5695 s (~2.9x root), leaving enough for REDUCE_TIME_STEP (~2116 s) and RUN_LONGER on R2 (~1756 s) afterwards.
  - Requested: REFINE_MESH {'factor': 1.4142} on X2_inlet_shear.m1.41-ca5c50f2e498 — St mesh uncertainty (3.68%) is the only component that exceeds the tolerance, and it is INCONCLUSIVE. It rests on an assumed order p=2 from two levels. Cd mesh is also close to its budget (1.44% vs 1.5%). Refining the finest run, R3, continues the same refinement family and gives a third level. That lets the observed order be measured and the St and Cd mesh uncertainty be certified or shown to be a FAIL. It avoids the far-field mesh confounding present in R1 and R2. Budget allows it and still leaves room for REDUCE_TIME_STEP and RUN_LONGER on R2.
  - Outcome: executed -> X2_inlet_shear.m2-3f2d80a2a02e (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 0.019654, 2.9, 0.019654

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. I can't ACCEPT, because the time and domain components are INCONCLUSIVE for both Cd and St. I can't REJECT, because no FAIL has been measured.
  - Mesh is now measured for both quantities. Cd mesh uncertainty is 0.00761 and St mesh uncertainty is 0.0118. St uses a three-level Celik estimate with observed order p=3.01. Both are below 0.015. R0 (Cd 1.3306, St 0.16318) to R4 (Cd 1.334, St 0.16454) is a change of 0.254% for Cd and 0.828% for St.
  - R0 statistics are good. It has 11 cycles, a Cd CI95 of 0.00097218, statistics uncertainty of 0.002267 (Cd) and 0.002498 (St), and averaging bias of 0.0004734 (Cd) and 0.000352 (St). More run time on R0 is not useful.
  - The domain check is INCONCLUSIVE only because R2 is statistically unreliable. R2 has Cd drift_rel -0.02625, Cd uncertainty 0.02625 and St uncertainty 0.019654. R2's window values (Cd 1.329, St 0.16325) are close to R0's (Cd 1.3306, St 0.16318), but this is indicative only. R2's reported-setup Cd of 1.3922 differs from its window Cd, so the transient is slow. R2's stationary window starts at 107.29 and is an MSER cap (stationary_window_start_is_mser_cap true).
  - R1 and R2 have checkMesh_ok false and a coarser far-field mesh than R0 (representative size 0.79405 D vs 0.45745 D, wake_last_cell_D 1.9729 vs 1.0209). The domain comparison is therefore slightly confounded. The near-field settings are the same: 160 cells around the cylinder and wall_first_cell_D 0.005.
  - The time component is unmeasured. R0 uses dt 0.01, max Courant 0.7323 and 612.82 steps per period. This is probably adequate, but unmeasured is not a pass. REDUCE_TIME_STEP on R0 (~2116 s) is the only way to close it.
  - Budget: 4 of 6 experiments used and 6.14 of 12.0 compute. Two experiments remain. Closing both open components needs exactly two: RUN_LONGER on R2 and REDUCE_TIME_STEP on R0. I put the domain first because it is the less certain to resolve (R2 may still be unreliable), and a failure there needs to show up before the time-step run. A flawed domain would also change R0's answer more than a time-step error would.
  - All runs record a non-uniform inlet: ux_min 0.1125, ux_max 0.1875, mean 0.15, ux_nonuniformity 0.5. The question specifies a uniform stream. No menu primitive can measure or remove this, and the verifier has no check for it. It is not a FAIL, but it is an unquantified risk and must be flagged to the submitter.
  - Requested: RUN_LONGER {'additional_convective_times': 200.0} on X2_inlet_shear.long230-1a1e9e99a483 — The domain check is INCONCLUSIVE only because R2 is statistically unreliable (Cd drift_rel -0.02625, Cd uncertainty 0.02625, St uncertainty 0.019654). R2's window start (107.29) is an MSER cap, so the transient may not have ended. Extending R2 is the only way to get a certified R0 vs R2 domain comparison. Two experiments remain, and this one plus REDUCE_TIME_STEP on R0 closes both open components. I run the domain experiment first because it is the less certain to resolve and may still expose a change above tolerance.
  - Outcome: executed -> X2_inlet_shear.long430-1e25bc8ea220 (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 0.019654, 0.019654, 0.019654

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with failed_checks empty. I can't ACCEPT, because the time and domain components are INCONCLUSIVE for both Cd and St. I can't REJECT, because no FAIL was measured.
  - Mesh is certified for both quantities. Cd mesh uncertainty is 0.00761 and St mesh uncertainty is 0.0118 (three-level Celik, observed p=3.01). R0 (Cd 1.3306, St 0.16318) to R4 (Cd 1.334, St 0.16454) changes by 0.254% for Cd and 0.828% for St.
  - R0 statistics and averaging are fine: 11 cycles, Cd CI95 0.00097218, statistics uncertainty 0.002267 (Cd) and 0.002498 (St), averaging bias 0.0004734 (Cd) and 0.000352 (St). RUN_LONGER on R0 would add little.
  - R5 (R2 run to 430 convective units) is now statistically reliable. It has 40 cycles, Cd CI95 0.0002689 and drift_rel 0.0017393. Its stationary window values are Cd 1.3216 and St 0.16254, against R0's Cd 1.3306 and St 0.16318. The demonstrated change is 0.68% for Cd and 0.39% for St, far below the 0.03 tolerance. No domain FAIL is indicated.
  - The domain check is still INCONCLUSIVE. With only two levels (R0, R5) the verifier assumes order p=1 with Fs=3, which gives 0.04075 (Cd) and 0.02349 (St). Both exceed the 0.015 half-tolerance budget. This is a conservative extrapolation, not a measured error.
  - R1, R2 and R5 have checkMesh_ok false and a coarser far-field mesh than R0 (representative size 0.79405 D vs 0.45745 D, wake_last_cell_D 1.9729 vs 1.0209). The domain comparison is therefore slightly confounded with mesh.
  - A third domain level would probably not give a usable result with one experiment left. R1, from R0, was run only to 80 convective units and was unreliable (drift_rel 0.27794). R5 needed a stationary window starting at 180.58 in the larger domain. An EXPAND_DOMAIN child of R5 would likely hit the same transient problem.
  - The time component is still unmeasured: no REDUCE_TIME_STEP run exists. R0 uses dt 0.01 convective units, max Courant 0.7323 and 612.82 steps per period. R3 and R4, also children of R0, were reliable at 80 units (Cd CI95 2.576e-05 and 1.7905e-05). A time-step child of R0 should therefore give a clean, same-domain time estimate for about 2116 s.
  - Budget: 5 of 6 experiments used and 7.91 of 12.0 compute. One experiment remains. It can close the time component but not the domain component. The final outcome will likely be INCONCLUSIVE, unless the time-step run exposes a change above tolerance. That would be a FAIL.
  - All runs record a non-uniform inlet: ux_min 0.1125, ux_max 0.1875, mean 0.15, ux_nonuniformity 0.5. The question specifies a uniform stream. No menu primitive can measure or remove this and the verifier has no check for it. It is not a FAIL, but it is an unquantified risk and must be flagged to the submitter.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on X2_inlet_shear-32168bfbca6b — The time component is unmeasured for both quantities, and it is the only open component that one experiment can close cleanly. R0's same-domain, same-mesh children (R3, R4) ran reliably at 80 units, so a time-step child of R0 should be reliable. Domain refinement would likely give an unreliable short run in a larger domain, as R1 did. The cost is about 2116 s, which fits the remaining compute budget (7.91 of 12.0 used).
  - Outcome: executed -> X2_inlet_shear.dt0.005-2ef6d66a694b (completed)

Run X2_inlet_shear.D2x-8d92db3cbed0: EXPAND_DOMAIN from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.4857 (+11.66%).
  - Observation: strouhal_number 0.16318 → 0.17529 (+7.42%).

Run X2_inlet_shear.long230-1a1e9e99a483: RUN_LONGER from X2_inlet_shear.D2x-8d92db3cbed0 (time.end_time: 80→230).
  - Observation: mean_drag_coefficient 1.4857 → 1.329 (-10.55%).
  - Observation: strouhal_number 0.17529 → 0.16325 (-6.87%).

Run X2_inlet_shear.m1.41-ca5c50f2e498: REFINE_MESH from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.00869, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3338 (+0.24%).
  - Observation: strouhal_number 0.16318 → 0.16419 (+0.62%).

Run X2_inlet_shear.m2-3f2d80a2a02e: REFINE_MESH from X2_inlet_shear.m1.41-ca5c50f2e498 (mesh.refinement: 1.414→2, time.delta_t: 0.00869→0.007432).
  - Observation: mean_drag_coefficient 1.3338 → 1.334 (+0.01%).
  - Observation: strouhal_number 0.16419 → 0.16454 (+0.21%).

Run X2_inlet_shear.long430-1e25bc8ea220: RUN_LONGER from X2_inlet_shear.long230-1a1e9e99a483 (time.end_time: 230→430).
  - Observation: mean_drag_coefficient 1.329 → 1.3216 (-0.56%).
  - Observation: strouhal_number 0.16325 → 0.16254 (-0.43%).

Run X2_inlet_shear.dt0.005-2ef6d66a694b: REDUCE_TIME_STEP from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3268 (-0.28%).
  - Observation: strouhal_number 0.16318 → 0.16332 (+0.08%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X2_inlet_shear-32168bfbca6b` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=1984 s; record: results/runs/X2_inlet_shear-32168bfbca6b/run.json
- `X2_inlet_shear.D2x-8d92db3cbed0` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T10:07:14+00:00 wall=1191 s; record: results/runs/X2_inlet_shear.D2x-8d92db3cbed0/run.json
- `X2_inlet_shear.long230-1a1e9e99a483` status=completed parent=X2_inlet_shear.D2x-8d92db3cbed0 created=2026-10-19T15:20:12+00:00 wall=2714 s; record: results/runs/X2_inlet_shear.long230-1a1e9e99a483/run.json
- `X2_inlet_shear.m1.41-ca5c50f2e498` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T10:06:49+00:00 wall=2448 s; record: results/runs/X2_inlet_shear.m1.41-ca5c50f2e498/run.json
- `X2_inlet_shear.m2-3f2d80a2a02e` status=completed parent=X2_inlet_shear.m1.41-ca5c50f2e498 created=2026-10-19T11:25:18+00:00 wall=7000 s; record: results/runs/X2_inlet_shear.m2-3f2d80a2a02e/run.json
- `X2_inlet_shear.long430-1e25bc8ea220` status=completed parent=X2_inlet_shear.long230-1a1e9e99a483 created=2026-10-19T18:29:37+00:00 wall=2550 s; record: results/runs/X2_inlet_shear.long430-1e25bc8ea220/run.json
- `X2_inlet_shear.dt0.005-2ef6d66a694b` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T18:29:05+00:00 wall=1343 s; record: results/runs/X2_inlet_shear.dt0.005-2ef6d66a694b/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 4116667876.0, "relative_to_root": 8.974641107477654, "experiment_wall_seconds": 17246.720580720994, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.64112492, "loop_wall_seconds": 50653.543833955}
