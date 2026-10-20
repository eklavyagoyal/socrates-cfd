# Verification report: E1_noslip_side_walls (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3403
- strouhal_number: 0.16429

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
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 9.70e-04 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.15% <= 1.50% (root-to-finest change 0.761%) [three-level Celik procedure, observed order p=2.49, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.20% > 1.50% but the demonstrated change 1.23% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.70, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.83% <= 1.50% (root-to-finest change 0.209%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-03)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.55% <= 1.50% (root-to-finest change 0.137%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.7e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 2.84% > 1.50% but the demonstrated change 1.62% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=0.92, Fs=1.25]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 3.34% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level, observed order 3.21 outside [0.5, 2.0]x formal; p=min(observed, formal)=1.00 with Fs=3]

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
├── Spatial discretisation (mesh sensitivity): PASS U=0.0115
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.5-d5d24400570b
│   └── E1_noslip_side_walls.m2-39a4571e43e5
├── Temporal discretisation (time-step sensitivity): PASS U=0.00834
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0284
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D1.5x-c6109b1680cd
    └── E1_noslip_side_walls.D2x-6e1f5c2d9088

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
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.022
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.m1.5-d5d24400570b
│   └── E1_noslip_side_walls.m2-39a4571e43e5
├── Temporal discretisation (time-step sensitivity): PASS U=0.00547
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0334
    └── E1_noslip_side_walls-88a7cd5812e8
    └── E1_noslip_side_walls.D2x-1620b1098386
    └── E1_noslip_side_walls.D1.5x-c6109b1680cd
    └── E1_noslip_side_walls.D2x-6e1f5c2d9088

