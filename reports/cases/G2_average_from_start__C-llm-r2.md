# Verification report: G2_average_from_start (C-llm-r2)

## QUESTION

A long circular rod of diameter 10 mm is placed across a uniform, slow stream of air (0.15 m/s, ~20 degC).  Estimate the time-mean drag coefficient and the vortex-shedding Strouhal number of the rod, per unit span, to within 3 % each.  Treat the stream as unbounded.

Requested: mean_drag_coefficient, strouhal_number; tolerance mean_drag_coefficient 3%, strouhal_number 3%.

## RESULT (as reported by the submitted simulation)

- mean_drag_coefficient: 1.3196
- strouhal_number: 0.16144

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
- **INCONCLUSIVE** physics_regime — lift oscillation present but its amplitude changes by +6.7% across the analysed window: not yet a sustained limit cycle (decaying or still growing); a longer record is needed
- **PASS** convection_scheme_order — convection scheme 'Gauss linearUpwind grad(U)' is nominally second order
- **PASS** averaging_window [mean_drag_coefficient] — reported mean_drag_coefficient is biased by 0.864% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** averaging_window [strouhal_number] — reported strouhal_number is biased by 1.219% relative to the stationary-window value (measured bias, added linearly to the error budget)
- **PASS** statistical_uncertainty [mean_drag_coefficient] — statistical/stationarity uncertainty 5.59e-05 <= 1.50%
- **PASS** statistical_uncertainty [strouhal_number] — statistical/stationarity uncertainty 4.53e-05 <= 1.50%
- **INCONCLUSIVE** mesh_sensitivity [mean_drag_coefficient] — estimated mesh uncertainty of mean_drag_coefficient = 1.69% > 1.50% but the demonstrated change 0.28% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 5.6e-05)]
- **INCONCLUSIVE** mesh_sensitivity [strouhal_number] — estimated mesh uncertainty of strouhal_number = 3.62% > 1.50% but the demonstrated change 0.61% <= tau; more refinement would be needed [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.8e-05)]
- **PASS** time_sensitivity [mean_drag_coefficient] — estimated time uncertainty of mean_drag_coefficient = 1.11% <= 1.50% (root-to-finest change 0.277%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 5.6e-05)]
- **PASS** time_sensitivity [strouhal_number] — estimated time uncertainty of strouhal_number = 0.30% <= 1.50% (root-to-finest change 0.076%) [two-level Richardson, assumed order p=2, Fs=3 (noise floor 7.5e-05)]
- **PASS** domain_sensitivity [mean_drag_coefficient] — estimated domain uncertainty of mean_drag_coefficient = 1.31% <= 1.50% (root-to-finest change 0.658%) [three-level Celik procedure, observed order p=1.44, Fs=1.25]
- **PASS** domain_sensitivity [strouhal_number] — estimated domain uncertainty of strouhal_number = 0.86% <= 1.50% (root-to-finest change 0.448%) [three-level Celik procedure, observed order p=1.52, Fs=1.25]

### Evidence graph

```
CLAIM: mean_drag_coefficient of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.00864
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=5.59e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0169
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m1.41-0f6f3498eef5
├── Temporal discretisation (time-step sensitivity): PASS U=0.0111
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.dt0.005-9ef3c201ac13
└── Artificial boundaries (domain sensitivity): PASS U=0.0131
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D1.5x-b31588b6c8c7
    └── G2_average_from_start.D2x-1f60c8b74afa

CLAIM: strouhal_number of run G2_average_from_start-e7384e5a2c24 is reliable to within 3%  [INCONCLUSIVE]
├── solver_completion: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mesh_quality: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── mass_conservation: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── linear_solver_convergence: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── courant_number: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── reynolds_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── force_reference_consistency: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── physics_regime: INCONCLUSIVE
│   └── G2_average_from_start-e7384e5a2c24
├── convection_scheme_order: PASS
│   └── G2_average_from_start-e7384e5a2c24
├── Averaging window (reported vs stationary value): PASS U=0.0122
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Temporal statistics (stationarity, cycles): PASS U=4.53e-05
│   └── G2_average_from_start-e7384e5a2c24
│   └── G2_average_from_start.long160-24e243b2227c
├── Spatial discretisation (mesh sensitivity): INCONCLUSIVE U=0.0362
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.m1.41-0f6f3498eef5
├── Temporal discretisation (time-step sensitivity): PASS U=0.00303
│   └── G2_average_from_start.long160-24e243b2227c
│   └── G2_average_from_start.dt0.005-9ef3c201ac13
└── Artificial boundaries (domain sensitivity): PASS U=0.00862
    └── G2_average_from_start.long160-24e243b2227c
    └── G2_average_from_start.D1.5x-b31588b6c8c7
    └── G2_average_from_start.D2x-1f60c8b74afa

```

