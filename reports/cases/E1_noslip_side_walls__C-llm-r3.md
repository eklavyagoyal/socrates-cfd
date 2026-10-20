# Verification report: E1_noslip_side_walls (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3403
- strouhal_number: 0.16429

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 9.70e-04 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.14% <= 1.50% (root-to-finest change 0.761%) [three-level Celik procedure, observed order p=2.57, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.12% > 1.50% but the demonstrated change 1.23% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.84, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.83% <= 1.50% (root-to-finest change 0.209%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.55% <= 1.50% (root-to-finest change 0.137%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.7e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.43% > 1.50% but the demonstrated change 1.41% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.18, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.76% > 1.50% but the demonstrated change 1.02% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.18, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=9.32e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.0012
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): PASS U=0.0114
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-39a4571e43e5
├── Temporal discretisation (time-step sensitivity): PASS U=0.00834
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0243
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D1.5x-f702a7c7fa9d
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D3x-5e6cfbc7fe84

CLAIM: strouhal_number of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=6.51e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.00097
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0212
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-39a4571e43e5
├── Temporal discretisation (time-step sensitivity): PASS U=0.00547
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0176
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D1.5x-f702a7c7fa9d
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D3x-5e6cfbc7fe84

```

## EXPERIMENT HISTORY

Run E1_noslip_side_walls-88a7cd5812e8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - R0 mesh, time and domain uncertainty components are all unmeasured for both mean_drag_coefficient and strouhal_number. Together they decide the 0.03 tolerance.
  - R0 averaging and statistics are small. Drag has averaging 9.319e-05 and statistics 0.001199. Strouhal has averaging 6.507e-05 and statistics 0.0009705. R0 has 13 stationary cycles, so RUN_LONGER would add little.
  - R0 mesh is coarse for resolving a vortex street. It has 30580 cells, representative_cell_size_D 0.45745 and wake_last_cell_D 1.0209. Wake spacing is about 111 cells over 50 D. Vortex shedding frequency and drag are sensitive to wake and near-wall resolution, and the mesh has never been refined.
  - R0 time step is 0.01 convective units with 608.73 steps per shedding period and max Courant 0.73374. Backward time scheme and linearUpwind are second order. Temporal error is therefore less likely to be the dominant error.
  - R0 domain has 30 D upstream, 50 D downstream, 40 D half height and blockage 0.0125. The lateral boundary is a noSlipWall, which is a possible bias, but it is far away. Domain error is probably smaller than mesh error, so test it afterwards.
  - REFINE_MESH from R0 costs about 2284 s against a budget of 12x root compute and 6 experiments. It is affordable and the most informative first step.
  - Requested: REFINE_MESH {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Mesh error is the largest unmeasured component for both quantities. R0 has a coarse mesh (30580 cells, representative_cell_size_D 0.45745, wake_last_cell_D 1.0209) and has never been refined. Time step and domain look comparatively adequate. A factor of 2.0 gives a clear signal above the statistical noise of 0.001199 for drag and 0.0009705 for Strouhal.
  - Outcome: executed -> E1_noslip_side_walls.m2-39a4571e43e5 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. ACCEPT is not allowed, and REJECT is not justified.
  - The R0 averaging and statistics components pass. Drag has averaging 9.319e-05 and statistics 0.001199. Strouhal has averaging 6.507e-05 and statistics 0.0009705. R0 has 13 stationary cycles, so RUN_LONGER would add little.
  - The mesh component is now estimated but is over budget. Drag is 0.03044 and Strouhal is 0.0491, against a half-tolerance of 0.015. The estimate comes from a two-level Richardson with an assumed order p=2.
  - From R0 to R1 the measured change is small. Drag goes from 1.3402 to 1.3505, which is 0.76%. Strouhal goes from 0.16428 to 0.16632, which is 1.23%. Both are below the 3% tolerance, so there is no FAIL.
  - The change from R0 to R1 mixes spatial and temporal effects. R1 time_step_convective_units is 0.0061329, against 0.01 for R0, so the time step was reduced along with the mesh. The assumed p=2 therefore cannot be checked.
  - A third mesh level would give an observed convergence order, replacing the assumed p=2. The Strouhal estimate of 0.0491 is about four times the measured change of 1.23%, so the observed order could bring it below 0.015 or confirm it is too large.
  - REFINE_MESH from R1 is not allowed because cumulative refinement 2.83 exceeds the limit of 2.0. REFINE_MESH from R0 with factor 1.4142 is allowed. It sits geometrically between R0 and R1, and R0, the new run and R1 together form a three-level family.
  - Time and domain are still unmeasured for both quantities. They are the next priorities. EXPAND_DOMAIN on R0 costs 1311 s and REDUCE_TIME_STEP on R0 costs 1974 s. Budget used is 1 of 6 experiments and 3.48 of 12.0 relative compute.
  - The menu estimate of 2284 s for REFINE_MESH from R0 was far below the recorded R1 cost of 13751 s. Menu cost estimates may be unreliable, so remaining compute should be watched.
  - Requested: REFINE_MESH {'factor': 1.4142} on E1_noslip_side_walls-88a7cd5812e8 — Mesh is the only component with an estimate above its 0.015 half-tolerance: drag 0.03044 and Strouhal 0.0491, from a two-level Richardson with assumed p=2. R1 cannot be refined further (cumulative refinement limit 2.0). An intermediate level between R0 and R1 gives three levels, so the order can be observed and not assumed. It also separates spatial error from the time-step change that came with R1.
  - Outcome: executed -> E1_noslip_side_walls.m1.41-f15d7e2db685 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and no FAIL justifies REJECT.
  - Mesh drag is now measured on R0, R2 and R1: uncertainty 0.01143, observed order p=2.57, root-to-finest change 0.761%. This passes. Drag is 1.3402 (R0), 1.3475 (R2), 1.3505 (R1), which is monotonic.
  - Strouhal mesh is still INCONCLUSIVE: 0.0212 against a half-tolerance of 0.015, observed order p=1.84. The values are monotonic (0.16428, 0.16562, 0.16632). The demonstrated change is 1.23%, below the 3% tolerance, so there is no FAIL.
  - Time uncertainty is unmeasured for both quantities, and domain uncertainty is unmeasured for both. Both are required for ACCEPT, and neither has been tested. Averaging and statistics are small and pass (drag 9.319e-05 and 0.001199; Strouhal 6.507e-05 and 0.0009705). R0 has 13 stationary cycles, so RUN_LONGER adds little.
  - Domain is the largest untested physical risk. The lateral boundary is noSlipWall at half_height_D 40.0, and blockage is 0.0125. The inlet pressure is zeroGradient and the outlet pressure is fixedValue. A wall-bounded stream is not the 'unbounded' stream the question asks for, and nothing has measured the effect.
  - Time is less likely to dominate. R0 has 608.73 steps per shedding period and max Courant 0.73374, and the scheme is backward in time. It is still unmeasured and is the next candidate after domain.
  - EXPAND_DOMAIN on R0 is the cheapest menu entry, with an estimate of 1311 s. Budget used is 2 of 6 experiments and 4.71 of 12.0 relative compute. The earlier REFINE_MESH estimate was far below the recorded R1 cost, so I treat the menu costs as lower bounds.
  - The parent is R0, the root, so the verifier compares the result directly against the root quantities. R1 is not allowed as a parent, and R2 costs more (3034 s).
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Domain truncation and wall blockage are completely unmeasured for both quantities. The lateral boundary is a noSlipWall at half_height_D 40.0 and the problem requires an unbounded stream. EXPAND_DOMAIN is the cheapest menu entry on R0 (estimate 1311 s). It leaves the near-field mesh unchanged, so any change is attributable to the boundaries.
  - Outcome: executed -> E1_noslip_side_walls.D2x-1620b1098386 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - Averaging and statistics pass for both quantities. Drag: 9.319e-05 and 0.001199. Strouhal: 6.507e-05 and 0.0009705. R0 has 13 stationary cycles, so RUN_LONGER adds little.
  - Drag mesh passes (0.01143, observed p=2.57). Drag is 1.3402 (R0), 1.3475 (R2), 1.3505 (R1), which is monotonic. Strouhal mesh is INCONCLUSIVE: 0.0212 against a half-tolerance of 0.015, p=1.84. The demonstrated change of 1.23% is below the 3% tolerance.
  - Domain is now measured but unresolved. R3 (domain 2x R0) gives drag 1.3259 against 1.3402 for R0, a change of 1.08%. It gives Strouhal 0.16301 against 0.16428, a change of 0.78%. Both are below 3%, so there is no FAIL.
  - The domain uncertainty is 0.0647 for drag and 0.04674 for Strouhal. Both come from a two-level Richardson with assumed p=1 and Fs=3, so they are dominated by the assumed order and safety factor. They exceed the 0.015 half-tolerance and are the largest components.
  - R3 reports checkMesh_ok false. Its far-field mesh is also coarser than R0: representative_cell_size_D is 0.79405 against 0.45745 and wake_last_cell_D is 1.9729 against 1.0209. The R0-to-R3 change may therefore mix domain and mesh effects, and the measured domain trend is not clean.
  - A third domain size between R0 and R3 gives a three-level family with an observed order. EXPAND_DOMAIN on R0 with factor 1.5 gives domain scales 1, 1.5 and 2 with near-constant ratios. It is the cheapest option (estimate 1311 s).
  - Time uncertainty is still unmeasured for both quantities. It is required for ACCEPT and is the next priority. Budget used is 3 of 6 experiments and 5.42 of 12.0 relative compute, so the domain run and the time-step run both fit. Menu cost estimates have been lower than recorded costs, so I treat them as lower bounds.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on E1_noslip_side_walls-88a7cd5812e8 — Domain is the largest uncertainty component: 0.0647 for drag and 0.04674 for Strouhal, both from a two-level estimate with assumed order p=1 and Fs=3. R3 gives only two domain levels, and its checkMesh_ok is false. A run at 1.5x R0 gives a three-level family (1, 1.5, 2) with an observed order. It is the cheapest menu entry on R0 and keeps the near-field mesh unchanged.
  - Outcome: executed -> E1_noslip_side_walls.D1.5x-f702a7c7fa9d (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT is not justified because no FAIL has been measured.
  - Time uncertainty is unmeasured for both mean_drag_coefficient and strouhal_number, because no REDUCE_TIME_STEP run exists. The verifier lists 'time' as missing for both quantities, so ACCEPT is impossible until it is measured.
  - Averaging and statistics pass on R0. Drag has 9.319e-05 and 0.001199. Strouhal has 6.507e-05 and 0.0009705. R0 has 13 stationary cycles, so RUN_LONGER would add little.
  - Drag mesh passes (0.01143, observed p=2.57). Drag is 1.3402 (R0), 1.3475 (R2) and 1.3505 (R1), which is monotonic.
  - Strouhal mesh is INCONCLUSIVE (0.0212 against a half-tolerance of 0.015, p=1.84). Values are 0.16428 (R0), 0.16562 (R2) and 0.16632 (R1), and the demonstrated change of 1.23% is below 3%.
  - Domain now has a three-level family (R0, R4, R3) and is still INCONCLUSIVE. Drag is 1.3402, 1.3302 and 1.3259 (uncertainty 0.02135, p=1.46, demonstrated change 1.08%). Strouhal is 0.16428, 0.16338 and 0.16301 (uncertainty 0.01505, p=1.51, demonstrated change 0.78%). Both trends are monotonic and the changes are below 3%, so there is no FAIL.
  - The R1 and R2 time steps differ from R0 (0.0061329 and 0.0086733 against 0.01). The mesh estimates, especially for Strouhal, therefore mix spatial and temporal effects. R3 also has checkMesh_ok false and a coarser far field (wake_last_cell_D 1.9729 against 1.0209), so the domain estimate is partly confounded by mesh.
  - A REDUCE_TIME_STEP run on R0 is the only experiment that fills a missing component. It also separates temporal error from the mesh trend. R0 has 608.73 steps per period and max Courant 0.73374, so the time error may be small, but it is unmeasured and gates ACCEPT.
  - Budget used is 4 of 6 experiments and 6.05 of 12.0 relative compute. The REDUCE_TIME_STEP estimate on R0 is 1974 s, so it fits. One further experiment would remain afterwards. Menu estimates have been lower than recorded costs (R1), so I treat them as lower bounds.
  - The parent is R0, the root, so the verifier compares the result directly with the submitted quantities. R1 would cost 12876 s and is unaffordable.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Time uncertainty is the only component unmeasured for both quantities, and the verifier cannot return ACCEPT without it. A run on R0 at fixed mesh isolates temporal error and tests whether the time-step changes in R1 and R2 confound the mesh trend. It is affordable (estimate 1974 s) within the remaining budget of 2 experiments and 5.95 relative compute.
  - Outcome: executed -> E1_noslip_side_walls.dt0.005-c41af2c90410 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 5.95

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. No demonstrated change exceeds the 0.03 tolerance, so REJECT is not justified.
  - Time is now measured. R5 (dt 0.005) gives drag 1.3374 and Strouhal 0.1645, against R0 at 1.3402 and 0.16428. Time uncertainty is 0.008342 for drag and 0.005466 for Strouhal, both PASS.
  - Time-step confounding of the mesh trend is small. Halving dt on R0 moves Strouhal by only 0.137%, while R0 to R1 moves it by 1.23%. The Strouhal mesh trend is therefore mainly spatial.
  - Averaging and statistics pass for both quantities. Drag has 9.319e-05 and 0.001199. Strouhal has 6.507e-05 and 0.0009705. R0 has 13 stationary cycles, so RUN_LONGER adds little.
  - Drag mesh passes at 0.01143 (p=2.57). Strouhal mesh is INCONCLUSIVE at 0.0212 against the 0.015 half-tolerance (p=1.84). Strouhal values are 0.16428 (R0), 0.16562 (R2) and 0.16632 (R1), monotonic, with a demonstrated change of 1.23%.
  - Domain is INCONCLUSIVE for both quantities. Drag is 0.02135 (p=1.46, change 1.08%). Strouhal is 0.01505 (p=1.51, change 0.78%). Values are monotonic: drag 1.3402, 1.3302, 1.3259 and Strouhal 0.16428, 0.16338, 0.16301 for R0, R4, R3.
  - Domain is the only component that is over budget for drag and also over budget for Strouhal. The trend is still moving at the largest domain (R3, 2x). R3 also has checkMesh_ok false and a coarser far field, so its signal is partly confounded by mesh.
  - R1 cannot be refined further (cumulative refinement limit). Strouhal mesh uncertainty cannot be closed with the one remaining experiment, so ACCEPT is unlikely. A domain run still attacks the largest drag term and the Strouhal domain term.
  - Budget: 5 of 6 experiments and 7.12 of 12.0 relative compute are used, which leaves about 4.88 times the root cost. EXPAND_DOMAIN on R0 is the cheapest menu entry (estimate 1311 s). It fits, and the menu estimates have run below recorded costs, so I treat them as lower bounds.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on E1_noslip_side_walls-88a7cd5812e8 — Domain is the largest drag component (0.02135) and sits just over the half-tolerance for Strouhal (0.01505). Both domain terms are over budget, and the trends in R4 and R3 are still moving. A 3.0x domain extends the sequence beyond R3 (2x) and tests whether it is converging. It keeps the near-field mesh unchanged and uses root R0 as the parent, so the verifier compares directly with the submitted quantities. It is among the cheapest entries and fits the remaining compute.
  - Outcome: executed -> E1_noslip_side_walls.D3x-5e6cfbc7fe84 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 4.88

Run E1_noslip_side_walls.m2-39a4571e43e5: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3505 (+0.77%).
  - Observation: strouhal_number 0.16428 → 0.16632 (+1.24%).

Run E1_noslip_side_walls.m1.41-f15d7e2db685: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3475 (+0.55%).
  - Observation: strouhal_number 0.16428 → 0.16562 (+0.82%).

Run E1_noslip_side_walls.D2x-1620b1098386: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3259 (-1.07%).
  - Observation: strouhal_number 0.16428 → 0.16301 (-0.77%).

Run E1_noslip_side_walls.D1.5x-f702a7c7fa9d: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3302 (-0.75%).
  - Observation: strouhal_number 0.16428 → 0.16338 (-0.55%).

Run E1_noslip_side_walls.dt0.005-c41af2c90410: REDUCE_TIME_STEP from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3374 (-0.21%).
  - Observation: strouhal_number 0.16428 → 0.1645 (+0.14%).

Run E1_noslip_side_walls.D3x-5e6cfbc7fe84: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3216 (-1.39%).
  - Observation: strouhal_number 0.16428 → 0.16263 (-1.01%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `E1_noslip_side_walls-88a7cd5812e8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1851 s; record: results/runs/E1_noslip_side_walls-88a7cd5812e8/run.json
- `E1_noslip_side_walls.m2-39a4571e43e5` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:09:25+00:00 wall=1.375e+04 s; record: results/runs/E1_noslip_side_walls.m2-39a4571e43e5/run.json
- `E1_noslip_side_walls.m1.41-f15d7e2db685` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:08:43+00:00 wall=2302 s; record: results/runs/E1_noslip_side_walls.m1.41-f15d7e2db685/run.json
- `E1_noslip_side_walls.D2x-1620b1098386` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T20:14:34+00:00 wall=1058 s; record: results/runs/E1_noslip_side_walls.D2x-1620b1098386/run.json
- `E1_noslip_side_walls.D1.5x-f702a7c7fa9d` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T02:45:52+00:00 wall=862.7 s; record: results/runs/E1_noslip_side_walls.D1.5x-f702a7c7fa9d/run.json
- `E1_noslip_side_walls.dt0.005-c41af2c90410` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T01:16:41+00:00 wall=1163 s; record: results/runs/E1_noslip_side_walls.dt0.005-c41af2c90410/run.json
- `E1_noslip_side_walls.D3x-5e6cfbc7fe84` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T15:55:56+00:00 wall=1707 s; record: results/runs/E1_noslip_side_walls.D3x-5e6cfbc7fe84/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3646942064.0, "relative_to_root": 7.950604020056682, "experiment_wall_seconds": 20843.660896770998, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.57818276, "loop_wall_seconds": 1871.7603699149986}