```

## EXPERIMENT HISTORY

Run E1_noslip_side_walls-88a7cd5812e8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. REJECT is also not allowed because nothing has failed.
  - R0 passes the sampling checks. The averaging bias is 9.319e-05 for Cd and 6.507e-05 for St. The statistical uncertainty is 0.001199 for Cd and 0.0009705 for St, against a tolerance of 0.03. The record has 13 stationary cycles.
  - Mesh, time and domain uncertainties are all unmeasured for both quantities. No refinement, time-step or domain experiment has been run.
  - R0 mesh is coarse for the wake. It has 30580 cells, a representative cell size of 0.45745 D and a wake last cell of 1.0209 D. It has 160 cells around the cylinder and a wall first cell of 0.005 D. The wake is resolved by only 111 streamwise cells, and the wake sets St and the mean drag. This is the most likely source of an error larger than 3%.
  - Time and domain look less likely to dominate. The time scheme is backward, with dt = 0.01 D/U, max Courant 0.73374 and 608.73 steps per shedding period. The domain is 30 D upstream, 50 D downstream and 40 D half-height, with blockage 0.0125. The lateral boundaries are noSlipWall rather than a free-stream condition, so domain error is still unmeasured and should be tested later.
  - A refinement of R0 is the most informative single experiment. R0 has no refinement family yet, so the parent is R0. Factor 1.5 gives a signal clearly above noise. The estimated cost is about 2284 s at the default factor, which is well within the budget of 12 times the root cost (1850.8 s).
  - Requested: REFINE_MESH {'factor': 1.5} on E1_noslip_side_walls-88a7cd5812e8 — Mesh error is unmeasured and the most likely source of a change larger than the 3% tolerance, because the R0 wake mesh is coarse. Domain and time-step effects are also unmeasured but look less likely to dominate.
  - Outcome: executed -> E1_noslip_side_walls.m1.5-d5d24400570b (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred, so the decision is MORE_EVIDENCE.
  - R0 sampling is adequate. It has 13 stationary cycles, Cd statistical uncertainty 0.001199 and St statistical uncertainty 0.0009705. The averaging bias is 9.319e-05 for Cd and 6.507e-05 for St. Both are far below the 0.03 tolerance.
  - The R0 to R1 mesh refinement is done. Cd moved from 1.3402 to 1.3482 (0.59%). St moved from 0.16428 to 0.16575 (0.89%). Both changes are below the 3% tolerance, so there is no FAIL.
  - The mesh component is still INCONCLUSIVE. The two-level Richardson estimate with assumed p=2 gives 3.18% for Cd and 4.79% for St, both above the 1.5% half-tolerance. A third level could reduce this, but R1 cannot be refined further (cumulative refinement 2.12 exceeds the limit of 2.0).
  - Time uncertainty is unmeasured. R0 has dt = 0.01 D/U, max Courant 0.73374 and 608.73 steps per period with a backward scheme, and R1 has 737.81 steps per period. There is no evidence of a problem, but there is no measurement either.
  - Domain uncertainty is unmeasured and is the least defended setting. The lateral boundaries are noSlipWall at 40 D half-height, with 30 D upstream and 50 D downstream. The inlet pressure is zeroGradient and the outlet pressure is fixedValue. The question requires an unbounded stream. Wall-bounded lateral boundaries are a physical constraint, not a numerical one, so they could shift Cd and St beyond tolerance regardless of mesh and time-step convergence.
  - EXPAND_DOMAIN on R0 is the cheapest experiment (1311 s estimated) and the one most likely to expose a flaw larger than the tolerance. Budget is ample: 1 of 6 experiments used and 1.47 of 12 compute units used. Using R0 as parent keeps the near-field mesh identical, so the comparison isolates the boundary effect.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Domain truncation is unmeasured and is the least defended setting: noSlipWall lateral boundaries conflict with the 'unbounded' requirement. It is also the cheapest experiment (1311 s). Mesh has already shown a sub-tolerance change (0.59% Cd, 0.89% St), whereas the domain effect has no measurement at all.
  - Outcome: executed -> E1_noslip_side_walls.D2x-1620b1098386 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred, so the decision is MORE_EVIDENCE.
  - R0 sampling is adequate. It has 13 stationary cycles, a Cd statistical uncertainty of 0.001199 and an St statistical uncertainty of 0.0009705. Averaging bias is 9.319e-05 for Cd and 6.507e-05 for St.
  - Mesh: R0 to R1 moved Cd from 1.3402 to 1.3482 (0.59%) and St from 0.16428 to 0.16575 (0.89%). The assumed-p=2 Richardson uncertainty is 0.03184 for Cd and 0.04788 for St, both above the 0.015 half-tolerance. R1 cannot be refined further (cumulative refinement limit).
  - Domain: R2 (60 D upstream, 100 D downstream, 80 D half-height) gave Cd 1.3259 and St 0.16301, against R0 Cd 1.3402 and St 0.16428. The changes are 1.08% for Cd and 0.78% for St. The domain uncertainty is 0.0647 for Cd and 0.04674 for St, the largest Cd component. It rests on an assumed order p=1 and only two levels.
  - R2 is a weak comparison. checkMesh_ok is false for R2, its far-field mesh is coarser (representative cell size 0.79405 D, wake last cell 1.9729 D) and it has only 6 stationary cycles with the stationary window start at the MSER cap. The domain signal is therefore partly confounded with mesh quality. The cause of the checkMesh failure is not in the package.
  - Time: no REDUCE_TIME_STEP run exists, so the temporal component is unmeasured. R0 has dt = 0.01 D/U, max Courant 0.73374 and 608.73 steps per period. There is no sign of a problem, but absence of evidence is not a pass.
  - Next experiment: EXPAND_DOMAIN on R2 with factor 1.5, which costs 1694 s. It gives a third domain level with a measured order, instead of an assumed p=1, and tests whether the 1.08% Cd shift continues beyond R2 or has saturated. The domain term is currently the largest Cd component. Budget is ample: 2 of 6 experiments and 2.18 of 12 compute units used. Mesh convergence order and time step stay queued as later experiments.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on E1_noslip_side_walls.D2x-1620b1098386 — The domain component is the largest Cd uncertainty (0.0647) and rests on two levels with an assumed order p=1. R2 also has checkMesh_ok false and only 6 cycles. A further expansion from R2 gives a third level, so the order can be measured, and it checks whether the 1.08% Cd and 0.78% St shifts have converged. It is cheap at 1694 s.
  - Outcome: executed -> E1_noslip_side_walls.D1.5x-c6109b1680cd (completed)

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred, so the decision is MORE_EVIDENCE.
  - R0 sampling passes. It has 13 stationary cycles, a Cd statistical uncertainty of 0.001199 and an St statistical uncertainty of 0.0009705. The averaging bias is 9.319e-05 for Cd and 6.507e-05 for St. These are far below the 0.03 tolerance.
  - Mesh is now the largest unresolved component. R0 to R1 moved Cd from 1.3402 to 1.3482 and St from 0.16428 to 0.16575. The two-level Richardson estimate uses an assumed p=2 and gives 0.03184 for Cd and 0.04788 for St. Both exceed the 0.015 half-tolerance. R1 cannot be refined further (cumulative refinement 2.12 exceeds the limit of 2.0). A measured order needs a third level built from R0.
  - Domain has three levels. Cd goes R0 1.3402, R2 1.3259, R3 1.3213. St goes R0 0.16428, R2 0.16301, R3 0.16259. The Celik estimate with observed order p=1.07 gives 0.02602 for Cd, and with p=1.03 gives 0.0192 for St. Both are above 0.015. R3 cannot be expanded further (cumulative domain factor limit 4.0). More domain runs are therefore not available. R2 and R3 also have checkMesh_ok false, and their far-field cells are coarser, so part of the domain signal may be a mesh artefact. The cause is not in the package.
  - Time is entirely unmeasured. R0 uses dt = 0.01 D/U, max Courant 0.73374 and 608.73 steps per period. R1 used dt = 0.0081772 D/U, because the time step was reduced for the Courant limit. The R0 to R1 mesh signal is therefore partly confounded with a time-step change. The time component is required for ACCEPT and is currently missing.
  - Budget remains: 3 of 6 experiments and 3.0 of 12 compute units are used. A third mesh level on R0 is the most informative next step. It targets the largest uncertainty, St 0.04788, and replaces the assumed order with a measured one. A REDUCE_TIME_STEP run on R0 should follow, so that both the time and mesh components get measured.
  - Requested: REFINE_MESH {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — Mesh has the largest uncertainty for both quantities (Cd 0.03184, St 0.04788) and rests on two levels with an assumed order. R1 cannot be refined further, so a finer level must be built from R0. A factor of 2.0 gives a clearly separated third level and a measured order. It stays within the cumulative refinement limit of 2.0.
  - Outcome: executed -> E1_noslip_side_walls.m2-39a4571e43e5 (completed)

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred, so the decision is MORE_EVIDENCE.
  - R0 sampling passes. It has 13 stationary cycles. The Cd statistical uncertainty is 0.001199 and the St statistical uncertainty is 0.0009705. The averaging bias is 9.319e-05 for Cd and 6.507e-05 for St.
  - Mesh for Cd passes (R0, R1, R4): uncertainty 0.01155 with measured order p=2.49. Cd went 1.3402 (R0), 1.3482 (R1), 1.3505 (R4). Mesh for St is INCONCLUSIVE at 0.02202 with p=1.70. St went 0.16428, 0.16575, 0.16632. The root-to-finest change in St is 1.23%, below the 3% tolerance. R4 cannot be refined further, so the menu cannot reduce this component directly.
  - Domain is INCONCLUSIVE: Cd 0.02602 (p=1.07) and St 0.0192 (p=1.03). Cd went 1.3402 (R0), 1.3259 (R2), 1.3213 (R3). St went 0.16428, 0.16301, 0.16259. The R2-to-R3 steps (0.35% for Cd, 0.26% for St) are smaller than R0-to-R2, so the effect is shrinking. R3 is at the cumulative domain factor limit (4.0), so no further expansion is possible. R2 and R3 have checkMesh_ok false and a coarser far field, which may confound this estimate. The cause of the checkMesh failure is not in the package.
  - Time is still completely unmeasured for both quantities. No REDUCE_TIME_STEP run exists, and the verifier lists time as missing for Cd and St. R0 uses dt=0.01 D/U, max Courant 0.73374 and 608.73 steps per period. The refined runs used smaller steps: R1 dt=0.0081772 and R4 dt=0.0061329. The mesh signal is therefore partly confounded with the time step. ACCEPT is impossible without this component.
  - The time step is the only component that can still be measured cheaply on the root mesh. REDUCE_TIME_STEP on R0 costs 1974 s. It also shows how much of the R0-to-R1/R4 change came from the smaller time step. Budget: 4 of 6 experiments are used and 6.48 of 12.0 compute units, so this fits.
  - Domain and St mesh uncertainties may still exceed the 0.015 half-tolerance after the time run. If so, the final report will likely be INCONCLUSIVE rather than ACCEPT. That is the honest outcome, not a reason to skip the missing time measurement.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on E1_noslip_side_walls-88a7cd5812e8 — The time component is the only one still entirely unmeasured. It blocks ACCEPT for both quantities. Mesh and domain have been tested as far as the menu allows. R0 is the cheapest parent (1974 s) and keeps the mesh and domain identical, so the comparison isolates temporal error. It also separates the time-step effect from the mesh effect seen in R1 and R4, which used smaller time steps.
  - Outcome: executed -> E1_noslip_side_walls.dt0.005-c41af2c90410 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 0.35%, 0.26%

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT and REJECT are both barred, so the decision is MORE_EVIDENCE.
  - R0 sampling passes. It has 13 stationary cycles. Cd statistical uncertainty is 0.001199 and St is 0.0009705. Averaging bias is 9.319e-05 for Cd and 6.507e-05 for St.
  - Time now passes. R5 (dt 0.005) gave Cd 1.3374 and St 0.1645, against R0 Cd 1.3402 and St 0.16428. Time uncertainty is 0.008342 for Cd and 0.005466 for St, both below 0.015.
  - Cd mesh passes at 0.01155 (p=2.49, R0/R1/R4). St mesh is INCONCLUSIVE at 0.02202 (p=1.70). R1 and R4 cannot be refined further, so the menu cannot directly lower the St mesh term. R1 and R4 also used smaller time steps than R0 (0.0081772 and 0.0061329), so their mesh signal is partly confounded with time step.
  - Domain is the largest remaining term for both quantities: Cd 0.02602 (p=1.07) and St 0.0192 (p=1.03), both above 0.015. Cd runs R0 1.3402, R2 1.3259, R3 1.3213. St runs R0 0.16428, R2 0.16301, R3 0.16259. Blockage falls 0.0125, 0.00625, 0.0041667. The trend is monotone and the steps shrink (R2 to R3 is smaller than R0 to R2), but it has not been shown to saturate.
  - R3 cannot be expanded further. R2 can: EXPAND_DOMAIN on R2 with factor 2.0 gives a cumulative factor of 4.0, which is at the limit, not above it. Estimated cost is 1694 s. That is the last experiment (6 of 6) and keeps compute within the 12.0 cap (7.55 used).
  - A fourth domain level (R2, R3, new) lets the verifier fit the domain order on the three largest domains, where the changes should be smallest. It targets the one term that blocks both Cd and St. REFINE_MESH on R5 costs 3962 s and would give only a two-level comparison, so it is less informative.
  - Caveat: R2 and R3 have checkMesh_ok false and a coarser far field (cell size 0.79405 D and 1.1025 D). The cause is not in the package, so part of the domain signal could be a mesh artefact. The new run inherits that risk. Even if the domain term falls, the St mesh term (0.02202) may still keep the final result INCONCLUSIVE.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on E1_noslip_side_walls.D2x-1620b1098386 — Domain is the largest remaining uncertainty for both quantities (Cd 0.02602, St 0.0192) and the only one the menu can still reduce. R3 is at the cumulative limit, but R2 with factor 2.0 reaches exactly 4.0 and is allowed. It gives a fourth domain level that tests whether the shrinking Cd and St shifts have saturated. Cost is about 1694 s, within budget.
  - Outcome: executed -> E1_noslip_side_walls.D2x-6e1f5c2d9088 (completed)

Run E1_noslip_side_walls.m1.5-d5d24400570b: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→1.5, time.delta_t: 0.01→0.008177, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3482 (+0.59%).
  - Observation: strouhal_number 0.16428 → 0.16575 (+0.90%).

Run E1_noslip_side_walls.D2x-1620b1098386: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3259 (-1.07%).
  - Observation: strouhal_number 0.16428 → 0.16301 (-0.77%).

Run E1_noslip_side_walls.D1.5x-c6109b1680cd: EXPAND_DOMAIN from E1_noslip_side_walls.D2x-1620b1098386 (domain.downstream: 100→150, domain.half_height: 80→120, domain.upstream: 60→90, mesh.n_downstream: 145→165, mesh.n_lateral: 55→61, mesh.n_upstream: 43→48).
  - Observation: mean_drag_coefficient 1.3259 → 1.3213 (-0.35%).
  - Observation: strouhal_number 0.16301 → 0.16259 (-0.25%).

Run E1_noslip_side_walls.m2-39a4571e43e5: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, mesh.refinement: 1→2, time.delta_t: 0.01→0.006133, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3505 (+0.77%).
  - Observation: strouhal_number 0.16428 → 0.16632 (+1.24%).

Run E1_noslip_side_walls.dt0.005-c41af2c90410: REDUCE_TIME_STEP from E1_noslip_side_walls-88a7cd5812e8 (averaging.start_time: 75→40, time.delta_t: 0.01→0.005, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3402 → 1.3374 (-0.21%).
  - Observation: strouhal_number 0.16428 → 0.1645 (+0.14%).

Run E1_noslip_side_walls.D2x-6e1f5c2d9088: EXPAND_DOMAIN from E1_noslip_side_walls.D2x-1620b1098386 (domain.downstream: 100→200, domain.half_height: 80→160, domain.upstream: 60→120, mesh.n_downstream: 145→180, mesh.n_lateral: 55→65, mesh.n_upstream: 43→51).
  - Observation: mean_drag_coefficient 1.3259 → 1.3188 (-0.54%).
  - Observation: strouhal_number 0.16301 → 0.16256 (-0.27%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `E1_noslip_side_walls-88a7cd5812e8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1851 s; record: results/runs/E1_noslip_side_walls-88a7cd5812e8/run.json
