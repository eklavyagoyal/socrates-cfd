# Verification report: A2_moderate_mesh (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3221
- strouhal_number: 0.16157

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

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
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.55% > 1.50% but the demonstrated change 0.90% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.19, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.90% <= 1.50% (root-to-finest change 0.583%) [three-level Celik procedure, observed order p=1.52, Fs=1.25]

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0155
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D1.5x-0eba1d38476e

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
└── Artificial boundaries (domain sensitivity): PASS U=0.00899
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D1.5x-0eba1d38476e

```

## EXPERIMENT HISTORY

Run A2_moderate_mesh-1c5ea01594aa: submitted simulation (17162 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. Mesh, time and domain uncertainty components are all unmeasured, so ACCEPT is not allowed. Nothing supports REJECT.
  - The averaging and statistics components pass. For drag, averaging is 4.434e-05 and statistics is 7.165e-05. For Strouhal, they are 8.516e-06 and 5.21e-05. The stationary window has 12 cycles and the drag CI95 is 2.1297e-05. Sampling is therefore not the limiting factor.
  - R0 has a coarse mesh: 17162 cells, representative cell size 0.61063 D, and wake_last_cell_D of 1.3639 across 83 streamwise wake cells. The recorded wake resolution is the likeliest source of a spatial error larger than the 0.03 tolerance in both drag and Strouhal number.
  - The time step is probably less critical. R0 uses backward time stepping with max Courant 0.56482 and 618.93 steps per shedding period. The domain looks reasonably large: upstream 30 D, downstream 50 D, half-height 40 D, blockage 0.0125. Neither is proven, but both are less likely than mesh to move the answer by more than 3%.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute. A mesh refinement from R0 costs an estimated 2266 s, against 2124 s for R0 itself.
  - I chose the largest factor (2.0), giving about 1.41x linear refinement in 2D. A larger step gives a clearer mesh-sensitivity signal than the default 1.4142, which is only about 1.19x linear and could fall inside the noise.
  - Requested: REFINE_MESH {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Mesh resolution is the most likely source of an error larger than the 3% tolerance. R0 has only 17162 cells, with 0.61063 D representative cell size and wake cells up to 1.3639 D. Mesh uncertainty is unmeasured for both quantities. The factor of 2.0 gives the largest, clearest signal and is affordable within the budget.
  - Outcome: executed -> A2_moderate_mesh.m1.5-773c4ec70534 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.19

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and nothing supports REJECT.
  - Averaging and statistics pass for both quantities. For R0 drag they are 4.434e-05 and 7.165e-05. For Strouhal they are 8.516e-06 and 5.21e-05. R0 has 12 stationary cycles.
  - R0 to R1 changed the stationary-window drag from 1.3222 to 1.335, which is 0.96%. It changed Strouhal from 0.16157 to 0.16454, which is 1.80%. R1 has 4x the cells (17162 to 68888) and half the cell size (0.61063 D to 0.30478 D).
  - The mesh uncertainty is unresolved. It is 0.03828 for drag and 0.07206 for Strouhal. Both are above 0.5*tolerance (0.015). The estimate uses only two levels, with an assumed order p=2 and Fs=3, so it is conservative and unverified.
  - Strouhal moved 1.80% on this mesh step alone, which is more than half of the 3% tolerance. Mesh is still the dominant open component.
  - R1 cannot be refined further (cumulative refinement 2.83 exceeds the limit of 2.0). The only way to a third mesh level is a REFINE_MESH from R0 at an intermediate factor.
  - With factor 1.4142, R0 (0.61063 D), the new run and R1 (0.30478 D) should form a roughly geometric sequence with linear ratio about 1.41 each. This allows an observed convergence order and a better-conditioned extrapolation, replacing the assumed p=2.
  - The cost is 2266 s. Budget used is 1 of 6 experiments and 2.69 of 12 relative compute, so it is affordable. Time-step and domain runs on R0 remain for later iterations (R0 time step 0.01 D/U, domain 30 D upstream, 50 D downstream, 40 D half-height).
  - Requested: REFINE_MESH {'factor': 1.4142} on A2_moderate_mesh-1c5ea01594aa — Mesh uncertainty is the largest open component: 0.03828 for drag and 0.07206 for Strouhal, from a two-level Richardson estimate with assumed p=2. R1 cannot be refined further. A third level at factor 1.4142 from R0 gives a roughly geometric three-grid sequence, which permits an observed order and a more reliable mesh error bound.
  - Outcome: executed -> A2_moderate_mesh.m1.06-c5d153eb41a5 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and nothing supports REJECT.
  - Averaging and statistics pass for R0. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. R0 has 12 stationary cycles.
  - The mesh study (R0, R2, R1) is monotonic. Drag is 1.3222, 1.3321, 1.335. Strouhal is 0.16157, 0.16364, 0.16454. The drag mesh component now passes at 0.01305 (observed p=3.58).
  - The Strouhal mesh component is still INCONCLUSIVE at 0.02755 (p=2.43), above the 0.015 per-component limit. R0-to-R1 changed Strouhal by 1.80%. The R2-to-R1 step is smaller than the R0-to-R2 step, which suggests the sequence is converging.
  - R1 cannot be refined further. A refinement from R2 at factor 1.3 to 1.4142 reaches a cumulative factor of at most 2.0, which is no finer than R1. It would add little at a cost of 4573 s. More mesh work is therefore low value now.
  - The domain component is unmeasured for both quantities. Time is also unmeasured. Both are required before any ACCEPT. The domain is declared unbounded. The recorded domain is upstream 30 D, downstream 50 D, half-height 40 D, blockage 0.0125, with symmetryPlane lateral boundaries. The effect of that truncation on the 3% quantities has not been measured.
  - The time step looks less likely to dominate. R0 has 618.93 steps per shedding period, max Courant 0.56482 and a backward scheme. It remains unmeasured, so it is a follow-up.
  - EXPAND_DOMAIN on R0 is the cheapest experiment (1498 s). Budget used is 2 of 6 experiments and 3.75 of 12 relative compute. A domain run (about 0.7 of root cost) and a time-step run (about 1.07) both fit afterwards.
  - The near-field mesh stays unchanged in EXPAND_DOMAIN, so the comparison with R0 isolates the boundary effect. Factor 2.0 halves the recorded blockage and doubles all boundary distances. That is a clear signal without the larger cost of 3.0.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — The domain uncertainty is unmeasured for both quantities and is required for ACCEPT. The domain is claimed unbounded but is finite (30 D upstream, 50 D downstream, 40 D half-height, blockage 0.0125, symmetryPlane sides). It is the cheapest experiment (1498 s from R0). Further mesh refinement is nearly exhausted: R1 is at the cumulative limit and a refinement from R2 cannot go finer than R1. Time-step error is less likely to dominate.
  - Outcome: executed -> A2_moderate_mesh.D2x-4a8a18327a27 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.07

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. Nothing supports REJECT, because no measured change exceeds the 0.03 tolerance.
  - Averaging and statistics pass for R0. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. R0 has 12 stationary cycles.
  - The mesh study (R0, R2, R1) is monotonic. Drag is 1.3222, 1.3321, 1.335 and its mesh uncertainty passes at 0.01305 (p=3.58). Strouhal is 0.16157, 0.16364, 0.16454 and its mesh uncertainty is 0.02755 (p=2.43), above 0.015. R1 is at the cumulative refinement limit, and refining R2 costs 4573 s without going finer than R1, so more mesh work is low value now.
  - R3 (domain doubled) changed drag from 1.3222 to 1.3131 (0.69%) and Strouhal from 0.16157 to 0.16082 (0.47%). Both are well under 1.5%. The domain uncertainties of 0.04147 and 0.02803 come only from an assumed p=1 and Fs=3 two-level estimate. They are conservative, not measured.
  - R3 has checkMesh_ok=false, its drag CI95 is 0.00063061, its drift is -0.0013441, and it has only 6 cycles. Its drag CI95 is about 30 times the R0 value (2.1297e-05). R3 is therefore a noisier domain datum than R0. This is a caveat, not a FAIL.
  - Time-step error is entirely unmeasured for both quantities. It is a required component with no data, so it is the largest blind spot. R0 uses dt=0.01 with 618.93 steps per period and max Courant 0.56482. R1 used dt=0.0079672 and R2 used 0.01, so the mesh-study levels also carry a small time-step confound.
  - Budget: 3 of 6 experiments and 4.46 of 12 relative compute are used. REDUCE_TIME_STEP on R0 costs 2266 s. A later domain run (1949 s from R3) still fits afterwards.
  - Factor 2.0 is the default and gives a clear signal against the noise levels. It is cheaper than a factor of 4, which would cost more.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Time error is the only component with no data for either quantity, and ACCEPT requires it. Mesh is nearly exhausted: R1 is at the cumulative limit. The domain shift is small (0.69% drag, 0.47% Strouhal), so the time step is the more likely hidden error source. Running it on R0 attributes the time uncertainty directly to the root at 2266 s, which fits the remaining budget and still leaves room for a domain follow-up.
  - Outcome: executed -> A2_moderate_mesh.dt0.005-4720e4eddcde (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not supported, because no demonstrated change exceeds the 0.03 tolerance.
  - R0 passes averaging and statistics. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. R0 has 12 stationary cycles.
  - The time component is now measured and passes. Drag is 0.01168 and Strouhal is 0.003615. R4 (dt=0.005) changed drag from 1.3222 to 1.3183 and Strouhal from 0.16157 to 0.16172.
  - The drag mesh component passes at 0.01305 (R0, R2, R1, observed p=3.58). The Strouhal mesh component is INCONCLUSIVE at 0.02755 (p=2.43), above the 0.015 per-component limit. The demonstrated R0-to-R1 Strouhal change is 1.80%. R1 is at the cumulative refinement limit, so no finer mesh level is available.
  - The domain component is INCONCLUSIVE for both quantities: drag 0.04147, Strouhal 0.02803. This is the only open component for drag and one of two for Strouhal. R3 (domain doubled) changed drag from 1.3222 to 1.3131 (0.69%) and Strouhal from 0.16157 to 0.16082 (0.47%). The uncertainty estimate relies on an assumed p=1 and Fs=3 from only two levels, so it is conservative and not measured.
  - R3 is a weaker datum. It has checkMesh_ok=false, drag CI95 0.00063061, drift -0.0013441 and only 6 cycles. The 'noise floor 1.3e-03' in the domain check partly reflects this.
  - A third domain level would give an observed domain order and could cut the domain uncertainty below 0.015. It is the cheapest option that addresses a missing component shared by both quantities (1949 s from R3). Budget used is 4 of 6 experiments and 5.53 of 12 relative compute, so it fits.
  - A mesh refinement from R2 or R4 is more expensive (4573 s and 4531 s). It cannot give a level finer than R1 and would not address the domain gap.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on A2_moderate_mesh.D2x-4a8a18327a27 — Domain uncertainty is INCONCLUSIVE for both quantities (drag 0.04147, Strouhal 0.02803). It rests on an assumed p=1 and Fs=3 from two levels (R0, R3). A third domain level from R3 gives an observed order. This is the cheapest listed experiment (1949 s) that addresses a component missing for both quantities. Mesh and time are otherwise resolved or cannot be advanced.
  - Outcome: executed -> A2_moderate_mesh.D1.5x-0eba1d38476e (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not supported, because no demonstrated change exceeds the 0.03 tolerance.
  - Drag: averaging 4.434e-05, statistics 7.165e-05, mesh 0.01305 (R0,R2,R1; p=3.58), time 0.01168 (R0,R4) all PASS. The domain component is INCONCLUSIVE at 0.01546 (R0,R3,R5; p=1.19). That is just above the 0.015 limit, and the demonstrated domain change is 0.90%.
  - Strouhal: averaging 8.516e-06, statistics 5.21e-05, time 0.003615 and domain 0.008985 PASS. The mesh component is INCONCLUSIVE at 0.02755 (R0,R2,R1; p=2.43).
  - The Strouhal mesh gap is structural, not a lack of data. R0 to R1 changed Strouhal by 1.80% (0.16157 to 0.16454), which already exceeds the 1.5% per-component limit. R0 is the root and its own mesh error cannot be reduced by a further run. The mesh sequence is monotonic (0.16157, 0.16364, 0.16454), so another level would refine the order estimate but would not move R0 back inside 1.5%.
  - The domain gap for drag is small and might be closed. But the Strouhal mesh gap would remain open, so the overall verdict could not reach ACCEPT.
  - Budget: 5 of 6 experiments and 6.36 of 12 relative compute used. EXPAND_DOMAIN is not allowed from R5 (cumulative domain factor limit) and REFINE_MESH is not allowed from R1 (cumulative refinement limit). A mesh refinement from R2 can reach at most R1's cumulative level, which is no finer than R1.
  - No remaining experiment can both resolve the Strouhal mesh component and produce a REJECT-grade demonstrated change above 3%. I am therefore not spending the last run, and the system should report INCONCLUSIVE.
  - Outcome: planner chose to stop (no useful affordable experiment)

Run A2_moderate_mesh.m1.5-773c4ec70534: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.5, time.delta_t: 0.01→0.007967, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.335 (+0.97%).
  - Observation: strouhal_number 0.16157 → 0.16454 (+1.84%).

Run A2_moderate_mesh.m1.06-c5d153eb41a5: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.061, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3321 (+0.75%).
  - Observation: strouhal_number 0.16157 → 0.16364 (+1.28%).

Run A2_moderate_mesh.D2x-4a8a18327a27: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3131 (-0.69%).
  - Observation: strouhal_number 0.16157 → 0.16082 (-0.46%).

Run A2_moderate_mesh.dt0.005-4720e4eddcde: REDUCE_TIME_STEP from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3183 (-0.29%).
  - Observation: strouhal_number 0.16157 → 0.16172 (+0.09%).

Run A2_moderate_mesh.D1.5x-0eba1d38476e: EXPAND_DOMAIN from A2_moderate_mesh.D2x-4a8a18327a27 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3131 → 1.3104 (-0.21%).
  - Observation: strouhal_number 0.16082 → 0.16063 (-0.11%).

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
- `A2_moderate_mesh.dt0.005-4720e4eddcde` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:07:48+00:00 wall=764.5 s; record: results/runs/A2_moderate_mesh.dt0.005-4720e4eddcde/run.json
- `A2_moderate_mesh.D1.5x-0eba1d38476e` status=completed parent=A2_moderate_mesh.D2x-4a8a18327a27 created=2026-10-20T15:32:55+00:00 wall=785.4 s; record: results/runs/A2_moderate_mesh.D1.5x-0eba1d38476e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1636200408.0, "relative_to_root": 6.355904160354271, "experiment_wall_seconds": 6038.877490843983, "n_experiments": 5, "planner_calls": 6, "planner_cost_usd": 0.5692785250000001, "loop_wall_seconds": 937.711530073997}
