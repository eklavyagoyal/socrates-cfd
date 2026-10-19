# Verification report: B2_moderate_domain (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3713
- strouhal_number: 0.16704

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 3.00e-10 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.74 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 2.49e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 9.90e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — no REFINE_MESH experiment has been run; mesh error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — no REFINE_MESH experiment has been run; mesh error of strouhal_number is unknown
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **FAIL** domain_sensitivity [mean_drag_coefficient] — mean_drag_coefficient of the run under verification changes by 3.39% under domain refinement (> tau=3%); its value is not converged to the requested tolerance
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 3.70% > 1.50% but the demonstrated change 2.45% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.28, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run B2_moderate_domain-55b85b2cd33e is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── mesh_quality: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── mass_conservation: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── linear_solver_convergence: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── courant_number: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── reynolds_consistency: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── force_reference_consistency: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── physics_regime: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── convection_scheme_order: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── Averaging window (reported vs stationary value): PASS U=1.86e-06
│   └── B2_moderate_domain-55b85b2cd33e
├── Temporal statistics (stationarity, cycles): PASS U=2.49e-05
│   └── B2_moderate_domain-55b85b2cd33e
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── B2_moderate_domain-55b85b2cd33e
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── B2_moderate_domain-55b85b2cd33e
└── Artificial boundaries (domain sensitivity): FAIL
    └── B2_moderate_domain-55b85b2cd33e
    └── B2_moderate_domain.D2x-44c88f366919
    └── B2_moderate_domain.D2x-39e861cedde4

CLAIM: strouhal_number of run B2_moderate_domain-55b85b2cd33e is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── mesh_quality: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── mass_conservation: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── linear_solver_convergence: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── courant_number: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── reynolds_consistency: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── force_reference_consistency: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── physics_regime: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── convection_scheme_order: PASS
│   └── B2_moderate_domain-55b85b2cd33e
├── Averaging window (reported vs stationary value): PASS U=7.01e-06
│   └── B2_moderate_domain-55b85b2cd33e
├── Temporal statistics (stationarity, cycles): PASS U=9.9e-06
│   └── B2_moderate_domain-55b85b2cd33e
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE
│   └── B2_moderate_domain-55b85b2cd33e
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── B2_moderate_domain-55b85b2cd33e
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.037
    └── B2_moderate_domain-55b85b2cd33e
    └── B2_moderate_domain.D2x-44c88f366919
    └── B2_moderate_domain.D2x-39e861cedde4