## EXPERIMENT HISTORY

Run G2_average_from_start-e7384e5a2c24: submitted simulation (30580 cells, dt=0.01 D/U, half-height 40 D).

**Critic iteration 1** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed, and there is no FAIL to justify REJECT.
  - R0 mesh, time and domain uncertainties are all unmeasured (no REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run). A missing component is not a pass, for both mean_drag_coefficient and strouhal_number.
  - The physics_regime check is INCONCLUSIVE. The lift amplitude changes by +6.7% across the analysed window, so R0 may not yet be a sustained limit cycle.
  - The stationary window starts at 27.88 convective times, which is flagged as the MSER cap (stationary_window_start_is_mser_cap = true). It holds only 5 cycles out of a 59.99 record.
  - The R0 drag drift is 0.010388 relative and its CI95 is 0.0058205. The statistics uncertainty is 0.01039 for drag and 0.008104 for Strouhal number. The averaging biases are 0.005234 (drag) and 0.009529 (Strouhal number).
  - Averaging bias plus statistics already use a large share of the 0.03 tolerance. The error budget requires each component to be <= 0.5*tolerance and the linear-plus-RSS total to be <= tolerance. Little room is left for mesh, time and domain terms, so a longer record that shrinks these terms is valuable.
  - If the transient has not ended, every later comparison run (mesh, time step, domain) would inherit a non-stationary window and a 5-cycle noise floor. That would make their differences hard to interpret. Settling stationarity first makes the later experiments meaningful.
  - RUN_LONGER on R0 costs 1060 s (default 100 additional convective times). That is cheaper than the other menu entries (1126, 1697, 1963 s). It fits within the budget of 6 experiments and 12x root compute (R0 cost 636.22 s).
  - Later experiments are still needed after this one. R0 has a coarse wake (wake_last_cell_D 1.0209, representative_cell_size_D 0.45745), and its time step is 0.01 with 613.51 steps per period. The domain extents are 30D upstream, 50D downstream and 40D half height with symmetry lateral boundaries. Mesh refinement is the likely next choice.
  - Requested: RUN_LONGER {'additional_convective_times': 100.0} on G2_average_from_start-e7384e5a2c24 — The physics_regime check is INCONCLUSIVE because the lift amplitude is still changing (+6.7%). The stationary window is MSER-capped with only 5 cycles. Averaging and statistics already use a large part of the 0.03 budget. This is the cheapest experiment, and it must be settled before mesh, time-step and domain comparisons can be trusted.
  - Outcome: executed -> G2_average_from_start.long160-24e243b2227c (completed)

