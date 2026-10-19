# Verification report: X2_inlet_shear (C-rule-v2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3312
- strouhal_number: 0.16312

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** geometry_consistency — meshed cylinder diameter matches the specification within 1e-03
- **FAIL** inlet_uniformity — inlet velocity is not the specified uniform stream (Ux 0.1125..0.1875 m/s, non-uniformity 50.00%)
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.047% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.035% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.27e-03 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.50e-03 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── geometry_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── inlet_uniformity: FAIL
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000473
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.00227
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── X2_inlet_shear-32168bfbca6b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── X2_inlet_shear-32168bfbca6b

CLAIM: strouhal_number of run X2_inlet_shear-32168bfbca6b is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mesh_quality: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── mass_conservation: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── linear_solver_convergence: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── courant_number: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── reynolds_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── force_reference_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── physics_regime: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── convection_scheme_order: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── geometry_consistency: PASS
│   └── X2_inlet_shear-32168bfbca6b
├── inlet_uniformity: FAIL
│   └── X2_inlet_shear-32168bfbca6b
├── Averaging window (reported vs stationary value): PASS U=0.000352
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal statistics (stationarity, cycles): PASS U=0.0025
│   └── X2_inlet_shear-32168bfbca6b
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── X2_inlet_shear-32168bfbca6b
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── X2_inlet_shear-32168bfbca6b
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── X2_inlet_shear-32168bfbca6b

```

## EXPERIMENT HISTORY

Run X2_inlet_shear-32168bfbca6b: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

## FINAL JUSTIFICATION

Failed checks (measured): inlet_uniformity.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X2_inlet_shear-32168bfbca6b` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=1984 s; record: results/runs/X2_inlet_shear-32168bfbca6b/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 0.0, "relative_to_root": 0.0, "experiment_wall_seconds": 0, "n_experiments": 0, "planner_calls": 0, "planner_cost_usd": 0, "loop_wall_seconds": 0.0006344970024656504}
