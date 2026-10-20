# Verification report: K2_fine_large (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3278
- strouhal_number: 0.16382

## VERDICT: **ACCEPT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.34% <= 1.50% (root-to-finest change 0.076%) [oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 0.99% <= 1.50% (root-to-finest change 0.460%) [three-level Celik procedure, observed order p=1.74, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.79% <= 1.50% (root-to-finest change 0.198%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.068%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.27% <= 1.50% (root-to-finest change 0.700%) [three-level Celik procedure, observed order p=1.06, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.34% <= 1.50% (root-to-finest change 0.358%) [three-level, observed order 2.48 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [ACCEPT]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0034
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
│   └── K2_fine_large.m2.06-7ad5498c706d
├── Temporal discretisation (time-step sensitivity): PASS U=0.00791
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.0127
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D2x-bc527461f36d
    └── K2_fine_large.D1.5x-39e38799b1d6

CLAIM: strouhal_number of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [ACCEPT]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.00993
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
│   └── K2_fine_large.m2.06-7ad5498c706d
├── Temporal discretisation (time-step sensitivity): PASS U=0.0027
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): PASS U=0.0134
    └── K2_fine_large-2d999cd1eb7c
    └── K2_fine_large.D2x-bc527461f36d
    └── K2_fine_large.D1.5x-39e38799b1d6

