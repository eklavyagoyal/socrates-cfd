# Verification report: B2_moderate_domain (C-llm-r2)

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
  - No deterministic FAIL in the package, so REJECT is not allowed. The verdict is INCONCLUSIVE, so ACCEPT is not allowed.
  - R0 averaging and statistics pass for both quantities. For Cd the uncertainties are 1.858e-06 (averaging) and 2.492e-05 (statistics). For St they are 7.006e-06 and 9.904e-06. The window covers 13 stationary cycles.
  - Mesh, time and domain components are all INCONCLUSIVE because no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists. No combined uncertainty can be formed against the 0.03 tolerance.
  - Domain is the most likely source of an error larger than 3%. The case is declared unbounded, but R0 uses half_height_D 10.0 with symmetryPlane lateral boundaries, which gives blockage_ratio 0.05. Upstream is 15 D and downstream is 25 D. The 5% blockage is a recorded confinement that conflicts with the 'unbounded' requirement.
  - Time and mesh risks are secondary. Time: dt is 0.01 D/U, max Courant is 0.73526, there are 598.66 steps per period, and the scheme is second-order backward. Mesh: 19160 cells, 160 cells around the cylinder, wall_first_cell_D 0.005. Mesh is a real risk because wake_last_cell_D is 0.55293 and representative_cell_size_D is 0.20424. I would run it next if the domain effect is small.
  - EXPAND_DOMAIN is also the cheapest informative option, at an estimated 763 s against 1258 s for REFINE_MESH and 1088 s for REDUCE_TIME_STEP. The budget is ample: 0 of 6 experiments used and 0 of 12 compute units used.
  - The St frequency resolution is 0.013333 against St 0.16704, about 8%. This is coarser than the 3% tolerance. A change in St between runs smaller than this resolution may not be detectable from the FFT alone. The verifier's St uncertainty (9.904e-06) therefore needs care. The domain run will show whether the Cd difference is resolvable even if the St difference is not.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain-55b85b2cd33e — R0 has 5% blockage with symmetry lateral boundaries, 15 D upstream and 25 D downstream, but the question requires an unbounded stream. Domain confinement is the most likely error to exceed the 3% tolerance, and this is the cheapest experiment (about 763 s).
  - Outcome: executed -> B2_moderate_domain.D2x-44c88f366919 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 8%

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not allowed, because no FAIL invalidates R0.
  - R0 averaging and statistics pass. Cd: 1.858e-06 and 2.492e-05. St: 7.006e-06 and 9.904e-06. The R0 window has 13 cycles.
  - R1 (EXPAND_DOMAIN of R0) moved Cd from 1.3713 to 1.3394 and St from 0.16704 to 0.16421. The verifier records demonstrated changes of 2.37% and 1.72%. Both are below the 0.03 tolerance, so this is not a FAIL.
  - The domain component is still unresolved. The verifier's two-level Richardson estimate with an assumed order p=1 gives 0.1422 for Cd and 0.1035 for St. Both are far above the 1.50% component limit. Only two domain levels exist, so the order is assumed, not measured. A third level is needed to show whether the domain sequence is converging.
  - The domain change is confounded with mesh coarsening. R1 has 26860 cells with representative_cell_size_D 0.34512 and wake_last_cell_D 1.0348. R0 has 0.20424 and 0.55293. R1 is also short, with 6 stationary cycles and 80 convective units. The R0 to R1 difference therefore mixes boundary and far-field/wake-mesh effects.
  - The R1 St frequency resolution is 0.025 and the R0 resolution is 0.013333. Both are coarse against St of about 0.164 to 0.167. The 1.72% St change may be near FFT resolution. The St domain trend is weak evidence until it is confirmed.
  - Mesh and time components remain INCONCLUSIVE because no REFINE_MESH or REDUCE_TIME_STEP run exists. They must be run later. Budget is ample: 1 of 6 experiments and 0.75 of 12 compute units used.
  - Next step: continue the domain sequence from R1 with the same factor of 2.0. This gives three geometrically spaced levels (R0, R1, new) and lets the domain convergence order be measured. R1 is the finest-domain run. The cost is about 1027 s.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on B2_moderate_domain.D2x-44c88f366919 — Domain is the only component with a demonstrated change (Cd 2.37%, St 1.72%). The verifier's domain uncertainty is 0.1422 for Cd and 0.1035 for St, based on an assumed order p=1 from two levels. A third level from R1 with the same factor of 2.0 allows a measured order and a proper extrapolation. It is the most direct way to tell whether the R0 to R1 shift is converging or still of tolerance size.
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
- Experiment cost: {"experiment_cell_steps": 504240000.0, "relative_to_root": 1.7544885177453027, "experiment_wall_seconds": 1962.1250563380017, "n_experiments": 2, "planner_calls": 2, "planner_cost_usd": 0.12438292000000001, "loop_wall_seconds": 62.052667446998385}
