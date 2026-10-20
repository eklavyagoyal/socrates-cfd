# Verification report: A2_moderate_mesh (C-llm)

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
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.32% <= 1.50% (root-to-finest change 0.958%) [three-level Celik procedure, observed order p=3.36, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.74% > 1.50% but the demonstrated change 1.80% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.47, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.17% <= 1.50% (root-to-finest change 0.292%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.36% <= 1.50% (root-to-finest change 0.090%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.4e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.35% <= 1.50% (root-to-finest change 0.941%) [three-level Celik procedure, observed order p=1.48, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.84% <= 1.50% (root-to-finest change 0.611%) [three-level Celik procedure, observed order p=1.71, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [ACCEPT]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.12-bb89255d27e3
│   └── A2_moderate_mesh.m1.5-773c4ec70534
├── Temporal discretisation (time-step sensitivity): PASS U=0.0117
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): PASS U=0.0135
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D2x-b76a220ade27

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
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0274
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.m1.12-bb89255d27e3
│   └── A2_moderate_mesh.m1.5-773c4ec70534
├── Temporal discretisation (time-step sensitivity): PASS U=0.00362
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): PASS U=0.00843
    └── A2_moderate_mesh-1c5ea01594aa
    └── A2_moderate_mesh.D2x-4a8a18327a27
    └── A2_moderate_mesh.D2x-b76a220ade27

```

## EXPERIMENT HISTORY

Run A2_moderate_mesh-1c5ea01594aa: submitted simulation (17162 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified because no FAIL exists.
  - R0 averaging and statistics components pass for both quantities. For drag they are 4.434e-05 and 7.165e-05. For Strouhal they are 8.516e-06 and 5.21e-05. Both are far below the 0.03 tolerance (half-tolerance budget 0.015).
  - Mesh, time and domain components are all unmeasured, so no combined uncertainty exists for mean_drag_coefficient (1.3222) or strouhal_number (0.16157).
  - R0 mesh is coarse for a wake-shedding problem: 17162 cells, representative_cell_size_D 0.61063, wake_cells_streamwise 83 and wake_last_cell_D 1.3639. The mesh error could plausibly exceed 1.5 % for both quantities.
  - Time-step risk looks smaller: second-order backward scheme, 0.01 convective units, max Courant 0.56482 and 618.93 steps per shedding period.
  - Domain risk looks moderate: upstream 30 D, downstream 50 D, half-height 40 D, blockage 0.0125 with symmetry sides and outlet inletOutlet. The domain is large, but its effect is still unmeasured.
  - The averaging window starts at the MSER cap (stationary_window_start_is_mser_cap true, start 71.557). However, the window mean differs from the reported value by only about 0.004 %, so the transient is not the leading concern.
  - REFINE_MESH on R0 is the most informative next step. It tests the most under-resolved discretisation component, and its cost (2266 s) is affordable within the budget of 6 experiments and 12x compute.
  - Requested: REFINE_MESH {'factor': 1.5} on A2_moderate_mesh-1c5ea01594aa — Mesh resolution is the most likely unmeasured error source, with a coarse wake and 17162 cells in total. A factor of 1.5 gives a measurable change at moderate cost. A larger factor risks forcing a time-step change that would confound the result and consuming the compute budget.
  - Outcome: executed -> A2_moderate_mesh.m1.12-bb89255d27e3 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because mesh, time and domain components are not all measured and within budget. REJECT is not justified because there is no FAIL.
  - R0 averaging and statistics components pass. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. All are far below the 0.03 tolerance.
  - R1 (REFINE_MESH of R0, 17162 to 38778 cells, cell size 0.61063 D to 0.40623 D) moved drag from 1.3222 to 1.3327 (demonstrated change 0.79%). It moved Strouhal from 0.16157 to 0.16387 (demonstrated change 1.40%). Both changes are in the same direction and below tau, so there is no FAIL.
  - The mesh uncertainty of R0 is 0.04264 for drag and 0.07539 for Strouhal. Both are above the 1.50% half-tolerance limit. They come from a two-level Richardson estimate with an assumed order p=2 and Fs=3, not a measured convergence order. Mesh is therefore the largest and best-evidenced open component.
  - Strouhal changed by 1.40% for a refinement of about 1.5x in cell size. This is close to the 1.5% half-tolerance on its own, so R0 is not demonstrably mesh-converged. Even if time and domain turn out negligible, R0 cannot be accepted until the mesh component is measured.
  - Time-step and domain errors are still unmeasured. The time risk looks low: backward scheme, 0.01 convective units, max Courant 0.56482 for R0 and 0.6703 for R1, about 619 steps per shedding period. The domain looks generous: 30 D upstream, 50 D downstream, 40 D half-height, blockage 0.0125. They remain unmeasured, and the verifier does not count a low prior as a pass.
  - R1 cannot be refined again (cumulative refinement limit 2.0). A third mesh level from parent R0 at factor 2.0 would give three levels (R0, R1, R2). That would let the verifier estimate the observed convergence order and replace the assumed p=2 and Fs=3.
  - Budget allows it: 1 of 6 experiments used and 1.21x of 12x compute used. R1 cost 931.9 s against an estimate of 2266 s for R0 refinement, so a finer mesh is affordable.
  - Requested: REFINE_MESH {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — Mesh is the largest unmeasured-order error: the R0 mesh uncertainty is 0.04264 for drag and 0.07539 for Strouhal, both above the 1.5% component limit. It rests on an assumed order p=2 and Fs=3. R1 cannot be refined further (cumulative limit 2.0). Refining R0 by 2.0 gives a third level that is clearly finer than R1, so the observed order can be measured. Budget is ample (1.21 of 12.0 compute, 1 of 6 experiments).
  - Outcome: executed -> A2_moderate_mesh.m1.5-773c4ec70534 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with failed_checks empty. ACCEPT is not allowed because time and domain are unmeasured for both quantities. REJECT is not justified because there is no FAIL.
  - R0 averaging and statistics components pass. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. All are far below the 0.03 tolerance.
  - The three-level mesh study (R0, R1, R2) is complete. Drag moved 1.3222 -> 1.3327 -> 1.335, with observed p=3.36 and mesh uncertainty 0.01325 <= 0.015, so the mesh component PASSES for drag.
  - Strouhal moved 0.16157 -> 0.16387 -> 0.16454, with observed p=2.47. The root mesh uncertainty is 0.02738, above the 0.015 component limit, so the mesh check is INCONCLUSIVE (demonstrated change 1.80% <= tau).
  - Further mesh refinement is not allowed: R1 and R2 are not permitted as REFINE_MESH parents (cumulative refinement limit), and R0 has already been refined to R2. The Strouhal mesh component cannot be improved with the remaining menu. The other missing components still need measuring, and the Strouhal mesh estimate may be confounded by the time step (see below).
  - R2 used time_step_convective_units 0.0079672 against 0.01 for R0 and R1, so the R1->R2 Strouhal change mixes mesh and time-step effects. A REDUCE_TIME_STEP run on R0 would separate them.
  - The domain is unmeasured. R0 has upstream 30 D, downstream 50 D, half-height 40 D, blockage 0.0125, symmetryPlane sides and inletOutlet outflow. The check says 'no EXPAND_DOMAIN experiment has been run'. A low prior does not count as a pass.
  - EXPAND_DOMAIN on R0 is the cheapest remaining experiment (estimated 1498 s against 2266 s for REDUCE_TIME_STEP on R0) and it targets a component that is missing for both quantities. Budget remains: 2 of 6 experiments and 3.89 of 12.0 compute used, so time-step verification can follow.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — The domain component is unmeasured for both quantities and blocks any ACCEPT. It is the cheapest remaining experiment on R0 (estimated 1498 s). Mesh refinement cannot go further, and the time-step experiment is planned next. Using R0 as parent compares directly against the root.
  - Outcome: executed -> A2_moderate_mesh.D2x-4a8a18327a27 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and REJECT is not justified because no FAIL exists.
  - R0 averaging and statistics components pass. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. All are far below the 0.03 tolerance.
  - The R0, R1, R2 mesh study gives drag 1.3222, 1.3327, 1.335 with observed p=3.36 and mesh uncertainty 0.01325 <= 0.015, so the drag mesh component passes. Strouhal goes 0.16157, 0.16387, 0.16454 with mesh uncertainty 0.02738, which is INCONCLUSIVE. R1 and R2 are not allowed as REFINE_MESH parents, so mesh refinement cannot be continued.
  - The time component is unmeasured for both quantities (no REDUCE_TIME_STEP run). R2 used a time step of 0.0079672 against 0.01 for R0 and R1. The R1-to-R2 Strouhal change therefore mixes mesh and time-step effects, which may inflate the Strouhal mesh uncertainty.
  - The domain component has one measurement, R3 against R0. Drag changed 1.3222 to 1.3131 (0.69%) and Strouhal changed 0.16157 to 0.16082 (0.47%). Both changes are below tau, so there is no FAIL. The domain uncertainties (0.04147 drag, 0.02803 Strouhal) rest on an assumed order p=1 and Fs=3.
  - The R3 comparison is confounded. R3 has checkMesh_ok false, a coarser representative cell size (1.0621 D vs 0.61063 D) and a coarser wake (wake_last_cell_D 2.621 vs 1.3639). The domain estimate is therefore not a clean measurement. R3 also has only 6 stationary cycles and a drag drift of -0.0013441.
  - REDUCE_TIME_STEP on R0 is the most informative next step. It is the only component with no data. It affects both quantities. It also separates the time-step effect from the mesh effect in the Strouhal sequence. Cost is 2266 s against the remaining budget (3 of 6 experiments and 4.6 of 12.0 compute used). A domain follow-up (EXPAND_DOMAIN from R3, 1949 s) can follow.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on A2_moderate_mesh-1c5ea01594aa — The time component is the only one with no data for either quantity. It blocks ACCEPT and may confound the Strouhal mesh sequence, because R2 used a different time step from R0 and R1. Using R0 as parent compares directly against the root on the identical mesh. Cost is 2266 s, which fits the remaining budget.
  - Outcome: executed -> A2_moderate_mesh.dt0.005-4720e4eddcde (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed because the domain component is unmeasured for both quantities and the Strouhal mesh component is unmeasured. REJECT is not justified because there is no FAIL.
  - R0 averaging and statistics pass. Drag: 4.434e-05 and 7.165e-05. Strouhal: 8.516e-06 and 5.21e-05. All are far below the 0.03 tolerance.
  - The R4 time-step check passes for both quantities. Time uncertainty is 0.01168 for drag and 0.003615 for Strouhal. Both are below 0.015. R0 to R4 moved drag from 1.3222 to 1.3183 and Strouhal from 0.16157 to 0.16172.
  - The drag mesh check passes: 0.01325 with observed p=3.36 over R0, R1 and R2. The Strouhal mesh check is INCONCLUSIVE at 0.02738 > 0.015 (observed p=2.47, demonstrated change 1.80%). R1 and R2 cannot be REFINE_MESH parents (cumulative limit), and R0 is already refined to R2, so this component cannot be improved directly. R2 also used time step 0.0079672 against 0.01. R4 shows a Strouhal time effect of only 0.090%, so the R2 time step does not explain the Strouhal mesh shift.
  - The domain check is INCONCLUSIVE for both quantities. Drag uncertainty is 0.04147 and Strouhal 0.02803, from R0 vs R3 with an assumed order p=1 and Fs=3. The demonstrated changes are 0.69% for drag and 0.47% for Strouhal. Both are below tau, so there is no FAIL.
  - The R0 vs R3 domain comparison is confounded. R3 has checkMesh_ok false, representative_cell_size_D 1.0621 against 0.61063, and wake_last_cell_D 2.621 against 1.3639. R3 also has noise: ci95 0.00063061 and drag drift -0.0013441. The R0-to-R3 change cannot be separated into a domain effect and a coarser-wake mesh effect. The lower R3 drag and Strouhal are also consistent with the mesh trend, in which coarser meshes give lower values.
  - EXPAND_DOMAIN with parent R3 (estimated 1949 s) keeps the R3 mesh and adds cells only further out. It gives a clean domain level with no change to the near field or wake. With R0, R3 and the new run, the verifier can measure an observed domain order instead of assuming p=1. This is the experiment most likely to move the domain component, the largest open term for drag (0.04147).
  - Budget: 4 of 6 experiments used and 5.66 of 12.0 compute used. This run fits, and one experiment remains afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on A2_moderate_mesh.D2x-4a8a18327a27 — The domain component is the largest open term for drag (0.04147) and is open for Strouhal (0.02803). The existing R0 vs R3 comparison is confounded by R3's coarser wake and mesh (cell size 1.0621 D, wake_last_cell_D 2.621, checkMesh_ok false) and rests on an assumed order p=1. Expanding R3 by 2.0 keeps R3's mesh in the near field and wake, so the change from R3 is a clean domain effect. Together with R0 and R3 it gives three domain levels, so the observed order can be measured. Estimated cost is 1949 s, which fits the budget.
  - Outcome: executed -> A2_moderate_mesh.D2x-b76a220ade27 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed for the root run R0, and REJECT is not justified because no FAIL exists.
  - mean_drag_coefficient is ACCEPT. All components pass: averaging 4.434e-05, statistics 7.165e-05, mesh 0.01325 (observed p=3.36), time 0.01168, domain 0.0135. Combined uncertainty is 0.02228, against tolerance 0.03.
  - strouhal_number is INCONCLUSIVE only because of the mesh component. Averaging 8.516e-06, statistics 5.21e-05, time 0.003615 and domain 0.008429 all pass. The mesh uncertainty is 0.02738, which is above the 0.015 component limit, so no combined uncertainty exists.
  - The Strouhal mesh sequence is R0 0.16157, R1 0.16387, R2 0.16454. The changes shrink (observed p=2.47), so the sequence is monotonic and converging. The demonstrated R0-to-finest change is 1.80%, below tau, so there is no FAIL. The R0 error is real but not a violation.
  - R4 shows the Strouhal time-step effect is small (R0 0.16157 to R4 0.16172, change 0.090%). The smaller R2 time step (0.0079672) therefore does not explain the mesh shift. The mesh uncertainty is not a time-step artefact.
  - R3 and R5 give consistent domain evidence for Strouhal: R0 0.16157, R3 0.16082, R5 0.16059. Domain uncertainty is 0.84% and passes. Drag moved 1.3222, 1.3131, 1.3099, with domain uncertainty 1.35%, which also passes.
  - The remaining Strouhal gap is a property of the R0 mesh (cell size 0.61063 D, 83 wake cells). R0 sits below the finer-mesh values. Additional runs on other parents change other components, not the R0 mesh error. REFINE_MESH from R0 would only add another level of the same family. R1 and R2 are barred as parents by the cumulative refinement limit.
  - One experiment remains (5 of 6 used, compute 6.58 of 12.0). None of the menu entries (REFINE_MESH on R3, R4 or R5, RUN_LONGER, further REDUCE_TIME_STEP, EXPAND_DOMAIN) would turn the Strouhal mesh component of R0 into a PASS. Spending the compute would not change the answer. The system should report INCONCLUSIVE for Strouhal rather than imply the evidence is complete.
  - Outcome: planner chose to stop (no useful affordable experiment)

Run A2_moderate_mesh.m1.12-bb89255d27e3: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.125, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3327 (+0.80%).
  - Observation: strouhal_number 0.16157 → 0.16387 (+1.42%).

Run A2_moderate_mesh.m1.5-773c4ec70534: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, mesh.refinement: 0.75→1.5, time.delta_t: 0.01→0.007967, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.335 (+0.97%).
  - Observation: strouhal_number 0.16157 → 0.16454 (+1.84%).

Run A2_moderate_mesh.D2x-4a8a18327a27: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3131 (-0.69%).
  - Observation: strouhal_number 0.16157 → 0.16082 (-0.46%).

Run A2_moderate_mesh.dt0.005-4720e4eddcde: REDUCE_TIME_STEP from A2_moderate_mesh-1c5ea01594aa (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3222 → 1.3183 (-0.29%).
  - Observation: strouhal_number 0.16157 → 0.16172 (+0.09%).

Run A2_moderate_mesh.D2x-b76a220ade27: EXPAND_DOMAIN from A2_moderate_mesh.D2x-4a8a18327a27 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3131 → 1.3099 (-0.25%).
  - Observation: strouhal_number 0.16082 → 0.16059 (-0.14%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0223 vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A2_moderate_mesh-1c5ea01594aa` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=2124 s; record: results/runs/A2_moderate_mesh-1c5ea01594aa/run.json
- `A2_moderate_mesh.m1.12-bb89255d27e3` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-20T01:15:56+00:00 wall=931.9 s; record: results/runs/A2_moderate_mesh.m1.12-bb89255d27e3/run.json
- `A2_moderate_mesh.m1.5-773c4ec70534` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T09:44:02+00:00 wall=2827 s; record: results/runs/A2_moderate_mesh.m1.5-773c4ec70534/run.json
- `A2_moderate_mesh.D2x-4a8a18327a27` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:38:04+00:00 wall=438.6 s; record: results/runs/A2_moderate_mesh.D2x-4a8a18327a27/run.json
- `A2_moderate_mesh.dt0.005-4720e4eddcde` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:07:48+00:00 wall=764.5 s; record: results/runs/A2_moderate_mesh.dt0.005-4720e4eddcde/run.json
- `A2_moderate_mesh.D2x-b76a220ade27` status=completed parent=A2_moderate_mesh.D2x-4a8a18327a27 created=2026-10-20T01:15:35+00:00 wall=611.5 s; record: results/runs/A2_moderate_mesh.D2x-b76a220ade27/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1694248408.0, "relative_to_root": 6.581394584935711, "experiment_wall_seconds": 5573.900033996985, "n_experiments": 5, "planner_calls": 6, "planner_cost_usd": 0.565981225, "loop_wall_seconds": 4204.54164277}
