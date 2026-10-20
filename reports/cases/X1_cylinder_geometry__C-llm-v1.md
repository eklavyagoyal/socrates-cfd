# Verification report: X1_cylinder_geometry (C-llm-v1)

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
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.76% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.01, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.94% > 1.50% but the demonstrated change 0.60% <= tau; more refinement would be needed [oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs=3]

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0176
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D1.5x-ba707c13ea01
    └── X1_cylinder_geometry.D2x-077be73cf4dd

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0194
    └── X1_cylinder_geometry-53f173b2191e
    └── X1_cylinder_geometry.D2x-bfc063153665
    └── X1_cylinder_geometry.D1.5x-ba707c13ea01
    └── X1_cylinder_geometry.D2x-077be73cf4dd

```

## EXPERIMENT HISTORY

Run X1_cylinder_geometry-53f173b2191e: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. The mesh, time and domain components are all unmeasured for both Cd and St, so I can't ACCEPT. Nothing supports a REJECT.
  - R0 passes the averaging and statistics components. Cd drift is 9.23e-05 and the Cd CI95 is 2.7463e-05. The St statistics uncertainty is 7.54e-05. These are far below the 0.03 tolerance, so sampling is not the limiting factor.
  - R0's mesh is coarse. It has 30580 cells, a representative cell size of 0.45745 D, a last wake cell of 1.0209 D, and 111 streamwise wake cells. The wake is poorly resolved, and the wake sets both the shedding frequency and the drag. A mesh error above 0.5*tolerance (1.5%) is plausible.
  - The reported St frequency resolution is 0.013333 against St = 0.15804. That is coarse relative to the 3 % tolerance. A finer mesh with its own St estimate will show whether St is mesh-sensitive.
  - Time-step and Courant evidence looks reasonable. dt is 0.01 D/U, max Courant is 0.70408, and there are 632.77 steps per shedding period. The scheme is second order (backward in time, linearUpwind in space). Time error is therefore less likely to dominate than mesh error.
  - The domain is large for an unbounded-stream assumption, with a blockage ratio of 0.0125, 30 D upstream, 50 D downstream and 40 D half-height. Domain error is unmeasured, but it is less likely to be the dominant error than the coarse wake mesh.
  - A mesh refinement of R0 is the most informative next step. It tests the component most likely to shift Cd or St by more than 3 %. Its cost is within budget: 0 of 6 experiments and 0 of 12x compute used, with an R0 mesh refinement estimated at 1683 s for the default factor.
  - Requested: REFINE_MESH {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Mesh error is unmeasured and is the most likely component to move Cd or St by more than the tolerance. The wake is coarse (last wake cell 1.0209 D, 30580 cells). A factor of 2.0 gives the largest allowed signal-to-noise for the first step of a refinement sequence, and the compute budget (12x root) can afford it.
  - Outcome: executed -> X1_cylinder_geometry.m2-4b1380d73d43 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.25

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, and nothing supports a REJECT.
  - Drag mesh component for R0 is now measured: 1.405% (R0 to R1 change 0.351%). That is within 0.5*tolerance (1.5%) and passes. The St mesh component is 3.56% against the 3% tolerance, so it is INCONCLUSIVE. The demonstrated R0-to-R1 St change is only 0.89%, but the estimate uses an assumed order p=2 with Fs=3, and only two mesh levels exist.
  - Time and domain components are still unmeasured for both Cd and St. Both are required for ACCEPT.
  - R0 to R1 is confounded. R1 used dt=0.0063913 against R0's 0.01 (R1 max Courant 0.74197, R0 0.70408), so the 0.351% Cd and 0.89% St changes mix mesh and time-step effects. A REDUCE_TIME_STEP run on R0 isolates the temporal effect and shows how much of the St change is temporal.
  - R0 averaging and statistics are solid: Cd CI95 2.7463e-05, drift 9.2298e-05, St statistics 7.54e-05. R1 has only 6 stationary cycles and a St frequency resolution of 0.025002. The R0 St frequency resolution is 0.013333.
  - Budget allows this: 1 of 6 experiments and 3.34 of 12x compute used. REDUCE_TIME_STEP on R0 is estimated at 1516 s, against 9486 s on R1. R0 is the cheaper parent and isolates time on the root mesh.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Time error is unmeasured for both quantities. It is also confounded with the R0 to R1 mesh comparison, because R1 used a smaller time step. Running it on R0 isolates the temporal effect on the root mesh at about 1516 s, against 9486 s for R1. It also shows how much of the St change seen in R1 is not mesh-related.
  - Outcome: executed -> X1_cylinder_geometry.dt0.005-e8d467b210a1 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no checks have failed. I can't ACCEPT, and nothing supports a REJECT.
  - Domain uncertainty is unmeasured for both mean_drag_coefficient and strouhal_number (no EXPAND_DOMAIN run). This blocks ACCEPT for both quantities, whatever the other components show.
  - R0 Cd components all pass. Averaging is 2.147e-05, statistics 9.23e-05, mesh 0.01405 (R0 to R1 change 0.351%) and time 0.0109 (R0 to R2 change 0.272%). Mesh and time are each below 0.5*tolerance (0.015), but only by a modest margin.
  - Strouhal time passes at 0.003328 (R0 to R2 change 0.083%). Strouhal mesh is INCONCLUSIVE at 0.0356. The observed R0 to R1 St change is only 0.89%, and the estimate comes from assumed order p=2 with Fs=3. R1 St is 0.15946 against R0's 0.15804.
  - The R0 domain is large: 30 D upstream, 50 D downstream, 40 D half-height, blockage 0.0125. The boundary treatment is not trivial, though: symmetryPlane lateral boundaries, zeroGradient inlet pressure and a fixedValue outlet pressure. Its effect on Cd and St is unmeasured, and it could be comparable to the 1.5% component budget.
  - EXPAND_DOMAIN on R0 costs about 1006 s, the cheapest informative option. Budget used is 2 of 6 experiments and 4.4 of 12x compute. After this run there is room for a third mesh level for St (REFINE_MESH on R0 at about 1683 s).
  - The expanded-domain run should come first. It closes a missing component for both quantities, and it could produce a FAIL that makes further mesh work moot.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X1_cylinder_geometry-53f173b2191e — Domain error is missing for both requested quantities and blocks ACCEPT regardless of the other components. R0 is the cheapest parent (about 1006 s, against 2012 s for R2). R1 is not allowed because the child mesh would exceed the cell limit. Running it first can also expose a FAIL early.
  - Outcome: executed -> X1_cylinder_geometry.D2x-bfc063153665 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, and there is nothing to support a REJECT.
  - Cd: the mesh component (0.01405) and the time component (0.0109) pass, but the domain component (0.04066) is INCONCLUSIVE. It is above 0.5*tolerance (1.5%) and the combined uncertainty is null.
  - St: the time component (0.003328) passes. The mesh component (0.0356) and the domain component (0.02715) are both INCONCLUSIVE.
  - Domain run R3 (60/100/80 D, blockage 0.00625) shifts Cd from 1.3941 (R0) to 1.3847, a 0.68% change. St moves from 0.15804 to 0.15732, a 0.45% change. Both changes are below tau=0.03, so there is no FAIL.
  - The domain uncertainty comes from a two-level estimate with an assumed order p=1 and Fs=3. R3's own noise is much larger than R0's: Cd ci95 0.0007818 against 2.7463e-05, and drift -0.0015793 against 9.2298e-05. The noise floor is 1.6e-03 for Cd and 1.4e-03 for St.
  - R3 is not a clean domain-only comparison. Its far-field mesh is coarser (last wake cell 1.9729 D against 1.0209 D, 40600 cells) and checkMesh_ok is false for R3. The 0.68% and 0.45% changes could include far-field mesh effects.
  - A third domain level is needed to measure the observed order. Expanding R3 by 1.5 gives 1x, 2x and 3x domains. For a 1/L-type truncation error the 2x-to-3x step is much smaller than the 1x-to-2x step, so the observed order can be read against R3's noise. A 1.5x step from R0 would give smaller, noisier differences.
  - Budget: 3 of 6 experiments used and 5.11 of 12x compute. EXPAND_DOMAIN on R3 is estimated at 1300 s, so the budget allows it and still leaves room for a third mesh level for the St mesh component.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on X1_cylinder_geometry.D2x-bfc063153665 — The domain component blocks ACCEPT for both Cd and St. The two-level estimate uses an assumed p=1 with R3's high noise, and R3 has a coarser far field and checkMesh_ok false. A third, larger domain level gives an observed convergence order and shows whether the domain effect is shrinking. A 3x domain gives a larger signal-to-noise ratio than a 1.5x step from R0. Estimated cost is about 1300 s, within budget.
  - Outcome: executed -> X1_cylinder_geometry.D1.5x-ba707c13ea01 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, and nothing supports a REJECT.
  - Cd: averaging 2.147e-05, statistics 9.23e-05, mesh 0.01405 and time 0.0109 all PASS. Only the domain component is INCONCLUSIVE, at 0.02097 against the 0.015 component limit (observed order p=0.76, Fs=1.25, three levels R0, R3, R4).
  - St: averaging, statistics and time (0.003328) PASS. Mesh (0.0356, two levels, assumed p=2) and domain (0.01743, observed p=0.57) are both INCONCLUSIVE.
  - Domain sequence for Cd: R0 1.3941 (30/50/40 D), R3 1.3847 (60/100/80 D), R4 1.3811 (90/150/120 D). The R3-to-R4 step is smaller than the R0-to-R3 step, so the effect is shrinking. St: R0 0.15804, R3 0.15732, R4 0.15702. Convergence is slow (p below 1), and that low order is what inflates the domain uncertainty.
  - R3 and R4 are noisier than R0. Cd drift is -0.0015793 in R3 and -0.0015517 in R4, against 9.2298e-05 in R0. Both have 6 stationary cycles and window starts at the MSER cap. Both have checkMesh_ok=false and a coarser far field (last wake cell 1.9729 D in R3, 2.9337 D in R4, against 1.0209 D in R0). These are confounds for the domain order estimate.
  - EXPAND_DOMAIN on R4 is not allowed (cumulative factor limit 4.0). R3 with factor 2.0 reaches exactly the cumulative limit of 4.0 and gives a 4x domain level (R0 at 1x, R3 at 2x, new run at 4x, constant ratio 2). That is a cleaner sequence for the order than the 1x, 2x, 3x set. It tests whether the Cd and St changes keep shrinking.
  - Domain blocks ACCEPT for both quantities, so it comes before the St mesh third level. Budget: 4 of 6 experiments and 5.94 of 12x compute used, so two experiments remain. This domain run (about 1300 s estimated on R3) leaves room for one REFINE_MESH on R0 (about 1683 s) for the St mesh order.
  - All demonstrated changes are below tau=0.03, so no FAIL is expected. The open question is whether the uncertainty estimates can be brought within 0.5*tolerance with measured orders.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X1_cylinder_geometry.D2x-bfc063153665 — Domain uncertainty blocks ACCEPT for both Cd (0.02097) and St (0.01743). EXPAND_DOMAIN on R4 is not allowed because of the cumulative limit of 4.0. R3 with factor 2.0 reaches a 4x domain, giving a constant-ratio sequence (1x, 2x, 4x) for a better-determined observed order. It costs about 1300 s and is affordable within the remaining budget.
  - Outcome: executed -> X1_cylinder_geometry.D2x-077be73cf4dd (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, and no measured FAIL supports a REJECT.
  - Cd: averaging 2.147e-05, statistics 9.23e-05, mesh 0.01405 and time 0.0109 all PASS. Only the domain component is INCONCLUSIVE, at 0.01762 against the 0.015 component limit (three-level Celik, observed p=1.01, Fs=1.25, runs R0, R3, R4, R5).
  - St: averaging 4.791e-06, statistics 7.54e-05 and time 0.003328 PASS. Mesh (0.0356) and domain (0.01937) are both INCONCLUSIVE.
  - The St mesh estimate rests on two levels (R0, R1) with assumed p=2 and Fs=3. The demonstrated R0-to-R1 St change is small: 0.15804 to 0.15946, or 0.89%. A third level would give an observed order. That is the only way to replace the assumed-order 0.0356.
  - Domain sequence for Cd: R0 1.3941 (30/50/40 D), R3 1.3847 (60/100/80 D), R4 1.3811 (90/150/120 D), R5 1.3795 (120/200/160 D). St: 0.15804, 0.15732, 0.15702, 0.15709. The Cd steps shrink. The St sequence is oscillatory, so the verifier falls back to a range-based estimate with Fs=3.
  - R3, R4 and R5 are noisier than R0. Cd drift is -0.0015793, -0.0015517 and -0.0018255, against 9.2298e-05 for R0. All three have checkMesh_ok=false and a coarser far field. This limits what further domain runs can show.
  - EXPAND_DOMAIN is not allowed from R4 or R5 because of the cumulative factor limit of 4.0. The domain sequence already has four levels, and another level cannot be expected to clear the 0.015 limit.
  - Budget: 5 of 6 experiments and 6.85 of 12x compute are used. Exactly one experiment remains. REFINE_MESH on R0 is estimated at 1683 s, about 1.2x the root cost of 1420.9 s, so it is affordable.
  - I expect one run cannot close every blocker. St domain would still be INCONCLUSIVE. A mesh-order measurement is still the most informative use of the last run. It replaces the largest single estimate in the package (0.0356, from an assumed order and two levels) with a measured one. It also tests whether R0's mesh error is stable.
  - Requested: REFINE_MESH {'factor': 1.4142} on X1_cylinder_geometry-53f173b2191e — The St mesh component is estimated from two levels with an assumed order (0.0356 against the 0.015 limit). It is the largest unmeasured-order uncertainty in the package. Running it on R0 with factor 1.4142 gives a constant-ratio three-level sequence with R1, and an observed order for both St and Cd. R0 is the cheapest parent (1683 s). EXPAND_DOMAIN has no more allowed parents, apart from R0, R2 and R3, and the domain sequence already has four levels.
  - Outcome: executed -> X1_cylinder_geometry.m1.41-fd9653d19a94 (completed)

Run X1_cylinder_geometry.m2-4b1380d73d43: REFINE_MESH from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006391, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.399 (+0.35%).
  - Observation: strouhal_number 0.15804 → 0.15946 (+0.90%).

Run X1_cylinder_geometry.dt0.005-e8d467b210a1: REDUCE_TIME_STEP from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3903 (-0.27%).
  - Observation: strouhal_number 0.15804 → 0.15817 (+0.08%).

Run X1_cylinder_geometry.D2x-bfc063153665: EXPAND_DOMAIN from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3847 (-0.67%).
  - Observation: strouhal_number 0.15804 → 0.15732 (-0.45%).

Run X1_cylinder_geometry.D1.5x-ba707c13ea01: EXPAND_DOMAIN from X1_cylinder_geometry.D2x-bfc063153665 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3847 → 1.3811 (-0.26%).
  - Observation: strouhal_number 0.15732 → 0.15702 (-0.19%).

Run X1_cylinder_geometry.D2x-077be73cf4dd: EXPAND_DOMAIN from X1_cylinder_geometry.D2x-bfc063153665 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3847 → 1.3795 (-0.38%).
  - Observation: strouhal_number 0.15732 → 0.15709 (-0.15%).

Run X1_cylinder_geometry.m1.41-fd9653d19a94: REFINE_MESH from X1_cylinder_geometry-53f173b2191e (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.009039, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3941 → 1.3988 (+0.34%).
  - Observation: strouhal_number 0.15804 → 0.159 (+0.61%).

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
- `X1_cylinder_geometry.dt0.005-e8d467b210a1` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-20T01:15:35+00:00 wall=1156 s; record: results/runs/X1_cylinder_geometry.dt0.005-e8d467b210a1/run.json
- `X1_cylinder_geometry.D2x-bfc063153665` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T22:11:23+00:00 wall=1034 s; record: results/runs/X1_cylinder_geometry.D2x-bfc063153665/run.json
- `X1_cylinder_geometry.D1.5x-ba707c13ea01` status=completed parent=X1_cylinder_geometry.D2x-bfc063153665 created=2026-10-20T01:16:51+00:00 wall=1150 s; record: results/runs/X1_cylinder_geometry.D1.5x-ba707c13ea01/run.json
- `X1_cylinder_geometry.D2x-077be73cf4dd` status=completed parent=X1_cylinder_geometry.D2x-bfc063153665 created=2026-10-20T03:41:01+00:00 wall=1891 s; record: results/runs/X1_cylinder_geometry.D2x-077be73cf4dd/run.json
- `X1_cylinder_geometry.m1.41-fd9653d19a94` status=completed parent=X1_cylinder_geometry-53f173b2191e created=2026-10-19T18:32:11+00:00 wall=2137 s; record: results/runs/X1_cylinder_geometry.m1.41-fd9653d19a94/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3687157906.0, "relative_to_root": 8.038277536516242, "experiment_wall_seconds": 14108.697553363001, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.60780896, "loop_wall_seconds": 1924.169558408}
