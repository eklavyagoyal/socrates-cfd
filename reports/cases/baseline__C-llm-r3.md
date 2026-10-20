# Verification report: baseline (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3313
- strouhal_number: 0.16344

## VERDICT: **ACCEPT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 8.23e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 6.60e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.86% <= 1.50% (root-to-finest change 0.284%) [three-level, observed order inf outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.33% <= 1.50% (root-to-finest change 0.866%) [three-level Celik procedure, observed order p=2.39, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.10% <= 1.50% (root-to-finest change 0.276%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.31% <= 1.50% (root-to-finest change 0.077%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.6e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.23% <= 1.50% (root-to-finest change 0.647%) [three-level Celik procedure, observed order p=1.55, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.79% <= 1.50% (root-to-finest change 0.436%) [three-level Celik procedure, observed order p=1.68, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run baseline-408129116207 is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── baseline-408129116207
├── mesh_quality: PASS
│   └── baseline-408129116207
├── mass_conservation: PASS
│   └── baseline-408129116207
├── linear_solver_convergence: PASS
│   └── baseline-408129116207
├── courant_number: PASS
│   └── baseline-408129116207
├── reynolds_consistency: PASS
│   └── baseline-408129116207
├── force_reference_consistency: PASS
│   └── baseline-408129116207
├── physics_regime: PASS
│   └── baseline-408129116207
├── convection_scheme_order: PASS
│   └── baseline-408129116207
├── Averaging window (reported vs stationary value): PASS U=9.37e-05
│   └── baseline-408129116207
├── Temporal statistics (stationarity, cycles): PASS U=8.23e-05
│   └── baseline-408129116207
├── Spatial discretisation (mesh sensitivity): PASS U=0.00858
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-93c9ab8d6f2d
├── Temporal discretisation (time-step sensitivity): PASS U=0.011
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): PASS U=0.0123
    └── baseline-408129116207
    └── baseline.D1.5x-c018e6157314
    └── baseline.D2x-efba395f6c27

CLAIM: strouhal_number of run baseline-408129116207 is reliable to within 3%  [ACCEPT]
├── solver_completion: PASS
│   └── baseline-408129116207
├── mesh_quality: PASS
│   └── baseline-408129116207
├── mass_conservation: PASS
│   └── baseline-408129116207
├── linear_solver_convergence: PASS
│   └── baseline-408129116207
├── courant_number: PASS
│   └── baseline-408129116207
├── reynolds_consistency: PASS
│   └── baseline-408129116207
├── force_reference_consistency: PASS
│   └── baseline-408129116207
├── physics_regime: PASS
│   └── baseline-408129116207
├── convection_scheme_order: PASS
│   └── baseline-408129116207
├── Averaging window (reported vs stationary value): PASS U=1.55e-05
│   └── baseline-408129116207
├── Temporal statistics (stationarity, cycles): PASS U=6.6e-05
│   └── baseline-408129116207
├── Spatial discretisation (mesh sensitivity): PASS U=0.0133
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-93c9ab8d6f2d
├── Temporal discretisation (time-step sensitivity): PASS U=0.00309
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): PASS U=0.00794
    └── baseline-408129116207
    └── baseline.D1.5x-c018e6157314
    └── baseline.D2x-efba395f6c27

