# Verification report: G1_premature_averaging (C-llm-r3)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.2961
- strouhal_number: 0.16129

## VERDICT: **INCONCLUSIVE**

Stop reason: planner stopped.

## EVIDENCE

- **PASS** solver_completion — solver ran to its configured end and printed 'End'
- **PASS** mesh_quality — checkMesh reports 'Mesh OK'; non-orthogonality, skewness and aspect ratio within OpenFOAM's limits. This shows the mesh is valid, NOT that it resolves the flow.
- **PASS** mass_conservation — max relative boundary-flux imbalance 8.33e-11 <= 1.50e-03; cannot bias the requested quantities beyond tau/10
- **PASS** linear_solver_convergence — final pressure solve reached the configured tolerance in 100.0% of steps
- **PASS** courant_number — max Courant number 0.73 < 1.0 (PISO mode). Stability/accuracy guideline only; temporal discretisation error is not quantified by this.
- **PASS** reynolds_consistency — case Re=100 matches spec Re=100
- **PASS** force_reference_consistency — magUInf equals inlet velocity and Aref equals D x mesh span
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +25.8% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 2.609% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.294% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 9.23e-04 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 7.00e-04 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.83% > 1.50% but the demonstrated change 0.31% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 9.2e-04)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 3.74% > 1.50% but the demonstrated change 0.63% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.0e-04)]
- **INCONCLUSIVE** time_sensitivity [mean_drag_coefficient] — no REDUCE_TIME_STEP experiment has been run; time error of mean_drag_coefficient is unknown
- **INCONCLUSIVE** time_sensitivity [strouhal_number] — no REDUCE_TIME_STEP experiment has been run; time error of strouhal_number is unknown
- **INCONCLUSIVE** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 3.77% > 1.50% but the demonstrated change 0.63% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.4e-03)]
- **INCONCLUSIVE** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 2.53% > 1.50% but the demonstrated change 0.42% <= tau; more refinement would be needed [two-level Richardson, assumed order p=1, Fs=3 (noise floor 1.3e-03)]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0261
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long100-bf9115c8c872
├── Temporal statistics (stationarity, cycles): PASS U=0.000923
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long100-bf9115c8c872
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0183
│   └── G1_premature_averaging.long100-bf9115c8c872
│   └── G1_premature_averaging.m1.41-f8bb4a846d17
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0377
    └── G1_premature_averaging.long100-bf9115c8c872
    └── G1_premature_averaging.D2x-6e506d02ef0a

CLAIM: strouhal_number of run G1_premature_averaging-17c0143468d7 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mesh_quality: PASS
│   └── G1_premature_averaging-17c0143468d7
├── mass_conservation: PASS
│   └── G1_premature_averaging-17c0143468d7
├── linear_solver_convergence: PASS
│   └── G1_premature_averaging-17c0143468d7
├── courant_number: PASS
│   └── G1_premature_averaging-17c0143468d7
├── reynolds_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── force_reference_consistency: PASS
│   └── G1_premature_averaging-17c0143468d7
├── physics_regime: INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
├── convection_scheme_order: PASS
│   └── G1_premature_averaging-17c0143468d7
├── Averaging window (reported vs stationary value): PASS U=0.0129
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long100-bf9115c8c872
├── Temporal statistics (stationarity, cycles): PASS U=0.0007
│   └── G1_premature_averaging-17c0143468d7
│   └── G1_premature_averaging.long100-bf9115c8c872
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0374
│   └── G1_premature_averaging.long100-bf9115c8c872
│   └── G1_premature_averaging.m1.41-f8bb4a846d17
├── Temporal discretisation (time-step sensitivity): INCONCLUSIVE
│   └── G1_premature_averaging-17c0143468d7
└── Artificial boundaries (domain sensitivity): INCONCLUSIVE U=0.0253
    └── G1_premature_averaging.long100-bf9115c8c872
    └── G1_premature_averaging.D2x-6e506d02ef0a

