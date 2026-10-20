# Verification report: J1_coarse_wake (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3229
- strouhal_number: 0.16213

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 6.52e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 6.49e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

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
├── Averaging window (reported vs stationary value): PASS U=3.34e-06
│   └── J1_coarse_wake-a7868b40e5b3
├── Temporal statistics (stationarity, cycles): PASS U=6.52e-06
│   └── J1_coarse_wake-a7868b40e5b3
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── J1_coarse_wake-a7868b40e5b3
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── J1_coarse_wake-a7868b40e5b3
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── J1_coarse_wake-a7868b40e5b3

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
├── Averaging window (reported vs stationary value): PASS U=1.01e-06
│   └── J1_coarse_wake-a7868b40e5b3
├── Temporal statistics (stationarity, cycles): PASS U=6.49e-06
│   └── J1_coarse_wake-a7868b40e5b3
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── J1_coarse_wake-a7868b40e5b3
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── J1_coarse_wake-a7868b40e5b3
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── J1_coarse_wake-a7868b40e5b3

```

## EXPERIMENT HISTORY

Run J1_coarse_wake-a7868b40e5b3: submitted simulation (20440 cells, dt=0.01 D/U, half-height 40 D).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_quality.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `J1_coarse_wake-a7868b40e5b3` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1580 s; record: results/runs/J1_coarse_wake-a7868b40e5b3/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 0.0, "relative_to_root": 0.0, "experiment_wall_seconds": 0, "n_experiments": 0, "planner_calls": 0, "planner_cost_usd": 0, "loop_wall_seconds": 0.0006517139991046861}
