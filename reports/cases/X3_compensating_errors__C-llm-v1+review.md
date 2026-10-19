# Verification report: X3_compensating_errors (C-llm-v1+review)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3918
- strouhal_number: 0.1642

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 3.89e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.39 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.003% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 6.93e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 6.65e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **FAIL** domain_sensitivity [mean_drag_coefficient] — mean_drag_coefficient of the run under verification changes by 5.14% under domain refinement (> tau=3%); its value is not converged to the requested tolerance
- **FAIL** domain_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 3.83% under domain refinement (> tau=3%); its value is not converged to the requested tolerance

### Evidence graph

```
CLAIM: mean_drag_coefficient of run X3_compensating_errors-b45927f15797 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── X3_compensating_errors-b45927f15797
├── mesh_quality: PASS
│   └── X3_compensating_errors-b45927f15797
├── mass_conservation: PASS
│   └── X3_compensating_errors-b45927f15797
├── linear_solver_convergence: PASS
│   └── X3_compensating_errors-b45927f15797
├── courant_number: PASS
│   └── X3_compensating_errors-b45927f15797
├── reynolds_consistency: PASS
│   └── X3_compensating_errors-b45927f15797
├── force_reference_consistency: PASS
│   └── X3_compensating_errors-b45927f15797
├── physics_regime: PASS
│   └── X3_compensating_errors-b45927f15797
├── convection_scheme_order: PASS
│   └── X3_compensating_errors-b45927f15797
├── Averaging window (reported vs stationary value): PASS U=3.19e-05
│   └── X3_compensating_errors-b45927f15797
├── Temporal statistics (stationarity, cycles): PASS U=6.93e-05
│   └── X3_compensating_errors-b45927f15797
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── X3_compensating_errors-b45927f15797
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── X3_compensating_errors-b45927f15797
└── Artificial boundaries (domain sensitivity): FAIL
    └── X3_compensating_errors-b45927f15797
    └── X3_compensating_errors.D2x-1574421fa2c4

CLAIM: strouhal_number of run X3_compensating_errors-b45927f15797 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── X3_compensating_errors-b45927f15797
├── mesh_quality: PASS
│   └── X3_compensating_errors-b45927f15797
├── mass_conservation: PASS
│   └── X3_compensating_errors-b45927f15797
├── linear_solver_convergence: PASS
│   └── X3_compensating_errors-b45927f15797
├── courant_number: PASS
│   └── X3_compensating_errors-b45927f15797
├── reynolds_consistency: PASS
│   └── X3_compensating_errors-b45927f15797
├── force_reference_consistency: PASS
│   └── X3_compensating_errors-b45927f15797
├── physics_regime: PASS
│   └── X3_compensating_errors-b45927f15797
├── convection_scheme_order: PASS
│   └── X3_compensating_errors-b45927f15797
├── Averaging window (reported vs stationary value): PASS U=1.05e-05
│   └── X3_compensating_errors-b45927f15797
├── Temporal statistics (stationarity, cycles): PASS U=6.65e-05
│   └── X3_compensating_errors-b45927f15797
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── X3_compensating_errors-b45927f15797
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── X3_compensating_errors-b45927f15797
└── Artificial boundaries (domain sensitivity): FAIL
    └── X3_compensating_errors-b45927f15797
    └── X3_compensating_errors.D2x-1574421fa2c4

```

## EXPERIMENT HISTORY

Run X3_compensating_errors-b45927f15797: submitted simulation (3904 cells, dt=0.01 D/U, half-height 6 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The verifier verdict is INCONCLUSIVE with no failed checks, so I can't ACCEPT or REJECT. R0 mesh, time and domain uncertainty components are all unmeasured.
  - Averaging and statistics are well controlled for R0. Drag CI95 is 2.3708e-05 and the statistics uncertainty is 6.927e-05 for drag and 6.654e-05 for Strouhal. There are 13 stationary cycles and drift_rel is 6.9266e-05. These are tiny against the 0.03 tolerance, so RUN_LONGER would add little.
  - R0 has a blockage ratio of 0.083333 with half_height_D 6.0 and symmetryPlane lateral boundaries. The question says to treat the stream as unbounded. Confinement this large could shift both drag and Strouhal by more than 3 %, and it is a systematic error that no other check bounds.
  - The mesh is coarse (3904 cells, representative_cell_size_D 0.30334, wake_last_cell_D 0.90784), so mesh error is also a real risk. The domain experiment is cheaper (109 s vs 150 s) and addresses the explicit 'unbounded' requirement, so I run it first.
  - Time-step error is less likely to dominate. R0 uses a second-order backward scheme, max Courant is 0.3914, and there are 609 steps per shedding period. The time error is still unmeasured.
  - R0's recorded strouhal_frequency_resolution is 0.013333, about 8 % of the reported St of 0.1642. This is coarser than the tolerance and should be checked. The reported St matches the FFT value, but the frequency estimate needs verification.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on X3_compensating_errors-b45927f15797 — The question requires an unbounded stream, but R0 has 8.33 % blockage with symmetry lateral boundaries at 6D half-height and only 10D upstream and 20D downstream. This is the most likely systematic flaw to exceed the 3 % tolerance, and it is the cheapest unmeasured component (109 s).
  - Outcome: executed -> X3_compensating_errors.D2x-1574421fa2c4 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 8.33, 8.33

Run X3_compensating_errors.D2x-1574421fa2c4: EXPAND_DOMAIN from X3_compensating_errors-b45927f15797 (averaging.start_time: 75→40, domain.downstream: 20→40, domain.half_height: 6→12, domain.upstream: 10→20, mesh.n_downstream: 69→101, mesh.n_lateral: 16→27, mesh.n_upstream: 21→29, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3918 → 1.3238 (-4.89%).
  - Observation: strouhal_number 0.1642 → 0.15814 (-3.69%).

## FINAL JUSTIFICATION

Failed checks (measured): domain_sensitivity[mean_drag_coefficient], domain_sensitivity[strouhal_number].
- mean_drag_coefficient: REJECT (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=FAIL; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=FAIL; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `X3_compensating_errors-b45927f15797` status=completed parent=None created=2026-10-19T09:08:43+00:00 wall=141.9 s; record: results/runs/X3_compensating_errors-b45927f15797/run.json
- `X3_compensating_errors.D2x-1574421fa2c4` status=completed parent=X3_compensating_errors-b45927f15797 created=2026-10-19T16:32:47+00:00 wall=102.7 s; record: results/runs/X3_compensating_errors.D2x-1574421fa2c4/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 45056000.0, "relative_to_root": 0.7693989071038252, "experiment_wall_seconds": 102.6904518559968, "n_experiments": 1, "planner_calls": 1, "planner_cost_usd": 0.056067075, "loop_wall_seconds": 3790.418334214999}
