# Verification report: K1_central_scheme (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3404
- strouhal_number: 0.16329

## VERDICT: **INCONCLUSIVE**

Stop reason: experiment budget exhausted.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linear' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.33e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.22e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 3.61% > 1.50% but the demonstrated change 0.29% <= tau; more refinement would be needed [three-level, observed order 0.46 outside [0.5, 2.0]x formal; p=min(observed, formal)=0.46 with Fs=3]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.51% > 1.50% but the demonstrated change 0.86% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.78, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.91% <= 1.50% (root-to-finest change 0.228%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.3e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.48% <= 1.50% (root-to-finest change 0.120%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.57% > 1.50% but the demonstrated change 1.01% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.17, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.14% > 1.50% but the demonstrated change 0.59% <= tau; more refinement would be needed [three-level, observed order 2.01 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=7.04e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000133
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0361
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.5-55111cd42ba7
│   └── K1_central_scheme.m2-325af4c14f68
├── Temporal discretisation (time-step sensitivity): PASS U=0.00913
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0157
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D2x-0c7e73f08a9e

CLAIM: strouhal_number of run K1_central_scheme-e4e5fb66bdca is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mesh_quality: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── mass_conservation: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── linear_solver_convergence: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── courant_number: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── reynolds_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── force_reference_consistency: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── physics_regime: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── convection_scheme_order: PASS
│   └── K1_central_scheme-e4e5fb66bdca
├── Averaging window (reported vs stationary value): PASS U=1.32e-05
│   └── K1_central_scheme-e4e5fb66bdca
├── Temporal statistics (stationarity, cycles): PASS U=0.000122
│   └── K1_central_scheme-e4e5fb66bdca
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0151
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.m1.5-55111cd42ba7
│   └── K1_central_scheme.m2-325af4c14f68
├── Temporal discretisation (time-step sensitivity): PASS U=0.00478
│   └── K1_central_scheme-e4e5fb66bdca
│   └── K1_central_scheme.dt0.005-4f460bac38b7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0214
    └── K1_central_scheme-e4e5fb66bdca
    └── K1_central_scheme.D2x-b0a7ed20bbb5
    └── K1_central_scheme.D2x-0c7e73f08a9e

