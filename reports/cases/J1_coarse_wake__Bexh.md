# Verification report: J1_coarse_wake (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3229
- strouhal_number: 0.16213

## VERDICT: **REJECT**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **FAIL** mesh_quality — checkMesh reports 1 failed check(s): ['***Cells with small determinant (< 0.001) found, number of cells: 48']
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.27e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.77e-06 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.18% <= 1.50% (root-to-finest change 0.721%) [three-level Celik procedure, observed order p=2.09, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.17% > 1.50% but the demonstrated change 1.39% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.29, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.17% <= 1.50% (root-to-finest change 0.292%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 2.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.31% <= 1.50% (root-to-finest change 0.078%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.58% > 1.50% but the demonstrated change 0.76% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.5e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 3.20% > 1.50% but the demonstrated change 0.53% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run J1_coarse_wake-a7868b40e5b3 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── mesh_quality: FAIL
│   └── J1_coarse_wake-a7868b40e5b3
├── mass_conservation: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── linear_solver_convergence: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── courant_number: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── reynolds_consistency: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── force_reference_consistency: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── physics_regime: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── convection_scheme_order: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── Averaging window (reported vs stationary value): PASS U=4.27e-06
│   └── J1_coarse_wake-a7868b40e5b3
│   └── J1_coarse_wake.long250-3f0bba3224d0
├── Temporal statistics (stationarity, cycles): PASS U=1.27e-06
│   └── J1_coarse_wake-a7868b40e5b3
│   └── J1_coarse_wake.long250-3f0bba3224d0
├── Spatial discretisation (mesh sensitivity): PASS U=0.0118
│   └── J1_coarse_wake.long250-3f0bba3224d0
│   └── J1_coarse_wake.m1.41-eeef8dc41497
│   └── J1_coarse_wake.m2-4e289fbff8ee
├── Temporal discretisation (time-step sensitivity): PASS U=0.0117
│   └── J1_coarse_wake.long250-3f0bba3224d0
│   └── J1_coarse_wake.dt0.005-12edfa23616b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0458
    └── J1_coarse_wake.long250-3f0bba3224d0
    └── J1_coarse_wake.D2x-59e747f0bd71

CLAIM: strouhal_number of run J1_coarse_wake-a7868b40e5b3 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── mesh_quality: FAIL
│   └── J1_coarse_wake-a7868b40e5b3
├── mass_conservation: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── linear_solver_convergence: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── courant_number: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── reynolds_consistency: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── force_reference_consistency: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── physics_regime: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── convection_scheme_order: PASS
│   └── J1_coarse_wake-a7868b40e5b3
├── Averaging window (reported vs stationary value): PASS U=2.93e-07
│   └── J1_coarse_wake-a7868b40e5b3
│   └── J1_coarse_wake.long250-3f0bba3224d0
├── Temporal statistics (stationarity, cycles): PASS U=2.77e-06
│   └── J1_coarse_wake-a7868b40e5b3
│   └── J1_coarse_wake.long250-3f0bba3224d0
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0217
│   └── J1_coarse_wake.long250-3f0bba3224d0
│   └── J1_coarse_wake.m1.41-eeef8dc41497
│   └── J1_coarse_wake.m2-4e289fbff8ee
├── Temporal discretisation (time-step sensitivity): PASS U=0.00314
│   └── J1_coarse_wake.long250-3f0bba3224d0
│   └── J1_coarse_wake.dt0.005-12edfa23616b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.032
    └── J1_coarse_wake.long250-3f0bba3224d0
    └── J1_coarse_wake.D2x-59e747f0bd71

```

## EXPERIMENT HISTORY

Run J1_coarse_wake-a7868b40e5b3: submitted simulation (20440 cells, dt=0.01 D/U, half-height 40 D).

Run J1_coarse_wake.long250-3f0bba3224d0: RUN_LONGER from J1_coarse_wake-a7868b40e5b3 ().
  - Observation: mean_drag_coefficient 1.3229 → 1.3229 (+0.00%).
  - Observation: strouhal_number 0.16212 → 0.16213 (+0.00%).

Run J1_coarse_wake.m1.41-eeef8dc41497: REFINE_MESH from J1_coarse_wake-a7868b40e5b3 ().
  - Observation: mean_drag_coefficient 1.3229 → 1.3294 (+0.49%).
  - Observation: strouhal_number 0.16212 → 0.1637 (+0.97%).

Run J1_coarse_wake.m2-4e289fbff8ee: REFINE_MESH from J1_coarse_wake.m1.41-eeef8dc41497 ().
  - Observation: mean_drag_coefficient 1.3294 → 1.3325 (+0.23%).
  - Observation: strouhal_number 0.1637 → 0.16441 (+0.43%).

Run J1_coarse_wake.dt0.005-12edfa23616b: REDUCE_TIME_STEP from J1_coarse_wake-a7868b40e5b3 ().
  - Observation: mean_drag_coefficient 1.3229 → 1.319 (-0.29%).
  - Observation: strouhal_number 0.16212 → 0.16225 (+0.08%).

Run J1_coarse_wake.D2x-59e747f0bd71: EXPAND_DOMAIN from J1_coarse_wake-a7868b40e5b3 ().
  - Observation: mean_drag_coefficient 1.3229 → 1.3129 (-0.76%).
  - Observation: strouhal_number 0.16212 → 0.16126 (-0.53%).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_quality.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `J1_coarse_wake-a7868b40e5b3` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1580 s; record: results/runs/J1_coarse_wake-a7868b40e5b3/run.json
- `J1_coarse_wake.long250-3f0bba3224d0` status=completed parent=J1_coarse_wake-a7868b40e5b3 created=2026-10-19T13:28:02+00:00 wall=801.6 s; record: results/runs/J1_coarse_wake.long250-3f0bba3224d0/run.json
- `J1_coarse_wake.m1.41-eeef8dc41497` status=completed parent=J1_coarse_wake-a7868b40e5b3 created=2026-10-19T20:07:30+00:00 wall=2149 s; record: results/runs/J1_coarse_wake.m1.41-eeef8dc41497/run.json
- `J1_coarse_wake.m2-4e289fbff8ee` status=completed parent=J1_coarse_wake.m1.41-eeef8dc41497 created=2026-10-20T06:49:28+00:00 wall=7455 s; record: results/runs/J1_coarse_wake.m2-4e289fbff8ee/run.json
- `J1_coarse_wake.dt0.005-12edfa23616b` status=completed parent=J1_coarse_wake-a7868b40e5b3 created=2026-10-20T11:46:56+00:00 wall=1445 s; record: results/runs/J1_coarse_wake.dt0.005-12edfa23616b/run.json
- `J1_coarse_wake.D2x-59e747f0bd71` status=completed parent=J1_coarse_wake-a7868b40e5b3 created=2026-10-20T12:11:02+00:00 wall=1070 s; record: results/runs/J1_coarse_wake.D2x-59e747f0bd71/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
