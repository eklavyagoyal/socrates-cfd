# Verification report: C1_large_timestep (C-llm-r2)

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
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and there is no basis for REJECT.
  - R0 averaging and statistics components pass with tiny uncertainties. Drag: 8.688e-05 and 0.0001028. Strouhal: 1.261e-05 and 8.418e-05. The run has 12 stationary cycles. The tolerance is 0.03 for each quantity.
  - Mesh, time and domain components are all unmeasured for both quantities: no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists, so no combined uncertainty can be formed.
  - R0 mesh is coarse: 30580 cells, representative cell size 0.45745 D, and wake_last_cell_D 1.0209. Coarse wake cells can bias both the Strouhal number and the mean drag, and the verifier has no mesh evidence yet. Mesh is therefore my leading suspect for an error larger than 3%.
  - Time and domain are secondary suspects. Max Courant is 3.4157 with 122.32 steps per shedding period and backward time scheme. Blockage is 0.0125, with lateral symmetryPlane boundaries at 40 D and the outlet at 50 D.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute used. REFINE_MESH from R0 costs about 1240 s against a 1158.6 s root. The default factor keeps that cost estimate valid, and the experiment is expected to resolve the mesh component for both quantities.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep-49d90ffccdac — Mesh error is the largest unmeasured component and the most likely to exceed the 3% tolerance, given the coarse near-wake resolution. It is needed for both quantities, and the budget affords it.
  - Outcome: executed -> C1_large_timestep.m1.41-c9c1535204d3 (failed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. There is no measured FAIL, so REJECT is not allowed either.
  - R0 averaging and statistics pass for both quantities. Drag: 8.688e-05 and 0.0001028. Strouhal: 1.261e-05 and 8.418e-05. R0 has 12 stationary cycles. Mesh, time and domain are still unmeasured for both quantities.
  - R1 (REFINE_MESH from R0) did not complete. It stopped after 52 steps at record length 2.5 convective units. Its max_courant is 3.7412e+103 and its mass_imbalance_max is 2.3546e+67. R1 gives no mesh evidence. It must not be read as a mesh-sensitivity result.
  - R1 kept time_step_convective_units at 0.05, the same as R0, while its cells around the cylinder rose from 160 to 228 and its wall_first_cell_D fell from 0.005 to 0.0035832. R0 already ran at max Courant 3.4157 with 3 outer correctors, which the verifier calls INCONCLUSIVE for temporal accuracy. The most plausible cause of the R1 blow-up is that the finer mesh at the same dt exceeded the stability limit of the PIMPLE setup. This is a hypothesis, not a measurement.
  - Repeating REFINE_MESH from R0 with the same dt would probably diverge again. A smaller dt is the common fix for both the R1 failure and the unmeasured time component. REDUCE_TIME_STEP on R0 costs about 1236 s. It fills the missing time component for both quantities and tests whether the R0 results depend on dt at Courant 3.4.
  - Budget is fine: 1 of 6 experiments used and 0.03 of 12 relative compute used. R0 allows RUN_LONGER, but it is not the priority because the statistics are already tight.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on C1_large_timestep-49d90ffccdac — R1 diverged at the same dt, so a mesh refinement repeated from R0 is likely to fail again. Time-step refinement is cheap at about 1236 s. It supplies the missing time component and shows whether a smaller dt gives a stable setup for the later mesh refinement.
  - Outcome: executed -> C1_large_timestep.dt0.025-610f857bd6ea (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.7

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both not allowed.
  - R0 averaging, statistics and time components pass for both quantities. Drag: 8.688e-05, 0.0001028 and 0.0007653. Strouhal: 1.261e-05, 8.418e-05 and 0.002544. Each is far below the 1.5% component budget. R2 (REDUCE_TIME_STEP, dt 0.025) completed with 7 stationary cycles. Its drag is 1.3235 against 1.3237 for R0, and its Strouhal number is 0.16361 against 0.16351.
  - Mesh and domain components are still unmeasured for both quantities, so no combined uncertainty exists. The tolerance is 0.03.
  - R1 (REFINE_MESH from R0) diverged after 52 steps, with max_courant 3.7412e+103 and mass_imbalance_max 2.3546e+67. It gives no mesh evidence. It ran at dt 0.05, the same as R0, on a finer mesh with 228 cells around the cylinder, and R0 already ran at max Courant 3.4157.
  - R2 has the halved dt of 0.025 and max Courant 1.4804, which leaves stability margin. Refining the mesh from R2 should inherit this dt, so the finer mesh should stay stable. The refined run is also compared against an R2 baseline that is already time-converged. This is a hypothesis, not a measurement.
  - R0 mesh is coarse: 0.45745 D cell size and wake_last_cell_D of 1.0209. Mesh is the component most likely to move drag or St by more than the budget. Domain (blockage 0.0125, 40 D lateral, 50 D outlet) is the second unmeasured component and is cheaper. It can be run next.
  - Budget allows it: 2 of 6 experiments used and 1.1 of 12 relative compute used. REFINE_MESH from R2 costs about 2480 s.
  - Requested: REFINE_MESH {'factor': 1.4142} on C1_large_timestep.dt0.025-610f857bd6ea — Mesh is the largest unmeasured component and the one most likely to exceed the tolerance. The R0-parented refinement R1 diverged at dt 0.05. R2 carries the halved dt of 0.025 with max Courant 1.4804, so a refined mesh built from R2 should be stable. Its baseline is time-converged and the cost of about 2480 s is affordable.
  - Outcome: executed -> C1_large_timestep.m1.41-ad97e5a246ce (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both barred.
  - R0 averaging, statistics and time components pass for both quantities. Drag: 8.688e-05, 0.0001028, 0.0007653. Strouhal: 1.261e-05, 8.418e-05, 0.002544. The tolerance is 0.03.
  - R3 (REFINE_MESH from R2, dt 0.025) completed with 6 stationary cycles. Its drag is 1.3292 against 1.3235 for R2. Its Strouhal number is 0.16467 against 0.16362 for R2. Both changes are visibly well below the 0.03 tolerance. R3 is the first valid refined-mesh result.
  - The verifier still lists mesh as INCONCLUSIVE for R0 and says no REFINE_MESH run exists. It cites only R0 for the mesh check and does not use R3. I cannot overrule this. R3's evidence is only indicative until the verifier counts it. R1 diverged and gives no mesh evidence.
  - Domain is unmeasured for both quantities: no EXPAND_DOMAIN run exists. The recorded setup has blockage 0.0125, upstream 30 D, downstream 50 D and half-height 40 D with symmetryPlane sides. The question says to treat the stream as unbounded. A domain error cannot be ruled out without a measurement.
  - EXPAND_DOMAIN from R0 costs about 820 s, the cheapest experiment. The verifier compares against the root, so R0 is the right parent. Budget: 3 of 6 experiments and 3.24 of 12 relative compute used. This leaves room for a later mesh follow-up if the verifier still reports the mesh component as missing.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on C1_large_timestep-49d90ffccdac — The domain component is unmeasured for both quantities and is the only component with no evidence at all. The cost is about 820 s, the lowest on the menu. The question requires an unbounded stream, and the setup has symmetry sides at 40 D and a finite outlet at 50 D.
  - Outcome: executed -> C1_large_timestep.D2x-f2b47ea2de80 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred.
  - R0 averaging, statistics and time components pass for both quantities. Drag: 8.688e-05, 0.0001028 and 0.0007653. St: 1.261e-05, 8.418e-05 and 0.002544. R0 has 12 stationary cycles, and the tolerance is 0.03.
  - The domain component is the dominant open item. R4 (EXPAND_DOMAIN from R0, factor 2) gives drag 1.3149 against 1.3237 for R0 (change 0.67%) and St 0.16279 against 0.16351 (change 0.44%). Both changes are below the 0.03 tolerance. The two-level Richardson estimate at assumed p=1 is still 0.04044 for drag and 0.02653 for St. Both exceed the 1.5% component budget, and the verifier says more refinement would be needed.
  - R4 is a weaker run than R0. checkMesh_ok is false, with no recorded reason. Its wake_last_cell_D is 1.9729 against 1.0209 for R0. It has only 7 stationary cycles. Its drag CI95 is 0.00064741 and its drag drift is -0.0015459, against 3.1562e-05 and 0.00010279 for R0. The domain estimate rests on this one run, so the p=1 extrapolation could be inflated or biased. A second, independent expansion level would show whether the domain trend converges.
  - The mesh component is still INCONCLUSIVE in the verifier, which says no REFINE_MESH run exists. R1 diverged after 52 steps and gives no evidence. R3 (refined from R2) shows drag 1.3292 against 1.3235 for R2 and St 0.16467 against 0.16362. The verifier does not use R3 for root R0, so I cannot treat it as an accepted mesh component.
  - Budget: 4 of 6 experiments and 3.95 of 12 relative compute are used. EXPAND_DOMAIN from R0 at factor 3.0 costs about 820 s or a little more. This leaves one experiment for a mesh follow-up.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on C1_large_timestep-49d90ffccdac — Domain is the only component whose estimate (drag 0.04044, St 0.02653) exceeds the tolerance, and it rests on a single run (R4) with checkMesh_ok false and a poorer statistical window. A second expansion level gives a three-point sequence and an observed convergence order. Parenting on R0 keeps the root comparison the verifier uses. It avoids inheriting R4's failed mesh and is cheaper than expanding from R4.
  - Outcome: executed -> C1_large_timestep.D3x-f035e789cb02 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.43%, 0.64%

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT and REJECT are both barred.
  - R0 averaging, statistics and time components pass. Drag: 8.688e-05, 0.0001028, 0.0007653. St: 1.261e-05, 8.418e-05, 0.002544. R0 has 12 stationary cycles.
  - Domain drag now passes: 0.01202 (R0, R4, R5, observed p=1.75), under the 1.5% component budget. Domain St is 0.01577, just over the 1.5% budget. The verifier notes the demonstrated change is 0.53%, below the 0.03 tolerance, and that the differences are within 2x statistical noise. R4 and R5 both have checkMesh_ok false, so I cannot judge their reliability.
  - Mesh is still INCONCLUSIVE for both quantities. The verifier cites only R0 and says no REFINE_MESH experiment has been run. R1 (from R0) diverged after 52 steps at dt 0.05, with max_courant 3.7412e+103. R3 (from R2, dt 0.025) completed, but the verifier does not count it for root R0. R3 gives drag 1.3292 against 1.3235 for R2 and St 0.16467 against 0.16362 for R2. That is indicative only.
  - Mesh is the only component missing for both quantities, so it is the largest open gap in the error budget. A completed REFINE_MESH child of R0 is the only way to close it for the root.
  - Budget: 5 of 6 experiments used, 4.78 of 12 relative compute used. One experiment is left. REFINE_MESH from R0 costs about 1240 s, which the compute budget covers.
  - One experiment cannot close both the mesh gap and the St domain gap, so ACCEPT is unlikely this round. The mesh run is still the most useful choice because it could reveal a change above tolerance, which would give a FAIL.
  - R1's failure shows a risk. The finer mesh at dt 0.05 diverged, and R0 already ran at max Courant 3.4157. R3 had max Courant 2.1087 at dt 0.025. I chose the minimum factor of 1.3 to limit the growth in Courant number. The menu says dt is reduced if the predicted Courant number exceeds the limit. The recorded R1 dt was not reduced, so divergence is still possible.
  - Requested: REFINE_MESH {'factor': 1.3} on C1_large_timestep-49d90ffccdac — Mesh is the only component missing for both quantities, and the verifier needs a completed REFINE_MESH child of root R0. The minimum factor of 1.3 limits the Courant-number growth that probably caused R1 to diverge. The cost of about 1240 s is affordable.
  - Outcome: executed -> C1_large_timestep.m1.3-88f06517ee4c (failed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.43%, 0.64%

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

Run C1_large_timestep.m1.3-88f06517ee4c: REFINE_MESH from C1_large_timestep-49d90ffccdac (averaging.start_time: 75→40, mesh.refinement: 1→1.3, time.end_time: 150→80).

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
- `C1_large_timestep.m1.41-c9c1535204d3` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T03:41:02+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.41-c9c1535204d3/run.json
- `C1_large_timestep.dt0.025-610f857bd6ea` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T16:55:27+00:00 wall=906.3 s; record: results/runs/C1_large_timestep.dt0.025-610f857bd6ea/run.json
- `C1_large_timestep.m1.41-ad97e5a246ce` status=completed parent=C1_large_timestep.dt0.025-610f857bd6ea created=2026-10-20T04:12:40+00:00 wall=2916 s; record: results/runs/C1_large_timestep.m1.41-ad97e5a246ce/run.json
- `C1_large_timestep.D2x-f2b47ea2de80` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T04:12:05+00:00 wall=885.8 s; record: results/runs/C1_large_timestep.D2x-f2b47ea2de80/run.json
- `C1_large_timestep.D3x-f035e789cb02` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T07:52:12+00:00 wall=1272 s; record: results/runs/C1_large_timestep.D3x-f035e789cb02/run.json
- `C1_large_timestep.m1.3-88f06517ee4c` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T12:53:39+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.3-88f06517ee4c/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 441594824.0, "relative_to_root": 4.813547242206235, "experiment_wall_seconds": 5979.559148694007, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.538120025, "loop_wall_seconds": 4082.670491103998}
