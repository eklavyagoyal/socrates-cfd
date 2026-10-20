# Verification report: K1_central_scheme (C-llm-r2)

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
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — mesh sequence of mean_drag_coefficient diverges under refinement (R = eps21/eps32 = 1.47 >= 1; Eca & Hoekstra 2014); root-to-finest change 0.29%; not in the asymptotic range, no extrapolation
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.45% <= 1.50% (root-to-finest change 0.858%) [three-level Celik procedure, observed order p=1.94, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.91% <= 1.50% (root-to-finest change 0.228%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.3e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.48% <= 1.50% (root-to-finest change 0.120%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.56% > 1.50% but the demonstrated change 1.01% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.18, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.14% <= 1.50% (root-to-finest change 0.594%) [three-level Celik procedure, observed order p=0.76, Fs=1.25]

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
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-325af4c14f68
├── Temporal discretisation (time-step sensitivity): PASS U=0.00913
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0156
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D3x-14d3dc15d928
    └── K1_central_scheme.D2x-0c7e73f08a9e

CLAIM: strouhal_number of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [ACCEPT]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0145
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.41-9a011a4052fe
│   └── K1_central_scheme.m2-325af4c14f68
├── Temporal discretisation (time-step sensitivity): PASS U=0.00478
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): PASS U=0.0114
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D3x-14d3dc15d928
    └── K1_central_scheme.D2x-0c7e73f08a9e

```

## EXPERIMENT HISTORY

Run K1_central_scheme-e4e5fb66bdca: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT has no basis.
  - R0 passes the averaging and statistics components: the drag averaging bias is 7.04e-05 and the statistics uncertainty is 0.0001331. For Strouhal the values are 1.316e-05 and 0.000122. All are far below the 0.03 tolerance. R0 has 12 stationary cycles.
  - The mesh, time and domain components are all unmeasured, because no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists. Absence of evidence is not a pass.
  - R0 has 30580 cells with a representative cell size of 0.45745 D and a last wake cell of 1.0209 D. It uses Gauss linear convection with 160 cells around the cylinder. Spatial error in the wake and shedding is the most plausible source of an error larger than 3 %.
  - The time step is 0.01 D/U with a max Courant number of 0.736, giving 612.39 steps per shedding period with a 'backward' (second-order) scheme. Temporal error looks less likely to dominate, but it is unmeasured.
  - The domain has a blockage ratio of 0.0125, 30 D upstream, 50 D downstream and 40 D half-height. The boundary conditions are plausible and the domain is moderately large, so it is a lower-priority risk than the mesh.
  - Budget allows the mesh run first (about 5070 s). Time and domain runs (about 4367 s and 2899 s) can follow within the compute and experiment limits.
  - Requested: REFINE_MESH {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — Mesh is the most likely uncontrolled error source: R0 is relatively coarse (30580 cells, 0.45745 D representative size, 1.0209 D last wake cell). Averaging and statistics are already negligible, so the remaining risk is discretisation. A factor of 2.0 gives the largest signal-to-noise ratio and is affordable within the budget.
  - Outcome: executed -> K1_central_scheme.m2-325af4c14f68 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.25

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and there is no FAIL to justify REJECT.
  - R0 averaging and statistics components pass. Drag: averaging 7.04e-05, statistics 0.0001331. Strouhal: averaging 1.316e-05, statistics 0.000122. R0 has 12 stationary cycles.
  - Mesh, drag: R0 Cd 1.3403 vs R1 Cd 1.3365 (root-to-finest change 0.289%). The mesh uncertainty is 0.01155 and the mesh check passes.
  - Mesh, Strouhal: R0 St 0.1633 vs R1 St 0.16471 (change 0.86%). The Richardson estimate with assumed p=2 gives 0.03431, so the mesh check is INCONCLUSIVE. Only two levels exist, so the observed order is unknown.
  - Time and domain components are unmeasured for both quantities. No REDUCE_TIME_STEP or EXPAND_DOMAIN run exists, and absence of evidence is not a pass.
  - R1 used a time step of 0.006111 against 0.01 for R0, so the R0-to-R1 difference mixes spatial and temporal effects.
  - The domain is 30 D upstream, 50 D downstream and 40 D half-height, with blockage ratio 0.0125. This is untested. EXPAND_DOMAIN on R0 is the cheapest unmeasured component, at 2899 s against 4367 s for time and 5070 s for mesh.
  - Budget: 1 of 6 experiments used and 3.49 of 12.0 compute units used. Time, domain and a further mesh level are all affordable, so a sequence of experiments is possible.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — Domain truncation is completely unmeasured for both quantities and is a possible systematic error larger than the 3% tolerance. It is the cheapest experiment (2899 s) and can be run directly on R0, because R1 is not allowed (child mesh would have 162400 cells, above the 160000 limit). The near-field mesh is unchanged, so the comparison with R0 isolates the boundary effect.
  - Outcome: executed -> K1_central_scheme.D2x-b0a7ed20bbb5 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT has no basis because no FAIL has been measured.
  - R0 averaging and statistics pass. Drag: averaging 7.04e-05, statistics 0.0001331. Strouhal: averaging 1.316e-05, statistics 0.000122. R0 has 12 stationary cycles.
  - Drag mesh component passes at 0.01155 (R0 Cd 1.3403, R1 Cd 1.3365). The Strouhal mesh component is INCONCLUSIVE at 0.03431 (R0 St 0.1633, R1 St 0.16471). It rests on an assumed order p=2 from two levels only.
  - Domain is the largest unresolved drag term. Drag domain uncertainty is 0.04162, above the 0.03 tolerance. Strouhal domain uncertainty is 0.02852, above 0.5*tolerance. Both come from an assumed p=1 two-level estimate (R0 Cd 1.3403 vs R2 Cd 1.3311; R0 St 0.1633 vs R2 St 0.16252). The observed domain changes are below tolerance, but the order is not measured.
  - R2 has checkMesh_ok false, a coarser representative cell size of 0.79405 D and a last wake cell of 1.9729 D. It also has only 6 stationary cycles. The R0-to-R2 difference therefore mixes domain, far-field mesh and statistical effects.
  - Time sensitivity is unmeasured for both quantities. No REDUCE_TIME_STEP run exists. R0 has 612.39 steps per shedding period with a backward scheme and a max Courant number of 0.73638, so a large temporal error is less likely but unproven. R1 also changed the time step to 0.006111, which confounds the Strouhal mesh estimate.
  - Budget: 2 of 6 experiments used and 4.2 of 12.0 compute units used. A time-step run (4367 s on R0), a further domain run and an intermediate mesh run all fit.
  - Next experiment is EXPAND_DOMAIN with factor 3.0 on R0. It extends the domain sequence (R0 at 1x, R2 at 2x, new run at 3x) to give an observed domain order. This replaces the assumed p=1 and can tighten the largest uncertainty. The time-step and Strouhal-mesh runs follow afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on K1_central_scheme-e4e5fb66bdca — Domain is the largest unresolved uncertainty for drag (0.04162) and is also above half the tolerance for Strouhal (0.02852). Both values rest on an assumed p=1 two-level estimate, and R2 has checkMesh_ok false and a coarse far field. A 3x domain from R0 adds a third nested level, so the observed domain order can be measured instead of assumed. R1 is not allowed as parent because its child would exceed the cell limit.
  - Outcome: executed -> K1_central_scheme.D3x-14d3dc15d928 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT has no basis because no FAIL has been measured.
  - R0 averaging and statistics pass. Drag: averaging 7.04e-05, statistics 0.0001331. Strouhal: averaging 1.316e-05, statistics 0.000122. R0 has 12 stationary cycles.
  - Time sensitivity is INCONCLUSIVE for both quantities because no REDUCE_TIME_STEP run exists. This component is completely unmeasured, so neither quantity can pass until it is measured.
  - R1 used dt 0.006111 against 0.01 for R0, so the R0-to-R1 Strouhal shift (0.1633 to 0.16471, 0.86%) mixes spatial and temporal effects. This confounds the Strouhal mesh estimate of 0.03431, which is above the 0.03 tolerance.
  - Drag mesh passes at 0.01155 (R0 Cd 1.3403, R1 Cd 1.3365).
  - Domain now has three levels, R0, R2 and R3. Drag goes 1.3403, 1.3311, 1.3283, which is monotonic, with a demonstrated change of 0.91%. Strouhal goes 0.1633, 0.16252, 0.16246. The drag domain uncertainty is 0.01575 (observed p=1.16), only marginally above the 0.015 limit. The Strouhal domain uncertainty is 0.0179, and the observed order of 3.28 was capped to p=1.
  - R2 and R3 have checkMesh_ok false and a coarser far-field mesh. They also have only 6 stationary cycles and larger statistical CIs, 0.00082395 and 0.0013228 for Cd. The domain trend is therefore not a clean measurement.
  - The domain changes are below tolerance, and the domain trend is already monotonic and flattening. The unmeasured time component is therefore the most informative next experiment.
  - R0 has 612.39 steps per shedding period, a backward scheme and max Courant number 0.73638. A large temporal error is not expected, but it is unproven.
  - REDUCE_TIME_STEP on R0 costs 4367 s, about 1.07 compute units. That brings use to about 6.1 of 12.0 and 4 of 6 experiments. A later intermediate REFINE_MESH on R0 for the Strouhal mesh order, and possibly an EXPAND_DOMAIN on R2, still fit.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — Temporal error is the only component that is entirely unmeasured for both quantities, and no verdict other than INCONCLUSIVE is possible without it. It also separates the temporal and spatial parts of the R0-to-R1 Strouhal shift, since R1 changed dt to 0.006111. Using R0 as parent keeps the mesh and domain identical, so the comparison isolates the time step. R0 is far cheaper than R1 (28584 s).
  - Outcome: executed -> K1_central_scheme.dt0.005-4f460bac38b7 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 1.07, 6.1

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT has no basis because no measured change exceeds the 0.03 tolerance.
  - R0 averaging and statistics pass. Drag: averaging 7.04e-05, statistics 0.0001331. Strouhal: averaging 1.316e-05, statistics 0.000122. R0 has 12 stationary cycles.
  - R4 (dt halved from R0) closed the time component. Drag time uncertainty is 0.009131 and Strouhal time uncertainty is 0.004782, both passing. R0 Cd 1.3403 vs R4 Cd 1.3373. R0 St 0.1633 vs R4 St 0.16349.
  - The Strouhal mesh uncertainty is the largest open item at 0.03431, above both 0.015 and the 0.03 tolerance. It comes from a two-level estimate with assumed p=2 (R0 St 0.1633, R1 St 0.16471, change 0.86%). The observed order is unknown. R4 shows that dt alone moves St by 0.12%, so most of the R0-to-R1 shift is probably spatial, but this is not measured.
  - Drag mesh passes at 0.01155 (R0 Cd 1.3403, R1 Cd 1.3365, change 0.289%).
  - Domain is INCONCLUSIVE for both quantities. Drag is 0.01575 (observed p=1.16) and Strouhal is 0.0179 (observed order 3.28, capped to p=1). Both are only just above 0.015. The demonstrated changes (0.91% and 0.52%) are below tolerance. R2 and R3 have checkMesh_ok false, coarser far-field meshes and only 6 cycles, so the domain trend is partly confounded.
  - Budget: 4 of 6 experiments used and 6.09 of 12.0 compute units. Two more experiments fit: an intermediate mesh run costs about 5070 s and a domain run on R2 costs 3746 s. The mesh run goes first because it targets the only component above the tolerance itself.
  - REFINE_MESH on R0 with factor 1.4142 (the default) gives R0, new run and R1 as three levels. Their linear ratios are 1.414 and 1.414. The Celik procedure then yields an observed order instead of the assumed p=2.
  - Requested: REFINE_MESH {'factor': 1.4142} on K1_central_scheme-e4e5fb66bdca — The Strouhal mesh component (0.03431) is the largest unresolved uncertainty and exceeds the 0.03 tolerance. It rests on two levels and an assumed p=2. An intermediate level between R0 and R1 gives three levels with a constant refinement ratio, so the observed order can be measured. R1 is not allowed as parent (cumulative refinement limit). R0 is cheaper than R4, R2 and R3, and keeps domain and dt comparable. The time component is now measured, so dt effects can be separated.
  - Outcome: executed -> K1_central_scheme.m1.41-9a011a4052fe (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and there are no failed checks. ACCEPT is not allowed. REJECT has no basis, because no measured change exceeds the 0.03 tolerance.
  - R0 averaging and statistics pass. Drag: averaging 7.04e-05, statistics 0.0001331. Strouhal: averaging 1.316e-05, statistics 0.000122. R0 has 12 stationary cycles.
  - Time passes for both quantities, using R0 and R4: drag 0.009131 and Strouhal 0.004782. Strouhal mesh now passes at 0.01447 (R0, R5, R1; observed p=1.94).
  - Drag mesh is INCONCLUSIVE. The sequence is R0 1.3403, R5 1.3388, R1 1.3365, and the verifier flags R=1.47 >= 1 (divergent). The root-to-finest change is only 0.29%, far below 0.03.
  - The drag mesh sequence is confounded by the time step. REFINE_MESH changed dt: R0 0.01, R5 0.0086422, R1 0.006111. R4 shows dt alone moves drag by 0.228% (R0 1.3403 vs R4 1.3373), which is comparable to the whole mesh change. Another mesh run would carry the same confounding, and R1 is too expensive to rerun at a smaller dt (28584 s).
  - Domain is INCONCLUSIVE for both quantities: drag 0.01575 (p=1.16) and Strouhal 0.0179 (observed order 3.28, capped to p=1). Both are only just above the 0.015 limit (0.5*tolerance). The demonstrated changes are 0.91% (drag) and 0.52% (Strouhal), both below tolerance.
  - Domain is the only open component common to both quantities. The R0, R2 and R3 sequence has uneven ratios (1x, 2x, 3x). R2 and R3 have checkMesh_ok false, a coarser far field and only 6 cycles.
  - Budget: 5 of 6 experiments and 7.33 of 12.0 compute units used. This is the last experiment. EXPAND_DOMAIN factor 2.0 on R2 costs 3746 s, which fits. It gives a constant-ratio sequence R0, R2, R4x (1x, 2x, 4x) and tests whether the domain trend flattens.
  - One experiment cannot close both the drag mesh and the domain components. Domain is chosen because it affects both quantities and is the cheapest option. The drag mesh INCONCLUSIVE is likely driven by the dt confounding, not by a large spatial error.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K1_central_scheme.D2x-b0a7ed20bbb5 — Domain is the open component common to both quantities (drag 0.01575, Strouhal 0.0179, both marginally above 0.015). Expanding R2 by 2.0 gives cumulative 4x, within the limit. That makes a constant-ratio sequence (1x, 2x, 4x) and tests whether the trend flattens. It is cheap (3746 s) and fits the remaining budget. R3 is not allowed as parent (cumulative limit 4.0). R1 is not allowed (cell limit).
  - Outcome: executed -> K1_central_scheme.D2x-0c7e73f08a9e (completed)

Run K1_central_scheme.m2-325af4c14f68: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006111, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3365 (-0.29%).
  - Observation: strouhal_number 0.1633 → 0.16471 (+0.87%).

Run K1_central_scheme.D2x-b0a7ed20bbb5: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3311 (-0.69%).
  - Observation: strouhal_number 0.1633 → 0.16252 (-0.47%).

Run K1_central_scheme.D3x-14d3dc15d928: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3283 (-0.90%).
  - Observation: strouhal_number 0.1633 → 0.16246 (-0.51%).

Run K1_central_scheme.dt0.005-4f460bac38b7: REDUCE_TIME_STEP from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3373 (-0.23%).
  - Observation: strouhal_number 0.1633 → 0.16349 (+0.12%).

Run K1_central_scheme.m1.41-9a011a4052fe: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008642, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3388 (-0.12%).
  - Observation: strouhal_number 0.1633 → 0.16423 (+0.57%).

Run K1_central_scheme.D2x-0c7e73f08a9e: EXPAND_DOMAIN from K1_central_scheme.D2x-b0a7ed20bbb5 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3311 → 1.327 (-0.31%).
  - Observation: strouhal_number 0.16252 → 0.16233 (-0.12%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0191 vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K1_central_scheme-e4e5fb66bdca` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=4094 s; record: results/runs/K1_central_scheme-e4e5fb66bdca/run.json
- `K1_central_scheme.m2-325af4c14f68` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T04:38:25+00:00 wall=8379 s; record: results/runs/K1_central_scheme.m2-325af4c14f68/run.json
- `K1_central_scheme.D2x-b0a7ed20bbb5` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T16:16:09+00:00 wall=988.1 s; record: results/runs/K1_central_scheme.D2x-b0a7ed20bbb5/run.json
- `K1_central_scheme.D3x-14d3dc15d928` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T08:01:33+00:00 wall=1665 s; record: results/runs/K1_central_scheme.D3x-14d3dc15d928/run.json
- `K1_central_scheme.dt0.005-4f460bac38b7` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T03:41:02+00:00 wall=1455 s; record: results/runs/K1_central_scheme.dt0.005-4f460bac38b7/run.json
- `K1_central_scheme.m1.41-9a011a4052fe` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T09:33:11+00:00 wall=3361 s; record: results/runs/K1_central_scheme.m1.41-9a011a4052fe/run.json
- `K1_central_scheme.D2x-0c7e73f08a9e` status=completed parent=K1_central_scheme.D2x-b0a7ed20bbb5 created=2026-10-20T04:05:21+00:00 wall=1867 s; record: results/runs/K1_central_scheme.D2x-0c7e73f08a9e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3783580182.0, "relative_to_root": 8.248485245258339, "experiment_wall_seconds": 17715.466370598995, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.5817613899999999, "loop_wall_seconds": 5118.881600273999}
