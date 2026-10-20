# Verification report: A1_coarse_mesh (C-llm)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2951
- strouhal_number: 0.15561

## VERDICT: **REJECT**

Stop reason: deterministic verifier verdict is decisive.

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
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.005% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 0.002% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 1.88e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 1.62e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 10.79% > 1.50% but the demonstrated change 2.70% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 3.1e-04)]
- **FAIL** mesh_sensitivity [strouhal_number] — strouhal_number of the run under verification changes by 4.78% under mesh refinement (> tau=3%); its value is not converged to the requested tolerance
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — no EXPAND_DOMAIN experiment has been run; domain error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — no EXPAND_DOMAIN experiment has been run; domain error of strouhal_number is unknown

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
├── Averaging window (reported vs stationary value): PASS U=5e-05
│   └── A1_coarse_mesh-8db269c22d05
├── Temporal statistics (stationarity, cycles): PASS U=0.000188
│   └── A1_coarse_mesh-8db269c22d05
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.108
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.m1-127e3ddbb1e9
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── A1_coarse_mesh-8db269c22d05
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── A1_coarse_mesh-8db269c22d05

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
├── Averaging window (reported vs stationary value): PASS U=2.35e-05
│   └── A1_coarse_mesh-8db269c22d05
├── Temporal statistics (stationarity, cycles): PASS U=0.000162
│   └── A1_coarse_mesh-8db269c22d05
├── Spatial discretisation (mesh sensitivity): FAIL
│   └── A1_coarse_mesh-8db269c22d05
│   └── A1_coarse_mesh.m1-127e3ddbb1e9
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── A1_coarse_mesh-8db269c22d05
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE
    └── A1_coarse_mesh-8db269c22d05

```

## EXPERIMENT HISTORY

Run A1_coarse_mesh-8db269c22d05: submitted simulation (7616 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. The mesh, time and domain components are unmeasured for both mean_drag_coefficient and strouhal_number.
  - R0 averaging and statistics components pass and are tiny. Drag: 4.998e-05 averaging and 0.000188 statistics. Strouhal: 2.353e-05 averaging and 0.0001616 statistics. Both are far below the 0.03 tolerance, so more shedding cycles would add little.
  - R0 mesh is very coarse for a wake-shedding problem: 7616 cells, representative_cell_size_D 0.91664, wake_last_cell_D 2.0173, wake_cells_streamwise 56 and cells_around_cylinder 80. This is the most likely source of an error larger than 3 %.
  - Time resolution looks adequate: time_step_convective_units 0.01, steps_per_shedding_period 642.64 and max Courant 0.38878. A time-step error large enough to matter is less likely than a mesh error, though it is unmeasured.
  - Domain: blockage_ratio 0.0125, upstream_D 30, downstream_D 50 and half_height_D 40 with symmetryPlane sides. These are moderate and the effect is unmeasured. Lower priority than mesh.
  - The stationary window start is capped by MSER (stationary_window_start_is_mser_cap true, start 67.598). Drift is small (mean_drag_coefficient_drift_rel 0.00018797) and the run has 12 stationary cycles, so this is a minor concern.
  - Next experiment: REFINE_MESH on R0 with the maximum factor 2.0, to maximise the detectable change on this coarse mesh. It costs about 302 s, which is small against the 12x compute budget with 0 of 6 experiments used.
  - Requested: REFINE_MESH {'factor': 2.0} on A1_coarse_mesh-8db269c22d05 — R0 has the coarsest-looking resolution of all the unverified components (7616 cells, wake_last_cell_D 2.0173, representative_cell_size_D 0.91664). Mesh error is the most likely flaw to change the answer by more than the 3 % tolerance. The maximum factor gives the strongest signal on a coarse mesh at a cost of about 302 s.
  - Outcome: executed -> A1_coarse_mesh.m1-127e3ddbb1e9 (completed)

Run A1_coarse_mesh.m1-127e3ddbb1e9: REFINE_MESH from A1_coarse_mesh-8db269c22d05 (averaging.start_time: 75→40, mesh.refinement: 0.5→1, time.end_time: 150→80).
  - Observation: mean_drag_coefficient 1.2951 → 1.331 (+2.78%).
  - Observation: strouhal_number 0.15561 → 0.16342 (+5.02%).

## FINAL JUSTIFICATION

Failed checks (measured): mesh_sensitivity[strouhal_number].
- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: REJECT (components: averaging=PASS, statistics=PASS, mesh=FAIL, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `A1_coarse_mesh-8db269c22d05` status=completed parent=None created=2026-10-19T07:02:08+00:00 wall=283.8 s; record: results/runs/A1_coarse_mesh-8db269c22d05/run.json
- `A1_coarse_mesh.m1-127e3ddbb1e9` status=completed parent=A1_coarse_mesh-8db269c22d05 created=2026-10-20T01:15:57+00:00 wall=663.6 s; record: results/runs/A1_coarse_mesh.m1-127e3ddbb1e9/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 244640000.0, "relative_to_root": 2.141456582633053, "experiment_wall_seconds": 663.6272216059997, "n_experiments": 1, "planner_calls": 1, "planner_cost_usd": 0.05224191, "loop_wall_seconds": 6694.275413182}
