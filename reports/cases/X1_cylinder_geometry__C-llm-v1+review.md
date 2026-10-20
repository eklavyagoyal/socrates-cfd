# Verification report: X1_cylinder_geometry (C-llm-v1+review)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3941
- strouhal_number: 0.15804

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.70 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 9.23e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 7.54e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.09% <= 1.50% (root-to-finest change 0.351%) [three-level, observed order 9.87 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.43% <= 1.50% (root-to-finest change 0.890%) [three-level Celik procedure, observed order p=2.17, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.09% <= 1.50% (root-to-finest change 0.272%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.33% <= 1.50% (root-to-finest change 0.083%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.10% > 1.50% but the demonstrated change 0.94% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.76, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.74% > 1.50% but the demonstrated change 0.65% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.57, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X1_cylinder_geometry-53f173b2191e is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mesh_quality: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mass_conservation: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── linear_solver_convergence: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── courant_number: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── reynolds_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── force_reference_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── physics_regime: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── convection_scheme_order: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── Averaging window (reported vs stationary value): PASS U=2.15e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Temporal statistics (stationarity, cycles): PASS U=9.23e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Spatial discretisation (mesh sensitivity): PASS U=0.0109
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.m1.41-fd9653d19a94
│   └── X1_cylinder_geometry.m2-4b1380d73d43
├── Temporal discretisation (time-step sensitivity): PASS U=0.0109
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.dt0.005-e8d467b210a1
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.021
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D1.5x-ba707c13ea01

CLAIM: strouhal_number of run X1_cylinder_geometry-53f173b2191e is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mesh_quality: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── mass_conservation: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── linear_solver_convergence: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── courant_number: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── reynolds_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── force_reference_consistency: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── physics_regime: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── convection_scheme_order: PASS
│   └── X1_cylinder_geometry-53f173b2191e
├── Averaging window (reported vs stationary value): PASS U=4.79e-06
│   └── X1_cylinder_geometry-53f173b2191e
├── Temporal statistics (stationarity, cycles): PASS U=7.54e-05
│   └── X1_cylinder_geometry-53f173b2191e
├── Spatial discretisation (mesh sensitivity): PASS U=0.0143
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.m1.41-fd9653d19a94
│   └── X1_cylinder_geometry.m2-4b1380d73d43
├── Temporal discretisation (time-step sensitivity): PASS U=0.00333
│   └── X1_cylinder_geometry-53f173b2191e
│   └── X1_cylinder_geometry.dt0.005-e8d467b210a1
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0174
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D1.5x-ba707c13ea01

```

## EXPERIMENT HISTORY

Run X1_cylinder_geometry-53f173b2191e: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. Mesh, time and domain uncertainty are all unmeasured for both mean_drag_coefficient and strouhal_number, so ACCEPT is not allowed. Nothing invalidates R0, so REJECT is not allowed either.
  - R0 is clean on the checks that were run. The solver completed, max Courant is 0.70408, mass imbalance is 8.3333e-11, and the Re=100 and force-reference checks pass. The averaging and statistics components are tiny: Cd drift is 9.2298e-05 relative and Cd ci95 is 2.7463e-05 over 12 cycles.
  - The mesh is the most likely source of an error larger than the 3% tolerance. R0 has only 30580 cells, with representative_cell_size_D 0.45745 and wake_last_cell_D 1.0209 over 111 streamwise wake cells. The wake is coarse, and Strouhal number and mean drag depend on how well the near wake is resolved. Strouhal frequency resolution is 0.013333, against a reported St of 0.15804.
  - Time error is less worrying but unmeasured. The time step is 0.01 convective units with 632.77 steps per shedding period, and the scheme is backward. Domain error is also unmeasured. Blockage is 0.0125, with 30D upstream, 50D downstream and 40D half-height, so a boundary effect is plausible but probably smaller than a mesh effect.
  - The stationary window start (73.434) is at the MSER cap, but drift and half-difference are about 1e-4 or less. Run length is not the first priority.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 compute units used. A refinement factor of 2.0 gives the clearest signal above noise. The 947-1683 s menu costs are small against the budget.
  - Requested: REFINE_MESH {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Mesh resolution is the most likely unmeasured error source. R0 has 30580 cells and a coarse wake (wake_last_cell_D 1.0209). Averaging and statistical uncertainties are already negligible, so the remaining risk is in discretisation and domain. A factor of 2.0 gives the largest refinement the menu allows and so the clearest signal above noise.
  - Outcome: executed -> X1_cylinder_geometry.m2-4b1380d73d43 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and nothing invalidates R0, so REJECT is not allowed either.
  - R0 is clean on the checks that ran. Cd drift is 9.2298e-05, the Cd ci95 is 2.7463e-05 over 12 cycles, max Courant is 0.70408 and mass imbalance is 8.3333e-11.
  - R1 (REFINE_MESH, 122320 cells) changes Cd from 1.3941 to 1.399, a root-to-finest change of 0.351%. The Cd mesh uncertainty is 0.01405, which is within 0.5*tolerance (0.015).
  - R1 changes St from 0.15804 to 0.15946, a change of 0.89%. The St mesh component is 0.0356 and is INCONCLUSIVE. It rests on an assumed order p=2 with two levels only.
  - Another refinement of R1 is not allowed, because cumulative refinement 2.83 exceeds the limit of 2.0. A third mesh level would have to be a milder refinement of R0.
  - Time and domain components are unmeasured for both Cd and St. Even a perfect mesh result could not give ACCEPT without them.
  - The domain is the cheapest unmeasured item (R0 cost 1006 s). The root uses a 0.0125 blockage with symmetryPlane lateral boundaries, 30D upstream and 50D downstream. The problem says to treat the stream as unbounded. The St mesh question is already partly bounded by the demonstrated 0.89% change, so the domain is the less-bounded risk.
  - Budget is ample: 1 of 6 experiments and 3.34 of 12 compute units used. A domain run (about 0.7 root units) fits, and time-step and further mesh runs remain affordable afterward.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Domain truncation is unmeasured for both quantities, and the problem requires an unbounded stream. EXPAND_DOMAIN is the cheapest menu item (1006 s on R0) and is not allowed on R1. Expanding R0 keeps the near-field mesh unchanged, so the comparison isolates the boundary effect.
  - Outcome: executed -> X1_cylinder_geometry.D2x-bfc063153665 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because time and domain are unmeasured for Cd and St, and mesh is unresolved for St. REJECT is not allowed because nothing invalidates R0.
  - R0 is clean on the checks that ran. Cd drift is 9.2298e-05, the Cd ci95 is 2.7463e-05 over 12 cycles, max Courant is 0.70408 and mass imbalance is 8.3333e-11.
  - R1 (REFINE_MESH) gives Cd 1.399 against 1.3941 for R0, a 0.351% change. The Cd mesh uncertainty is 0.01405, within 0.5*tolerance (0.015). St moves from 0.15804 to 0.15946, a 0.89% change, but the St mesh uncertainty is 0.0356 (INCONCLUSIVE) because it rests on assumed p=2 with two levels.
  - R2 (EXPAND_DOMAIN) gives Cd 1.3847 against 1.3941 for R0, a 0.68% change. St is 0.15732 against 0.15804, a 0.45% change. Both changes are below the 3% tolerance, but the verifier's two-level estimates with assumed p=1 are 0.04066 for Cd and 0.02715 for St. The Cd estimate alone exceeds the 0.03 tolerance, so the domain component is the largest blocker to ACCEPT.
  - The R2 domain signal is confounded. R2 has checkMesh_ok false. Its wake is also coarser than R0: representative_cell_size_D 0.79405 against 0.45745, and wake_last_cell_D 1.9729 against 1.0209. R2 St is lower than R0 St, and R0 St is lower than R1 St. That ordering is consistent with a coarser-mesh effect as well as a domain effect. R2 also has only 6 cycles and Cd drift of -0.0015793, so its statistics are weaker than R0's.
  - The next experiment is a third nested domain level. Expanding R2 by 1.5 keeps R2's near-field mesh and gives a 3x-R0 domain. That lets the verifier measure the domain convergence order instead of assuming p=1. The cost is 1300 s on R2.
  - Budget is ample: 2 of 6 experiments and 4.05 of 12 compute units used. The time-step run and a third mesh level can still be afforded afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on X1_cylinder_geometry.D2x-bfc063153665 — The domain component is the largest unresolved blocker. The Cd estimate of 0.04066 exceeds the 0.03 tolerance, and the St estimate is 0.02715. Both come from two levels with assumed p=1. The R0-to-R2 comparison is also confounded by R2's coarser wake and by its checkMesh_ok false. Expanding R2 by 1.5 gives a third nested level that keeps the near-field mesh, so the domain order can be measured. The cost is 1300 s.
  - Outcome: executed -> X1_cylinder_geometry.D1.5x-ba707c13ea01 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because the time component is unmeasured for both Cd and St, and the domain and St mesh components are INCONCLUSIVE. REJECT is not allowed because nothing invalidates R0.
  - R0 is clean on the checks that ran. Cd drift is 9.2298e-05, the Cd ci95 is 2.7463e-05 over 12 cycles, max Courant is 0.70408, and mass imbalance is 8.3333e-11.
  - Mesh: R1 gives Cd 1.399 against 1.3941 for R0 (0.351% change). The Cd mesh uncertainty is 0.01405, which PASSES. R1 gives St 0.15946 against 0.15804 (0.89% change). The St mesh uncertainty of 0.0356 is INCONCLUSIVE because it rests on two levels and an assumed p=2. R1 cannot be refined further, since cumulative refinement 2.83 exceeds the limit of 2.0.
  - Domain: Cd is 1.3941 (R0), 1.3847 (R2) and 1.3811 (R3). The successive changes are 0.68% and then 0.26%, so the shift is shrinking. St is 0.15804, 0.15732 and 0.15702. The observed orders are low (Cd p=0.76, St p=0.57), so the Celik estimates are Cd 0.02097 and St 0.01743, both above 0.015. These estimates rest on noisy 6-cycle runs. R2 and R3 also have coarser wakes (representative_cell_size_D 0.79405 and 1.1025 against 0.45745) and checkMesh_ok false. The domain signal is therefore confounded with mesh coarsening. R3 is at the cumulative domain factor limit, so another domain experiment cannot add much.
  - Time: no REDUCE_TIME_STEP run exists. R0 uses dt=0.01 convective units with 632.77 steps per period, and max Courant is 0.70408. Temporal error is an unmeasured component for both quantities, and ACCEPT is impossible without it. It is also the only missing component with a clean, uncontaminated experiment still available.
  - Budget: 3 of 6 experiments and 4.87 of 12 compute units are used. REDUCE_TIME_STEP on R0 costs 1516 s, which is about one root unit, so it is affordable. It leaves room for one more mesh or domain run afterwards.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Time-step error is the only uncertainty component with no measurement at all for either quantity, so no ACCEPT is possible without it. The domain and mesh components already have several runs. Further domain expansion is nearly exhausted, since R3 is at the cumulative factor limit of 4.0, and the R2 and R3 comparisons are confounded by coarser meshes. R0 is the root and shares its mesh with the child, so the comparison isolates temporal error. The cost is 1516 s, about one root unit.
  - Outcome: executed -> X1_cylinder_geometry.dt0.005-e8d467b210a1 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.68%, 0.26%

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because the St mesh component and the domain components for Cd and St are INCONCLUSIVE. REJECT is not allowed because nothing invalidates R0.
  - R0 is clean on the checks that ran. Cd drift is 9.2298e-05, the Cd ci95 is 2.7463e-05 over 12 cycles, max Courant is 0.70408 and mass imbalance is 8.3333e-11.
  - Time is now measured and passes. R4 (dt 0.005) gives Cd 1.3903 against 1.3941 for R0, and St 0.15817 against 0.15804. The time uncertainties are Cd 0.0109 and St 0.003328, both at or below 0.015.
  - Cd mesh passes at 0.01405. The R0 to R1 change is 0.351%, and Cd is 1.3941 for R0 and 1.399 for R1.
  - St mesh is INCONCLUSIVE at 0.0356. R1 moves St from 0.15804 to 0.15946 (0.89%), but the estimate is a two-level Richardson with an assumed order p=2. R1 cannot be refined further (cumulative refinement limit 2.0). A third level is needed to measure the St order.
  - Domain is INCONCLUSIVE for both quantities. Cd is 1.3941 (R0), 1.3847 (R2) and 1.3811 (R3). St is 0.15804, 0.15732 and 0.15702. The observed orders are low (Cd p=0.76, St p=0.57), giving Cd 0.02097 and St 0.01743, both above 0.015.
  - The domain shift is shrinking but is confounded. R2 and R3 have checkMesh_ok false and coarser meshes (representative_cell_size_D 0.79405 and 1.1025 against 0.45745 for R0). They also have only 6 cycles. Further domain expansion is not allowed on R3 (cumulative limit 4.0), and no menu action fixes the confounding directly.
  - Budget: 4 of 6 experiments and 5.94 of 12 compute units are used. Two experiments remain. A third mesh level on R0 costs 1683 s, about 1.2 root units. The St mesh component is the only blocker with a clean, uncontaminated experiment available. Cd and St mesh estimates then improve together.
  - The remaining experiment after this one can go to the domain component, for example EXPAND_DOMAIN on R0 at 1.5. The cumulative budget allows both.
  - Requested: REFINE_MESH {'factor': 1.4142} on X1_cylinder_geometry-53f173b2191e — The St mesh component is INCONCLUSIVE because it rests on two levels and an assumed p=2 (0.0356 against a 0.015 budget share). R1 cannot be refined further. A geometrically intermediate level on R0 gives a third mesh level, so the St (and Cd) observed order can be measured instead of assumed. It costs 1683 s, so the budget still leaves one experiment for the domain component.
  - Outcome: executed -> X1_cylinder_geometry.m1.41-fd9653d19a94 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not allowed because nothing invalidates R0.
  - R0 is clean on the checks that ran. Cd drift is 9.2298e-05, Cd ci95 is 2.7463e-05 over 12 cycles, max Courant is 0.70408 and mass imbalance is 8.3333e-11.
  - Averaging, statistics, mesh and time all PASS for both quantities. Cd: mesh 0.01087, time 0.0109. St: mesh 0.01425, time 0.003328. R5 supplied the third mesh level, so the St mesh estimate now has a measured order (p=2.17).
  - Domain is the only INCONCLUSIVE component. Cd domain uncertainty is 0.02097 and St is 0.01743, both above the 0.015 budget share. The demonstrated changes are 0.94% for Cd and 0.65% for St, both below the 0.03 tolerance.
  - The domain trend is monotone and shrinking. Cd is 1.3941 (R0), 1.3847 (R2), 1.3811 (R3). St is 0.15804, 0.15732, 0.15702. The observed orders are low (Cd p=0.76, St p=0.57), so the Celik estimates are large.
  - R2 and R3 are confounded. Both have checkMesh_ok false, coarser meshes (representative_cell_size_D 0.79405 and 1.1025 against 0.45745) and only 6 cycles. R0, R2 and R3 also differ in mesh, so part of the 0.94% shift may not be a domain effect.
  - An EXPAND_DOMAIN run on R0 keeps R0's near-field mesh, which passed checkMesh, and changes only the boundary distances. Comparing it with R0 and with R3 separates the real boundary effect from the mesh-coarsening effect.
  - Budget: 5 of 6 experiments and 7.12 of 12 compute units are used, so one experiment remains. EXPAND_DOMAIN on R0 is estimated at 1006 s, which fits.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on X1_cylinder_geometry-53f173b2191e — Domain is the only blocker. R2 and R3 are confounded by coarser meshes and checkMesh_ok false. Expanding R0 by 3.0 gives the same boundary distances as R3 but keeps R0's near-field mesh. This gives a clean root-to-large-domain comparison and shows how much of the R0-to-R3 shift is mesh-related. It fits within budget (R0 expand estimate 1006 s).
  - Outcome: executed -> X1_cylinder_geometry.D3x-72b5700b7a9e (completed)

Run X1_cylinder_geometry.m2-4b1380d73d43: REFINE_MESH from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006391, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.399 (+0.35%).
  - Observation: strouhal_number 0.15804 → 0.15946 (+0.90%).

Run X1_cylinder_geometry.D2x-bfc063153665: EXPAND_DOMAIN from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3847 (-0.67%).
  - Observation: strouhal_number 0.15804 → 0.15732 (-0.45%).

Run X1_cylinder_geometry.D1.5x-ba707c13ea01: EXPAND_DOMAIN from X1_cylinder_geometry.D2x-bfc063153665 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3847 → 1.3811 (-0.26%).
  - Observation: strouhal_number 0.15732 → 0.15702 (-0.19%).

Run X1_cylinder_geometry.dt0.005-e8d467b210a1: REDUCE_TIME_STEP from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3903 (-0.27%).
  - Observation: strouhal_number 0.15804 → 0.15817 (+0.08%).

Run X1_cylinder_geometry.m1.41-fd9653d19a94: REFINE_MESH from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.009039, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3988 (+0.34%).
  - Observation: strouhal_number 0.15804 → 0.159 (+0.61%).

Run X1_cylinder_geometry.D3x-72b5700b7a9e: EXPAND_DOMAIN from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3822 (-0.85%).
  - Observation: strouhal_number 0.15804 → 0.15712 (-0.58%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X1_cylinder_geometry-53f173b2191e` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=1421 s; record: results/runs/X1_cylinder_geometry-53f173b2191e/run.json
- `X1_cylinder_geometry.m2-4b1380d73d43` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T18:32:36+00:00 wall=6740 s; record: results/runs/X1_cylinder_geometry.m2-4b1380d73d43/run.json
- `X1_cylinder_geometry.D2x-bfc063153665` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T22:11:23+00:00 wall=1034 s; record: results/runs/X1_cylinder_geometry.D2x-bfc063153665/run.json
- `X1_cylinder_geometry.D1.5x-ba707c13ea01` status=completed parent=X1_cylinder_geometry.D2x-bfc063153665 created=2026-10-20T01:16:51+00:00 wall=1150 s; record: results/runs/X1_cylinder_geometry.D1.5x-ba707c13ea01/run.json
- `X1_cylinder_geometry.dt0.005-e8d467b210a1` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-20T01:15:35+00:00 wall=1156 s; record: results/runs/X1_cylinder_geometry.dt0.005-e8d467b210a1/run.json
- `X1_cylinder_geometry.m1.41-fd9653d19a94` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T18:32:11+00:00 wall=2137 s; record: results/runs/X1_cylinder_geometry.m1.41-fd9653d19a94/run.json
- `X1_cylinder_geometry.D3x-72b5700b7a9e` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-20T03:43:49+00:00 wall=1531 s; record: results/runs/X1_cylinder_geometry.D3x-72b5700b7a9e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3647781906.0, "relative_to_root": 7.952434937867888, "experiment_wall_seconds": 13748.134977570002, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.59226866, "loop_wall_seconds": 7191.082324749999}
