**Missing or stale results (NOT counted in the rates of the system concerned; recompute before drawing conclusions):** C-rule-prereg/F1_upwind_convection: missing; C-rule-prereg/G1_premature_averaging: missing; Bexh/H1_dynamic_viscosity: missing

_Percentages: errors against the reference T are relative to T. Verifier sensitivity changes are relative to the finer (child) member of a study, |q_fine − q_root| / |q_fine| (checks/sensitivity.py; the finest member for a three-level chain). Observation lines in the case reports (reports/cases/) and the loop traces in benchmark_results.md are relative to the parent run, (q_child − q_parent) / q_parent._

| case | label (with mitigation) | max err / τ | unstable | label without mitigation | A | B | L-judge | C-rule | C-rule-prereg | C-llm | Bexh |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | 0.40 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| K1_central_scheme | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| K2_fine_large | ambiguous | 0.31 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| A1_coarse_mesh | flawed | 1.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| A2_moderate_mesh | ambiguous | 0.48 | strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| B1_small_domain | flawed | 4.90 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| B2_moderate_domain | flawed | 1.41 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | INCONCLUSIVE · |
| C1_large_timestep | ambiguous | 0.21 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| C2_euler_large_timestep | ambiguous | 1.11 | mean_drag_coefficient,strouhal_number | flawed | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| D1_steady_solver | flawed | 5.66 |  | flawed | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| E1_noslip_side_walls | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| F1_upwind_convection | flawed | 7.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | — ? | REJECT ✓ | REJECT ✓ |
| G1_premature_averaging | ambiguous | 0.54 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | REJECT ~ | INCONCLUSIVE ~· | — ? | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| H1_dynamic_viscosity | flawed | 2.02 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| I1_force_reference | flawed | 3.68 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| J1_coarse_wake | ambiguous | 0.37 | strouhal_number | credible | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ |
| G2_average_from_start | ambiguous | 0.51 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · `~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · S stale (not counted)

| metric | A | B | L-judge | C-rule | C-rule-prereg | C-llm | Bexh |
|---|---|---|---|---|---|---|---|
| cases | 17 | 17 | 17 | 17 | 15 | 17 | 16 |
| flawed cases (decided) | 7 | 7 | 7 | 7 | 6 | 7 | 6 |
| credible cases (decided) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ambiguous cases (decided) | 10 | 10 | 10 | 10 | 9 | 10 | 10 |
| **false acceptance** (flawed → ACCEPT) | 0.86 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection (flawed → REJECT) | 0.14 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 | 0.83 |
| missed but safe (flawed → INCONCLUSIVE) | 0.00 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.17 |
| correct acceptance (credible → ACCEPT) | — | — | — | — | — | — | — |
| false rejection (credible → REJECT) | — | — | — | — | — | — | — |
| inconclusive (all decided) | 0.00 | 0.76 | 0.06 | 0.53 | 0.53 | 0.53 | 0.62 |
| ambiguous cases: verdicts | ACC:9 REJ:1 INC:0 | ACC:0 REJ:1 INC:9 | ACC:7 REJ:2 INC:1 | ACC:0 REJ:1 INC:9 | ACC:0 REJ:1 INC:8 | ACC:0 REJ:1 INC:9 | ACC:0 REJ:1 INC:9 |
| ambiguous cases ACCEPTed although best-estimate error > τ | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| errors (excluded from rates) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| stale results (excluded) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| missing results | 0 | 0 | 0 | 0 | 2 | 0 | 1 |
| errors by label | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 |
| mean extra simulations / case | 0.00 | 0.00 | 0.00 | 3.47 | 3.13 | 3.06 | 4.81 |
| mean extra compute / case (× root) | 0.00 | 0.00 | 0.00 | 4.78 | 4.53 | 4.89 | 7.38 |
| total experiment wall time (h) | 0.00 | 0.00 | 0.00 | 31.73 | 30.06 | 40.17 | 43.72 |
| LLM cost (USD) | 0.00 | 0.00 | 0.54 | 0.00 | 0.00 | 5.13 | 0.00 |
| authority violations | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| untraceable numbers in LLM text | 0 | 0 | 27 | 0 | 0 | 59 | 0 |
| first experiment targets the flaw | — | — | — | 1/4 | 1/3 | 4/4 | — |

### Labels without the truth-uncertainty mitigation (design.md §19 rule, point estimates)

_Same verdicts; only the labels change. Both label sets are pre-registered: the §19 rule, and the risk mitigation 'label near-boundary cases ambiguous' (design.md, major technical risks 2), operationalised in review R18 (4639ddb, 2026-10-19 08:24 UTC; some verdicts already existed, but no reference T and hence no label did) as 'the interval e ± U(T) straddles τ or τ/2'. The table above uses the mitigation. Both label sets apply the narrow reading of the §19 set-up clauses (see 'Attack cases against the reference'). Under the set-up reading, E1_noslip_side_walls (no-slip side walls where the problem is unbounded; max err 0.63 τ) would be flawed instead of ambiguous, and the ACCEPTs of A and L-judge on it would be false acceptances; no other benchmark label changes (the other cases are flawed by error or have numerical defects only)._

| metric | A | B | L-judge | C-rule | C-rule-prereg | C-llm | Bexh |
|---|---|---|---|---|---|---|---|
| flawed cases | 8 | 8 | 8 | 8 | 7 | 8 | 7 |
| credible cases | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| ambiguous cases | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| **false acceptance** | 0.88 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection | 0.12 | 0.38 | 0.88 | 0.88 | 0.86 | 0.88 | 0.71 |
| missed but safe | 0.00 | 0.62 | 0.12 | 0.12 | 0.14 | 0.12 | 0.29 |
| correct acceptance | 0.80 | 0.00 | 0.80 | 0.00 | 0.00 | 0.00 | 0.00 |
| false rejection | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |

### Calibration: the verifier's uncertainty estimate vs the error against the reference

_Cases where mesh, time and domain all carry an estimate. U = averaging bias + RSS(components). 'within U(T)': not covered by U alone, but by U combined with the reference's own uncertainty._

| case | system | quantity | error vs reference | verifier U | verdict | covered |
|---|---|---|---|---|---|---|
| baseline | C-rule | mean_drag_coefficient | 1.20% | 2.42% | INCONCLUSIVE | yes |
| baseline | C-rule | strouhal_number | 0.31% | 1.59% | ACCEPT | yes |
| K1_central_scheme | C-rule | mean_drag_coefficient | 1.90% | 6.74% | INCONCLUSIVE | yes |
| K1_central_scheme | C-rule | strouhal_number | 0.39% | 2.53% | INCONCLUSIVE | yes |
| K2_fine_large | C-rule | mean_drag_coefficient | 0.94% | 1.47% | ACCEPT | yes |
| K2_fine_large | C-rule | strouhal_number | 0.07% | 2.54% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-rule | mean_drag_coefficient | 0.51% | 2.40% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-rule | strouhal_number | 1.45% | 2.74% | INCONCLUSIVE | yes |
| B2_moderate_domain | C-rule | strouhal_number | 1.89% | 3.91% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule | mean_drag_coefficient | 1.89% | 3.45% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule | strouhal_number | 0.21% | 2.94% | INCONCLUSIVE | yes |
| baseline | C-rule-prereg | mean_drag_coefficient | 1.20% | 2.42% | INCONCLUSIVE | yes |
| baseline | C-rule-prereg | strouhal_number | 0.31% | 1.59% | ACCEPT | yes |
| K1_central_scheme | C-rule-prereg | mean_drag_coefficient | 1.90% | 6.74% | INCONCLUSIVE | yes |
| K1_central_scheme | C-rule-prereg | strouhal_number | 0.39% | 2.53% | INCONCLUSIVE | yes |
| K2_fine_large | C-rule-prereg | mean_drag_coefficient | 0.94% | 1.47% | ACCEPT | yes |
| K2_fine_large | C-rule-prereg | strouhal_number | 0.07% | 2.54% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-rule-prereg | mean_drag_coefficient | 0.51% | 2.40% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-rule-prereg | strouhal_number | 1.45% | 2.74% | INCONCLUSIVE | yes |
| B2_moderate_domain | C-rule-prereg | strouhal_number | 1.89% | 3.91% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule-prereg | mean_drag_coefficient | 1.89% | 3.45% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule-prereg | strouhal_number | 0.21% | 2.94% | INCONCLUSIVE | yes |
| baseline | C-llm | mean_drag_coefficient | 1.20% | 2.24% | INCONCLUSIVE | yes |
| baseline | C-llm | strouhal_number | 0.31% | 2.31% | INCONCLUSIVE | yes |
| K1_central_scheme | C-llm | mean_drag_coefficient | 1.90% | 4.05% | INCONCLUSIVE | yes |
| K1_central_scheme | C-llm | strouhal_number | 0.39% | 2.66% | INCONCLUSIVE | yes |
| K2_fine_large | C-llm | mean_drag_coefficient | 0.94% | 2.54% | INCONCLUSIVE | yes |
| K2_fine_large | C-llm | strouhal_number | 0.07% | 1.52% | ACCEPT | yes |
| A2_moderate_mesh | C-llm | mean_drag_coefficient | 0.51% | 2.23% | ACCEPT | yes |
| A2_moderate_mesh | C-llm | strouhal_number | 1.45% | 2.89% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-llm | mean_drag_coefficient | 1.89% | 3.03% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-llm | strouhal_number | 0.21% | 2.94% | INCONCLUSIVE | yes |
| baseline | Bexh | mean_drag_coefficient | 1.20% | 4.21% | INCONCLUSIVE | yes |
| baseline | Bexh | strouhal_number | 0.31% | 2.96% | INCONCLUSIVE | yes |
| K1_central_scheme | Bexh | mean_drag_coefficient | 1.90% | 17.89% | INCONCLUSIVE | yes |
| K1_central_scheme | Bexh | strouhal_number | 0.39% | 3.14% | INCONCLUSIVE | yes |
| K2_fine_large | Bexh | mean_drag_coefficient | 0.94% | 3.35% | INCONCLUSIVE | yes |
| K2_fine_large | Bexh | strouhal_number | 0.07% | 2.88% | INCONCLUSIVE | yes |
| A1_coarse_mesh | Bexh | mean_drag_coefficient | 1.55% | 6.29% | INCONCLUSIVE | yes |
| A2_moderate_mesh | Bexh | mean_drag_coefficient | 0.51% | 4.61% | INCONCLUSIVE | yes |
| A2_moderate_mesh | Bexh | strouhal_number | 1.45% | 3.83% | INCONCLUSIVE | yes |
| B2_moderate_domain | Bexh | mean_drag_coefficient | 4.24% | 14.28% | INCONCLUSIVE | yes |
| B2_moderate_domain | Bexh | strouhal_number | 1.89% | 10.43% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | Bexh | mean_drag_coefficient | 1.89% | 8.88% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | Bexh | strouhal_number | 0.21% | 5.64% | INCONCLUSIVE | yes |
| F1_upwind_convection | Bexh | mean_drag_coefficient | 3.55% | 95.60% | INCONCLUSIVE | yes |
| G1_premature_averaging | Bexh | mean_drag_coefficient | 1.47% | 6.87% | INCONCLUSIVE | yes |
| G1_premature_averaging | Bexh | strouhal_number | 1.62% | 4.30% | INCONCLUSIVE | yes |
| I1_force_reference | Bexh | mean_drag_coefficient | 11.05% | 4.21% | INCONCLUSIVE | **NO** |
| I1_force_reference | Bexh | strouhal_number | 0.31% | 2.96% | INCONCLUSIVE | yes |
| J1_coarse_wake | Bexh | mean_drag_coefficient | 0.56% | 4.87% | INCONCLUSIVE | yes |
| J1_coarse_wake | Bexh | strouhal_number | 1.11% | 3.88% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | mean_drag_coefficient | 0.32% | 5.18% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | strouhal_number | 1.52% | 4.27% | INCONCLUSIVE | yes |

Benchmark cases only: covered by U: 53/54; by U combined with U(T): 53/54.

Attack cases (results/attacks/, same definition; errors of the attack roots against the same reference; results counted as in the attack section below):

| case | system | quantity | error vs reference | verifier U | verdict | covered |
|---|---|---|---|---|---|---|
| X1_cylinder_geometry | C-rule-v1 | mean_drag_coefficient | 5.98% | 2.28% | INCONCLUSIVE | **NO** |
| X1_cylinder_geometry | C-rule-v1 | strouhal_number | 3.60% | 1.62% | ACCEPT | **NO** |
| X1_cylinder_geometry | C-llm-v1 | mean_drag_coefficient | 5.98% | 2.34% | INCONCLUSIVE | **NO** |
| X1_cylinder_geometry | C-llm-v1 | strouhal_number | 3.60% | 2.43% | INCONCLUSIVE | **NO** |
| X2_inlet_shear | C-llm-v1 | mean_drag_coefficient | 1.20% | 4.35% | INCONCLUSIVE | yes |
| X2_inlet_shear | C-llm-v1 | strouhal_number | 0.50% | 2.78% | INCONCLUSIVE | yes |
| X1_cylinder_geometry | C-llm-v1+review | mean_drag_coefficient | 5.98% | 2.60% | INCONCLUSIVE | **NO** |
| X1_cylinder_geometry | C-llm-v1+review | strouhal_number | 3.60% | 2.28% | INCONCLUSIVE | **NO** |
| X2_inlet_shear | C-llm-v1+review | mean_drag_coefficient | 1.20% | 4.35% | INCONCLUSIVE | yes |
| X2_inlet_shear | C-llm-v1+review | strouhal_number | 0.50% | 2.78% | INCONCLUSIVE | yes |

Attack cases only: covered by U: 4/10; by U combined with U(T): 4/10. Attacks with a set-up departure (X1_cylinder_geometry, X2_inlet_shear): 4/10 covered by U; attacks that change the numerics only: no row.

_The set-up-departure attacks (X1_cylinder_geometry: cylinder diameter 1.05 D where the problem specifies D = 10 mm; X2_inlet_shear: sheared inlet profile where the problem specifies a uniform stream) carry an error that U does not estimate by construction: U covers averaging, statistics, mesh, time and domain for the problem as set up. A NO on those rows mainly reflects the set-up error, not an under-estimated discretisation uncertainty._

### LLM run-to-run variance (independent repeats of C-llm)

| case | label | C-llm | C-llm-r2 | C-llm-r3 | same verdict | same experiment sequence |
|---|---|---|---|---|---|---|
| baseline | ambiguous | INCONCLUSIVE (REFINE → EXPAND → REDUCE → EXPAND → REFINE → EXPAND) | INCONCLUSIVE (REFINE → REFINE → EXPAND → EXPAND → REDUCE → EXPAND) | ACCEPT (REFINE → EXPAND → REDUCE → EXPAND → REFINE) | **no** | no |
| K1_central_scheme | ambiguous | INCONCLUSIVE (REFINE → REFINE → EXPAND → REDUCE → EXPAND → REDUCE) | INCONCLUSIVE (REFINE → EXPAND → EXPAND → REDUCE → REFINE → EXPAND) | INCONCLUSIVE (REFINE → EXPAND → EXPAND → REDUCE → REFINE → REDUCE) | yes | no |
| K2_fine_large | ambiguous | INCONCLUSIVE (REFINE → EXPAND → REDUCE → RUN → EXPAND → REFINE) | ACCEPT (REFINE → EXPAND → REDUCE → EXPAND → REFINE) | — | **no** (of 2 runs) | no (of 2 runs) |
| A1_coarse_mesh | flawed | REJECT (REFINE) | REJECT (REFINE) | REJECT (REFINE) | yes | yes |
| A2_moderate_mesh | ambiguous | INCONCLUSIVE (REFINE → REFINE → EXPAND → REDUCE → EXPAND) | INCONCLUSIVE (REFINE → REFINE → EXPAND → EXPAND → REDUCE → RUN) | — | yes (of 2 runs) | no (of 2 runs) |
| B1_small_domain | flawed | REJECT (EXPAND) | REJECT (EXPAND) | — | yes (of 2 runs) | no (of 2 runs) |
| B2_moderate_domain | flawed | REJECT (EXPAND → EXPAND) | REJECT (EXPAND → EXPAND) | — | yes (of 2 runs) | yes (of 2 runs) |
| C1_large_timestep | ambiguous | INCONCLUSIVE (REFINE → REDUCE → REFINE → EXPAND → REFINE → EXPAND) | INCONCLUSIVE (REFINE → REDUCE → REFINE → EXPAND → EXPAND → REFINE) | — | yes (of 2 runs) | no (of 2 runs) |
| C2_euler_large_timestep | ambiguous | INCONCLUSIVE (REFINE → REDUCE → REDUCE → REFINE → REFINE → EXPAND) | INCONCLUSIVE (REDUCE → REDUCE → REDUCE → REFINE → REFINE → EXPAND) | — | yes (of 2 runs) | no (of 2 runs) |
| D1_steady_solver | flawed | REJECT (none) | REJECT (none) | — | yes (of 2 runs) | yes (of 2 runs) |
| E1_noslip_side_walls | ambiguous | INCONCLUSIVE (EXPAND → REFINE → REDUCE → REFINE → EXPAND) | INCONCLUSIVE (REFINE → EXPAND → EXPAND → REFINE → REDUCE → EXPAND) | — | yes (of 2 runs) | no (of 2 runs) |
| F1_upwind_convection | flawed | REJECT (REFINE → RUN) | REJECT (REFINE → RUN) | — | yes (of 2 runs) | no (of 2 runs) |
| G1_premature_averaging | ambiguous | INCONCLUSIVE (RUN → REFINE → EXPAND) | INCONCLUSIVE (RUN → REFINE → EXPAND) | — | yes (of 2 runs) | yes (of 2 runs) |
| H1_dynamic_viscosity | flawed | REJECT (none) | REJECT (none) | — | yes (of 2 runs) | yes (of 2 runs) |
| I1_force_reference | flawed | REJECT (none) | REJECT (none) | — | yes (of 2 runs) | yes (of 2 runs) |
| J1_coarse_wake | ambiguous | REJECT (none) | REJECT (none) | — | yes (of 2 runs) | yes (of 2 runs) |
| G2_average_from_start | ambiguous | INCONCLUSIVE (RUN → REFINE → EXPAND) | INCONCLUSIVE (RUN → REFINE → EXPAND → REDUCE → EXPAND) | — | yes (of 2 runs) | no (of 2 runs) |

Cases with at least two runs: 17; identical verdict across the available runs in 15/17; identical experiment sequence in 7/17. Complete sets (all 3 runs): 3; identical verdict in 2/3; identical sequence in 1/3.
Pairwise against the first run (C-llm): C-llm-r2: identical verdict 16/17, identical sequence 7/17; C-llm-r3: identical verdict 2/3, identical sequence 1/3.

### Attack cases against the reference

_Attack roots (cases/attacks/) labelled with the benchmark rule (orchestration/truth.label_case) against the same reference T. Errors are signed, (reported − T)/T. Readings of the §19 set-up clauses: set-up reading: any departure from the problem statement (case definition) makes the case flawed; literal reading: flawed needs e > τ or a set-up that answers a different problem (wrong Re or regime), credible needs a consistent set-up, so a departure leaves a case with e ≤ τ/2 ambiguous (labels with the truth-uncertainty mitigation, as in scripts/posthoc_acceptance_rule.py); narrow reading (the convention of orchestration/truth.label_case and benchmark/labels.json): only set-up problems detected from the evidence (wrong Re, steady formulation) and missing quantities count, every other departure is judged by its error._

| attack | reported Cd | reported St | err Cd | err St | max err / τ | set-up departure (case definition) | label: set-up reading | label: literal reading | label: narrow reading, point estimates | label: narrow reading, with mitigation |
|---|---|---|---|---|---|---|---|---|---|---|
| X1_cylinder_geometry | 1.3941 | 0.1580 | +5.98% | -3.60% | 1.99 | cylinder diameter 1.05 D where the problem specifies D = 10 mm | flawed | flawed | flawed | flawed |
| X2_inlet_shear | 1.3312 | 0.1631 | +1.20% | -0.50% | 0.40 | sheared inlet profile where the problem specifies a uniform stream | flawed | ambiguous | credible | ambiguous |
| X3_compensating_errors | 1.3918 | 0.1642 | +5.81% | +0.16% | 1.94 | none | flawed | flawed | flawed | flawed |

**X2_inlet_shear:** the point-estimate errors (Cd 1.20%, St 0.50%) are within τ/2 = 1.5% for every quantity; the label depends on how the §19 set-up clauses are read (docs/design.md §19, pre-registered evaluation protocol): a case is flawed "if the set-up answers a different problem (wrong Re or regime)" and credible "if max e_q ≤ τ/2 and the set-up is consistent". X2_inlet_shear departs from the problem statement (sheared inlet profile where the problem specifies a uniform stream); the evidence-based set-up checks (configured Re, solver) find neither a wrong Re nor a wrong regime (configured Re = 100, solver pimpleFoam). Set-up reading (the parenthesis gives examples; any departure counts): flawed. Literal reading (the parenthesis is exhaustive, and a set-up that departs from the problem statement is not consistent): ambiguous, so its verdicts are not scored. Narrow reading (the parenthesis is exhaustive and 'consistent' means no wrong Re or regime, the convention of orchestration/truth.label_case): labelled by its error, credible on point estimates (its REJECTs are false rejections) and ambiguous with the truth-uncertainty mitigation (Cd 1.20% ± 0.94% straddles τ/2).

Attack verdicts. Where the readings disagree, the label column and each cell show the label or outcome under each reading, in the order set-up reading / literal reading / narrow reading, point estimates / narrow reading, with mitigation.

| attack | label | B-v1 | L-judge | C-rule-v1 | C-llm-v1 | C-llm-v1+review | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|---|
| X1_cylinder_geometry | flawed | INCONCLUSIVE · | REJECT ✓ | INCONCLUSIVE · | INCONCLUSIVE · | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ |
| X2_inlet_shear | flawed / ambiguous / credible / ambiguous | INCONCLUSIVE · / ~· / · / ~· | REJECT ✓ / ~ / ✗ / ~ | INCONCLUSIVE · / ~· / · / ~· | INCONCLUSIVE · / ~· / · / ~· | INCONCLUSIVE · / ~· / · / ~· | REJECT ✓ / ~ / ✗ / ~ | REJECT ✓ / ~ / ✗ / ~ |
| X3_compensating_errors | flawed | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | INCONCLUSIVE · | REJECT ✓ |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE · `~` / `~·` ambiguous label, not scored · ? missing · S not counted (see notes) · † counted, not covered by the last replay (see notes)

Failed checks behind the verifier REJECTs (L-judge gives no checks): C-rule-v1/X3_compensating_errors: mesh_sensitivity[strouhal_number]; C-llm-v1/X3_compensating_errors: domain_sensitivity[mean_drag_coefficient], domain_sensitivity[strouhal_number]; C-llm-v1+review/X3_compensating_errors: domain_sensitivity[mean_drag_coefficient], domain_sensitivity[strouhal_number]; B-v2/X1_cylinder_geometry: geometry_consistency; B-v2/X2_inlet_shear: inlet_uniformity; C-rule-v2/X1_cylinder_geometry: geometry_consistency; C-rule-v2/X2_inlet_shear: inlet_uniformity; C-rule-v2/X3_compensating_errors: mesh_sensitivity[strouhal_number].

B-v2 and C-rule-v2 use the v2 checks geometry_consistency and inlet_uniformity (configs/verification_v2.yaml, line 1: "v2 = pre-registered v1 + post-attack extensions"); C-llm-v1+review uses the LLM acceptance review. Both extensions were committed in 8161f5c (2026-10-19 07:40 UTC), before the attacks ran, but they are post-hoc extensions of the pre-registered verifier: their detections of X1–X3 are not blind tests (docs/methodology.md §6, 'Deviations from pre-registration', item 6).

| reading | B-v1 | L-judge | C-rule-v1 | C-llm-v1 | C-llm-v1+review | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|
| set-up reading: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 3) | 3 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 2 / 0 / 0 (of 3) | 3 / 0 / 0 (of 3) |
| literal reading: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 2 scored, 1 ambiguous) | 2 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 2 / 0 / 0 (of 2 scored, 1 ambiguous) |
| narrow reading, point estimates: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 3) | 2 / 0 / 1 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 1 (of 3) | 2 / 0 / 1 (of 3) |
| narrow reading, with mitigation: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 2 scored, 1 ambiguous) | 2 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 1 / 0 / 0 (of 2 scored, 1 ambiguous) | 2 / 0 / 0 (of 2 scored, 1 ambiguous) |

### Per-quantity verdict accuracy

_Per-quantity verdicts of the deterministic verifier (`per_qoi`) against the error e of the root's reported value. ACCEPT with e > τ is a false acceptance at quantity level. REJECT with e ≤ τ/2 rejects a quantity whose root value is accurate, and can still be right: a FAIL of the mesh, time or domain component is a demonstrated change > τ under refinement, so the root value is not converged even when it lies near T by cancellation; and the case-level REJECT may rest on another quantity. Case-level REJECTs that come from case-wide checks (mesh_quality, set-up checks) leave the per-quantity verdicts INCONCLUSIVE and do not appear in this table; the case-level REJECTs of results with every quantity e ≤ τ/2 are listed at the end of this section. Benchmark: current, non-error results; attacks: results counted in the attack section. The ACCEPT columns partition the ACCEPTs. †: includes an attack result not covered by the last replay._

| group | system | quantity verdicts | ACCEPT | ACCEPT, e ≤ τ/2 | ACCEPT, τ/2 < e ≤ τ | **ACCEPT, e > τ** | REJECT | REJECT, e ≤ τ/2 | INCONCLUSIVE |
|---|---|---|---|---|---|---|---|---|---|
| benchmark | B | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 33 |
| benchmark | C-rule | 33 | 2 | 2 | 0 | 0 | 5 | 0 | 26 |
| benchmark | C-rule-prereg | 29 | 2 | 2 | 0 | 0 | 4 | 0 | 23 |
| benchmark | C-llm | 33 | 2 | 2 | 0 | 0 | 5 | 0 | 26 |
| benchmark | Bexh | 31 | 0 | 0 | 0 | 0 | 4 | 0 | 27 |
| benchmark | C-llm-r2 | 33 | 3 | 3 | 0 | 0 | 5 | 0 | 25 |
| benchmark | C-llm-r3 | 6 | 2 | 2 | 0 | 0 | 1 | 0 | 3 |
| attacks | B-v1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| attacks | C-rule-v1 | 6 | 1 | 0 | 0 | 1 | 1 | 1 | 4 |
| attacks | C-llm-v1 | 6 | 0 | 0 | 0 | 0 | 2 | 1 | 4 |
| attacks | C-llm-v1+review | 6 | 0 | 0 | 0 | 0 | 2 | 1 | 4 |
| attacks | B-v2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| attacks | C-rule-v2 | 6 | 0 | 0 | 0 | 0 | 1 | 1 | 5 |

Not scored (no reported value of the root, or no per-quantity verdict): benchmark D1_steady_solver/strouhal_number (not produced): B, C-rule, C-rule-prereg, C-llm, Bexh, C-llm-r2.

Quantity-level false acceptances and rejections of an accurate quantity (last column: the finding holds for every reference value within T ± U(T)):

| group | case | system | quantity | error | U(T) | verifier U | quantity verdict | failing components | case verdict | finding | holds within ± U(T) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| attacks | X1_cylinder_geometry | C-rule-v1 | strouhal_number | 3.60% | 0.46% | 1.62% | ACCEPT | — | INCONCLUSIVE | false acceptance (e > τ) | yes |
| attacks | X3_compensating_errors | C-rule-v1 | strouhal_number | 0.16% | 0.46% | — | REJECT | mesh FAIL | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-llm-v1 | strouhal_number | 0.16% | 0.46% | — | REJECT | domain FAIL | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-llm-v1+review | strouhal_number | 0.16% | 0.46% | — | REJECT | domain FAIL | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-rule-v2 | strouhal_number | 0.16% | 0.46% | — | REJECT | mesh FAIL | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |

Case-level REJECTs of results with every quantity e ≤ τ/2, whatever their source (whether such a REJECT is a false rejection depends on the label, last column):

| group | case | system | err Cd | err St | quantity verdicts | failed checks | label |
|---|---|---|---|---|---|---|---|
| benchmark | J1_coarse_wake | B | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| benchmark | J1_coarse_wake | C-rule | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| benchmark | J1_coarse_wake | C-rule-prereg | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| benchmark | J1_coarse_wake | C-llm | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| benchmark | J1_coarse_wake | Bexh | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| benchmark | J1_coarse_wake | C-llm-r2 | 0.56% | 1.11% | Cd INCONCLUSIVE, St INCONCLUSIVE | mesh_quality | credible (point estimates), ambiguous (with mitigation) |
| attacks | X2_inlet_shear | B-v2 | 1.20% | 0.50% | Cd INCONCLUSIVE, St INCONCLUSIVE | inlet_uniformity | flawed (set-up reading), ambiguous (literal reading), credible (narrow reading, point estimates), ambiguous (narrow reading, with mitigation) |
| attacks | X2_inlet_shear | C-rule-v2 | 1.20% | 0.50% | Cd INCONCLUSIVE, St INCONCLUSIVE | inlet_uniformity | flawed (set-up reading), ambiguous (literal reading), credible (narrow reading, point estimates), ambiguous (narrow reading, with mitigation) |

### Criterion 5b decision rule (docs/methodology.md, 'Decision rule for success criterion 5b')

_C-llm (first run) against C-rule over the cases where both have a current, non-error result; repeats (C-llm-r*) do not enter. Correct decisions: flawed → REJECT, credible → ACCEPT. Cost: experiment cell-steps relative to the root, per case (wall time excluded). The sign test is exact, two-sided, binomial with p = 0.5, over the paired cases whose costs differ by more than 5 %. The rule does not fix the base of the 5 %: the classification uses the larger of the two costs, and the table also gives the difference relative to the C-rule cost and to the smaller of the two costs. The rule was fixed after 15 of the 17 C-llm results were known, so it is not blind to those 15 (docs/methodology.md, 'Decision rule for success criterion 5b')._

| case | label (with mitigation) | label (point estimates) | C-rule | C-llm | C-rule compute (× root) | C-llm compute (× root) | difference / cost (larger / C-rule / smaller) | differ > 5 % | cheaper |
|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 6.76 | 8.23 | 17.9% / 21.7% / 21.7% | yes | C-rule |
| K1_central_scheme | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.77 | 10.06 | 32.7% / 48.5% / 48.5% | yes | C-rule |
| K2_fine_large | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 3.74 | 6.00 | 37.6% / 60.2% / 60.2% | yes | C-rule |
| A1_coarse_mesh | flawed | flawed | REJECT | REJECT | 1.06 | 2.14 | 50.3% / 101.3% / 101.3% | yes | C-rule |
| A2_moderate_mesh | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 5.91 | 6.58 | 10.2% / 11.4% / 11.4% | yes | C-rule |
| B1_small_domain | flawed | flawed | REJECT | REJECT | 6.16 | 0.78 | 87.4% / 87.4% / 692.8% | yes | C-llm |
| B2_moderate_domain | flawed | flawed | REJECT | REJECT | 6.94 | 1.75 | 74.7% / 74.7% / 295.8% | yes | C-llm |
| C1_large_timestep | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 2.72 | 4.81 | 43.4% / 76.6% / 76.6% | yes | C-rule |
| C2_euler_large_timestep | ambiguous | flawed | INCONCLUSIVE | INCONCLUSIVE | 9.13 | 9.68 | 5.7% / 6.0% / 6.0% | yes | C-rule |
| D1_steady_solver | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| E1_noslip_side_walls | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.78 | 6.50 | 4.1% / 4.1% / 4.3% | no | — |
| F1_upwind_convection | flawed | flawed | REJECT | REJECT | 3.90 | 4.80 | 18.9% / 23.2% / 23.2% | yes | C-rule |
| G1_premature_averaging | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 10.00 | 9.78 | 2.2% / 2.2% / 2.2% | no | — |
| H1_dynamic_viscosity | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| I1_force_reference | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| J1_coarse_wake | ambiguous | credible | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| G2_average_from_start | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 11.42 | 11.95 | 4.4% / 4.6% / 4.6% | no | — |

Paired cases: 17 of 17.

| label view | correct: C-rule | correct: C-llm | **false acc.**: C-rule | **false acc.**: C-llm | false rej.: C-rule | false rej.: C-llm |
|---|---|---|---|---|---|---|
| with mitigation | 7 | 7 | 0 | 0 | 0 | 0 |
| point estimates | 7 | 7 | 0 | 0 | 1 | 1 |

- Accuracy: more correct decisions in at least one view: no; no more false acceptances or false rejections in either view: yes → LLM planner beats the rule planner on accuracy: **no**.
- Cost: total paired compute C-rule 81.29 × root, C-llm 83.06 × root (C-llm lower: no); costs differ in 10 cases, C-llm cheaper in 2, C-rule cheaper in 8; sign test p = 0.109 → LLM planner beats the rule planner on cost: **no**.
- Base of the 5 %: the three bases (larger / C-rule / smaller) classify every paired case the same way; closest to 5 %: G2_average_from_start 4.4%–4.6%, E1_noslip_side_walls 4.1%–4.3%, C2_euler_large_timestep 5.7%–6.0%.
- LLM cost on the paired cases (counts against the LLM): 5.13 USD.

**Criterion 5b: does not meet 5b: the LLM planner adds no measurable value on this benchmark.**

### Criterion 5b, sensitivity analysis: against the rule planner as literally pre-registered (scripts/run_rule_prereg.py)

_Not the committed decision rule, which names C-rule as the comparator. C-rule-prereg is the rule planner without the two RUN_LONGER rules added after the first results (docs/methodology.md §6, Deviations, item 2); same loop, validator and budgets._

_C-llm (first run) against C-rule-prereg over the cases where both have a current, non-error result; repeats (C-llm-r*) do not enter. Correct decisions: flawed → REJECT, credible → ACCEPT. Cost: experiment cell-steps relative to the root, per case (wall time excluded). The sign test is exact, two-sided, binomial with p = 0.5, over the paired cases whose costs differ by more than 5 %. The rule does not fix the base of the 5 %: the classification uses the larger of the two costs, and the table also gives the difference relative to the C-rule-prereg cost and to the smaller of the two costs. The rule was fixed after 15 of the 17 C-llm results were known, so it is not blind to those 15 (docs/methodology.md, 'Decision rule for success criterion 5b')._

| case | label (with mitigation) | label (point estimates) | C-rule-prereg | C-llm | C-rule-prereg compute (× root) | C-llm compute (× root) | difference / cost (larger / C-rule-prereg / smaller) | differ > 5 % | cheaper |
|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 6.76 | 8.23 | 17.9% / 21.7% / 21.7% | yes | C-rule-prereg |
| K1_central_scheme | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.77 | 10.06 | 32.7% / 48.5% / 48.5% | yes | C-rule-prereg |
| K2_fine_large | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 3.74 | 6.00 | 37.6% / 60.2% / 60.2% | yes | C-rule-prereg |
| A1_coarse_mesh | flawed | flawed | REJECT | REJECT | 1.06 | 2.14 | 50.3% / 101.3% / 101.3% | yes | C-rule-prereg |
| A2_moderate_mesh | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 5.91 | 6.58 | 10.2% / 11.4% / 11.4% | yes | C-rule-prereg |
| B1_small_domain | flawed | flawed | REJECT | REJECT | 6.16 | 0.78 | 87.4% / 87.4% / 692.8% | yes | C-llm |
| B2_moderate_domain | flawed | flawed | REJECT | REJECT | 6.94 | 1.75 | 74.7% / 74.7% / 295.8% | yes | C-llm |
| C1_large_timestep | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 2.72 | 4.81 | 43.4% / 76.6% / 76.6% | yes | C-rule-prereg |
| C2_euler_large_timestep | ambiguous | flawed | INCONCLUSIVE | INCONCLUSIVE | 9.13 | 9.68 | 5.7% / 6.0% / 6.0% | yes | C-rule-prereg |
| D1_steady_solver | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| E1_noslip_side_walls | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.78 | 6.50 | 4.1% / 4.1% / 4.3% | no | — |
| H1_dynamic_viscosity | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| I1_force_reference | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| J1_coarse_wake | ambiguous | credible | REJECT | REJECT | 0.00 | 0.00 | — / — / — | no | — |
| G2_average_from_start | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 11.94 | 11.95 | 0.0% / 0.0% / 0.0% | no | — |

Paired cases: 15 of 17. Not paired: F1_upwind_convection (C-rule-prereg: missing); G1_premature_averaging (C-rule-prereg: missing).

| label view | correct: C-rule-prereg | correct: C-llm | **false acc.**: C-rule-prereg | **false acc.**: C-llm | false rej.: C-rule-prereg | false rej.: C-llm |
|---|---|---|---|---|---|---|
| with mitigation | 6 | 6 | 0 | 0 | 0 | 0 |
| point estimates | 6 | 6 | 0 | 0 | 1 | 1 |

- Accuracy: more correct decisions in at least one view: no; no more false acceptances or false rejections in either view: yes → LLM planner beats the rule planner on accuracy: **no**.
- Cost: total paired compute C-rule-prereg 67.92 × root, C-llm 68.47 × root (C-llm lower: no); costs differ in 9 cases, C-llm cheaper in 2, C-rule-prereg cheaper in 7; sign test p = 0.18 → LLM planner beats the rule planner on cost: **no**.
- Base of the 5 %: the three bases (larger / C-rule-prereg / smaller) classify every paired case the same way; closest to 5 %: E1_noslip_side_walls 4.1%–4.3%, C2_euler_large_timestep 5.7%–6.0%, G2_average_from_start 0.0%–0.0%.
- LLM cost on the paired cases (counts against the LLM): 4.68 USD.

**Criterion 5b: does not meet 5b: the LLM planner adds no measurable value on this benchmark.** Provisional: the rule is applied to the 15 paired cases; the conclusion can change when the 2 unpaired case(s) have current, non-error results in both systems.
