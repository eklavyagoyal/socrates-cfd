# Verification report: A2_moderate_mesh (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3221
- strouhal_number: 0.16157

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.56 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.004% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 7.17e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 5.21e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.30% <= 1.50% (root-to-finest change 0.958%) [three-level Celik procedure, observed order p=3.58, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.75% > 1.50% but the demonstrated change 1.80% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.43, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.17% <= 1.50% (root-to-finest change 0.292%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.36% <= 1.50% (root-to-finest change 0.090%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.4e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.39% > 1.50% but the demonstrated change 0.97% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.66, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.38% <= 1.50% (root-to-finest change 0.643%) [three-level Celik procedure, observed order p=0.80, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=4.43e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Temporal statistics (stationarity, cycles): PASS U=7.17e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Spatial discretisation (mesh sensitivity): PASS U=0.013
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-773c4ec70534
├── Temporal discretisation (time-step sensitivity): PASS U=0.0117
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0239
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.long180-555e22f6f9da

CLAIM: strouhal_number of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=8.52e-06
│   └── A2_moderate_mesh-1c5ea01594aa
├── Temporal statistics (stationarity, cycles): PASS U=5.21e-05
│   └── A2_moderate_mesh-1c5ea01594aa
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0275
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-773c4ec70534
├── Temporal discretisation (time-step sensitivity): PASS U=0.00362
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): PASS U=0.0138
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.long180-555e22f6f9da

```

## EXPERIMENT HISTORY

Run A2_moderate_mesh-1c5ea01594aa: submitted simulation (17162 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT has no measured FAIL to rest on.
  - R0 averaging and statistics components pass for both quantities. Drag: averaging 4.434e-05, statistics 7.165e-05. Strouhal: averaging 8.516e-06, statistics 5.21e-05. The stationary window has 12 cycles.
  - Mesh, time and domain components are all unmeasured, because no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists. The budget rule needs a measured value for each component.
  - R0 is coarse for a shedding wake. Representative cell size is 0.61063 D, the wake has 83 streamwise cells, and the last wake cell is 1.3639 D. The mesh has 17162 cells with 120 around the cylinder. Spatial error is the component most likely to exceed 0.5*tolerance (0.015) for drag and Strouhal.
  - Time and domain look less suspect on the recorded configuration. Time: dt is 0.01 convective units, max Courant is 0.56482, there are 618.93 steps per period, and the scheme is backward. Domain: blockage is 0.0125, with 30 D upstream, 50 D downstream and 40 D half-height. These two are lower priority, but still unmeasured.
  - The first experiment is REFINE_MESH from R0 at factor 2.0. The larger factor gives a clearer signal against the 0.03 tolerance. Its cost is within the 12x-root compute budget (R0 cost 2124 s, default-factor estimate 2266 s).
  - Requested: REFINE_MESH {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Mesh error is the largest unmeasured component. R0 is coarse for resolving the shedding wake, so spatial error is the most likely flaw to move drag or Strouhal by more than the 3% tolerance.
  - Outcome: executed -> A2_moderate_mesh.m1.5-773c4ec70534 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT has no measured FAIL to rest on: the demonstrated R0->R1 changes are 0.96% (drag) and 1.80% (Strouhal), both below the 0.03 tolerance.
  - R0 averaging and statistics pass for both quantities. Drag: averaging 4.434e-05, statistics 7.165e-05. Strouhal: averaging 8.516e-06, statistics 5.21e-05. R0 has 12 stationary cycles.
  - Mesh is the dominant unresolved component. R0->R1 changed drag from 1.3222 to 1.335 and Strouhal from 0.16157 to 0.16454. The two-level Richardson estimate assumed p=2 and gave a root mesh uncertainty of 0.03828 (drag) and 0.07206 (Strouhal). Both exceed the 0.015 component budget (0.5*tolerance) and are not an observed-order result.
  - No further refinement is possible. R1 is not allowed as a refine parent because cumulative refinement 2.83 exceeds the limit of 2.0. A mesh level between R0 and R1 (factor 1.4142 from R0, cumulative 1.41 <= 2.0) is therefore the only way to get three-level data. It would give an observed convergence order instead of an assumed one, and could shrink or confirm the mesh uncertainty.
  - R0 is coarse: 120 cells around the cylinder, representative size 0.61063 D, last wake cell 1.3639 D. R1 has 240 cells around the cylinder and a last wake cell of 0.68337 D. Strouhal moved 1.80% between these meshes, so mesh is the most likely component to push R0 beyond tolerance.
  - Time and domain remain unmeasured, so they are still blocking. They look less suspect on the recorded configuration: R0 has max Courant 0.56482, 618.93 steps per period and blockage ratio 0.0125. Closing them is pointless if the mesh component cannot be closed, so they come after the mesh.
  - Cost is acceptable. The estimate for REFINE_MESH from R0 is 2266 s. Compute used is 2.69 of 12.0 times the root, and 1 of 6 experiments is used.
  - Caveat: R0 strouhal_frequency_resolution is 0.013333 and R1's is 0.025003. Both are larger than the 0.00297 R0-R1 St difference (0.16454 - 0.16157). The recorded St values (including strouhal_number_fft) therefore rest on sub-bin peak estimation. A third mesh level will show whether the St trend is monotone and not noise.
  - Requested: REFINE_MESH {'factor': 1.4142} on A2_moderate_mesh-1c5ea01594aa — Mesh is the only component with a measured estimate above its budget (0.03828 drag, 0.07206 Strouhal vs 0.015). R1 cannot be refined further (cumulative 2.83 > 2.0). An intermediate level from R0 gives three mesh levels, so the order is observed and not assumed, which is the cheapest way to establish whether the root mesh error can be bounded.
  - Outcome: executed -> A2_moderate_mesh.m1.06-c5d153eb41a5 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 0.00297

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT has no measured FAIL to rest on, because the demonstrated mesh changes are 0.958% for drag and 1.80% for Strouhal, both below the 0.03 tolerance.
  - R0 averaging and statistics pass for both quantities. Drag: averaging 4.434e-05, statistics 7.165e-05. Strouhal: averaging 8.516e-06, statistics 5.21e-05. R0 has 12 stationary cycles.
  - The drag mesh component now passes with 0.01305 (three-level Celik, R0/R2/R1, observed p=3.58). It is under the 0.015 budget.
  - The Strouhal mesh component is still INCONCLUSIVE at 0.02755 (observed p=2.43), above 0.015. St is monotone across levels: R0 0.16157, R2 0.16364, R1 0.16454. The monotone trend supports a genuine mesh trend, not frequency-estimation noise. The 1.80% demonstrated change is below tau.
  - Further mesh refinement adds little. R1 is already at the 2.0 cumulative limit. A refinement of R2 would be near-duplicate R1 data. R0 itself cannot become finer.
  - The time and domain components are unmeasured for both quantities and are blocking for both. Neither quantity can be accepted until they are measured, whatever happens to the Strouhal mesh component.
  - EXPAND_DOMAIN is the cheapest of the unmeasured components, with an estimate of 1498 s from R0. The question explicitly requires an unbounded stream. R0 uses symmetryPlane lateral boundaries, a fixedValue outlet pressure, a zeroGradient inlet pressure and a blockage ratio of 0.0125. These boundary choices are the main physical-model assumption not yet tested.
  - Parent R0 is correct, since R0 is the root whose domain error is being bounded. Budget is sufficient: 2 of 6 experiments used and 3.75 of 12.0 compute used.
  - REDUCE_TIME_STEP on R0 is the next priority after this. R0 has dt 0.01, max Courant 0.56482 and 618.93 steps per period. R1 used dt 0.0079672 and R2 used dt 0.01, so the mesh-trend comparison is mildly confounded by the time step.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Domain error is unmeasured for both quantities and blocks both verdicts. The question requires an unbounded stream, and R0 uses finite boundaries with a blockage of 0.0125. This is the cheapest unmeasured component at 1498 s from R0 and tests an untested physical assumption.
  - Outcome: executed -> A2_moderate_mesh.D2x-4a8a18327a27 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. ACCEPT is not allowed. REJECT has no measured FAIL to rest on, because every demonstrated change is below the 0.03 tolerance: drag mesh 0.958%, drag domain 0.69%, Strouhal mesh 1.80%, Strouhal domain 0.47%.
  - R0 averaging and statistics pass for both quantities. Drag: averaging 4.434e-05, statistics 7.165e-05. Strouhal: averaging 8.516e-06, statistics 5.21e-05. R0 has 12 stationary cycles.
  - Drag mesh passes at 0.01305 (three-level Celik on R0/R2/R1, observed p=3.58). Strouhal mesh is still INCONCLUSIVE at 0.02755 (observed p=2.43). The Strouhal values are monotone: R0 0.16157, R2 0.16364, R1 0.16454.
  - Domain uncertainty is the largest open component for both quantities: drag 0.04147 and Strouhal 0.02803. Both exceed the 0.015 budget and the drag value exceeds the 0.03 tolerance. Both come from a two-level Richardson estimate with an assumed order p=1 and Fs=3, not from a measured order. The R0->R3 changes are only 0.69% (drag 1.3222 -> 1.3131) and 0.47% (Strouhal 0.16157 -> 0.16082), so the large uncertainty comes from the assumed order and safety factor.
  - R3 is a weak domain datum. checkMesh_ok is false for R3. Its far-field mesh is coarser (representative size 1.0621 D, last wake cell 2.621 D). Its drag noise is larger: ci95 0.00063061 and drift -0.0013441, against 2.1297e-05 and 7.1653e-05 for R0. The R0->R3 change therefore mixes domain size, far-field mesh and noise. A further domain level, with the near-field mesh unchanged, tests whether the trend is monotone and gives an observed order.
  - Time error is unmeasured for both quantities, and no REDUCE_TIME_STEP run exists. It still blocks both verdicts. It looks less suspect on the recorded configuration: R0 has dt 0.01, max Courant 0.56482, 618.93 steps per period and a backward scheme. It is the next priority after the domain.
  - Budget: 3 of 6 experiments used and 4.46 of 12.0 relative compute used. A domain run from R0 costs about 1498 s at factor 2. A factor-3.0 run adds far-field cells, so its cost is higher than that but still fits the remaining budget. A time-step run would fit too.
  - A fresh EXPAND_DOMAIN from R0 at factor 3.0 gives domain levels of 1x, 2x (R3) and 3x on the same near-field mesh. That allows an observed-order Richardson estimate. Factor 3.0 gives a larger signal than 1.5 against the noise floors (1.3e-3 for drag, 1.2e-3 for Strouhal). Choosing R0 as parent keeps the comparison clean of R3's failed checkMesh.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on A2_moderate_mesh-1c5ea01594aa — Domain is the largest open uncertainty component (drag 0.04147, Strouhal 0.02803), and it rests on an assumed order p=1 from only R0 and R3. R3 also failed checkMesh and has a coarser far field. A 3x domain from R0 adds a third level on the same near-field mesh, so the order is observed and not assumed. This is the most direct way to bound the domain error that the unbounded-stream requirement depends on.
  - Outcome: executed -> A2_moderate_mesh.D3x-912cd516504f (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT has no measured FAIL to rest on.
  - Drag now has averaging 4.434e-05, statistics 7.165e-05, mesh 0.01305 (p=3.58) and domain 0.01267 (R0/R3/R4), all PASS. The only missing drag component is time. No REDUCE_TIME_STEP run exists.
  - Strouhal has averaging 8.516e-06 and statistics 5.21e-05 (PASS). Mesh (0.02755) and domain (0.02075) are INCONCLUSIVE because they are above 0.015 but the demonstrated changes are within tolerance. Time is missing.
  - Strouhal values are monotone in mesh (R0 0.16157, R2 0.16364, R1 0.16454) and in domain (R0 0.16157, R3 0.16082, R4 0.1607). The demonstrated changes are 1.80% (mesh) and 0.54% (domain), both below 0.03.
  - Time is the only component that blocks both quantities and has no measurement at all. Every other component has at least one measured estimate. Until time is measured, neither quantity can reach a combined uncertainty.
  - R0 uses dt=0.01 convective units, max Courant 0.56482 and 618.93 steps per period. Mesh runs used different time steps: R1 had dt=0.0079672 and R2 had dt=0.01. So the mesh trend is mildly confounded by the time step, and a time-step run checks this.
  - R3 and R4 have checkMesh_ok false and a coarser far field. This limits how much a further domain run adds, and the drag domain component already passes.
  - Cost: REDUCE_TIME_STEP from R0 is estimated at 2266 s. Used so far are 4 of 6 experiments and 5.29 of 12.0 relative compute, so this fits. One experiment would remain afterwards.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Time is the only unmeasured component for drag, and it also blocks Strouhal. It is the only component with no estimate at all. Drag mesh and domain pass and Strouhal mesh and domain have measured, if inconclusive, estimates. The cost of 2266 s fits the remaining budget.
  - Outcome: executed -> A2_moderate_mesh.dt0.005-4720e4eddcde (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT has no measured FAIL to rest on, because every demonstrated change is below the 0.03 tolerance.
  - Drag is ACCEPT per quantity, with combined uncertainty 0.02166. Components: averaging 4.434e-05, statistics 7.165e-05, mesh 0.01305, time 0.01168, domain 0.01267. Strouhal is INCONCLUSIVE because mesh (0.02755) and domain (0.02075) are above the 0.015 component budget. Its time component passes at 0.003615.
  - R5 closed the time component for both quantities. Drag changed from 1.3222 (R0) to 1.3183 (R5) and Strouhal from 0.16157 to 0.16172, so the temporal error is small.
  - The Strouhal mesh uncertainty rests on a monotone sequence: R0 0.16157, R2 0.16364, R1 0.16454. The R0 to R1 change is 1.80%. No finer mesh is allowed, because R1 is at the cumulative refinement limit. A further mesh run cannot shrink the root-mesh Strouhal uncertainty, so I am not spending the last experiment there.
  - The domain datum is weak. R4 (the largest domain, 90 D upstream, 150 D downstream) has drag drift_rel -0.002607 and ci95 0.0011453. R3 has drift_rel -0.0013441 and ci95 0.00063061. R0 has 7.1653e-05 and 2.1297e-05. The R3 and R4 windows are 40 to 80 convective units, with 6 cycles, against 12 cycles for R0.
  - R3 and R4 also have checkMesh_ok false. The domain drag change (R0 1.3222, R3 1.3131, R4 1.311) is still drifting in the largest domain. That could hide a larger domain effect, and it also makes the Strouhal observed order (2.25, outside the formal bracket) unreliable. The Strouhal frequency resolution is 0.025 for R3 and R4, which is coarser than the R0-to-R4 Strouhal difference (0.16157 to 0.1607).
  - RUN_LONGER on R4 tests this. It adds cycles, tightens the frequency resolution, and shows whether the R4 drag plateau holds or keeps drifting. This is the last experiment. It costs 2205 s from the recorded estimate. That fits the budget: 5 of 6 experiments and 6.36 of 12.0 compute used.
  - The Strouhal mesh component probably cannot be closed at 0.015 for R0, because the demonstrated R0 to R1 change is already 1.80%. A final INCONCLUSIVE for Strouhal is therefore likely.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on A2_moderate_mesh.D3x-912cd516504f — R4 is the largest-domain datum for the domain extrapolation, and it is the least stationary run: drag drift_rel -0.002607 and ci95 0.0011453 over 6 cycles, with Strouhal resolution 0.025. Domain is the one open component where the evidence is noise-limited and may hide an effect larger than estimated. Mesh and time cannot be improved further or are already closed.
  - Outcome: executed -> A2_moderate_mesh.long180-555e22f6f9da (completed)

Run A2_moderate_mesh.m1.5-773c4ec70534: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.5, time.delta_t: 0.01→0.007967, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.335 (+0.97%).
  - Observation: strouhal_number 0.16157 → 0.16454 (+1.84%).

Run A2_moderate_mesh.m1.06-c5d153eb41a5: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.061, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3321 (+0.75%).
  - Observation: strouhal_number 0.16157 → 0.16364 (+1.28%).

Run A2_moderate_mesh.D2x-4a8a18327a27: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3131 (-0.69%).
  - Observation: strouhal_number 0.16157 → 0.16082 (-0.46%).

Run A2_moderate_mesh.D3x-912cd516504f: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.311 (-0.84%).
  - Observation: strouhal_number 0.16157 → 0.1607 (-0.54%).

Run A2_moderate_mesh.dt0.005-4720e4eddcde: REDUCE_TIME_STEP from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3183 (-0.29%).
  - Observation: strouhal_number 0.16157 → 0.16172 (+0.09%).

Run A2_moderate_mesh.long180-555e22f6f9da: RUN_LONGER from A2_moderate_mesh.D3x-912cd516504f (time.end_time: 80→180).
  - Observation: mean_drag_coefficient 1.311 → 1.3094 (-0.12%).
  - Observation: strouhal_number 0.1607 → 0.16054 (-0.10%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A2_moderate_mesh-1c5ea01594aa` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=2124 s; record: results/runs/A2_moderate_mesh-1c5ea01594aa/run.json
- `A2_moderate_mesh.m1.5-773c4ec70534` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T09:44:02+00:00 wall=2827 s; record: results/runs/A2_moderate_mesh.m1.5-773c4ec70534/run.json
- `A2_moderate_mesh.m1.06-c5d153eb41a5` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T09:43:44+00:00 wall=1223 s; record: results/runs/A2_moderate_mesh.m1.06-c5d153eb41a5/run.json
- `A2_moderate_mesh.D2x-4a8a18327a27` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:38:04+00:00 wall=438.6 s; record: results/runs/A2_moderate_mesh.D2x-4a8a18327a27/run.json
- `A2_moderate_mesh.D3x-912cd516504f` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-20T07:52:10+00:00 wall=805.6 s; record: results/runs/A2_moderate_mesh.D3x-912cd516504f/run.json
- `A2_moderate_mesh.dt0.005-4720e4eddcde` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:07:48+00:00 wall=764.5 s; record: results/runs/A2_moderate_mesh.dt0.005-4720e4eddcde/run.json
- `A2_moderate_mesh.long180-555e22f6f9da` status=completed parent=A2_moderate_mesh.D3x-912cd516504f created=2026-10-20T08:14:38+00:00 wall=1011 s; record: results/runs/A2_moderate_mesh.long180-555e22f6f9da/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1903400408.0, "relative_to_root": 7.393856224993202, "experiment_wall_seconds": 7069.7734267709875, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.616145325, "loop_wall_seconds": 11180.737798963}
