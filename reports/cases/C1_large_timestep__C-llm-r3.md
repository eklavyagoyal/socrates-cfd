# Verification report: C1_large_timestep (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3238
- strouhal_number: 0.16351

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 3.42 with 3 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.03e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 8.42e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.08% <= 1.50% (root-to-finest change 0.019%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.0e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.25% <= 1.50% (root-to-finest change 0.064%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.4e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.20% <= 1.50% (root-to-finest change 0.820%) [three-level Celik procedure, observed order p=1.75, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.58% > 1.50% but the demonstrated change 0.53% <= tau; more refinement would be needed [differences within 2x statistical noise (2.4e-03); range-based U with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=8.69e-05
│   └── C1_large_timestep-49d90ffccdac
├── Temporal statistics (stationarity, cycles): PASS U=0.000103
│   └── C1_large_timestep-49d90ffccdac
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.000765
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): PASS U=0.012
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D3x-f035e789cb02

CLAIM: strouhal_number of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=1.26e-05
│   └── C1_large_timestep-49d90ffccdac
├── Temporal statistics (stationarity, cycles): PASS U=8.42e-05
│   └── C1_large_timestep-49d90ffccdac
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.00254
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0158
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D3x-f035e789cb02

```

## EXPERIMENT HISTORY

Run C1_large_timestep-49d90ffccdac: submitted simulation (30580 cells, dt=0.05 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable.
  - Averaging and statistics components pass for both quantities. Drag: 8.688e-05 and 1.028e-04. Strouhal: 1.261e-05 and 8.418e-05. R0 has 12 stationary cycles, and drag drift is 1.03e-04 relative.
  - Mesh, time and domain components are all unmeasured for both quantities. Neither requested quantity can be accepted until each is measured.
  - R0 mesh is coarse: 30580 cells, representative size 0.45745 D, 160 cells around the cylinder, and wake_last_cell_D 1.0209. The wake region that sets shedding frequency and drag is probably under-resolved. Spatial error is the most likely component to exceed 0.5*tolerance (1.5%).
  - Time-step evidence is weaker but not alarming. Max Courant number is 3.4157 with 3 outer correctors, and backward differencing gives 122.32 steps per shedding period. Courant is flagged INCONCLUSIVE, not FAIL.
  - Domain evidence is also weaker. Blockage is 0.0125 with 30 D upstream, 50 D downstream and 40 D half-height, and the sides are symmetryPlane. The truncation effect is probably smaller than the mesh effect.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute. R0 mesh refinement costs about 1240 s, close to R0's 1158.6 s.
  - Requested: REFINE_MESH {'factor': 2.0} on C1_large_timestep-49d90ffccdac — R0 has the coarsest-looking resolution, and mesh error is the component most likely to change either quantity by more than the tolerance. Factor 2.0 gives the strongest signal for estimating spatial error, and the budget allows it.
  - Outcome: executed -> C1_large_timestep.m2-6e4f672cac17 (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable.
  - R0 averaging and statistics components pass for both quantities. Drag: 8.688e-05 and 1.028e-04. Strouhal: 1.261e-05 and 8.418e-05. R0 has 12 stationary cycles. The stationary window start is the MSER cap (70.747).
  - Mesh, time and domain components are still unmeasured for both quantities, so no combined uncertainty exists.
  - R1 (REFINE_MESH, factor 2.0, cells 122320) diverged after 44 steps (record length 2.1 convective units). Its max Courant number is 9.2409e+102 and its mass imbalance is 3.8064e+86. It has no force or Strouhal data. A diverged run is not evidence about mesh convergence, and it does not invalidate R0, which completed with Courant 3.4157 and mass imbalance 2.5e-10.
  - R1 kept the time step of 0.05, while its finer mesh (320 cells around the cylinder, wall_first_cell_D 0.0025143) raises the Courant number. The likely cause is an instability from too large a Courant number at startup. I cannot confirm this from the package, because only the final divergent values are recorded.
  - REFINE_MESH from R1 is not allowed (cumulative refinement 2.83 exceeds the 2.0 limit). The mesh component can therefore only be measured by a new refinement child of R0.
  - R0 is still coarse (representative size 0.45745 D, wake_last_cell_D 1.0209), so mesh error is still the most likely component to exceed 1.5%. A milder factor of 1.4142 is more likely to stay stable than 2.0 and still gives a measurable difference.
  - Budget remains: 1 of 6 experiments used, compute 0.06 of 12. A retry costs about 1240 s, so a second failure is affordable.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep-49d90ffccdac — The factor 2.0 refinement (R1) diverged, so the mesh error is still unmeasured. Mesh error is the component most likely to exceed 1.5% on R0's coarse mesh. A factor of 1.4142 keeps the Courant number increase moderate and still gives a measurable difference. R1 cannot be refined further.
  - Outcome: executed -> C1_large_timestep.m1.41-c9c1535204d3 (failed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both unavailable.
  - R0 averaging and statistics components pass for both quantities. Drag: 8.688e-05 and 1.028e-04. Strouhal: 1.261e-05 and 8.418e-05. R0 has 12 stationary cycles.
  - Mesh, time and domain components are still unmeasured for both quantities, so no combined uncertainty exists.
  - R1 (factor 2.0, 122320 cells) diverged after 44 steps. R2 (factor 1.4142, 61366 cells) diverged after 52 steps. Their max Courant numbers are 9.2409e+102 and 3.7412e+103. Both kept time_step_convective_units 0.05 and both stopped within about 2.5 convective units. Neither run has force or Strouhal data, so neither says anything about mesh convergence.
  - Both refinements failed at the same time step that R0 survives (R0 max Courant 3.4157, mass imbalance 2.5e-10). This points to a time-step or startup stability margin, not a mesh-specific defect. Another REFINE_MESH from R0 would very likely repeat the failure, because the menu keeps the time step.
  - The R0 Courant check is INCONCLUSIVE because temporal accuracy at Courant 3.4157 is unproven. R0 has 122.32 steps per shedding period.
  - REDUCE_TIME_STEP on R0 costs about 1236 s. It gives the missing time component directly. It also shows how sensitive the R0 setup is to the time step, which is the likely cause of the R1 and R2 failures. It uses the same mesh as R0, so it should be stable.
  - Budget is ample: 2 of 6 experiments used, 0.09 of 12 relative compute.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C1_large_timestep-49d90ffccdac — Both mesh refinements (R1, R2) diverged at time step 0.05 within about 2.5 convective units, while R0 completed at Courant 3.4157. Time-step sensitivity is unmeasured and the Courant check is INCONCLUSIVE. Halving the time step on R0's identical mesh is cheap (about 1236 s) and should be stable. It measures the temporal error component and tests the Courant-margin explanation for the failed refinements.
  - Outcome: executed -> C1_large_timestep.dt0.025-610f857bd6ea (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable.
  - R3 (REDUCE_TIME_STEP, dt 0.025, same mesh as R0) completed with max Courant 1.4804. The time component now passes for both quantities. Drag time uncertainty is 0.0007653 and the R0-to-R3 change is 0.019%. Strouhal time uncertainty is 0.002544 and the change is 0.064%. R0's Courant number of 3.4157 therefore did not materially bias the results.
  - Averaging and statistics pass for both quantities. Drag: 8.688e-05 and 1.028e-04. Strouhal: 1.261e-05 and 8.418e-05.
  - The mesh and domain components are still unmeasured for both quantities, so no combined uncertainty exists.
  - R1 (factor 2.0, 122320 cells) diverged after 44 steps. R2 (factor 1.4142, 61366 cells) diverged after 52 steps. Both kept dt 0.05, and neither has force or Strouhal data. They are not evidence about mesh convergence.
  - R3 shows that halving dt on the R0 mesh runs stably. A mesh refinement with R3 as parent should inherit dt 0.025, which lowers the Courant number. This is a plausible but unproven fix for the R1 and R2 divergence.
  - R0 is still the coarse mesh (representative size 0.45745 D, 160 cells around the cylinder, wake_last_cell_D 1.0209). Mesh error is the most likely component to exceed 0.5*tolerance.
  - R3's finest-dt result compared with a refined mesh at the same dt isolates the spatial error cleanly.
  - I chose factor 1.4142 over 2.0 to keep the Courant increase moderate after two failures. R2 failed at roughly 1.41x the cell-size ratio at dt 0.05, but dt 0.025 gives a margin. Two successive 1.4142 refinements stay within the cumulative limit of 2.0 and would allow a three-level estimate later.
  - Budget remains: 3 of 6 experiments used and 1.16 of 12 relative compute. A refinement from R3 costs about 2480 s, which is affordable.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep.dt0.025-610f857bd6ea — Mesh error is unmeasured and R0 is coarse. Both earlier refinements from R0 diverged at dt 0.05. R3 has the same mesh with dt 0.025 and completed at Courant 1.4804, so refining from R3 should carry the smaller time step and run stably. A moderate factor limits the Courant increase and leaves cumulative-refinement room for a second step.
  - Outcome: executed -> C1_large_timestep.m1.41-ad97e5a246ce (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. Mesh and domain components are still INCONCLUSIVE for both quantities, so there is no combined uncertainty.
  - R0 averaging, statistics and time components pass. Drag: 8.688e-05, 1.028e-04 and 7.653e-04. Strouhal: 1.261e-05, 8.418e-05 and 2.544e-03. R3 (dt 0.025) differs from R0 by 0.019% in drag and 0.064% in Strouhal.
  - R4 (REFINE_MESH from R3, 61366 cells, dt 0.025) completed with max Courant 2.1087 and mass imbalance 8.3333e-11. That supports the idea that R1 and R2 diverged at dt 0.05.
  - R3 to R4 shows a real mesh sensitivity. Cd goes 1.3235 -> 1.3292, about 0.43%. St goes 0.16361 -> 0.16467, about 0.65%. Both are below the 3% tolerance. Neither is negligible against the 1.5% per-component budget once a safety factor of 3 is applied. The Strouhal number is the more sensitive of the two.
  - The verifier still reports 'no REFINE_MESH experiment has been run' for R0. It apparently does not credit the R3->R4 pair to the root, so the mesh component is formally unmeasured for R0. R4 is the only mesh-refined evidence.
  - The domain component is entirely unmeasured. R0 has 1.25% blockage, symmetryPlane lateral boundaries, 30 D upstream, 50 D downstream and 40 D half-height. No EXPAND_DOMAIN run exists, and absence of evidence is not a pass.
  - Budget: 4 of 6 experiments used, 3.3 of 12 relative compute. EXPAND_DOMAIN on R0 costs about 820 s. It is the cheapest experiment and gives a component that nothing else supplies. With two experiments left, running it first leaves one for a mesh follow-up and avoids spending 4944 s on mesh if the domain effect already breaks the tolerance.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C1_large_timestep-49d90ffccdac — The domain component is wholly unmeasured for both quantities. It is the cheapest remaining experiment (about 820 s from R0) and the child mesh stays within the cell limit. R0 is the root and has the same near-field mesh and dt, so the change is attributable to the boundaries alone. Running it before a costly mesh follow-up keeps one experiment in reserve.
  - Outcome: executed -> C1_large_timestep.D2x-f2b47ea2de80 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 0.43%, 0.65%, 0.43%, 0.65%

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not available. Mesh and domain are still INCONCLUSIVE for both quantities, so there is no combined uncertainty.
  - Averaging, statistics and time pass for R0. Drag: 8.688e-05, 1.028e-04 and 7.653e-04. Strouhal: 1.261e-05, 8.418e-05 and 2.544e-03. R3 (dt 0.025) shifts Cd from 1.3237 to 1.3235 and St from 0.16351 to 0.16361.
  - Domain (R5, 2x boundaries): Cd goes 1.3237 -> 1.3149 (0.67%) and St goes 0.16351 -> 0.16279 (0.44%). The verifier's estimate is 4.04% for Cd and 2.65% for St. Both exceed 1.5% only because it assumed order p=1 with Fs=3 from a single pair. The measured changes are below the 3% tolerance.
  - R5 reports checkMesh_ok false and its far-field cells are coarser (representative size 0.79405 D versus 0.45745 D). Its Cd drift is -0.0015459 relative, with ci95 0.00064741. The domain shift is therefore not cleanly attributable to the boundaries, and R5 is not a safe parent.
  - Mesh: R1 and R2 (children of R0 at dt 0.05) diverged, with Courant numbers of 9.2409e+102 and 3.7412e+103. R4 (refined from R3, dt 0.025, 61366 cells) completed. Over R3 -> R4, Cd goes 1.3235 -> 1.3292 (about 0.43%) and St goes 0.16361 -> 0.16467 (about 0.65%). The verifier gives R0 no mesh component because no valid REFINE_MESH child of R0 exists.
  - Budget left: 1 of 6 experiments, and 4.01 of 12 relative compute (R0 cost 1158.6 s). One run cannot close both the mesh and domain gaps. A mesh refinement of R0 is likely to repeat the R1 and R2 divergence at dt 0.05. A domain expansion of R0 is a stable, cheap run that can turn the two-level assumed-order estimate into a three-level estimate with measured order.
  - ACCEPT is probably out of reach whatever I choose, because the mesh component will stay unmeasured. This is the most informative remaining run, and the result may well be INCONCLUSIVE.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on C1_large_timestep-49d90ffccdac — Only one experiment remains. A REFINE_MESH child of R0 is likely to diverge at dt 0.05, as R1 and R2 did. The domain component has a two-level estimate based on an assumed order, and R5 has a failed checkMesh and a coarser far field. A 3.0x expansion of R0 is stable (R5 completed), costs about 1 to 1.5x R0's wall time, and fits the budget. It gives a three-level sequence (1x, 2x, 3x) to measure the domain convergence order.
  - Outcome: executed -> C1_large_timestep.D3x-f035e789cb02 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 0.43%, 0.65%, 0.43%, 0.65%

Run C1_large_timestep.m2-6e4f672cac17: REFINE_MESH from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, mesh.refinement: 1→2, time.end_time: 150→80).

Run C1_large_timestep.m1.41-c9c1535204d3: REFINE_MESH from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.end_time: 150→80).

Run C1_large_timestep.dt0.025-610f857bd6ea: REDUCE_TIME_STEP from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, time.delta_t: 0.05→0.025, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3237 → 1.3235 (-0.02%).
  - Observation: strouhal_number 0.16351 → 0.16361 (+0.06%).

Run C1_large_timestep.m1.41-ad97e5a246ce: REFINE_MESH from C1_large_timestep.dt0.025-610f857bd6ea (mesh.refinement: 1→1.414).
  - Observation: mean_drag_coefficient 1.3235 → 1.3292 (+0.44%).
  - Observation: strouhal_number 0.16361 → 0.16467 (+0.65%).

Run C1_large_timestep.D2x-f2b47ea2de80: EXPAND_DOMAIN from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3237 → 1.3149 (-0.67%).
  - Observation: strouhal_number 0.16351 → 0.16279 (-0.44%).

Run C1_large_timestep.D3x-f035e789cb02: EXPAND_DOMAIN from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, domain.downstream: 50→150, domain.half_height: 40→120, domain.upstream: 30→90, mesh.n_downstream: 111→166, mesh.n_lateral: 45→61, mesh.n_upstream: 35→48, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3237 → 1.313 (-0.81%).
  - Observation: strouhal_number 0.16351 → 0.16266 (-0.52%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C1_large_timestep-49d90ffccdac` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1159 s; record: results/runs/C1_large_timestep-49d90ffccdac/run.json
- `C1_large_timestep.m2-6e4f672cac17` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T09:09:24+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m2-6e4f672cac17/run.json
- `C1_large_timestep.m1.41-c9c1535204d3` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T03:41:02+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.41-c9c1535204d3/run.json
- `C1_large_timestep.dt0.025-610f857bd6ea` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T16:55:27+00:00 wall=906.3 s; record: results/runs/C1_large_timestep.dt0.025-610f857bd6ea/run.json
- `C1_large_timestep.m1.41-ad97e5a246ce` status=completed parent=C1_large_timestep.dt0.025-610f857bd6ea created=2026-10-20T04:12:40+00:00 wall=2916 s; record: results/runs/C1_large_timestep.m1.41-ad97e5a246ce/run.json
- `C1_large_timestep.D2x-f2b47ea2de80` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T04:12:05+00:00 wall=885.8 s; record: results/runs/C1_large_timestep.D2x-f2b47ea2de80/run.json
- `C1_large_timestep.D3x-f035e789cb02` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T07:52:12+00:00 wall=1272 s; record: results/runs/C1_large_timestep.D3x-f035e789cb02/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 443837112.0, "relative_to_root": 4.837989012426423, "experiment_wall_seconds": 5979.559148694007, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.57686986, "loop_wall_seconds": 162.0397138729968}
