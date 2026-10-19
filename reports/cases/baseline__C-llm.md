# Verification report: baseline (C-llm)

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
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.86% <= 1.50% (root-to-finest change 0.284%) [three-level, observed order inf outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.33% <= 1.50% (root-to-finest change 0.866%) [three-level Celik procedure, observed order p=2.39, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.10% <= 1.50% (root-to-finest change 0.276%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 8.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.31% <= 1.50% (root-to-finest change 0.077%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.6e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.74% > 1.50% but the demonstrated change 1.01% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.94, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.85% > 1.50% but the demonstrated change 0.59% <= tau; more refinement would be needed [oscillatory convergence (sign(eps32/eps21)<0); range-based U with Fs=3]

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
├── Spatial discretisation (mesh sensitivity): PASS U=0.00858
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-93c9ab8d6f2d
├── Temporal discretisation (time-step sensitivity): PASS U=0.011
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0174
    └── baseline-408129116207
    └── baseline.D2x-efba395f6c27
    └── baseline.D1.5x-ed421affd588
    └── baseline.D2x-4312d7d8fec3

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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0133
│   └── baseline-408129116207
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-93c9ab8d6f2d
├── Temporal discretisation (time-step sensitivity): PASS U=0.00309
│   └── baseline-408129116207
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0185
    └── baseline-408129116207
    └── baseline.D2x-efba395f6c27
    └── baseline.D1.5x-ed421affd588
    └── baseline.D2x-4312d7d8fec3

```

## EXPERIMENT HISTORY

Run baseline-408129116207: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is not justified either.
  - Mesh, time and domain uncertainty components are all unmeasured for both requested quantities, so no combined uncertainty exists.
  - The averaging and statistics components are small and PASS. Drag: averaging 9.366e-05, statistics 8.229e-05. Strouhal: averaging 1.551e-05, statistics 6.605e-05. R0 has 12 stationary cycles. Running longer would not reduce the dominant unknowns.
  - R0 mesh is coarse: 30580 cells, representative_cell_size_D 0.45745, wake_last_cell_D 1.0209. These are the most likely source of a spatial error larger than 3% in drag and Strouhal number, because wake and shear-layer resolution drive both.
  - R0 time step is 0.01 convective units with 611.87 steps per shedding period, max Courant 0.73373, and a second-order backward scheme. Temporal error is likely less important than spatial error.
  - R0 domain extents are 30 D upstream, 50 D downstream and 40 D half-height, with a blockage ratio of 0.0125. These are fairly generous, so domain error is less likely to be the largest unknown.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 compute units used. A mesh refinement costs about 1779 s, against 1441.6 s for the root run.
  - Requested: REFINE_MESH {'factor': 2.0} on baseline-408129116207 — Mesh resolution is the most likely unmeasured error source that could shift mean Cd or St by more than the 3% tolerance. R0 is a single coarse mesh with 30580 cells and a representative cell size of 0.45745 D, so its mesh error is entirely unquantified. The largest factor gives the clearest signal above the very small statistical noise, which is about 1e-4.
  - Outcome: executed -> baseline.m2-93c9ab8d6f2d (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed and REJECT is not justified.
  - Mesh, R0 vs R1: mean Cd changed from 1.3311 to 1.3349 in the stationary windows (root-to-finest change 0.284%, mesh uncertainty 0.01137, PASS). St changed from 0.16343 to 0.16486 (change 0.87%). The mesh uncertainty for St is 0.03464, above 0.5*tolerance, so the mesh check is INCONCLUSIVE.
  - The St mesh uncertainty cannot be reduced by more refinement. R1 cannot be refined further because cumulative refinement 2.83 exceeds the limit of 2.0. R0 to a factor of at most 2.0 has already been done as R1.
  - Time and domain components are unmeasured for both quantities, so no combined uncertainty exists. No REDUCE_TIME_STEP or EXPAND_DOMAIN run exists.
  - Averaging and statistics are negligible. Cd: 9.366e-05 and 8.229e-05. St: 1.551e-05 and 6.605e-05. R0 has 12 stationary cycles and R1 has 7. RUN_LONGER would not address any open component.
  - Time step is probably not the dominant risk. R0 has 611.87 steps per shedding period, max Courant 0.73373 and a backward (second-order) scheme. R0 time step is 0.01 convective units.
  - Domain is the least characterised error source. R0 uses lateral symmetryPlane boundaries at 40 D half-height, 30 D upstream, 50 D downstream, blockage 0.0125, inlet pressure zeroGradient and outlet fixedValue. The question asks for an unbounded stream, and St appears sensitive at the 1-3% level (mesh change 0.87%). A domain error is therefore plausible at the budget level of 1.5%.
  - EXPAND_DOMAIN on R0 is the cheapest experiment (1021 s) and is allowed. It cannot be run from R1, whose child mesh would have 162400 cells against a limit of 160000. Budget: 1 of 6 experiments used and 3.48 of 12 compute units used.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on baseline-408129116207 — Domain truncation and blockage error is unmeasured for both quantities and is a plausible source of a shift above 1.5%. The question requires an unbounded stream, and the R0 domain uses symmetry lateral boundaries and a zeroGradient inlet pressure. Mesh refinement is exhausted (R1 is at the cumulative limit). EXPAND_DOMAIN on R0 is the cheapest allowed experiment (1021 s) and keeps the near-field mesh unchanged, so the comparison isolates the boundary effect. R1 cannot be the parent because the child mesh would exceed 160000 cells.
  - Outcome: executed -> baseline.D2x-efba395f6c27 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. A REJECT is not justified, because no measured change exceeds the 0.03 tolerance.
  - Time is unmeasured for both quantities. No REDUCE_TIME_STEP run exists, so time is listed as a missing uncertainty component for mean_drag_coefficient and strouhal_number. The 0.03 tolerance cannot be assessed without it.
  - R0 time step is 0.01 convective units, with 611.87 steps per shedding period and max Courant 0.73373. R0 uses a second-order backward scheme, but the time error has not been measured. A REDUCE_TIME_STEP run on R0 costs 1538 s.
  - Mesh, R0 vs R1: Cd 1.3311 to 1.3349 (change 0.284%, mesh uncertainty 0.01137, PASS). St 0.16343 to 0.16486 (change 0.87%, uncertainty 0.03464, INCONCLUSIVE). The St mesh component cannot be tightened with a further REFINE_MESH from R1, which is not allowed because cumulative refinement 2.83 exceeds 2.0.
  - Domain, R0 vs R2: Cd 1.3311 to 1.3226 (change 0.65%) and St 0.16343 to 0.16272 (change 0.44%). The estimated uncertainties are 0.03879 for Cd and 0.02615 for St, both INCONCLUSIVE. The demonstrated changes are below the 0.03 tolerance, so a domain-driven failure is less likely than an unmeasured time error.
  - R2 is a weak domain comparison. Its checkMesh_ok is false and its mesh is coarser than R0: representative_cell_size_D 0.79405 against 0.45745, and wake_last_cell_D 1.9729 against 1.0209. R2 also has only 6 stationary cycles, with Cd drift -0.0015761 and ci95 0.00074166. The domain change is therefore confounded with mesh coarsening and noise.
  - Averaging and statistics are negligible for both quantities. Cd: 9.366e-05 and 8.229e-05. St: 1.551e-05 and 6.605e-05. RUN_LONGER would not address any open component.
  - Budget is sufficient: 2 of 6 experiments and 4.19 of 12 compute units used. REDUCE_TIME_STEP on R0 is the cheapest way to fill a fully unmeasured component, and an EXPAND_DOMAIN run from R2 (1319 s) can follow.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on baseline-408129116207 — Time is the only uncertainty component still entirely unmeasured for both quantities, and the 0.03 tolerance cannot be assessed without it. Running on R0 keeps the mesh and domain identical, so the comparison isolates temporal error. R0 is cheap (1538 s) and has 12 stationary cycles with very small statistical noise. R1 costs 10029 s and R2 is confounded by its failed checkMesh.
  - Outcome: executed -> baseline.dt0.005-693742b868bc (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not justified, because no demonstrated change exceeds the 0.03 tolerance.
  - Time is now measured (R0 vs R3). Cd stationary changed from 1.3311 to 1.3275 (change 0.276%, uncertainty 0.01103, PASS). St changed from 0.16343 to 0.16356 (change 0.077%, uncertainty 0.003094, PASS).
  - Mesh (R0 vs R1): Cd changed from 1.3311 to 1.3349 (change 0.284%, uncertainty 0.01137, PASS). St changed from 0.16343 to 0.16486 (change 0.87%, uncertainty 0.03464 > 0.5*tolerance, INCONCLUSIVE).
  - Domain (R0 vs R2) is INCONCLUSIVE for both quantities. Cd changed from 1.3311 to 1.3226 (change 0.65%, uncertainty 0.03879). St changed from 0.16343 to 0.16272 (change 0.44%, uncertainty 0.02615). The estimates rest on a two-level Richardson with assumed order p=1.
  - The domain component is the main open item for both quantities. Cd cannot reach a combined uncertainty without it, and St also needs it. The Cd domain uncertainty of 0.03879 alone exceeds the 0.03 tolerance.
  - R2 is a weak domain comparison. Its checkMesh_ok is false. Its mesh is coarser than R0 (representative_cell_size_D 0.79405 vs 0.45745, wake_last_cell_D 1.9729 vs 1.0209). It has only 6 stationary cycles with Cd drift_rel -0.0015761 and ci95 0.00074166. The R0-to-R2 change is therefore confounded with mesh and noise, and a measured order from a third domain level is needed.
  - Averaging and statistics are negligible. Cd: 9.366e-05 and 8.229e-05. St: 1.551e-05 and 6.605e-05. RUN_LONGER on R0 would not address any open component.
  - A REFINE_MESH on R0 at a factor below 2.0 could give an intermediate mesh level for the St mesh estimate. It does not help Cd and does not clear the domain blocker that affects both quantities, so it is lower priority now.
  - Budget: 3 of 6 experiments and 5.25 of 12 compute units used. EXPAND_DOMAIN from R2 costs 1319 s, about 0.91 root units, which is affordable.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on baseline.D2x-efba395f6c27 — Domain uncertainty is INCONCLUSIVE for both Cd (0.03879) and St (0.02615), and it blocks any combined uncertainty. The R0-to-R2 comparison is confounded by R2's coarser mesh and failed checkMesh, and it rests on an assumed order. Expanding from R2 extends the R0, R2 family to a third level with the largest lever arm. That lets the domain order be measured. It costs about 1319 s, so the total stays well inside the 12-unit compute budget.
  - Outcome: executed -> baseline.D2x-4312d7d8fec3 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 0.91

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not justified, because no demonstrated change exceeds the 0.03 tolerance.
  - Two components are still open. Cd domain is 0.0181, above 0.5*tolerance, and the check is INCONCLUSIVE. St mesh is 0.03464, above 0.5*tolerance, and the check is INCONCLUSIVE. combined_uncertainty is null for both quantities.
  - Cd domain (R0, R2, R4): stationary Cd goes 1.3311, 1.3226, 1.3179, with a root-to-finest change of 1.01%. The observed order is p=0.86, which is slow convergence, so the Celik estimate is 1.81%. R4 cannot be expanded further because the cumulative domain factor would exceed 4.0. R2 and R4 have checkMesh_ok false, with coarser meshes (representative_cell_size_D 0.79405 and 1.397 against 0.45745 for R0), so the domain change is confounded with mesh coarsening. A further domain run would add little, and the Cd domain component may stay open.
  - St mesh (R0, R1): St goes 0.16343 to 0.16486, a change of 0.87%. The estimate of 0.03464 uses an assumed order p=2 and Fs=3 on only two levels. R1 cannot be refined further because cumulative refinement 2.83 exceeds 2.0. REFINE_MESH on R0 with an intermediate factor of 1.4142 gives a third mesh level between R0 and R1. That allows a measured order and the three-level Fs=1.25 procedure, which is the only route in the menu that can clear the St mesh component.
  - Time (R0, R3) is measured and passes. Cd uncertainty is 0.01103 and St uncertainty is 0.003094. Averaging and statistics are negligible for both quantities (Cd 9.366e-05 and 8.229e-05, St 1.551e-05 and 6.605e-05), so RUN_LONGER would not address any open component.
  - The R0 parent costs 1779 s. Budget is 4 of 6 experiments and 6.17 of 12 compute units used, so the run is affordable.
  - Requested: REFINE_MESH {'factor': 1.4142} on baseline-408129116207 — St mesh is the open component that a menu experiment can resolve. The existing estimate of 0.03464 rests on two levels and an assumed order. An intermediate mesh from R0 at factor 1.4142 gives a geometrically consistent three-level sequence with R1 (cell-size ratios of about 1.414 each) and a measured order. The Cd domain component cannot be improved by expansion beyond R4. A further domain run from R2 would add less information.
  - Outcome: executed -> baseline.m1.41-807cdf343a51 (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified. No demonstrated change exceeds the 0.03 tolerance.
  - The Strouhal number is now ACCEPT with combined uncertainty 0.01603. R5 supplied the third mesh level: mesh uncertainty 0.01335 with observed order p=2.39. Every St component is within 0.5*tolerance.
  - Mean Cd has one open component. Domain uncertainty is 0.0181, above 0.5*tolerance (0.015), and the check is INCONCLUSIVE. combined_uncertainty is null.
  - The other Cd components pass. Averaging 9.366e-05, statistics 8.229e-05, mesh 0.008577 (R0, R5, R1), time 0.01103 (R0, R3).
  - Domain sequence R0, R2, R4 gives stationary Cd 1.3311, 1.3226, 1.3179. The root-to-finest change is 1.01%. The observed order is slow (p=0.86), which drives the 1.81% Celik estimate.
  - R2 and R4 have checkMesh_ok false and coarser meshes (representative_cell_size_D 0.79405 and 1.397 against 0.45745 for R0). R2 and R4 have only 6 cycles, with Cd ci95 0.00074166 and 0.00073239. The domain trend is therefore confounded with mesh coarsening and noise. The measured order may be unreliable.
  - R4 cannot be expanded further (cumulative domain factor limit 4.0). R1 cannot be refined or expanded. RUN_LONGER does not address the domain component, because statistical noise is already far below the domain signal. REFINE_MESH and REDUCE_TIME_STEP target components that already pass for Cd.
  - Budget: 5 of 6 experiments used and 7.4 of 12 compute units used. One experiment remains. EXPAND_DOMAIN from R2 costs 1319 s, about 0.91 root units, and is affordable.
  - Only one experiment remains and it may not be enough to clear Cd domain. The slow measured order means the estimate may stay above 1.5%, and the final outcome could be INCONCLUSIVE.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on baseline.D2x-efba395f6c27 — Cd domain is the only open component for the only unresolved quantity. R4 is at the cumulative limit, so no further expansion is possible beyond it. Expanding R2 by 1.5 (domain 3x R0) adds a fourth domain level between R2 and R4. This tests whether the slow observed order (p=0.86) is real or an artefact of the three-level fit with coarse far-field meshes. It is the cheapest informative option (1319 s, about 0.91 root units) and stays within the 12-unit budget.
  - Outcome: executed -> baseline.D1.5x-ed421affd588 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.91, 0.91

Run baseline.m2-93c9ab8d6f2d: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.29%).
  - Observation: strouhal_number 0.16343 → 0.16486 (+0.87%).

Run baseline.D2x-efba395f6c27: EXPAND_DOMAIN from baseline-408129116207 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3226 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

Run baseline.dt0.005-693742b868bc: REDUCE_TIME_STEP from baseline-408129116207 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run baseline.D2x-4312d7d8fec3: EXPAND_DOMAIN from baseline.D2x-efba395f6c27 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3226 → 1.3179 (-0.36%).
  - Observation: strouhal_number 0.16272 → 0.16248 (-0.15%).

Run baseline.m1.41-807cdf343a51: REFINE_MESH from baseline-408129116207 (averaging.start_time: 75→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run baseline.D1.5x-ed421affd588: EXPAND_DOMAIN from baseline.D2x-efba395f6c27 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3226 → 1.3194 (-0.24%).
  - Observation: strouhal_number 0.16272 → 0.16243 (-0.18%).

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
- `baseline.m2-93c9ab8d6f2d` status=completed parent=baseline-408129116207 created=2026-10-19T07:38:06+00:00 wall=9774 s; record: results/runs/baseline.m2-93c9ab8d6f2d/run.json
- `baseline.D2x-efba395f6c27` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=3659 s; record: results/runs/baseline.D2x-efba395f6c27/run.json
- `baseline.dt0.005-693742b868bc` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=4058 s; record: results/runs/baseline.dt0.005-693742b868bc/run.json
- `baseline.D2x-4312d7d8fec3` status=completed parent=baseline.D2x-efba395f6c27 created=2026-10-19T09:15:09+00:00 wall=3214 s; record: results/runs/baseline.D2x-4312d7d8fec3/run.json
- `baseline.m1.41-807cdf343a51` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=5234 s; record: results/runs/baseline.m1.41-807cdf343a51/run.json
- `baseline.D1.5x-ed421affd588` status=completed parent=baseline.D2x-efba395f6c27 created=2026-10-19T10:32:36+00:00 wall=2088 s; record: results/runs/baseline.D1.5x-ed421affd588/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3774510064.0, "relative_to_root": 8.228711715718335, "experiment_wall_seconds": 28027.630013498, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.602997625, "loop_wall_seconds": 15550.257513706}
