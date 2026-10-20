# Verification report: B2_moderate_domain (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3713
- strouhal_number: 0.16704

## VERDICT: **INCONCLUSIVE**


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
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.000% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.53e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 8.85e-06 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 0.57% <= 1.50% (root-to-finest change 0.392%) [three-level Celik procedure, observed order p=2.89, Fs=1.25]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.18% <= 1.50% (root-to-finest change 0.808%) [three-level Celik procedure, observed order p=2.82, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.12% <= 1.50% (root-to-finest change 0.281%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 1.9e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.44% <= 1.50% (root-to-finest change 0.111%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.9e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 14.23% > 1.50% but the demonstrated change 2.37% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.8e-04)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 10.35% > 1.50% but the demonstrated change 1.72% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-04)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run B2_moderate_domain-55b85b2cd33e is reliable to within 3%  [INCONCLUSIVE]
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
├── Averaging window (reported vs stationary value): PASS U=2.63e-06
│   └── B2_moderate_domain-55b85b2cd33e
│   └── B2_moderate_domain.long250-c6e14395cdc1
├── Temporal statistics (stationarity, cycles): PASS U=1.53e-06
│   └── B2_moderate_domain-55b85b2cd33e
│   └── B2_moderate_domain.long250-c6e14395cdc1
├── Spatial discretisation (mesh sensitivity): PASS U=0.00566
│   └── B2_moderate_domain.long250-c6e14395cdc1
│   └── B2_moderate_domain.m1.41-d86d8d024222
│   └── B2_moderate_domain.m2-cc5b5f3a7d40
├── Temporal discretisation (time-step sensitivity): PASS U=0.0112
│   └── B2_moderate_domain.long250-c6e14395cdc1
│   └── B2_moderate_domain.dt0.005-525718785aa3
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.142
    └── B2_moderate_domain.long250-c6e14395cdc1
    └── B2_moderate_domain.D2x-44c88f366919

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
├── Averaging window (reported vs stationary value): PASS U=3.15e-06
│   └── B2_moderate_domain-55b85b2cd33e
│   └── B2_moderate_domain.long250-c6e14395cdc1
├── Temporal statistics (stationarity, cycles): PASS U=8.85e-06
│   └── B2_moderate_domain-55b85b2cd33e
│   └── B2_moderate_domain.long250-c6e14395cdc1
├── Spatial discretisation (mesh sensitivity): PASS U=0.0118
│   └── B2_moderate_domain.long250-c6e14395cdc1
│   └── B2_moderate_domain.m1.41-d86d8d024222
│   └── B2_moderate_domain.m2-cc5b5f3a7d40
├── Temporal discretisation (time-step sensitivity): PASS U=0.00443
│   └── B2_moderate_domain.long250-c6e14395cdc1
│   └── B2_moderate_domain.dt0.005-525718785aa3
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.103
    └── B2_moderate_domain.long250-c6e14395cdc1
    └── B2_moderate_domain.D2x-44c88f366919

```

## EXPERIMENT HISTORY

Run B2_moderate_domain-55b85b2cd33e: submitted simulation (19160 cells, dt=0.01 D/U, half-height 10 D).

Run B2_moderate_domain.long250-c6e14395cdc1: RUN_LONGER from B2_moderate_domain-55b85b2cd33e ().
  - Observation: mean_drag_coefficient 1.3713 → 1.3713 (+0.00%).
  - Observation: strouhal_number 0.16704 → 0.16704 (+0.00%).

Run B2_moderate_domain.m1.41-d86d8d024222: REFINE_MESH from B2_moderate_domain-55b85b2cd33e ().
  - Observation: mean_drag_coefficient 1.3713 → 1.3752 (+0.29%).
  - Observation: strouhal_number 0.16704 → 0.16803 (+0.59%).

Run B2_moderate_domain.m2-cc5b5f3a7d40: REFINE_MESH from B2_moderate_domain.m1.41-d86d8d024222 ().
  - Observation: mean_drag_coefficient 1.3752 → 1.3767 (+0.11%).
  - Observation: strouhal_number 0.16803 → 0.1684 (+0.22%).

Run B2_moderate_domain.dt0.005-525718785aa3: REDUCE_TIME_STEP from B2_moderate_domain-55b85b2cd33e ().
  - Observation: mean_drag_coefficient 1.3713 → 1.3674 (-0.28%).
  - Observation: strouhal_number 0.16704 → 0.16723 (+0.11%).

Run B2_moderate_domain.D2x-44c88f366919: EXPAND_DOMAIN from B2_moderate_domain-55b85b2cd33e ().
  - Observation: mean_drag_coefficient 1.3713 → 1.3395 (-2.32%).
  - Observation: strouhal_number 0.16704 → 0.16421 (-1.70%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `B2_moderate_domain-55b85b2cd33e` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=1020 s; record: results/runs/B2_moderate_domain-55b85b2cd33e/run.json
- `B2_moderate_domain.long250-c6e14395cdc1` status=completed parent=B2_moderate_domain-55b85b2cd33e created=2026-10-19T11:04:04+00:00 wall=632.1 s; record: results/runs/B2_moderate_domain.long250-c6e14395cdc1/run.json
- `B2_moderate_domain.m1.41-d86d8d024222` status=completed parent=B2_moderate_domain-55b85b2cd33e created=2026-10-19T09:08:42+00:00 wall=1687 s; record: results/runs/B2_moderate_domain.m1.41-d86d8d024222/run.json
- `B2_moderate_domain.m2-cc5b5f3a7d40` status=completed parent=B2_moderate_domain.m1.41-d86d8d024222 created=2026-10-20T03:41:02+00:00 wall=4336 s; record: results/runs/B2_moderate_domain.m2-cc5b5f3a7d40/run.json
- `B2_moderate_domain.dt0.005-525718785aa3` status=completed parent=B2_moderate_domain-55b85b2cd33e created=2026-10-20T04:53:21+00:00 wall=968.7 s; record: results/runs/B2_moderate_domain.dt0.005-525718785aa3/run.json
- `B2_moderate_domain.D2x-44c88f366919` status=completed parent=B2_moderate_domain-55b85b2cd33e created=2026-10-19T09:09:24+00:00 wall=924.8 s; record: results/runs/B2_moderate_domain.D2x-44c88f366919/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
