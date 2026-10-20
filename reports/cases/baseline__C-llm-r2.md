# Verification report: baseline (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3313
- strouhal_number: 0.16344

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.009% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 8.23e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 6.60e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.15% <= 1.50% (root-to-finest change 0.333%) [three-level, observed order 4.93 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.32% <= 1.50% (root-to-finest change 0.862%) [three-level Celik procedure, observed order p=2.43, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.10% <= 1.50% (root-to-finest change 0.276%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.31% <= 1.50% (root-to-finest change 0.077%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.6e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.88% > 1.50% but the demonstrated change 0.89% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.82, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.59% > 1.50% but the demonstrated change 0.62% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.61, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run baseline-408129116207 is reliable to within 3%  [INCONCLUSIVE]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0115
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.011
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0188
    └── baseline-408129116207
    └── baseline.D1.5x-c018e6157314
    └── baseline.D2x-efba395f6c27
    └── baseline.D1.5x-ed421affd588

CLAIM: strouhal_number of run baseline-408129116207 is reliable to within 3%  [INCONCLUSIVE]
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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.00309
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0159
    └── baseline-408129116207
    └── baseline.D1.5x-c018e6157314
    └── baseline.D2x-efba395f6c27
    └── baseline.D1.5x-ed421affd588

```

## EXPERIMENT HISTORY

Run baseline-408129116207: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both ruled out. Mesh, time and domain uncertainty are unmeasured for both quantities (R0).
  - R0 averaging and statistics components are measured and tiny. For drag they are 9.366e-05 and 8.229e-05. For Strouhal they are 1.551e-05 and 6.605e-05. Averaging and statistics are not the limiting factor, so RUN_LONGER would add little.
  - R0 completed (15000 steps, max Courant 0.73373). It has 12 stationary cycles and 611.87 steps per shedding period. Mass imbalance is 8.3333e-11, and the checks for linear-solver convergence, Reynolds consistency and force reference all pass. Together these make time-step error less likely to be the dominant error than spatial error.
  - R0 spatial resolution is the weakest recorded point. The representative cell size is 0.45745 D on 30580 cells, and the last wake cell is 1.0209 D. Wake resolution controls shedding frequency and the mean drag. Strouhal number and drag could therefore shift by more than 3% on refinement.
  - The domain is 30 D upstream, 50 D downstream and 40 D half-height, with blockage ratio 0.0125. It is already fairly large, so domain error is a lower-priority hypothesis than mesh error.
  - REFINE_MESH from R0 is the most informative single experiment. It addresses both requested quantities. It costs 1779 s, and the budget allows 6 experiments and 12x the root compute, with none used so far.
  - Requested: REFINE_MESH {'factor': 1.4142} on baseline-408129116207 — Mesh error is the largest unmeasured component and the most likely to move the mean drag or Strouhal number by more than the 3% tolerance. R0 has a coarse representative cell size (0.45745 D) and a coarse far wake (last cell 1.0209 D). The other recorded components (averaging, statistics, Courant, mass balance, solver residuals) are already well controlled.
  - Outcome: executed -> baseline.m1.41-807cdf343a51 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both ruled out.
  - Mesh uncertainty is the only component with a measured value above budget: 0.0169 for mean drag and 0.03625 for Strouhal number. Both exceed the 1.5% budget (0.5*tolerance), and the Strouhal value is above the 0.03 tolerance itself.
  - The R0 to R1 change is small: drag 1.3311 to 1.3349, Strouhal 0.16343 to 0.16443. The verifier says the demonstrated change is within tolerance, so no FAIL applies. The two-level Richardson estimate assumes order p=2. A third mesh level on R1 would give an observed order and a better-founded estimate.
  - R1 also changed the time step (0.01 to 0.0086734 convective units), so the R0 to R1 difference mixes spatial and temporal effects. Refining from R1 continues the refinement family, and the later time-step run on R0 or R1 will help separate the two effects.
  - Averaging and statistics are small for both runs. Drag values are 9.366e-05 and 8.229e-05. Strouhal values are 1.551e-05 and 6.605e-05. RUN_LONGER would add little.
  - Time and domain components are unmeasured. Mesh uncertainty alone could break the error budget, so it is resolved first. Domain (blockage 0.0125, 30 D upstream, 50 D downstream, 40 D half-height) and time step (R0 has 611.87 steps per period, max Courant 0.73373) are lower-priority hypotheses.
  - Budget: 1 of 6 experiments used and 1.23 of 12 compute units used. REFINE_MESH from R1 is listed at 4087 s. R1 recorded 5234 s against a listed estimate of 1779 s for R0, so actual cost may exceed the listed estimates. Remaining budget should be watched for the later time-step and domain runs.
  - Requested: REFINE_MESH {'factor': 1.4142} on baseline.m1.41-807cdf343a51 — Mesh is the only component with a measured uncertainty above budget (drag 0.0169, Strouhal 0.03625 against a 1.5% component budget). It rests on a two-level estimate with assumed order p=2. A third level on the R1 family gives an observed order and a defensible mesh uncertainty for both requested quantities.
  - Outcome: executed -> baseline.m2-476115cbbf20 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so neither ACCEPT nor REJECT is allowed. The time and domain components are missing for both mean_drag_coefficient and strouhal_number.
  - Mesh is now measured from R0, R1 and R2. Drag mesh uncertainty is 0.01151 and Strouhal mesh uncertainty is 0.01321. Both are at or below the 0.015 component budget (0.5*tolerance). Averaging and statistics are tiny: drag 9.366e-05 and 8.229e-05, Strouhal 1.551e-05 and 6.605e-05. RUN_LONGER and further REFINE_MESH would add little.
  - Mesh refinement moved the R0 stationary-window values as follows. Drag went from 1.3311 (R0) to 1.3349 (R1) to 1.3356 (R2). Strouhal went from 0.16343 to 0.16443 to 0.16485. Each change shrinks with refinement, so the mesh component is settled enough to move on.
  - R0 has a blockage ratio of 0.0125, 30 D upstream, 50 D downstream and 40 D half-height. It uses symmetryPlane lateral boundaries, a fixedValue outlet pressure and a zeroGradient inlet pressure. The question says to treat the stream as unbounded. No run tests the boundary placement, so a bias larger than the 0.015 component budget cannot be excluded. This is the least-tested assumption.
  - Time-step error is a lesser concern. R0 has 611.87 steps per shedding period, a max Courant number of 0.73373, and the backward scheme. R1 and R2 used smaller steps (0.0086734 and 0.0075244 against 0.01) and moved Strouhal by 0.86% in total, which is a weak hint that time error is small. It is still unmeasured and will be needed later.
  - Budget: 2 of 6 experiments used and 4.07 of 12 compute units used. EXPAND_DOMAIN from R0 is the cheapest informative option at 1021 s. It is allowed for R0 but not for R2, because the R2 child would exceed the 160000-cell limit. REDUCE_TIME_STEP from R0 (1538 s) fits in the remaining budget afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on baseline-408129116207 — Domain truncation and blockage error is unmeasured for both quantities. The boundaries are the least-tested modelling assumption, and the question requires an unbounded stream. Mesh, averaging and statistics are already within budget. R0 is the cheapest parent at 1021 s, and a domain run from R2 is not allowed by the cell limit. This experiment can directly expose a bias larger than the tolerance.
  - Outcome: executed -> baseline.D2x-efba395f6c27 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both ruled out. Time and domain components are still not measured to budget for either quantity.
  - Mesh, averaging and statistics are within budget. Drag: mesh 0.01151, averaging 9.366e-05, statistics 8.229e-05. Strouhal: mesh 0.01321, averaging 1.551e-05, statistics 6.605e-05. REFINE_MESH and RUN_LONGER would add little.
  - Domain is the largest uncertainty component and is over budget. The estimate is 0.03879 for drag and 0.02615 for Strouhal, against a 0.015 component budget. The R0 to R3 change is small: drag 1.3311 to 1.3226 (0.65%) and Strouhal 0.16343 to 0.16272 (0.44%). The estimate rests on a two-level Richardson with assumed order p=1 and Fs=3, so it is not a measured convergence order.
  - The R0 to R3 domain comparison is confounded by mesh differences. R3 has representative cell size 0.79405 D against 0.45745 D for R0. R3 last wake cell is 1.9729 D against 1.0209 D for R0. R3 also has checkMesh_ok=false. Its drag CI95 is 0.00074166 and its drift is -0.0015761, with only 6 stationary cycles. The change attributed to the domain may therefore include a far-field resolution effect.
  - A further domain step from R3 (factor 1.5) gives a three-level domain sequence. That allows an observed order and a measured domain uncertainty in place of the assumed p=1 and Fs=3. It costs 1319 s, the cheapest informative option. It exposes whether the drag and Strouhal trend continues. R3 is the right parent because the continuing sequence shares R3's mesh construction.
  - Time-step error is entirely unmeasured. R0 has 611.87 steps per period, max Courant 0.73373 and the backward scheme. It is probably smaller than the domain term, but it must be measured. REDUCE_TIME_STEP from R0 (1538 s) is the next experiment after the domain run.
  - Budget: 3 of 6 experiments are used. 4.78 of 12 compute units are used. Both the domain run and the time-step run should fit.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on baseline.D2x-efba395f6c27 — Domain uncertainty is the largest component and is over budget (drag 0.03879, Strouhal 0.02615). It rests on an assumed-order two-level estimate from R0 and R3. R3 also has a coarser far-field mesh and checkMesh_ok=false. A third domain level from R3 gives an observed order and a measured domain uncertainty for both quantities. It is cheap, at 1319 s.
  - Outcome: executed -> baseline.D1.5x-ed421affd588 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both ruled out. The time component is missing for both quantities. The domain component is estimated but above budget.
  - Averaging, statistics and mesh are within budget. Drag: averaging 9.366e-05, statistics 8.229e-05, mesh 0.01151. Strouhal: averaging 1.551e-05, statistics 6.605e-05, mesh 0.01321. REFINE_MESH and RUN_LONGER would add little.
  - The domain sequence R0, R3 and R4 is now complete. Drag went 1.3311, 1.3226, 1.3194. Strouhal went 0.16343, 0.16272, 0.16243. The estimated domain uncertainty is 0.01882 for drag and 0.01591 for Strouhal, both above 0.015. The verifier notes the demonstrated change is within tolerance (0.89% drag, 0.62% Strouhal), with observed orders p=0.82 and p=0.61.
  - No further domain step is possible from R4, because the cumulative factor limit of 4.0 is reached. R2 is also disallowed by the cell limit. R3 and R4 have checkMesh_ok=false and a coarser far field than R0, so the domain estimate is confounded by mesh differences. That cannot be fixed with the remaining menu in a clean way.
  - Time-step error is entirely unmeasured. Without it the verifier cannot produce a combined uncertainty or an ACCEPT. R0 has 611.87 steps per shedding period and max Courant 0.73373. The time-step effect has not been isolated, because R1 and R2 changed mesh and time step together.
  - Budget: 4 of 6 experiments are used and 5.6 of 12 compute units are used. REDUCE_TIME_STEP from R0 is listed at 1538 s, which fits. It leaves one experiment for a possible follow-up.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on baseline-408129116207 — The time component is the only wholly unmeasured uncertainty and is required for any combined uncertainty or ACCEPT. Averaging, statistics and mesh are within budget. The domain sequence cannot be extended from R4 (cumulative factor limit). R0 is the root and the cheapest parent at 1538 s, and it isolates temporal error on an identical mesh.
  - Outcome: executed -> baseline.dt0.005-693742b868bc (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT and REJECT are both ruled out. The only blocker is the domain component for both quantities. Its combined_uncertainty is null.
  - R5 measured the time component, which was the gap last iteration. Drag went from 1.3311 (R0) to 1.3275 (R5). Strouhal went from 0.16343 to 0.16356. Time uncertainty is 0.01103 for drag and 0.003094 for Strouhal. Both are under the 0.015 component budget.
  - Mesh, averaging and statistics are also within budget. Drag: mesh 0.01151, averaging 9.366e-05, statistics 8.229e-05. Strouhal: mesh 0.01321, averaging 1.551e-05, statistics 6.605e-05. REFINE_MESH, REDUCE_TIME_STEP and RUN_LONGER on R0 would add little.
  - Domain uncertainty is above 0.015: drag 0.01882, Strouhal 0.01591. The demonstrated changes are within the 0.03 tolerance (drag 0.89%, Strouhal 0.62%). Observed orders are low (p=0.82 and p=0.61). Drag went 1.3311 (R0), 1.3226 (R3), 1.3194 (R4). Strouhal went 0.16343, 0.16272, 0.16243.
  - The R0, R3, R4 domain sequence is noisy and confounded. R3 and R4 have checkMesh_ok=false and a coarser mesh than R0 (cell size 0.79405 D and 1.1025 D against 0.45745 D). R3 drag drift is -0.0015761 and R4 drift is -0.0014782, each over 6 stationary cycles. Those drifts are comparable to the R3-to-R4 change. Mesh refinement raised both quantities (R0 to R2), so a coarser mesh can lower them independently of the domain size.
  - EXPAND_DOMAIN from R4 is not allowed (cumulative factor limit). From R2 it is not allowed (cell limit). One experiment remains, and 6.67 of 12 compute units are used. EXPAND_DOMAIN from R0 with factor 1.5 is cheap and directly targets the last blocker. It adds an intermediate domain point between R0 (30 D upstream) and R3 (60 D upstream). The point shows whether the trend is smooth or noise-dominated, and it helps bound the domain effect.
  - No experiment is certain to bring domain uncertainty under 0.015. Even so, it is the most informative remaining choice. Reporting INCONCLUSIVE without trying would leave the one affordable test unused.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on baseline-408129116207 — Domain is the only component that is still INCONCLUSIVE and over budget. R4 cannot be expanded further (cumulative factor limit) and R2 cannot be expanded (cell limit). R0 with factor 1.5 adds a cheap intermediate domain point. It fills the sequence between R0 and R3 and tests whether the trend in drag and Strouhal number is smooth or dominated by noise and mesh differences.
  - Outcome: executed -> baseline.D1.5x-c018e6157314 (completed)

Run baseline.m1.41-807cdf343a51: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run baseline.m2-476115cbbf20: REFINE_MESH from baseline.m1.41-807cdf343a51 (mesh.refinement: 1.414→2, time.delta_t: 0.008673→0.007524).
  - Observation: mean_drag_coefficient 1.3349 → 1.3356 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run baseline.D2x-efba395f6c27: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3226 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

Run baseline.D1.5x-ed421affd588: EXPAND_DOMAIN from baseline.D2x-efba395f6c27 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3226 → 1.3194 (-0.24%).
  - Observation: strouhal_number 0.16272 → 0.16243 (-0.18%).

Run baseline.dt0.005-693742b868bc: REDUCE_TIME_STEP from baseline-408129116207 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run baseline.D1.5x-c018e6157314: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3251 (-0.46%).
  - Observation: strouhal_number 0.16343 → 0.16292 (-0.31%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `baseline-408129116207` status=completed parent=None created=2026-10-19T07:00:06+00:00 wall=1442 s; record: results/runs/baseline-408129116207/run.json
- `baseline.m1.41-807cdf343a51` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=5234 s; record: results/runs/baseline.m1.41-807cdf343a51/run.json
- `baseline.m2-476115cbbf20` status=completed parent=baseline.m1.41-807cdf343a51 created=2026-10-19T09:41:41+00:00 wall=6871 s; record: results/runs/baseline.m2-476115cbbf20/run.json
- `baseline.D2x-efba395f6c27` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=3659 s; record: results/runs/baseline.D2x-efba395f6c27/run.json
- `baseline.D1.5x-ed421affd588` status=completed parent=baseline.D2x-efba395f6c27 created=2026-10-19T10:32:36+00:00 wall=2088 s; record: results/runs/baseline.D1.5x-ed421affd588/run.json
- `baseline.dt0.005-693742b868bc` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=4058 s; record: results/runs/baseline.dt0.005-693742b868bc/run.json
- `baseline.D1.5x-c018e6157314` status=completed parent=baseline-408129116207 created=2026-10-20T07:52:56+00:00 wall=1316 s; record: results/runs/baseline.D1.5x-c018e6157314/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3350610224.0, "relative_to_root": 7.304578643993896, "experiment_wall_seconds": 23225.887380456, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.61025996, "loop_wall_seconds": 1940.6719889949982}
