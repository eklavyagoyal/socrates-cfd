# Verification report: C2_euler_large_timestep (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2901
- strouhal_number: 0.15849

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 2.92 with 2 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.66e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.27e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 3.72% > 1.50% but the demonstrated change 1.81% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.66, Fs=1.25]
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 4.15% > 1.50% but the demonstrated change 2.36% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.88, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.27% > 1.50% but the demonstrated change 0.71% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.7e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.72% > 1.50% but the demonstrated change 0.45% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.6e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=9.49e-07
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal statistics (stationarity, cycles): PASS U=0.000166
│   └── C2_euler_large_timestep-268eddd71f94
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0372
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0427
    └── C2_euler_large_timestep-268eddd71f94
    └── C2_euler_large_timestep.D2x-a912f88e2d43

CLAIM: strouhal_number of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=1.57e-05
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal statistics (stationarity, cycles): PASS U=0.000127
│   └── C2_euler_large_timestep-268eddd71f94
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0415
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0272
    └── C2_euler_large_timestep-268eddd71f94
    └── C2_euler_large_timestep.D2x-a912f88e2d43

```

## EXPERIMENT HISTORY

Run C2_euler_large_timestep-268eddd71f94: submitted simulation (30580 cells, dt=0.04 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - R0 passes the numerical-hygiene checks: solver completed, checkMesh OK, mass imbalance 2.5e-10, final linear residual max 9.999e-08, and Re consistent at 100.
  - R0 passes the averaging and statistics components for both quantities. Drag statistics uncertainty is 0.0001664 and Strouhal statistics uncertainty is 0.0001267, against a tolerance of 0.03. There are 12 stationary cycles.
  - Three uncertainty components are unmeasured for both quantities: mesh, time and domain. No combined uncertainty can be formed.
  - Mesh is the largest unmeasured risk. R0 has 30580 cells, representative cell size 0.45745 D and wake_last_cell_D 1.0209. The wake is coarse in the far field, where shedding vortices are advected and dissipated, and this could shift Strouhal number and drag.
  - Time is also unmeasured. The check is INCONCLUSIVE: max Courant is 2.9248 with Euler time stepping and dt = 0.04. There are 157.74 steps per shedding period.
  - Domain is the least worrying. R0 has 30 D upstream, 50 D downstream, 40 D half-height and blockage ratio 0.0125, but it is still unmeasured.
  - Stationary-window start 73.298 is flagged as the MSER cap. Drift is small (mean_drag_coefficient_drift_rel 0.00016636), so this is a lower-priority concern.
  - REFINE_MESH on R0 is chosen first. It costs about the same as the time-step experiment (1130 s vs 1126 s) and fits the budget (0 of 6 experiments used).
  - Requested: REFINE_MESH {'factor': 1.4142} on C2_euler_large_timestep-268eddd71f94 — Mesh error is unmeasured and R0's grid is coarse in the wake (last wake cell 1.0209 D, representative size 0.45745 D). This is the experiment most likely to shift drag or Strouhal number by more than the 3% tolerance. Time and domain checks remain for later iterations.
  - Outcome: executed -> C2_euler_large_timestep.m1.41-eb9ef468444b (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not justified, because R1 is a numerical blow-up and not a measured change in Cd or St.
  - R0 passes the hygiene, averaging and statistics checks. Mass imbalance is 2.5e-10. There are 12 stationary cycles. Drag statistics uncertainty is 0.0001664 and Strouhal statistics uncertainty is 0.0001267, against a tolerance of 0.03.
  - R1 (REFINE_MESH from R0) did not complete. It stopped after 73 time steps, with max Courant 3.1978e+103 and mass imbalance 1.8456e+76. It produced no usable Cd or St, so the mesh component is still unmeasured.
  - R1 kept time_step_convective_units at 0.04, the same as R0. Its representative cell size fell from 0.45745 D to 0.32292 D, and its wall-first-cell size from 0.005 D to 0.0035832 D. R0 already ran at max Courant 2.9248 with 2 outer correctors, so R1 plausibly ran at a higher Courant number. I cannot prove this from the package, because R1 recorded no pre-divergence Courant value.
  - Repeating REFINE_MESH at the same dt would probably blow up again. R1 cannot be a parent for REFINE_MESH or REDUCE_TIME_STEP in a useful way, since RUN_LONGER on R1 is explicitly not allowed and its cost is about double.
  - The time component is unmeasured. The courant_number check is INCONCLUSIVE at 2.925. A time-step reduction from R0 measures the temporal error directly. It also tests whether R0's large Courant number is the suspected cause of the R1 divergence. It is cheap (1126 s) and uses a mesh already known to be stable.
  - Budget: 1 of 6 experiments used, and relative compute used is 0.04 of 12. There is room for more experiments.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — R1 (REFINE_MESH) blew up at the unchanged dt of 0.04, so the mesh component cannot be measured until the time-step stability margin is understood. R0 runs at max Courant 2.9248, and its time error is unmeasured. Halving dt on R0's known-stable mesh measures the temporal error directly. It is cheap at 1126 s, and it tests the cause of the R1 failure.
  - Outcome: executed -> C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not justified, because no demonstrated change exceeds the 0.03 tolerance.
  - R0 passes hygiene, averaging and statistics checks: mass imbalance 2.5e-10, 12 stationary cycles, drag statistics uncertainty 0.0001664 and Strouhal statistics uncertainty 0.0001267.
  - R1 (REFINE_MESH from R0) did not complete: 73 steps, max Courant 3.1978e+103. It gave no Cd or St, so the mesh component is still unmeasured.
  - R2 (REDUCE_TIME_STEP, dt 0.04 -> 0.02, same mesh) completed with max Courant 1.1744. This supports the view that R0's max Courant 2.9248 was close to the stable limit.
  - R2 differs from R0 in Cd (1.2901 -> 1.3047, demonstrated change 1.11%) and in St (0.15849 -> 0.16097, demonstrated change 1.54%). Both changes are below tau, but they are not negligible next to the 1.5% per-component budget.
  - The verifier's two-level Richardson estimate assumes order p=1 and gives time uncertainty of 0.06683 for Cd and 0.09224 for St. Both are far above the 1.5% component limit. Two time levels cannot show whether the sequence is converging or what the observed order is.
  - Mesh and domain are still unmeasured for both quantities, so no combined uncertainty can be formed.
  - A further halving of dt on R2 gives three levels (0.04, 0.02, 0.01). That allows an observed convergence order and a justified time uncertainty. R2 is also the stable baseline for a later REFINE_MESH, because R1 diverged at R0's dt.
  - Budget: 2 of 6 experiments used, and relative compute used is 1.11 of 12. The listed cost of 2252 s is affordable.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — R0 to R2 showed a St change of 1.54% and a Cd change of 1.11%. Two levels with an assumed order p=1 give time uncertainty of 0.09224 (St) and 0.06683 (Cd), which cannot be resolved without a third level. Continuing the dt sequence from R2 (dt 0.02 -> 0.01) gives an observed order. It also provides a time-converged baseline for the mesh study that follows.
  - Outcome: executed -> C2_euler_large_timestep.dt0.01-f9cf9b35455e (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and REJECT is not allowed because there is no deterministic FAIL.
  - R0 passes the hygiene, averaging and statistics checks. Mass imbalance is 2.5e-10, there are 12 stationary cycles, drag statistics uncertainty is 0.0001664 and Strouhal statistics uncertainty is 0.0001267.
  - The time sequence is now three levels. R0 (dt 0.04), R2 (dt 0.02) and R3 (dt 0.01) give Cd 1.2901, 1.3047, 1.3139 and St 0.15849, 0.16097, 0.16232.
  - The step-to-step changes shrink but slowly. Observed order is p=0.66 for Cd and p=0.88 for St, so R3 is not yet time-converged.
  - The verifier gives time uncertainty for R0 of 0.03719 (Cd) and 0.04147 (St). Both are above the 0.015 component limit and above the 0.03 tolerance. The demonstrated R0-to-R3 changes are 1.81% (Cd) and 2.36% (St), both within tau, so the check is INCONCLUSIVE and not FAIL. This is a strong warning about R0 as submitted, but I cannot overrule the verifier.
  - A fourth dt level (R3 to dt 0.005) would cost 4504 s. The recorded trend suggests it would sharpen the time estimate but not remove the time component, and it would use about 4.3 of the 8.76 root-cost units of compute left.
  - The mesh component is still unmeasured for both quantities. R1 (REFINE_MESH from R0) diverged at the unchanged dt 0.04, with max Courant 3.1978e+103 and 73 steps, so it gave no data.
  - R2 completed at max Courant 1.1744. It is a stable parent for a mesh refinement, because the refined mesh will have a higher Courant number at the same dt. REFINE_MESH from R2 costs 2260 s, half the cost of R3 as parent.
  - The domain component is also unmeasured. EXPAND_DOMAIN from R0 is the cheapest experiment at 748 s and can follow.
  - Budget: 3 of 6 experiments used and 3.24 of 12 compute units used. The mesh refinement and a domain expansion both fit.
  - Requested: REFINE_MESH {'factor': 1.4142} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — Mesh error is the largest unmeasured component for both Cd and St. The only earlier attempt (R1 from R0) diverged at dt 0.04. R2 (dt 0.02, max Courant 1.1744) is a stable baseline and costs 2260 s, half the cost of R3 as parent. Another time halving would cost 4504 s and would only refine an estimate that already exceeds the 0.015 component limit.
  - Outcome: executed -> C2_euler_large_timestep.m1.41-9ec9f782d7ff (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 4.3, 8.76

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed, because there is no deterministic FAIL.
  - R0 passes the hygiene, averaging and statistics checks. Mass imbalance is 2.5e-10 and there are 12 stationary cycles. Drag statistics uncertainty is 0.0001664 and Strouhal statistics uncertainty is 0.0001267.
  - The time sequence has three levels. R0 (dt 0.04), R2 (dt 0.02) and R3 (dt 0.01) give Cd 1.2901, 1.3047, 1.3139 and St 0.15849, 0.16097, 0.16232. Observed order is p=0.66 for Cd and p=0.88 for St. Time uncertainty for R0 is 0.03719 (Cd) and 0.04147 (St). Both are above the 0.015 component limit. The demonstrated changes of 1.81% and 2.36% are within tau, so the check is INCONCLUSIVE and not FAIL.
  - R4 (REFINE_MESH from R2) is flagged as completed but its output is not physical. Cd is 0.29242, St is 25.0 and rms Cl is 3.6727. Max Courant is 12.006, against 1.1744 for R2. Mass imbalance is 3.9167e-09, against 1.6667e-10 for R2. Drag drift_rel is 0.171 and half_diff_rel is 0.32385. It is a numerical instability, not a measured mesh effect.
  - R1 also diverged, with max Courant 3.1978e+103 at dt 0.04. R4 was unstable at dt 0.02 on the same refined mesh (228 cells around the cylinder, non-orthogonality 43.816, skewness 0.55022). Two failures on this mesh family at dt 0.04 and 0.02 suggest a time-step or mesh-stability problem. This cannot be proven from the package.
  - The verifier's mesh check still says no REFINE_MESH experiment has been run, so it has not used R4. I cannot call R4 a mesh FAIL, and I should not use it as a mesh measurement. The mesh component is still unmeasured, so no combined uncertainty can be formed.
  - Domain is also unmeasured. EXPAND_DOMAIN from R0 costs 748 s.
  - Budget: 4 of 6 experiments used and 5.38 of 12 compute units used. REFINE_MESH from R3 costs 4520 s, about 4.28 units. That leaves about 2.3 units, enough for EXPAND_DOMAIN from R0 (748 s, about 0.7 units).
  - R3 is the best parent for a retry. It has dt 0.01 and max Courant 0.58962, the lowest of the completed runs, which gives the most stability margin for a finer mesh. The smallest allowed factor (1.3) keeps the mesh change mild. Another time halving would cost 4504 s and would not remove the time uncertainty or measure mesh or domain.
  - Requested: REFINE_MESH {'factor': 1.3} on C2_euler_large_timestep.dt0.01-f9cf9b35455e — Mesh error is still unmeasured for both Cd and St. R1 (dt 0.04) and R4 (dt 0.02) diverged or went non-physical on the refined mesh, so neither gives a usable measurement. R3 has the smallest dt (0.01) and the lowest max Courant (0.58962) of the completed runs, so it gives the most stability margin. The smallest allowed factor (1.3) keeps the change small. The cost of 4520 s fits the remaining budget and still leaves room for EXPAND_DOMAIN from R0.
  - Outcome: executed -> C2_euler_large_timestep.m1.3-85139c80f1bb (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 4.28, 2.3

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed because no deterministic FAIL exists.
  - R0 passes hygiene, averaging and statistics. Mass imbalance is 2.5e-10, there are 12 stationary cycles, drag statistics uncertainty is 0.0001664 and Strouhal statistics uncertainty is 0.0001267.
  - Time is unresolved. R0, R2 and R3 (dt 0.04, 0.02, 0.01) give Cd 1.2901, 1.3047, 1.3139 and St 0.15849, 0.16097, 0.16232. Observed order is p=0.66 for Cd and p=0.88 for St. The verifier's R0 time uncertainty is 0.03719 (Cd) and 0.04147 (St), above the 0.015 component limit. The demonstrated changes of 1.81% and 2.36% are within tau, so the check is INCONCLUSIVE and not FAIL.
  - R5 (REFINE_MESH from R3, 51472 cells, dt 0.01, max Courant 0.76851) completed and is physical. It gives Cd 1.3186 and St 0.16317, against R3's 1.3139 and 0.16232. The mesh effect at fixed fine dt looks small next to the time effect, and R5's ci95 and drift values are small.
  - The verifier's mesh check still reports 'no REFINE_MESH experiment has been run'. Its time check uses only R0, R2 and R3. It has not ingested R5, so mesh is formally INCONCLUSIVE. This is an observability blind spot, and I cannot count R5 as a verifier-measured mesh component.
  - R1 (dt 0.04) and R4 (dt 0.02, Cd 0.29242, St 25.0, max Courant 12.006) are numerical failures on the 228-cell-around-cylinder mesh. They are not measurements and are excluded from the evidence.
  - Domain is the only component with no data at all. R0 has blockage_ratio 0.0125, lateral symmetryPlane boundaries, 30 D upstream, 50 D downstream and 40 D half-height. No EXPAND_DOMAIN run exists.
  - Budget: 5 of 6 experiments used and 8.97 of 12 compute units used. About 3.03 units remain, roughly 3200 s at the root cost scale. Only one experiment is left. EXPAND_DOMAIN from R0 costs 748 s and fits comfortably. Another time halving or a mesh refinement from R3 or R5 does not fit.
  - A domain run cannot remove R0's time uncertainty. It closes the last component with no data. If the domain effect is large, it exposes a flaw that would change the answer by more than the tolerance. If it is small, the remaining blocker is isolated to R0's time step, which is a well-documented finding.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — Domain truncation is the only uncertainty component with no data. R0 is the root, so a direct comparison with R0 answers the root question. At 748 s it is the cheapest option and fits the remaining budget of about 3.03 compute units. Mesh now has a completed physical pair (R3 and R5), and time has three levels. Neither can be improved with one affordable run.
  - Outcome: executed -> C2_euler_large_timestep.D2x-a912f88e2d43 (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 3.03, 3200, 3.03

Run C2_euler_large_timestep.m1.41-eb9ef468444b: REFINE_MESH from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.end_time: 150→80).

Run C2_euler_large_timestep.dt0.02-2f2ce6b4d241: REDUCE_TIME_STEP from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, time.delta_t: 0.04→0.02, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.3047 (+1.13%).
  - Observation: strouhal_number 0.15848 → 0.16096 (+1.56%).

Run C2_euler_large_timestep.dt0.01-f9cf9b35455e: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (time.delta_t: 0.02→0.01).
  - Observation: mean_drag_coefficient 1.3047 → 1.3139 (+0.70%).
  - Observation: strouhal_number 0.16096 → 0.16231 (+0.84%).

Run C2_euler_large_timestep.m1.41-9ec9f782d7ff: REFINE_MESH from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (mesh.refinement: 1→1.414).
  - Observation: mean_drag_coefficient 1.3047 → 0.30334 (-76.75%).
  - Observation: strouhal_number 0.16096 → 2.3956 (+1388.36%).

Run C2_euler_large_timestep.m1.3-85139c80f1bb: REFINE_MESH from C2_euler_large_timestep.dt0.01-f9cf9b35455e (mesh.refinement: 1→1.3).
  - Observation: mean_drag_coefficient 1.3139 → 1.3186 (+0.36%).
  - Observation: strouhal_number 0.16231 → 0.16317 (+0.53%).

Run C2_euler_large_timestep.D2x-a912f88e2d43: EXPAND_DOMAIN from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.281 (-0.71%).
  - Observation: strouhal_number 0.15848 → 0.15777 (-0.45%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C2_euler_large_timestep-268eddd71f94` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1056 s; record: results/runs/C2_euler_large_timestep-268eddd71f94/run.json
