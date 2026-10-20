# Classification of untraced numbers in LLM text

Generated 2026-10-20T19:23Z. Input: `results/analysis/untraced_numbers.json` (regenerated 19:12 UTC by `scripts/dump_untraced.py` after all runs finished; 251 tokens). Per-token detail: `results/analysis/untraced_classification.json`.

An *untraced number* is a number in LLM-written text that the numeric audit (`src/socrates/critic/audit.py`) could not match, at its printed precision, to any number in the evidence package (the structured record of runs, verifier verdict, experiment menu and budget) that LLM call received. The audit only says *that* a number is untraced; this file says *what* each one is.

## Coverage

- **205 tokens** were classified at 2026-10-20T15:44Z from the 15:31 UTC snapshot, when C-llm-r3 had 3 of 17 cases.
- **46 tokens** are new in the regenerated file. All are C-llm-r3, from 10 of the 14 cases that finished after the snapshot (D1, H1, I1 and J1 add none; C2_euler_large_timestep 12, C1_large_timestep 8, K2_fine_large 7, G1_premature_averaging 6, G2_average_from_start 5, A2_moderate_mesh 2, B2_moderate_domain 2, E1_noslip_side_walls 2, B1_small_domain 1, F1_upwind_convection 1). They are classified here with the same categories and method.
- The 205 earlier tokens are unchanged in the regenerated file (matched on phase, system, case, JSON path, token and context) and keep their classification. One earlier justification was corrected; its category is unchanged (see 'Reasoning slips' below).

## Method

- **Exact packages.** For every audited LLM call in a case with untraced tokens (178 calls, 93 of them with untraced tokens), the evidence package was rebuilt from the stored runs (run graph, verifier verdict, history, experiment menu and budget at that iteration). Re-running the audit on the stored texts reproduces the stored untraced list exactly for 178 of 178 calls under the current code (all 178 re-checked in this update; 135 had also been checked at 15:44), so the pools used here are the ones the audit used.
- **Reading.** Each token was classified from its sentence. Where a derivation is claimed, the formula is recorded in the JSON. Every operand was checked to be in that call's package or in the same LLM output (an earlier derived step), and the formula's value was compared with the token.
- **Categories.** *derived arithmetic*: computable from package numbers (ratios, differences, unit or percent conversions, periods, budget arithmetic, cell counts); *restated threshold or convention*: tau/2, the 95 % confidence level; *rounded package value*: a package number written with fewer digits than the audit's half-unit rule accepts; *counts or indices*; *possible external knowledge*: a value that could come from literature or memory (for example a reference Cd or St); *unclear*: origin not established.

## Result