- `E1_noslip_side_walls.m1.5-d5d24400570b` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T07:50:45+00:00 wall=3718 s; record: results/runs/E1_noslip_side_walls.m1.5-d5d24400570b/run.json
- `E1_noslip_side_walls.D2x-1620b1098386` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T20:14:34+00:00 wall=1058 s; record: results/runs/E1_noslip_side_walls.D2x-1620b1098386/run.json
- `E1_noslip_side_walls.D1.5x-c6109b1680cd` status=completed parent=E1_noslip_side_walls.D2x-1620b1098386 created=2026-10-20T10:16:56+00:00 wall=1783 s; record: results/runs/E1_noslip_side_walls.D1.5x-c6109b1680cd/run.json
- `E1_noslip_side_walls.m2-39a4571e43e5` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:09:25+00:00 wall=1.375e+04 s; record: results/runs/E1_noslip_side_walls.m2-39a4571e43e5/run.json
- `E1_noslip_side_walls.dt0.005-c41af2c90410` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T01:16:41+00:00 wall=1163 s; record: results/runs/E1_noslip_side_walls.dt0.005-c41af2c90410/run.json
- `E1_noslip_side_walls.D2x-6e1f5c2d9088` status=completed parent=E1_noslip_side_walls.D2x-1620b1098386 created=2026-10-20T02:45:12+00:00 wall=1285 s; record: results/runs/E1_noslip_side_walls.D2x-6e1f5c2d9088/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 3882401384.0, "relative_to_root": 8.463922790494877, "experiment_wall_seconds": 22756.490061081986, "n_experiments": 6, "planner_calls": 6, "planner_cost_usd": 0.626934925, "loop_wall_seconds": 13064.652381735}
