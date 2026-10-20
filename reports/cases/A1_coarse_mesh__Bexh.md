# Verification report: A1_coarse_mesh (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2951
- strouhal_number: 0.15561

## VERDICT: **REJECT**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.39 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.26e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.56e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 4.51% > 1.50% but the demonstrated change 2.71% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=1.96, Fs=1.25]
- **FAIL** mesh_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 4.78% under mesh refinement (> tau=3%); its value is not converged to the requested tolerance
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 0.97% <= 1.50% (root-to-finest change 0.241%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 4.7e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.56% <= 1.50% (root-to-finest change 0.141%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 6.9e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.28% > 1.50% but the demonstrated change 0.71% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.95% > 1.50% but the demonstrated change 0.49% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run A1_coarse_mesh-8db269c22d05 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── mesh_quality: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── mass_conservation: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── linear_solver_convergence: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── courant_number: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── reynolds_consistency: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── force_reference_consistency: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── physics_regime: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── convection_scheme_order: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── Averaging window (reported vs stationary value): PASS U=6.36e-06
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.long250-430da87fc0b2
├── Temporal statistics (stationarity, cycles): PASS U=1.26e-06
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.long250-430da87fc0b2
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0451
│   └── A1_coarse_mesh.long250-430da87fc0b2
│   └── A1_coarse_mesh.m0.707-a67b9e3443d4
│   └── A1_coarse_mesh.m1-26cfdbe9e736
├── Temporal discretisation (time-step sensitivity): PASS U=0.00965
│   └── A1_coarse_mesh.long250-430da87fc0b2
│   └── A1_coarse_mesh.dt0.005-7544dcbae909
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0428
    └── A1_coarse_mesh.long250-430da87fc0b2
    └── A1_coarse_mesh.D2x-0c836e0d97c0

CLAIM: strouhal_number of run A1_coarse_mesh-8db269c22d05 is reliable to within 3%  [REJECT]
├── solver_completion: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── mesh_quality: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── mass_conservation: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── linear_solver_convergence: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── courant_number: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── reynolds_consistency: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── force_reference_consistency: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── physics_regime: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── convection_scheme_order: PASS
│   └── A1_coarse_mesh-8db269c22d05
├── Averaging window (reported vs stationary value): PASS U=1.3e-05
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.long250-430da87fc0b2
├── Temporal statistics (stationarity, cycles): PASS U=1.56e-05
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.long250-430da87fc0b2
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── A1_coarse_mesh.long250-430da87fc0b2
│   └── A1_coarse_mesh.m0.707-a67b9e3443d4
│   └── A1_coarse_mesh.m1-26cfdbe9e736
├── Temporal discretisation (time-step sensitivity): PASS U=0.00564
│   └── A1_coarse_mesh.long250-430da87fc0b2
│   └── A1_coarse_mesh.dt0.005-7544dcbae909
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0295
    └── A1_coarse_mesh.long250-430da87fc0b2
    └── A1_coarse_mesh.D2x-0c836e0d97c0

```

## EXPERIMENT HISTORY

Run A1_coarse_mesh-8db269c22d05: submitted simulation (7616 cells, dt=0.01 D/U, half-height 40 D).

Run A1_coarse_mesh.long250-430da87fc0b2: RUN_LONGER from A1_coarse_mesh-8db269c22d05 ().
  - Observation: mean_drag_coefficient 1.2951 → 1.2951 (+0.00%).
  - Observation: strouhal_number 0.15561 → 0.15561 (+0.00%).

Run A1_coarse_mesh.m0.707-a67b9e3443d4: REFINE_MESH from A1_coarse_mesh-8db269c22d05 ().
  - Observation: mean_drag_coefficient 1.2951 → 1.3189 (+1.84%).
  - Observation: strouhal_number 0.15561 → 0.16089 (+3.39%).

Run A1_coarse_mesh.m1-26cfdbe9e736: REFINE_MESH from A1_coarse_mesh.m0.707-a67b9e3443d4 ().
  - Observation: mean_drag_coefficient 1.3189 → 1.3311 (+0.93%).
  - Observation: strouhal_number 0.16089 → 0.16343 (+1.58%).

Run A1_coarse_mesh.dt0.005-7544dcbae909: REDUCE_TIME_STEP from A1_coarse_mesh-8db269c22d05 ().
  - Observation: mean_drag_coefficient 1.2951 → 1.292 (-0.24%).
  - Observation: strouhal_number 0.15561 → 0.15583 (+0.14%).

Run A1_coarse_mesh.D2x-0c836e0d97c0: EXPAND_DOMAIN from A1_coarse_mesh-8db269c22d05 ().
  - Observation: mean_drag_coefficient 1.2951 → 1.2859 (-0.70%).
  - Observation: strouhal_number 0.15561 → 0.15485 (-0.49%).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_sensitivity[strouhal_number].
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=FAIL, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A1_coarse_mesh-8db269c22d05` status=completed parent=None created=2026-10-19T07:02:08+00:00 wall=283.8 s; record: results/runs/A1_coarse_mesh-8db269c22d05/run.json
- `A1_coarse_mesh.long250-430da87fc0b2` status=completed parent=A1_coarse_mesh-8db269c22d05 created=2026-10-19T13:28:02+00:00 wall=172.5 s; record: results/runs/A1_coarse_mesh.long250-430da87fc0b2/run.json
- `A1_coarse_mesh.m0.707-a67b9e3443d4` status=completed parent=A1_coarse_mesh-8db269c22d05 created=2026-10-19T08:25:17+00:00 wall=379.7 s; record: results/runs/A1_coarse_mesh.m0.707-a67b9e3443d4/run.json
- `A1_coarse_mesh.m1-26cfdbe9e736` status=completed parent=A1_coarse_mesh.m0.707-a67b9e3443d4 created=2026-10-19T17:02:34+00:00 wall=807.3 s; record: results/runs/A1_coarse_mesh.m1-26cfdbe9e736/run.json
- `A1_coarse_mesh.dt0.005-7544dcbae909` status=completed parent=A1_coarse_mesh-8db269c22d05 created=2026-10-19T18:43:58+00:00 wall=251.9 s; record: results/runs/A1_coarse_mesh.dt0.005-7544dcbae909/run.json
- `A1_coarse_mesh.D2x-0c836e0d97c0` status=completed parent=A1_coarse_mesh-8db269c22d05 created=2026-10-20T06:49:23+00:00 wall=269.1 s; record: results/runs/A1_coarse_mesh.D2x-0c836e0d97c0/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
