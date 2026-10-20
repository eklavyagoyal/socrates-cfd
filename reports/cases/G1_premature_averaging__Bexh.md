# Verification report: G1_premature_averaging (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2961
- strouhal_number: 0.16129

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +25.8% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 2.631% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.312% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.20e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.01e-04 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.16% <= 1.50% (root-to-finest change 0.334%) [three-level, observed order 4.73 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.33% <= 1.50% (root-to-finest change 0.863%) [three-level Celik procedure, observed order p=2.39, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.11% <= 1.50% (root-to-finest change 0.277%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.2e-04)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.30% <= 1.50% (root-to-finest change 0.076%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.0e-04)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.92% > 1.50% but the demonstrated change 0.65% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.66% > 1.50% but the demonstrated change 0.44% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0263
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Temporal statistics (stationarity, cycles): PASS U=0.00012
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Spatial discretisation (mesh sensitivity): PASS U=0.0116
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.m1.41-88dff6e86104
│   └── G1_premature_averaging.m2-4626a1ae57d2
├── Temporal discretisation (time-step sensitivity): PASS U=0.0111
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.dt0.005-81ad3cc0e1fa
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0392
    └── G1_premature_averaging.long140-34c6cca905d9
    └── G1_premature_averaging.D2x-8095ac8f3890

CLAIM: strouhal_number of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0131
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Temporal statistics (stationarity, cycles): PASS U=0.000101
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long140-34c6cca905d9
├── Spatial discretisation (mesh sensitivity): PASS U=0.0133
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.m1.41-88dff6e86104
│   └── G1_premature_averaging.m2-4626a1ae57d2
├── Temporal discretisation (time-step sensitivity): PASS U=0.00303
│   └── G1_premature_averaging.long140-34c6cca905d9
│   └── G1_premature_averaging.dt0.005-81ad3cc0e1fa
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0266
    └── G1_premature_averaging.long140-34c6cca905d9
    └── G1_premature_averaging.D2x-8095ac8f3890

```

## EXPERIMENT HISTORY

Run G1_premature_averaging-17c0143468d7: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run G1_premature_averaging.long140-34c6cca905d9: RUN_LONGER from G1_premature_averaging-17c0143468d7 ().
  - Observation: mean_drag_coefficient 1.3039 → 1.3311 (+2.09%).
  - Observation: strouhal_number 0.16058 → 0.16343 (+1.78%).

Run G1_premature_averaging.m1.41-88dff6e86104: REFINE_MESH from G1_premature_averaging-17c0143468d7 ().
  - Observation: mean_drag_coefficient 1.3039 → 1.3349 (+2.38%).
  - Observation: strouhal_number 0.16058 → 0.16443 (+2.39%).

Run G1_premature_averaging.m2-4626a1ae57d2: REFINE_MESH from G1_premature_averaging.m1.41-88dff6e86104 ().
  - Observation: mean_drag_coefficient 1.3349 → 1.3356 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run G1_premature_averaging.dt0.005-81ad3cc0e1fa: REDUCE_TIME_STEP from G1_premature_averaging-17c0143468d7 ().
  - Observation: mean_drag_coefficient 1.3039 → 1.3274 (+1.81%).
  - Observation: strouhal_number 0.16058 → 0.16356 (+1.85%).

Run G1_premature_averaging.D2x-8095ac8f3890: EXPAND_DOMAIN from G1_premature_averaging-17c0143468d7 ().
  - Observation: mean_drag_coefficient 1.3039 → 1.3225 (+1.43%).
  - Observation: strouhal_number 0.16058 → 0.16271 (+1.33%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G1_premature_averaging-17c0143468d7` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=391.6 s; record: results/runs/G1_premature_averaging-17c0143468d7/run.json
- `G1_premature_averaging.long140-34c6cca905d9` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-19T09:08:45+00:00 wall=939.3 s; record: results/runs/G1_premature_averaging.long140-34c6cca905d9/run.json
- `G1_premature_averaging.m1.41-88dff6e86104` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-19T18:15:24+00:00 wall=2355 s; record: results/runs/G1_premature_averaging.m1.41-88dff6e86104/run.json
- `G1_premature_averaging.m2-4626a1ae57d2` status=completed parent=G1_premature_averaging.m1.41-88dff6e86104 created=2026-10-19T19:01:45+00:00 wall=5994 s; record: results/runs/G1_premature_averaging.m2-4626a1ae57d2/run.json
- `G1_premature_averaging.dt0.005-81ad3cc0e1fa` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-19T20:41:40+00:00 wall=1739 s; record: results/runs/G1_premature_averaging.dt0.005-81ad3cc0e1fa/run.json
- `G1_premature_averaging.D2x-8095ac8f3890` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-20T06:49:28+00:00 wall=1452 s; record: results/runs/G1_premature_averaging.D2x-8095ac8f3890/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
