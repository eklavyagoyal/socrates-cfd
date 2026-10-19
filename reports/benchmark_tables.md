**Missing or stale results (NOT counted in the rates of the system concerned; recompute before drawing conclusions):** C-rule/K1_central_scheme: missing; C-rule/K2_fine_large: missing; C-rule/A2_moderate_mesh: missing; C-rule/B1_small_domain: missing; C-rule/B2_moderate_domain: missing; C-rule/C1_large_timestep: missing; C-rule/C2_euler_large_timestep: missing; C-rule/E1_noslip_side_walls: missing; C-rule/F1_upwind_convection: missing; C-rule/G1_premature_averaging: missing; C-rule/G2_average_from_start: missing; C-llm/baseline: missing; C-llm/K1_central_scheme: missing; C-llm/K2_fine_large: missing; C-llm/A1_coarse_mesh: missing; C-llm/A2_moderate_mesh: missing; C-llm/B2_moderate_domain: missing; C-llm/C1_large_timestep: missing; C-llm/C2_euler_large_timestep: missing; C-llm/E1_noslip_side_walls: missing; C-llm/F1_upwind_convection: missing; C-llm/G1_premature_averaging: missing; C-llm/G2_average_from_start: missing; Bexh/K1_central_scheme: missing; Bexh/K2_fine_large: missing; Bexh/A1_coarse_mesh: missing; Bexh/A2_moderate_mesh: missing; Bexh/B1_small_domain: missing; Bexh/B2_moderate_domain: missing; Bexh/C1_large_timestep: missing; Bexh/C2_euler_large_timestep: missing; Bexh/E1_noslip_side_walls: missing; Bexh/F1_upwind_convection: missing; Bexh/G1_premature_averaging: missing; Bexh/H1_dynamic_viscosity: missing; Bexh/I1_force_reference: missing; Bexh/J1_coarse_wake: missing; Bexh/G2_average_from_start: missing

| case | label | max err / τ | unstable | point-estimate label (secondary) | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | 0.45 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | INCONCLUSIVE ~· | — ? | INCONCLUSIVE ~· |
| K1_central_scheme | ambiguous | 0.69 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| K2_fine_large | ambiguous | 0.37 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| A1_coarse_mesh | flawed | 1.87 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | — ? | — ? |
| A2_moderate_mesh | ambiguous | 0.66 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| B1_small_domain | flawed | 4.96 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | REJECT ✓ | — ? |
| B2_moderate_domain | flawed | 1.47 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | — ? | — ? |
| C1_large_timestep | ambiguous | 0.27 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| C2_euler_large_timestep | ambiguous | 1.29 | mean_drag_coefficient,strouhal_number | flawed | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | — ? | — ? | — ? |
| D1_steady_solver | flawed | 5.61 |  | flawed | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| E1_noslip_side_walls | ambiguous | 0.68 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |
| F1_upwind_convection | flawed | 7.83 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | — ? | — ? |
| G1_premature_averaging | ambiguous | 0.72 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | REJECT ~ | — ? | — ? | — ? |
| H1_dynamic_viscosity | flawed | 2.19 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| I1_force_reference | flawed | 3.64 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | — ? |
| J1_coarse_wake | ambiguous | 0.55 | strouhal_number | ambiguous | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | — ? |
| G2_average_from_start | ambiguous | 0.69 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? | — ? |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · `~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · S stale (not counted)

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| cases | 17 | 17 | 17 | 6 | 5 | 2 |
| flawed cases (decided) | 7 | 7 | 7 | 4 | 4 | 1 |
| credible cases (decided) | 0 | 0 | 0 | 0 | 0 | 0 |
| ambiguous cases (decided) | 10 | 10 | 10 | 2 | 1 | 1 |
| **false acceptance** (flawed → ACCEPT) | 0.86 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection (flawed → REJECT) | 0.14 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 |
| missed but safe (flawed → INCONCLUSIVE) | 0.00 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 |
| correct acceptance (credible → ACCEPT) | — | — | — | — | — | — |
| false rejection (credible → REJECT) | — | — | — | — | — | — |
| inconclusive (all decided) | 0.00 | 0.76 | 0.06 | 0.17 | 0.00 | 0.50 |
| ambiguous cases: verdicts | ACC:9 REJ:1 INC:0 | ACC:0 REJ:1 INC:9 | ACC:7 REJ:2 INC:1 | ACC:0 REJ:1 INC:1 | ACC:0 REJ:1 INC:0 | ACC:0 REJ:0 INC:1 |
| ambiguous cases ACCEPTed although best-estimate error > τ | 1 | 0 | 0 | 0 | 0 | 0 |
| errors (excluded from rates) | 0 | 0 | 0 | 0 | 0 | 0 |
| stale results (excluded) | 0 | 0 | 0 | 0 | 0 | 0 |
| missing results | 0 | 0 | 0 | 11 | 12 | 15 |
| errors by label | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 |
| mean extra simulations / case | 0.00 | 0.00 | 0.00 | 1.00 | 0.20 | 4.00 |
| mean extra compute / case (× root) | 0.00 | 0.00 | 0.00 | 1.30 | 0.16 | 5.81 |
| total experiment wall time (h) | 0.00 | 0.00 | 0.00 | 6.50 | 0.19 | 6.20 |
| LLM cost (USD) | 0.00 | 0.00 | 0.54 | 0.00 | 0.05 | 0.00 |
| authority violations | 0 | 0 | 0 | 0 | 0 | 0 |
| untraceable numbers in LLM text | 0 | 0 | 27 | 0 | 1 | 0 |
| first experiment targets the flaw | — | — | — | 1/1 | 1/1 | — |

### Secondary view (post-hoc): labels from point estimates, truth uncertainty ignored

_Same verdicts; only the labels change. The pre-registered labels above are primary._

| metric | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| flawed cases | 8 | 8 | 8 | 4 | 4 | 1 |
| credible cases | 3 | 3 | 3 | 1 | 0 | 1 |
| ambiguous cases | 6 | 6 | 6 | 1 | 1 | 0 |
| **false acceptance** | 0.88 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection | 0.12 | 0.38 | 0.88 | 1.00 | 1.00 | 1.00 |
| missed but safe | 0.00 | 0.62 | 0.12 | 0.00 | 0.00 | 0.00 |
| correct acceptance | 1.00 | 0.00 | 1.00 | 0.00 | — | 0.00 |
| false rejection | 0.00 | 0.00 | 0.00 | 0.00 | — | 0.00 |

### Calibration: the verifier's uncertainty estimate vs the error against the reference

_Cases where mesh, time and domain all carry an estimate. U = averaging bias + RSS(components). 'within U(T)': not covered by U alone, but by U combined with the reference's own uncertainty._

| case | system | quantity | error vs reference | verifier U | verdict | covered |
|---|---|---|---|---|---|---|
| baseline | C-rule | mean_drag_coefficient | 1.36% | 2.42% | INCONCLUSIVE | yes |
| baseline | C-rule | strouhal_number | 0.86% | 1.59% | ACCEPT | yes |
| baseline | Bexh | mean_drag_coefficient | 1.36% | 4.21% | INCONCLUSIVE | yes |
| baseline | Bexh | strouhal_number | 0.86% | 2.96% | INCONCLUSIVE | yes |

Covered by U: 4/4; by U combined with U(T): 4/4.
