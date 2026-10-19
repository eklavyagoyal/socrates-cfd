**Missing or stale results (NOT counted in the rates of the system concerned; recompute before drawing conclusions):** system Bexh: no results; A/K1_central_scheme: stale (evidence re-extracted after the result was written: ['K1_central_scheme-e4e5fb66bdca']); B/K1_central_scheme: stale (evidence re-extracted after the result was written: ['K1_central_scheme-e4e5fb66bdca']); L-judge/K1_central_scheme: stale (evidence re-extracted after the result was written: ['K1_central_scheme-e4e5fb66bdca']); C-rule/baseline: missing; C-rule/K1_central_scheme: missing; C-rule/K2_fine_large: missing; C-rule/A2_moderate_mesh: missing; C-rule/B1_small_domain: missing; C-rule/B2_moderate_domain: missing; C-rule/C1_large_timestep: missing; C-rule/C2_euler_large_timestep: missing; C-rule/E1_noslip_side_walls: missing; C-rule/F1_upwind_convection: missing; C-rule/G1_premature_averaging: missing; C-rule/G2_average_from_start: missing; C-llm/baseline: missing; C-llm/K1_central_scheme: missing; C-llm/K2_fine_large: missing; C-llm/A1_coarse_mesh: missing; C-llm/A2_moderate_mesh: missing; C-llm/B2_moderate_domain: missing; C-llm/C1_large_timestep: missing; C-llm/C2_euler_large_timestep: missing; C-llm/E1_noslip_side_walls: missing; C-llm/F1_upwind_convection: missing; C-llm/G1_premature_averaging: missing; C-llm/G2_average_from_start: missing

| case | label | max err / τ | unstable | point-estimate label (secondary) | A | B | L-judge | C-rule | C-llm |
|---|---|---|---|---|---|---|---|---|---|
| baseline | ambiguous | 0.46 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |
| K1_central_scheme | ambiguous | 0.69 | mean_drag_coefficient,strouhal_number | ambiguous | stale S | stale S | stale S | — ? | — ? |
| K2_fine_large | ambiguous | 0.37 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |
| A1_coarse_mesh | flawed | 1.84 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | REJECT ✓ | — ? |
| A2_moderate_mesh | ambiguous | 0.64 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |
| B1_small_domain | flawed | 4.97 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | REJECT ✓ |
| B2_moderate_domain | flawed | 1.47 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | — ? |
| C1_large_timestep | ambiguous | 0.27 | mean_drag_coefficient,strouhal_number | credible | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |
| C2_euler_large_timestep | ambiguous | 1.26 | mean_drag_coefficient,strouhal_number | flawed | ACCEPT ~ | INCONCLUSIVE ~· | INCONCLUSIVE ~· | — ? | — ? |
| D1_steady_solver | flawed | 5.61 |  | flawed | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| E1_noslip_side_walls | ambiguous | 0.69 | mean_drag_coefficient | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |
| F1_upwind_convection | flawed | 7.81 |  | flawed | ACCEPT ✗✗ | INCONCLUSIVE · | REJECT ✓ | — ? | — ? |
| G1_premature_averaging | ambiguous | 0.69 | mean_drag_coefficient,strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | REJECT ~ | — ? | — ? |
| H1_dynamic_viscosity | flawed | 2.17 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| I1_force_reference | flawed | 3.64 |  | flawed | ACCEPT ✗✗ | REJECT ✓ | REJECT ✓ | REJECT ✓ | REJECT ✓ |
| J1_coarse_wake | ambiguous | 0.52 | strouhal_number | ambiguous | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ | REJECT ~ |
| G2_average_from_start | ambiguous | 0.66 | strouhal_number | ambiguous | ACCEPT ~ | INCONCLUSIVE ~· | ACCEPT ~ | — ? | — ? |

✓ correct · ✗✗ **false acceptance** · ✗ false rejection · `·` INCONCLUSIVE (safe, undecided) · `~` / `~·` verdict on an ambiguous case (not scored; INCONCLUSIVE expected) · E error · ? missing · S stale (not counted)

| metric | A | B | L-judge | C-rule | C-llm |
|---|---|---|---|---|---|
| cases | 16 | 16 | 16 | 5 | 5 |
| flawed cases (decided) | 7 | 7 | 7 | 4 | 4 |
| credible cases (decided) | 0 | 0 | 0 | 0 | 0 |
| ambiguous cases (decided) | 9 | 9 | 9 | 1 | 1 |
| **false acceptance** (flawed → ACCEPT) | 0.86 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection (flawed → REJECT) | 0.14 | 0.43 | 1.00 | 1.00 | 1.00 |
| missed but safe (flawed → INCONCLUSIVE) | 0.00 | 0.57 | 0.00 | 0.00 | 0.00 |
| correct acceptance (credible → ACCEPT) | — | — | — | — | — |
| false rejection (credible → REJECT) | — | — | — | — | — |
| inconclusive (all decided) | 0.00 | 0.75 | 0.06 | 0.00 | 0.00 |
| ambiguous cases: verdicts | ACC:8 REJ:1 INC:0 | ACC:0 REJ:1 INC:8 | ACC:6 REJ:2 INC:1 | ACC:0 REJ:1 INC:0 | ACC:0 REJ:1 INC:0 |
| ambiguous cases ACCEPTed although best-estimate error > τ | 1 | 0 | 0 | 0 | 0 |
| errors (excluded from rates) | 0 | 0 | 0 | 0 | 0 |
| stale results (excluded) | 1 | 1 | 1 | 0 | 0 |
| missing results | 0 | 0 | 0 | 12 | 12 |
| errors by label | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 | fla:0 cre:0 amb:0 |
| mean extra simulations / case | 0.00 | 0.00 | 0.00 | 0.20 | 0.20 |
| mean extra compute / case (× root) | 0.00 | 0.00 | 0.00 | 0.21 | 0.16 |
| total experiment wall time (h) | 0.00 | 0.00 | 0.00 | 0.11 | 0.19 |
| LLM cost (USD) | 0.00 | 0.00 | 0.49 | 0.00 | 0.05 |
| authority violations | 0 | 0 | 0 | 0 | 0 |
| untraceable numbers in LLM text | 0 | 0 | 24 | 0 | 1 |
| first experiment targets the flaw | — | — | — | 1/1 | 1/1 |

### Secondary view (post-hoc): labels from point estimates, truth uncertainty ignored

_Same verdicts; only the labels change. The pre-registered labels above are primary._

| metric | A | B | L-judge | C-rule | C-llm |
|---|---|---|---|---|---|
| flawed cases | 8 | 8 | 8 | 4 | 4 |
| credible cases | 3 | 3 | 3 | 0 | 0 |
| ambiguous cases | 5 | 5 | 5 | 1 | 1 |
| **false acceptance** | 0.88 | 0.00 | 0.00 | 0.00 | 0.00 |
| detection | 0.12 | 0.38 | 0.88 | 1.00 | 1.00 |
| missed but safe | 0.00 | 0.62 | 0.12 | 0.00 | 0.00 |
| correct acceptance | 1.00 | 0.00 | 1.00 | — | — |
| false rejection | 0.00 | 0.00 | 0.00 | — | — |