**Critic iteration 2** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed and there is no FAIL to justify REJECT.
  - Mesh, time and domain uncertainties are still unmeasured for both mean_drag_coefficient and strouhal_number. No REFINE_MESH, REDUCE_TIME_STEP or EXPAND_DOMAIN run exists, and a missing component is not a pass.
  - RUN_LONGER (R1, 160 convective times) settled the statistics. R1 has 13 stationary cycles. Drag drift is 5.59e-05, CI95 is 1.5832e-05, and the statistics uncertainties are 5.59e-05 (drag) and 4.525e-05 (Strouhal number).
  - R0's submitted-setup values are biased relative to the R1 stationary window. Drag is 1.3196 vs 1.3311 (averaging bias 0.008643). Strouhal number is 0.16144 vs 0.16344 (bias 0.01219). This bias is added linearly, so it takes a sizeable share of the 0.03 tolerance. Mesh, time and domain together must fit in what is left.
  - The R1 stationary window start (76.938) is still flagged as the MSER cap. However, the measured drag drift is tiny, so the averaging and statistics components are no longer the limiting items.
  - The physics_regime check is still INCONCLUSIVE. It cites only R0, where the lift amplitude changes by +6.7%. R1 rms lift is 0.22857 in the stationary window. This does not block the next experiment.
  - The mesh is the most likely source of a large unmeasured error. representative_cell_size_D is 0.45745, wake_last_cell_D is 1.0209 with 111 streamwise wake cells, and there are 160 cells around the cylinder. The Strouhal number depends on wake resolution, and drag on near-wall resolution (wall_first_cell_D 0.005). Time step and domain look comparatively benign: the Courant number is 0.73373 with 611.86 steps per period, the blockage ratio is 0.0125, and the extents are 30D upstream, 50D downstream and 40D half height.
  - Budget: 1 of 6 experiments used and compute is 1.67 of 12.0 relative to root. REFINE_MESH (1963 s) is affordable. The time-step (1697 s) and domain (1126 s) runs still fit afterwards.
  - Use R1 as parent. It has the longer, well-converged stationary window, so differences from the refined run are not masked by sampling noise. The listed refinement cost is the same for R0 and R1.
  - Requested: REFINE_MESH {'factor': 1.4142} on G2_average_from_start.long160-24e243b2227c — Mesh, time and domain uncertainties are all unmeasured. The mesh is the coarsest-looking element of the setup (representative_cell_size_D 0.45745, wake_last_cell_D 1.0209), and the Strouhal number and drag are sensitive to wake and near-wall resolution. R1 supplies a converged 13-cycle baseline, so any shift can be attributed to the mesh rather than sampling noise.
  - Outcome: executed -> G2_average_from_start.m1.41-0f6f3498eef5 (completed)

