# Verification report: E1_noslip_side_walls (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3403
- strouhal_number: 0.16429

## VERDICT: **INCONCLUSIVE**


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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.051% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.043% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.39e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 4.48e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 5.49% > 1.50% but the demonstrated change 0.83% <= tau; more refinement would be needed [three-level, observed order 0.86 outside [0.5, 2.0]x formal; p=min(observed, formal)=0.86 with Fs=3]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.55% > 1.50% but the demonstrated change 1.23% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.32, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.08% <= 1.50% (root-to-finest change 0.269%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 5.4e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.35% <= 1.50% (root-to-finest change 0.087%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 4.5e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 6.84% > 1.50% but the demonstrated change 1.14% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 6.7e-04)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 4.98% > 1.50% but the demonstrated change 0.83% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 6.1e-04)]

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
├── Averaging window (reported vs stationary value): PASS U=0.000511
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.long250-f705e9196f25
├── Temporal statistics (stationarity, cycles): PASS U=0.000539
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.long250-f705e9196f25
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0549
│   └── E1_noslip_side_walls.long250-f705e9196f25
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.0108
│   └── E1_noslip_side_walls.long250-f705e9196f25
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0684
    └── E1_noslip_side_walls.long250-f705e9196f25
    └── E1_noslip_side_walls.D2x-1620b1098386

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
├── Averaging window (reported vs stationary value): PASS U=0.000433
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.long250-f705e9196f25
├── Temporal statistics (stationarity, cycles): PASS U=0.000448
│   └── E1_noslip_side_walls-88a7cd5812e8
│   └── E1_noslip_side_walls.long250-f705e9196f25
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0255
│   └── E1_noslip_side_walls.long250-f705e9196f25
│   └── E1_noslip_side_walls.m1.41-f15d7e2db685
│   └── E1_noslip_side_walls.m2-24c0dd986308
├── Temporal discretisation (time-step sensitivity): PASS U=0.00348
│   └── E1_noslip_side_walls.long250-f705e9196f25
│   └── E1_noslip_side_walls.dt0.005-c41af2c90410
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0498
    └── E1_noslip_side_walls.long250-f705e9196f25
    └── E1_noslip_side_walls.D2x-1620b1098386

```

## EXPERIMENT HISTORY

Run E1_noslip_side_walls-88a7cd5812e8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run E1_noslip_side_walls.long250-f705e9196f25: RUN_LONGER from E1_noslip_side_walls-88a7cd5812e8 ().
  - Observation: mean_drag_coefficient 1.3402 → 1.341 (+0.06%).
  - Observation: strouhal_number 0.16428 → 0.16436 (+0.05%).

Run E1_noslip_side_walls.m1.41-f15d7e2db685: REFINE_MESH from E1_noslip_side_walls-88a7cd5812e8 ().
  - Observation: mean_drag_coefficient 1.3402 → 1.3475 (+0.55%).
  - Observation: strouhal_number 0.16428 → 0.16562 (+0.82%).

Run E1_noslip_side_walls.m2-24c0dd986308: REFINE_MESH from E1_noslip_side_walls.m1.41-f15d7e2db685 ().
  - Observation: mean_drag_coefficient 1.3475 → 1.3523 (+0.35%).
  - Observation: strouhal_number 0.16562 → 0.16641 (+0.48%).

Run E1_noslip_side_walls.dt0.005-c41af2c90410: REDUCE_TIME_STEP from E1_noslip_side_walls-88a7cd5812e8 ().
  - Observation: mean_drag_coefficient 1.3402 → 1.3374 (-0.21%).
  - Observation: strouhal_number 0.16428 → 0.1645 (+0.14%).

Run E1_noslip_side_walls.D2x-1620b1098386: EXPAND_DOMAIN from E1_noslip_side_walls-88a7cd5812e8 ().
  - Observation: mean_drag_coefficient 1.3402 → 1.3259 (-1.07%).
  - Observation: strouhal_number 0.16428 → 0.16301 (-0.77%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `E1_noslip_side_walls-88a7cd5812e8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1851 s; record: results/runs/E1_noslip_side_walls-88a7cd5812e8/run.json
- `E1_noslip_side_walls.long250-f705e9196f25` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T13:28:02+00:00 wall=1354 s; record: results/runs/E1_noslip_side_walls.long250-f705e9196f25/run.json
- `E1_noslip_side_walls.m1.41-f15d7e2db685` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T09:08:43+00:00 wall=2302 s; record: results/runs/E1_noslip_side_walls.m1.41-f15d7e2db685/run.json
- `E1_noslip_side_walls.m2-24c0dd986308` status=completed parent=E1_noslip_side_walls.m1.41-f15d7e2db685 created=2026-10-20T01:15:34+00:00 wall=5373 s; record: results/runs/E1_noslip_side_walls.m2-24c0dd986308/run.json
- `E1_noslip_side_walls.dt0.005-c41af2c90410` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-20T01:16:41+00:00 wall=1163 s; record: results/runs/E1_noslip_side_walls.dt0.005-c41af2c90410/run.json
- `E1_noslip_side_walls.D2x-1620b1098386` status=completed parent=E1_noslip_side_walls-88a7cd5812e8 created=2026-10-19T20:14:34+00:00 wall=1058 s; record: results/runs/E1_noslip_side_walls.D2x-1620b1098386/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