```

## EXPERIMENT HISTORY

Run B2_moderate_domain-55b85b2cd33e: submitted simulation (19160 cells, dt=0.01 D/U, half-height 10 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so I can't ACCEPT. Nothing invalidates R0, so I can't REJECT.
  - Measured components for R0 are tiny. Averaging and statistics uncertainty for mean_drag_coefficient are 1.858e-06 and 2.492e-05. For strouhal_number they are 7.006e-06 and 9.904e-06. Both are far below the 0.03 tolerance. The stationary window has 13 cycles. Sampling is therefore not the limiting factor.
  - Mesh, time and domain components are all unmeasured for both quantities, so combined_uncertainty is null. Each is INCONCLUSIVE because no experiment has been run.
  - The time-step evidence is moderately reassuring. R0 has time_step_convective_units 0.01, max Courant 0.73526 and 598.66 steps per shedding period. It also uses a second-order backward scheme. I rank time error as the least likely of the three to exceed 3%.
  - The domain is the most suspect. R0 has blockage_ratio 0.05, half_height_D 10 with symmetryPlane lateral boundaries, upstream_D 15 and downstream_D 25. The question asks for an unbounded stream. Symmetry walls at 5% blockage can plausibly shift both mean drag and Strouhal number by a few percent.
  - The mesh is fairly coarse, with 19160 cells, representative_cell_size_D 0.20424 and wake_last_cell_D 0.55293. Mesh error is a real candidate. EXPAND_DOMAIN costs less (763 s versus 1258 s for REFINE_MESH). It also tests the assumption the question states explicitly, that the stream is unbounded.
  - Budget is ample: 0 of 6 experiments used and 0 of 12 relative compute used. Mesh and time experiments can follow.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain-55b85b2cd33e — R0 has 5% blockage with symmetry lateral boundaries (half height 10 D), and the question requires an unbounded stream. Artificial-boundary truncation is the error source most likely to move mean Cd and St by more than the 3% tolerance. It is also the cheapest experiment (763 s), because the near-field mesh is unchanged.
  - Outcome: executed -> B2_moderate_domain.D2x-44c88f366919 (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks. I can't ACCEPT, and nothing in the package invalidates R0, so I can't REJECT.
  - R0 sampling is not the limiting factor. Averaging and statistics uncertainty for mean_drag_coefficient are 1.858e-06 and 2.492e-05, and for strouhal_number they are 7.006e-06 and 9.904e-06. R0 has 13 stationary cycles.
  - R1 (EXPAND_DOMAIN from R0) moved both quantities. Mean Cd went from 1.3713 (R0) to 1.3395 (R1), and St went from 0.16704 to 0.16421. The verifier records demonstrated changes of 2.37% and 1.72%, both below the 0.03 tolerance. So there is no FAIL.
  - The domain component is still unresolved. The verifier estimates 0.1422 for Cd and 0.1035 for St, using a two-level Richardson extrapolation with an assumed order p=1 and Fs=3. Both are above the 0.5*tolerance budget. The order is assumed, not measured, and the verifier says more refinement is needed.
  - R1 is only a partially converged domain. It has blockage_ratio 0.025, half_height_D 20, upstream_D 30 and downstream_D 50, with symmetryPlane lateral boundaries. The question requires an unbounded stream. The Cd and St shifts are monotonic and not yet shown to be flattening.
  - A third domain level from R1 gives a three-level sequence with a constant factor of 2.0 (R0, R1, R2). This lets the verifier measure the convergence order instead of assuming it. It is the cheapest way to cut the largest uncertainty component.
  - R1 has 6 stationary cycles, and its St frequency resolution is 0.025, coarser than R0's 0.013333. Its stationary-window St (0.16421) is reported to 5 digits, so the cycle count is not a concern for the domain comparison. Still, R2 should keep a similar or longer record.
  - Mesh and time errors are unmeasured for both quantities. They stay as later experiments, because the domain term dominates the budget now.
  - Budget is ample: 1 of 6 experiments used, and 0.75 of 12 relative compute used.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain.D2x-44c88f366919 — Domain is the largest unresolved component: the verifier estimates 0.1422 for Cd and 0.1035 for St, using an assumed order p=1. R1 changed Cd from 1.3713 to 1.3395 and St from 0.16704 to 0.16421, so the boundaries still matter. A third level with the same factor of 2.0 as R0 to R1 lets the verifier measure the convergence order and extrapolate to the unbounded stream the question requires.
  - Outcome: executed -> B2_moderate_domain.D2x-39e861cedde4 (completed)

Run B2_moderate_domain.D2x-44c88f366919: EXPAND_DOMAIN from B2_moderate_domain-55b85b2cd33e (averaging.start_time: 75→40, domain.downstream: 25→50, domain.half_height: 10→20, domain.upstream: 15→30, mesh.n_downstream: 78→110, mesh.n_lateral: 24→35, mesh.n_upstream: 27→36, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.3713 → 1.3395 (-2.32%).
  - Observation: strouhal_number 0.16704 → 0.16421 (-1.70%).

Run B2_moderate_domain.D2x-39e861cedde4: EXPAND_DOMAIN from B2_moderate_domain.D2x-44c88f366919 (domain.downstream: 50→100, domain.half_height: 20→40, domain.upstream: 30→60, mesh.n_downstream: 110→144, mesh.n_lateral: 35→45, mesh.n_upstream: 36→45).
  - Observation: mean_drag_coefficient 1.3395 → 1.3263 (-0.98%).
  - Observation: strouhal_number 0.16421 → 0.16305 (-0.71%).

## FINAL JUSTIFICATION

Failed checks (measured): domain_sensitivity[mean_drag_coefficient].
- mean_drag_coefficient: REJECT (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=FAIL; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `B2_moderate_domain-55b85b2cd33e` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1020 s; record: results/runs/B2_moderate_domain-55b85b2cd33e/run.json
- `B2_moderate_domain.D2x-44c88f366919` status=completed parent=B2_moderate_domain-55b85b2cd33e created=2026-10-19T09:09:24+00:00 wall=924.8 s; record: results/runs/B2_moderate_domain.D2x-44c88f366919/run.json
- `B2_moderate_domain.D2x-39e861cedde4` status=completed parent=B2_moderate_domain.D2x-44c88f366919 created=2026-10-19T17:18:20+00:00 wall=1037 s; record: results/runs/B2_moderate_domain.D2x-39e861cedde4/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 504240000.0, "relative_to_root": 1.7544885177453027, "experiment_wall_seconds": 1962.1250563380017, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12484521999999999, "loop_wall_seconds": 35525.780881692}
