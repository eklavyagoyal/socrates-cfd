# Verification report: K1_central_scheme (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3404
- strouhal_number: 0.16329

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linear' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.33e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.22e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 6.48% > 1.50% but the demonstrated change 0.23% <= tau; more refinement would be needed [three-level, observed order 0.16 outside [0.5, 2.0]x formal; p=min(observed, formal)=0.16 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.26% <= 1.50% (root-to-finest change 0.817%) [three-level Celik procedure, observed order p=2.37, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.91% <= 1.50% (root-to-finest change 0.228%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.3e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.48% <= 1.50% (root-to-finest change 0.120%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.58% > 1.50% but the demonstrated change 0.91% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.16, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.79% > 1.50% but the demonstrated change 0.52% <= tau; more refinement would be needed [three-level, observed order 3.28 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=7.04e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000133
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0648
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-f0705353471c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00913
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0158
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D3x-14d3dc15d928

CLAIM: strouhal_number of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=1.32e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000122
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): PASS U=0.0126
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-f0705353471c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00478
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0179
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D3x-14d3dc15d928

```

## EXPERIMENT HISTORY

Run K1_central_scheme-e4e5fb66bdca: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. Mesh, time and domain uncertainty are all unmeasured for both mean_drag_coefficient and strouhal_number, so ACCEPT is not allowed. REJECT is not justified because nothing has failed.
  - R0 averaging and statistics components are measured and tiny. For drag they are 7.04e-05 and 0.0001331. For Strouhal they are 1.316e-05 and 0.000122. The stationary window has 12 cycles and drag drift_rel is -0.00013306. The 3% tolerance is therefore not limited by sampling, and RUN_LONGER would add little.
  - R0 mesh is the least resolved element. It has 30580 cells, a representative cell size of 0.45745 D, and 160 cells around the cylinder. The wake has 111 streamwise cells with a last cell of 1.0209 D. The scheme is Gauss linear, which has no numerical dissipation. A coarse wake could shift shedding frequency and drag by more than the 3% tolerance. That makes mesh the most likely source of an error larger than tolerance.
  - R0 time step is 0.01 D/U with backward differencing and max Courant 0.73638. This gives 612.39 steps per shedding period, which is well resolved. Temporal error is less likely to dominate than spatial error.
  - R0 domain extents are 30 D upstream, 50 D downstream and 40 D half-height, with a blockage ratio of 0.0125 and symmetryPlane lateral boundaries. The domain is moderately large. Its error is unmeasured but probably smaller than the mesh error, and EXPAND_DOMAIN is cheaper (2899 s) and can follow later.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 compute units used. REFINE_MESH at the default factor costs about 5070 s, roughly 1.24 times the root cost.
  - Requested: REFINE_MESH {'factor': 1.4142} on K1_central_scheme-e4e5fb66bdca — Mesh resolution is the most likely source of an error larger than 3%: the wake is coarse and the scheme is non-dissipative central differencing. Time step and domain look comparatively adequate. A single systematic refinement exposes any dominant spatial error for both quantities.
  - Outcome: executed -> K1_central_scheme.m1.41-9a011a4052fe (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.24

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because the time and domain components are unmeasured for both quantities. The Strouhal mesh component is also unresolved. REJECT is not justified because nothing has failed.
  - The R0 to R1 mesh refinement changed mean drag from 1.3403 to 1.3388, a 0.117% change. The mesh uncertainty is 0.006993, which is within budget. The drag mesh component passes.
  - The Strouhal number changed from 0.1633 (R0) to 0.16423 (R1), a 0.57% change. The two-level Richardson estimate with assumed order p=2 and Fs=3 gives 3.42%, which is above 1.5%. This is an estimate-limited INCONCLUSIVE. It is not a demonstrated failure.
  - Sampling is not limiting. R0 has 12 stationary cycles and a drag CI95 of 3.62e-05. R1 has 7 cycles and a drag CI95 of 2.3805e-05. RUN_LONGER would add little.
  - R0 uses a time step of 0.01 D/U, backward differencing, 612.39 steps per shedding period and max Courant 0.73638. R1 used a smaller step of 0.0086422, so the R0-to-R1 change mixes spatial and temporal effects. The temporal error is plausibly small, but it is unmeasured.
  - The domain is the cheapest unmeasured component (2899 s from R0, about 0.71x the root cost). It has not been tested. The setup has symmetryPlane lateral boundaries at 40 D, a 30 D inlet, a 50 D outlet, a fixedValue outlet pressure and a zeroGradient inlet pressure. The spec says to treat the stream as unbounded, so truncation error must be measured. If it exceeds tolerance, the verifier will record a FAIL cheaply and early.
  - Budget is ample. 1 of 6 experiments and 1.24 of 12 compute units are used. The domain, time-step and R1-parent mesh runs (about 0.71, 1.07 and 2.84 root-costs) all fit in the remaining budget.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — The domain component is unmeasured for both quantities and is the cheapest experiment (2899 s). It can expose a boundary-truncation flaw larger than the 3% tolerance, which would give an early FAIL and avoid the more expensive R1-parent refinement. R0 is the root and has the best-sampled record (12 cycles), so it is the right comparison parent.
  - Outcome: executed -> K1_central_scheme.D2x-b0a7ed20bbb5 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 0.71, 0.71, 1.07, 2.84

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not justified because nothing has failed.
  - Averaging and statistics pass for both quantities. Drag averaging is 7.04e-05 and statistics is 0.0001331. Strouhal averaging is 1.316e-05 and statistics is 0.000122. R0 has 12 stationary cycles. RUN_LONGER would add little.
  - Drag mesh passes at 0.006993. The R0 to R1 drag change is 1.3403 to 1.3388. Strouhal mesh is INCONCLUSIVE at 0.03415. The Strouhal change is 0.1633 to 0.16423, and the estimate rests on an assumed order p=2.
  - The domain component is the largest unresolved item for drag at 0.04162 and for Strouhal at 0.02852. Both are above the 3% tolerance and rest on an assumed order p=1. R2 doubled the domain, and drag moved from 1.3403 to 1.3311 and Strouhal from 0.1633 to 0.16252. Both changes are inside tolerance, but a two-level estimate cannot confirm that.
  - R2 is a weak comparator. Its checkMesh_ok is false. Its far-field mesh is coarser (representative size 0.79405 D, wake last cell 1.9729 D). It has only 6 cycles, a drag CI95 of 0.00082395 and a drag drift_rel of -0.001767. The domain effect is therefore confounded with far-field resolution and sampling noise.
  - Time-step error is unmeasured for both quantities. R0 uses 0.01 D/U, backward differencing, 612.39 steps per period and max Courant 0.73638. This looks well resolved, so it is less likely than domain to exceed tolerance. It is still required for ACCEPT.
  - Budget allows more work. 2 of 6 experiments and 1.95 of 12 compute units are used. A larger domain run fits easily. REDUCE_TIME_STEP on R0 (4367 s) and REFINE_MESH on R1 (11642 s) can follow.
  - Next experiment: EXPAND_DOMAIN on R0 with factor 3.0. I choose R0 as parent because R0 passes checkMesh and has the best-sampled record. This avoids inheriting the R2 mesh failure. It also gives a third domain level (R0, R2, new run) for an observed convergence order.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on K1_central_scheme-e4e5fb66bdca — Domain is the largest unresolved uncertainty for both quantities (drag 0.04162, Strouhal 0.02852, both above tolerance and from an assumed order p=1). The only domain comparison, R2, is confounded by a coarser far-field mesh, checkMesh_ok false and only 6 cycles. A larger domain from the root R0 gives a third domain level for an observed trend. It does so without inheriting the R2 mesh problem. It is cheaper than any refinement from R1.
  - Outcome: executed -> K1_central_scheme.D3x-14d3dc15d928 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed because components are unmeasured. REJECT is not justified because nothing has failed.
  - Averaging and statistics pass for both quantities. Drag values are 7.04e-05 and 0.0001331. Strouhal values are 1.316e-05 and 0.000122. R0 has 12 stationary cycles, a drag CI95 of 3.62e-05 and a drag drift_rel of -0.00013306. RUN_LONGER would add little.
  - The drag mesh component passes at 0.006993 (R0 1.3403 to R1 1.3388). The Strouhal mesh component is INCONCLUSIVE at 0.03415 (R0 0.1633 to R1 0.16423, a 0.57% change). That estimate rests on an assumed order p=2 and Fs=3.
  - The domain component is now a three-level estimate (R0, R2, R3). Drag is 0.01575 and Strouhal is 0.0179. Both are only marginally above the 1.5% half-tolerance. The verifier records demonstrated changes of 0.91% (drag) and 0.52% (Strouhal), both below the 3% tolerance. The drag trend from R0 to R2 to R3 is 1.3403, 1.3311, 1.3283. R2 and R3 have checkMesh_ok false and only 6 cycles each, so their domain estimate is confounded.
  - The time component is entirely unmeasured for both quantities (no REDUCE_TIME_STEP run). It is required for ACCEPT. It is the only component for which the verifier has no number at all, so it could still hide an error above tolerance.
  - R0 uses 0.01 D/U with backward differencing, 612.39 steps per period and max Courant 0.73638. The R0-to-R1 change mixes spatial and temporal effects because R1 used 0.0086422. A pure time-step test on R0 is therefore needed to separate them.
  - EXPAND_DOMAIN from R3 is not allowed (cumulative factor limit 4.0). A further domain run would have to come from R2 and would add a fourth level of already confounded runs.
  - Budget: 3 of 6 experiments and 2.78 of 12 root-cost units are used. REDUCE_TIME_STEP on R0 costs 4367 s. REFINE_MESH on R1 (11642 s) and a domain run from R2 (3746 s) should still fit afterwards.
  - I chose R0 as parent because it is the root, passes checkMesh and has the best-sampled record (12 cycles).
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — The time component is the only one with no measurement for either quantity. It blocks ACCEPT and could expose an error above tolerance. A pure time-step test on R0 is cheap (4367 s) and separates temporal from spatial effects, which R1 mixed because its step differs. Further domain expansion from R3 is not allowed, and the R1 mesh refinement is expensive (11642 s), so time is the best next experiment.
  - Outcome: executed -> K1_central_scheme.dt0.005-4f460bac38b7 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed because components are unmeasured. REJECT is not justified because no FAIL is recorded.
  - Averaging and statistics pass for both quantities. Drag values are 7.04e-05 and 0.0001331. Strouhal values are 1.316e-05 and 0.000122. R0 has 12 stationary cycles and a drag CI95 of 3.62e-05. RUN_LONGER would add little.
  - The time component now passes. It is 0.009131 for drag and 0.004782 for Strouhal. The R0 to R4 changes are 1.3403 to 1.3373 for drag and 0.1633 to 0.16349 for Strouhal.
  - The drag mesh component passes at 0.006993. The R0 to R1 change is 1.3403 to 1.3388.
  - The Strouhal mesh component is INCONCLUSIVE at 0.03415, which is above the 0.03 tolerance. It comes from a two-level Richardson estimate with assumed order p=2 and Fs=3. The demonstrated R0 to R1 change is only 0.57% (0.1633 to 0.16423). A third mesh level would replace the assumed order with a measured one. This is the largest unresolved component.
  - The domain component is INCONCLUSIVE for both quantities. Drag is 0.01575 and Strouhal is 0.0179, both just above 0.015. The demonstrated changes are 0.91% (drag) and 0.52% (Strouhal). The R0, R2, R3 drag trend is 1.3403, 1.3311, 1.3283. The shifts shrink, but R2 and R3 have checkMesh_ok false and only 6 cycles each, so the estimate is confounded by far-field coarsening and sampling.
  - R4 shows that the time step affects the answer. R1 used a smaller step (0.0086422) than R0 (0.01), so the R0 to R1 mesh change includes some temporal effect. A refinement parented on R1 continues the refinement family and gives three levels (R0, R1, new) for an observed order.
  - Budget: 4 of 6 experiments and 3.84 of 12 root-cost units are used. REFINE_MESH on R1 costs 11642 s, about 2.84 root units. That leaves 1 experiment and about 5.3 units, enough for an EXPAND_DOMAIN run on R2 (3746 s) afterwards.
  - Requested: REFINE_MESH {'factor': 1.4142} on K1_central_scheme.m1.41-9a011a4052fe — Strouhal mesh is the largest unresolved component at 0.03415, above the 0.03 tolerance, and rests on an assumed order. Continuing the refinement family from R1 gives three mesh levels (R0, R1, new) and a measured order. Drag mesh already passes, so this mainly targets Strouhal. The remaining budget still allows a domain run from R2 afterwards.
  - Outcome: executed -> K1_central_scheme.m2-f0705353471c (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 2.84

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not justified because no FAIL is recorded.
  - Averaging, statistics and time pass for both quantities. Drag: averaging 7.04e-05, statistics 0.0001331, time 0.009131. Strouhal: averaging 1.316e-05, statistics 0.000122, time 0.004782. RUN_LONGER would add little. R0 has 12 stationary cycles and a drag CI95 of 3.62e-05.
  - The Strouhal mesh component now passes at 0.01264 (R0, R1, R5, observed p=2.37). Strouhal is therefore blocked only by domain (0.0179, above 0.015).
  - Drag mesh is INCONCLUSIVE at 0.06483 (observed p=0.16, Fs=3). The demonstrated drag change is only 0.23%. The drag values are R0 1.3403, R1 1.3388 and R5 1.3373. These are almost equal steps, which produce the very low observed order.
  - The mesh levels also differ in time step. R0 used 0.01, R1 used 0.0086422 and R5 used 0.0075022. On the unchanged R0 mesh, R4 (dt 0.005) gave 1.3373. R5 (finer mesh, dt 0.0075022) also gave 1.3373. So the near-constant drag steps may be driven by the time step and not by the mesh. The verifier's mesh check does not separate the two effects.
  - Domain is INCONCLUSIVE for both quantities (drag 0.01575, Strouhal 0.0179). Both are marginally above 0.015, and the demonstrated changes are 0.91% and 0.52%. R2 and R3 have checkMesh_ok false and only 6 cycles each. R2 drag drift_rel is -0.001767 and R3's is -0.0029789.
  - Budget: 5 of 6 experiments are used, so exactly one remains. About 5.31 root-cost units of compute remain (6.69 of 12 used). REDUCE_TIME_STEP on R5 (23284 s) is unaffordable. REFINE_MESH on R5 and EXPAND_DOMAIN on R3 are not allowed. A domain run from R2 costs 3746 s but would add another run with a coarse far-field mesh and few cycles.
  - The most informative remaining experiment is REDUCE_TIME_STEP on R1. It uses a dt close to R4's 0.005. R4 and the new run would then be a mesh pair (R0 mesh and R1 mesh) at nearly matched dt. This tests whether the drag mesh sensitivity is real or a time-step artefact. It costs about 10140 s at factor 2, which fits the budget.
  - Requested: REDUCE_TIME_STEP {'factor': 1.7284} on K1_central_scheme.m1.41-9a011a4052fe — Drag mesh is the largest unresolved component (0.06483, observed p=0.16). R0, R1 and R5 differ in time step, so the mesh and time effects are confounded. R4 (dt 0.005, R0 mesh) and R5 (finer mesh, dt 0.0075022) both give drag 1.3373. Reducing R1's dt to about 0.005 gives a mesh pair with R4 at matched dt. It fits the remaining budget (about 10140 s at factor 2, and less at 1.7284).
  - Outcome: executed -> K1_central_scheme.dt0.005-5fad5168407b (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 5.31, 1.7284

Run K1_central_scheme.m1.41-9a011a4052fe: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008642, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3388 (-0.12%).
  - Observation: strouhal_number 0.1633 → 0.16423 (+0.57%).

Run K1_central_scheme.D2x-b0a7ed20bbb5: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3311 (-0.69%).
  - Observation: strouhal_number 0.1633 → 0.16252 (-0.47%).

Run K1_central_scheme.D3x-14d3dc15d928: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3283 (-0.90%).
  - Observation: strouhal_number 0.1633 → 0.16246 (-0.51%).

Run K1_central_scheme.dt0.005-4f460bac38b7: REDUCE_TIME_STEP from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3373 (-0.23%).
  - Observation: strouhal_number 0.1633 → 0.16349 (+0.12%).

Run K1_central_scheme.m2-f0705353471c: REFINE_MESH from K1_central_scheme.m1.41-9a011a4052fe (mesh.refinement: 1.414→2, time.delta_t: 0.008642→0.007502).
  - Observation: mean_drag_coefficient 1.3388 → 1.3373 (-0.11%).
  - Observation: strouhal_number 0.16423 → 0.16464 (+0.25%).

Run K1_central_scheme.dt0.005-5fad5168407b: REDUCE_TIME_STEP from K1_central_scheme.m1.41-9a011a4052fe (time.delta_t: 0.008642→0.005001).
  - Observation: mean_drag_coefficient 1.3388 → 1.3371 (-0.13%).
  - Observation: strouhal_number 0.16423 → 0.16429 (+0.04%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K1_central_scheme-e4e5fb66bdca` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=4094 s; record: results/runs/K1_central_scheme-e4e5fb66bdca/run.json