```

## EXPERIMENT HISTORY

Run G1_premature_averaging-17c0143468d7: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - Deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT is not allowed. Nothing measured invalidates R0, so REJECT is not justified either.
  - R0 passes the hygiene checks: solver_completion, mesh_quality, mass_conservation (8.333e-11), linear_solver_convergence, courant_number (0.7337), reynolds_consistency, force_reference_consistency and convection_scheme_order. These show the run is valid. They do not show that the answer is converged.
  - physics_regime is INCONCLUSIVE. The lift amplitude changes by +25.8% across the analysed window, so R0 is not yet a sustained limit cycle (decaying or still growing). The record ends at 40 convective units.
  - The stationary window starts at 15.276, and stationary_window_start_is_mser_cap is true. The start of stationarity is therefore capped, not detected, and the transient may extend further.
  - The stationary window has only 3 cycles (< 4). Drag CI95 is 0.044509 and drift is 0.040105 relative. Strouhal statistical uncertainty is 3.58%. Drag drift (4.01%) and Strouhal uncertainty (3.58%) both exceed the 0.03 tolerance, and the required component budget is 0.5*tolerance.
  - Drag differs between the submitted setup (1.2961) and the stationary window (1.3039). Strouhal differs between the submitted setup (0.16129) and the stationary window (0.16058, FFT 0.16169). The FFT frequency resolution is 0.033333, which is coarse relative to the 3% tolerance.
  - Mesh, time and domain components are all unmeasured. Any refinement, time-step or domain experiment run now would compare two short, non-stationary records. Differences from the transient would be confounded with discretisation or truncation error. RUN_LONGER is therefore the prerequisite experiment: it tests whether the transient has ended and gives the statistics needed to interpret later comparisons.
  - Domain extents (30D upstream, 50D downstream, 40D half height, blockage 0.0125) are generous. Mesh (0.45745 D representative cell size) and time step (0.01) are the next suspects once a stationary reference exists.
  - Requested: RUN_LONGER {'additional_convective_times': 60.0} on G1_premature_averaging-17c0143468d7 — R0's lift amplitude is still changing (+25.8%) and its window has only 3 cycles, with the window start capped by MSER. Statistics, averaging and physics_regime are all INCONCLUSIVE because of this. Any mesh, time or domain comparison needs a stationary reference record first. Extending R0 costs the least of the primitives and is the prerequisite for interpreting the others. The 60-unit extension costs about 1.5x the root. That leaves budget for later experiments within the 12x compute cap, which the full default 100-unit extension plus the other three primitives would exceed.
  - Outcome: executed -> G1_premature_averaging.long100-bf9115c8c872 (completed)
  - Numeric audit: 1 number(s) not traceable to evidence: 60

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks, so ACCEPT and REJECT are both unavailable. The mesh, time and domain components are unmeasured for both quantities.
  - R1 (RUN_LONGER, 100 convective units) fixed the statistical problem. Its stationary window has 8 cycles. Drag CI95 is 0.00037742, drift is 0.00092276 and half-difference is 0.00041292. The Strouhal numbers are 0.1634 (window) and 0.16342 (FFT). The statistics component passes: 0.0009228 for drag and 0.0006999 for Strouhal.
  - R0 as submitted is biased against R1's stationary window. Drag is 1.2961 against 1.3308, flagged as a 2.609% bias. Strouhal is 0.16129 against 0.1634, flagged as a 1.294% bias. These averaging biases are added linearly to the budget. They use up most of the 0.03 tolerance for drag, leaving little room for discretisation error.
  - The R0 stationary-window values moved a lot with run length. Drag went from 1.3039 to 1.3308, rms Cl from 0.19955 to 0.22827, and Cl amplitude mean from 0.28229 to 0.32291. The record is long enough that the transient has probably ended. physics_regime is still INCONCLUSIVE, and its recorded evidence is R0 only. In R1 the stationary window start (46.311) is still flagged as an MSER cap.
  - The domain is generous: 30D upstream, 50D downstream, 40D half-height, blockage ratio 0.0125. The time step is 0.01 with max Courant 0.73373 and a second-order backward scheme. The mesh is the coarsest-looking element: representative cell size 0.45745 D, wake last cell 1.0209 D, 30580 cells. It is the most likely source of an error larger than the tolerance. The R0-to-R1 change in Cl amplitude shows the wake dynamics are sensitive.
  - Choose REFINE_MESH with parent R1. R1 is the only run with a stationary reference window, so a refined child compared against it is not confounded by transient. The default factor 1.4142 keeps the cost near the listed estimate of 1812 s. Compute used is 1.5 of 12.0 relative to root. The listed costs suggest mesh, time and domain may not all fit in the remaining budget, so the most informative one is run first.
  - Requested: REFINE_MESH {'factor': 1.4142} on G1_premature_averaging.long100-bf9115c8c872 — Mesh resolution is the most likely source of an error larger than the tolerance (0.45745 D representative cell size, 1.0209 D last wake cell). The mesh component is unmeasured for both quantities. R1 is the stationary reference, with 8 cycles and drag CI95 0.00037742, so a refined child can be compared against it cleanly.
  - Outcome: executed -> G1_premature_averaging.m1.41-f8bb4a846d17 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and nothing measured justifies REJECT.
  - R1 fixed the statistics problem. It has 8 stationary cycles, drag CI95 0.00037742 and drift 0.00092276. Both statistics components pass (drag 0.0009228, Strouhal 0.0006999).
  - R2 is the refined mesh (61366 cells vs 30580). Its stationary drag is 1.3349 against R1's 1.3308, and its Strouhal number is 0.16443 against 0.1634. The two-level Richardson estimate at assumed p=2 gives a mesh uncertainty of 0.01832 for drag and 0.03739 for Strouhal. The Strouhal figure is above the 0.03 tolerance. The demonstrated changes (0.31% and 0.63%) are within tolerance, so the verifier marks the mesh component INCONCLUSIVE rather than FAIL.
  - R1 to R2 changed the time step (0.01 to 0.0086734) along with the mesh. The mesh estimate therefore also contains some temporal effect. The time component is still unmeasured, because no REDUCE_TIME_STEP run exists.
  - Domain sensitivity is unmeasured for both quantities. No EXPAND_DOMAIN run exists. The domain is 30D upstream, 50D downstream and 40D half-height, with symmetryPlane lateral boundaries and zeroGradient inlet pressure, which is a boundary-condition set the data do not exonerate.
  - The submitted root R0 is biased against the stationary window. Averaging bias is 0.02609 for drag and 0.01294 for Strouhal. This bias is added linearly, so it leaves little budget for the other components.
  - The physics_regime check is INCONCLUSIVE. It cites only R0's +25.8% lift amplitude change, and the stationary window starts of R0, R1 and R2 are all flagged as MSER caps.
  - Budget: 2 of 6 experiments used and 6.13 of 12.0 compute units used. A root run costs 391.64 s, so about 5.87 units (~2300 s) remain. A REFINE_MESH from R2 (4164 s) and every other experiment with parent R2 are unaffordable. With parent R1, EXPAND_DOMAIN (1040 s) is the cheapest primitive on an unmeasured component, and RUN_LONGER (979 s) could still follow it.
  - EXPAND_DOMAIN on R1 is the best choice. It measures one whole missing component at the lowest cost. It also leaves room for one more cheap run. Domain truncation is a plausible source of a Strouhal shift that the recorded configuration cannot rule out.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on G1_premature_averaging.long100-bf9115c8c872 — The domain component is unmeasured for both quantities and cannot be inferred from the recorded configuration. EXPAND_DOMAIN is the cheapest primitive for an unmeasured component (1040 s from R1), so it is affordable within the remaining budget. R1 is the stationary 8-cycle reference on the same mesh and time step as the expanded run, so any change can be attributed to the domain.
  - Outcome: executed -> G1_premature_averaging.D2x-6e506d02ef0a (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 5.87, 2300

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. REJECT is not allowed either, because no measured FAIL invalidates R0.
  - The mesh, time and domain components are INCONCLUSIVE for both quantities, so no combined uncertainty exists. The time component has never been measured: no REDUCE_TIME_STEP run exists.
  - R1 (8 cycles) gives a clean statistical reference. Drag CI95 is 0.00037742 and drift is 0.00092276. Strouhal is 0.1634 (window) and 0.16342 (FFT). The statistics component passes: 0.0009228 for drag and 0.0006999 for Strouhal.
  - R0 as submitted carries a measured averaging bias of 0.02609 for drag (1.2961 reported) and 0.01294 for Strouhal (0.16129 reported). The rule adds this bias linearly to the root-sum-square of the other components. The drag mesh estimate (0.01832) and domain estimate (0.03768) already combine to about 0.042, so the budget is exceeded however the other components turn out. Both the drag domain estimate and the Strouhal mesh estimate (0.03739) are above 0.03 on their own.
  - R2 (finer mesh) gives drag 1.3349 and Strouhal 0.16443, against R1's 1.3308 and 0.1634. R1 to R2 also changed the time step (0.01 to 0.0086734). The mesh estimate therefore mixes spatial and temporal effects, and it rests on an assumed order p=2.
  - R3 (expanded domain) gives drag 1.3225 and Strouhal 0.16272, against R1's 1.3308 and 0.1634. The demonstrated changes are 0.63% and 0.42%, and both are below tolerance. R3 has checkMesh_ok=false and a coarser far field (representative cell size 0.79405 D against 0.45745 D). Its domain comparison is therefore weaker evidence than it looks.
  - physics_regime is still INCONCLUSIVE. It cites R0's +25.8% lift-amplitude change, and the stationary-window starts in R0, R1, R2 and R3 are all flagged as MSER caps.
  - Budget: 8.78 of 12.0 compute units are used, which leaves about 3.22 units (about 1260 s at the 391.64 s root cost). REDUCE_TIME_STEP costs 1567 s from R0 or R1 (about 4.0 units) and REFINE_MESH costs 1812 s or more. Neither is affordable. The experiments that fit are RUN_LONGER (979 s) and EXPAND_DOMAIN (1040 s) from R0 or R1.
  - None of the affordable experiments can close the missing time component or the mesh component. They also cannot remove R0's averaging bias. ACCEPT is therefore out of reach in the remaining budget, and none of the changes seen so far suggests a demonstrated change above tolerance that a cheap run would expose. I return no experiment, and the system will report INCONCLUSIVE.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 3 number(s) not traceable to evidence: 0.042, 3.22, 1260

Run G1_premature_averaging.long100-bf9115c8c872: RUN_LONGER from G1_premature_averaging-17c0143468d7 (time.end_time: 40→100).
  - Observation: mean_drag_coefficient 1.3039 → 1.3308 (+2.07%).
  - Observation: strouhal_number 0.16058 → 0.1634 (+1.76%).

Run G1_premature_averaging.m1.41-f8bb4a846d17: REFINE_MESH from G1_premature_averaging.long100-bf9115c8c872 (averaging.start_time: 10→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 100→80).
  - Observation: mean_drag_coefficient 1.3308 → 1.3349 (+0.31%).
  - Observation: strouhal_number 0.1634 → 0.16443 (+0.63%).

Run G1_premature_averaging.D2x-6e506d02ef0a: EXPAND_DOMAIN from G1_premature_averaging.long100-bf9115c8c872 (averaging.start_time: 10→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 100→80).
  - Observation: mean_drag_coefficient 1.3308 → 1.3225 (-0.62%).
  - Observation: strouhal_number 0.1634 → 0.16272 (-0.42%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=INCONCLUSIVE, domain=INCONCLUSIVE; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh, time, domain.
- strouhal_number: not established — mesh, time, domain.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G1_premature_averaging-17c0143468d7` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=391.6 s; record: results/runs/G1_premature_averaging-17c0143468d7/run.json
- `G1_premature_averaging.long100-bf9115c8c872` status=completed parent=G1_premature_averaging-17c0143468d7 created=2026-10-20T16:25:32+00:00 wall=725 s; record: results/runs/G1_premature_averaging.long100-bf9115c8c872/run.json
- `G1_premature_averaging.m1.41-f8bb4a846d17` status=completed parent=G1_premature_averaging.long100-bf9115c8c872 created=2026-10-20T16:38:05+00:00 wall=2788 s; record: results/runs/G1_premature_averaging.m1.41-f8bb4a846d17/run.json
- `G1_premature_averaging.D2x-6e506d02ef0a` status=completed parent=G1_premature_averaging.long100-bf9115c8c872 created=2026-10-20T17:25:02+00:00 wall=1300 s; record: results/runs/G1_premature_averaging.D2x-6e506d02ef0a/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1074319984.0, "relative_to_root": 8.782864486592544, "experiment_wall_seconds": 4812.613291719004, "n_experiments": 3, "planner_calls": 4, "planner_cost_usd": 0.35064566999999996, "loop_wall_seconds": 4927.264108903}
