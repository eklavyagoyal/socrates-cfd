# Verification report: B1_small_domain (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.5089
- strouhal_number: 0.17963

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 6.67e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.12e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.62e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **FAIL** domain_sensitivity [mean_drag_coefficient] — mean_drag_coefficient of the run under verification changes by 8.86% under domain refinement (> tau=3%); its value is not converged to the requested tolerance
- **FAIL** domain_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 6.65% under domain refinement (> tau=3%); its value is not converged to the requested tolerance

### Evidence graph

```
CLAIM: mean_drag_coefficient of run B1_small_domain-a69ffb97a2e6 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mesh_quality: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mass_conservation: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── linear_solver_convergence: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── courant_number: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── reynolds_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── force_reference_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── physics_regime: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── convection_scheme_order: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── Averaging window (reported vs stationary value): PASS U=1.31e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal statistics (stationarity, cycles): PASS U=1.12e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── B1_small_domain-a69ffb97a2e6
└── Artificial boundaries (domain sensitivity): FAIL
    └── B1_small_domain-a69ffb97a2e6
    └── B1_small_domain.D2x-1e192fc39a3e

CLAIM: strouhal_number of run B1_small_domain-a69ffb97a2e6 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mesh_quality: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── mass_conservation: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── linear_solver_convergence: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── courant_number: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── reynolds_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── force_reference_consistency: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── physics_regime: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── convection_scheme_order: PASS
│   └── B1_small_domain-a69ffb97a2e6
├── Averaging window (reported vs stationary value): PASS U=9.75e-08
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal statistics (stationarity, cycles): PASS U=1.62e-05
│   └── B1_small_domain-a69ffb97a2e6
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── B1_small_domain-a69ffb97a2e6
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── B1_small_domain-a69ffb97a2e6
└── Artificial boundaries (domain sensitivity): FAIL
    └── B1_small_domain-a69ffb97a2e6
    └── B1_small_domain.D2x-1e192fc39a3e

```

## EXPERIMENT HISTORY

Run B1_small_domain-a69ffb97a2e6: submitted simulation (13070 cells, dt=0.01 D/U, half-height 4 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict for R0 is INCONCLUSIVE with no failed checks. I can't ACCEPT, and there is no measured FAIL to justify REJECT.
  - R0's averaging and statistics components pass. Drag CI95 is 5.8838e-06 and the Strouhal statistics uncertainty is 1.621e-05, both far below the 0.03 tolerance. R0 has 14 stationary cycles and a drag drift of 1.1249e-05.
  - Mesh, time and domain uncertainty are all unmeasured for both quantities, so combined_uncertainty is null.
  - The domain is the most likely source of an error larger than 3%. The recorded blockage ratio is 0.125 (half_height_D 4.0 with symmetryPlane lateral boundaries), the inlet is 8D upstream and the outlet 15D downstream. The question asks for an unbounded stream. Confinement of this size can shift both mean drag (R0: 1.5089) and Strouhal number (R0: 0.17963) by more than the tolerance.
  - Temporal resolution looks adequate: max Courant is 0.74419, with 556.7 steps per shedding period and a second-order backward scheme. The mesh has 160 cells around the cylinder and a wall-first-cell height of 0.005 D, so it is likely fine near the body. Both are less likely to exceed 3% than the domain truncation.
  - EXPAND_DOMAIN is the cheapest experiment (397 s against 545 s for REDUCE_TIME_STEP and 640 s for REFINE_MESH). It leaves the near-field mesh unchanged, so it isolates the boundary effect. Budget is untouched: 0 of 6 experiments used.
  - Mesh and time experiments will still be needed afterwards, because the verifier requires every component to be measured.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B1_small_domain-a69ffb97a2e6 — Blockage ratio 0.125 with symmetryPlane lateral walls at 4D, 8D upstream and 15D downstream is the largest plausible bias for an unbounded-stream request. This is the cheapest primitive (397 s), and it leaves the near-field mesh and time step unchanged, so any change in Cd or St is attributable to the boundaries.
  - Outcome: executed -> B1_small_domain.D2x-1e192fc39a3e (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 0.0625

Run B1_small_domain.D2x-1e192fc39a3e: EXPAND_DOMAIN from B1_small_domain-a69ffb97a2e6 (averaging.start_time: 75→40, domain.downstream: 15→30, domain.half_height: 4→8, domain.upstream: 8→16, mesh.n_downstream: 56→86, mesh.n_lateral: 9→21, mesh.n_upstream: 19→28, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.5089 → 1.3862 (-8.13%).
  - Observation: strouhal_number 0.17963 → 0.16844 (-6.23%).

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

- `B1_small_domain-a69ffb97a2e6` status=completed parent=None created=2026-10-19T07:02:08+00:00 wall=511 s; record: results/runs/B1_small_domain-a69ffb97a2e6/run.json
- `B1_small_domain.D2x-1e192fc39a3e` status=completed parent=B1_small_domain-a69ffb97a2e6 created=2026-10-19T09:09:23+00:00 wall=695.4 s; record: results/runs/B1_small_domain.D2x-1e192fc39a3e/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 152224000.0, "relative_to_root": 0.776454985972966, "experiment_wall_seconds": 695.4309916049988, "n_experiments": 1, "planner_calls": 1, "planner_cost_usd": 0.049585010000000006, "loop_wall_seconds": 16.713631076003367}
