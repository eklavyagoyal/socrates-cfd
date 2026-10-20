# Verification report: C2_euler_large_timestep (C-llm-r2)

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
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 3.32% > 1.50% but the demonstrated change 2.17% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.81, Fs=1.25]
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 4.02% > 1.50% but the demonstrated change 2.77% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.93, Fs=1.25]
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
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0332
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
│   └── C2_euler_large_timestep.dt0.005-752b3af02251
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
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0402
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
│   └── C2_euler_large_timestep.dt0.01-f9cf9b35455e
│   └── C2_euler_large_timestep.dt0.005-752b3af02251
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0272
    └── C2_euler_large_timestep-268eddd71f94
    └── C2_euler_large_timestep.D2x-a912f88e2d43

```

## EXPERIMENT HISTORY

Run C2_euler_large_timestep-268eddd71f94: submitted simulation (30580 cells, dt=0.04 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - R0 statistics and averaging are well converged. Drag statistical uncertainty is 0.0001664 and Strouhal statistical uncertainty is 0.0001267. There are 12 stationary cycles. These are far below the 0.03 tolerance.
  - Mesh, time and domain components are all unmeasured for both quantities, so no combined uncertainty exists.
  - Time discretisation is the weakest point of R0. The scheme is first-order Euler at dt = 0.04 D/U, and max Courant is 2.9248 with 2 outer correctors. The Courant check is INCONCLUSIVE because temporal accuracy is unproven without time-step refinement.
  - R0 has 157.74 steps per shedding period. Euler numerical dissipation at this Courant number could shift the shedding frequency and mean drag, so a time error above the 0.5*tolerance budget is plausible.
  - REDUCE_TIME_STEP isolates the time error on the identical mesh. REFINE_MESH could change dt automatically and confound mesh and time effects.
  - Domain truncation looks less likely to dominate. R0 has blockage 0.0125, upstream 30 D, downstream 50 D and half-height 40 D. It is still unmeasured.
  - The cost is about 1126 s, roughly 1.07x the root run. The budget is 0 of 6 experiments and 0 of 12x compute used, so it is affordable.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — Time error is entirely unmeasured. R0 uses first-order Euler at max Courant 2.92, which is the most likely source of a flaw larger than the tolerance. Halving dt on the same mesh isolates this error without confounding by mesh changes, at a cost of about 1126 s.
  - Outcome: executed -> C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.07

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - R0 averaging and statistics pass. Drag statistical uncertainty is 0.0001664 and Strouhal statistical uncertainty is 0.0001267, with 12 stationary cycles. R1 has 6 cycles and is also tightly converged (drag ci95 4.1571e-05).
  - Halving dt (R0 0.04 to R1 0.02) moved mean Cd from 1.2901 to 1.3047, a 1.11% change, and St from 0.15849 to 0.16097, a 1.54% change. Both changes are far above the recorded noise floors (1.7e-04 and 1.3e-04), so the time error is real.
  - The St change from one halving of dt already exceeds the 1.5% component budget (0.5*tolerance). The first-order Euler error of R1 itself is therefore probably not negligible.
  - The verifier's time uncertainties are 0.06683 for Cd and 0.09224 for St. They rest on a two-level Richardson estimate with an assumed order p=1 and Fs=3. Both exceed the 0.03 tolerance, and the demonstrated change is below tolerance, so the time check stays INCONCLUSIVE.
  - The observed temporal order is unmeasured. A third dt level (R0, R1, new) would let the observed order be computed and replace the assumed p=1.
  - Mesh and domain components are still unmeasured for both quantities. Time is the only component with a recorded signal that is large enough to threaten the tolerance, so it is the most informative thing to resolve first.
  - Budget is sufficient. 1 of 6 experiments and 1.07 of 12x compute are used. The chosen run costs about 2252 s, roughly 2.1x the R0 cost.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — Time sensitivity is the only component with a measured, non-negligible signal. Cd changed by 1.11% and St by 1.54% when dt was halved. The verifier's p=1 Richardson uncertainties (0.06683 and 0.09224) are assumed-order estimates. A third dt level on the same mesh continues the refinement family from the finest run. It gives an observed order and a measured residual time error without mixing in mesh or domain effects.
  - Outcome: executed -> C2_euler_large_timestep.dt0.01-f9cf9b35455e (completed)
  - Numeric audit: 3 number(s) not traceable to evidence: 2.1, 0.8%, 0.55%

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and there are no failed checks. ACCEPT is not allowed. REJECT is not allowed because no FAIL has been measured.
  - R0 averaging and statistics pass. Drag statistical uncertainty is 0.0001664 and St statistical uncertainty is 0.0001267, over 12 stationary cycles. These are not the limiting components.
  - The time-step sequence has not converged. Cd is 1.2901 (R0, dt 0.04), 1.3047 (R1, dt 0.02) and 1.3139 (R2, dt 0.01). St is 0.15849, 0.16097 and 0.16232. The noise floors (Cd ci95 2.5e-05 to 5.2e-05) are far smaller than these changes.
  - The step-to-step changes are not shrinking at the first-order rate expected for Euler. Cd changes by 0.0146 and then 0.0092 (ratio 0.63). St changes by 0.00248 and then 0.00135 (ratio 0.54). The verifier's observed orders are p=0.66 (Cd) and p=0.88 (St).
  - The verifier estimates R0 time uncertainty at 0.03719 for Cd and 0.04147 for St. Both are above the 0.03 tolerance and well above the 0.015 component budget. The demonstrated change R0 to R2 is only 1.81% for Cd and 2.36% for St, which is below tolerance. The check therefore stays INCONCLUSIVE, not FAIL, and I cannot overrule that.
  - Time error is the dominant known flaw. Even if mesh and domain pass, the root cannot be accepted until the time component is resolved. A third level (R3, dt 0.005) would give a better order estimate and a larger demonstrated change. It could show the root's time error exceeds tolerance, which would give a deterministic FAIL.
  - Mesh and domain are still unmeasured for both quantities (no REFINE_MESH or EXPAND_DOMAIN run). They must be run later. The recorded configuration gives no specific sign that they dominate. Blockage is 0.0125, with 30 D upstream, 50 D downstream and 40 D half-height.
  - Budget: 2 of 6 experiments and 3.2 of 12x compute are used. REDUCE_TIME_STEP from R2 costs about 4504 s (about 4.3x root), which brings compute to about 7.5x. That leaves about 4.5x, enough for REFINE_MESH from R0 (about 1130 s) and EXPAND_DOMAIN from R0 (about 748 s).
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep.dt0.01-f9cf9b35455e — Time sensitivity is the only component with a measured signal that threatens the tolerance. Cd and St are still moving at the finest level (R1 to R2: 0.71% for Cd, 0.84% for St), and the observed orders are below 1 (0.66 and 0.88). The verifier's R0 time uncertainties (3.72% and 4.15%) exceed tolerance, but only extrapolation supports them. Continuing the family from the finest run, R2, adds a fourth level on the identical mesh. This isolates time error from mesh and domain effects, tests whether the sequence is asymptotic, and can turn the estimate into a demonstrated change.
  - Outcome: executed -> C2_euler_large_timestep.dt0.005-752b3af02251 (completed)
  - Numeric audit: 17 number(s) not traceable to evidence: 0.0146, 0.0092, 0.63, 0.00248, 0.00135

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed because the mesh, time and domain components are not all measured and within budget. REJECT is not allowed because no deterministic FAIL has been recorded.
  - R0 averaging and statistics are not limiting. Drag statistical uncertainty is 0.0001664 and Strouhal statistical uncertainty is 0.0001267, over 12 stationary cycles.
  - The dt sequence on the same mesh is monotonic. Cd is 1.2901 (R0, dt 0.04), 1.3047 (R1), 1.3139 (R2) and 1.3188 (R3, dt 0.005). St is 0.15849, 0.16097, 0.16232 and 0.163. The changes are well above the recorded noise (Cd ci95 1.29e-05 to 5.23e-05).
  - The step-to-step changes are shrinking. Cd changes by 0.0146, 0.0092 and then 0.0049. St changes by 0.00248, 0.00135 and then 0.00068. So the time series is approaching convergence, but not at a sub-tolerance level for R0.
  - The verifier's three-level Celik estimate of R0 time uncertainty is 0.0332 for Cd (p=0.81) and 0.04024 for St (p=0.93). Both exceed the 0.015 component budget and the 0.03 tolerance. The demonstrated changes (2.17% for Cd, 2.77% for St) are below tolerance, so the time check is INCONCLUSIVE rather than FAIL. I cannot overrule this.
  - No further time-step refinement is possible. REDUCE_TIME_STEP from R3 is not allowed (limit 0.005), so the time branch is exhausted. The remaining unmeasured components are mesh and domain.
  - Mesh is the most likely remaining flaw. The mesh is coarse: representative cell size 0.45745 D, 160 cells around the cylinder, wake last cell 1.0209 D, and 111 wake cells over 50 D. The spatial error of both quantities is wholly unmeasured.
  - The parent should be R1, not R0. R0 has max Courant 2.9248, and REFINE_MESH may shorten dt if the predicted Courant number exceeds the PISO limit. That would confound mesh and time effects. R1 has max Courant 1.1744, so dt is more likely to be kept and the mesh effect is isolated. R1 costs 2260 s, about 2.14x root.
  - Budget: 3 of 6 experiments and 7.47 of 12x compute are used. After the R1 mesh run, about 2.4x remains. That is enough for EXPAND_DOMAIN from R0 (748 s, about 0.7x) or from R1 (1495 s, about 1.4x).
  - Domain truncation is less likely to dominate but is unmeasured. Blockage is 0.0125, with 30 D upstream, 50 D downstream and 40 D half-height with symmetry lateral boundaries. I rank it second.
  - Requested: REFINE_MESH {'factor': 1.4142} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — Time refinement is exhausted (R3 cannot be reduced further), and the mesh error of Cd and St is entirely unmeasured on a coarse mesh (0.45745 D representative cell size, 160 cells around the cylinder). R1 is chosen as parent because its max Courant of 1.1744 leaves room to refine without forcing a dt change, so the mesh effect is not confounded with time. R0 (max Courant 2.9248) is more likely to trigger an automatic dt reduction. Cost is about 2260 s (about 2.14x root), which fits the remaining compute budget and leaves room for EXPAND_DOMAIN.
  - Outcome: executed -> C2_euler_large_timestep.m1.41-9ec9f782d7ff (completed)
  - Numeric audit: 11 number(s) not traceable to evidence: 0.0146, 0.0092, 0.0049, 0.00248, 0.00135

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed because no deterministic FAIL is recorded.
  - R4 (REFINE_MESH from R1) is a numerically failed run, not a valid mesh-sensitivity measurement. Its Cd is 0.29242 and R1's is 1.3047. Its rms Cl is 3.6727 against 0.19618 for R1. Its St is 25.0 (FFT 25.0) against 0.16097 for R1. Its max Courant is 12.006 against 1.1744 for R1. Its stationary-window start is 8.4433, and drag drift is 0.171 with half-difference 0.32385. The verifier still reports mesh as INCONCLUSIVE.
  - Treating R4 as a mesh effect would be a hidden failure. A 77% drop in Cd and a 155-fold St jump are blow-up signatures. They do not show that the root mesh is wrong. I may not use R4 to overrule or to support the root.
  - Time branch: Cd is 1.2901 (R0), 1.3047 (R1), 1.3139 (R2) and 1.3188 (R3). St is 0.15849, 0.16097, 0.16232 and 0.163. The verifier's Celik time uncertainty for R0 is 0.0332 for Cd (p=0.81) and 0.04024 for St (p=0.93). Both exceed the 0.015 component budget and the 0.03 tolerance. The demonstrated changes (2.17% and 2.77%) are below tolerance, so the check is INCONCLUSIVE, not FAIL. REDUCE_TIME_STEP from R3 is not allowed.
  - R0 averaging and statistics pass (drag 0.0001664 and St 0.0001267 over 12 cycles). Mesh and domain are unmeasured for both quantities.
  - Budget: 4 of 6 experiments and 9.61 of 12x compute are used, so about 2.39x (about 2500 s) remains. REFINE_MESH from R1 (2260 s) would use nearly all of it and has already failed once. REFINE_MESH from R0 (1130 s) plus EXPAND_DOMAIN from R0 (748 s) fits in the remaining budget.
  - Parent choice: R0 is the root and the cheapest parent. The menu says the time step is reduced automatically if the predicted Courant number exceeds the PISO limit, and that change is recorded. This makes a repeat blow-up less likely than keeping dt = 0.02 on the finer mesh. The smallest factor, 1.3, limits the Courant growth. The comparison will have to account for any recorded dt change.
  - The time uncertainty already makes ACCEPT unreachable. A valid mesh run can still expose a demonstrated change above tolerance, which would give a deterministic FAIL and allow REJECT. If the change is small, it narrows the unresolved components to time and domain.
  - Requested: REFINE_MESH {'factor': 1.3} on C2_euler_large_timestep-268eddd71f94 — R4 is a diverged run and gives no valid mesh information. The mesh error of Cd and St is still unmeasured. R0 is the cheapest parent (1130 s), and the remaining budget (about 2.39x root) also covers EXPAND_DOMAIN from R0 (748 s). The menu allows automatic dt reduction when the predicted Courant number is too high, which should avoid repeating R4's blow-up at dt = 0.02. The minimum factor 1.3 limits the Courant increase and the cost.
  - Outcome: executed -> C2_euler_large_timestep.m1.3-53f0c75d4a04 (failed)
  - Numeric audit: 5 number(s) not traceable to evidence: 77%, 155, 2.39, 2500, 2.39

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed because no deterministic FAIL is recorded.
  - R0 averaging and statistics pass. Drag statistical uncertainty is 0.0001664 and St statistical uncertainty is 0.0001267, over 12 stationary cycles. Neither limits the result.
  - Time branch is exhausted. Cd is 1.2901 (R0), 1.3047 (R1), 1.3139 (R2), 1.3188 (R3). St is 0.15849, 0.16097, 0.16232, 0.163. The verifier's Celik time uncertainty for R0 is 0.0332 (Cd, p=0.81) and 0.04024 (St, p=0.93), both above the 0.015 component budget and the 0.03 tolerance. The demonstrated changes (2.17% and 2.77%) are below tolerance, so the check is INCONCLUSIVE and not FAIL. REDUCE_TIME_STEP from R3 is not allowed.
  - Both mesh-refinement attempts diverged: R4 (from R1, 228 cells around the cylinder) has max Courant 12.006, Cd 0.29242, rms Cl 3.6727 and St 25.0. R5 (from R0, 208 cells around the cylinder) stopped after 80 steps with max Courant 9.2058e+104 and mass imbalance 8.8373e+65. Neither gives valid mesh sensitivity, and I will not read either as a mesh effect. R5 kept dt = 0.04, so the automatic dt reduction did not prevent the blow-up.
  - A third REFINE_MESH from R0 or R1 would probably diverge again. Higher factors only make the cells smaller. Parents R2 (4520 s) and R3 (9039 s) cost more than the remaining budget. The budget has 1 experiment and about 2.36x root compute left, which is roughly 2490 s given the root cost of 1055.7 s. R1 mesh refinement (2260 s) would use nearly all of it and has already failed.
  - EXPAND_DOMAIN from R0 costs 748 s and fits the budget. The near-field mesh is unchanged, so it keeps R0's stable setup and should not repeat the refinement blow-up. It measures the domain component, which is unmeasured for both quantities. R0's blockage ratio is 0.0125, with symmetryPlane lateral boundaries at 40 D, 30 D upstream and 50 D downstream. A demonstrated change above tolerance would give a deterministic FAIL and allow REJECT.
  - Expect the final report to be INCONCLUSIVE regardless. Mesh remains unmeasured and the R0 time uncertainty exceeds budget. This is a stated limitation, not a pass.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — Domain error is unmeasured for both quantities, and this is the only remaining experiment that is affordable and likely to complete. Two REFINE_MESH runs diverged (R4 max Courant 12.006, R5 max Courant 9.2058e+104). Parents R2 and R3 are too expensive. EXPAND_DOMAIN from R0 costs about 748 s and leaves the near-field mesh and dt of R0 unchanged, so it isolates truncation and blockage.
  - Outcome: executed -> C2_euler_large_timestep.D2x-a912f88e2d43 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 2.36, 2490, 0.42%, 0.42%

Run C2_euler_large_timestep.dt0.02-2f2ce6b4d241: REDUCE_TIME_STEP from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, time.delta_t: 0.04→0.02, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.3047 (+1.13%).
  - Observation: strouhal_number 0.15848 → 0.16096 (+1.56%).

Run C2_euler_large_timestep.dt0.01-f9cf9b35455e: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (time.delta_t: 0.02→0.01).
  - Observation: mean_drag_coefficient 1.3047 → 1.3139 (+0.70%).
  - Observation: strouhal_number 0.16096 → 0.16231 (+0.84%).

Run C2_euler_large_timestep.dt0.005-752b3af02251: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.01-f9cf9b35455e (time.delta_t: 0.01→0.005).
  - Observation: mean_drag_coefficient 1.3139 → 1.3188 (+0.37%).
  - Observation: strouhal_number 0.16231 → 0.163 (+0.42%).

Run C2_euler_large_timestep.m1.41-9ec9f782d7ff: REFINE_MESH from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (mesh.refinement: 1→1.414).
  - Observation: mean_drag_coefficient 1.3047 → 0.30334 (-76.75%).
  - Observation: strouhal_number 0.16096 → 2.3956 (+1388.36%).

Run C2_euler_large_timestep.m1.3-53f0c75d4a04: REFINE_MESH from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, mesh.refinement: 1→1.3, time.end_time: 150→80).

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
- `C2_euler_large_timestep.dt0.02-2f2ce6b4d241` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T17:02:32+00:00 wall=818.4 s; record: results/runs/C2_euler_large_timestep.dt0.02-2f2ce6b4d241/run.json
- `C2_euler_large_timestep.dt0.01-f9cf9b35455e` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-19T19:14:28+00:00 wall=1418 s; record: results/runs/C2_euler_large_timestep.dt0.01-f9cf9b35455e/run.json
- `C2_euler_large_timestep.dt0.005-752b3af02251` status=completed parent=C2_euler_large_timestep.dt0.01-f9cf9b35455e created=2026-10-19T19:42:57+00:00 wall=2541 s; record: results/runs/C2_euler_large_timestep.dt0.005-752b3af02251/run.json
- `C2_euler_large_timestep.m1.41-9ec9f782d7ff` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-20T01:17:15+00:00 wall=2536 s; record: results/runs/C2_euler_large_timestep.m1.41-9ec9f782d7ff/run.json
- `C2_euler_large_timestep.m1.3-53f0c75d4a04` status=failed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-20T07:52:54+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m1.3-53f0c75d4a04/run.json
- `C2_euler_large_timestep.D2x-a912f88e2d43` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T19:14:28+00:00 wall=643.5 s; record: results/runs/C2_euler_large_timestep.D2x-a912f88e2d43/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1187021760.0, "relative_to_root": 10.351181687377371, "experiment_wall_seconds": 7957.117383687017, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.61821726, "loop_wall_seconds": 16791.815202591002}
