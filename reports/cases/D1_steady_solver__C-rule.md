# Verification report: D1_steady_solver (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.0921
- strouhal_number: n/a

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 4.77e-05 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **FAIL** linear_solver_convergence — steady solver did not satisfy its residualControl before the iteration limit
- **INCONCLUSIVE** courant_number — not applicable to a steady pseudo-time solver; temporal behaviour unverifiable
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **FAIL** physics_regime — Re=100.0 lies in the periodic-shedding regime (onset Re~47.0); a steady formulation can only return the unstable symmetric branch, whose drag is not the time-mean drag of the physical flow
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **INCONCLUSIVE** averaging_window [mean_drag_coefficient] — steady solver: no time averaging performed
- **INCONCLUSIVE** averaging_window [strouhal_number] — steady solver: no time averaging performed
- **INCONCLUSIVE** statistical_uncertainty [mean_drag_coefficient] — steady solver: no statistics
- **INCONCLUSIVE** statistical_uncertainty [strouhal_number] — steady solver: no statistics
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

### Evidence graph

```
CLAIM: mean_drag_coefficient of run D1_steady_solver-9cd0391edef9 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── D1_steady_solver-9cd0391edef9
├── mesh_quality: PASS
│   └── D1_steady_solver-9cd0391edef9
├── mass_conservation: PASS
│   └── D1_steady_solver-9cd0391edef9
├── linear_solver_convergence: FAIL
│   └── D1_steady_solver-9cd0391edef9
├── courant_number: INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── reynolds_consistency: PASS
│   └── D1_steady_solver-9cd0391edef9
├── force_reference_consistency: PASS
│   └── D1_steady_solver-9cd0391edef9
├── physics_regime: FAIL
│   └── D1_steady_solver-9cd0391edef9
├── convection_scheme_order: PASS
│   └── D1_steady_solver-9cd0391edef9
├── Averaging window (reported vs stationary value): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Temporal statistics (stationarity, cycles): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── D1_steady_solver-9cd0391edef9

CLAIM: strouhal_number of run D1_steady_solver-9cd0391edef9 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── D1_steady_solver-9cd0391edef9
├── mesh_quality: PASS
│   └── D1_steady_solver-9cd0391edef9
├── mass_conservation: PASS
│   └── D1_steady_solver-9cd0391edef9
├── linear_solver_convergence: FAIL
│   └── D1_steady_solver-9cd0391edef9
├── courant_number: INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── reynolds_consistency: PASS
│   └── D1_steady_solver-9cd0391edef9
├── force_reference_consistency: PASS
│   └── D1_steady_solver-9cd0391edef9
├── physics_regime: FAIL
│   └── D1_steady_solver-9cd0391edef9
├── convection_scheme_order: PASS
│   └── D1_steady_solver-9cd0391edef9
├── Averaging window (reported vs stationary value): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Temporal statistics (stationarity, cycles): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── D1_steady_solver-9cd0391edef9
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── D1_steady_solver-9cd0391edef9

```

## EXPERIMENT HISTORY

Run D1_steady_solver-9cd0391edef9: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

## FINAL JUSTIFICATION

Failed checks (measured): linear_solver_convergence, physics_regime.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=INCONCLUSIVE, statistics=INCONCLUSIVE, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=INCONCLUSIVE, statistics=INCONCLUSIVE, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — averaging, statistics, mesh, time, domain.
- strouhal_number: not established — averaging, statistics, mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `D1_steady_solver-9cd0391edef9` status=completed parent=None created=2026-10-19T07:02:08+00:00 wall=246.7 s; record: results/runs/D1_steady_solver-9cd0391edef9/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 0.0, "relative_to_root": 0.0, "experiment_wall_seconds": 0, "n_experiments": 0, "planner_calls": 0, "planner_cost_usd": 0, "loop_wall_seconds": 0.00035603400101535954}