- `K1_central_scheme.m1.41-9a011a4052fe` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T09:33:11+00:00 wall=3361 s; record: results/runs/K1_central_scheme.m1.41-9a011a4052fe/run.json
- `K1_central_scheme.D2x-b0a7ed20bbb5` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T16:16:09+00:00 wall=988.1 s; record: results/runs/K1_central_scheme.D2x-b0a7ed20bbb5/run.json
- `K1_central_scheme.D3x-14d3dc15d928` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T08:01:33+00:00 wall=1665 s; record: results/runs/K1_central_scheme.D3x-14d3dc15d928/run.json
- `K1_central_scheme.dt0.005-4f460bac38b7` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T03:41:02+00:00 wall=1455 s; record: results/runs/K1_central_scheme.dt0.005-4f460bac38b7/run.json
- `K1_central_scheme.m2-f0705353471c` status=completed parent=K1_central_scheme.m1.41-9a011a4052fe created=2026-10-20T01:15:34+00:00 wall=4868 s; record: results/runs/K1_central_scheme.m2-f0705353471c/run.json
- `K1_central_scheme.dt0.005-5fad5168407b` status=completed parent=K1_central_scheme.m1.41-9a011a4052fe created=2026-10-20T14:14:26+00:00 wall=4570 s; record: results/runs/K1_central_scheme.dt0.005-5fad5168407b/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 4048560078.0, "relative_to_root": 8.826161059516023, "experiment_wall_seconds": 16907.761387531988, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.613594325, "loop_wall_seconds": 4733.633871093007}
