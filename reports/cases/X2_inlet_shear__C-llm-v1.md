# Verification report: X2_inlet_shear (C-llm-v1)

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
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so REJECT is not allowed. ACCEPT is also not allowed, because mesh, time and domain uncertainty are all unmeasured for both mean_drag_coefficient and strouhal_number.
  - R0 averaging and statistics components pass. Averaging bias is 0.0004734 (Cd) and 0.000352 (St). Statistical uncertainty is 0.002267 (Cd) and 0.002498 (St). Both are far below the 0.03 tolerance, with 11 stationary cycles and a Cd drift of -0.0022666. The remaining risk is in the discretisation and boundary components.
  - R0 inlet_velocity_measured shows ux_min 0.1125, ux_max 0.1875, mean 0.15 and ux_nonuniformity 0.5. The problem statement requires a uniform stream, but the measured inlet is not uniform. The verifier did not flag this, so I cannot treat it as a FAIL. It is a credible way for the domain to bias Cd and St by more than 3 %.
  - R0 domain: 30 D upstream, 50 D downstream, 40 D half height, symmetryPlane lateral boundaries, zeroGradient inlet pressure and a blockage ratio of 0.0125. Any boundary or inlet-shear effect is unquantified, and the question says to treat the stream as unbounded.
  - R0 time resolution looks reasonable: 612.82 steps per shedding period, max Courant 0.7323, backward scheme. The risk of a time-step error larger than 3 % is lower than the domain risk, but it is unmeasured.
  - R0 mesh is moderate: 30580 cells, representative size 0.45745 D, 160 cells around the cylinder, wake last cell 1.0209 D. Mesh error is unmeasured and is the second priority.
  - R0 stationary_window_start_is_mser_cap is true, with the window starting at 80.781 against a declared start of 75.0. This is a minor concern about transient removal. The measured drift is small, so RUN_LONGER is a lower priority.
  - EXPAND_DOMAIN costs 1405 s, the cheapest discretisation or boundary experiment, against 2443 s for REFINE_MESH and 2116 s for REDUCE_TIME_STEP. Budget is unused (0 of 6 experiments, 0 of 12 relative compute), so mesh and time checks can follow.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X2_inlet_shear-32168bfbca6b — Domain truncation or blockage, together with the measured non-uniform inlet (ux 0.1125 to 0.1875, nonuniformity 0.5) against a uniform-stream specification, is the most likely flaw to move Cd or St by more than 3 %. It is also the cheapest discretisation or boundary experiment (1405 s), so it exposes the largest unquantified risk first.
  - Outcome: executed -> X2_inlet_shear.D2x-8d92db3cbed0 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. REJECT is not allowed, and ACCEPT is not allowed because the mesh, time and domain components are unmeasured for Cd and St.
  - R0 averaging and statistics pass. Averaging bias is 0.0004734 (Cd) and 0.000352 (St). Statistical uncertainty is 0.002267 (Cd) and 0.002498 (St), over 11 stationary cycles.
  - R1 (EXPAND_DOMAIN from R0, 60 D upstream, 100 D downstream, 80 D half height) completed, but the verifier calls it statistically unreliable. Its stationary-window Cd ci95 is 0.10446 and its drift_rel is 0.27794. For St the uncertainty is 0.1947993.
  - R1's stationary window starts at 4.0695 convective units and the run ends at 80.0. R0's window only started at 80.781. So R1's early transient was almost certainly not removed, and its Cd and St (stationary window 1.4857 and 0.17529) cannot be compared with R0 (1.3306 and 0.16318).
  - R1's FFT St is 0.16948 and its windowed St is 0.17529. These disagree, and its frequency resolution is 0.025. This is more evidence that R1 is too short.
  - The domain check explicitly asks for R1 to be run longer first. RUN_LONGER on R1 is the only experiment that can turn the domain component from INCONCLUSIVE into a measurement. Refining the mesh or reducing the time step now would leave the domain question open.
  - R1 reports checkMesh_ok false, although its non-orthogonality (43.313) and skewness (0.53384) match R0. The mesh_quality check was only evaluated for R0. This needs to be explained before R1 is trusted.
  - Both R0 and R1 record a non-uniform inlet (ux_min 0.1125, ux_max 0.1875, ux_nonuniformity 0.5, mean 0.15), but the question specifies a uniform stream. The verifier did not flag it, so I cannot treat it as a FAIL. No menu action can change it, and it is the same in both runs. The domain test cannot isolate it.
  - Budget: 1 of 6 experiments used and 0.71 of 12 relative compute used. RUN_LONGER from R1 is estimated at 1756 s for the default length, which is affordable.
  - Requested: RUN_LONGER {'additional_convective_times': 150.0} on X2_inlet_shear.D2x-8d92db3cbed0 — The domain sensitivity check is INCONCLUSIVE because R1 is not statistically reliable (Cd ci95 0.10446, drift_rel 0.27794, 80 convective units only). The verifier asks for R1 to be run longer first. This is the cheapest way (estimated 1756 s at default length) to get a usable domain comparison. It also tests whether the large R0-R1 differences are start-up artefacts or real boundary effects.
  - Outcome: executed -> X2_inlet_shear.long230-1a1e9e99a483 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with failed_checks empty, so REJECT is not allowed. ACCEPT is not allowed because the mesh, time and domain components are unmeasured for both mean_drag_coefficient and strouhal_number.
  - R0 averaging and statistics pass: Cd bias 0.0004734 and statistical uncertainty 0.002267, St bias 0.000352 and statistical uncertainty 0.002498, over 11 stationary cycles.
  - R2 (RUN_LONGER on R1, 230 convective units, 20 stationary cycles) is much closer to R0 than R1 was. Stationary Cd is 1.329 against R0 1.3306. Stationary St is 0.16325 against R0 0.16318.
  - The domain check is still INCONCLUSIVE because R2 is not statistically reliable. Its Cd uncertainty is 0.02625 and its St uncertainty is 0.019654. Both exceed the 0.015 component budget (0.5*tolerance).
  - R2 Cd drift_rel is -0.02625, half_diff_rel is -0.012289 and ci95 is 0.005543. Its stationary_window_start_is_mser_cap is true (start 107.29). Together these indicate the start-up transient of the larger domain is still decaying, so the window is not yet stationary.
  - R2 reported Cd is 1.3922, against 1.329 in its stationary window. Early transient data still contaminates the full record, which supports the same reading.
  - R1 and R2 share a mesh with checkMesh_ok false, even though R1/R2 non-orthogonality (43.313) and skewness (0.53384) equal R0. R0 is the run under evaluation and reports checkMesh_ok true. The R1/R2 flag is unexplained, which weakens R2 as a domain reference.
  - All three runs record a non-uniform inlet (ux_min 0.1125, ux_max 0.1875, ux_nonuniformity 0.5, mean 0.15), while the question specifies a uniform stream. The verifier raised no FAIL, so I cannot overrule it. No menu action changes it, and it is identical in R0, R1 and R2, so the domain comparison cannot isolate it.
  - Continuing R2 is the only way to make the domain component measurable, and mesh and time experiments would still be blocked behind it. Budget used is 2 of 6 experiments and 2.04 of 12 relative compute. RUN_LONGER on R2 is estimated at 1756 s at the default length, so 200 units should fit comfortably.
  - Requested: RUN_LONGER {'additional_convective_times': 200.0} on X2_inlet_shear.long230-1a1e9e99a483 — The domain sensitivity check for Cd and St is INCONCLUSIVE because R2 is not statistically reliable (Cd uncertainty 0.02625, St uncertainty 0.019654, drift_rel -0.02625, window start 107.29 is an MSER cap). The verifier asks for the run to be run longer first. Mesh and time experiments would not unblock the domain component.
  - Outcome: executed -> X2_inlet_shear.long430-1e25bc8ea220 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 0.019654, 200, 0.019654, 0.019654

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. REJECT is not allowed. ACCEPT is not allowed because the mesh, time and domain components are unresolved for both mean_drag_coefficient and strouhal_number.
  - R0 averaging and statistics pass. Cd bias is 0.0004734 and Cd statistical uncertainty is 0.002267. St bias is 0.000352 and St statistical uncertainty is 0.002498. R0 has 11 stationary cycles.
  - R3 (RUN_LONGER on R2, 430 units, 40 stationary cycles, window start 180.58, not an MSER cap) is now statistically reliable. Its Cd ci95 is 0.0002689 and its Cd drift_rel is 0.0017393. Stationary Cd is 1.3216 against R0 1.3306. Stationary St is 0.16254 against R0 0.16318.
  - The verifier shows the demonstrated R0-to-R3 change is 0.68% for Cd and 0.39% for St, both within the 3% tolerance. The domain component is still INCONCLUSIVE (Cd 0.04075, St 0.02349). The reason is that it is a two-level Richardson estimate with an assumed order p=1 and safety factor 3, and it exceeds the 0.015 component budget. Domain is therefore a conservative extrapolation, not a measured failure.
  - Mesh and time are completely unmeasured. REFINE_MESH and REDUCE_TIME_STEP have not been run. These two components block ACCEPT regardless of the domain outcome. A large mesh change would produce a FAIL and end the search early.
  - R0 mesh: 30580 cells, representative size 0.45745 D, wake last cell 1.0209 D, 160 cells around the cylinder. R0 time: 612.82 steps per period, max Courant 0.7323. Mesh is more likely than time step to be the limiting discretisation error. Mesh is the first priority.
  - Budget: 3 of 6 experiments used and 3.81 of 12 relative compute used. Three experiments remain (mesh, time, and one more domain level). Their estimated costs are 2443 s, 2116 s and 1815 s, against a root cost of 1983.8 s. This is affordable.
  - All runs record a non-uniform inlet (ux_min 0.1125, ux_max 0.1875, ux_nonuniformity 0.5, mean 0.15). The question specifies a uniform stream. The verifier did not raise a FAIL, so I cannot overrule it. No menu action can change the inlet, and it is identical in R0 to R3, so the domain runs cannot isolate it.
  - R1, R2 and R3 report checkMesh_ok false, while R0 reports true. Their non-orthogonality (43.313) and skewness (0.53384) are identical to R0. This is unexplained and weakens R1 to R3 as references for the domain comparison.
  - Requested: REFINE_MESH {'factor': 1.4142} on X2_inlet_shear-32168bfbca6b — Mesh error is completely unmeasured for Cd and St and blocks ACCEPT whatever the domain result. R0 is the run under evaluation and has a statistically adequate record, so refining from R0 gives a clean mesh-sensitivity comparison. The domain question is already bounded by the 0.68% (Cd) and 0.39% (St) demonstrated change between R0 and R3. Mesh is more likely than time step to be the dominant discretisation error. The cost is 2443 s, which fits within the remaining budget alongside the time-step and domain-level runs.
  - Outcome: executed -> X2_inlet_shear.m1.41-ca5c50f2e498 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty, so REJECT is not allowed. ACCEPT is not allowed because the time component is unmeasured for both Cd and St. The domain component is also unresolved for both, and the mesh component is unresolved for St.
  - R0 averaging and statistics pass. Cd bias is 0.0004734 and statistical uncertainty is 0.002267. St bias is 0.000352 and statistical uncertainty is 0.002498. R0 has 11 stationary cycles.
  - R4 (REFINE_MESH from R0) gives stationary Cd 1.3338 against R0 1.3306, a change of 0.240%. The Cd mesh component passes at 0.01436. St is 0.16419 against 0.16318, a change of 0.62%. The St mesh component is still INCONCLUSIVE at 0.0368, because the two-level Richardson estimate with assumed p=2 and Fs=3 exceeds the 0.015 budget.
  - R3 is statistically reliable: Cd ci95 is 0.0002689, drift_rel is 0.0017393, and there are 40 cycles. Its stationary Cd is 1.3216 and its St is 0.16254. The demonstrated R0-to-R3 changes are 0.68% (Cd) and 0.39% (St), both within tolerance. The domain components (Cd 0.04075, St 0.02349) are conservative p=1, Fs=3 extrapolations, not measured failures.
  - Time-step error has never been tested for either quantity. R0 uses dt = 0.01 convective units, which is 612.82 steps per period, with max Courant 0.7323. The verifier lists 'time' as missing for both Cd and St. No ACCEPT is possible without it, and a large change would be a deterministic FAIL that ends the search.
  - R4 used dt = 0.0086903 against R0's 0.01. The R0-to-R4 St and Cd changes therefore mix spatial and temporal effects. An isolated REDUCE_TIME_STEP on R0's identical mesh separates them and gives a clean time-error estimate.
  - Budget: 4 of 6 experiments are used, and 5.04 of 12 relative compute is used. REDUCE_TIME_STEP from R0 costs 2116 s, about 1.07 times the root cost, so one more experiment will still be affordable afterwards. Using R0 as parent is the cheapest option (R4 would cost 4886 s).
  - Open concern: all runs record a non-uniform inlet (ux_min 0.1125, ux_max 0.1875, ux_nonuniformity 0.5, mean 0.15) while the question specifies a uniform stream. The verifier raised no FAIL, so I cannot overrule it. No menu action changes the inlet, and it is identical across R0 to R4. It should be reviewed by a human.
  - Open concern: R1, R2 and R3 report checkMesh_ok false while R0 and R4 report true. Their non-orthogonality (43.313) and skewness (0.53384) equal R0's. The flag is unexplained and weakens R1 to R3 as domain references.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on X2_inlet_shear-32168bfbca6b — Time-step error is completely unmeasured for Cd and St, and it blocks ACCEPT regardless of the other components. A large change would give a deterministic FAIL. R0 is the run under evaluation. Halving dt on R0's identical mesh isolates temporal error, which is confounded with spatial error in R4 because R4's dt was also reduced. It costs 2116 s, which leaves budget for one more experiment.
  - Outcome: executed -> X2_inlet_shear.dt0.005-2ef6d66a694b (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.07

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. REJECT is not allowed. ACCEPT is not allowed because the St mesh component and the Cd and St domain components are INCONCLUSIVE, and combined_uncertainty is null.
  - R0 averaging and statistics pass. Cd bias is 0.0004734 and Cd statistical uncertainty is 0.002267. St bias is 0.000352 and St statistical uncertainty is 0.002498. R0 has 11 stationary cycles, but its stationary window start (80.781) is an MSER cap.
  - The time component now passes. R5 (dt 0.005) gives Cd 1.3268 against R0 1.3306, a change of 0.285%, and St 0.16332 against 0.16318, a change of 0.085%. The time uncertainties are 0.01139 (Cd) and 0.007495 (St).
  - The Cd mesh component passes. R4 gives Cd 1.3338 against R0 1.3306, a change of 0.240%, and the uncertainty is 0.01436. The St mesh component is still INCONCLUSIVE at 0.0368, with a demonstrated change of 0.62% (R4 0.16419 against R0 0.16318). The estimate is two-level, with assumed p=2 and Fs=3. R4 also changed dt (0.0086903), but R5 shows the dt effect on St is only 0.085%, so the R0-to-R4 St change is mostly spatial.
  - The domain components are INCONCLUSIVE (Cd 0.04075, St 0.02349). The demonstrated R0-to-R3 changes are only 0.68% (Cd 1.3216 against 1.3306) and 0.39% (St 0.16254 against 0.16318). R3 is statistically reliable (40 cycles, Cd ci95 0.0002689, drift_rel 0.0017393). The large uncertainty is the p=1, Fs=3 extrapolation from two levels, not a measured failure.
  - Only 1 experiment remains (5 of 6 used). Compute used is 6.1 of 12 relative to the root, which is about 11,700 s left. Open items: the St mesh uncertainty and the Cd and St domain uncertainties. One experiment cannot close all of them, so ACCEPT is probably out of reach and the final report will probably be INCONCLUSIVE. I still choose the experiment that gives a reliable, interpretable measurement.
  - A third domain level is a poor use of the last run. R1 (80 units) and R2 (230 units) showed that enlarged domains need several hundred convective units before the window is stationary (R3 needed 430). One new expanded-domain run would probably be unreliable again, and a RUN_LONGER on it would exceed the budget.
  - REFINE_MESH from R4 (factor 1.4142) gives a third mesh level R0, R4, new. The small-domain family converges quickly (R4 had 6 cycles and Cd ci95 2.6e-05), so the result should be usable. It gives a measured convergence order for St, and it also checks the Cd mesh estimate. Cost is 5695 s, which brings the total to about 8.97 of 12. A large change would give a deterministic FAIL.
  - Concern for human review: every run records a non-uniform inlet (ux_min 0.1125, ux_max 0.1875, ux_nonuniformity 0.5, mean 0.15, uy_max_abs 0.0), while the question specifies a uniform stream. The verifier did not flag it and no menu action can change it. The R0-to-R3 shift may partly come from this, because the inlet ux range is identical in both domains but the half height doubles.
  - Concern for human review: R1, R2 and R3 report checkMesh_ok false, while R0, R4 and R5 report true. Their non-orthogonality (43.313) and skewness (0.53384) are identical to R0. The cause is unexplained, and it weakens R1 to R3 as domain references.
  - Requested: REFINE_MESH {'factor': 1.4142} on X2_inlet_shear.m1.41-ca5c50f2e498 — The St mesh component is INCONCLUSIVE because only two levels exist and p=2 is assumed (uncertainty 0.0368, demonstrated change 0.62%). Refining from R4 gives a third mesh level and a measured order. The small-domain family reaches a stationary window quickly, so the run should be statistically reliable. An expanded-domain run would probably not be reliable within the remaining budget. It costs 5695 s, which fits within the remaining compute (about 8.97 of 12 relative to the root afterwards).
  - Outcome: executed -> X2_inlet_shear.m2-3f2d80a2a02e (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 700, 8.97, 8.97

Run X2_inlet_shear.D2x-8d92db3cbed0: EXPAND_DOMAIN from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.4857 (+11.66%).
  - Observation: strouhal_number 0.16318 → 0.17529 (+7.42%).

Run X2_inlet_shear.long230-1a1e9e99a483: RUN_LONGER from X2_inlet_shear.D2x-8d92db3cbed0 (time.end_time: 80→230).
  - Observation: mean_drag_coefficient 1.4857 → 1.329 (-10.55%).
  - Observation: strouhal_number 0.17529 → 0.16325 (-6.87%).

Run X2_inlet_shear.long430-1e25bc8ea220: RUN_LONGER from X2_inlet_shear.long230-1a1e9e99a483 (time.end_time: 230→430).
  - Observation: mean_drag_coefficient 1.329 → 1.3216 (-0.56%).
  - Observation: strouhal_number 0.16325 → 0.16254 (-0.43%).

Run X2_inlet_shear.m1.41-ca5c50f2e498: REFINE_MESH from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.00869, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3338 (+0.24%).
  - Observation: strouhal_number 0.16318 → 0.16419 (+0.62%).

Run X2_inlet_shear.dt0.005-2ef6d66a694b: REDUCE_TIME_STEP from X2_inlet_shear-32168bfbca6b (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3306 → 1.3268 (-0.28%).
  - Observation: strouhal_number 0.16318 → 0.16332 (+0.08%).

Run X2_inlet_shear.m2-3f2d80a2a02e: REFINE_MESH from X2_inlet_shear.m1.41-ca5c50f2e498 (mesh.refinement: 1.414→2, time.delta_t: 0.00869→0.007432).
  - Observation: mean_drag_coefficient 1.3338 → 1.334 (+0.01%).
  - Observation: strouhal_number 0.16419 → 0.16454 (+0.21%).

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
- `X2_inlet_shear.long430-1e25bc8ea220` status=completed parent=X2_inlet_shear.long230-1a1e9e99a483 created=2026-10-19T18:29:37+00:00 wall=2550 s; record: results/runs/X2_inlet_shear.long430-1e25bc8ea220/run.json
- `X2_inlet_shear.m1.41-ca5c50f2e498` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T10:06:49+00:00 wall=2448 s; record: results/runs/X2_inlet_shear.m1.41-ca5c50f2e498/run.json
- `X2_inlet_shear.dt0.005-2ef6d66a694b` status=completed parent=X2_inlet_shear-32168bfbca6b created=2026-10-19T18:29:05+00:00 wall=1343 s; record: results/runs/X2_inlet_shear.dt0.005-2ef6d66a694b/run.json
- `X2_inlet_shear.m2-3f2d80a2a02e` status=completed parent=X2_inlet_shear.m1.41-ca5c50f2e498 created=2026-10-19T11:25:18+00:00 wall=7000 s; record: results/runs/X2_inlet_shear.m2-3f2d80a2a02e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 4116667876.0, "relative_to_root": 8.974641107477654, "experiment_wall_seconds": 17246.720580720994, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.61153126, "loop_wall_seconds": 166.38372657999997}
