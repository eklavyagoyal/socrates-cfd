# Verification report: I1_force_reference (Bexh)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.1701
- strouhal_number: 0.16344

## VERDICT: **REJECT**


## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **FAIL** force_reference_consistency — force-coefficient normalisation inconsistent with the case: {'magUInf': {'used': 0.16, 'consistent': 0.15}}; coefficients are mis-scaled
- **PASS** physics_regime — sustained periodic lift oscillation present, as expected for 47.0 < Re=100.0 < 188.5
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.007% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.001% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.01e-06 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.24e-05 <= 1.50%
- **PASS** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.14% <= 1.50% (root-to-finest change 0.331%) [three-level, observed order 4.91 outside [0.5, 2.0]x formal; p=min(observed, formal)=2.00 with Fs=3]
- **PASS** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 1.32% <= 1.50% (root-to-finest change 0.860%) [three-level Celik procedure, observed order p=2.42, Fs=1.25]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.11% <= 1.50% (root-to-finest change 0.278%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.0e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.30% <= 1.50% (root-to-finest change 0.075%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.9e-05)]
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.89% > 1.50% but the demonstrated change 0.65% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.6e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.63% > 1.50% but the demonstrated change 0.44% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run I1_force_reference-43978f7eb1a8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── I1_force_reference-43978f7eb1a8
├── mesh_quality: PASS
│   └── I1_force_reference-43978f7eb1a8
├── mass_conservation: PASS
│   └── I1_force_reference-43978f7eb1a8
├── linear_solver_convergence: PASS
│   └── I1_force_reference-43978f7eb1a8
├── courant_number: PASS
│   └── I1_force_reference-43978f7eb1a8
├── reynolds_consistency: PASS
│   └── I1_force_reference-43978f7eb1a8
├── force_reference_consistency: FAIL
│   └── I1_force_reference-43978f7eb1a8
├── physics_regime: PASS
│   └── I1_force_reference-43978f7eb1a8
├── convection_scheme_order: PASS
│   └── I1_force_reference-43978f7eb1a8
├── Averaging window (reported vs stationary value): PASS U=7.17e-05
│   └── I1_force_reference-43978f7eb1a8
│   └── I1_force_reference.long250-5357ce2e7a83
├── Temporal statistics (stationarity, cycles): PASS U=5.01e-06
│   └── I1_force_reference-43978f7eb1a8
│   └── I1_force_reference.long250-5357ce2e7a83
├── Spatial discretisation (mesh sensitivity): PASS U=0.0114
│   └── I1_force_reference.long250-5357ce2e7a83
│   └── I1_force_reference.m1.41-6e947ef8f640
│   └── I1_force_reference.m2-0d93eefe5eb2
├── Temporal discretisation (time-step sensitivity): PASS U=0.0111
│   └── I1_force_reference.long250-5357ce2e7a83
│   └── I1_force_reference.dt0.005-7e9f2608e755
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0389
    └── I1_force_reference.long250-5357ce2e7a83
    └── I1_force_reference.D2x-02155fb848e3

CLAIM: strouhal_number of run I1_force_reference-43978f7eb1a8 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── I1_force_reference-43978f7eb1a8
├── mesh_quality: PASS
│   └── I1_force_reference-43978f7eb1a8
├── mass_conservation: PASS
│   └── I1_force_reference-43978f7eb1a8
├── linear_solver_convergence: PASS
│   └── I1_force_reference-43978f7eb1a8
├── courant_number: PASS
│   └── I1_force_reference-43978f7eb1a8
├── reynolds_consistency: PASS
│   └── I1_force_reference-43978f7eb1a8
├── force_reference_consistency: FAIL
│   └── I1_force_reference-43978f7eb1a8
├── physics_regime: PASS
│   └── I1_force_reference-43978f7eb1a8
├── convection_scheme_order: PASS
│   └── I1_force_reference-43978f7eb1a8
├── Averaging window (reported vs stationary value): PASS U=7.47e-06
│   └── I1_force_reference-43978f7eb1a8
│   └── I1_force_reference.long250-5357ce2e7a83
├── Temporal statistics (stationarity, cycles): PASS U=1.24e-05
│   └── I1_force_reference-43978f7eb1a8
│   └── I1_force_reference.long250-5357ce2e7a83
├── Spatial discretisation (mesh sensitivity): PASS U=0.0132
│   └── I1_force_reference.long250-5357ce2e7a83
│   └── I1_force_reference.m1.41-6e947ef8f640
│   └── I1_force_reference.m2-0d93eefe5eb2
├── Temporal discretisation (time-step sensitivity): PASS U=0.003
│   └── I1_force_reference.long250-5357ce2e7a83
│   └── I1_force_reference.dt0.005-7e9f2608e755
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0263
    └── I1_force_reference.long250-5357ce2e7a83
    └── I1_force_reference.D2x-02155fb848e3

