# Verification report: H1_dynamic_viscosity (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3486
- strouhal_number: 0.15402

## VERDICT: **REJECT**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.72 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **FAIL** reynolds_consistency — case solves Re=83.33 but the problem specifies Re=100 (relative mismatch 16.67%); the simulation answers a different question
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.004% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.23e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 3.96e-06 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.97% <= 1.50% (root-to-finest change 0.283%) [three-level, observed order 5.20 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.11% <= 1.50% (root-to-finest change 0.757%) [three-level Celik procedure, observed order p=2.74, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.96% <= 1.50% (root-to-finest change 0.239%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.21% <= 1.50% (root-to-finest change 0.052%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.8e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.99% > 1.50% but the demonstrated change 0.66% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.9e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.79% > 1.50% but the demonstrated change 0.46% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.9e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run H1_dynamic_viscosity-4ab90bfffff4 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── mesh_quality: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── mass_conservation: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── linear_solver_convergence: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── courant_number: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── reynolds_consistency: FAIL
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── force_reference_consistency: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── physics_regime: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── convection_scheme_order: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Averaging window (reported vs stationary value): PASS U=3.83e-05
│   └── H1_dynamic_viscosity-4ab90bfffff4
│   └── H1_dynamic_viscosity.long250-9fe13958c389
├── Temporal statistics (stationarity, cycles): PASS U=2.23e-06
│   └── H1_dynamic_viscosity-4ab90bfffff4
│   └── H1_dynamic_viscosity.long250-9fe13958c389
├── Spatial discretisation (mesh sensitivity): PASS U=0.00969
│   └── H1_dynamic_viscosity.long250-9fe13958c389
│   └── H1_dynamic_viscosity.m1.41-f0d5b0a7b270
│   └── H1_dynamic_viscosity.m2-21637f9f044c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00958
│   └── H1_dynamic_viscosity.long250-9fe13958c389
│   └── H1_dynamic_viscosity.dt0.005-f10119c4bb2c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0399
    └── H1_dynamic_viscosity.long250-9fe13958c389
    └── H1_dynamic_viscosity.D2x-643a7dd2c873

CLAIM: strouhal_number of run H1_dynamic_viscosity-4ab90bfffff4 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── mesh_quality: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── mass_conservation: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── linear_solver_convergence: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── courant_number: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── reynolds_consistency: FAIL
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── force_reference_consistency: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── physics_regime: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── convection_scheme_order: PASS
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Averaging window (reported vs stationary value): PASS U=8.28e-06
│   └── H1_dynamic_viscosity-4ab90bfffff4
│   └── H1_dynamic_viscosity.long250-9fe13958c389
├── Temporal statistics (stationarity, cycles): PASS U=3.96e-06
│   └── H1_dynamic_viscosity-4ab90bfffff4
│   └── H1_dynamic_viscosity.long250-9fe13958c389
├── Spatial discretisation (mesh sensitivity): PASS U=0.0111
│   └── H1_dynamic_viscosity.long250-9fe13958c389
│   └── H1_dynamic_viscosity.m1.41-f0d5b0a7b270
│   └── H1_dynamic_viscosity.m2-21637f9f044c
├── Temporal discretisation (time-step sensitivity): PASS U=0.00207
│   └── H1_dynamic_viscosity.long250-9fe13958c389
│   └── H1_dynamic_viscosity.dt0.005-f10119c4bb2c
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0279
    └── H1_dynamic_viscosity.long250-9fe13958c389
    └── H1_dynamic_viscosity.D2x-643a7dd2c873

```

## EXPERIMENT HISTORY

Run H1_dynamic_viscosity-4ab90bfffff4: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run H1_dynamic_viscosity.long250-9fe13958c389: RUN_LONGER from H1_dynamic_viscosity-4ab90bfffff4 ().
  - Observation: mean_drag_coefficient 1.3486 → 1.3487 (+0.00%).
  - Observation: strouhal_number 0.15401 → 0.15402 (+0.00%).

Run H1_dynamic_viscosity.m1.41-f0d5b0a7b270: REFINE_MESH from H1_dynamic_viscosity-4ab90bfffff4 ().
  - Observation: mean_drag_coefficient 1.3486 → 1.352 (+0.25%).
  - Observation: strouhal_number 0.15401 → 0.15487 (+0.55%).

Run H1_dynamic_viscosity.m2-21637f9f044c: REFINE_MESH from H1_dynamic_viscosity.m1.41-f0d5b0a7b270 ().
  - Observation: mean_drag_coefficient 1.352 → 1.3525 (+0.04%).
  - Observation: strouhal_number 0.15487 → 0.15519 (+0.21%).

Run H1_dynamic_viscosity.dt0.005-f10119c4bb2c: REDUCE_TIME_STEP from H1_dynamic_viscosity-4ab90bfffff4 ().
  - Observation: mean_drag_coefficient 1.3486 → 1.3454 (-0.24%).
  - Observation: strouhal_number 0.15401 → 0.1541 (+0.05%).

Run H1_dynamic_viscosity.D2x-643a7dd2c873: EXPAND_DOMAIN from H1_dynamic_viscosity-4ab90bfffff4 ().
  - Observation: mean_drag_coefficient 1.3486 → 1.3398 (-0.66%).
  - Observation: strouhal_number 0.15401 → 0.15331 (-0.46%).

## FINAL JUSTIFICATION

Failed checks (measured): reynolds_consistency.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `H1_dynamic_viscosity-4ab90bfffff4` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1797 s; record: results/runs/H1_dynamic_viscosity-4ab90bfffff4/run.json
- `H1_dynamic_viscosity.long250-9fe13958c389` status=completed parent=H1_dynamic_viscosity-4ab90bfffff4 created=2026-10-19T13:28:02+00:00 wall=1015 s; record: results/runs/H1_dynamic_viscosity.long250-9fe13958c389/run.json
- `H1_dynamic_viscosity.m1.41-f0d5b0a7b270` status=completed parent=H1_dynamic_viscosity-4ab90bfffff4 created=2026-10-20T06:49:23+00:00 wall=3056 s; record: results/runs/H1_dynamic_viscosity.m1.41-f0d5b0a7b270/run.json
- `H1_dynamic_viscosity.m2-21637f9f044c` status=completed parent=H1_dynamic_viscosity.m1.41-f0d5b0a7b270 created=2026-10-20T13:01:58+00:00 wall=7922 s; record: results/runs/H1_dynamic_viscosity.m2-21637f9f044c/run.json
- `H1_dynamic_viscosity.dt0.005-f10119c4bb2c` status=completed parent=H1_dynamic_viscosity-4ab90bfffff4 created=2026-10-20T15:31:51+00:00 wall=1755 s; record: results/runs/H1_dynamic_viscosity.dt0.005-f10119c4bb2c/run.json
- `H1_dynamic_viscosity.D2x-643a7dd2c873` status=completed parent=H1_dynamic_viscosity-4ab90bfffff4 created=2026-10-20T16:22:38+00:00 wall=1386 s; record: results/runs/H1_dynamic_viscosity.D2x-643a7dd2c873/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