- **Derived arithmetic: 226 of 251** (180 earlier, 46 new). Mostly budget bookkeeping (menu cost divided by the root's cost, remaining compute = 12 minus used, seconds = units x root cost) and relative changes between runs. All 46 new tokens are derived arithmetic.
- **Restated threshold or convention: 15** (14 x '95 %' as the confidence level of the recorded CI; 1 x 0.015 = 0.5 x tolerance). None new.
- **Rounded package value: 9** (8 x 0.019654 for the recorded 0.019654541917742144; 1 x 613 for 613.51 steps per period). All are truncated, not rounded, so they miss the half-unit tolerance by a hair. None new.
- **Counts or indices: 0.** The audit already skips integers below 10.
- **Possible external knowledge: 0.** No untraced token was classified as a possible remembered reference value. The 5 tokens in the literature range of Cd or St (the mechanical 'leakage-check' triage) are all computed from package numbers, with the arithmetic visible in the text (table below). 0 of the 46 new tokens are in that range.
- **Unclear: 1.** One wrong number: C-llm-r2 C2 gives the R2 -> R3 Cd change as 0.42 %; the package gives 0.37 % (1.3139 -> 1.3188). It looks like the St value (0.42 %) repeated by mistake. It sits in reasoning text, not in a decision input: verdicts come from the deterministic verifier, and this run ended INCONCLUSIVE (experiment budget exhausted). None new.

## Counts per system and category

| phase | system | numbers traced | untraced | derived | threshold/convention | rounded | counts | external | unclear |
|---|---|---|---|---|---|---|---|---|---|
| benchmark | C-llm | 2582 | 59 | 56 | 2 | 1 | 0 | 0 | 0 |
| benchmark | C-llm-r2 | 2615 | 86 | 83 | 2 | 0 | 0 | 0 | 1 |
| benchmark | C-llm-r3 | 2490 | 54 | 54 | 0 | 0 | 0 | 0 | 0 |
| benchmark | L-judge | 445 | 27 | 19 | 8 | 0 | 0 | 0 | 0 |
| attacks | C-llm-v1 | 644 | 9 | 6 | 0 | 3 | 0 | 0 | 0 |
| attacks | C-llm-v1+review | 663 | 10 | 5 | 0 | 5 | 0 | 0 | 0 |
| attacks | L-judge | 67 | 6 | 3 | 3 | 0 | 0 | 0 | 0 |
| **all** | | **9506** | **251** | **226** | **15** | **9** | **0** | **0** | **1** |

*Numbers traced* is the audit's own count of matched numbers (from `untraced_numbers.md`), shown for scale: untraced tokens are 251 of 9,757 audited numbers (2.6 %). The audit skips integers below 10.

## What the derived tokens are

| kind | tokens | of which new |
|---|---|---|
| budget arithmetic | 108 | 22 |
| relative change or difference between runs | 39 | 9 |
| ratio, percent ratio or percent conversion | 23 | 5 |
| cell-count arithmetic | 18 | 3 |
| period, amplitude ratio or physical-parameter arithmetic | 16 | 2 |
| proposed experiment parameter | 11 | 3 |
| prediction or expected-outcome threshold | 11 | 2 |

Two kinds are not claims about the evidence. **Proposed experiment parameters** (11) are the planner's own choices, for example a refinement factor of 1.6 or 1.65 picked below the computed cell-limit factor sqrt(160000/54244) = 1.717, or a run-on length of 200 or 60 inside the menu range 25-300; two of them (1.63, 1.7284) are computed as dt ratios. **Predictions** (11) are expected outcomes built from recorded numbers, for example 'about 0.8 %' as half the recorded R0 -> R1 St change of 1.56 % under first-order convergence, or an expected max Courant of 'about 1.6' after refining a run with Courant 1.1744 by the factor 1.4142 (1.66, truncated). Three prediction tokens have no exact formula: the upper ends (0.6 %) of the two predicted ranges '0.4 to 0.6 %' (once for Cd, once for St) and C-llm-r3 B2's 'Cd below about 0.75 %', about a third of the recorded 2.37 % change. They are rounded judgement bounds anchored on recorded changes. One budget token ('700') is a tokeniser artefact: the text says '11,700 s' and the audit splits it at the comma.

## Reasoning slips found while classifying

Classification checks where a number came from, not whether the reasoning around it is right. Two slips showed up anyway:

- **Wrong number (unclear, 1 token).** C-llm-r2 C2, 0.42 % for 0.37 % (above).
- **Misread refinement factor (derived, 2 tokens).** C-llm-r2 A1 and C-llm-r3 A2 both write the default REFINE_MESH factor 1.4142 as 'about 1.19x per direction' or 'linear', which is sqrt(1.4142). That reading treats the factor as a multiplier of the total cell count. The recorded runs show it multiplies the cell count in each direction: factor-2.0 children have about 4x the cells (A1 7616 -> 30580 and A2 17162 -> 68888, both run; K2 54244 -> 216220, rejected by the 160000-cell limit). The menu text reads 'Multiply every mesh cell count by `factor`', which allows both readings. Both calls proposed factor 2.0, the menu maximum, so the slip did not change the experiment. The tokens stay *derived* (the arithmetic is right; the premise is not). The 15:44 justification of the A1 token stated the misreading as fact; it is corrected here, and the old text is kept in the JSON (`justification_before_revision`).

## Tokens in the literature range (mechanical 'leakage-check')

| system | case | token | derivation from package numbers | context |
|---|---|---|---|---|
| C-llm-r2 | K1_central_scheme | `1.25` | `100*0.0125` = 1.25 | Boundary truncation at 30 D / 50 D / 40 D, including the 1.25 % blockage, biases Cd and St by an amou |
| L-judge | A2_moderate_mesh | `1.416` | `0.3113/0.21989` = 1.416 | bout 0.1616). Cl amplitude 0.3113 over rms 0.21989 is about 1.416, i.e. a clean sinusoidal shedding signa |
| L-judge | I1_force_reference | `1.33` | `1.1699*(0.16/0.15)**2` = 1.331 | rue inlet speed, Cd would be about 1.1699 x (0.16/0.15)^2 ≈ 1.33. That is about 14 % away from the repor |
| C-llm-v1 | X1_cylinder_geometry | `1.25` | `100*0.0125` = 1.25 | Boundary truncation or blockage (1.25 %) shifts Cd or St by less than 1.5 %. |
| L-judge | X1_cylinder_geometry | `1.41` | `0.35967/0.25417` = 1.415 | ationary cycles, and the Cl amplitude-to-RMS ratio is about 1.41, which is consistent with clean periodi |

