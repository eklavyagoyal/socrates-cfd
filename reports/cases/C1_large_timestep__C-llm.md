# Verification report: C1_large_timestep (C-llm)

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
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.55% > 1.50% but the demonstrated change 0.88% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.14, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.02% <= 1.50% (root-to-finest change 0.580%) [three-level Celik procedure, observed order p=1.13, Fs=1.25]

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
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0155
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D1.5x-1dc17ff14755

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
└── Artificial boundaries (domain sensitivity): PASS U=0.0102
    └── C1_large_timestep-49d90ffccdac
    └── C1_large_timestep.D2x-f2b47ea2de80
    └── C1_large_timestep.D1.5x-1dc17ff14755

```

## EXPERIMENT HISTORY

Run C1_large_timestep-49d90ffccdac: submitted simulation (30580 cells, dt=0.05 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. Mesh, time and domain uncertainty components are all unmeasured for both mean_drag_coefficient and strouhal_number.
  - Averaging and statistics are measured and negligible. For drag: averaging 8.688e-05 and statistics 0.0001028. For Strouhal: averaging 1.261e-05 and statistics 8.418e-05. Both are far below the 0.03 tolerance. Stationary window: 12 cycles, drag CI95 3.1562e-05, drift 0.00010279. More run length would add little.
  - R0 mesh is coarse: 30580 cells, representative cell size 0.45745 D, wake_last_cell_D 1.0209 and 111 wake cells streamwise. checkMesh only shows the mesh is valid, not that it resolves the flow. Spatial error is the most likely component to move drag or St by more than 3%, and the verifier has no mesh data.
  - Courant is 3.4157 with dt = 0.05 D/U, 3 outer correctors and backward time scheme. The courant_number check is INCONCLUSIVE, so temporal accuracy is unproven. This is a secondary risk.
  - Domain extents are 30 D upstream, 50 D downstream and 40 D half-height, with blockage 0.0125 and symmetryPlane lateral boundaries. These are fairly generous, so domain error is less likely to dominate than mesh error.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute used. R0 REFINE_MESH costs about 1240 s. I choose it first and keep the time-step and domain experiments for later.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep-49d90ffccdac — Mesh error is unmeasured and is the most likely component to change the answer by more than 3%. R0 is coarse (30580 cells, representative size 0.45745 D, wake last cell 1.0209 D). Averaging and statistics are already negligible. The default factor is cheap (about 1240 s) and leaves budget for time-step and domain checks.
  - Outcome: executed -> C1_large_timestep.m1.41-c9c1535204d3 (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both unavailable. Mesh, time and domain components are still unmeasured for mean_drag_coefficient and strouhal_number.
  - R0 averaging and statistics are negligible. Drag: averaging 8.688e-05, statistics 0.0001028. Strouhal: averaging 1.261e-05, statistics 8.418e-05. R0 has 12 stationary cycles and drag CI95 3.1562e-05. RUN_LONGER would add little.
  - R1 (REFINE_MESH from R0) did not complete. It stopped after 52 time steps with max_courant 3.7412e+103 and mass_imbalance_max 2.3546e+67, so it is a numerical blow-up. It gives no mesh-sensitivity information, and the mesh check stays INCONCLUSIVE.
  - R1 kept time_step_convective_units 0.05, the same as R0. Its cells are smaller: representative size 0.32292 D against 0.45745 D, and wall_first_cell_D 0.0035832 against 0.005. Its Courant number is therefore higher than R0's 3.4157, which was already flagged INCONCLUSIVE by the courant_number check. A time-step-driven instability is the leading explanation. This is a hypothesis, not a measurement, because R1 has no usable Courant history.
  - R1 cannot be a parent for further experiments. It did not complete, and RUN_LONGER is explicitly disallowed on it. Repeating REFINE_MESH at the same dt would probably fail again.
  - The time error at R0 is needed whatever happens: the courant_number check is INCONCLUSIVE and the time component is unmeasured. REDUCE_TIME_STEP from R0 costs about 1236 s. It tests the Co hypothesis, and it gives the temporal sensitivity of Cd and St. A smaller dt can also guide a stable mesh-refinement retry afterwards.
  - Budget is ample: 1 of 6 experiments used and 0.03 of 12 relative compute used.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C1_large_timestep-49d90ffccdac — R1 blew up at an unchanged dt of 0.05 D/U on a finer mesh, which points to Courant-driven instability. R0's temporal error is unmeasured, and its Co of 3.4157 is flagged INCONCLUSIVE. R0 is the only completed run to use as a parent. Halving dt is cheap (about 1236 s). It measures the time component and shows whether a smaller dt stabilises the flow. That informs a robust mesh-refinement retry.
  - Outcome: executed -> C1_large_timestep.dt0.025-610f857bd6ea (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. The mesh and domain components are unmeasured for both mean_drag_coefficient and strouhal_number.
  - Averaging, statistics and time are measured and pass. Drag: averaging 8.688e-05, statistics 0.0001028, time 0.0007653. Strouhal: averaging 1.261e-05, statistics 8.418e-05, time 0.002544. All are far below the 0.03 tolerance. RUN_LONGER would add little.
  - R2 (REDUCE_TIME_STEP from R0, dt 0.025) completed with max_courant 1.4804. Its mean Cd is 1.3235 against 1.3237 for R0. Its St is 0.16361 against 0.16351 for R0. Time-step sensitivity is therefore negligible at this tolerance.
  - R1 (REFINE_MESH from R0 at dt 0.05) diverged after 52 steps, with max_courant 3.7412e+103. It gives no mesh information. R0's Courant number was 3.4157 at dt 0.05, and R2 is stable at dt 0.025, so a Courant-driven instability on the finer mesh is the leading explanation. This is a hypothesis, not a measurement.
  - Repeating REFINE_MESH from R0 would keep dt 0.05 and would probably blow up again. R2 is a completed run with the smaller dt of 0.025, so refining from R2 gives the best chance of a stable run. A time step carried over from R2 is the most robust choice.
  - The mesh is still the most likely remaining error source. R0 has 30580 cells, representative size 0.45745 D and wake_last_cell_D 1.0209. The domain extents are generous: 30 D upstream, 50 D downstream, 40 D half-height, blockage 0.0125. The domain check stays pending after the mesh test.
  - Budget: 2 of 6 experiments used, and 1.1 of 12 relative compute used. REFINE_MESH from R2 costs about 2480 s, which is affordable.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep.dt0.025-610f857bd6ea — The mesh error is unmeasured and is the most likely component to move Cd or St. R1 diverged at the unchanged dt of 0.05 from R0. R2 is a completed run with dt 0.025 and max_courant 1.4804, and its time sensitivity is negligible. Refining from R2 carries the smaller dt, so the refined run is more likely to be stable. It also keeps the mesh comparison free of time-step effects.
  - Outcome: executed -> C1_large_timestep.m1.41-ad97e5a246ce (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both unavailable. The mesh and domain components are still INCONCLUSIVE for mean_drag_coefficient and strouhal_number, and combined_uncertainty is null.
  - Averaging, statistics and time pass. Drag: averaging 8.688e-05, statistics 0.0001028, time 0.0007653. Strouhal: averaging 1.261e-05, statistics 8.418e-05, time 0.002544. All are far below the 0.03 tolerance, so RUN_LONGER would add little. R0 has 12 stationary cycles.
  - R3 (REFINE_MESH from R2) completed with 61366 cells and max_courant 2.1087. Mean Cd is 1.3292 against 1.3235 for R2. St is 0.16467 against 0.16362 for R2. Both changes are small next to the 0.03 tolerance, but they are not zero. There are only two mesh levels in the R2 to R3 family.
  - The verifier still reports the mesh component as missing for root R0. Its mesh check lists only R0 and says no REFINE_MESH has been run. It does not appear to use R3, which descends from R2, and R1 diverged. I cannot tell from the package whether the verifier will credit R3. I treat the mesh evidence as indicative, not as a closed component.
  - The domain component has no measurement at all. R0 uses 30 D upstream, 50 D downstream and 40 D half-height, with blockage_ratio 0.0125, symmetryPlane lateral boundaries, inlet pressure zeroGradient and outlet pressure fixedValue. The question requires an unbounded stream. A domain error is independent of the mesh and time results, and nothing recorded bounds it.
  - EXPAND_DOMAIN from R0 is the cheapest experiment, at about 820 s. It leaves the near-field mesh and the time step unchanged. It fills the only component with no measurement and compares directly against the root. Budget: 3 of 6 experiments used and 3.24 of 12 relative compute used, so this is affordable.
  - A third mesh level (REFINE_MESH from R3, about 4944 s) is the likely follow-up if the verifier still reports the mesh component as missing, or if the mesh change turns out to be large against the 0.03 tolerance. It is more expensive, so the domain test goes first.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C1_large_timestep-49d90ffccdac — The domain component is completely unmeasured for both quantities and the problem requires an unbounded stream. The experiment is cheap (about 820 s), keeps the near-field mesh and time step unchanged, and compares directly against the root R0. Mesh and time already have measurements, and a third mesh level costs about 4944 s.
  - Outcome: executed -> C1_large_timestep.D2x-f2b47ea2de80 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are not allowed. combined_uncertainty is null for both quantities. Mesh and domain components are still missing.
  - Averaging, statistics and time pass. Drag: averaging 8.688e-05, statistics 0.0001028, time 0.0007653. Strouhal: averaging 1.261e-05, statistics 8.418e-05, time 0.002544. R0 has 12 stationary cycles, so RUN_LONGER would add little.
  - Mesh check lists only R0 and says 'no REFINE_MESH experiment has been run'. R1 (REFINE_MESH from R0) blew up after 52 steps with max_courant 3.7412e+103. R3 completed (Cd 1.3292 vs 1.3235 in R2, St 0.16467 vs 0.16362), but it descends from R2 at dt 0.025 and the verifier does not credit it. The time and domain checks used only direct children of R0 (R2, R4), so the mesh check probably needs a completed direct child of R0.
  - R3 is indicative only. The Cd change from R2 to R3 is about 0.43% and the St change is about 0.64%. Both are small against the 0.03 tolerance. With the verifier's Fs=3 safety factor, a two-level estimate could still land near the 0.015 per-component budget. This is not a verifier result.
  - Domain check is INCONCLUSIVE. Domain uncertainty is 0.04044 for Cd and 0.02653 for St, both above 0.5*tolerance. The demonstrated R0 to R4 change is only 0.67% for Cd and 0.44% for St. The large estimate comes from the assumed order p=1 with Fs=3, so a third domain level would be needed to tighten it. R4 also has checkMesh_ok false and wake_last_cell_D 1.9729, so R4 is a weaker comparison.
  - R1 kept dt 0.05 on the finer mesh. R3 on the same mesh was stable at dt 0.025 with max_courant 2.1087. R0 was stable at max_courant 3.4157. A Courant-driven blow-up is plausible but unmeasured. The smallest allowed mesh factor (1.3) raises Courant least, so it gives the best chance of a completed direct child of R0.
  - Budget: 4 of 6 experiments used and 3.95 of 12 relative compute used. Two experiments remain. REFINE_MESH from R0 costs about 1240 s. A later EXPAND_DOMAIN from R4 costs about 1060 s and would give a third domain level.
  - Requested: REFINE_MESH {'factor': 1.3} on C1_large_timestep-49d90ffccdac — The mesh component has no verifier-credited measurement. R1 diverged and R3 descends from R2, so neither is credited. A completed direct child of R0 is needed. Factor 1.3 is the menu minimum and raises the Courant number least compared with the failed R1, so it is the most likely to run stably. It costs about 1240 s and leaves one experiment for the domain check.
  - Outcome: executed -> C1_large_timestep.m1.3-88f06517ee4c (failed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.43%, 0.64%

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. combined_uncertainty is null for mean_drag_coefficient and strouhal_number.
  - Averaging, statistics and time pass. Drag: averaging 8.688e-05, statistics 0.0001028, time 0.0007653. Strouhal: averaging 1.261e-05, statistics 8.418e-05, time 0.002544. R0 has 12 stationary cycles, so RUN_LONGER would add nothing useful.
  - Mesh is still INCONCLUSIVE. R1 (factor 1.4142, dt 0.05) and R5 (factor 1.3, dt 0.05) both diverged, with max_courant 3.7412e+103 and 1.5949e+103. The mesh check lists only R0 and reports that no REFINE_MESH experiment has been run. R5 used the menu minimum factor and still failed, so another REFINE_MESH from R0 is very unlikely to complete. Its cause is unmeasured, and no Courant history before blow-up is recorded.
  - R3 (REFINE_MESH from R2, dt 0.025) completed with Cd 1.3292 against 1.3235 for R2, and St 0.16467 against 0.16362. The verifier does not credit it for root R0. Only one experiment remains, so a third mesh level from R3 (about 4944 s) cannot be relied on to give the root a credited mesh component.
  - Domain is INCONCLUSIVE. The estimated uncertainty is 0.04044 for Cd and 0.02653 for St, both above 0.5*tolerance. The demonstrated R0 to R4 changes are 0.67% for Cd and 0.44% for St, both below tau. The large estimates come from the assumed order p=1 with Fs=3 on a two-level comparison. A third domain level is what lets the verifier estimate the observed order.
  - R4 has checkMesh_ok false, wake_last_cell_D 1.9729 and drag drift -0.0015459. Its stationary window has 7 cycles and drag CI95 0.00064741. This weakens the domain comparison. Only one experiment remains and the mesh component is probably unreachable, so I expect the final verdict to stay INCONCLUSIVE even if the domain closes.
  - EXPAND_DOMAIN from R4 with factor 1.5 is the cheapest experiment (about 1060 s), and it can close the domain component. The budget allows it: 5 of 6 experiments used and 3.98 of 12 relative compute used.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on C1_large_timestep.D2x-f2b47ea2de80 — Domain is the one component that a single experiment can plausibly close. It adds a third domain level (R0, R4, new), so the verifier can use an observed order instead of the assumed p=1 with Fs=3. It is cheap (about 1060 s). Mesh cannot be closed: R1 and R5 both diverged at dt 0.05, including at the minimum factor 1.3, and a refinement from R3 is expensive and not credited for R0.
  - Outcome: executed -> C1_large_timestep.D1.5x-1dc17ff14755 (completed)

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

Run C1_large_timestep.m1.3-88f06517ee4c: REFINE_MESH from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, mesh.refinement: 1→1.3, time.end_time: 150→80).

Run C1_large_timestep.D1.5x-1dc17ff14755: EXPAND_DOMAIN from C1_large_timestep.D2x-f2b47ea2de80 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3149 → 1.3121 (-0.21%).
  - Observation: strouhal_number 0.16279 → 0.16257 (-0.14%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C1_large_timestep-49d90ffccdac` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1159 s; record: results/runs/C1_large_timestep-49d90ffccdac/run.json
