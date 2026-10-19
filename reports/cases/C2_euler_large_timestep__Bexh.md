# Verification report: C2_euler_large_timestep (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2901
- strouhal_number: 0.15849

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 2.92 with 2 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.004% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 3.85e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 4.58e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 6.66% > 1.50% but the demonstrated change 1.11% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 9.1e-05)]
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 9.21% > 1.50% but the demonstrated change 1.53% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 8.4e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.29% > 1.50% but the demonstrated change 0.71% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.7e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.74% > 1.50% but the demonstrated change 0.46% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.6e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=3.93e-05
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.long250-6341491e2554
├── Temporal statistics (stationarity, cycles): PASS U=3.85e-06
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.long250-6341491e2554
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0666
│   └── C2_euler_large_timestep.long250-6341491e2554
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0429
    └── C2_euler_large_timestep.long250-6341491e2554
    └── C2_euler_large_timestep.D2x-a912f88e2d43

CLAIM: strouhal_number of run C2_euler_large_timestep-268eddd71f94 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mesh_quality: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── mass_conservation: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── linear_solver_convergence: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── courant_number: INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── reynolds_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── force_reference_consistency: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── physics_regime: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── convection_scheme_order: PASS
│   └── C2_euler_large_timestep-268eddd71f94
├── Averaging window (reported vs stationary value): PASS U=1.6e-05
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.long250-6341491e2554
├── Temporal statistics (stationarity, cycles): PASS U=4.58e-06
│   └── C2_euler_large_timestep-268eddd71f94
│   └── C2_euler_large_timestep.long250-6341491e2554
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C2_euler_large_timestep-268eddd71f94
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE U=0.0921
│   └── C2_euler_large_timestep.long250-6341491e2554
│   └── C2_euler_large_timestep.dt0.02-2f2ce6b4d241
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0274
    └── C2_euler_large_timestep.long250-6341491e2554
    └── C2_euler_large_timestep.D2x-a912f88e2d43

```

## EXPERIMENT HISTORY

Run C2_euler_large_timestep-268eddd71f94: submitted simulation (30580 cells, dt=0.04 D/U, half-height 40 D).

Run C2_euler_large_timestep.long250-6341491e2554: RUN_LONGER from C2_euler_large_timestep-268eddd71f94 ().
  - Observation: mean_drag_coefficient 1.2901 → 1.2902 (+0.00%).
  - Observation: strouhal_number 0.15848 → 0.15849 (+0.00%).

Run C2_euler_large_timestep.m1.41-eb9ef468444b: REFINE_MESH from C2_euler_large_timestep-268eddd71f94 ().

Run C2_euler_large_timestep.m2-4c431502ff02: REFINE_MESH from C2_euler_large_timestep.m1.41-eb9ef468444b ().

Run C2_euler_large_timestep.dt0.02-2f2ce6b4d241: REDUCE_TIME_STEP from C2_euler_large_timestep-268eddd71f94 ().
  - Observation: mean_drag_coefficient 1.2901 → 1.3047 (+1.13%).
  - Observation: strouhal_number 0.15848 → 0.16096 (+1.56%).

Run C2_euler_large_timestep.D2x-a912f88e2d43: EXPAND_DOMAIN from C2_euler_large_timestep-268eddd71f94 ().
  - Observation: mean_drag_coefficient 1.2901 → 1.281 (-0.71%).
  - Observation: strouhal_number 0.15848 → 0.15777 (-0.45%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C2_euler_large_timestep-268eddd71f94` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1056 s; record: results/runs/C2_euler_large_timestep-268eddd71f94/run.json
- `C2_euler_large_timestep.long250-6341491e2554` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T12:12:03+00:00 wall=854 s; record: results/runs/C2_euler_large_timestep.long250-6341491e2554/run.json
- `C2_euler_large_timestep.m1.41-eb9ef468444b` status=failed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T09:08:42+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m1.41-eb9ef468444b/run.json
- `C2_euler_large_timestep.m2-4c431502ff02` status=failed parent=C2_euler_large_timestep.m1.41-eb9ef468444b created=2026-10-19T17:02:32+00:00 wall=n/a s; record: results/runs/C2_euler_large_timestep.m2-4c431502ff02/run.json
- `C2_euler_large_timestep.dt0.02-2f2ce6b4d241` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T17:02:32+00:00 wall=818.4 s; record: results/runs/C2_euler_large_timestep.dt0.02-2f2ce6b4d241/run.json
- `C2_euler_large_timestep.D2x-a912f88e2d43` status=completed parent=C2_euler_large_timestep-268eddd71f94 created=2026-10-19T19:14:28+00:00 wall=643.5 s; record: results/runs/C2_euler_large_timestep.D2x-a912f88e2d43/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
