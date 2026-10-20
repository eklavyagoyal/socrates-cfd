# Verification report: A2_moderate_mesh (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3221
- strouhal_number: 0.16157

## VERDICT: **INCONCLUSIVE**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.56 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.006% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 9.34e-07 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.61e-06 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.60% > 1.50% but the demonstrated change 1.06% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.49, Fs=1.25]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 2.58% > 1.50% but the demonstrated change 1.75% <= tau; more refinement would be needed [three-level Celik procedure, observed order p=2.71, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.18% <= 1.50% (root-to-finest change 0.294%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.2e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.36% <= 1.50% (root-to-finest change 0.089%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.4e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 4.16% > 1.50% but the demonstrated change 0.69% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.81% > 1.50% but the demonstrated change 0.47% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.2e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=6.17e-05
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
├── Temporal statistics (stationarity, cycles): PASS U=9.34e-07
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.016
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-69c39fb43565
├── Temporal discretisation (time-step sensitivity): PASS U=0.0118
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0416
    └── A2_moderate_mesh.long250-4d9d2cfead3f
    └── A2_moderate_mesh.D2x-4a8a18327a27

CLAIM: strouhal_number of run A2_moderate_mesh-1c5ea01594aa is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mesh_quality: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── mass_conservation: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── linear_solver_convergence: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── courant_number: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── reynolds_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── force_reference_consistency: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── physics_regime: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── convection_scheme_order: PASS
│   └── A2_moderate_mesh-1c5ea01594aa
├── Averaging window (reported vs stationary value): PASS U=5.07e-06
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
├── Temporal statistics (stationarity, cycles): PASS U=1.61e-06
│   └── A2_moderate_mesh-1c5ea01594aa
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0258
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
│   └── A2_moderate_mesh.m1.06-c5d153eb41a5
│   └── A2_moderate_mesh.m1.5-69c39fb43565
├── Temporal discretisation (time-step sensitivity): PASS U=0.00356
│   └── A2_moderate_mesh.long250-4d9d2cfead3f
│   └── A2_moderate_mesh.dt0.005-4720e4eddcde
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0281
    └── A2_moderate_mesh.long250-4d9d2cfead3f
    └── A2_moderate_mesh.D2x-4a8a18327a27

```

## EXPERIMENT HISTORY

Run A2_moderate_mesh-1c5ea01594aa: submitted simulation (17162 cells, dt=0.01 D/U, half-height 40 D).

Run A2_moderate_mesh.long250-4d9d2cfead3f: RUN_LONGER from A2_moderate_mesh-1c5ea01594aa ().
  - Observation: mean_drag_coefficient 1.3222 → 1.3222 (+0.00%).
  - Observation: strouhal_number 0.16157 → 0.16157 (+0.00%).

Run A2_moderate_mesh.m1.06-c5d153eb41a5: REFINE_MESH from A2_moderate_mesh-1c5ea01594aa ().
  - Observation: mean_drag_coefficient 1.3222 → 1.3321 (+0.75%).
  - Observation: strouhal_number 0.16157 → 0.16364 (+1.28%).

Run A2_moderate_mesh.m1.5-69c39fb43565: REFINE_MESH from A2_moderate_mesh.m1.06-c5d153eb41a5 ().
  - Observation: mean_drag_coefficient 1.3321 → 1.3363 (+0.32%).
  - Observation: strouhal_number 0.16364 → 0.16446 (+0.50%).

Run A2_moderate_mesh.dt0.005-4720e4eddcde: REDUCE_TIME_STEP from A2_moderate_mesh-1c5ea01594aa ().
  - Observation: mean_drag_coefficient 1.3222 → 1.3183 (-0.29%).
  - Observation: strouhal_number 0.16157 → 0.16172 (+0.09%).

Run A2_moderate_mesh.D2x-4a8a18327a27: EXPAND_DOMAIN from A2_moderate_mesh-1c5ea01594aa ().
  - Observation: mean_drag_coefficient 1.3222 → 1.3131 (-0.69%).
  - Observation: strouhal_number 0.16157 → 0.16082 (-0.46%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, domain.
- strouhal_number: not established — mesh, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A2_moderate_mesh-1c5ea01594aa` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=2124 s; record: results/runs/A2_moderate_mesh-1c5ea01594aa/run.json
- `A2_moderate_mesh.long250-4d9d2cfead3f` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T13:28:02+00:00 wall=455.3 s; record: results/runs/A2_moderate_mesh.long250-4d9d2cfead3f/run.json
- `A2_moderate_mesh.m1.06-c5d153eb41a5` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T09:43:44+00:00 wall=1223 s; record: results/runs/A2_moderate_mesh.m1.06-c5d153eb41a5/run.json
- `A2_moderate_mesh.m1.5-69c39fb43565` status=completed parent=A2_moderate_mesh.m1.06-c5d153eb41a5 created=2026-10-19T10:04:58+00:00 wall=2428 s; record: results/runs/A2_moderate_mesh.m1.5-69c39fb43565/run.json
- `A2_moderate_mesh.dt0.005-4720e4eddcde` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:07:48+00:00 wall=764.5 s; record: results/runs/A2_moderate_mesh.dt0.005-4720e4eddcde/run.json
- `A2_moderate_mesh.D2x-4a8a18327a27` status=completed parent=A2_moderate_mesh-1c5ea01594aa created=2026-10-19T11:38:04+00:00 wall=438.6 s; record: results/runs/A2_moderate_mesh.D2x-4a8a18327a27/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