**Critic iteration 3** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE with no failed checks. ACCEPT is not allowed. There is no FAIL, so REJECT is not justified.
  - R1 (RUN_LONGER, 13 stationary cycles) settled the statistics. Drag drift is 5.59e-05 and the statistics uncertainties are 5.59e-05 (drag) and 4.525e-05 (Strouhal). The averaging bias of R0's submitted values is 0.008643 (drag) and 0.01219 (Strouhal).
  - R2 (REFINE_MESH from R1, factor about 1.41) gives a demonstrated change of 0.28% in drag (1.3311 to 1.3349) and 0.61% in Strouhal (0.16344 to 0.16443). Both are below the 3% tolerance. The two-level Richardson estimate of mesh uncertainty is 1.69% (drag) and 3.62% (Strouhal). It assumes p=2, so it is an estimate, not a measured order.
  - Time and domain components are still completely unmeasured for both quantities. No REDUCE_TIME_STEP or EXPAND_DOMAIN run exists, and a missing component is not a pass.
  - The domain is the cheapest unmeasured component to test. EXPAND_DOMAIN on R1 is estimated at 1126 s, against 1697 s for REDUCE_TIME_STEP and 1963 s for REFINE_MESH. The domain is truncated at 30D upstream, 50D downstream and 40D half height, with a symmetryPlane lateral boundary and a blockage ratio of 0.0125. The question says to treat the stream as unbounded, so this truncation is a direct risk to the answer.
  - Time-step error looks less likely to dominate. The setup uses a second-order backward scheme, 611.86 steps per shedding period and max Courant number 0.73373. That is a hypothesis, and only a REDUCE_TIME_STEP run can test it.
  - R1 is the right parent. It has the same mesh and time step as R0 and a long stationary window, so any shift can be attributed to the domain and not to sampling noise. R2 as parent would cost 2607 s and has only 6 cycles.
  - Budget: 2 of 6 experiments are used and 4.75 of 12.0 root-compute units. EXPAND_DOMAIN on R1 adds about 1.77 units. A REDUCE_TIME_STEP run (about 2.67 units) can still follow it.
  - The root mesh uncertainty for Strouhal (3.62%) already exceeds the 0.5*tolerance component limit. The remaining menu may therefore not reach ACCEPT for the root. I cannot use that to pre-empt the evidence. The deterministic verdict stays INCONCLUSIVE.
  - Requested: EXPAND_DOMAIN {'factor': 2.0} on G2_average_from_start.long160-24e243b2227c — Domain truncation is a completely unmeasured error component for both quantities, and the question requires an unbounded stream. EXPAND_DOMAIN is the cheapest experiment (1126 s on R1). R1 has the same mesh and time step as R0 and a converged 13-cycle stationary window, so any shift is attributable to the boundaries.
  - Outcome: executed -> G2_average_from_start.D2x-1f60c8b74afa (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 1.77, 2.67

**Critic iteration 4** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed. No FAIL exists, so REJECT is not justified.
  - R1 is the 160-convective-time continuation of R0. It has 13 stationary cycles, drag drift 5.59e-05 and a drag CI95 of 1.5832e-05. The statistics components (5.59e-05 for drag, 4.525e-05 for Strouhal) are settled.
  - R2 is the refined mesh. Compared with R1, the stationary-window drag moves from 1.3311 to 1.3349 (0.28%) and Strouhal from 0.16344 to 0.16443 (0.61%). The demonstrated changes are below the 0.03 tolerance. The assumed-order (p=2) two-level Richardson mesh uncertainties are 0.01686 (drag) and 0.03619 (Strouhal). The Strouhal value exceeds both 0.5*tolerance and the full tolerance. The order is assumed, not measured, so this is INCONCLUSIVE rather than FAIL.
  - R3 is the expanded domain (60D upstream, 100D downstream, 80D half height). Compared with R1, drag moves from 1.3311 to 1.3224 (0.66%) and Strouhal from 0.16344 to 0.16271 (0.45%). The demonstrated changes are below the tolerance. The estimated domain uncertainties (assumed p=1) are 0.03948 (drag) and 0.02687 (Strouhal), so the domain component is INCONCLUSIVE.
  - R3 reports checkMesh_ok=false, while R1, R2 and R0 report true. This is a recorded flag on the domain-expansion run. It does not appear in the deterministic failed_checks, and I cannot overrule or reinterpret the verifier. It does reduce how far R3 should be trusted as a clean domain comparison.
  - The time-step component is completely unmeasured for both quantities. No REDUCE_TIME_STEP run exists, and a missing component is not a pass. R0 and R1 use dt = 0.01 convective units, max Courant number 0.73373 and about 612 steps per shedding period. That is evidence only for plausibility. It is not a measurement.
  - physics_regime is still INCONCLUSIVE. It cites only R0, where the lift amplitude changes by +6.7% across the window. The R1 record is longer, with rms lift 0.22857.
  - Budget: 3 of 6 experiments are used and 6.52 of 12.0 root-compute units are used. That leaves about 5.48 units, or about 3490 s at the root cost of 636.22 s. REDUCE_TIME_STEP on R1 costs 1697 s (about 2.67 units) and is affordable. A third mesh level from R2 (4510 s) is not affordable. REFINE_MESH from R1 (1963 s) would be affordable but would not add an independent time measurement.
  - ACCEPT may still be out of reach. The Strouhal mesh and domain estimates exceed 0.5*tolerance. I cannot pre-empt the verifier. The time term is the only component that can be measured with a single affordable run, and it is needed before any combined uncertainty is formed.
  - Requested: REDUCE_TIME_STEP {'factor': 2.0} on G2_average_from_start.long160-24e243b2227c — The time-step uncertainty is the only error component with no measurement at all for either quantity. Mesh and domain already have two-level estimates, and a third mesh level is unaffordable. R1 has the same mesh and dt as R0 and a converged 13-cycle stationary window, so any shift can be attributed to the time step. The cost of 1697 s (about 2.67 root units) fits the remaining budget and leaves room for one further cheap experiment.
  - Outcome: executed -> G2_average_from_start.dt0.005-9ef3c201ac13 (completed)
  - Numeric audit: 4 number(s) not traceable to evidence: 5.48, 3490, 2.67, 2.67

**Critic iteration 5** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and there is no FAIL to justify REJECT.
  - Averaging and statistics PASS for both quantities. Drag drift is 5.59e-05 and the Strouhal statistics uncertainty is 4.525e-05 (R1, 13 cycles).
  - Time PASS from R1 vs R4: drag uncertainty is 0.01106 and Strouhal is 0.003034. The demonstrated changes are 0.277% (drag) and 0.076% (Strouhal).
  - Mesh is INCONCLUSIVE from R1 vs R2. Drag uncertainty is 0.01686 and Strouhal is 0.03619. The demonstrated changes are only 0.28% and 0.61%, so the large estimates come from the assumed order p=2 and Fs=3, not from a measured order.
  - Domain is INCONCLUSIVE from R1 vs R3. Drag uncertainty is 0.03948 and Strouhal is 0.02687, with assumed p=1. The demonstrated changes are 0.66% and 0.45%, well below the 0.03 tolerance. R3 also has checkMesh_ok=false and a coarser far-field mesh (representative_cell_size_D 0.79405). This confounds the domain comparison.
  - Budget: 4 of 6 experiments are used and 9.19 of 12.0 root-compute units are used. A third mesh level is unaffordable: REFINE_MESH on R1 costs 1963 s and on R2 costs 4510 s. The remaining headroom is about 2.8 root units, about 1790 s at the R0 cost of 636.22 s.
  - The domain term is the only unresolved component that an affordable run can address. EXPAND_DOMAIN from R1 with factor 1.5 costs 1126 s. It gives a third domain level (R1, new run, R3). That allows an observed convergence order, not an assumed p=1, and checks whether the R3 shift is boundary-driven rather than a far-field-mesh artefact.
  - ACCEPT may remain out of reach, because the Strouhal mesh estimate (0.03619) exceeds the full tolerance. I cannot pre-empt the verifier on that. The measured shifts so far suggest no demonstrated failure, so MORE_EVIDENCE rather than REJECT.
  - physics_regime is still INCONCLUSIVE. It cites only R0, where the lift amplitude changes by +6.7%. R1 is the longer record and has a stationary window of 13 cycles.
  - Requested: EXPAND_DOMAIN {'factor': 1.5} on G2_average_from_start.long160-24e243b2227c — Domain is the only component with a confounded, assumed-order (p=1) estimate that an affordable run can improve. Factor 1.5 from R1 (1126 s) fits the remaining compute budget. It gives a third domain extent, so the order can be measured. It also gives a comparison that does not depend on the coarser far-field mesh of R3, which has checkMesh_ok=false. A third mesh level is unaffordable.
  - Outcome: executed -> G2_average_from_start.D1.5x-b31588b6c8c7 (completed)
  - Numeric audit: 2 number(s) not traceable to evidence: 2.8, 1790

**Critic iteration 6** (deterministic verdict INCONCLUSIVE):
  - The deterministic verdict is INCONCLUSIVE and failed_checks is empty. ACCEPT is not allowed, and there is no FAIL to justify REJECT.
  - Averaging, statistics and time pass for both quantities. For drag the components are 0.008643, 5.59e-05 and 0.01106. For Strouhal they are 0.01219, 4.525e-05 and 0.003034. The time result comes from R1 vs R4.
  - Domain now passes. The three-level Celik procedure (R1, R5, R3) gives observed orders p=1.44 (drag) and p=1.52 (Strouhal). The domain uncertainties are 0.01309 (drag) and 0.008615 (Strouhal). The R5 extension did its job.
  - The only INCONCLUSIVE component is mesh, from R1 vs R2. The uncertainty is 0.01686 for drag and 0.03619 for Strouhal. Both use an assumed order p=2 with Fs=3. The demonstrated changes are only 0.28% (drag) and 0.61% (Strouhal), well below the 0.03 tolerance. Combined uncertainty is null.
  - The Strouhal mesh estimate of 0.03619 exceeds both 0.5*tolerance and the full tolerance. This comes from the assumed order, not a measured one. It cannot be resolved without a third mesh level. I cannot treat it as a pass or as a failure.
  - The remaining budget cannot pay for any menu entry. Compute used is 10.77 of 12.0 root units. The 1.23 left is about 783 s at the R0 cost of 636.22 s. The cheapest menu entries are 1060 s (RUN_LONGER on R0 or R1) and 1126 s (EXPAND_DOMAIN on R0 or R1). A third mesh level costs 1963 s from R1 or 4510 s from R2. One experiment slot remains (5 of 6 used), but compute is the binding limit.
  - Under rule 5 the answer is MORE_EVIDENCE with next_experiment null. The system will report INCONCLUSIVE.
  - physics_regime is still INCONCLUSIVE. It cites R0 only, with a +6.7% lift amplitude change. R1 has 13 stationary cycles, and the R1 stationary-window start is still the MSER cap.
  - Outcome: planner chose to stop (no useful affordable experiment)
  - Numeric audit: 2 number(s) not traceable to evidence: 1.23, 783

Run G2_average_from_start.long160-24e243b2227c: RUN_LONGER from G2_average_from_start-e7384e5a2c24 (time.end_time: 60→160).
  - Observation: mean_drag_coefficient 1.3266 → 1.3311 (+0.34%).
  - Observation: strouhal_number 0.163 → 0.16344 (+0.27%).

Run G2_average_from_start.m1.41-0f6f3498eef5: REFINE_MESH from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, mesh.refinement: 1→1.414, time.delta_t: 0.01→0.008673, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3349 (+0.28%).
  - Observation: strouhal_number 0.16344 → 0.16443 (+0.61%).

Run G2_average_from_start.D2x-1f60c8b74afa: EXPAND_DOMAIN from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, domain.downstream: 50→100, domain.half_height: 40→80, domain.upstream: 30→60, mesh.n_downstream: 111→145, mesh.n_lateral: 45→55, mesh.n_upstream: 35→43, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3224 (-0.65%).
  - Observation: strouhal_number 0.16344 → 0.16271 (-0.45%).

Run G2_average_from_start.dt0.005-9ef3c201ac13: REDUCE_TIME_STEP from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, time.delta_t: 0.01→0.005, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3275 (-0.28%).
  - Observation: strouhal_number 0.16344 → 0.16356 (+0.08%).

Run G2_average_from_start.D1.5x-b31588b6c8c7: EXPAND_DOMAIN from G2_average_from_start.long160-24e243b2227c (averaging.start_time: 0→40, domain.downstream: 50→75, domain.half_height: 40→60, domain.upstream: 30→45, mesh.n_downstream: 111→131, mesh.n_lateral: 45→51, mesh.n_upstream: 35→40, time.end_time: 160→80).
  - Observation: mean_drag_coefficient 1.3311 → 1.3251 (-0.46%).
  - Observation: strouhal_number 0.16344 → 0.16292 (-0.31%).

## FINAL JUSTIFICATION

- mean_drag_coefficient: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).
- strouhal_number: INCONCLUSIVE (components: averaging=PASS, statistics=PASS, mesh=INCONCLUSIVE, time=PASS, domain=PASS; combined uncertainty n/a vs tolerance 3%).

