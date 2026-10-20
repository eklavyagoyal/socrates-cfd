# Verification report: C2_euler_large_timestep (C-llm-r3)

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
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified either.
  - R0 is well averaged and statistically converged. Drag averaging uncertainty is 9.486e-07 and statistics uncertainty is 0.0001664. Strouhal averaging uncertainty is 1.575e-05 and statistics uncertainty is 0.0001267. There are 12 stationary cycles.
  - Mesh, time and domain uncertainty components are all unmeasured for both quantities (INCONCLUSIVE). No combined uncertainty can be formed against the 0.03 tolerance.
  - The time discretisation is the most suspect. R0 uses the Euler scheme with max Courant 2.9248 and 2 PIMPLE outer correctors at dt = 0.04 D/U. That gives 157.74 steps per shedding period. The courant_number check is INCONCLUSIVE because temporal accuracy is unproven. Euler is first order, so a time-step error would bias the Strouhal number and mean drag directly.
  - The spatial discretisation is second-order convection (linearUpwind). The mesh has 160 cells around the cylinder, a wall_first_cell_D of 0.005, and a wake_last_cell_D of 1.0209. It is unrefined, so a mesh error is possible, but it is a second candidate.
  - The domain extents are 30D upstream, 50D downstream and 40D half-height, with blockage 0.0125. They are large and the cells are not changed by domain expansion, so this is the least likely to move the answer by more than 3%.
  - REDUCE_TIME_STEP isolates the time error on the identical mesh. REFINE_MESH could also change the time step if the Courant limit is hit, which would confound the two effects. Its estimated cost (1126 s) is comparable to the other options and well within the budget (0 of 6 experiments used, 0 of 12 compute units used).
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — R0 is first-order in time (Euler) with max Courant 2.9248 and 2 outer correctors. The verifier says temporal accuracy is unproven without time-step refinement. This is the most likely flaw to move St or Cd by more than the tolerance. Halving dt on the identical mesh isolates it cleanly.
  - Outcome: executed -> C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and nothing measured supports REJECT.
  - R0 is well averaged and statistically converged. Drag averaging is 9.486e-07 and statistics 0.0001664. Strouhal averaging is 1.575e-05 and statistics 0.0001267. R0 has 12 stationary cycles.
  - R1 (dt halved from 0.04 to 0.02, same mesh) moved Cd from 1.2901 to 1.3047 and St from 0.15849 to 0.16097. The verifier records these as demonstrated changes of 1.11% and 1.54%. Both are below the 3% tolerance, so there is no FAIL.
  - The time component is still unresolved. The verifier's two-level Richardson estimate, with assumed order p=1 and Fs=3, gives 0.06683 for Cd and 0.09224 for St. Both exceed 0.5*tolerance (1.5%) and the 3% tolerance. The St change of 1.54% is already above 1.5%.
  - Both quantities shift in the same direction with dt. With only two levels the observed order cannot be measured, so the p=1 assumption is untested. The time error is the largest known contributor and is not yet bounded.
  - A third time-step level on R1 gives the observed convergence order. It either confirms asymptotic convergence with a smaller extrapolated error, or shows the error is still large.
  - Mesh and domain components are still unmeasured for both quantities (no REFINE_MESH or EXPAND_DOMAIN run). They cannot be closed until the time error is bounded, so mesh and domain remain next in line.
  - Budget allows this: 1 of 6 experiments and 1.07 of 12 compute units are used. The estimated cost of 2252 s from parent R1 is affordable.
  - Caveat: R1 has a shorter record, with 6 stationary cycles and a stationary-window start at the MSER cap (42.506). Its statistics are still tight (Cd CI95 4.1571e-05).
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — The time component has the largest recorded uncertainty (Cd 0.06683, St 0.09224). It rests on a two-level estimate with assumed order p=1. Continuing the dt family from R1 (dt = 0.02) to dt = 0.01 gives a third level, so the observed order and a measured extrapolation can replace the assumption. The mesh is unchanged, so the effect is isolated.
  - Outcome: executed -> C2_euler_large_timestep.dt0.01-f9cf9b35455e (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. The measured evidence does not support a REJECT either.
  - R0 averaging and statistics are well controlled. Drag: averaging 9.486e-07, statistics 0.0001664. St: averaging 1.575e-05, statistics 0.0001267. R0 has 12 stationary cycles.
  - The dt family R0 (dt 0.04), R1 (0.02), R2 (0.01) is monotonic. Cd goes 1.2901 -> 1.3047 -> 1.3139. St goes 0.15849 -> 0.16097 -> 0.16232. Rms Cl goes 0.18045 -> 0.19618 -> 0.2052.
  - The three-level Celik analysis gives an observed order p=0.66 for Cd and p=0.88 for St. Time uncertainty of the root is 0.03719 for Cd and 0.04147 for St. Both exceed 0.5*tolerance (1.5%), and both are above the 3% tolerance.
  - The verifier's demonstrated R0-to-R2 changes are 1.81% (Cd) and 2.36% (St). These are below tau, so there is no deterministic FAIL yet.
  - The successive changes shrink only slowly. The observed order is below the nominal first order of Euler, so the sequence is probably not yet asymptotic. The time component cannot be closed or bounded reliably from three levels.
  - Mesh and domain are still unmeasured for both quantities (no REFINE_MESH or EXPAND_DOMAIN run). The combined uncertainty therefore cannot be formed.
  - R1 and R2 have shorter records (80 convective units, 6 cycles, window start at the MSER cap) than R0 (150 units, 12 cycles). Their statistical CI95 values are small (Cd 4.1571e-05 and 2.496e-05), but this is a mild confound for comparing the time levels.
  - Budget: 2 of 6 experiments used and 3.2 of 12 compute units used. A further dt halving from R2 costs an estimated 4504 s, about 4.3 units of R0 cost. That leaves room for one mesh run and one domain run from R0 (1130 s and 748 s).
  - Time is still the largest known uncertainty and it drives the verdict for the root. A fourth level tests whether the error is asymptotic. It also shows whether the R0-to-finest change passes tau, which would give a deterministic FAIL, or whether the time error closes.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C2_euler_large_timestep.dt0.01-f9cf9b35455e — Time is the dominant recorded uncertainty (Cd 0.03719, St 0.04147). The observed orders are low (p=0.66 and p=0.88) and the dt sequence has not flattened (St 0.15849 -> 0.16097 -> 0.16232). A fourth level on the same mesh isolates the temporal error and checks whether the sequence is asymptotic. It also shows whether the root's demonstrated change exceeds tolerance.
  - Outcome: executed -> C2_euler_large_timestep.dt0.005-752b3af02251 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 4.3

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not supported, because the demonstrated R0-to-R3 changes (Cd 2.17%, St 2.77%) are below the 0.03 tolerance.
  - R0 averaging and statistics are well controlled. Cd averaging is 9.486e-07 and statistics 0.0001664. St averaging is 1.575e-05 and statistics 0.0001267. R0 has 12 stationary cycles.
  - The dt family is monotone: Cd goes 1.2901 (R0), 1.3047 (R1), 1.3139 (R2), 1.3188 (R3). St goes 0.15849, 0.16097, 0.16232, 0.163. Each successive change is smaller than the one before. The sequence is converging, but R0 is still on the coarse-dt side.
  - The time component is INCONCLUSIVE: Cd 0.0332 at observed order p=0.81, and St 0.04024 at p=0.93. Both exceed 0.5*tolerance. The root's time error is the dominant known term.
  - No further REDUCE_TIME_STEP is possible. R3 is at the limit (dt 0.005 D/U, and the menu says 0.0025 is not allowed). R3 is also the only run parent whose RUN_LONGER, REFINE_MESH or EXPAND_DOMAIN cost is prohibitive (9039, 5980 and 5631 s). The time family is therefore as refined as the menu permits.
  - Mesh and domain are unmeasured for both quantities (no REFINE_MESH or EXPAND_DOMAIN run). No combined uncertainty can be formed. These are the largest unknowns that an experiment can still address.
  - Mesh is the most likely remaining flaw. R0 has 160 cells around the cylinder, representative_cell_size_D 0.45745 and wake_last_cell_D 1.0209. The strong dt sensitivity of rms Cl (0.18045 to 0.21018) shows a wake that responds strongly to numerical damping. Such a wake is likely to respond to spatial resolution as well.
  - Domain truncation is less likely to matter. The domain is 30D upstream, 50D downstream and 40D half-height, with blockage 0.0125. It is cheaper (R0: 748 s) and should be run next if budget remains.
  - Budget: 3 of 6 experiments and 7.47 of 12 compute units are used. A REFINE_MESH from R0 costs 1130 s, about 1.07 units, which is affordable. Refining from R0 keeps dt equal to the root. That isolates the mesh effect from the already-measured time effect, and it is the cheapest parent.
  - Even if mesh and domain pass, the root run (dt 0.04) carries a time uncertainty above tolerance on its own. The deterministic verifier would then likely stay INCONCLUSIVE or FAIL for R0. The mesh and domain results are still needed to find out whether a finer-dt, finer-mesh answer can be trusted.
  - Requested: REFINE_MESH {'factor': 1.4142} on C2_euler_large_timestep-268eddd71f94 — Mesh error is entirely unmeasured for both quantities. The dt family cannot be refined further, and domain truncation is a less likely source of a 3% shift. R0 as parent is the cheapest option (1130 s) and keeps dt equal to the root, so the mesh effect is separated from the measured time effect.
  - Outcome: executed -> C2_euler_large_timestep.m1.41-eb9ef468444b (failed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.07

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not supported, because the largest demonstrated change from R0 to R3 (Cd 2.17%, St 2.77%) is below the 0.03 tolerance.
  - R0 is well averaged and statistically converged. Cd averaging is 9.486e-07 and statistics 0.0001664. St averaging is 1.575e-05 and statistics 0.0001267. There are 12 stationary cycles.
  - The dt family is monotone and converging. Cd goes 1.2901 (R0), 1.3047 (R1), 1.3139 (R2), 1.3188 (R3). St goes 0.15849, 0.16097, 0.16232, 0.163. The time uncertainty of the root is Cd 0.0332 (p=0.81) and St 0.04024 (p=0.93). Both exceed 0.5*tolerance, so the time component stays INCONCLUSIVE. R3 is at the dt limit, so no further REDUCE_TIME_STEP is possible.
  - R4 (REFINE_MESH from R0, factor 1.4142, dt 0.04 kept) diverged after 73 steps. Its max Courant was 3.1978e+103 and the mass imbalance was 1.8456e+76. It gives no mesh information. It also shows that refining at the root's dt of 0.04 is unstable. The root's max Courant of 2.9248 was already large, and refinement shrinks the cell size from 0.45745 D to 0.32292 D.
  - A repeat from R0 would probably diverge again. Refining from R1 (dt 0.02, max Courant 1.1744) gives an estimated Courant of about 1.6 after refinement. That is below R0's stable 2.9248. Refining from R2 would be safer but costs 4520 s (about 4.3 units) and would use almost all the remaining budget.
  - Mesh and domain errors are still unmeasured for both quantities. A mesh run is needed to bound the mesh component. The parent R1 gives a clean same-dt comparison: only the mesh changes, and R1 already has Cd 1.3047 and St 0.16097 to compare against.
  - Budget: 4 of 6 experiments and 7.51 of 12 units are used. REFINE_MESH from R1 costs 2260 s (about 2.14 units), leaving about 2.35 units. That is enough for one EXPAND_DOMAIN run from R0 (748 s) or R1 (1495 s).
  - Caveat: even if mesh and domain pass, the root's own time uncertainty (Cd 0.0332, St 0.04024) is above tolerance. The root is likely to stay INCONCLUSIVE or fail the time component. The mesh and domain results are still needed to know whether any answer can be trusted.
  - Requested: REFINE_MESH {'factor': 1.4142} on C2_euler_large_timestep.dt0.02-2f2ce6b4d241 — Mesh error is entirely unmeasured. R4 from R0 diverged (max Courant 3.1978e+103), so a mesh comparison at dt=0.04 is not viable. R1 has dt=0.02 and max Courant 1.1744, which leaves headroom for refinement. It keeps dt equal to its parent, so the mesh effect is isolated. It costs about 2.14 units of the 4.49 remaining, which still leaves room for an EXPAND_DOMAIN run.
  - Outcome: executed -> C2_euler_large_timestep.m1.41-9ec9f782d7ff (completed)
  - Numeric audit: 6 number(s) not traceable to evidence: 1.6, 4.3, 2.14, 2.35, 2.14

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not allowed either, because the demonstrated R0-to-R3 changes (Cd 2.17%, St 2.77%) are below the 0.03 tolerance.
  - R0 is well averaged and statistically converged: Cd averaging 9.486e-07, statistics 0.0001664; St averaging 1.575e-05, statistics 0.0001267; 12 stationary cycles.
  - The time family is monotone and converging: Cd 1.2901 (R0), 1.3047 (R1), 1.3139 (R2), 1.3188 (R3); St 0.15849, 0.16097, 0.16232, 0.163. The root time uncertainty is Cd 0.0332 (p=0.81) and St 0.04024 (p=0.93). Both exceed 0.5*tolerance. R3 is at the dt limit, so this component cannot be improved further.
  - R5 (REFINE_MESH from R1) is flagged 'completed' but is numerically invalid and must not be used as mesh evidence. It reports Cd 0.29242, rms Cl 3.6727, St 25.0 and max Courant 12.006, with 20.871 steps per shedding period. Its drag drift is 0.171 and its half-difference is 0.32385. R0-R3 recorded rms Cl of only 0.18-0.21 and St of about 0.16. A finished run is not a healthy run. The verifier still reports the mesh component as 'no REFINE_MESH experiment has been run', so it did not accept R5 as a valid mesh result.
  - R4 (from R0) diverged after 73 steps, with max Courant 3.1978e+103 and mass imbalance 1.8456e+76. R5 (from R1, dt halved) also failed. Both refined meshes (228 cells around the cylinder, wall_first_cell_D 0.0035832, patch extent 0.0099991 m) were unstable at different dt. This suggests the refined mesh or its setup is the problem, not only the Courant number. A third refinement attempt has a high chance of failing again.
  - Budget: 5 of 6 experiments used, 9.65 of 12 compute units used, so about 2.35 units remain and exactly one experiment is left. REFINE_MESH from R2 (4520 s) and RUN_LONGER from R2 (2815 s) are unaffordable. Other mesh or time options from R3 are also unaffordable.
  - EXPAND_DOMAIN from R0 costs 748 s, about 0.71 units. The near-field mesh is unchanged, so it avoids the instability seen in R4 and R5. It uses the root as parent, so the domain effect is isolated from the measured time effect. It closes one unmeasured component, and a demonstrated change above tolerance would give a deterministic FAIL.
  - Caveat: even if the domain check passes, mesh stays unmeasured and the root's time uncertainty (Cd 0.0332, St 0.04024) stays above 0.5*tolerance. The system will probably end INCONCLUSIVE. This is the most informative reliable use of the last experiment.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C2_euler_large_timestep-268eddd71f94 — Domain error is unmeasured for both quantities. Both REFINE_MESH attempts were unusable (R4 diverged, R5 gave St 25.0 and rms Cl 3.6727), and a third attempt would probably fail. EXPAND_DOMAIN leaves the near-field mesh unchanged, so it should run stably. It costs about 748 s (about 0.71 units) against about 2.35 units remaining. R0 as parent compares directly against the root at the same dt.
  - Outcome: executed -> C2_euler_large_timestep.D2x-a912f88e2d43 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 2.35, 0.71, 0.71, 2.35

Run C2_euler_large_timestep.dt0.02-2f2ce6b4d241: REDUCE_TIME_STEP from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, time.delta_t: 0.04→0.02, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2901 → 1.3047 (+1.13%).
  - Observation: strouhal_number 0.15848 → 0.16096 (+1.56%).

Run C2_euler_large_timestep.dt0.01-f9cf9b35455e: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (time.delta_t: 0.02→0.01).
  - Observation: mean_drag_coefficient 1.3047 → 1.3139 (+0.70%).
  - Observation: strouhal_number 0.16096 → 0.16231 (+0.84%).

Run C2_euler_large_timestep.dt0.005-752b3af02251: REDUCE_TIME_STEP from C2_euler_large_timestep.dt0.01-f9cf9b35455e (time.delta_t: 0.01→0.005).
  - Observation: mean_drag_coefficient 1.3139 → 1.3188 (+0.37%).
  - Observation: strouhal_number 0.16231 → 0.163 (+0.42%).

Run C2_euler_large_timestep.m1.41-eb9ef468444b: REFINE_MESH from C2_euler_large_timestep-268eddd71f94 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.end_time: 150→80).

Run C2_euler_large_timestep.m1.41-9ec9f782d7ff: REFINE_MESH from C2_euler_large_timestep.dt0.02-2f2ce6b4d241 (mesh.refinement: 1→1.414).
  - Observation: mean_drag_coefficient 1.3047 → 0.30334 (-76.75%).
  - Observation: strouhal_number 0.16096 → 2.3956 (+1388.36%).

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
- `C2_euler_large_timestep.m1.41-eb9ef468444b` status=failed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T09:08:42+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m1.41-eb9ef468444b/run.json
- `C2_euler_large_timestep.m1.41-9ec9f782d7ff` status=completed parent=C2_euler_large_timestep.dt0.02-2f2ce6b4d241 created=2026-10-20T01:17:15+00:00 wall=2536 s; record: results/runs/C2_euler_large_timestep.m1.41-9ec9f782d7ff/run.json
- `C2_euler_large_timestep.D2x-a912f88e2d43` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T19:14:28+00:00 wall=643.5 s; record: results/runs/C2_euler_large_timestep.D2x-a912f88e2d43/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1187383718.0, "relative_to_root": 10.354338068454327, "experiment_wall_seconds": 7957.117383687017, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.61916976, "loop_wall_seconds": 178.77622174400312}