```

## EXPERIMENT HISTORY

Run I1_force_reference-43978f7eb1a8: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

Run I1_force_reference.long250-5357ce2e7a83: RUN_LONGER from I1_force_reference-43978f7eb1a8 ().
  - Observation: mean_drag_coefficient 1.1699 → 1.17 (+0.00%).
  - Observation: strouhal_number 0.16343 → 0.16344 (+0.00%).

Run I1_force_reference.m1.41-6e947ef8f640: REFINE_MESH from I1_force_reference-43978f7eb1a8 ().
  - Observation: mean_drag_coefficient 1.1699 → 1.1733 (+0.28%).
  - Observation: strouhal_number 0.16343 → 0.16443 (+0.61%).

Run I1_force_reference.m2-0d93eefe5eb2: REFINE_MESH from I1_force_reference.m1.41-6e947ef8f640 ().
  - Observation: mean_drag_coefficient 1.1733 → 1.1739 (+0.05%).
  - Observation: strouhal_number 0.16443 → 0.16485 (+0.26%).

Run I1_force_reference.dt0.005-7e9f2608e755: REDUCE_TIME_STEP from I1_force_reference-43978f7eb1a8 ().
  - Observation: mean_drag_coefficient 1.1699 → 1.1667 (-0.27%).
  - Observation: strouhal_number 0.16343 → 0.16356 (+0.08%).

Run I1_force_reference.D2x-02155fb848e3: EXPAND_DOMAIN from I1_force_reference-43978f7eb1a8 ().
  - Observation: mean_drag_coefficient 1.1699 → 1.1624 (-0.64%).
  - Observation: strouhal_number 0.16343 → 0.16272 (-0.43%).

## FINAL JUSTIFICATION

Failed checks (measured): force_reference_consistency.
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=PASS, time=PASS, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — domain.
- strouhal_number: not established — domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `I1_force_reference-43978f7eb1a8` status=completed parent=None created=2026-10-19T07:16:32+00:00 wall=4804 s; record: results/runs/I1_force_reference-43978f7eb1a8/run.json
- `I1_force_reference.long250-5357ce2e7a83` status=completed parent=I1_force_reference-43978f7eb1a8 created=2026-10-19T11:04:04+00:00 wall=1040 s; record: results/runs/I1_force_reference.long250-5357ce2e7a83/run.json
- `I1_force_reference.m1.41-6e947ef8f640` status=completed parent=I1_force_reference-43978f7eb1a8 created=2026-10-19T12:12:03+00:00 wall=2719 s; record: results/runs/I1_force_reference.m1.41-6e947ef8f640/run.json
- `I1_force_reference.m2-0d93eefe5eb2` status=completed parent=I1_force_reference.m1.41-6e947ef8f640 created=2026-10-19T14:11:04+00:00 wall=7113 s; record: results/runs/I1_force_reference.m2-0d93eefe5eb2/run.json
- `I1_force_reference.dt0.005-7e9f2608e755` status=completed parent=I1_force_reference-43978f7eb1a8 created=2026-10-19T16:42:44+00:00 wall=1352 s; record: results/runs/I1_force_reference.dt0.005-7e9f2608e755/run.json
- `I1_force_reference.D2x-02155fb848e3` status=completed parent=I1_force_reference-43978f7eb1a8 created=2026-10-19T18:04:28+00:00 wall=1081 s; record: results/runs/I1_force_reference.D2x-02155fb848e3/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
