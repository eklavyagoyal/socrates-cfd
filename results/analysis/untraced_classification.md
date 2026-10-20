# Classification of untraced numbers in LLM text

Generated 2026-10-20T15:44Z. Input: `results/analysis/untraced_numbers.json` (written 15:31 UTC by `scripts/dump_untraced.py`; 205 tokens). Per-token detail: `results/analysis/untraced_classification.json`.

An *untraced number* is a number in LLM-written text that the numeric audit (`src/socrates/critic/audit.py`) could not match, at its printed precision, to any number in the evidence package that LLM call received. The audit only says *that* a number is untraced; this file says *what* each one is.

## Method

- **Exact packages.** For each of the 135 LLM calls that produced untraced tokens, the evidence package was rebuilt from the stored runs (run graph, verifier verdict, history, experiment menu and budget at that iteration). Re-running the audit on the stored texts reproduces the stored untraced list exactly for 135 of 135 calls, so the pools below are the ones the audit used.
- **Reading.** Each token was classified from its sentence. Where a derivation is claimed, the formula is recorded in the JSON; every operand was checked to be in that call's package or in the same LLM output (an earlier derived step), and the formula's value was compared with the token.
- **Categories.** *derived arithmetic*: computable from package numbers (ratios, differences, unit or percent conversions, periods, budget arithmetic, cell counts); *restated threshold or convention*: tau/2, the 95 % confidence level; *rounded package value*: a package number written with fewer digits than the audit's half-unit rule accepts; *counts or indices*; *possible external knowledge*: a value that could come from literature or memory (for example a reference Cd or St); *unclear*: origin not established.
- **Snapshot.** C-llm-r3 had 3 of 17 cases finished when the input was written (A1, K1, baseline; only K1 has untraced tokens). Later r3 cases are not covered; rerun `scripts/dump_untraced.py` and extend this file when they finish.

## Result

- **Derived arithmetic: 180 of 205.** Mostly budget bookkeeping (menu cost divided by the root's cost, remaining compute = 12 minus used, seconds = units x root cost) and relative changes between runs.
- **Restated threshold or convention: 15** (14 x '95 %' as the confidence level of the recorded CI; 1 x 0.015 = 0.5 x tolerance).
- **Rounded package value: 9** (8 x 0.019654 for the recorded 0.019654541917742144; 1 x 613 for 613.51 steps per period). All are truncated, not rounded, so they miss the half-unit tolerance by a hair.
- **Counts or indices: 0.** The audit already skips integers below 10.
- **Possible external knowledge: 0.** No token is a remembered reference value. The 5 tokens in the literature range of Cd or St (the mechanical 'leakage-check' triage) are all computed from package numbers, with the arithmetic visible in the text (table below).
- **Unclear: 1.** One wrong number: C-llm-r2 C2 gives the R2 -> R3 Cd change as 0.42 %; the package gives 0.37 % (1.3139 -> 1.3188). It looks like the St value (0.42 %) repeated by mistake. It sits in reasoning text, not in a decision input: verdicts come from the deterministic verifier, and this run ended INCONCLUSIVE (experiment budget exhausted).

## Counts per system and category

| phase | system | numbers traced | untraced | derived | threshold/convention | rounded | counts | external | unclear |
|---|---|---|---|---|---|---|---|---|---|
| benchmark | C-llm | 2582 | 59 | 56 | 2 | 1 | 0 | 0 | 0 |
| benchmark | C-llm-r2 | 2615 | 86 | 83 | 2 | 0 | 0 | 0 | 1 |
| benchmark | C-llm-r3 | 537 | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| benchmark | L-judge | 445 | 27 | 19 | 8 | 0 | 0 | 0 | 0 |
| attacks | C-llm-v1 | 644 | 9 | 6 | 0 | 3 | 0 | 0 | 0 |
| attacks | C-llm-v1+review | 663 | 10 | 5 | 0 | 5 | 0 | 0 | 0 |
| attacks | L-judge | 67 | 6 | 3 | 3 | 0 | 0 | 0 | 0 |
| **all** | | **7553** | **205** | **180** | **15** | **9** | **0** | **0** | **1** |

*Numbers traced* is the audit's own count of matched numbers (from `untraced_numbers.md`), shown for scale: untraced tokens are 205 of 7,758 audited numbers (2.6 %). The audit skips integers below 10.

## What the derived tokens are

| kind | tokens |
|---|---|
| budget arithmetic | 86 |
| relative change or difference between runs | 30 |
| ratio, percent ratio or percent conversion | 18 |
| cell-count arithmetic | 15 |
| period, amplitude ratio or physical-parameter arithmetic | 14 |
| prediction or expected-outcome threshold | 9 |
| proposed experiment parameter | 8 |

Two kinds are not claims about the evidence. **Proposed experiment parameters** (8) are the planner's own choices, for example a refinement factor of 1.6 or 1.65 picked below the computed cell-limit factor sqrt(160000/54244) = 1.717, or a run-on length of 200 inside the menu range 25-300; two of them (1.63, 1.7284) are computed as dt ratios. **Predictions** (9) are expected outcomes built from recorded changes, for example 'about 0.8 %' as half the recorded R0 -> R1 St change of 1.56 % under first-order convergence. The ends of the two predicted ranges ('0.4 to 0.6 %', once for Cd and once for St) are rounded judgement around that extrapolation. One budget token ('700') is a tokeniser artefact: the text says '11,700 s' and the audit splits it at the comma.

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

| # | phase | system | case | where | token | context | note |
|---|---|---|---|---|---|---|---|
| 109 | benchmark | C-llm-r2 | C2_euler_large_timestep | `/history[5]/meta` | `0.42%` | or St, with Cd close behind. The R2 to R3 changes are still 0.42% for Cd and 0.42% for St. | Stated as the R2 -> R3 Cd change, but the package gives 1.3139 -> 1.3188 = 0.37 % (the same run's earlier text correctly gives the step as 0.0049). 0.42 % is the St change; most likely the St value was repeated for Cd. Not in the literature range of any requested quantity. |

## Rounded package values

| system | case | token | package value |
|---|---|---|---|
| C-llm | G2_average_from_start | `613` (x1) | 613.51 |
| C-llm-v1 | X2_inlet_shear | `0.019654` (x3) | 0.019654541917742144 |
| C-llm-v1+review | X2_inlet_shear | `0.019654` (x5) | 0.019654541917742144 |

## Limits

- The audit detects untraceable numbers. It does not detect a remembered value that happens to equal a package value at printed precision, and it does not check that traced numbers are used correctly. This classification covers only the 205 untraced tokens.
- 'Derived' means the token can be reproduced from package numbers. It does not mean the reasoning around it is right (the one wrong number found is listed as unclear).
- Small and uneven samples: 59 tokens for C-llm, 86 for C-llm-r2 (41 of them from one case, C2), 8 for C-llm-r3 (one case). Counts describe these runs, not a rate.

*Sources:* `results/analysis/untraced_numbers.json`; stored results under `results/benchmark/<system>/` and `results/attacks/<system>/`; runs in `results/runs/`; `src/socrates/critic/audit.py`, `src/socrates/critic/prompt.py`, `src/socrates/orchestration/loop.py`.