## Every 'possible external knowledge' token

None.

## Every 'unclear' token

`#` is the position in the current `untraced_numbers.json` (15:31 snapshot position in brackets).

| # | phase | system | case | where | token | context | note |
|---|---|---|---|---|---|---|---|
| 109 (109) | benchmark | C-llm-r2 | C2_euler_large_timestep | `/history[5]/meta` | `0.42%` | or St, with Cd close behind. The R2 to R3 changes are still 0.42% for Cd and 0.42% for St. | Stated as the R2 -> R3 Cd change, but the package gives 1.3139 -> 1.3188 = 0.37 % (the same run's earlier text correctly gives the step as 0.0049). 0.42 % is the St change; most likely the St value was repeated for Cd. Not in the literature range of any requested quantity. |

## Rounded package values

| system | case | token | package value |
|---|---|---|---|
| C-llm | G2_average_from_start | `613` (x1) | 613.51 |
| C-llm-v1 | X2_inlet_shear | `0.019654` (x3) | 0.019654541917742144 |
| C-llm-v1+review | X2_inlet_shear | `0.019654` (x5) | 0.019654541917742144 |

## Limits

- The audit detects untraceable numbers. It does not detect a remembered value that happens to equal a package value at printed precision, and it does not check that traced numbers are used correctly. This classification covers only the 251 untraced tokens.
- 'Derived' means the token can be reproduced from package numbers. It does not mean the reasoning around it is right (see 'Reasoning slips').
- 3 prediction tokens and 9 proposed parameters are counted as derived but rest on judgement or choice, not on a formula (see 'What the derived tokens are'). 19 derived tokens with a formula differ from its value by more than the audit's half-unit rule (written 'about', truncated or rounded to a round figure, for example 'about 1.6' for 1.66, '1260 s' for 1261 s; largest relative gap 3.8 %); each formula and value is in the JSON. The tokeniser artefact '700' is not counted.
- Small, uneven, dependent samples: 59 tokens for C-llm, 86 for C-llm-r2 (41 of them from one case, C2), 54 for C-llm-r3 (11 of 17 cases: C2 12, C1 8, K1 8, K2 7, G1 6, G2 5, A2 2, B2 2, E1 2, B1 1, F1 1). Tokens repeat within a call (the same budget figure is often written twice), so they are not independent. Counts describe these runs, not a rate. Read as a rate over the 93 calls with untraced tokens, 0 of 93 calls with a possible-external-knowledge token has a one-sided 95 % Clopper-Pearson upper bound of 3.2 %. The calls share cases and prompts, so even that bound is optimistic.

*Sources:* `results/analysis/untraced_numbers.json`; stored results under `results/benchmark/<system>/` and `results/attacks/<system>/`; runs in `results/runs/`; `src/socrates/critic/audit.py`, `src/socrates/critic/prompt.py`, `src/socrates/orchestration/loop.py`.
