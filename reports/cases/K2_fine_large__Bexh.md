# Verification report: K2_fine_large (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3278
- strouhal_number: 0.16382

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 0.00e+00 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.65 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 7.23e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 7.02e-06 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.68% <= 1.50% (root-to-finest change 0.113%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.5e-06)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.17% > 1.50% but the demonstrated change 0.36% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 4.3e-05)]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.79% <= 1.50% (root-to-finest change 0.198%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.7e-06)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.27% <= 1.50% (root-to-finest change 0.067%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.17% > 1.50% but the demonstrated change 0.53% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 2.0e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 1.88% > 1.50% but the demonstrated change 0.31% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.5e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=7.18e-05
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.long250-0d48c4a802f5
├── Temporal statistics (stationarity, cycles): PASS U=7.23e-06
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.long250-0d48c4a802f5
├── Spatial discretisation (mesh sensitivity): PASS U=0.00684
│   └── K2_fine_large.long250-0d48c4a802f5
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
├── Temporal discretisation (time-step sensitivity): PASS U=0.0079
│   └── K2_fine_large.long250-0d48c4a802f5
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0317
    └── K2_fine_large.long250-0d48c4a802f5
    └── K2_fine_large.D2x-bc527461f36d

CLAIM: strouhal_number of run K2_fine_large-2d999cd1eb7c is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mesh_quality: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── mass_conservation: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── linear_solver_convergence: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── courant_number: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── reynolds_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── force_reference_consistency: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── physics_regime: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── convection_scheme_order: PASS
│   └── K2_fine_large-2d999cd1eb7c
├── Averaging window (reported vs stationary value): PASS U=5.2e-06
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.long250-0d48c4a802f5
├── Temporal statistics (stationarity, cycles): PASS U=7.02e-06
│   └── K2_fine_large-2d999cd1eb7c
│   └── K2_fine_large.long250-0d48c4a802f5
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0217
│   └── K2_fine_large.long250-0d48c4a802f5
│   └── K2_fine_large.m1.77-e5d0ad1d73b4
├── Temporal discretisation (time-step sensitivity): PASS U=0.0027
│   └── K2_fine_large.long250-0d48c4a802f5
│   └── K2_fine_large.dt0.0035-6a0f9a80f290
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0188
    └── K2_fine_large.long250-0d48c4a802f5
    └── K2_fine_large.D2x-bc527461f36d

```

## EXPERIMENT HISTORY

Run K2_fine_large-2d999cd1eb7c: submitted simulation (54244 cells, dt=0.007 D/U, half-height 60 D).

Run K2_fine_large.long250-0d48c4a802f5: RUN_LONGER from K2_fine_large-2d999cd1eb7c ().
  - Observation: mean_drag_coefficient 1.3277 → 1.3277 (-0.00%).
  - Observation: strouhal_number 0.16382 → 0.16382 (+0.00%).

Run K2_fine_large.m1.77-e5d0ad1d73b4: REFINE_MESH from K2_fine_large-2d999cd1eb7c ().
  - Observation: mean_drag_coefficient 1.3277 → 1.3293 (+0.11%).
  - Observation: strouhal_number 0.16382 → 0.16441 (+0.36%).

Run K2_fine_large.dt0.0035-6a0f9a80f290: REDUCE_TIME_STEP from K2_fine_large-2d999cd1eb7c ().
  - Observation: mean_drag_coefficient 1.3277 → 1.3251 (-0.20%).
  - Observation: strouhal_number 0.16382 → 0.16393 (+0.07%).

Run K2_fine_large.D2x-bc527461f36d: EXPAND_DOMAIN from K2_fine_large-2d999cd1eb7c ().
  - Observation: mean_drag_coefficient 1.3277 → 1.3208 (-0.53%).
  - Observation: strouhal_number 0.16382 → 0.16331 (-0.31%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `K2_fine_large-2d999cd1eb7c` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=8041 s; record: results/runs/K2_fine_large-2d999cd1eb7c/run.json
- `K2_fine_large.long250-0d48c4a802f5` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-19T13:28:02+00:00 wall=4435 s; record: results/runs/K2_fine_large.long250-0d48c4a802f5/run.json
- `K2_fine_large.m1.77-e5d0ad1d73b4` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-19T10:01:45+00:00 wall=4914 s; record: results/runs/K2_fine_large.m1.77-e5d0ad1d73b4/run.json
- `K2_fine_large.dt0.0035-6a0f9a80f290` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T01:15:34+00:00 wall=3507 s; record: results/runs/K2_fine_large.dt0.0035-6a0f9a80f290/run.json
- `K2_fine_large.D2x-bc527461f36d` status=completed parent=K2_fine_large-2d999cd1eb7c created=2026-10-20T03:41:02+00:00 wall=3765 s; record: results/runs/K2_fine_large.D2x-bc527461f36d/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