- `C2_euler_large_timestep.m1.41-eb9ef468444b` status=failed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T09:08:42+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m1.41-eb9ef468444b/run.json
- `C2_euler_large_timestep.dt0.02-2f2ce6b4d241` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T17:02:32+00:00 wall=818.4 s; record: results/runs/C2_euler_large_timestep.dt0.02-2f2ce6b4d241/run.json
- `C2_euler_large_timestep.dt0.01-f9cf9b35455e` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-19T19:14:28+00:00 wall=1418 s; record: results/runs/C2_euler_large_timestep.dt0.01-f9cf9b35455e/run.json
- `C2_euler_large_timestep.m1.41-9ec9f782d7ff` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-20T01:17:15+00:00 wall=2536 s; record: results/runs/C2_euler_large_timestep.m1.41-9ec9f782d7ff/run.json
- `C2_euler_large_timestep.m1.3-85139c80f1bb` status=completed parent=C2_euler_large_timestep.dt0.01-f9cf9b35455e created=2026-10-20T02:09:37+00:00 wall=2458 s; record: results/runs/C2_euler_large_timestep.m1.3-85139c80f1bb/run.json
- `C2_euler_large_timestep.D2x-a912f88e2d43` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T19:14:28+00:00 wall=643.5 s; record: results/runs/C2_euler_large_timestep.D2x-a912f88e2d43/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1109879718.0, "relative_to_root": 9.678480209287116, "experiment_wall_seconds": 7874.704146686012, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.5778258900000001, "loop_wall_seconds": 7988.171085455}
