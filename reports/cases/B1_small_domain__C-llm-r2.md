# Verification report: B1_small_domain (C-llm-r2)

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
- **FAIL** domain_sensitivity [mean_drag_coefficient] — mean_drag_coefficient of the run under verification changes by 11.13% under domain refinement (> tau=3%); its value is not converged to the requested tolerance
- **FAIL** domain_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 8.32% under domain refinement (> tau=3%); its value is not converged to the requested tolerance

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
    └── B1_small_domain.D3x-5d5208a40ce1

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
    └── B1_small_domain.D3x-5d5208a40ce1

```

## EXPERIMENT HISTORY

Run B1_small_domain-a69ffb97a2e6: submitted simulation (13070 cells, dt=0.01 D/U, half-height 4 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and REJECT is not justified.
  - Mesh, time and domain uncertainty components are all unmeasured for mean_drag_coefficient and strouhal_number (no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run).
  - R0 averaging and statistics are tiny: drag CI95 5.8838e-06, drift_rel 1.1249e-05, 14 stationary cycles. Sampling noise is not the limiting issue.
  - R0 domain is confined: upstream_D 8.0, downstream_D 15.0, half_height_D 4.0, blockage_ratio 0.125, symmetryPlane lateral boundaries. The spec says to treat the stream as unbounded. A 12.5% blockage is the most likely flaw to shift Cd and St by more than the 0.03 tolerance.
  - Mesh and time are moderate: 160 cells around the cylinder, wall_first_cell_D 0.005, max Courant 0.74419, 556.7 steps per shedding period, second-order backward/linearUpwind. These are less likely to be the dominant error than the artificial boundaries.
  - The Strouhal frequency resolution is 0.013333 against a value of 0.17963, which is about 7%. This is coarser than the 3% tolerance, so St will need a finer-resolved measurement later. The reported St equals the FFT value 0.17963, and the uncertainty reported for St statistics is 1.621e-05.
  - stationary_window_start_is_mser_cap is true (window start 70.199). The drift is tiny, but the transient end is not independently confirmed, so RUN_LONGER is a lower-priority follow-up.
  - Budget is ample: 0 of 6 experiments used and 0 of 12.0 relative compute. EXPAND_DOMAIN from R0 costs about 397 s, the cheapest of the three discretisation experiments, and a large factor maximises sensitivity to the boundary effect.
  - Requested: EXPAND_DOMAIN {'factor': 3.0} on B1_small_domain-a69ffb97a2e6 — R0 has 12.5% blockage with symmetry lateral boundaries (half height 4D, upstream 8D, downstream 15D), while the question requires an unbounded stream. This is the most likely flaw to change Cd and St by more than 3%. It is also the cheapest discretisation experiment (about 397 s) and leaves the near-field mesh unchanged, so the effect is isolated.
  - Outcome: executed -> B1_small_domain.D3x-5d5208a40ce1 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 7%

Run B1_small_domain.D3x-5d5208a40ce1: EXPAND_DOMAIN from B1_small_domain-a69ffb97a2e6 (averaging.start_time: 75→40, domain.downstream: 15→45, domain.half_height: 4→12, domain.upstream: 8→24, mesh.n_downstream: 56→105, mesh.n_lateral: 9→27, mesh.n_upstream: 19→34, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.5089 → 1.3578 (-10.02%).
  - Observation: strouhal_number 0.17963 → 0.16584 (-7.68%).

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
- `B1_small_domain.D3x-5d5208a40ce1` status=completed parent=B1_small_domain-a69ffb97a2e6 created=2026-10-20T07:50:45+00:00 wall=838.3 s; record: results/runs/B1_small_domain.D3x-5d5208a40ce1/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 185808000.0, "relative_to_root": 0.9477582249426166, "experiment_wall_seconds": 838.3041549000009, "n_experiments": 1, "planner_calls": 1, "planner_cost_usd": 0.05322301, "loop_wall_seconds": 2778.5993378839994}
