# Verification report: C1_large_timestep (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3238
- strouhal_number: 0.16351

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 2.50e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **INCONCLUSIVE** courant_number — max Courant number 3.42 with 3 PIMPLE outer correctors: stable large-Co operation is possible but temporal accuracy is unproven without time-step refinement
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.006% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.14e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 3.35e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.09% <= 1.50% (root-to-finest change 0.022%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.1e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.25% <= 1.50% (root-to-finest change 0.062%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.8e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.06% > 1.50% but the demonstrated change 0.68% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.5e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.67% > 1.50% but the demonstrated change 0.44% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=6.22e-05
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.long250-e98556fadbd6
├── Temporal statistics (stationarity, cycles): PASS U=1.14e-05
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.long250-e98556fadbd6
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.000864
│   └── C1_large_timestep.long250-e98556fadbd6
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0406
    └── C1_large_timestep.long250-e98556fadbd6
    └── C1_large_timestep.D2x-f2b47ea2de80

CLAIM: strouhal_number of run C1_large_timestep-49d90ffccdac is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mesh_quality: PASS
│   └── C1_large_timestep-49d90ffccdac
├── mass_conservation: PASS
│   └── C1_large_timestep-49d90ffccdac
├── linear_solver_convergence: PASS
│   └── C1_large_timestep-49d90ffccdac
├── courant_number: INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── reynolds_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── force_reference_consistency: PASS
│   └── C1_large_timestep-49d90ffccdac
├── physics_regime: PASS
│   └── C1_large_timestep-49d90ffccdac
├── convection_scheme_order: PASS
│   └── C1_large_timestep-49d90ffccdac
├── Averaging window (reported vs stationary value): PASS U=7.75e-06
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.long250-e98556fadbd6
├── Temporal statistics (stationarity, cycles): PASS U=3.35e-06
│   └── C1_large_timestep-49d90ffccdac
│   └── C1_large_timestep.long250-e98556fadbd6
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── C1_large_timestep-49d90ffccdac
├── Temporal discretisation (time-step sensitivity): PASS U=0.00246
│   └── C1_large_timestep.long250-e98556fadbd6
│   └── C1_large_timestep.dt0.025-610f857bd6ea
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0267
    └── C1_large_timestep.long250-e98556fadbd6
    └── C1_large_timestep.D2x-f2b47ea2de80

```

## EXPERIMENT HISTORY

Run C1_large_timestep-49d90ffccdac: submitted simulation (30580 cells, dt=0.05 D/U, half-height 40 D).

Run C1_large_timestep.long250-e98556fadbd6: RUN_LONGER from C1_large_timestep-49d90ffccdac ().
  - Observation: mean_drag_coefficient 1.3237 → 1.3238 (+0.00%).
  - Observation: strouhal_number 0.16351 → 0.16351 (+0.00%).

Run C1_large_timestep.m1.41-c9c1535204d3: REFINE_MESH from C1_large_timestep-49d90ffccdac ().

Run C1_large_timestep.m2-a3ed547121c5: REFINE_MESH from C1_large_timestep.m1.41-c9c1535204d3 ().

Run C1_large_timestep.dt0.025-610f857bd6ea: REDUCE_TIME_STEP from C1_large_timestep-49d90ffccdac ().
  - Observation: mean_drag_coefficient 1.3237 → 1.3235 (-0.02%).
  - Observation: strouhal_number 0.16351 → 0.16361 (+0.06%).

Run C1_large_timestep.D2x-f2b47ea2de80: EXPAND_DOMAIN from C1_large_timestep-49d90ffccdac ().
  - Observation: mean_drag_coefficient 1.3237 → 1.3149 (-0.67%).
  - Observation: strouhal_number 0.16351 → 0.16279 (-0.44%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `C1_large_timestep-49d90ffccdac` status=completed parent=None created=2026-10-19T07:09:37+00:00 wall=1159 s; record: results/runs/C1_large_timestep-49d90ffccdac/run.json
- `C1_large_timestep.long250-e98556fadbd6` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T13:28:02+00:00 wall=670.7 s; record: results/runs/C1_large_timestep.long250-e98556fadbd6/run.json
- `C1_large_timestep.m1.41-c9c1535204d3` status=failed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T03:41:02+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m1.41-c9c1535204d3/run.json
- `C1_large_timestep.m2-a3ed547121c5` status=failed parent=C1_large_timestep.m1.41-c9c1535204d3 created=2026-10-20T06:49:20+00:00 wall=n/a s; record: results/runs/C1_large_timestep.m2-a3ed547121c5/run.json
- `C1_large_timestep.dt0.025-610f857bd6ea` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-19T16:55:27+00:00 wall=906.3 s; record: results/runs/C1_large_timestep.dt0.025-610f857bd6ea/run.json
- `C1_large_timestep.D2x-f2b47ea2de80` status=completed parent=C1_large_timestep-49d90ffccdac created=2026-10-20T04:12:05+00:00 wall=885.8 s; record: results/runs/C1_large_timestep.D2x-f2b47ea2de80/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
