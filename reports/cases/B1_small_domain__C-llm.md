# Verification report: B1_small_domain (C-llm)

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
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. The mesh, time and domain uncertainty components are all unmeasured for both mean_drag_coefficient and strouhal_number.
  - R0 statistics are very tight. The drag CI95 is 5.8838e-06 and the drift is 1.1249e-05, over 14 stationary cycles. The averaging and statistics checks PASS, so more run length would add little.
  - The R0 numerics checks PASS. Courant is 0.74419, mass imbalance is 6.6667e-10, linear solver convergence is 100%, and the scheme is nominally second order. These checks do not measure discretisation or truncation error.
  - The domain is the most likely source of an error larger than 3%. R0 has blockage_ratio 0.125, with half_height_D 4.0 on symmetryPlane lateral boundaries, upstream_D 8.0 and downstream_D 15.0. The problem asks for an unbounded stream, so this confinement is a likely bias.
  - The mesh is moderate, with 13070 cells, 160 cells around the cylinder and representative_cell_size_D 0.1184. Wake_last_cell_D is 0.36188, which is coarse. Mesh error is possible but is the second priority.
  - The time step is 0.01 D/U with 556.7 steps per shedding period and a second-order backward scheme. Temporal error is the least likely to exceed tolerance.
  - Strouhal frequency resolution is 0.013333, which is about 7.4% of St=0.17963. This is coarse compared with the 3% tolerance, yet the FFT and the stationary-window St agree at 0.17963. This is a secondary concern.
  - stationary_window_start_is_mser_cap is true, with the window starting at 70.199 against a declared start of 75.0. The drift and half-difference are tiny, so this is a minor flag. A RUN_LONGER child could address it later.
  - Budget is ample: 0 of 6 experiments used and 0 of 12.0 relative compute. EXPAND_DOMAIN with factor 2.0 costs about 397 s, below the root's 511.01 s.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B1_small_domain-a69ffb97a2e6 — The requested stream is unbounded, but R0 has 12.5% blockage with symmetry lateral boundaries at 4D, upstream 8D and downstream 15D. This confinement is the most likely source of an error larger than the 3% tolerance. The near-field mesh is unchanged, so the run isolates the boundary effect. It is also the cheapest experiment on the menu, at about 397 s.
  - Outcome: executed -> B1_small_domain.D2x-1e192fc39a3e (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 7.4%

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
- Experiment cost: {"experiment_cell_steps": 152224000.0, "relative_to_root": 0.776454985972966, "experiment_wall_seconds": 695.4309916049988, "n_experiments": 1, "planner_calls": 1, "planner_cost_usd": 0.05218251, "loop_wall_seconds": 2152.499930161999}
