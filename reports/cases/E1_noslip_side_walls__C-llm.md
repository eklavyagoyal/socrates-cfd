# Verification report: E1_noslip_side_walls (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3403
- strouhal_number: 0.16429

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 9.70e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.96% > 1.50% but the demonstrated change 0.89% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.20, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.46% > 1.50% but the demonstrated change 1.28% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.50, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.83% <= 1.50% (root-to-finest change 0.209%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.55% <= 1.50% (root-to-finest change 0.137%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.7e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.13% > 1.50% but the demonstrated change 1.08% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.46, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.51% > 1.50% but the demonstrated change 0.78% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.51, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=9.32e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.0012
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0196
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.00834
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0213
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D1.5x-f702a7c7fa9d
    └── E1_noslip_side_walls.D2x-1620b1098386

CLAIM: strouhal_number of run E1_noslip_side_walls-88a7cd5812e8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mesh_quality: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── mass_conservation: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── linear_solver_convergence: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── courant_number: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── reynolds_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── force_reference_consistency: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── physics_regime: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── convection_scheme_order: PASS
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Averaging window (reported vs stationary value): PASS U=6.51e-05
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Temporal statistics (stationarity, cycles): PASS U=0.00097
│   └── E1_noslip_side_walls-88a7cd5812e8
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0246
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.00547
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0151
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D1.5x-f702a7c7fa9d
    └── E1_noslip_side_walls.D2x-1620b1098386

```

## EXPERIMENT HISTORY

Run E1_noslip_side_walls-88a7cd5812e8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. Mesh, time and domain uncertainty are all unmeasured for both mean_drag_coefficient and strouhal_number, so ACCEPT is not allowed. REJECT is not allowed either, because nothing has failed.
  - R0 averaging and statistics are within budget. For drag, averaging is 9.319e-05 and statistics is 0.001199. For Strouhal, averaging is 6.507e-05 and statistics is 0.0009705. The stationary window has 13 cycles and drag drift is 0.0011988. The requested tolerance is 0.03 for both quantities.
  - R0 sets the lateral boundary to noSlipWall at half_height_D=40.0, with upstream_D=30.0 and downstream_D=50.0. The question says to treat the stream as unbounded. A no-slip wall is not a far-field condition. It can add a wall boundary layer and extra blockage (blockage_ratio 0.0125), and that could bias drag and shedding frequency. This is the most suspicious configuration choice relative to the requirement.
  - Domain error is the cheapest component to measure (1311 s versus 2284 s for mesh and 1974 s for time step). It tests a setup choice that conflicts with the problem statement.
  - Mesh and time-step resolution are secondary concerns that still need measuring. R0 has 30580 cells, 160 cells around the cylinder, and a wake last cell of 1.0209 D. Time step is 0.01 with max Courant 0.73374 and 608.73 steps per shedding period. Both concerns remain open, and budget allows them (6 experiments, 12x compute).
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — R0 uses noSlipWall lateral boundaries at 40 D with blockage_ratio 0.0125, but the problem requires an unbounded stream. This is the most likely flaw to change the answer, and it is the cheapest experiment (1311 s).
  - Outcome: executed -> E1_noslip_side_walls.D2x-1620b1098386 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT is not allowed because nothing has failed.
  - R0 averaging and statistics pass. Drag: averaging 9.319e-05, statistics 0.001199. Strouhal: averaging 6.507e-05, statistics 0.0009705. The stationary window has 13 cycles.
  - Domain (R0 vs R1): drag changed by 1.08% and Strouhal by 0.78%, both below the 0.03 tolerance. The verifier still reports domain uncertainty of 0.0647 (drag) and 0.04674 (Strouhal). That figure uses an assumed order p=1 with Fs=3, so it is a conservative estimate and not a measured error.
  - The R0-to-R1 comparison is confounded. R1 has representative_cell_size_D 0.79405 against 0.45745 for R0, and wake_last_cell_D 1.9729 against 1.0209. R1 also has 6 stationary cycles against 13, and checkMesh_ok false. The 1.08% and 0.78% changes therefore mix domain and far-field resolution effects. R1 cannot serve as a clean parent.
  - Mesh and time-step errors are completely unmeasured for both quantities. R0 has 30580 cells, a representative cell size of 0.45745 D and wake_last_cell_D 1.0209. It is the coarsest resolution in the package and the most likely hidden flaw that could shift drag or Strouhal number by more than 3%.
  - Time step: 0.01 D/U, max Courant 0.73374, 608.73 steps per period, backward scheme. Temporal error is plausibly small but unmeasured, so it is the next priority after mesh.
  - Budget allows it: 1 of 6 experiments used and 0.71 of 12.0 compute used. REFINE_MESH from R0 costs 2284 s. R0 is the right parent because R1 has checkMesh_ok false and a coarser far-field mesh.
  - Requested: REFINE_MESH {'factor': 1.4142} on E1_noslip_side_walls-88a7cd5812e8 — Mesh error is unmeasured for both quantities, and R0 has the coarsest resolution in the package (representative cell size 0.45745 D, wake_last_cell_D 1.0209). R1 showed domain changes of only 1.08% (drag) and 0.78% (Strouhal), so mesh is the largest remaining unknown. R0 is the parent because R1 has checkMesh_ok false and a coarser far-field mesh.
  - Outcome: executed -> E1_noslip_side_walls.m1.41-f15d7e2db685 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no checks failed. ACCEPT is not allowed because mesh, time and domain are not within budget. REJECT is not allowed because nothing has failed.
  - R0 averaging and statistics pass. Drag: averaging 9.319e-05, statistics 0.001199. Strouhal: averaging 6.507e-05, statistics 0.0009705. The stationary window has 13 cycles against a tolerance of 0.03.
  - Mesh, R0 to R2: Cd changed from 1.3402 to 1.3475 (0.54%) and St from 0.16428 to 0.16562 (0.81%). Both changes are below the tolerance. The verifier still estimates mesh uncertainty at 0.03243 (Cd) and 0.04838 (St), which is above the 0.015 half-tolerance limit. That estimate uses an assumed order p=2 and Fs=3.
  - R2 is confounded: it changed the time step from 0.01 to 0.0086733 as well as the mesh (cells 61366, 228 cells around the cylinder). The mesh estimate therefore also contains an unmeasured temporal effect.
  - Time uncertainty has never been measured for either quantity. Every run uses dt of 0.01 or 0.0086733 with the backward scheme and a max Courant number of 0.73374 (R0) or 0.73815 (R2). The verifier cannot give a combined uncertainty or ACCEPT without a REDUCE_TIME_STEP run.
  - Domain, R0 to R1: Cd changed by 1.08% and St by 0.78%. The verifier estimate is 0.0647 (Cd) and 0.04674 (St) with assumed p=1. R1 has a coarser mesh (representative size 0.79405 D against 0.45745 D), only 6 stationary cycles, and checkMesh_ok false. Its domain signal is confounded, so repeating a domain run now would not be clean.
  - REDUCE_TIME_STEP on R0 is the cheapest experiment that isolates a completely missing component (1974 s). It also separates the time effect from the mesh effect seen in R2. The budget allows it: 2 of 6 experiments used and 1.94 of 12.0 compute used.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Time error is unmeasured for both quantities and is required for any ACCEPT. R0 is the clean parent because R1 has checkMesh_ok false and a coarser mesh. The run isolates the time effect that R2 confounded with the mesh effect, and it is cheap (1974 s).
  - Outcome: executed -> E1_noslip_side_walls.dt0.005-c41af2c90410 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and REJECT is not allowed because nothing has failed.
  - Within budget for R0: averaging (Cd 9.319e-05, St 6.507e-05), statistics (Cd 0.001199, St 0.0009705) and time (Cd 0.008342, St 0.005466). R3 (dt 0.005) moved Cd from 1.3402 to 1.3374 (0.209%) and St by 0.137%. The time component is now measured and passes.
  - Mesh is still INCONCLUSIVE: Cd 0.03243 and St 0.04838. Both exceed half the tolerance (0.015). R0 to R2 changed Cd by 0.54% and St by 0.81%, which is below the 0.03 tolerance. The verifier's estimate rests on an assumed order p=2 with Fs=3 from only two mesh levels. The order has not been measured.
  - Domain is still INCONCLUSIVE: Cd 0.0647 and St 0.04674. The observed R0 to R1 changes were 1.08% (Cd) and 0.78% (St). The estimate uses an assumed order p=1. R1 is not a clean domain level. Its representative cell size is 0.79405 D against 0.45745 D in R0, its wake_last_cell_D is 1.9729 against 1.0209, it has only 6 stationary cycles, and checkMesh_ok is false.
  - R2 (finer mesh, lower values at coarser resolution) and R1 (coarser mesh, Cd 1.3259 and St 0.163, both below R0) point the same way. Part of R1's apparent domain effect may therefore be a mesh-resolution effect. Mesh convergence has to be pinned down before the domain signal can be interpreted.
  - R3 shows that the time step is a small effect (0.209% in Cd). Most of the R0 to R2 change can therefore be attributed to the mesh. This removes the confound noted at iteration 3.
  - Choosing REFINE_MESH from R2 with factor 1.4142 gives R0, R2 and a new finer run at a near-constant refinement ratio. That allows a measured convergence order and removes the assumed p=2. Cost is 5280 s. Budget used is 3 of 6 experiments and 3.01 of 12.0 compute, so one or two further runs, such as a domain run, remain affordable.
  - Requested: REFINE_MESH {'factor': 1.4142} on E1_noslip_side_walls.m1.41-f15d7e2db685 — Mesh uncertainty (Cd 0.03243, St 0.04838) rests on two levels with an assumed order p=2. R3 showed the time step effect is small (Cd 0.209%, St 0.137%), so R0 to R2 is largely a clean mesh signal. A further level from R2 gives a constant-ratio three-level sequence (R0, R2, new) and a measured order. It also separates mesh from domain effects in R1.
  - Outcome: executed -> E1_noslip_side_walls.m2-24c0dd986308 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because mesh and domain are outside budget. REJECT is not allowed because nothing has failed.
  - R0 averaging, statistics and time are within budget. Cd: averaging 9.319e-05, statistics 0.001199, time 0.008342. St: averaging 6.507e-05, statistics 0.0009705, time 0.005466. R3 (dt 0.005) moved Cd from 1.3402 to 1.3374 and St from 0.16428 to 0.1645.
  - Mesh is now a three-level Celik estimate from R0, R2 and R4: Cd 0.01959 (p=1.20) and St 0.02459 (p=1.50). Both exceed the 0.015 half-tolerance limit. Cd rose 1.3402 -> 1.3475 -> 1.3523 and St rose 0.16428 -> 0.16562 -> 0.16641. The changes shrink with refinement. The menu allows no further refinement of R4, because the cumulative refinement limit is exceeded. More mesh work is therefore not the best use of budget.
  - Domain is the largest unresolved component: Cd 0.0647 and St 0.04674. Both rest on an assumed order p=1 with Fs=3 and only two levels (R0, R1). The observed R0 -> R1 changes were 1.08% (Cd) and 0.78% (St), both below the 0.03 tolerance.
  - R1 is a poor domain level. Its representative cell size is 0.79405 D against 0.45745 D for R0, wake_last_cell_D is 1.9729 against 1.0209, it has 6 stationary cycles against 13, and checkMesh_ok is false. Its change therefore mixes domain and far-field resolution effects. The R4 trend in the mesh sequence also shows Cd and St falling as the mesh coarsens, in the same direction as R1.
  - A third domain level from R0 at factor 1.5 gives a sequence R0 (1x), new run (1.5x), R1 (2x) with the near-field mesh unchanged. That allows a measured domain order in place of the assumed p=1. Its parent R0 passes checkMesh and has the most stationary cycles. It should be cheaper than the 1311 s listed for factor 2 from R0.
  - Budget: 4 of 6 experiments used and 5.86 of 12.0 compute used, so this run is affordable.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on E1_noslip_side_walls-88a7cd5812e8 — Domain is the largest unresolved component (Cd 0.0647, St 0.04674, assumed p=1 from two levels). R1 is confounded by a coarser far-field mesh, so the observed 1.08% and 0.78% changes are not a clean domain signal. A third level at 1.5x from R0 (near-field unchanged) gives R0, new run and R1 as a three-level sequence, so the order can be measured.
  - Outcome: executed -> E1_noslip_side_walls.D1.5x-f702a7c7fa9d (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. REJECT is not allowed because no check has failed.
  - R0 averaging, statistics and time pass. Cd: averaging 9.319e-05, statistics 0.001199, time 0.008342. St: averaging 6.507e-05, statistics 0.0009705, time 0.005466. R3 (dt 0.005) moved Cd from 1.3402 to 1.3374 and St from 0.16428 to 0.1645.
  - Mesh is still INCONCLUSIVE. It uses a three-level Celik estimate from R0, R2 and R4. Cd is 0.01959 (p=1.20) and St is 0.02459 (p=1.50). Both exceed the 0.015 half-tolerance limit. Cd rose 1.3402 -> 1.3475 -> 1.3523 and St rose 0.16428 -> 0.16562 -> 0.16641.
  - The R0-based mesh sequence cannot be extended. The menu lists REFINE_MESH from R4 as not allowed (cumulative refinement 2.83 exceeds limit 2.0). Any further mesh run from R0, R2 or R3 cannot add a finer level than R4, so R0's mesh component cannot be brought under 0.015.
  - Domain is still INCONCLUSIVE. The three-level sequence is R0, R5 and R1, with measured orders p=1.46 (Cd) and p=1.51 (St). Cd is 0.02135 and St is 0.01505. Cd fell 1.3402 -> 1.3302 -> 1.3259 and St fell 0.16428 -> 0.16338 -> 0.16301 as the domain grew. The decrease is monotone and shrinks, but the estimated domain uncertainty of R0 is still above 0.015. This is consistent with a real truncation/blockage bias from the noSlipWall lateral boundaries at 40 D (blockage_ratio 0.0125).
  - The error budget requires every component to be <= 0.5*tolerance, which is 0.015. Mesh (Cd 0.01959, St 0.02459) and domain (Cd 0.02135, St 0.01505) both exceed that for R0. Mesh cannot be improved, so one more run (5 of 6 used) cannot lead to ACCEPT. A domain run alone would still leave the mesh component INCONCLUSIVE.
  - Nothing has been measured that invalidates R0 by more than the 0.03 tolerance. The demonstrated changes (Cd 0.89% mesh, 1.08% domain; St 1.28% mesh, 0.78% domain) are all below tolerance. That is why this is not a REJECT. The honest outcome is INCONCLUSIVE, not a pass.
  - Outcome: planner chose to stop (no useful affordable experiment)

Run E1_noslip_side_walls.D2x-1620b1098386: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3259 (-1.07%).
  - Observation: strouhal_number 0.16428 → 0.16301 (-0.77%).

Run E1_noslip_side_walls.m1.41-f15d7e2db685: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3475 (+0.55%).
  - Observation: strouhal_number 0.16428 → 0.16562 (+0.82%).

Run E1_noslip_side_walls.dt0.005-c41af2c90410: REDUCE_TIME_STEP from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3374 (-0.21%).
  - Observation: strouhal_number 0.16428 → 0.1645 (+0.14%).

Run E1_noslip_side_walls.m2-24c0dd986308: REFINE_MESH from E1_noslip_side_walls.m1.41-f15d7e2db685 (mesh.refinement: 1.414→2, time.delta_t: 0.008673→0.007478).
  - Observation: mean_drag_coefficient 1.3475 → 1.3523 (+0.35%).
  - Observation: strouhal_number 0.16562 → 0.16641 (+0.48%).

Run E1_noslip_side_walls.D1.5x-f702a7c7fa9d: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3302 (-0.75%).
  - Observation: strouhal_number 0.16428 → 0.16338 (-0.55%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `E1_noslip_side_walls-88a7cd5812e8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1851 s; record: results/runs/E1_noslip_side_walls-88a7cd5812e8/run.json
- `E1_noslip_side_walls.D2x-1620b1098386` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T20:14:34+00:00 wall=1058 s; record: results/runs/E1_noslip_side_walls.D2x-1620b1098386/run.json
- `E1_noslip_side_walls.m1.41-f15d7e2db685` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:08:43+00:00 wall=2302 s; record: results/runs/E1_noslip_side_walls.m1.41-f15d7e2db685/run.json
- `E1_noslip_side_walls.dt0.005-c41af2c90410` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T01:16:41+00:00 wall=1163 s; record: results/runs/E1_noslip_side_walls.dt0.005-c41af2c90410/run.json
- `E1_noslip_side_walls.m2-24c0dd986308` status=completed parent=E1_noslip_side_walls.m1.41-f15d7e2db685 created=2026-10-20T01:15:34+00:00 wall=5373 s; record: results/runs/E1_noslip_side_walls.m2-24c0dd986308/run.json
- `E1_noslip_side_walls.D1.5x-f702a7c7fa9d` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T02:45:52+00:00 wall=862.7 s; record: results/runs/E1_noslip_side_walls.D1.5x-f702a7c7fa9d/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 2979717664.0, "relative_to_root": 6.496005371702638, "experiment_wall_seconds": 10758.546012559997, "n_experiments": 5, "planner_calls": 6, "planner_cost_usd": 0.599796155, "loop_wall_seconds": 7420.505871934}