```

## EXPERIMENT HISTORY

Run K1_central_scheme-e4e5fb66bdca: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. R0 has measured averaging and statistics components only, so ACCEPT is not allowed. REJECT is also not allowed because no check has failed.
  - Mesh, time and domain uncertainties are unmeasured for both mean_drag_coefficient and strouhal_number (no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists).
  - The measured R0 uncertainties are small. For mean_drag_coefficient, averaging is 7.04e-05 and statistics is 0.0001331. For strouhal_number, averaging is 1.316e-05 and statistics is 0.000122. R0 has 12 stationary cycles, and the drag drift is -0.00013306 relative. A RUN_LONGER experiment would therefore add little.
  - R0 mesh resolution is the weakest point. It has 30580 cells and a representative cell size of 0.45745 D. The wake last cell is 1.0209 D with 111 streamwise wake cells, so the wake is coarse. Gauss linear is non-dissipative on this mesh, and the Strouhal number is sensitive to wake resolution. The mean drag is 1.3404 and the Strouhal number is 0.16329, with a Strouhal frequency resolution of 0.013333. A spatial error above 0.5*0.03 is plausible.
  - The time step is 0.01 D/U with max Courant 0.73638 and 612.39 steps per shedding period. The scheme is backward (second order), so temporal error is less likely to dominate than spatial error.
  - The domain is 30 D upstream, 50 D downstream and 40 D half-height, with a blockage ratio of 0.0125. This is moderate, so domain error is a secondary risk. EXPAND_DOMAIN is the cheapest check at 2899 s.
  - The budget is ample: 0 of 6 experiments used and 0 of 12 relative compute used. REFINE_MESH on R0 is the most informative first experiment, and the time-step and domain checks can follow.
  - Requested: REFINE_MESH {'factor': 1.5} on K1_central_scheme-e4e5fb66bdca — R0 has a coarse wake (last cell 1.0209 D, representative cell size 0.45745 D) and a non-dissipative central scheme, so spatial error is the most likely contributor to change the answer by more than the 3% tolerance, especially for Strouhal number. The mesh component is unmeasured for both quantities.
  - Outcome: executed -> K1_central_scheme.m1.5-55111cd42ba7 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. ACCEPT is not allowed, and neither is REJECT.
  - Drag: averaging (7.04e-05), statistics (0.0001331) and mesh (0.008723) all PASS. Time and domain are unmeasured, so no combined uncertainty exists.
  - Strouhal number: mesh is INCONCLUSIVE at 0.03369, above the 1.5% component budget. The demonstrated R0 to R1 change is 0.62%, with St 0.1633 on R0 and 0.16432 on R1. The two-level Richardson estimate assumes p=2 and is not a measured order.
  - R1 is a two-level comparison only. A further refinement from R0 (the menu forbids refining R1: cumulative refinement 2.12 exceeds the limit of 2.0) would give three levels and an observed order for St. This is the only component the verifier has found above budget.
  - The R0 to R1 comparison is confounded. R1 has a shorter record (end time 80, 7 stationary cycles, St frequency resolution 0.025006) and a smaller time step (0.008148 against 0.01). The time-step effect is not isolated.
  - Time and domain are unmeasured for both quantities. R0 has 612.39 steps per shedding period, Courant number 0.73638 and a second-order backward scheme. The domain is 30 D upstream, 50 D downstream and 40 D half-height, with blockage 0.0125 and symmetryPlane sides. These checks are still required before ACCEPT.
  - Budget: 1 of 6 experiments used and 1.47 of 12 compute units used. Several more experiments are affordable, so a third mesh level is the next step. The time and domain checks follow.
  - Requested: REFINE_MESH {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — The only component the verifier has found above budget is the St mesh uncertainty (0.03369 > 1.5%). It rests on a two-level estimate with an assumed order. R1 cannot be refined further because the cumulative limit would be exceeded, so a finer run from R0 is the way to get a third level and an observed order.
  - Outcome: executed -> K1_central_scheme.m2-325af4c14f68 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. ACCEPT and REJECT are both barred.
  - Averaging and statistics PASS for both quantities. Drag: 7.04e-05 and 0.0001331. St: 1.316e-05 and 0.000122.
  - Drag mesh result: R0 1.3403, R1 1.3382, R2 1.3365. The demonstrated change is 0.29%, below tau. The mesh uncertainty is 0.03614 because the observed order is 0.46, outside [0.5, 2.0] times the formal order. This order is likely contaminated: the time step also changed with the mesh (R0 0.01, R1 0.008148, R2 0.006111).
  - St mesh result: R0 0.1633, R1 0.16432, R2 0.16471. The uncertainty is 0.01506, only just above the 1.5% component budget. The observed order is p=1.78 and the demonstrated change is 0.86%. St rose monotonically with refinement.
  - No further mesh refinement is available. R1 and R2 are barred by the cumulative limit, and a refinement from R0 is capped at factor 2.0, which R2 has already used.
  - Time and domain components are still unmeasured for both quantities, so no combined uncertainty exists. Both are required before ACCEPT.
  - The domain is the likeliest unmeasured error source. The question says to treat the stream as unbounded, but R0 uses finite boundaries (30 D upstream, 50 D downstream, 40 D half-height) with a blockage ratio of 0.0125, symmetryPlane sides and a fixedValue outlet pressure. EXPAND_DOMAIN on R0 is the cheapest experiment at 2899 s.
  - The time step is a lower risk. The backward scheme is second order, with 612.39 steps per shedding period and a max Courant number of 0.73638. REDUCE_TIME_STEP should follow.
  - Budget: 2 of 6 experiments used and 4.97 of 12 compute units used. Both the domain and time experiments are affordable.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — The domain component is unmeasured for both quantities, and the question requires an unbounded-stream answer. R0 has a finite blockage of 0.0125 with symmetryPlane lateral boundaries. Mesh refinement is exhausted, and R0 is the cheapest parent at 2899 s. The near-field mesh is unchanged, so any difference from R0 isolates boundary truncation.
  - Outcome: executed -> K1_central_scheme.D2x-b0a7ed20bbb5 (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and no check has failed. ACCEPT and REJECT are both barred. The largest demonstrated change is 0.86% (St, R0 to R2), below the 3% tolerance, so there is no measured FAIL.
  - Averaging and statistics PASS for both quantities. Drag: 7.04e-05 and 0.0001331. St: 1.316e-05 and 0.000122.
  - Time is the only component with no measurement at all. The verifier reports 'no REDUCE_TIME_STEP experiment has been run' for drag and St. R0 uses dt 0.01 D/U, max Courant 0.73638 and 612.39 steps per period.
  - Time is also confounded with the mesh results. dt was 0.01 (R0), 0.008148 (R1) and 0.006111 (R2). The drag mesh order of 0.46 and the 3.61% mesh uncertainty may therefore include a time-step effect. Drag was R0 1.3403, R1 1.3382, R2 1.3365. A same-mesh dt reduction separates the two.
  - Mesh: St uncertainty is 0.01506, only just above the 1.5% component budget (p=1.78, demonstrated change 0.86%). Drag is 0.03614 (observed order 0.46). No finer mesh is allowed: R1 and R2 are barred and R0 is capped at factor 2.0, already used by R2.
  - Domain: R3 differs from R0 by 0.69% in drag (1.3311 vs 1.3403) and 0.48% in St (0.16252 vs 0.1633). The uncertainties of 0.04162 and 0.02852 come from an assumed order p=1 with Fs=3, not a measured order. R3 also has checkMesh_ok=false and a coarser mesh (representative size 0.79405 D vs 0.45745 D), so its difference from R0 is confounded with mesh. This is a second-priority gap.
  - Budget: 3 of 6 experiments used and 5.67 of 12 compute units. REDUCE_TIME_STEP on R0 costs 4367 s, which is affordable and leaves room for a domain follow-up.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on K1_central_scheme-e4e5fb66bdca — Time is the only component with no measurement for either quantity. It also confounds the mesh-order estimates for R1 and R2, whose dt differed from R0. A same-mesh dt halving on R0 (4367 s) isolates the temporal error, and is cheaper than any run from R1 or R2. Mesh refinement is exhausted, and the domain needs a follow-up from R3 afterwards.
  - Outcome: executed -> K1_central_scheme.dt0.005-4f460bac38b7 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - Verifier verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both barred. The largest demonstrated change is 0.86% (St, R0 to R2), below the 3% tolerance.
  - Averaging, statistics and time PASS for both quantities. Time now has a measurement from R4 (dt 0.005 vs 0.01 on the same mesh). Drag changes 0.228% (R0 1.3403, R4 1.3373) and St changes 0.120% (0.1633 vs 0.16349). Time uncertainty is 0.009131 for drag and 0.004782 for St.
  - Domain is now the largest unresolved component: 0.04162 for drag and 0.02852 for St, both above the 1.5% component budget. These values come from a two-level comparison (R0, R3) with an assumed order p=1 and Fs=3. The demonstrated changes are small: 0.69% for drag (1.3403 vs 1.3311) and 0.48% for St (0.1633 vs 0.16252).
  - R3 has checkMesh_ok=false and a coarser mesh (representative size 0.79405 D vs 0.45745 D for R0), so the R0-to-R3 difference mixes domain and mesh effects. A third domain level would give a measured order and replace the assumed p=1.
  - Mesh is still INCONCLUSIVE: drag 0.03614 (observed order 0.46, outside [0.5, 2.0] times formal) and St 0.01506 (p=1.78). Mesh refinement is exhausted, since R1 and R2 are barred and a refinement from R0 is capped at factor 2.0, which R2 has already used. The drag order was measured with dt changing alongside the mesh (R0 0.01, R1 0.008148, R2 0.006111). Time effects here are about 0.2%, comparable to the 0.29% mesh change.
  - Budget: 4 of 6 experiments used and 6.74 of 12 compute units. EXPAND_DOMAIN on R3 costs 3746 s, about 0.9 of the root cost (4094 s), so it is affordable. REDUCE_TIME_STEP on R1 (12074 s, about 2.9 units) is also affordable, but it targets a less-dominant uncertainty.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on K1_central_scheme.D2x-b0a7ed20bbb5 — Domain is the largest unresolved component (drag 0.04162, St 0.02852) and rests on an assumed order p=1 from only two levels (R0, R3). Expanding R3 by the same factor of 2.0 as R0-to-R3 gives three domain levels and a measured order, at a cost of 3746 s. Mesh refinement is exhausted and time is already measured.
  - Outcome: executed -> K1_central_scheme.D2x-0c7e73f08a9e (completed)

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - Verifier verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred. The largest demonstrated change is 0.86% (St, R0 to R2), below the 3% tolerance.
  - Averaging, statistics and time PASS for both quantities. Drag: averaging 7.04e-05, statistics 0.0001331, time 0.009131 (R0 to R4 change 0.228%). St: averaging 1.316e-05, statistics 0.000122, time 0.004782 (change 0.120%).
  - Domain is INCONCLUSIVE with R0, R3 and R5 as the three levels. Drag 1.3403, 1.3311, 1.327 gives 0.01569. St 0.1633, 0.16252, 0.16233 gives 0.02137. The St order of 2.01 was outside the allowed range, so p was capped at 1.00. R3 and R5 have checkMesh_ok=false and a coarser far-field mesh, so domain and mesh effects are mixed. No further expansion is possible: R5 is barred by the cumulative domain limit, and R2 by the cell limit.
  - Mesh is INCONCLUSIVE. Drag is 0.03614, with R0 1.3403, R1 1.3382, R2 1.3365, observed order 0.46 and a demonstrated change of only 0.29%. St is 0.01506, just above the 1.5% component budget, with p=1.78.
  - The drag mesh order is confounded by time step. The dt was 0.01 (R0), 0.008148 (R1) and 0.006111 (R2). R4 shows that halving dt on the R0 mesh alone moves drag by 0.228%, comparable to the 0.29% mesh change. So the poor drag order of 0.46 is probably contaminated, and the 3.61% drag mesh uncertainty may be inflated.
  - Mesh refinement from R0 is already used at factor 2.0 by R2. R1 and R2 are barred from further refinement. A time-matched pair is therefore the only way to separate the mesh effect. R4 (R0 mesh, dt 0.005) plus a new run on the R1 mesh at dt 0.005 gives a mesh-only comparison.
  - Budget: 5 of 6 experiments used and 7.66 of 12 compute units. REDUCE_TIME_STEP on R1 costs 12074 s at factor 2.0, about 2.95 units, so the total stays under 12. Only one experiment remains, so it cannot close both the mesh and domain gaps. Mesh is the one with a testable confound, and it carries the largest uncertainty, 0.03614 for drag.
  - Requested: REDUCE_TIME_STEP {'factor': 1.63} on K1_central_scheme.m1.5-55111cd42ba7 — R1 has dt 0.008148, so factor 1.63 gives dt of about 0.005, the same as R4 on the R0 mesh. R4 and the new run are then a matched-dt mesh pair, which separates the spatial error from the temporal error. This addresses the drag mesh uncertainty of 0.03614, the largest unresolved component, whose observed order of 0.46 is confounded by dt. A smaller factor than 2.0 is cheaper than the 12074 s listed for factor 2.0 and stays within the compute budget.
  - Outcome: executed -> K1_central_scheme.dt0.005-e787dcd18d0f (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 2.95, 0.69%, 1.63, 0.16%

Run K1_central_scheme.m1.5-55111cd42ba7: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→1.5, time.delta_t: 0.01→0.008148, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3382 (-0.16%).
  - Observation: strouhal_number 0.1633 → 0.16432 (+0.63%).

Run K1_central_scheme.m2-325af4c14f68: REFINE_MESH from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006111, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3365 (-0.29%).
  - Observation: strouhal_number 0.1633 → 0.16471 (+0.87%).

Run K1_central_scheme.D2x-b0a7ed20bbb5: EXPAND_DOMAIN from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3311 (-0.69%).
  - Observation: strouhal_number 0.1633 → 0.16252 (-0.47%).

Run K1_central_scheme.dt0.005-4f460bac38b7: REDUCE_TIME_STEP from K1_central_scheme-e4e5fb66bdca (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3403 → 1.3373 (-0.23%).
  - Observation: strouhal_number 0.1633 → 0.16349 (+0.12%).

Run K1_central_scheme.D2x-0c7e73f08a9e: EXPAND_DOMAIN from K1_central_scheme.D2x-b0a7ed20bbb5 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3311 → 1.327 (-0.31%).
  - Observation: strouhal_number 0.16252 → 0.16233 (-0.12%).

Run K1_central_scheme.dt0.005-e787dcd18d0f: REDUCE_TIME_STEP from K1_central_scheme.m1.5-55111cd42ba7 (time.delta_t: 0.008148→0.004999).
  - Observation: mean_drag_coefficient 1.3382 → 1.337 (-0.09%).
  - Observation: strouhal_number 0.16432 → 0.16437 (+0.03%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K1_central_scheme-e4e5fb66bdca` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=4094 s; record: results/runs/K1_central_scheme-e4e5fb66bdca/run.json
