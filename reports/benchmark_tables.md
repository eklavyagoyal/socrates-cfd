**Missing or stale results (NOT counted in the rates of the system concerned; recompute before drawing conclusions):** C-rule/K1_central_scheme: missing; C-rule/K2_fine_large: missing; C-rule/B2_moderate_domain: missing; C-rule/C1_large_timestep: missing; C-rule/F1_upwind_convection: missing; C-rule/G1_premature_averaging: missing; C-rule/G2_average_from_start: missing; C-llm/K1_central_scheme: missing; C-llm/K2_fine_large: missing; C-llm/C1_large_timestep: missing; C-llm/G1_premature_averaging: missing; Bexh/K1_central_scheme: missing; Bexh/K2_fine_large: missing; Bexh/A1_coarse_mesh: missing; Bexh/A2_moderate_mesh: missing; Bexh/B1_small_domain: missing; Bexh/B2_moderate_domain: missing; Bexh/C1_large_timestep: missing; Bexh/E1_noslip_side_walls: missing; Bexh/F1_upwind_convection: missing; Bexh/G1_premature_averaging: missing; Bexh/H1_dynamic_viscosity: missing; Bexh/J1_coarse_wake: missing

| case | label (with mitigation) | max err / τ | unstable | label without mitigation | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | 0.40 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| K1_central_scheme | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| K2_fine_large | ambiguous | 0.31 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| A1_coarse_mesh | flawed | 1.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| A2_moderate_mesh | ambiguous | 0.48 | strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | — ? |
| B1_small_domain | flawed | 4.90 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| B2_moderate_domain | flawed | 1.41 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | REJECT ✓ | — ? |
| C1_large_timestep | ambiguous | 0.21 | mean_drag_coefficient | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| C2_euler_large_timestep | ambiguous | 1.11 | mean_drag_coefficient,strouhal_number | flawed | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· | INCONCLUSIVE ~· |
| D1_steady_solver | flawed | 5.66 |  | flawed | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| E1_noslip_side_walls | ambiguous | 0.63 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | — ? |
| F1_upwind_convection | flawed | 7.69 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | REJECT ✓ | — ? |
| G1_premature_averaging | ambiguous | 0.54 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | REJECT ~ | — ? | — ? | — ? |
| H1_dynamic_viscosity | flawed | 2.02 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| I1_force_reference | flawed | 3.68 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| J1_coarse_wake | ambiguous | 0.37 | strouhal_number | credible | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | — ? |
| G2_average_from_start | ambiguous | 0.51 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | INCONCLUSIVE ~· | INCONCLUSIVE ~· |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · `~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · S stale (not counted)

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| cases | 17 | 17 | 17 | 10 | 13 | 5 |
| flawed cases (decided) | 7 | 7 | 7 | 5 | 7 | 2 |
| credible cases (decided) | 0 | 0 | 0 | 0 | 0 | 0 |
| ambiguous cases (decided) | 10 | 10 | 10 | 5 | 6 | 3 |
| **false acceptance** (flawed → ACCEPT) | 0.86 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection (flawed → REJECT) | 0.14 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 |
| missed but safe (flawed → INCONCLUSIVE) | 0.00 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 |
| correct acceptance (credible → ACCEPT) | — | — | — | — | — | — |
| false rejection (credible → REJECT) | — | — | — | — | — | — |
| inconclusive (all decided) | 0.00 | 0.76 | 0.06 | 0.40 | 0.38 | 0.60 |
| ambiguous cases: verdicts | ACC:9 REJ:1 INC:0 | ACC:0 REJ:1 INC:9 | ACC:7 REJ:2 INC:1 | ACC:0 REJ:1 INC:4 | ACC:0 REJ:1 INC:5 | ACC:0 REJ:0 INC:3 |
| ambiguous cases ACCEPTed although best-estimate error > τ | 1 | 0 | 0 | 0 | 0 | 0 |
| errors (excluded from rates) | 0 | 0 | 0 | 0 | 0 | 0 |
| stale results (excluded) | 0 | 0 | 0 | 0 | 0 | 0 |
| missing results | 0 | 0 | 0 | 7 | 4 | 12 |
| errors by label | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 |
| mean extra simulations / case | 0.00 | 0.00 | 0.00 | 2.60 | 2.38 | 4.60 |
| mean extra compute / case (× root) | 0.00 | 0.00 | 0.00 | 3.58 | 4.03 | 7.39 |
| total experiment wall time (h) | 0.00 | 0.00 | 0.00 | 14.99 | 21.64 | 14.72 |
| LLM cost (USD) | 0.00 | 0.00 | 0.54 | 0.00 | 3.01 | 0.00 |
| authority violations | 0 | 0 | 0 | 0 | 0 | 0 |
| untraceable numbers in LLM text | 0 | 0 | 27 | 0 | 24 | 0 |
| first experiment targets the flaw | — | — | — | 1/2 | 4/4 | — |

### Labels without the truth-uncertainty mitigation (design.md §19 rule verbatim, point estimates)

_Same verdicts; only the labels change. Both label sets are pre-registered: the §19 rule, and the risk mitigation 'label near-boundary cases ambiguous' (design.md, major technical risks 2), operationalised in review R18 before any result as 'the interval e ± U(T) straddles τ or τ/2'. The table above uses the mitigation._

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| flawed cases | 8 | 8 | 8 | 6 | 8 | 3 |
| credible cases | 5 | 5 | 5 | 3 | 3 | 1 |
| ambiguous cases | 4 | 4 | 4 | 1 | 2 | 1 |
| **false acceptance** | 0.88 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection | 0.12 | 0.38 | 0.88 | 0.83 | 0.88 | 0.67 |
| missed but safe | 0.00 | 0.62 | 0.12 | 0.17 | 0.12 | 0.33 |
| correct acceptance | 0.80 | 0.00 | 0.80 | 0.00 | 0.00 | 0.00 |
| false rejection | 0.20 | 0.20 | 0.20 | 0.33 | 0.33 | 0.00 |

### Calibration: the verifier's uncertainty estimate vs the error against the reference

_Cases where mesh, time and domain all carry an estimate. U = averaging bias + RSS(components). 'within U(T)': not covered by U alone, but by U combined with the reference's own uncertainty._

| case | system | quantity | error vs reference | verifier U | verdict | covered |
|---|---|---|---|---|---|---|
| baseline | C-rule | mean_drag_coefficient | 1.20% | 2.42% | INCONCLUSIVE | yes |
| baseline | C-rule | strouhal_number | 0.31% | 1.59% | ACCEPT | yes |
| A2_moderate_mesh | C-rule | mean_drag_coefficient | 0.51% | 2.40% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-rule | strouhal_number | 1.45% | 2.74% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule | mean_drag_coefficient | 1.89% | 3.45% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-rule | strouhal_number | 0.21% | 2.94% | INCONCLUSIVE | yes |
| baseline | C-llm | mean_drag_coefficient | 1.20% | 2.24% | INCONCLUSIVE | yes |
| baseline | C-llm | strouhal_number | 0.31% | 2.31% | INCONCLUSIVE | yes |
| A2_moderate_mesh | C-llm | mean_drag_coefficient | 0.51% | 2.23% | ACCEPT | yes |
| A2_moderate_mesh | C-llm | strouhal_number | 1.45% | 2.89% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-llm | mean_drag_coefficient | 1.89% | 3.03% | INCONCLUSIVE | yes |
| E1_noslip_side_walls | C-llm | strouhal_number | 0.21% | 2.94% | INCONCLUSIVE | yes |
| baseline | Bexh | mean_drag_coefficient | 1.20% | 4.21% | INCONCLUSIVE | yes |
| baseline | Bexh | strouhal_number | 0.31% | 2.96% | INCONCLUSIVE | yes |
| I1_force_reference | Bexh | mean_drag_coefficient | 11.05% | 4.21% | INCONCLUSIVE | **NO** |
| I1_force_reference | Bexh | strouhal_number | 0.31% | 2.96% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | mean_drag_coefficient | 0.32% | 5.18% | INCONCLUSIVE | yes |
| G2_average_from_start | Bexh | strouhal_number | 1.52% | 4.27% | INCONCLUSIVE | yes |

Covered by U: 17/18; by U combined with U(T): 17/18.
