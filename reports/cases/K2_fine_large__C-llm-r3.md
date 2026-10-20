# Verification report: K2_fine_large (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3278
- strouhal_number: 0.16382

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.65 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.91e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.01e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.43% <= 1.50% (root-to-finest change 0.088%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.19% > 1.50% but the demonstrated change 0.44% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.3e-05)]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.79% <= 1.50% (root-to-finest change 0.198%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.068%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.87% > 1.50% but the demonstrated change 0.62% <= tau; more refinement would be needed [three-level, observed order 7.66 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.87% <= 1.50% (root-to-finest change 0.289%) [differences within 2x statistical noise (1.9e-03); range-based U with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=7.06e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.91e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): PASS U=0.00433
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m2-e923e7640822
├── Temporal discretisation (time-step sensitivity): PASS U=0.00791
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0187
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D1.5x-c2938461e5bc
    └── K2_fine_large.long180-dda8a9c17278
    └── K2_fine_large.D3x-7a1272bafc30

CLAIM: strouhal_number of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=4.99e-06
│   └── K2_fine_large-2d999cd1eb7c
├── Temporal statistics (stationarity, cycles): PASS U=2.01e-05
│   └── K2_fine_large-2d999cd1eb7c
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0219
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m2-e923e7640822
├── Temporal discretisation (time-step sensitivity): PASS U=0.0027
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.00867
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D1.5x-c2938461e5bc
    └── K2_fine_large.long180-dda8a9c17278
    └── K2_fine_large.D3x-7a1272bafc30

```

## EXPERIMENT HISTORY

Run K2_fine_large-2d999cd1eb7c: submitted simulation (54244 cells, dt=0.007 D/U, half-height 60 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified because there is no FAIL.
  - R0 passed solver completion, mesh quality, mass conservation (0.0 imbalance), linear-solver convergence, Courant number (0.648) and Re consistency (100 = 100). It also passed force reference, physics regime, averaging and statistics.
  - Averaging and statistics uncertainties are tiny. For drag they are 7.057e-05 and 2.908e-05 against a tolerance of 0.03. For Strouhal number they are 4.994e-06 and 2.011e-05.
  - Mesh, time and domain components are all INCONCLUSIVE because no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists. Absence of evidence is not a pass.
  - R0 mesh: 54244 cells, representative cell size 0.47033 D, wake_last_cell_D 0.96749 and 150 streamwise wake cells. The far-field and wake spacing is coarse relative to D, and the scheme is only nominally second order. Spatial error is the most plausible source of a change larger than 3 %.
  - Time resolution looks adequate: time step 0.007, 872.03 steps per shedding period and Courant 0.648. Time error is therefore less likely to dominate, but it is still unmeasured.
  - Domain: 40 D upstream, 60 D downstream, 60 D half-height, blockage 0.0083333. The domain looks generous, so it is a lower-priority risk.
  - The stationary window start (70.578) is flagged as the MSER cap. The drag drift (-2.9076e-05) and half-difference (-1.6483e-05) are tiny, so there is no sign of a lingering transient.
  - The Strouhal frequency resolution is 0.013334 against a value of 0.16382, which is coarser than the 3 % tolerance of about 0.0049. The reported Strouhal number equals the FFT value, so this is a secondary concern to check later with RUN_LONGER.
  - Budget: 0 of 6 experiments used and 0 of 12 compute units used. REFINE_MESH from R0 is affordable, and a factor of 2.0 gives the strongest signal over noise.
  - Requested: REFINE_MESH {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Spatial discretisation is the most likely source of a change larger than 3 %: the representative cell size is 0.47 D, the last wake cell is 0.967 D, and the mesh has never been refined. A factor of 2.0 gives the clearest signal. Time step, domain and averaging are already well characterised or look benign.
  - Outcome: rejected by validator: child mesh has 216220 cells > limit 160000
  - Numeric audit: 2 number(s) not traceable to evidence: 0.0049, 0.83

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because the mesh, time and domain components are unmeasured. REJECT is not justified because there is no FAIL.
  - R0 passed the solver completion, mesh quality, mass conservation, linear solver, Courant (0.648), Re consistency, force reference, physics regime, averaging and statistics checks. Averaging and statistics uncertainties are tiny: drag 7.057e-05 and 2.908e-05, Strouhal 4.994e-06 and 2.011e-05.
  - The previous REFINE_MESH factor 2.0 was rejected: the child mesh had 216220 cells against a limit of 160000. R0 has 54244 cells. A factor of 2.0 gave about 4x the cells, so cell count appears to scale roughly with factor squared. This is my inference from those two recorded counts.
  - Under that inference, a factor of about 1.7 or less keeps the child under 160000 cells. I chose 1.6 to leave margin for rounding. It should give roughly 1.4e5 cells, which is an estimate and not a recorded value. The factor is within the menu range of 1.3 to 2.0.
  - Mesh error is still the most plausible source of a change above 3 %. R0 has representative cell size 0.47033 D, wake_last_cell_D 0.96749, 150 streamwise wake cells and a nominally second-order scheme. It has never been refined.
  - Time resolution looks adequate (872.03 steps per period, Courant 0.648) and the domain is generous (40 D upstream, 60 D downstream, 60 D half-height, blockage 0.0083333). Both are still unmeasured and are lower priority.
  - Budget: 0 of 6 experiments used and 0 of 12 compute units used. The estimated cost of REFINE_MESH from R0 is 8677 s, against 8041 s for R0, so it is affordable.
  - Requested: REFINE_MESH {'factor': 1.6} on K2_fine_large-2d999cd1eb7c — Mesh error is the most likely source of a change above 3 % and has never been tested. The earlier factor of 2.0 gave 216220 cells, above the 160000 limit. Cell count appears to scale with about the square of the factor, so 1.6 should stay under the limit. It is the largest refinement that does so with margin, which gives the clearest signal over noise.
  - Outcome: executed -> K2_fine_large.m2-e923e7640822 (completed)
  - Numeric audit: 5 number(s) not traceable to evidence: 1.7, 1.6, 1.4e5, 0.83, 1.6

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because time and domain are unmeasured for both quantities. REJECT is not justified because there is no FAIL.
  - R0 and R1 are both complete and stationary. R0 has drag 1.3277 and Strouhal 0.16382. R1 has drag 1.3289 and Strouhal 0.16455. Averaging and statistics uncertainties are tiny: drag 7.057e-05 and 2.908e-05, Strouhal 4.994e-06 and 2.011e-05.
  - Drag mesh uncertainty is now measured at 0.004327 (0.43%), with a root-to-finest change of 0.088%. The mesh component is PASS for drag.
  - Strouhal mesh uncertainty is 0.02187 (2.19%), above the 1.5% component limit. The demonstrated R0-to-R1 change is only 0.44%, and the 2.19% comes from the assumed order p=2 with Fs=3. The check is INCONCLUSIVE, not FAIL.
  - REFINE_MESH from R1 is not allowed (cumulative 2.26 > 2.0). A later REFINE_MESH from R0 with a smaller factor could give a third level and an observed order. That is a later step.
  - Domain is the most informative remaining unknown. It is unmeasured for both quantities, and the question says to treat the stream as unbounded. The run has symmetryPlane lateral boundaries at 60 D half-height, fixedValue outlet pressure and zeroGradient inlet pressure. Blockage is 0.0083333, and no run has varied the boundary distances.
  - Time is also unmeasured, but R0 shows 872.03 steps per period at max Courant 0.648 and R1 shows 1000.1 steps per period at Courant 0.72231. Time error is judged less likely to dominate, but it still needs a run.
  - EXPAND_DOMAIN from R0 costs 5621 s, the cheapest menu entry. Budget used is 1 of 6 experiments and 1.56 of 12 compute units, so it is affordable. Parent R1 is disallowed (181768 cells > 160000), so R0 is the parent. Factor 2.0 gives a clear signal and should stay within the cell limit. This is an expectation, not a recorded count.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Domain truncation and blockage error is unmeasured for both quantities, and the problem requires an unbounded stream. It is the cheapest experiment (5621 s). R1 is not allowed as parent because the child would have 181768 cells, above the 160000 limit. R0 is therefore the parent. Factor 2.0 gives a clear signal over noise, and cells are added only far from the cylinder.
  - Outcome: executed -> K2_fine_large.D2x-bc527461f36d (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - R0 passes the solver, mesh-quality, mass-conservation, linear-solver, Courant (0.648), Re, force-reference, physics-regime, averaging and statistics checks. Averaging and statistics uncertainties are tiny: drag 7.057e-05 and 2.908e-05, Strouhal 4.994e-06 and 2.011e-05.
  - Mesh (R0 to R1): drag changes 1.3277 to 1.3289 and the mesh uncertainty is 0.004327, which is PASS. Strouhal changes 0.16382 to 0.16455 (0.44%). Its mesh uncertainty is 0.02187, above the 0.015 component limit, because of the assumed order p=2 with Fs=3. This is INCONCLUSIVE, not a FAIL.
  - Domain (R0 to R2): drag changes 1.3277 to 1.3208 (0.53%) and Strouhal 0.16382 to 0.1633 (0.31%). The estimated domain uncertainties are 0.03173 and 0.01884, both INCONCLUSIVE. These are inflated by the assumed order p=1.
  - Caveat on R2: checkMesh_ok is false. Its far-field and wake mesh is also much coarser (representative cell size 0.82162 D, last wake cell 1.8673 D, versus 0.47033 D and 0.96749 D for R0). Its drag CI95 is 0.00088885 and its drift is -0.0019997, much larger than for R0 or R1. The R0-to-R2 change therefore mixes domain size with mesh coarsening and a shorter record. It is a weak domain estimate.
  - Time uncertainty is unmeasured for both quantities, and no REDUCE_TIME_STEP run exists. It is a required component for ACCEPT. Temporal error cannot be inferred from steps per period or Courant number (R0 872.03 steps per period, Courant 0.648).
  - Budget: 2 of 6 experiments and 2.26 of 12 compute units used. REDUCE_TIME_STEP from R0 costs an estimated 8577 s and is affordable. R0 is the correct parent: it is the root, has the longest record (13 cycles), and was not refined or expanded.
  - Order of next steps: time first, because it is completely unmeasured and cannot be bounded any other way. After that, a third mesh level for Strouhal and a third domain level (EXPAND_DOMAIN from R2 or a differently sized domain) can give observed orders in place of the assumed ones.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Time error is the only component that is completely unmeasured for both quantities, and ACCEPT requires it. It cannot be bounded from existing runs. R0 is the root with the longest record and unmodified mesh and domain, so it isolates the time-step effect cleanly. The cost is an estimated 8577 s, which is within budget.
  - Outcome: executed -> K2_fine_large.dt0.0035-6a0f9a80f290 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - Time is now measured and passes. R3 (dt 0.0035) gives drag 1.3251 and St 0.16393 against R0 1.3277 and 0.16382. Time uncertainty is 0.007908 for drag and 0.0027 for St.
  - Drag mesh passes. R1 gives 1.3289 against R0 1.3277, with mesh uncertainty 0.004327. Averaging and statistics uncertainties are tiny for both quantities.
  - Domain is the blocking component for both quantities. Drag domain uncertainty is 0.03173, which exceeds the 0.5*tolerance limit of 0.015. St domain uncertainty is 0.01884. The demonstrated changes are small (0.53% drag, 0.31% St), so the large values come from the assumed order p=1 with Fs=3, not from a measured large effect.
  - R2 is a confounded domain estimate. checkMesh_ok is false. Its representative cell size is 0.82162 D against 0.47033 D for R0, and its last wake cell is 1.8673 D against 0.96749 D. Its drag CI95 is 0.00088885 and its drift is -0.0019997, both much worse than R0. The R0-to-R2 change mixes domain size, far-field coarsening and a shorter record.
  - A third domain level would give an observed order in place of the assumed p=1. EXPAND_DOMAIN from R0 with factor 1.5 gives levels R0 (1.0), new (1.5) and R2 (2.0). It is the cheapest menu entry at 5621 s. It also stays below the 160000 cell limit, because R2 at factor 2.0 has 71104 cells and R0 has 54244. This follows from the recorded counts and is not a measured count for the new run.
  - St mesh uncertainty is 0.02187 and is also INCONCLUSIVE. The R0-to-R1 St change is only 0.44%. A third mesh level (REFINE_MESH from R0, small factor) is the next step after domain. Budget is 3 of 6 experiments and 3.33 of 12 compute units used, so both are affordable.
  - R1 is not an allowed parent for EXPAND_DOMAIN (181768 cells > 160000). R0 is the root, has 13 cycles and a valid mesh, so it is the parent.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on K2_fine_large-2d999cd1eb7c — Domain uncertainty is the component that blocks ACCEPT for both quantities. It is estimated only from the confounded R2 (checkMesh_ok false, coarser far field, short record) with an assumed order p=1. A third domain level at factor 1.5 gives an observed order. It is the cheapest menu entry (5621 s from R0) and stays below the cell limit.
  - Outcome: executed -> K2_fine_large.D1.5x-c2938461e5bc (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed and REJECT is not justified.
  - Averaging, statistics and time pass for both quantities. Drag time uncertainty is 0.007908 and St time uncertainty is 0.0027. R3 (dt 0.0035) gives drag 1.3251 and St 0.16393, against R0 1.3277 and 0.16382.
  - Drag mesh passes at 0.004327 (R1 1.3289 vs R0 1.3277). St mesh is INCONCLUSIVE at 0.02187, above 0.015. The demonstrated R0-to-R1 change is only 0.44%, so the large value comes from the assumed p=2 with Fs=3 on two levels.
  - Drag domain is INCONCLUSIVE at 0.01587, just above 0.015. The verifier reports a demonstrated change of 0.53%. St domain passes at 0.00942.
  - Drag falls monotonically as the domain grows: R0 1.3277, R4 1.3237, R2 1.3208. This ordering is systematic and is not within noise.
  - R2 and R4 are weak domain points. Both have checkMesh_ok false and coarser far-field meshes than R0. They have only 6 cycles on a 80 D/U record. Their drag drift is -0.0019997 (R2) and -0.00081836 (R4), against -2.9076e-05 for R0. R2's CI95 is 0.00088885, against 1.0366e-05 for R0.
  - The R2 drift (-0.0019997) is a large fraction of the 0.53% R0-to-R2 difference. The drag spread may therefore include an unfinished transient in R2, not only a boundary effect. R0 was averaged over a 13-cycle window that reaches 150 D/U.
  - RUN_LONGER on R2 separates these two causes. It is the cheapest informative option (7027 s). A longer R2 record, comparable to R0's, tests whether the R2 value settles and whether the drag spread is a real domain effect.
  - Budget: 4 of 6 experiments and 3.96 of 12 compute units used. This run and a later REFINE_MESH from R0 with a small factor (for the St mesh order) both fit in the remaining budget.
  - RUN_LONGER is preferred to another EXPAND_DOMAIN. A new domain level would keep the same short-record and far-field confounders. It would also widen the spread if the drag trend continues.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on K2_fine_large.D2x-bc527461f36d — R2 is the largest-domain run and defines one end of the drag domain spread. Its record is short (6 cycles, 80 D/U), it has the largest drag drift (-0.0019997) and CI95 (0.00088885), and it has checkMesh_ok false. Extending it by 100 D/U gives a record comparable to R0's (150 D/U). This tests whether the 0.53% drag difference from R0 is a real boundary effect or a transient and sampling artefact. It costs an estimated 7027 s.
  - Outcome: executed -> K2_fine_large.long180-dda8a9c17278 (completed)

**Critic iteration 7** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and there is no FAIL to justify REJECT.
  - Averaging, statistics and time pass for both quantities. Drag time uncertainty is 0.007908 and St time uncertainty is 0.0027. Drag mesh passes at 0.004327.
  - Still INCONCLUSIVE: drag domain, St mesh (0.02187 against a 0.015 limit) and St domain (0.01522 against 0.015). The demonstrated changes are small: 0.44% for the St mesh change and 0.37% for the St domain change. These large uncertainties come from the assumed or poorly-determined orders (p=2 with Fs=3 for the St mesh, observed p=0.64 for the St domain).
  - R5 is the longer R2 run (14 cycles, CI95 2.2903e-05, drift -9.4811e-05). It gives drag 1.3196, against R2's 1.3208 over the shorter record. The drag drift in R2 was therefore not the cause of the R0-to-R2 difference. The R5 value moved further from R0, not toward it.
  - The drag domain trend is real and monotonic: R0 1.3277 (60 D half-height), R4 1.3237 (90 D), R2 1.3208 and R5 1.3196 (120 D). The verifier reports the sequence diverges (R = 1.02 >= 1), so no extrapolation is possible. The root-to-finest change is 0.62%, well below the 3% tolerance. This is a measured trend and not a FAIL.
  - St also falls with domain size: R0 0.16382, R4 0.16348, R5 0.16321. The domain component is therefore open for both quantities. The mesh component is open only for St.
  - Budget: 5 of 6 experiments and 4.83 of 12 compute units used. One experiment remains. EXPAND_DOMAIN addresses two open components (drag domain and St domain). REFINE_MESH addresses only one (St mesh), and it costs more (8677 s from R0).
  - The domain sequence has levels at 60, 90 and 120 D. A larger boundary distance tests whether the drag drift with domain size is flattening, which is the thing the Eca-Hoekstra check needs. Factor 3.0 from R0 gives 180 D, a clearly separated fourth level. The cost is the cheapest on the menu (5621 s from R0). The cell count should stay under the limit, since R2 at factor 2.0 has 71104 cells. This is an inference from recorded counts and not a measurement.
  - Parent R0 is deliberate. It is the root, has the longest record and the finest-quality near-field mesh, and it is the cheapest parent. R1 is not allowed as a parent (cell limit).
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on K2_fine_large-2d999cd1eb7c — Domain is the component that blocks ACCEPT for drag and also leaves St marginal. The drag domain sequence R0 1.3277, R4 1.3237, R5 1.3196 diverges under the Eca-Hoekstra check, so no extrapolation is possible. A 180 D level adds a clearly separated fourth point, so the verifier can test whether the trend flattens. It is the cheapest menu entry (5621 s from R0) and addresses two open components. It leaves compute within budget. R0 is the root with 13 cycles, and R1 is not allowed as a parent.
  - Outcome: executed -> K2_fine_large.D3x-7a1272bafc30 (completed)

Run K2_fine_large.m2-e923e7640822: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→2, time.delta_t: 0.007→0.006077, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3289 (+0.09%).
  - Observation: strouhal_number 0.16382 → 0.16455 (+0.44%).

Run K2_fine_large.D2x-bc527461f36d: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→120, domain.half_height: 60→120, domain.upstream: 40→80, mesh.n_downstream: 120→155, mesh.n_lateral: 51→61, mesh.n_upstream: 38→46, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3208 (-0.53%).
  - Observation: strouhal_number 0.16382 → 0.16331 (-0.31%).

Run K2_fine_large.dt0.0035-6a0f9a80f290: REDUCE_TIME_STEP from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, time.delta_t: 0.007→0.0035, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3251 (-0.20%).
  - Observation: strouhal_number 0.16382 → 0.16393 (+0.07%).

Run K2_fine_large.D1.5x-c2938461e5bc: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→90, domain.half_height: 60→90, domain.upstream: 40→60, mesh.n_downstream: 120→140, mesh.n_lateral: 51→57, mesh.n_upstream: 38→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3237 (-0.30%).
  - Observation: strouhal_number 0.16382 → 0.16349 (-0.20%).

Run K2_fine_large.long180-dda8a9c17278: RUN_LONGER from K2_fine_large.D2x-bc527461f36d (time.end_time: 80→180).
  - Observation: mean_drag_coefficient 1.3208 → 1.3196 (-0.09%).
  - Observation: strouhal_number 0.16331 → 0.16321 (-0.06%).

Run K2_fine_large.D3x-7a1272bafc30: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→180, domain.half_height: 60→180, domain.upstream: 40→120, mesh.n_downstream: 120→175, mesh.n_lateral: 51→67, mesh.n_upstream: 38→51, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3196 (-0.61%).
  - Observation: strouhal_number 0.16382 → 0.16335 (-0.29%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K2_fine_large-2d999cd1eb7c` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=8041 s; record: results/runs/K2_fine_large-2d999cd1eb7c/run.json
- `K2_fine_large.m2-e923e7640822` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:39+00:00 wall=1.145e+04 s; record: results/runs/K2_fine_large.m2-e923e7640822/run.json
- `K2_fine_large.D2x-bc527461f36d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:02+00:00 wall=3765 s; record: results/runs/K2_fine_large.D2x-bc527461f36d/run.json
- `K2_fine_large.dt0.0035-6a0f9a80f290` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T01:15:34+00:00 wall=3507 s; record: results/runs/K2_fine_large.dt0.0035-6a0f9a80f290/run.json
- `K2_fine_large.D1.5x-c2938461e5bc` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T14:15:17+00:00 wall=4059 s; record: results/runs/K2_fine_large.D1.5x-c2938461e5bc/run.json
- `K2_fine_large.long180-dda8a9c17278` status=completed parent=K2_fine_large.D2x-bc527461f36d created=2026-10-20T08:47:43+00:00 wall=4900 s; record: results/runs/K2_fine_large.long180-dda8a9c17278/run.json
- `K2_fine_large.D3x-7a1272bafc30` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T15:24:08+00:00 wall=4893 s; record: results/runs/K2_fine_large.D3x-7a1272bafc30/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 6558607222.0, "relative_to_root": 5.642323865908691, "experiment_wall_seconds": 32573.535929135996, "n_experiments": 6, "planner_calls": 7, "planner_cost_usd": 0.7358284350000001, "loop_wall_seconds": 9143.603104753005}
