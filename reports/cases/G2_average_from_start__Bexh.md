# Verification report: G2_average_from_start (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3196
- strouhal_number: 0.16144

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +6.7% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.864% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.219% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.59e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 4.53e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.15% <= 1.50% (root-to-finest change 0.332%) [three-level, observed order 4.90 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.32% <= 1.50% (root-to-finest change 0.861%) [three-level Celik procedure, observed order p=2.42, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.11% <= 1.50% (root-to-finest change 0.277%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 5.6e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.30% <= 1.50% (root-to-finest change 0.076%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.2e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.00% > 1.50% but the demonstrated change 0.67% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 9.6e-04)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.74% > 1.50% but the demonstrated change 0.46% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 9.1e-04)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.00864
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=5.59e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): PASS U=0.0115
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m1.41-f3197d3f2274
│   └── G2_average_from_start.m2-d3befbe0bda4
├── Temporal discretisation (time-step sensitivity): PASS U=0.0111
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.dt0.005-ee6872926d0a
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.04
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D2x-049f970e44a8

CLAIM: strouhal_number of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.0122
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=4.53e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m1.41-f3197d3f2274
│   └── G2_average_from_start.m2-d3befbe0bda4
├── Temporal discretisation (time-step sensitivity): PASS U=0.00303
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.dt0.005-ee6872926d0a
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0274
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D2x-049f970e44a8

```

## EXPERIMENT HISTORY

Run G2_average_from_start-e7384e5a2c24: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run G2_average_from_start.long160-24e243b2227c: RUN_LONGER from G2_average_from_start-e7384e5a2c24 ().
  - Observation: mean_drag_coefficient 1.3266 → 1.3311 (+0.34%).
  - Observation: strouhal_number 0.163 → 0.16344 (+0.27%).

Run G2_average_from_start.m1.41-f3197d3f2274: REFINE_MESH from G2_average_from_start-e7384e5a2c24 ().
  - Observation: mean_drag_coefficient 1.3266 → 1.3349 (+0.63%).
  - Observation: strouhal_number 0.163 → 0.16443 (+0.88%).

Run G2_average_from_start.m2-d3befbe0bda4: REFINE_MESH from G2_average_from_start.m1.41-f3197d3f2274 ().
  - Observation: mean_drag_coefficient 1.3349 → 1.3356 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run G2_average_from_start.dt0.005-ee6872926d0a: REDUCE_TIME_STEP from G2_average_from_start-e7384e5a2c24 ().
  - Observation: mean_drag_coefficient 1.3266 → 1.3275 (+0.07%).
  - Observation: strouhal_number 0.163 → 0.16356 (+0.35%).

Run G2_average_from_start.D2x-049f970e44a8: EXPAND_DOMAIN from G2_average_from_start-e7384e5a2c24 ().
  - Observation: mean_drag_coefficient 1.3266 → 1.3223 (-0.32%).
  - Observation: strouhal_number 0.163 → 0.16269 (-0.19%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G2_average_from_start-e7384e5a2c24` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=636.2 s; record: results/runs/G2_average_from_start-e7384e5a2c24/run.json
- `G2_average_from_start.long160-24e243b2227c` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T09:08:43+00:00 wall=1041 s; record: results/runs/G2_average_from_start.long160-24e243b2227c/run.json
- `G2_average_from_start.m1.41-f3197d3f2274` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T08:00:11+00:00 wall=4180 s; record: results/runs/G2_average_from_start.m1.41-f3197d3f2274/run.json
- `G2_average_from_start.m2-d3befbe0bda4` status=completed parent=G2_average_from_start.m1.41-f3197d3f2274 created=2026-10-19T11:04:08+00:00 wall=6652 s; record: results/runs/G2_average_from_start.m2-d3befbe0bda4/run.json
- `G2_average_from_start.dt0.005-ee6872926d0a` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T13:28:02+00:00 wall=2049 s; record: results/runs/G2_average_from_start.dt0.005-ee6872926d0a/run.json
- `G2_average_from_start.D2x-049f970e44a8` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T16:49:57+00:00 wall=1121 s; record: results/runs/G2_average_from_start.D2x-049f970e44a8/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