- `K1_central_scheme.m1.5-55111cd42ba7` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T03:41:28+00:00 wall=2958 s; record: results/runs/K1_central_scheme.m1.5-55111cd42ba7/run.json
- `K1_central_scheme.m2-325af4c14f68` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T04:38:25+00:00 wall=8379 s; record: results/runs/K1_central_scheme.m2-325af4c14f68/run.json
- `K1_central_scheme.D2x-b0a7ed20bbb5` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-19T16:16:09+00:00 wall=988.1 s; record: results/runs/K1_central_scheme.D2x-b0a7ed20bbb5/run.json
- `K1_central_scheme.dt0.005-4f460bac38b7` status=completed parent=K1_central_scheme-e4e5fb66bdca created=2026-10-20T03:41:02+00:00 wall=1455 s; record: results/runs/K1_central_scheme.dt0.005-4f460bac38b7/run.json
- `K1_central_scheme.D2x-0c7e73f08a9e` status=completed parent=K1_central_scheme.D2x-b0a7ed20bbb5 created=2026-10-20T04:05:21+00:00 wall=1867 s; record: results/runs/K1_central_scheme.D2x-0c7e73f08a9e/run.json
- `K1_central_scheme.dt0.005-e787dcd18d0f` status=completed parent=K1_central_scheme.m1.5-55111cd42ba7 created=2026-10-20T08:02:13+00:00 wall=5214 s; record: results/runs/K1_central_scheme.dt0.005-e787dcd18d0f/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 4613957056.0, "relative_to_root": 10.058768380204928, "experiment_wall_seconds": 20861.432444201, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.57144399, "loop_wall_seconds": 20887.264987623}