```

## EXPERIMENT HISTORY

Run K2_fine_large-2d999cd1eb7c: submitted simulation (54244 cells, dt=0.007 D/U, half-height 60 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, because the mesh, time and domain components are unmeasured for both Cd and St. I can't REJECT, because no FAIL exists.
  - R0 passes the averaging and statistics components. Mean Cd is 1.3278 as reported and 1.3277 in the stationary window. The Cd 95% CI is 1.0366e-05, and the averaging uncertainty is 7.057e-05. The St averaging uncertainty is 4.994e-06.
  - The averaging and statistics results are internal-consistency measures only. They say nothing about the discretisation or truncation error of R0.
  - The mesh is the least-verified part. R0 has 54244 cells, a representative cell size of 0.47033 D, a last wake cell of 0.96749 D, and 150 streamwise wake cells over a 60 D downstream length. Wake resolution drives both the shedding frequency and the mean drag, and it has never been tested.
  - The recorded time step is small enough to be a lower-priority risk. R0 uses backward time stepping with 872.03 steps per shedding period, and its max Courant number is 0.64796.
  - The domain is large relative to the body. R0 has 40 D upstream, 60 D downstream, 60 D half-height, and a blockage ratio of 0.0083333. The domain error is probably small, but it is unmeasured.
  - The St frequency resolution is 0.013334 against St = 0.16382, about 8% of the value. That is coarser than the 3% tolerance, so the St estimate relies on peak interpolation. Both the FFT and the reported St give 0.16382, but the resolution limit is a separate risk. RUN_LONGER would address it after the mesh question.
  - Budget is ample: 0 of 6 experiments and 0 of 12 compute units are used. REFINE_MESH from R0 costs an estimated 8677 s.
  - Requested: REFINE_MESH {'factor': 1.4142} on K2_fine_large-2d999cd1eb7c — Mesh resolution is the most likely unmeasured error source. The wake cells are coarse, and Cd and St both depend on wake resolution. The estimated cost of 8677 s is affordable. A refinement result will show whether the R0 values hold within tolerance, and it starts the refinement sequence.
  - Outcome: executed -> K2_fine_large.m1.77-e5d0ad1d73b4 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 95%, 8%

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, because the time and domain components are unmeasured for both quantities. I can't REJECT, because there is no FAIL.
  - R0 to R1 mesh change for mean Cd: 1.3277 -> 1.3293 (0.113%). Mesh uncertainty is 0.006837 (0.68%) and passes.
  - R0 to R1 mesh change for St: 0.16382 -> 0.16441 (0.36%). The verifier's two-level Richardson estimate (assumed p=2, Fs=3) gives 0.02166, above the 1.5% component budget. Its status is INCONCLUSIVE, not FAIL, because the demonstrated change is within tolerance.
  - R1 can't be refined further: the child mesh would have 216220 cells against a 160000 limit. The St mesh component can only improve with a different refinement level from R0, or with more evidence on resolution.
  - Averaging and statistics pass for both quantities. R0 has 13 stationary cycles. The Cd 95% CI is 1.0366e-05 and the Cd drift is -2.9076e-05. These are internal-consistency measures only.
  - Time-step error is unmeasured. R0 has 872.03 steps per shedding period, backward time scheme and max Courant 0.64796. R1 is similar (884.69 steps per period, Courant 0.72461). The risk looks low, but it has not been measured.
  - Domain error is unmeasured. R0 has 40 D upstream, 60 D downstream, 60 D half-height with symmetryPlane sides, and blockage 0.0083333. The question says to treat the stream as unbounded, and the boundaries have never been tested.
  - EXPAND_DOMAIN on R0 is the cheapest remaining experiment (5621 s, against 8577 s for REDUCE_TIME_STEP). It fills a missing component for both Cd and St and runs on the same mesh and time step as R0, so the comparison is clean.
  - Budget: 1 of 6 experiments and 1.08 of 12 compute units are used, so there is room for the remaining experiments.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Domain truncation is unmeasured for both Cd and St, and the problem states the stream is unbounded. It is the cheapest remaining experiment (5621 s on R0). It uses the same mesh and time step as R0, so any change is attributable to the boundaries. Cd and St mesh changes so far are small (0.113% and 0.36%), so a domain flaw is the more likely hidden error.
  - Outcome: executed -> K2_fine_large.D2x-bc527461f36d (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 95%

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, because time is unmeasured for both quantities and the domain and St-mesh components are over the 1.5% component budget. I can't REJECT, because there is no FAIL.
  - Time component is still entirely unmeasured for Cd and St. The verifier says no REDUCE_TIME_STEP experiment has been run. Without it the error budget can never close, whatever happens to the other components. R0 uses backward differencing with 872.03 steps per shedding period and max Courant 0.64796. That looks low-risk, but it is not measured.
  - Mesh, Cd: R0 1.3277 -> R1 1.3293 (0.113% change). Mesh uncertainty is 0.006837 and passes.
  - Mesh, St: R0 0.16382 -> R1 0.16441 (0.36% change). The two-level estimate gives 0.02166 (assumed p=2, Fs=3), so it stays INCONCLUSIVE. R1 can't be refined further (216220 cells against a 160000 limit).
  - Domain: R0 -> R2 changes Cd 1.3277 -> 1.3208 (0.53%) and St 0.16382 -> 0.1633 (0.31%). The demonstrated changes are well inside tolerance. The estimates (Cd 0.03173, St 0.01884, assumed p=1, Fs=3) are inflated by the conservative factor and have no observed order.
  - R2 is weaker evidence than R0. Its checkMesh_ok is false. Its far-field and wake cells are coarser (wake_last_cell_D 1.8673 against 0.96749). It has only 6 cycles on an 80 D/U record. Its Cd CI95 is 0.00088885, against 1.0366e-05 for R0. Some of the R0-to-R2 difference may therefore come from mesh and record differences, not from the boundaries.
  - R0 averaging and statistics pass (13 cycles, Cd CI95 1.0366e-05). These measure internal consistency only.
  - Budget is ample: 2 of 6 experiments used and 1.78 of 12 compute units. REDUCE_TIME_STEP on R0 is estimated at 8577 s.
  - I picked the time-step test because it is the only component with no measurement at all. It runs on R0's identical mesh and domain, so any change is attributable to the time step alone.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K2_fine_large-2d999cd1eb7c — Temporal error is the only component with no measurement for either quantity, so the budget can't close without it. R0 is the best-converged run (13 cycles, tight CI), and halving its time step on the same mesh and domain isolates the temporal effect. The cost is 8577 s, which is affordable.
  - Outcome: executed -> K2_fine_large.dt0.0035-6a0f9a80f290 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. I can't ACCEPT, and I can't REJECT because there is no FAIL.
  - Still unresolved: Cd domain 0.03173, St mesh 0.02166 and St domain 0.01884. Each is above the 0.015 component budget (0.5 x 3%). Cd domain is also above the full 3% tolerance. Averaging, statistics, time (Cd 0.007908, St 0.0027) and Cd mesh (0.006837) pass.
  - The three open estimates are inflated by assumptions, not by measured changes. The domain estimates use assumed order p=1 and Fs=3. The St mesh estimate uses assumed p=2 and Fs=3. The demonstrated changes are small: Cd domain 0.53%, St domain 0.31%, St mesh 0.36%, all inside the 3% tolerance.
  - Domain is the largest open item and affects both quantities. R0 to R2 changes Cd 1.3277 -> 1.3208 and St 0.16382 -> 0.1633. Only two domain levels exist, so no observed order can be computed.
  - R2 is weaker evidence than R0. R2 has checkMesh_ok=false and a coarser far field (wake_last_cell_D 1.8673 vs 0.96749). R2 has 6 cycles and a Cd CI95 of 0.00088885 (R0: 1.0366e-05). Part of the R0-to-R2 difference may come from that coarsening and the short record, not from the boundaries.
  - A third domain level continuing from R2 (factor 1.5 gives 3x R0) gives a nested sequence of R0, R2 and the child. That allows an observed convergence order for Cd and St, or shows whether the domain effect is saturating. Estimated cost is 7234 s.
  - Budget is available. 3 of 6 experiments are used and 2.84 of 12 compute units. After this run, a third mesh level for the St mesh estimate stays affordable. R1 can't be refined further, but REFINE_MESH from R0 at a factor up to about 1.7 stays under the 160000-cell limit.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on K2_fine_large.D2x-bc527461f36d — Domain is the largest unresolved component. It affects both Cd and St, and the Cd domain estimate (0.03173) is above the full tolerance. Only two domain levels exist, so no observed order can be formed. Continuing from R2 gives a nested sequence of R0, R2 and the child at 1x, 2x and 3x. The estimated cost is 7234 s, which fits the remaining budget and leaves room for a third mesh level for St.
  - Outcome: executed -> K2_fine_large.D1.5x-39e38799b1d6 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 1.7

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so I can't ACCEPT and I can't REJECT.
  - Mean drag coefficient already has per-quantity verdict ACCEPT. Its combined uncertainty is 0.01654 against the 0.03 tolerance. The R4 run closed the domain component, which is now 0.01273 with observed order p=1.06.
  - Strouhal number has one open item. Its mesh component is INCONCLUSIVE at 0.02166, above the 0.015 component budget. Averaging (4.994e-06), statistics (2.011e-05), time (0.0027) and domain (0.01336) all pass.
  - The St mesh estimate comes from a two-level Richardson using R0 and R1, with assumed p=2 and Fs=3. The measured change is small: St goes from 0.16382 (R0) to 0.16441 (R1), a 0.36% change. The estimate is therefore set by the assumed order and safety factor, not by a demonstrated error. The verifier says more refinement is needed.
  - A third mesh level would give an observed order and a three-level Celik estimate, as the domain study did with R0, R2 and R4. R1 can't be refined further (216220 cells against a 160000 limit). A REFINE_MESH from R0 at a larger factor can stay under the limit. That gives R0 (0.47033 D), R1 (0.33363 D) and a finer level.
  - The R0 refinement factor should leave margin under the cell limit. R0 has 54244 cells and R1's cell count scaled by about the square of the linear factor. A factor of 1.65 gives about 148000 cells. A factor of 1.7 would be about 157000 cells, too close to the 160000 limit.
  - Budget: 4 of 6 experiments are used and 3.66 of 12 compute units. One experiment is affordable. The estimated cost is below the 8677 s quoted for factor 1.4142 on R0, scaled up for the finer mesh.
  - The other Strouhal-number items are lower priority. R0 has 13 stationary cycles and the frequency estimates agree between the reported value and the FFT (0.16382 each). RUN_LONGER wouldn't close the mesh component.
  - Requested: REFINE_MESH {'factor': 1.65} on K2_fine_large-2d999cd1eb7c — The only open verifier item is the St mesh component (0.02166, INCONCLUSIVE). It comes from a two-level estimate with assumed p=2 and Fs=3. A third level from R0 gives an observed order and a three-level estimate. R1 can't be refined further because of the 160000 cell limit. Factor 1.65 gives about 148000 cells, which stays under the limit with margin.
  - Outcome: executed -> K2_fine_large.m2.06-7ad5498c706d (completed)
  - Numeric audit: 6 number(s) not traceable to evidence: 1.65, 148000, 1.7, 157000, 1.65

Run K2_fine_large.m1.77-e5d0ad1d73b4: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→1.768, time.delta_t: 0.007→0.006875, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3293 (+0.11%).
  - Observation: strouhal_number 0.16382 → 0.16441 (+0.36%).

Run K2_fine_large.D2x-bc527461f36d: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, domain.downstream: 60→120, domain.half_height: 60→120, domain.upstream: 40→80, mesh.n_downstream: 120→155, mesh.n_lateral: 51→61, mesh.n_upstream: 38→46, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3208 (-0.53%).
  - Observation: strouhal_number 0.16382 → 0.16331 (-0.31%).

Run K2_fine_large.dt0.0035-6a0f9a80f290: REDUCE_TIME_STEP from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, time.delta_t: 0.007→0.0035, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3251 (-0.20%).
  - Observation: strouhal_number 0.16382 → 0.16393 (+0.07%).

Run K2_fine_large.D1.5x-39e38799b1d6: EXPAND_DOMAIN from K2_fine_large.D2x-bc527461f36d (domain.downstream: 120→180, domain.half_height: 120→180, domain.upstream: 80→120, mesh.n_downstream: 155→176, mesh.n_lateral: 61→67, mesh.n_upstream: 46→51).
  - Observation: mean_drag_coefficient 1.3208 → 1.3185 (-0.17%).
  - Observation: strouhal_number 0.16331 → 0.16324 (-0.04%).

Run K2_fine_large.m2.06-7ad5498c706d: REFINE_MESH from K2_fine_large-2d999cd1eb7c (averaging.start_time: 75→40, mesh.refinement: 1.25→2.062, time.delta_t: 0.007→0.005893, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3277 → 1.3288 (+0.08%).
  - Observation: strouhal_number 0.16382 → 0.16458 (+0.46%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0154 vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0169 vs tolerance 3%).

## REMAINING LIMITATIONS

- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K2_fine_large-2d999cd1eb7c` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=8041 s; record: results/runs/K2_fine_large-2d999cd1eb7c/run.json
- `K2_fine_large.m1.77-e5d0ad1d73b4` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-19T10:01:45+00:00 wall=4914 s; record: results/runs/K2_fine_large.m1.77-e5d0ad1d73b4/run.json
- `K2_fine_large.D2x-bc527461f36d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:02+00:00 wall=3765 s; record: results/runs/K2_fine_large.D2x-bc527461f36d/run.json
- `K2_fine_large.dt0.0035-6a0f9a80f290` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T01:15:34+00:00 wall=3507 s; record: results/runs/K2_fine_large.dt0.0035-6a0f9a80f290/run.json
- `K2_fine_large.D1.5x-39e38799b1d6` status=completed parent=K2_fine_large.D2x-bc527461f36d created=2026-10-20T07:52:07+00:00 wall=5345 s; record: results/runs/K2_fine_large.D1.5x-39e38799b1d6/run.json
- `K2_fine_large.m2.06-7ad5498c706d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T09:43:02+00:00 wall=1.271e+04 s; record: results/runs/K2_fine_large.m2.06-7ad5498c706d/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 6239233304.0, "relative_to_root": 5.367568720695001, "experiment_wall_seconds": 30240.509237988008, "n_experiments": 5, "planner_calls": 5, "planner_cost_usd": 0.44710261500000004, "loop_wall_seconds": 19860.774626011997}
