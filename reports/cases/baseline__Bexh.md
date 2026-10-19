# Verification report: baseline (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3313
- strouhal_number: 0.16344

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.01e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.24e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.14% <= 1.50% (root-to-finest change 0.331%) [three-level, observed order 4.91 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.32% <= 1.50% (root-to-finest change 0.860%) [three-level Celik procedure, observed order p=2.42, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.11% <= 1.50% (root-to-finest change 0.278%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.0e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.30% <= 1.50% (root-to-finest change 0.075%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.9e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.89% > 1.50% but the demonstrated change 0.65% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.6e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.63% > 1.50% but the demonstrated change 0.44% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-03)]

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
├── Averaging window (reported vs stationary value): PASS U=7.17e-05
│   └── baseline-408129116207
│   └── baseline.long250-8b585d987e4c
├── Temporal statistics (stationarity, cycles): PASS U=5.01e-06
│   └── baseline-408129116207
│   └── baseline.long250-8b585d987e4c
├── Spatial discretisation (mesh sensitivity): PASS U=0.0114
│   └── baseline.long250-8b585d987e4c
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.0111
│   └── baseline.long250-8b585d987e4c
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0389
    └── baseline.long250-8b585d987e4c
    └── baseline.D2x-efba395f6c27

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
├── Averaging window (reported vs stationary value): PASS U=7.47e-06
│   └── baseline-408129116207
│   └── baseline.long250-8b585d987e4c
├── Temporal statistics (stationarity, cycles): PASS U=1.24e-05
│   └── baseline-408129116207
│   └── baseline.long250-8b585d987e4c
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── baseline.long250-8b585d987e4c
│   └── baseline.m1.41-807cdf343a51
│   └── baseline.m2-476115cbbf20
├── Temporal discretisation (time-step sensitivity): PASS U=0.003
│   └── baseline.long250-8b585d987e4c
│   └── baseline.dt0.005-693742b868bc
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0263
    └── baseline.long250-8b585d987e4c
    └── baseline.D2x-efba395f6c27

```

## EXPERIMENT HISTORY

Run baseline-408129116207: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run baseline.long250-8b585d987e4c: RUN_LONGER from baseline-408129116207 ().
  - Observation: mean_drag_coefficient 1.3311 → 1.3312 (+0.00%).
  - Observation: strouhal_number 0.16343 → 0.16344 (+0.00%).

Run baseline.m1.41-807cdf343a51: REFINE_MESH from baseline-408129116207 ().
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run baseline.m2-476115cbbf20: REFINE_MESH from baseline.m1.41-807cdf343a51 ().
  - Observation: mean_drag_coefficient 1.3349 → 1.3356 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run baseline.dt0.005-693742b868bc: REDUCE_TIME_STEP from baseline-408129116207 ().
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run baseline.D2x-efba395f6c27: EXPAND_DOMAIN from baseline-408129116207 ().
  - Observation: mean_drag_coefficient 1.3311 → 1.3226 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

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
- `baseline.long250-8b585d987e4c` status=completed parent=baseline-408129116207 created=2026-10-19T09:08:38+00:00 wall=1013 s; record: results/runs/baseline.long250-8b585d987e4c/run.json
- `baseline.m1.41-807cdf343a51` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=5234 s; record: results/runs/baseline.m1.41-807cdf343a51/run.json
- `baseline.m2-476115cbbf20` status=completed parent=baseline.m1.41-807cdf343a51 created=2026-10-19T09:41:41+00:00 wall=6871 s; record: results/runs/baseline.m2-476115cbbf20/run.json
- `baseline.dt0.005-693742b868bc` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=4058 s; record: results/runs/baseline.dt0.005-693742b868bc/run.json
- `baseline.D2x-efba395f6c27` status=completed parent=baseline-408129116207 created=2026-10-19T07:35:16+00:00 wall=3659 s; record: results/runs/baseline.D2x-efba395f6c27/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