```

## EXPERIMENT HISTORY

Run baseline-408129116207: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Verifier verdict is INCONCLUSIVE with no failed checks. The mesh, time and domain components are all unmeasured for both quantities, so ACCEPT is not allowed. REJECT is not justified because nothing has failed.
  - R0 averaging and statistics components pass for both quantities. Drag: averaging 9.366e-05, statistics 8.229e-05. Strouhal: averaging 1.551e-05, statistics 6.605e-05. There are 12 stationary cycles and the drag drift is 8.2286e-05. Statistical noise is not the limiting factor, so RUN_LONGER would add little.
  - R0 mesh is the most likely source of a change larger than 3%. The representative cell size is 0.45745 D, with 30580 cells in total. The wake last cell is 1.0209 D, so the far wake is coarse. The wall first cell is 0.005 D and there are 160 cells around the cylinder. Shedding frequency and mean drag both depend on wake and near-wall resolution.
  - R0 time step is probably a smaller risk. It uses backward (second-order) time stepping with 611.87 steps per shedding period and a max Courant number of 0.73373. The convection scheme is nominally second order (linearUpwind).
  - R0 domain is probably a smaller risk than the mesh. It has 30 D upstream, 50 D downstream and 40 D half-height, giving a blockage of 0.0125. Its effect is still unmeasured and should be checked later.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 compute units used. A refinement of R0 costs about 1779 s, against 1441.6 s for the root run. A large refinement factor gives the clearest signal against the 3% tolerance.
  - Requested: REFINE_MESH {'factor': 2.0} on baseline-408129116207 — Mesh resolution is the most likely source of a change larger than the 3% tolerance. R0 has a representative cell size of 0.45745 D, a wake last cell of 1.0209 D and 30580 cells. Time and domain settings look comparatively safe. Statistical and averaging uncertainties are already negligible.
  - Outcome: executed -> baseline.m2-93c9ab8d6f2d (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The verifier verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - R0 averaging and statistics pass for both quantities. Cd: averaging 9.366e-05, statistics 8.229e-05. St: averaging 1.551e-05, statistics 6.605e-05. R0 has 12 stationary cycles. RUN_LONGER would add little.
  - Mesh: R1 (cell size 0.22873 D, 122320 cells) changed Cd by 0.284% against R0 and St by 0.87%. The Cd mesh uncertainty is 0.01137, which passes. The St mesh uncertainty is 0.03464, which is inconclusive. It comes from the assumed p=2 and Fs=3 factors, not from a demonstrated change above tolerance.
  - A further mesh refinement from R1 is not allowed because the cumulative refinement limit of 2.0 is reached. The St mesh component can only be tightened later, for example with a third level from R0, and that does not resolve the time and domain gaps.
  - Time and domain are unmeasured for both quantities and block ACCEPT regardless of the mesh result. EXPAND_DOMAIN on R0 is the cheapest experiment (1021 s). The domain is the least checked assumption: blockage ratio 0.0125, lateral symmetryPlane boundaries at 40 D half-height, and 30 D upstream with a fixed-value outlet pressure at 50 D. These can shift Cd and St independently of the mesh.
  - Time step is a lower risk. R0 uses backward time stepping with 611.87 steps per shedding period and max Courant 0.73373. R1 used 989.02 steps per period and gave a St shift of only 0.87%. A REDUCE_TIME_STEP run should follow.
  - Budget is sufficient. 1 of 6 experiments are used and 3.48 of 12 compute units. Domain, time and a possible third mesh level all fit.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on baseline-408129116207 — Domain truncation and blockage are unmeasured for both quantities and cannot be inferred from the recorded evidence. This is the cheapest experiment (1021 s) and keeps the R0 near-field mesh unchanged. It isolates the effect of the artificial boundaries (blockage 0.0125, symmetry lateral boundaries, fixed-value outlet pressure) on Cd and St.
  - Outcome: executed -> baseline.D2x-efba395f6c27 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - Verifier verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - R0 averaging and statistics pass for both quantities (Cd: 9.366e-05 and 8.229e-05; St: 1.551e-05 and 6.605e-05), with 12 stationary cycles. RUN_LONGER would add little.
  - Time error is unmeasured for both Cd and St (no REDUCE_TIME_STEP run). This component blocks ACCEPT for both quantities whatever the other results are.
  - Mesh: R1 changed Cd by 0.284% and St by 0.87% against R0. The Cd mesh uncertainty is 0.01137 (PASS). The St mesh uncertainty is 0.03464 (INCONCLUSIVE) and comes from the assumed p=2 and Fs=3, not from a demonstrated change above tolerance. R1 has cumulative refinement 2.0, so further refinement from R1 is not allowed.
  - Domain: R2 changed Cd by 0.65% and St by 0.44% against R0. The estimated uncertainties of 0.03879 (Cd) and 0.02615 (St) come from the assumed p=1 and Fs=3. R2 has checkMesh_ok=false and a coarser far-field mesh (cell size 0.79405 D, wake last cell 1.9729 D), so the domain effect is confounded with mesh changes. R2 also has only 6 stationary cycles and a drag drift of -0.0015761.
  - Time is the only component with no measurement at all. REDUCE_TIME_STEP on R0 is cheap (1538 s). R0 has 611.87 steps per period and max Courant 0.73373; R1 had 989.02 steps per period and a St shift of 0.87%, so time error may be mixed into the mesh signal for St. The St mesh and time estimates cannot be separated until a time-step run exists.
  - Budget is sufficient: 2 of 6 experiments used and 4.19 of 12 compute units. A time-step run, a third mesh level and a further domain check all fit.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on baseline-408129116207 — The time component is completely unmeasured for both Cd and St and blocks ACCEPT regardless of the mesh and domain results. R0 is the cheapest parent (1538 s) and keeps the mesh and domain fixed. This isolates the temporal error. It also separates a possible time-step contribution from the 0.87% St change seen in R1, which used a smaller time step.
  - Outcome: executed -> baseline.dt0.005-693742b868bc (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The verifier verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed because the Cd domain component and the St mesh and domain components are unresolved. REJECT is not justified because nothing has failed.
  - R0 averaging and statistics pass for both quantities. Cd: averaging 9.366e-05, statistics 8.229e-05. St: averaging 1.551e-05, statistics 6.605e-05. R0 has 12 stationary cycles, so RUN_LONGER would add little.
  - Time now passes. R3 (dt 0.005) changed Cd by 0.276% and St by 0.077% against R0. The time uncertainties are 0.01103 (Cd) and 0.003094 (St), both within 0.5*tolerance (0.015).
  - Mesh: R1 changed Cd by 0.284%, giving a mesh uncertainty of 0.01137 (PASS). R1 changed St by 0.87%, giving 0.03464 (INCONCLUSIVE). This St value comes from the assumed p=2 and Fs=3 with only two levels, not from a demonstrated change above tolerance. Refining from R1 is not allowed (cumulative factor limit 2.0).
  - Domain is the only component missing for Cd, and it is also missing for St. R2 (domain 60/100/80 D) changed Cd by 0.65% and St by 0.44%. The uncertainties of 0.03879 (Cd) and 0.02615 (St) come from the assumed p=1 and Fs=3, and they exceed the 0.015 budget. The domain therefore blocks ACCEPT for both quantities.
  - The R2 domain result is confounded. R2 has checkMesh_ok=false, a coarser mesh (cell size 0.79405 D, wake last cell 1.9729 D) and only 6 stationary cycles. Its Cd drift is -0.0015761, with a noise floor of 1.6e-03. A third domain size on a mesh closer to R0 would give an observed convergence order for Cd and St together.
  - Budget: 3 of 6 experiments used and 5.25 of 12 compute units used. A domain run on R0 (about 1021 s or less) fits, and a third mesh level would still fit afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on baseline-408129116207 — Domain is the only missing component for Cd and also blocks St. The existing two-level pair R0/R2 gives 0.03879 (Cd) and 0.02615 (St) from an assumed order p=1. R2 is confounded by checkMesh_ok=false and a coarser far-field mesh. A run at 1.5x on R0 is the cheapest remaining experiment (at most 1021 s) and adds a third domain size between R0 and R2. This allows an observed convergence trend. Mesh and time sensitivities are already measured and are not the limiting factor for Cd.
  - Outcome: executed -> baseline.D1.5x-c018e6157314 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The verifier verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - Cd: the verifier returns ACCEPT for R0. All five components pass: averaging 9.366e-05, statistics 8.229e-05, mesh 0.01137, time 0.01103, domain 0.01231. Combined uncertainty is 0.02015, against a tolerance of 0.03.
  - St: only the mesh component is missing. Its uncertainty is 0.03464, against a budget of 0.015. The other components pass: averaging 1.551e-05, statistics 6.605e-05, time 0.003094, domain 0.007935.
  - The St mesh value comes from a two-level estimate (R0 vs R1) with assumed p=2 and Fs=3. It is not a demonstrated error. The R0-to-R1 St change is 0.87%, which is below the 3% tolerance. R0 St is 0.16344 and R1 St is 0.16486.
  - The St time effect is small: R3 changed St by 0.077% against R0 (0.16357 vs 0.16344). The R0-to-R1 St shift is therefore mainly spatial. The mesh order cannot be observed without a third level.
  - Domain now passes for both quantities with a three-level estimate from R0, R4 and R2. Observed order is p=1.55 for Cd and p=1.68 for St.
  - R1 is at the cumulative refinement limit of 2.0, so refining from R1 is not allowed. REFINE_MESH on R0 with factor 1.4142 gives an intermediate level between R0 and R1. It costs 1779 s.
  - Budget: 4 of 6 experiments are used. 5.89 of 12 compute units are used. One mesh run fits comfortably.
  - Requested: REFINE_MESH {'factor': 1.4142} on baseline-408129116207 — The St mesh component is the only unresolved item in the verifier. A third mesh level between R0 (0.45745 D) and R1 (0.22873 D) gives an observed convergence order and replaces the assumed p=2 and Fs=3 estimate. Time and domain pass for St, and every Cd component passes. R1 cannot be refined further because of the cumulative limit of 2.0.
  - Outcome: executed -> baseline.m1.41-807cdf343a51 (completed)

Run baseline.m2-93c9ab8d6f2d: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.29%).
  - Observation: strouhal_number 0.16343 → 0.16486 (+0.87%).

Run baseline.D2x-efba395f6c27: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3226 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

Run baseline.dt0.005-693742b868bc: REDUCE_TIME_STEP from baseline-408129116207 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run baseline.D1.5x-c018e6157314: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3251 (-0.46%).
  - Observation: strouhal_number 0.16343 → 0.16292 (-0.31%).

Run baseline.m1.41-807cdf343a51: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0187 vs tolerance 3%).
- strouhal_number: ACCEPT (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=PASS; combined uncertainty 0.0159 vs tolerance 3%).

## REMAINING LIMITATIONS

- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `baseline-408129116207` status=completed parent=None created=2026-10-19T07:00:06+00:00 wall=1442 s; record: results/runs/baseline-408129116207/run.json
- `baseline.m2-93c9ab8d6f2d` status=completed parent=baseline-408129116207 created=2026-10-19T07:38:06+00:00 wall=9774 s; record: results/runs/baseline.m2-93c9ab8d6f2d/run.json
- `baseline.D2x-efba395f6c27` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=3659 s; record: results/runs/baseline.D2x-efba395f6c27/run.json
- `baseline.dt0.005-693742b868bc` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=4058 s; record: results/runs/baseline.dt0.005-693742b868bc/run.json
- `baseline.D1.5x-c018e6157314` status=completed parent=baseline-408129116207 created=2026-10-20T07:52:56+00:00 wall=1316 s; record: results/runs/baseline.D1.5x-c018e6157314/run.json
- `baseline.m1.41-807cdf343a51` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=5234 s; record: results/runs/baseline.m1.41-807cdf343a51/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3266558064.0, "relative_to_root": 7.1213387050359716, "experiment_wall_seconds": 24040.648039223997, "n_experiments": 5, "planner_calls": 5, "planner_cost_usd": 0.419614315, "loop_wall_seconds": 94.3616346609997}
