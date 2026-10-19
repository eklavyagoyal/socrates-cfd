# Verification report: H1_dynamic_viscosity (C-rule)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3486
- strouhal_number: 0.15402

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient within 0.000% of the stationary-window value
- **PASS** averaging_window [strouhal_number] — reported strouhal_number within 0.002% of the stationary-window value
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.46e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 2.91e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

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
├── Averaging window (reported vs stationary value): PASS U=2.14e-06
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Temporal statistics (stationarity, cycles): PASS U=0.000146
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── H1_dynamic_viscosity-4ab90bfffff4
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── H1_dynamic_viscosity-4ab90bfffff4

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
├── Averaging window (reported vs stationary value): PASS U=2.31e-05
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Temporal statistics (stationarity, cycles): PASS U=2.91e-05
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── H1_dynamic_viscosity-4ab90bfffff4
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── H1_dynamic_viscosity-4ab90bfffff4
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── H1_dynamic_viscosity-4ab90bfffff4

```

## EXPERIMENT HISTORY

Run H1_dynamic_viscosity-4ab90bfffff4: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

## FINAL JUSTIFICATION

Failed checks (measured): reynolds_consistency.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `H1_dynamic_viscosity-4ab90bfffff4` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1797 s; record: results/runs/H1_dynamic_viscosity-4ab90bfffff4/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 0.0, "relative_to_root": 0.0, "experiment_wall_seconds": 0, "n_experiments": 0, "planner_calls": 0, "planner_cost_usd": 0, "loop_wall_seconds": 0.00033175499993376434}