## REMAINING LIMITATIONS

- mean_drag_coefficient: not established — mesh.
- strouhal_number: not established — mesh.
- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.
- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).

## PROVENANCE

- `G2_average_from_start-e7384e5a2c24` status=completed parent=None created=2026-10-19T07:35:18+00:00 wall=636.2 s; record: results/runs/G2_average_from_start-e7384e5a2c24/run.json
- `G2_average_from_start.long160-24e243b2227c` status=completed parent=G2_average_from_start-e7384e5a2c24 created=2026-10-19T09:08:43+00:00 wall=1041 s; record: results/runs/G2_average_from_start.long160-24e243b2227c/run.json
- `G2_average_from_start.m1.41-0f6f3498eef5` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-20T07:51:13+00:00 wall=3097 s; record: results/runs/G2_average_from_start.m1.41-0f6f3498eef5/run.json
- `G2_average_from_start.D2x-1f60c8b74afa` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-20T09:49:44+00:00 wall=1406 s; record: results/runs/G2_average_from_start.D2x-1f60c8b74afa/run.json
- `G2_average_from_start.dt0.005-9ef3c201ac13` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-20T10:39:59+00:00 wall=1777 s; record: results/runs/G2_average_from_start.dt0.005-9ef3c201ac13/run.json
- `G2_average_from_start.D1.5x-b31588b6c8c7` status=completed parent=G2_average_from_start.long160-24e243b2227c created=2026-10-19T16:42:03+00:00 wall=984.8 s; record: results/runs/G2_average_from_start.D1.5x-b31588b6c8c7/run.json
- OpenFOAM v2412 (package 2412.260127-1); problem specification and full configuration embedded in each run.json.
- Experiment cost: {"experiment_cell_steps": 1976815984.0, "relative_to_root": 10.774013429256595, "experiment_wall_seconds": 8305.447895315012, "n_experiments": 5, "planner_calls": 6, "planner_cost_usd": 0.5800209550000001, "loop_wall_seconds": 14782.543395941002}
