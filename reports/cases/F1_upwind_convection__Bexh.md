# Verification report: F1_upwind_convection (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2687
- strouhal_number: 0.12614

## VERDICT: **REJECT**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +11.3% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **INCONCLUSIVE** convection_scheme_order — convection scheme 'Gauss upwind' is formally first order; numerical diffusion must be shown negligible by mesh refinement before the result can be trusted
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.166% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.100% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.23e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.32e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 95.30% > 1.50% but the demonstrated change 2.07% <= tau; more refinement would be needed [three-level, observed order 0.07 outside [0.5, 2.0]x formal; p=min(observed, formal)=0.07 with Fs=3]
- **FAIL** mesh_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 11.44% under mesh refinement (> tau=3%); its value is not converged to the requested tolerance
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.39% <= 1.50% (root-to-finest change 0.097%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.069%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.5e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 5.03% > 1.50% but the demonstrated change 0.84% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 2.5e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 3.82% > 1.50% but the demonstrated change 0.64% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 2.3e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run F1_upwind_convection-e460c39ac86c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mesh_quality: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mass_conservation: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── linear_solver_convergence: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── courant_number: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── reynolds_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── force_reference_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── physics_regime: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── convection_scheme_order: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── Averaging window (reported vs stationary value): PASS U=0.00166
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long250-0dc1edea9982
├── Temporal statistics (stationarity, cycles): PASS U=0.000123
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long250-0dc1edea9982
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.953
│   └── F1_upwind_convection.long250-0dc1edea9982
│   └── F1_upwind_convection.m1.41-777f4291b366
│   └── F1_upwind_convection.m2-b8b419d05dcd
├── Temporal discretisation (time-step sensitivity): PASS U=0.00389
│   └── F1_upwind_convection.long250-0dc1edea9982
│   └── F1_upwind_convection.dt0.005-ab4ff52f420f
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0503
    └── F1_upwind_convection.long250-0dc1edea9982
    └── F1_upwind_convection.D2x-ea393aa80e46

CLAIM: strouhal_number of run F1_upwind_convection-e460c39ac86c is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mesh_quality: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── mass_conservation: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── linear_solver_convergence: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── courant_number: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── reynolds_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── force_reference_consistency: PASS
│   └── F1_upwind_convection-e460c39ac86c
├── physics_regime: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── convection_scheme_order: INCONCLUSIVE
│   └── F1_upwind_convection-e460c39ac86c
├── Averaging window (reported vs stationary value): PASS U=0.001
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long250-0dc1edea9982
├── Temporal statistics (stationarity, cycles): PASS U=0.000132
│   └── F1_upwind_convection-e460c39ac86c
│   └── F1_upwind_convection.long250-0dc1edea9982
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── F1_upwind_convection.long250-0dc1edea9982
│   └── F1_upwind_convection.m1.41-777f4291b366
│   └── F1_upwind_convection.m2-b8b419d05dcd
├── Temporal discretisation (time-step sensitivity): PASS U=0.00275
│   └── F1_upwind_convection.long250-0dc1edea9982
│   └── F1_upwind_convection.dt0.005-ab4ff52f420f
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0382
    └── F1_upwind_convection.long250-0dc1edea9982
    └── F1_upwind_convection.D2x-ea393aa80e46

```

## EXPERIMENT HISTORY

Run F1_upwind_convection-e460c39ac86c: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run F1_upwind_convection.long250-0dc1edea9982: RUN_LONGER from F1_upwind_convection-e460c39ac86c ().
  - Observation: mean_drag_coefficient 1.2674 → 1.2708 (+0.27%).
  - Observation: strouhal_number 0.12581 → 0.12626 (+0.36%).

Run F1_upwind_convection.m1.41-777f4291b366: REFINE_MESH from F1_upwind_convection-e460c39ac86c ().
  - Observation: mean_drag_coefficient 1.2674 → 1.2845 (+1.35%).
  - Observation: strouhal_number 0.12581 → 0.1354 (+7.62%).

Run F1_upwind_convection.m2-b8b419d05dcd: REFINE_MESH from F1_upwind_convection.m1.41-777f4291b366 ().
  - Observation: mean_drag_coefficient 1.2845 → 1.2977 (+1.03%).
  - Observation: strouhal_number 0.1354 → 0.14257 (+5.30%).

Run F1_upwind_convection.dt0.005-ab4ff52f420f: REDUCE_TIME_STEP from F1_upwind_convection-e460c39ac86c ().
  - Observation: mean_drag_coefficient 1.2674 → 1.2696 (+0.17%).
  - Observation: strouhal_number 0.12581 → 0.12635 (+0.43%).

Run F1_upwind_convection.D2x-ea393aa80e46: EXPAND_DOMAIN from F1_upwind_convection-e460c39ac86c ().
  - Observation: mean_drag_coefficient 1.2674 → 1.2602 (-0.56%).
  - Observation: strouhal_number 0.12581 → 0.12546 (-0.28%).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_sensitivity[strouhal_number].
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=FAIL, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `F1_upwind_convection-e460c39ac86c` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1374 s; record: results/runs/F1_upwind_convection-e460c39ac86c/run.json
- `F1_upwind_convection.long250-0dc1edea9982` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-19T09:08:42+00:00 wall=1220 s; record: results/runs/F1_upwind_convection.long250-0dc1edea9982/run.json
- `F1_upwind_convection.m1.41-777f4291b366` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-19T13:28:02+00:00 wall=3212 s; record: results/runs/F1_upwind_convection.m1.41-777f4291b366/run.json
- `F1_upwind_convection.m2-b8b419d05dcd` status=completed parent=F1_upwind_convection.m1.41-777f4291b366 created=2026-10-19T14:21:37+00:00 wall=5732 s; record: results/runs/F1_upwind_convection.m2-b8b419d05dcd/run.json
- `F1_upwind_convection.dt0.005-ab4ff52f420f` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-20T06:49:23+00:00 wall=1608 s; record: results/runs/F1_upwind_convection.dt0.005-ab4ff52f420f/run.json
- `F1_upwind_convection.D2x-ea393aa80e46` status=completed parent=F1_upwind_convection-e460c39ac86c created=2026-10-20T13:47:57+00:00 wall=1466 s; record: results/runs/F1_upwind_convection.D2x-ea393aa80e46/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
