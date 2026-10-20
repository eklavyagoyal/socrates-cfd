# Verification report: B2_moderate_domain (C-llm-r3)

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
  - Deterministic verdict is INCONCLUSIVE with no failed checks. Mesh, time and domain uncertainty components are all unmeasured for both quantities, so ACCEPT is not allowed. REJECT is not justified because there is no FAIL.
  - R0 is clean on the checks that were run. It completed, mass imbalance is 3e-10, max Courant is 0.73526, and Re is consistent at 100. The stationary window has 13 cycles. The Cd statistical uncertainty is 2.492e-05 and the St statistical uncertainty is 9.904e-06, both far below the 0.03 tolerance. Averaging, statistics and solver health are therefore not the limiting factors.
  - The recorded domain is small for an unbounded-stream requirement. R0 has blockage_ratio 0.05, half_height_D 10.0 with symmetryPlane lateral boundaries, upstream_D 15.0 and downstream_D 25.0. Symmetry walls at 5% blockage can plausibly shift both Cd and St by an amount comparable to the 3% tolerance. This effect is completely unmeasured (domain_sensitivity INCONCLUSIVE).
  - The mesh is moderate. representative_cell_size_D is 0.20424, cells_around_cylinder is 160 and wake_last_cell_D is 0.55293. Mesh error is also unmeasured, but it is a second priority.
  - Time-step error is the least suspicious. The scheme is backward (second order), time_step_convective_units is 0.01 and there are 598.66 steps per shedding period. The St frequency resolution is 0.013333, which is about 8% of St=0.16704, but the St value is consistent between the time-domain and FFT estimates.
  - EXPAND_DOMAIN on R0 is the cheapest experiment, at an estimated 763 s against 1020.3 s for the root run. It leaves the near-field mesh and time step unchanged, so it isolates the boundary effect. Budget is ample: 0 of 6 experiments used and 0 of 12 compute units used. Mesh and time-step experiments should follow afterwards.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain-55b85b2cd33e — Domain truncation is unmeasured and is the most likely flaw large enough to change Cd or St by more than 3%. R0 has 5% blockage with symmetryPlane lateral boundaries at 10D half-height, 15D upstream and 25D downstream. The question requires an unbounded stream. This is the cheapest experiment (about 763 s) and it isolates the boundary effect because the near-field mesh and time step are unchanged.
  - Outcome: executed -> B2_moderate_domain.D2x-44c88f366919 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 8%

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and there are no failed checks. ACCEPT is not allowed because mesh, time and domain are unresolved for both quantities. REJECT is not allowed because there is no FAIL.
  - The R0 to R1 domain expansion changed the answers measurably. Cd went from 1.3713 to 1.3395, a 2.37% change. St went from 0.16704 to 0.16421, a 1.72% change. Both are below the 0.03 tolerance, so this is not a FAIL, but both are larger than half the tolerance.
  - The verifier's two-level Richardson estimate, with an assumed order p=1, gives a domain uncertainty of 0.1422 for Cd and 0.1035 for St. Both are far above 0.5*tolerance (0.015). The convergence order is assumed, not measured, so the estimate is conservative and unconfirmed.
  - Domain convergence is the only component with a measured signal near the tolerance. It dominates the budget and should be resolved first.
  - R1 is not a pure domain change. Its representative_cell_size_D is 0.34512 against 0.20424 for R0, and its wake_last_cell_D is 1.0348 against 0.55293. Its record is shorter: 6 stationary cycles against 13, and an St frequency resolution of 0.025 against 0.013333. Part of the R0 to R1 difference could come from coarser outer or wake cells, not only from the boundary distances. A third level with the same cell-addition rule would show whether the change is converging.
  - Averaging and statistical uncertainties are negligible for R0: 1.858e-06 and 2.492e-05 for Cd, 7.006e-06 and 9.904e-06 for St. Solver health is clean: mass imbalance 3e-10, max Courant 0.73526, residual limit met in 100% of steps.
  - Mesh and time-step errors are still unmeasured. They come after the domain, because the domain error is already shown to be comparable to the tolerance. Budget is ample: 1 of 6 experiments used and 0.75 of 12.0 compute units used. EXPAND_DOMAIN from R1 is estimated at 1027 s.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain.D2x-44c88f366919 — Domain is the only unresolved component with a measured effect near the tolerance: Cd changed 2.37% and St 1.72% from R0 to R1. The verifier's domain uncertainty (0.1422 for Cd, 0.1035 for St) rests on an assumed order p=1 from two levels. A third level with the same expansion ratio of 2 (R0 to R1 to R2) gives a measured convergence order and a measured domain error. The cost estimate from R1 is 1027 s, within budget.
  - Outcome: executed -> B2_moderate_domain.D2x-39e861cedde4 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 0.75%

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
- Experiment cost: {"experiment_cell_steps": 504240000.0, "relative_to_root": 1.7544885177453027, "experiment_wall_seconds": 1962.1250563380017, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12524972, "loop_wall_seconds": 40.655671514999995}