- `C1_large_timestep.m1.41-c9c1535204d3` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T03:41:02+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.41-c9c1535204d3/run.json
- `C1_large_timestep.dt0.025-610f857bd6ea` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T16:55:27+00:00 wall=906.3 s; record: results/runs/C1_large_timestep.dt0.025-610f857bd6ea/run.json
- `C1_large_timestep.m1.41-ad97e5a246ce` status=completed parent=C1_large_timestep.dt0.025-610f857bd6ea created=2026-10-20T04:12:40+00:00 wall=2916 s; record: results/runs/C1_large_timestep.m1.41-ad97e5a246ce/run.json
- `C1_large_timestep.D2x-f2b47ea2de80` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T04:12:05+00:00 wall=885.8 s; record: results/runs/C1_large_timestep.D2x-f2b47ea2de80/run.json
- `C1_large_timestep.m1.3-88f06517ee4c` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T12:53:39+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.3-88f06517ee4c/run.json
- `C1_large_timestep.D1.5x-1dc17ff14755` status=completed parent=C1_large_timestep.D2x-f2b47ea2de80 created=2026-10-20T05:16:59+00:00 wall=1095 s; record: results/runs/C1_large_timestep.D1.5x-1dc17ff14755/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 441335624.0, "relative_to_root": 4.8107218661434485, "experiment_wall_seconds": 5802.993844127006, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.56105319, "loop_wall_seconds": 8514.192759571999}
