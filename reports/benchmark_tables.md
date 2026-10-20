**Missing or stale results (NOT counted in the rates of the system concerned; recompute before drawing conclusions):** C-llm/K2_fine_large: missing; Bexh/A1_coarse_mesh: missing; Bexh/B1_small_domain: missing; Bexh/F1_upwind_convection: missing; Bexh/H1_dynamic_viscosity: missing; Bexh/J1_coarse_wake: missing

_Percentages: errors against the reference T are relative to T. Verifier sensitivity changes are relative to the finer (child) member of a study, |q_fine − q_root| / |q_fine| (checks/sensitivity.py; the finest member for a three-level chain). Observation lines in the case reports (reports/cases/) and the loop traces in benchmark_results.md are relative to the parent run, (q_child − q_parent) / q_parent._

| case | label (with mitigation) | max err / τ | unstable | label without mitigation | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | 0.40 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| K1_central_scheme | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| K2_fine_large | ambiguous | 0.31 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | — ? | INCONCLUSIVE ~· |
| A1_coarse_mesh | flawed | 1.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| A2_moderate_mesh | ambiguous | 0.48 | strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| B1_small_domain | flawed | 4.90 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| B2_moderate_domain | flawed | 1.41 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | INCONCLUSIVE · |
| C1_large_timestep | ambiguous | 0.21 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| C2_euler_large_timestep | ambiguous | 1.11 | mean_drag_coefficient,strouhal_number | flawed | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| D1_steady_solver | flawed | 5.66 |  | flawed | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| E1_noslip_side_walls | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| F1_upwind_convection | flawed | 7.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| G1_premature_averaging | ambiguous | 0.54 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | REJECT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| H1_dynamic_viscosity | flawed | 2.02 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| I1_force_reference | flawed | 3.68 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| J1_coarse_wake | ambiguous | 0.37 | strouhal_number | credible | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | — ? |
| G2_average_from_start | ambiguous | 0.51 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · `~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · S stale (not counted)

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| cases | 17 | 17 | 17 | 17 | 16 | 12 |
| flawed cases (decided) | 7 | 7 | 7 | 7 | 7 | 3 |
| credible cases (decided) | 0 | 0 | 0 | 0 | 0 | 0 |
| ambiguous cases (decided) | 10 | 10 | 10 | 10 | 9 | 9 |
| **false acceptance** (flawed → ACCEPT) | 0.86 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection (flawed → REJECT) | 0.14 | 0.43 | 1.00 | 1.00 | 1.00 | 0.67 |
| missed but safe (flawed → INCONCLUSIVE) | 0.00 | 0.57 | 0.00 | 0.00 | 0.00 | 0.33 |
| correct acceptance (credible → ACCEPT) | — | — | — | — | — | — |
| false rejection (credible → REJECT) | — | — | — | — | — | — |
| inconclusive (all decided) | 0.00 | 0.76 | 0.06 | 0.53 | 0.50 | 0.83 |
| ambiguous cases: verdicts | ACC:9 REJ:1 INC:0 | ACC:0 REJ:1 INC:9 | ACC:7 REJ:2 INC:1 | ACC:0 REJ:1 INC:9 | ACC:0 REJ:1 INC:8 | ACC:0 REJ:0 INC:9 |
| ambiguous cases ACCEPTed although best-estimate error > τ | 1 | 0 | 0 | 0 | 0 | 0 |
| errors (excluded from rates) | 0 | 0 | 0 | 0 | 0 | 0 |
| stale results (excluded) | 0 | 0 | 0 | 0 | 0 | 0 |
| missing results | 0 | 0 | 0 | 0 | 1 | 5 |
| errors by label | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 |
| mean extra simulations / case | 0.00 | 0.00 | 0.00 | 3.47 | 2.88 | 4.75 |
| mean extra compute / case (× root) | 0.00 | 0.00 | 0.00 | 4.78 | 4.82 | 7.73 |
| total experiment wall time (h) | 0.00 | 0.00 | 0.00 | 31.73 | 30.31 | 33.66 |
| LLM cost (USD) | 0.00 | 0.00 | 0.54 | 0.00 | 4.47 | 0.00 |
| authority violations | 0 | 0 | 0 | 0 | 0 | 0 |
| untraceable numbers in LLM text | 0 | 0 | 27 | 0 | 46 | 0 |
| first experiment targets the flaw | — | — | — | 1/4 | 4/4 | — |

### Labels without the truth-uncertainty mitigation (design.md §19 rule verbatim, point estimates)

_Same verdicts; only the labels change. Both label sets are pre-registered: the §19 rule, and the risk mitigation 'label near-boundary cases ambiguous' (design.md, major technical risks 2), operationalised in review R18 before any result as 'the interval e ± U(T) straddles τ or τ/2'. The table above uses the mitigation._

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| flawed cases | 8 | 8 | 8 | 8 | 8 | 4 |
| credible cases | 5 | 5 | 5 | 5 | 4 | 4 |
| ambiguous cases | 4 | 4 | 4 | 4 | 4 | 4 |
| **false acceptance** | 0.88 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection | 0.12 | 0.38 | 0.88 | 0.88 | 0.88 | 0.50 |
| missed but safe | 0.00 | 0.62 | 0.12 | 0.12 | 0.12 | 0.50 |
| correct acceptance | 0.80 | 0.00 | 0.80 | 0.00 | 0.00 | 0.00 |
| false rejection | 0.20 | 0.20 | 0.20 | 0.20 | 0.25 | 0.00 |

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
| baseline | C-llm | mean_drag_coefficient | 1.20% | 2.24% | INCONCLUSIVE | yes |
| baseline | C-llm | strouhal_number | 0.31% | 2.31% | INCONCLUSIVE | yes |
| K1_central_scheme | C-llm | mean_drag_coefficient | 1.90% | 4.05% | INCONCLUSIVE | yes |
| K1_central_scheme | C-llm | strouhal_number | 0.39% | 2.66% | INCONCLUSIVE | yes |
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
| A2_moderate_mesh | Bexh | mean_drag_coefficient | 0.51% | 4.61% | INCONCLUSIVE | yes |
| A2_moderate_mesh | Bexh | strouhal_number | 1.45% | 3.83% | INCONCLUSIVE | yes |
| B2_moderate_domain | Bexh | mean_drag_coefficient | 4.24% | 14.28% | INCONCLUSIVE | yes |
| B2_moderate_domain | Bexh | strouhal_number | 1.89% | 10.43% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | Bexh | mean_drag_coefficient | 1.89% | 8.88% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | Bexh | strouhal_number | 0.21% | 5.64% | INCONCLUSIVE | yes |
| G1_premature_averaging | Bexh | mean_drag_coefficient | 1.47% | 6.87% | INCONCLUSIVE | yes |
| G1_premature_averaging | Bexh | strouhal_number | 1.62% | 4.30% | INCONCLUSIVE | yes |
| I1_force_reference | Bexh | mean_drag_coefficient | 11.05% | 4.21% | INCONCLUSIVE | **NO** |
| I1_force_reference | Bexh | strouhal_number | 0.31% | 2.96% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | mean_drag_coefficient | 0.32% | 5.18% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | strouhal_number | 1.52% | 4.27% | INCONCLUSIVE | yes |

Benchmark cases only: covered by U: 36/37; by U combined with U(T): 36/37.

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

Attack cases only: covered by U: 4/10; by U combined with U(T): 4/10.

### LLM run-to-run variance (independent repeats of C-llm)

| case | label | C-llm | C-llm-r2 | same verdict | same experiment sequence |
|---|---|---|---|---|---|
| baseline | ambiguous | INCONCLUSIVE (REFINE → EXPAND → REDUCE → EXPAND → REFINE → EXPAND) | INCONCLUSIVE (REFINE → REFINE → EXPAND → EXPAND → REDUCE → EXPAND) | yes | no |
| K1_central_scheme | ambiguous | INCONCLUSIVE (REFINE → REFINE → EXPAND → REDUCE → EXPAND → REDUCE) | INCONCLUSIVE (REFINE → EXPAND → EXPAND → REDUCE → REFINE → EXPAND) | yes | no |
| K2_fine_large | ambiguous | — | — | incomplete | incomplete |
| A1_coarse_mesh | flawed | REJECT (REFINE) | REJECT (REFINE) | yes | yes |
| A2_moderate_mesh | ambiguous | INCONCLUSIVE | — | incomplete | incomplete |
| B1_small_domain | flawed | REJECT (EXPAND) | REJECT (EXPAND) | yes | no |
| B2_moderate_domain | flawed | REJECT (EXPAND → EXPAND) | REJECT (EXPAND → EXPAND) | yes | yes |
| C1_large_timestep | ambiguous | INCONCLUSIVE (REFINE → REDUCE → REFINE → EXPAND → REFINE → EXPAND) | INCONCLUSIVE (REFINE → REDUCE → REFINE → EXPAND → EXPAND → REFINE) | yes | no |
| C2_euler_large_timestep | ambiguous | INCONCLUSIVE | — | incomplete | incomplete |
| D1_steady_solver | flawed | REJECT (none) | REJECT (none) | yes | yes |
| E1_noslip_side_walls | ambiguous | INCONCLUSIVE | — | incomplete | incomplete |
| F1_upwind_convection | flawed | REJECT | — | incomplete | incomplete |
| G1_premature_averaging | ambiguous | INCONCLUSIVE (RUN → REFINE → EXPAND) | INCONCLUSIVE (RUN → REFINE → EXPAND) | yes | yes |
| H1_dynamic_viscosity | flawed | REJECT (none) | REJECT (none) | yes | yes |
| I1_force_reference | flawed | REJECT (none) | REJECT (none) | yes | yes |
| J1_coarse_wake | ambiguous | REJECT (none) | REJECT (none) | yes | yes |
| G2_average_from_start | ambiguous | INCONCLUSIVE | — | incomplete | incomplete |

Complete repeat sets: 11; identical verdict in 11/11; identical experiment sequence in 7/11.

### Attack cases against the reference

_Attack roots (cases/attacks/) labelled with the benchmark rule (orchestration/truth.label_case) against the same reference T. Errors are signed, (reported − T)/T. Strict reading: only the set-up problems the benchmark labels use (wrong Re or steady formulation, read from the evidence) count; set-up reading: the attack's departure from the problem statement (case definition) counts as well._

| attack | reported Cd | reported St | err Cd | err St | max err / τ | set-up departure (case definition) | label: strict, point estimates | label: strict, with mitigation | label: set-up reading |
|---|---|---|---|---|---|---|---|---|---|
| X1_cylinder_geometry | 1.3941 | 0.1580 | +5.98% | -3.60% | 1.99 | meshed cylinder diameter 1.05 D while Re, force reference and St assume D | flawed | flawed | flawed |
| X2_inlet_shear | 1.3312 | 0.1631 | +1.20% | -0.50% | 0.40 | sheared inlet profile; the problem specifies a uniform stream | credible | ambiguous | flawed |
| X3_compensating_errors | 1.3918 | 0.1642 | +5.81% | +0.16% | 1.94 | none | flawed | flawed | flawed |

**X2_inlet_shear:** the point-estimate errors (Cd 1.20%, St 0.50%) are within τ/2 = 1.5% for every quantity, so X2_inlet_shear is flawed only if the §19 set-up clause applies. The clause (docs/design.md §19, pre-registered evaluation protocol): a case is flawed "if the set-up answers a different problem (wrong Re or regime)". The evidence shows neither (configured Re = 100, solver pimpleFoam). Strict reading (the parenthesis is exhaustive): X2_inlet_shear is labelled by its error, credible on point estimates and ambiguous with the truth-uncertainty mitigation (Cd 1.20% ± 0.94% straddles τ/2). Set-up reading (the parenthesis gives examples; here: sheared inlet profile; the problem specifies a uniform stream): flawed.

Attack verdicts. Where the readings disagree the cell shows the outcome under the set-up reading / under the strict reading on point estimates (with the mitigation the strict label of such a case may be ambiguous, and its verdict is then not scored; see the labels above).

| attack | label: set-up / strict (point) | B-v1 | L-judge | C-rule-v1 | C-llm-v1 | C-llm-v1+review | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|---|
| X1_cylinder_geometry | flawed / flawed | INCONCLUSIVE · | REJECT ✓ | INCONCLUSIVE · | INCONCLUSIVE · | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ |
| X2_inlet_shear | flawed / credible | INCONCLUSIVE · | REJECT ✓ / ✗ | INCONCLUSIVE · | INCONCLUSIVE · | INCONCLUSIVE · | REJECT ✓ / ✗ | REJECT ✓ / ✗ |
| X3_compensating_errors | flawed / flawed | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | INCONCLUSIVE · | REJECT ✓ |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE · `~` / `~·` ambiguous label, not scored · ? missing · S not counted (see notes)

| reading | B-v1 | L-judge | C-rule-v1 | C-llm-v1 | C-llm-v1+review | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|
| set-up reading: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 3) | 3 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 2 / 0 / 0 (of 3) | 3 / 0 / 0 (of 3) |
| strict reading, point estimates: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 3) | 2 / 0 / 1 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 1 (of 3) | 2 / 0 / 1 (of 3) |
| strict reading, with mitigation: correct / **false acc.** / false rej. | 0 / 0 / 0 (of 3) | 2 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 1 / 0 / 0 (of 3) | 2 / 0 / 0 (of 3) |

Notes on the attack results: C-rule-v1/X2_inlet_shear: counted, written after the last replay (run scripts/replay_verdicts.py to check it); C-llm-v1+review/X1_cylinder_geometry: counted, written after the last replay (run scripts/replay_verdicts.py to check it).

### Per-quantity verdict accuracy

_Per-quantity verdicts of the deterministic verifier (`per_qoi`) against the error e of the root's reported value. ACCEPT with e > τ is a false acceptance at quantity level; REJECT with e ≤ τ/2 rejects an accurate quantity (the case-level REJECT can still be right when another quantity is wrong). Benchmark: current, non-error results; attacks: results counted in the attack section. The ACCEPT columns partition the ACCEPTs._

| group | system | quantity verdicts | ACCEPT | ACCEPT, e ≤ τ/2 | ACCEPT, τ/2 < e ≤ τ | **ACCEPT, e > τ** | REJECT | REJECT, e ≤ τ/2 | INCONCLUSIVE |
|---|---|---|---|---|---|---|---|---|---|
| benchmark | B | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 33 |
| benchmark | C-rule | 33 | 2 | 2 | 0 | 0 | 5 | 0 | 26 |
| benchmark | C-llm | 31 | 1 | 1 | 0 | 0 | 5 | 0 | 25 |
| benchmark | Bexh | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 23 |
| benchmark | C-llm-r2 | 21 | 1 | 1 | 0 | 0 | 4 | 0 | 16 |
| attacks | B-v1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| attacks | C-rule-v1 | 6 | 1 | 0 | 0 | 1 | 1 | 1 | 4 |
| attacks | C-llm-v1 | 6 | 0 | 0 | 0 | 0 | 2 | 1 | 4 |
| attacks | C-llm-v1+review | 6 | 0 | 0 | 0 | 0 | 2 | 1 | 4 |
| attacks | B-v2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| attacks | C-rule-v2 | 6 | 0 | 0 | 0 | 0 | 1 | 1 | 5 |

Quantity-level false acceptances and rejections of an accurate quantity (last column: the finding holds for every reference value within T ± U(T)):

| group | case | system | quantity | error | U(T) | verifier U | quantity verdict | case verdict | finding | holds within ± U(T) |
|---|---|---|---|---|---|---|---|---|---|---|
| attacks | X1_cylinder_geometry | C-rule-v1 | strouhal_number | 3.60% | 0.46% | 1.62% | ACCEPT | INCONCLUSIVE | false acceptance (e > τ) | yes |
| attacks | X3_compensating_errors | C-rule-v1 | strouhal_number | 0.16% | 0.46% | — | REJECT | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-llm-v1 | strouhal_number | 0.16% | 0.46% | — | REJECT | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-llm-v1+review | strouhal_number | 0.16% | 0.46% | — | REJECT | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |
| attacks | X3_compensating_errors | C-rule-v2 | strouhal_number | 0.16% | 0.46% | — | REJECT | REJECT | REJECT of an accurate quantity (e ≤ τ/2) | yes |

### Criterion 5b decision rule (docs/methodology.md, 'Decision rule for success criterion 5b')

_C-llm (first run) against C-rule over the cases where both have a current, non-error result; repeats (C-llm-r*) do not enter. Correct decisions: flawed → REJECT, credible → ACCEPT. Cost: experiment cell-steps relative to the root, per case (wall time excluded). Costs differ when |C-llm − C-rule| > 5 % of the larger of the two; the sign test is exact, two-sided, binomial with p = 0.5, over those cases._

| case | label (with mitigation) | label (point estimates) | C-rule | C-llm | C-rule compute (× root) | C-llm compute (× root) | differ > 5 % | cheaper |
|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 6.76 | 8.23 | yes | C-rule |
| K1_central_scheme | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.77 | 10.06 | yes | C-rule |
| A1_coarse_mesh | flawed | flawed | REJECT | REJECT | 1.06 | 2.14 | yes | C-rule |
| A2_moderate_mesh | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 5.91 | 6.58 | yes | C-rule |
| B1_small_domain | flawed | flawed | REJECT | REJECT | 6.16 | 0.78 | yes | C-llm |
| B2_moderate_domain | flawed | flawed | REJECT | REJECT | 6.94 | 1.75 | yes | C-llm |
| C1_large_timestep | ambiguous | credible | INCONCLUSIVE | INCONCLUSIVE | 2.72 | 4.81 | yes | C-rule |
| C2_euler_large_timestep | ambiguous | flawed | INCONCLUSIVE | INCONCLUSIVE | 9.13 | 9.68 | yes | C-rule |
| D1_steady_solver | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | no | — |
| E1_noslip_side_walls | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 6.78 | 6.50 | no | — |
| F1_upwind_convection | flawed | flawed | REJECT | REJECT | 3.90 | 4.80 | yes | C-rule |
| G1_premature_averaging | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 10.00 | 9.78 | no | — |
| H1_dynamic_viscosity | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | no | — |
| I1_force_reference | flawed | flawed | REJECT | REJECT | 0.00 | 0.00 | no | — |
| J1_coarse_wake | ambiguous | credible | REJECT | REJECT | 0.00 | 0.00 | no | — |
| G2_average_from_start | ambiguous | ambiguous | INCONCLUSIVE | INCONCLUSIVE | 11.42 | 11.95 | no | — |

Paired cases: 16 of 17. Not paired: K2_fine_large (C-llm: missing).

| label view | correct: C-rule | correct: C-llm | **false acc.**: C-rule | **false acc.**: C-llm | false rej.: C-rule | false rej.: C-llm |
|---|---|---|---|---|---|---|
| with mitigation | 7 | 7 | 0 | 0 | 0 | 0 |
| point estimates | 7 | 7 | 0 | 0 | 1 | 1 |

- Accuracy: more correct decisions in at least one view: no; no more false acceptances or false rejections in either view: yes → LLM planner beats the rule planner on accuracy: **no**.
- Cost: total paired compute C-rule 77.55 × root, C-llm 77.06 × root (C-llm lower: yes); costs differ in 9 cases, C-llm cheaper in 2, C-rule cheaper in 7; sign test p = 0.18 → LLM planner beats the rule planner on cost: **no**.
- LLM cost on the paired cases (counts against the LLM): 4.47 USD.

**Criterion 5b: does not meet 5b: the LLM planner adds no measurable value on this benchmark.** Provisional: the rule is applied to the 16 paired cases; the conclusion can change when the 1 unpaired case(s) have current, non-error results in both systems.
