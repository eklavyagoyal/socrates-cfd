# Methodology

This document describes *how* evidence is produced and judged. The physical and
numerical set-up is in `docs/design.md`; sources are in `docs/research.md`.
**Software tests check that the code is correct. They say nothing about whether
any simulation is physically credible** (see §8).

## 1. Pipeline

```
ProblemSpec (YAML) ──► CaseConfig (YAML diff) ──► case writer ──► OpenFOAM v2412
      │                                                               │
      │                         raw outputs (logs, function objects, checkMesh)
      ▼                                                               ▼
  provenance (run.json) ◄──── run store (content-addressed) ◄── evidence extractor
                                                                      │
                               deterministic verifier ◄───────────────┘
                                       │ verdict + missing components
                         ┌─────────────┴──────────────┐
                    decisive?                      INCONCLUSIVE
                  (ACCEPT/REJECT) ──► report      planner (LLM critic | rule-based)
                                                       │ one primitive from the menu
                                              validator (ranges, limits, budget)
                                                       │
                                              child run (same pipeline) ──► graph
```

**Solver-specific code** is confined to `case_generation/` (blockMesh and dictionary
writers) and `openfoam/` (runner and parsers).

**Solver-independent code** is everything else: evidence schema, signal analysis,
checks, primitives (which act on `CaseConfig`), critic, loop and reporting.

## 2. Evidence extraction (`evidence/`)

| Evidence | Source | Method |
|---|---|---|
| Mesh validity and statistics | `log.checkMesh` | Regex parse. The verdict comes from "Mesh OK."/"Failed N" because checkMesh always exits 0 |
| Representative cell size h | checkMesh total volume / span / N | h = (A/N)^½, in-plane (Celik) |
| Courant number | solver log | One value per step (the last printed before `Time =`). The first 10 steps (impulsive start) are excluded and reported separately |
| Continuity errors | solver log | Last line per step |
| Pressure-solve convergence | solver log | Final residual of the *last* p solve per step. `solverInfo` records only the first solve |
| Global mass balance | `surfaceFieldValue sum(phi)` on all open patches | max \|Σφ\| / \|φ_inlet\| |
| Cd(t), Cl(t) | `forceCoeffs` `coefficient.dat` | Parsed by header names (v2412 column order is alphabetical). Restart folders merged, last duplicate kept |
| Cycles | Cl up-crossings about the median of the second half of the record | Linear interpolation |
| Transient end | MSER on per-cycle mean Cd, Cl amplitude and period | Truncation index = max of the three, capped at half the cycles |
| Stationary statistics | integer number of cycles after truncation | Time-weighted (trapezoid) means; Cl rms about its mean |
| Frequency | (a) mean period from crossings; (b) Hann-windowed FFT, zero-padded ×8, parabolic peak interpolation | Both reported; their disagreement enters the St uncertainty |
| Statistical uncertainty | per-cycle batch means | max of: t-quantile CI95 of the mean, linear drift over the window, half-window difference. Lag-1 autocorrelation of cycle means is reported because it is ~0.99 during the slow approach to the limit cycle |
| "Reported" value | declared averaging window from the case | What the case author's own post-processing would give: time-weighted mean; St from FFT peak |

Evidence is a pure function of (raw outputs, configuration, spec). It can be
regenerated with `RunStore.reextract` after an extractor change, which overwrites the
evidence file together with its record of any earlier re-extraction. The re-extractions after
the linear-solver parser fix (§7) and the other early extractor changes ran at 07:17–07:24 UTC
on 2026-10-19 and recorded only their time (committed in 4a53ce3 and f27a82d); no current
evidence file shows them. Since R19 the record carries the extractor fingerprint: 15 evidence
files carry `extraction.reextracted = true` (12 root runs at 08:24 UTC, the C1 and C2 roots at
09:08 and the K1 root at 09:33, all on 2026-10-19). Every evidence file in the final run store carries the same
extractor fingerprint (`e5ad2b6ece3659d0`): 207 files, one for each of the 198 completed and 9 failed run records; the
other 7 of the 214 records are 'running' records with no live owner and no evidence file (`results/analysis/run_audit.md`).

## 3. Deterministic checks (`checks/`)

- Every check returns **PASS / FAIL / INCONCLUSIVE** with value, threshold, threshold source, reason, the quantity it concerns, the error-budget component it estimates (if any), its uncertainty estimate, and the runs it used.
- **Missing evidence returns INCONCLUSIVE** (enforced by a test that feeds empty evidence to every check).

Thresholds come from three places (`configs/verification.yaml`):
1. **OpenFOAM defaults or guidance** (checkMesh limits, the Co < 1 PISO guideline);
2. **Literature** (regime boundaries; Roache/Celik safety factors);
3. **The user's tolerance τ**, via an explicit error budget:
   - each component's uncertainty must be ≤ τ/2 to PASS (except the averaging bias, which PASSes up to τ when its reference is reliable and is added linearly, R22/R23);
   - a demonstrated change > τ (by more than twice the statistical noise) FAILs;
   - ACCEPT needs the measured averaging bias plus the root-sum-square of the independent components ≤ τ (R23).

No physics threshold was invented. Where none is defensible, the check reports
the value and returns INCONCLUSIVE.

**Sensitivity (multi-run) analysis** (`checks/sensitivity.py`) estimates the
uncertainty of the *root* run's value from a one-factor refinement sequence:
- **Two levels:** Richardson with the assumed formal order, Fs = 3.
- **Three levels:** Celik observed order (bracketed root solve, R5), monotone/oscillatory classification, extrapolation. Fs = 1.25 if the observed order is within [0.5, 2]× formal, else Fs = 3 with p = min(observed, formal) (R4). Monotone divergence is not extrapolated (R21).
- **Oscillatory or noise-level data:** U = 3 × range.

The verifier assembles refinement families from the experiment graph by following
only edges of the same primitive from the root. Each member is substituted by its
longest RUN_LONGER continuation.

## 4. Experiment primitives (`experiments/primitives.py`)

**Validation.** Action name ∈ menu; parameters numeric and within range; cumulative
limits (refinement ≤ 2× root, ≤ 160k cells, Δt ≥ root/8, domain ≤ 4× root, end time ≤ 600 D/U).

**Derivation.** The child config is derived only through `CaseConfig.with_changes`,
so the diff is recorded exactly.

**Initialisation:**
- **map:** from a periodic parent, mapFields consistent (same domain) or non-consistent (expanded domain); run 80 D/U.
- **fresh:** perturbed start with the parent's duration, used when the parent is not periodic.
- **restart:** RUN_LONGER.

**Courant control in REFINE_MESH.** Δt is kept unless the predicted max Co would
exceed 0.9 while the parent was below 1. Any Δt change is recorded and reported with
the mesh-sensitivity result.

## 5. Planners and authority (`critic/`, `orchestration/loop.py`)

**Deterministic verdict first.** If it is ACCEPT or REJECT, the loop stops. The
planner is consulted only while the verdict is INCONCLUSIVE.

**LLM critic.** A headless LLM command-line client in non-interactive mode (`-p`) with:
- no tools (`--tools ""`), no MCP servers, no settings files, no session persistence, an empty working directory;
- a replacement system prompt stating the authority rules;
- a JSON-schema-constrained output, then pydantic validation (extra keys forbidden; the action is an enum of the four primitives).

**What the critic sees.** It receives only an evidence package:
- the question and spec, *without* reference values in blind mode;
- per-run summaries (configuration, mesh, diagnostics, temporal behaviour, quantities);
- all check results;
- the verifier's per-quantity component status;
- previous decisions;
- the experiment menu with cost estimates per candidate parent;
- the budget.

**Enforcement:**
- An ACCEPT/REJECT proposed while the verifier is INCONCLUSIVE is not executed. It is logged as an authority violation and fed back once.
- An action that fails validation or exceeds the compute budget is rejected and fed back.
- Repeated invalid outputs, or exhausting any budget, stops the loop with INCONCLUSIVE.

**Numeric audit** (`critic/audit.py`, R13 and R31). Every number in the critic's text
is matched against the numbers in its package at its printed precision: half a unit
in its last printed digit, so "1.33" matches values within 0.005. Magnitudes are compared.
- Percent tokens are matched against 100× package values; plain tokens only against package values.
- Percent strings in the package contribute both v and v/100; numbers inside dict keys count as known.
- Plain (non-percent) integers below 10 (counts, run indices, list numbering) are skipped.
- The critic-authored fields of earlier iterations are excluded from the pool, so a number it invented cannot become traced by repetition.

Untraceable numbers are counted and shown in reports. This catches fabricated values
and memorised literature values, unless such a value coincides with a recorded value
at printed precision.

**Rule-based planner (ablation).** The pre-registered order:
averaging/statistics → mesh → time → domain, with default parameters, continuing
refinement families from their finest member. Two rules added after the first results
are applied before this order (a deviation, §6):
- RUN_LONGER on a statistically unreliable refinement-family member (R6, commit 1df98b8);
- RUN_LONGER on the root's longest continuation while `physics_regime` is INCONCLUSIVE (with R24, commit 10f8b80).

The planner without these two rules, exactly as pre-registered, was run afterwards as **C-rule-prereg**
(`scripts/run_rule_prereg.py`; same loop, validator, budgets and decision code; earliest `started` time among its
results 12:53:58 UTC on 2026-10-20, last result 19:11 UTC) for a sensitivity analysis of criterion 5b (§8,
"Observations").

**LLM transport.** Calls are bounded: 300 s timeout, ≤ 3 attempts with exponential
backoff and jitter. Every attempt, error, latency and cost is recorded.

## 6. Evaluation protocol

Pre-registered in `docs/design.md` §19, committed at 07:13 UTC on 2026-10-19 (dd548bc), after the
first root runs had started (07:00–07:02). The decision code was revised after early verdicts were
known. Every benchmark result carries the final decision-code stamp. Attack results carry none and
rest on a replay of the verifier, repeated on the final result set (137 of 137 results reproduce; item 1
below). The details are under "Deviations from pre-registration" below.

**In-house reference** (final construction; details and numbers in `reports/baseline_validation.md`
§3–4). From the baseline's one-factor chains:
- mesh f = 1, √2, 2 (h = 0.457, 0.323, 0.229 D). REFINE_MESH ran the finer levels at a smaller Δt, so each level is shifted to the baseline Δt with the time chain's error model C·Δt^p;
- Δt: the finest three of four levels, 0.005, 0.0025, 0.00125;
- domain: half-height 40, 80, 160 D (×1, ×2, ×4), with the far field of the ×4 member refined (outer-block cell counts ×1.5), because EXPAND_DOMAIN coarsens the far field as the domain grows.

Then:
1. three-level Celik extrapolation per factor, with p = min(observed, formal) and Fs = 3 when the observed order is outside the band (R4/E1);
2. the corrections combined additively;
3. U(T) by root-sum-square of each chain's discretisation uncertainty, the members' statistical uncertainty, and three model-form or conditioning terms (far-field model form, time-overlap shift, time conditioning);
4. compared with the literature at each source's domain extent (report §5).

Result: Cd 1.3155 ± 0.94 %, St 0.1639 ± 0.46 % (`benchmark/labels.json`). The pre-registered
construction (stage 1: Δt = 0.01, 0.005, 0.0025; domain ×1, ×2, ×4 with the standard far field)
was replaced in three further stages (§8, "Observations").

**Labels.** Computed from each case's *reported* values versus the reference:
- **flawed** if max error > τ, a requested quantity is missing, or the set-up solves a different problem;
- **credible** if max error ≤ τ/2;
- **ambiguous** otherwise.

The set-up clause is applied in the narrow reading (`orchestration/truth.label_case`, `benchmark/labels.json`):
only set-up problems detected from the evidence (wrong Re, steady formulation of a periodic flow) and missing
quantities count; every other departure from the problem statement is judged by its error. The attack tables
(`reports/benchmark_tables.md`) also show the literal and set-up readings.

Two views are reported. The first applies the mitigation for the uncertainty of T (R18): a case is
ambiguous when [e − U(T), e + U(T)] straddles τ or τ/2, unless it is flawed for every T in that
interval. The second applies the §19 rule to point estimates.

**Metrics.**
- Detection, false-acceptance, correct-acceptance and false-rejection rates.
- Inconclusive rate.
- Experiments and compute per case.
- LLM cost.
- First-experiment usefulness: whether the first executed primitive equals the manifest's pre-registered "revealing experiment".
- Authority violations.
- Untraceable numbers.

**Sharing runs.** All systems use the same run store. Identical experiment requests
reuse identical runs, so system differences are not run-to-run noise. Each system's compute
figure counts every run it used, including reused ones, so it is a stand-alone cost (§8,
"Observations").

### Deviations from pre-registration

Times are UTC on 2026-10-19 unless stated; commits are from `git log`.

1. **Timeline.**
   - The first root runs were created at 07:00–07:02 (`created` in `results/runs/*/run.json`); A1 finished at 07:06.
   - `docs/design.md` with the protocol was committed at 07:13 (dd548bc).
   - The decision code (the files hashed by `orchestration/systems.py::decision_code_fingerprint`) then changed in ten commits up to 09:06, among them 4a53ce3 (07:18, "fix averaging check reference reliability (found on G1)").
   - Benchmark verdicts were first committed in 0ce5d5e (07:30: `results/bench_batch1.log`; A, B and L-judge on A1, B1, D1 and G1; C-rule on D1, run at 07:25). The first results snapshot, 8c77290 (07:43), holds A, B and L-judge verdicts on seven cases and C-rule and C-llm verdicts on D1 and J1.
   - Six decision-code commits followed the first committed verdicts: 667dd6c (07:35), 8161f5c (07:40), 1df98b8 (08:20), 4639ddb (08:24), 10f8b80 (08:59) and b65bf88 (09:06, the final fingerprint `6406c53bb2011ef5`).
   - `docs/design.md` was edited after dd548bc. Among the changes, §13 was brought in line with the corrected verifier (averaging as a measured bias, the order used below the band, monotone divergence, the FAIL noise rule, bias + RSS for ACCEPT), and the mapped-child duration in §18 was reduced from 100 to 80 D/U (b8057b0, 07:23, before the first committed child run, created at 07:24). The pre-registered text is the dd548bc version (`git show dd548bc:docs/design.md`). The pre-registered text of §19 is unchanged; an annotation marked as not part of it describes how T was actually built (the superseded extrapolation rule, the model-form terms, the refined ×4 member).

   Each benchmark result carries the decision-code stamp (all current ones: `6406c53bb2011ef5`). Attack results carry none and are checked only by `scripts/replay_verdicts.py` (E11). The final replay (`results/analysis/replay.json`, 2026-10-20 19:12 UTC, after the last result was stored) matches all 137 results that have a verifier verdict: 119 benchmark results (B, C-rule, C-rule-prereg, C-llm, C-llm-r2, C-llm-r3 and Bexh, 17 each) and 18 attack results (B-v1, B-v2, C-rule-v1, C-rule-v2, C-llm-v1 and C-llm-v1+review, 3 each). A and L-judge results have no verifier verdict to replay. The revisions were nevertheless made with some early verdicts known.
2. **Rule planner.** §19 fixes the C-rule order statistics/averaging → mesh → time → domain. The RUN_LONGER request for an INCONCLUSIVE `physics_regime` was added after the first results (10f8b80) and is applied before that order; so is the RUN_LONGER request for an unreliable family member (1df98b8). The regime rule cannot discharge the check it targets (§8, "Observations"). The planner without both rules was run afterwards as C-rule-prereg (§5); it gives C-rule's verdict on 16 of 17 cases and differs on F1 (§8, "Observations").
3. **Reference T.** T has four committed versions in `benchmark/labels.json`. All 17 A, B and L-judge results existed before the first version, as did 5 C-rule and 5 C-llm results (7 and 6 by the last version); 2 Bexh results existed by 3cff05d. C-llm-r2, C-rule-prereg and C-llm-r3 started on 2026-10-20 (07:50, 12:53 and 14:11 UTC), after the final version. Metrics and tables (`results/benchmark/metrics.json`, `reports/benchmark_tables.md`) were regenerated with each version.

   | commit | time | Cd | St | basis |
   |---|---|---|---|---|
   | 3d9f43c | 11:03 | 1.3133 ± 0.72 % | 0.1647 ± 1.06 % | stage 1 |
   | 3cff05d | 12:42 | 1.3134 ± 0.71 % | 0.1648 ± 1.29 % | stage 1, root taken from its 250 D/U continuation |
   | 33d5ebf | 13:25 | 1.3046 ± 1.15 % | 0.1638 ± 0.28 % | stage 2 |
   | 021fc5a | 16:43 | 1.3155 ± 0.94 % | 0.1639 ± 0.46 % | stage 4 (final) |

   Two further `results/baseline/truth.json` versions were never committed as T: 4776198 (13:51; Cd 1.3046 ± 1.19 %, St 0.1638 ± 0.48 %; time-overlap model-form and time-conditioning terms added) and the stage-3 estimate 26fee11 (14:26; Cd 1.290 ± 6.3 %). An interim interpretation of the results under the stage-1 T was written in `HANDOFF.md` at 4b2a419 (13:13, §39 "findings so far (not final)"), before the stage-2 and stage-4 versions.
4. **Robustness to the revisions of T.**
   - In the point-estimate view the flawed set is {A1, B1, B2, C2, D1, F1, H1, I1} under every committed version. The credible set changes: {C1, K2, baseline} (3d9f43c, 3cff05d) → {A2, C1, G2, J1} (33d5ebf) → {A2, C1, J1, K2, baseline} (021fc5a).
   - In the view with the truth-uncertainty mitigation, the flawed set {A1, B1, B2, D1, F1, H1, I1} and the empty credible set are the same under every version.
   - False-acceptance and detection rates therefore do not depend on the revisions of T. Correct-acceptance and false-rejection rates in the point-estimate view do.
5. **Decision rule for criterion 5b.** It was fixed after 15 of 17 C-llm results were known (3ee09b1, 2026-10-20 09:17; §8). Outcome under the rule: not met; in the sensitivity analysis against C-rule-prereg: met, by one case (§8, "Decision rule for success criterion 5b", Results).
6. **Post-attack extensions.** The v2 checks `geometry_consistency` and `inlet_uniformity` (`configs/verification_v2.yaml`, line 1: "v2 = pre-registered v1 + post-attack extensions") and the LLM acceptance review used by C-llm-v1+review were committed in 8161f5c (07:40).
   - This was after the attack cases X1–X3 were defined (0ce5d5e, 07:30) and before any attack ran. The attack roots were first created at 08:27, an attempt recorded only in git (22adb05) and replaced under the same run ids at 09:08.
   - They are post-hoc extensions of the pre-registered verifier, not part of the §19 protocol. A detection of X1–X3 by the v2 checks or by the acceptance review is therefore not a blind test.
7. **Post-hoc analyses.** Evaluated separately and not part of the §19 protocol:
   - the J1 variant that treats `-allGeometry`-only checkMesh failures as INCONCLUSIVE (`scripts/posthoc_allgeometry.py`, 83989a7 at 09:14, after J1's verdicts were committed at 07:43): static on all 17 cases (`results/posthoc/B-allgeo/`) and, for J1, adaptive with the rule planner (`--adaptive`, `results/posthoc/C-rule-allgeo/`, 2026-10-20 15:53 UTC); §8, "Observations";
   - the acceptance-rule variants of `scripts/posthoc_acceptance_rule.py` (§9);
   - the rule planner exactly as pre-registered, C-rule-prereg (`scripts/run_rule_prereg.py`, `results/benchmark/C-rule-prereg/`), used only for a sensitivity analysis of criterion 5b; the committed 5b rule names C-rule (§8);
   - tests of the LLM acceptance review on the two real ACCEPTs and on a counterfactual X1 ACCEPT (`scripts/posthoc_review_tests.py`, `results/posthoc/review-on-accepts/`; §8, "Observations").

## 7. Development log of methodological corrections

Each correction was found on real solver output and made as a general rule, not
tuned to a case. Items 1, 2, 3 and 5 are in the first two code commits (e27ac5b and e49066d,
07:00–07:09 UTC on 2026-10-19). Items 4 and 6 were committed in 4a53ce3 (07:18), and the
cross-process run lock in f27a82d (07:25). That was after the first root runs had started
(07:00–07:02) and after `docs/design.md` was committed (07:13), and item 4 was found on G1. No
reported verdict was computed before these corrections (§6, "Deviations from pre-registration").

1. **Oscillation detector.** It required ≥ 3 crossings in the last quarter of the record, which falsely reported "no oscillation" on 40–90 D/U records. Crossings are now counted on the last half.
2. **Linear-solver check.** It read `solverInfo`, which holds only the first p solve of each step, so it would have FAILed every valid run. It now parses the last p solve per step from the log. Evidence was re-extracted.
3. **checkMesh non-orthogonality > 70°** is a warning in OpenFOAM, not a failure. It now maps to INCONCLUSIVE, not FAIL.
4. **Averaging check.** It PASSed G1 by comparing the reported value with a stationary estimate that was itself transient-contaminated (3 cycles, 4 % drift). It now requires the reference estimate to satisfy the statistics criterion; otherwise INCONCLUSIVE.
5. **Scheme-order check.** It returned PASS when the scheme was not recorded. Caught by the missing-evidence test; now INCONCLUSIVE.
6. **Run-store race.** A second process requesting an in-flight run would have deleted it. The run store now tracks the owner PID and waits.

## 8. What the software tests do and do not establish

`tests/` holds 99 unit tests (83 test functions, some parametrised; plain `pytest`) and 8 OpenFOAM
integration tests (5 functions in `tests/test_integration_openfoam.py`, marker `openfoam`). The
integration tests are deselected by default (`addopts = "-m 'not openfoam'"` in `pyproject.toml`),
run with `pytest -m openfoam`, and are skipped when OpenFOAM is not installed. Together the tests cover:
- parsers, on real OpenFOAM v2412 output fixtures, including a diverged run;
- signal analysis, on synthetic signals with known answers and a real history;
- every check's status logic and the missing-evidence rule;
- Richardson/Celik mathematics (observed order recovered exactly for known p);
- the aggregation and error-budget rules;
- case generation and systematic refinement;
- primitive validation, including rejection of invalid or out-of-range actions;
- the critic schema, the blind LLM package and the numeric audit;
- loop authority with a scripted planner: unsupported ACCEPT not executed, invalid actions fed back, budgets, outage classification, result staleness;
- with OpenFOAM: root-run provenance and caching, every primitive, orphan adoption and restart cost.

**They do not establish** that any simulation is physically right. That is the job
of the verification evidence and of the validation against literature in
`reports/baseline_validation.md`.

### Corrections from the adversarial code review (the first benchmark batch was discarded)

A six-lens adversarial review (signal analysis, check logic, experiments/store/loop, LLM authority, CFD methodology,
evaluation validity) was run with independent reviewer agents while the first benchmark batch was in progress. The
findings below were each traced against the code before fixing. **All benchmark results produced before these fixes were
discarded and every system was re-run on the corrected code** (benchmark results now carry a decision-code fingerprint
and are recomputed automatically if that changes; attack results carry none, E11).

| # | Defect | Consequence if unfixed | Fix |
|---|---|---|---|
| R1 | Run ids embed the case name (`B1_small_domain-…`) and were shown to the LLM | "Blind" LLM was told the flaw; its experiment choice (e.g. EXPAND_DOMAIN first on B1) partly read the label | Opaque aliases R0, R1, … in every LLM-facing package (incl. dict keys, history, feedback); regression test on real evidence |
| R2 | OpenFOAM counts `writeInterval` from the restart time | A RUN_LONGER segment never wrote its final state; a chained continuation restarted from a stale time and its new forces went to `coefficient_<t>.dat`, which the parser ignored | writeInterval = segment length; post-run check that the latest time = endTime; ambiguous `coefficient_*.dat` siblings raise |
| R3 | Refinement families ignored children of RUN_LONGER continuations | The rule planner (which refines from the continuation) produced invisible experiments and looped on duplicates | Families built over same-config classes (run + continuations); duplicate experiments rejected with feedback |
| R4 | Observed order below the band fell back to the *higher* formal order | Slow (pre-asymptotic) convergence was extrapolated with a fast order: under-estimated uncertainty, spurious PASS | p = min(observed, formal) with Fs = 3; no positive solution → INCONCLUSIVE |
| R5 | Celik fixed-point iteration could return an unconverged iterate | Wrong p used with Fs = 1.25 | Bracketed root solve; None if no root |
| R6 | Family members' values used without a reliability check; two-level estimate ignored noise | A still-adjusting child could cause FAIL, a noise-level difference a PASS | Every member must pass the statistics criterion (else the planner is pointed to RUN_LONGER on it); noise floors on U and on the FAIL rule |
| R7 | Degenerate families (two runs at one level) divided by zero | Loop crash, case silently dropped | Levels collapsed; degenerate ratio → INCONCLUSIVE; verifier errors recorded as INCONCLUSIVE |
| R8 | `ddt` order parsing assumed order 2 unless the string started with "Euler" | CrankNicolson ψ < 1 or 'bounded Euler' treated as 2nd order | Explicit parser; unknown/non-time-accurate schemes → time component INCONCLUSIVE |
| R9 | RUN_LONGER cost included the parent's copied history | Budget exhausted early; compute metric inflated | Cost = steps computed by the run itself (also on re-extraction) |
| R10 | 1.4142 (LLM) vs √2 (rule) gave different run hashes | Identical simulations run twice | Factors canonicalised (snap to default within 0.1 %, else 3 decimals) |
| R11 | St statistical uncertainty lacked the drift/half-difference terms the design specifies | Drifting frequencies under-reported (~4×) | Period drift and half-window difference added |
| R12 | Diverged (non-finite) histories classified as "oscillating" | physics_regime PASS on a crashed run; invalid JSON | Non-finite/unbounded histories reported as such |
| R13 | Numeric audit expanded every token by 100× with 2 % tolerance | Literature values and years counted as "traced"; leakage invisible | Printed-precision matching, % only against 100×values, critic's own history excluded from the pool |
| R14 | Review/judge outputs not strictly validated (`concur: "false"` → True) | Fail-open on the only LLM path gating ACCEPT | pydantic StrictBool models; invalid → fail safe (INCONCLUSIVE / ERROR) |
| R15 | CLI inherited effort/extra-context environment; no model record | Non-reproducible LLM configuration | Explicit effort, environment filtering, CLI version and a model *fingerprint* (hash) recorded per call |
| R16 | L-judge was given the verifier's verdict and decision rule | The "ungated LLM judge" ablation merely re-labelled System B | Evidence-only package (no check outcomes, verdict or rule) |
| R17 | "Correct decisions" headline rewarded decisiveness; failed jobs vanished from denominators | A system with 5 false acceptances ranked above a safe one | Per-label pre-registered rates with false acceptance first; ERROR persisted and reported separately; every (system, case) required |
| R18 | Labels ignored the uncertainty of the in-house truth | Labels of near-boundary cases (B2 at 1.007 τ) set by noise | Pre-registered mitigation implemented: interval straddling τ or τ/2 → ambiguous, flagged |
| R19 | Provenance hashed only logs; re-extraction unrecorded | QoI source files and child initial fields unverifiable | Hashes of postProcessing and final fields; extractor fingerprint in every evidence file |
| R20 | Orphaned runs (owner died) were deleted and recomputed | Wasted compute when processes restart | Completed orphans are adopted and finalized |

Second-round findings from the same review (latest lens to finish), also fixed before the reported results were computed:

| # | Defect | Fix |
|---|---|---|
| R21 | Monotone *divergence* (differences growing under refinement) passed as convergence: Celik's absolute value hides it | R = ε21/ε32 ≥ 1 → no extrapolation (FAIL if change > τ, else INCONCLUSIVE); same in the truth extrapolation |
| R22 | Averaging bias in (τ/2, τ] was "missing evidence", so the rule planner requested RUN_LONGER forever, although no experiment can change the root's declared-window value | Treated as a measured bias: PASS up to τ (reliable reference required), FAIL above |
| R23 | A known, signed bias was RSS-combined as if it were an independent random uncertainty | Bias adds linearly: ACCEPT needs bias + RSS(other components) ≤ τ |
| R24 | A decaying (or still growing) oscillation passed the regime check as "sustained shedding" | Amplitude drift > τ across the window → INCONCLUSIVE (→ RUN_LONGER) |
| R25 | MSER hits its 50 % cap on every run here (exponential approach to the limit cycle), so "transient end detected" overstated what was detected | Reported as "stationary-window start" with an explicit cap flag; stationarity is judged by the drift/half-difference measures |

The fixes were themselves re-reviewed by a second adversarial pass. That fix-verification pass found the following,
also fixed before the reported results were computed (the benchmark was relaunched from scratch afterwards; the stamp
of every benchmark result records the decision-code fingerprint and the git commit it was produced with):

| # | Defect in a fix | Fix |
|---|---|---|
| R26 | The FAIL test sat after the "no observed order" and "divergent" branches, so a change ≫ τ on a non-monotone or divergent sequence came back INCONCLUSIVE | FAIL (change − 2·noise > τ) is tested first, for every sequence shape |
| R27 | An observed-order root above the search bracket returned "no order", so *very fast* convergence was INCONCLUSIVE | Above-bracket roots return an ∞ sentinel and take the above-band rule (formal order, Fs = 3) |
| R28 | The member-reliability gate used a different threshold from the noise floor in U, so a member could be "reliable" for one and not the other | One rule: a member is unreliable when Fs₂·u > frac·τ; unreliable members are listed for RUN_LONGER |
| R29 | A RUN_LONGER restart computed `writeInterval` from the parent's nominal end time, not the time actually restarted from | The actual restart time is persisted (`restart_from_time_s`) and used; the final-state check allows dt/2 and requires progress past the start; a final-state failure is not cached as a solver failure |
| R30 | Orphan adoption accepted a run whose only solver log was copied history, and finalized a continuation that never ran | Adoption requires a log produced by this run (not in the source run), the right `Case:` header and a written final state |
| R31 | Numeric audit: "1.50 %" in the package did not match "1.50 %" in critic text; numbers inside dict keys were unknown; excluding the whole history block also hid system-written outcomes | Percent strings contribute v and v/100; key digits are known; only critic-authored history fields are excluded |
| R32 | A loop that stopped because every LLM call failed was recorded as a verification INCONCLUSIVE, and resume kept it | Planner failures are counted separately from invalid actions; "all events were planner failures" is an infrastructure error, recomputed on resume and excluded from rate denominators |
| R33 | The decision-code fingerprint omitted case generation, primitives, the run store, parsers and the problem spec, and hashed base names only | Widened to every verdict-relevant file, hashed with relative paths; results also stamped with the benchmark commit and a dirty flag |
| R34 | An exception while writing a case report discarded the finished result | Report failures are written to `<case>.report_error.txt`; the result is kept |
| R35 | The analysis took the root run from System B only (crash when B errored) and counted errors in rate denominators | Root run taken from any system's result (must agree); errors excluded from denominators and reported per label |

### Review of the evaluation pipeline (truth, labels, metrics, reports)

E1–E10 were fixed before any number was reported (2b63972, 10:14 UTC on 2026-10-19); E11 was added on 2026-10-20
(49b583f), after the first metrics (3d9f43c, 11:03 UTC on 2026-10-19).

A further three-lens adversarial review (truth/labels mathematics, metrics, report assembly) targeted the scripts
that turn results into the reported numbers. None of these files is part of the decision-code fingerprint, so
fixing them did not invalidate any verdict.

| # | Defect | Fix |
|---|---|---|
| E1 | The truth extrapolation still used the formal order when the observed order was *below* the band (the R4 fix had been applied to the verifier only): slow convergence extrapolated with a fast order, truth biased toward the finest level with an uncertainty that may not cover it | Same rule as the verifier: p = min(observed, formal) with Fs = 3; the time-overlap correction uses the order actually used |
| E2 | Truth uncertainty ignored the statistical uncertainty of the chain members | Each member's statistical uncertainty is carried through the extrapolation weights into the RSS; per-member reliability table in the baseline report |
| E3 | A result computed before its root's evidence was re-extracted (K1) counted as current; the analysis never compared decision-code stamps | Results are stamped with the evidence digest of every run they used; stale results (other decision code, other root, evidence changed) are recomputed on resume and listed but **not counted** by the analysis |
| E4 | One disagreeing root among the systems' result files dropped the case from *every* system | The root of each case is the content-addressed run of its manifest definition, independent of results |
| E5 | An LLM outage preceded by one invalid proposal was scored as a verification INCONCLUSIVE | Classified by the cause of the stop: 'repeated planner failures' is always an infrastructure error (`orchestration/evaluation.py`, superseding `systems.is_infrastructure_error`) |
| E6 | Verdicts on *ambiguous* cases were painted as "correct" (System A's blanket ACCEPT looked green) | Neutral, unscored outcome classes for ambiguous cases; ACCEPTs of ambiguous cases whose best-estimate error exceeds τ are counted separately |
| E7 | ERROR results entered the experiment-count, compute and flaw-targeting tallies | Excluded |
| E8 | 'label unstable' was reported for cases that are flawed under every truth in the interval | Only reported when the interval can change the label |
| E9 | The baseline's literature check used the narrow band, not the pre-registered band widened by τ | Both shown; criterion 2 uses the widened band |
| E10 | Report assembly: L-judge excerpt showed a trailing caveat; outages shown as INCONCLUSIVE in attack tables; Bexh case reports omitted the experiments; git dirty flag false when git was unavailable | Fixed |
| E11 | Attack results carry no decision-code stamp, and a long-running process keeps the modules it loaded at start, so a file written after the last decision-code commit is not proof it used that code | `scripts/replay_verdicts.py` re-runs the current verifier on the stored run graph of every result (benchmark and attacks) and requires the verdict, failed checks, every component status and every component uncertainty to match (relative 1e-9) |

The review also showed that the evidence-only LLM judge (L-judge) is a strong baseline on the benchmark cases, whose
flaws are visible in the configuration. It was therefore added to the attack phase, whose cases are built to look
clean in their configuration.

### Decision rule for success criterion 5b (fixed 2026-10-20, commit 3ee09b1 at 09:17 UTC)

design.md §19 requires the LLM planner to "beat the pre-registered rule-based planner on accuracy or cost" but names
no cost metric, margin or test. A review found this gap after 15 of 17 C-llm results were known, so the rule below is
**not blind** to those 15; it is fixed before the last two (K1, K2) and before any repeat run is analysed.

- **Pairing.** C-llm (first run) against C-rule, over the cases where both have a current, non-error result.
  Repeats (C-llm-r2, …) measure variance only and do not enter this comparison.
- **Accuracy.** The LLM planner beats the rule planner if, in either label view, it makes more correct decisions
  (flawed → REJECT, credible → ACCEPT) on the paired cases, and in neither view more false acceptances or false
  rejections.
- **Cost.** The primary metric is experiment cell-steps relative to the root (the compute the planner requested).
  Wall time is excluded: CPU oversubscription and queueing contaminate it (two runs with identical cell-steps took
  1442 s and 4804 s). LLM cost in USD is reported alongside and counts against the LLM. The LLM planner beats on cost
  only if (i) its total paired relative compute is lower **and** (ii) an exact two-sided sign test over the paired
  cases whose costs differ by more than 5 % gives p < 0.05 in its favour.
- **Otherwise** the final report states, as §19 requires, that the LLM planner adds no measurable value on this
  benchmark. Other differences (first-experiment targeting, savings on single cases) are reported descriptively and
  do not meet the criterion.

**Results** (final result set, 2026-10-20 19:12 UTC; `reports/benchmark_tables.md`, "Criterion 5b decision rule"
and its sensitivity analysis; `results/benchmark/metrics.json`, `criterion_5b`). These are outcomes of the rule
above; the rule itself is unchanged.
- **Committed rule (primary answer): not met.** Paired cases: 17 of 17. Accuracy is tied: 7 correct decisions each
  in both label views, no false acceptance by either, and one false rejection each on point estimates (J1, by the
  static `mesh_quality` check). Cost: total paired compute 83.06× root for C-llm against 81.29× for C-rule; costs
  differ by more than 5 % in 10 cases, C-llm cheaper in 2 of them, sign test p = 0.109. LLM cost on the paired
  cases USD 5.13. So the LLM planner adds no measurable value on this benchmark.
- **Sensitivity analysis against C-rule-prereg (not the committed rule): met, on accuracy, by one case.** Against
  the rule planner exactly as pre-registered, C-llm makes 7 correct decisions to C-rule-prereg's 6 in both views,
  with no more false acceptances or false rejections. The whole difference is F1, which C-rule-prereg leaves
  INCONCLUSIVE because its mesh and time studies never get a statistically reliable root member (§8,
  "Observations"). Cost is not met there either: 83.06× against 90.45× root (C-llm lower), but C-llm is cheaper in
  only 4 of the 11 cases that differ by more than 5 %, p = 0.549.
- **How to read the two.** The committed rule is the answer to 5b. The sensitivity "win" does not show an ability of
  the LLM: it exposes a gap in the pre-registered rule planner that one deterministic rule closes. The post-hoc
  unreliable-member rule (1df98b8) requests exactly the continuation that F1's root needs; in C-rule's own F1 run the
  regime rule's continuations supplied it first. C-rule with only the unreliable-member rule was not run: that this
  one rule closes the gap is inferred from what the rule requests, and what was observed is that C-rule, with both
  post-hoc rules, REJECTs F1.
- **Not part of either comparison.** The repeats' two case-level ACCEPTs (C-llm-r2 on K2, C-llm-r3 on the
  baseline; §8, "Observations"), both correct on point estimates, come from the planner's choice of parameters and
  levels. Neither reproduces in the other LLM runs, and the rule excludes repeats; they are reported descriptively.

### Observations logged during the evaluation (not changed in the pre-registered verifier)

- **J1 (coarse wake):** `checkMesh -allGeometry` reports "Cells with small determinant (< 0.001): 48", which OpenFOAM counts as a failed check, so `mesh_quality` FAILs and every system REJECTs J1. Its reported Cd/St are within ~1 % of the baseline, so if the measured label is *credible*, this is a false rejection caused by an extended-geometry quality heuristic rather than by an accuracy problem. A post-hoc variant that treats `-allGeometry`-only failures as INCONCLUSIVE (to be discharged by mesh refinement) is evaluated separately and reported as a protocol deviation (§6, "Deviations from pre-registration", item 7).
  `scripts/locate_flagged_cells.py` places all 48 flagged cells at x ≈ 47 D, next to the outlet
  (`results/posthoc/flagged_cells.txt`); the enlarged-domain meshes of the baseline study fail the same check with
  cells 57–155 D from the cylinder. The flag reacts to stretched far-field cells, not to the wake region that sets
  the forces.
  - Static, on all 17 cases (`results/posthoc/B-allgeo/`), the variant changes only J1: REJECT → INCONCLUSIVE.
  - Adaptive, with the rule planner (`results/posthoc/C-rule-allgeo/J1_coarse_wake.json`), J1 ends INCONCLUSIVE
    after 5 experiments (REFINE_MESH √2 twice, REDUCE_TIME_STEP, EXPAND_DOMAIN ×2 twice; 6.54× root). The concern is
    not discharged, because the St mesh component is 2.17 % (> τ/2; demonstrated change 1.39 %), and both domain
    components are above τ/2 (Cd 1.64 %, St 2.28 %). The variant removes the false rejection of the point-estimate
    view but does not reach the correct ACCEPT.
- **The in-house reference needed three stages beyond the pre-registered study** (details and numbers:
  `reports/baseline_validation.md` §3–4). The committed versions of T, and which results were known when each was
  made, are listed in §6 ("Deviations from pre-registration").
  - Stage 2: the domain levels had not reached a limit cycle in 80 D/U (the wake had not crossed the enlarged
    domain); they were continued to 180/280 D/U, and dt/8 was added because St's time behaviour was unresolved.
  - Stage 3: a ×3 domain level showed the four-level domain chain is not asymptotic (the slope in 1/half-height
    grew with the domain).
  - Stage 4: EXPAND_DOMAIN keeps the per-cell growth rate, so the far field coarsens as the domain grows (last wake
    cell ≈ 1 D at ×1, 3.9 D at ×4). Refining the ×4 far field (outer-block counts ×1.5) raised Cd by 0.16 %; the
    same refinement on the ×1 domain changed Cd by 0.03 %, so most of the change is far-field resolution beyond the
    baseline's extent. The refined ×4 member replaced the standard one; the gap between the two chains is carried in
    U(T) as a far-field model-form term (0.82 % of Cd), so the replacement is consistency, not confirmation.
  - The finer mesh levels ran at a smaller dt (REFINE_MESH holds the Courant number). Each is shifted to the
    baseline dt with the time chain's model C·dt^p; an accidental pair of f = 2 runs showed weaker dt sensitivity than
    the model, so the full shift is also carried as a model-form term.
  - The same far-field coarsening inflates the verifier's own domain component: 2.62 % of Cd on the baseline's
    full-study graph (baseline + 11 study runs), so the verifier cannot ACCEPT the baseline's drag on that graph.
    This is a property of the pre-registered EXPAND_DOMAIN primitive and was not changed. One benchmark graph with a
    shorter chain of 80 D/U levels (its ×2 level unsettled) did ACCEPT the baseline (next item).
- **Two case-level ACCEPTs, both in LLM repeats, both resting on the levels the planner chose (the domain chain's
  observed order, and on K2 also a third mesh level).**
  - Of the 119 benchmark results and 18 attack results that carry a verifier verdict, exactly two are case-level
    ACCEPTs, and both come from repeats of the LLM planner. C-llm-r2 on K2: Cd combined U 1.54 % (mesh 0.34 %, time 0.79 %, domain
    1.27 %), St 1.69 % (mesh 0.99 %, time 0.27 %, domain 1.34 %); errors against T +0.94 % and −0.07 %. C-llm-r3 on
    the baseline: Cd 1.87 % (mesh 0.86 %, time 1.10 %, domain 1.23 %), St 1.59 % (mesh 1.33 %, time 0.31 %, domain
    0.79 %); errors +1.20 % and −0.31 %. No ACCEPT by C-llm (first run), C-rule, C-rule-prereg, Bexh or B. There is
    no case-level false acceptance by any verifier-based result on the benchmark or the attacks (System A, OpenFOAM
    diagnostics only, ACCEPTs 6 of the 7 flawed benchmark cases with the mitigation and 7 of 8 on point estimates). At quantity level there is one: X1's St under
    C-rule-v1 (error −3.60 % against U 1.62 %), inside an INCONCLUSIVE case verdict.
  - Both are correct on point estimates: each error lies within the stated U. Both cases are ambiguous with the
    truth-uncertainty mitigation, so there the ACCEPTs are not scored. 2 of 2 ACCEPTs correct on point estimates
    gives a one-sided 95 % Clopper–Pearson lower bound of 0.224 on the share of correct ACCEPTs.
  - What decides them is mainly the drag domain component, through its observed order. The order acts in two ways:
    it sets how far the extrapolated limit lies from the root (a higher order gives a smaller estimated error), and
    outside the band it switches the safety factor from 1.25 to 3. On the baseline only the first acts; on K2 both do.
    The observed order says how fast the value approaches its limit as the domain grows, estimated from the root
    and the two largest domains; inside [0.5, 2] × the formal order 1 the safety factor is Fs = 1.25, outside it
    p = min(observed, formal) with Fs = 3 (§3). The order of the same case differs between runs with the domain
    levels chosen and with how far those levels had settled:
    - K2 (root half-height 60 D): C-rule (= C-rule-prereg) ×1, ×2, ×4 gives 1.51, U 1.02 %, PASS; C-rule was
      blocked by its mesh study instead (its second REFINE_MESH was refused by the 160,000-cell limit, so St kept a
      two-level estimate, U 2.17 %). C-llm ×1, ×2, ×4 gives 2.79, outside the band, so Fs = 3 and U 2.38 %. C-llm-r2
      ×1, ×2, ×3 gives 1.06, U 1.27 %, PASS, and it took a third mesh level from the root with factor 1.65, inside
      the cell limit: ACCEPT. C-llm-r3 ×1, ×1.5, ×2, ×3 gives 7.66, so Fs = 3 and U 1.87 %; its mesh study also
      stayed two-level (REFINE_MESH ×2 refused by the cell limit, then a single ×1.6), so its St mesh component was
      2.19 %. The two PASSes use the
      ×2 level's 80 D/U run (`K2_fine_large.D2x-bc527461f36d`, Cd 1.32076); C-llm and C-llm-r3 use its continuation
      to 180 D/U (`K2_fine_large.long180-dda8a9c17278`, Cd 1.31963).
    - Baseline: 0.82–0.94 in the other three-level planner graphs (C-rule 0.86, C-llm 0.94, C-llm-r2 0.82; all
      inside the band, so Fs = 1.25; U 1.74–1.88 %)
      against 1.55 in C-llm-r3's chain ×1, ×1.5, ×2 (U 1.23 %, PASS). C-llm-r2's graph holds the same three runs
      plus a ×3 level. With the settled value of the ×2 level, C-llm-r3's estimate gives order 0.85 and 1.97 %
      (`reports/baseline_validation.md` §6).
  - So acceptance is fragile to the planner's choices. The order estimate moves U across τ/2: on the baseline
    through the extrapolation alone (Fs = 1.25 in every chain), on K2 also through the switch of Fs between 1.25
    and 3. Both ACCEPTs rest on their case's unsettled 80 D/U ×2 run. With the settled ×2 value the baseline estimate
    gives 1.97 %; on K2, with the 180 D/U continuation's Cd (1.31963 for 1.32076), C-llm-r2's own chain gives order
    2.51, Fs = 3, U 2.61 % (computed with `checks/sensitivity.assess_sequence` on the stored values and noise). In
    both cases the result is INCONCLUSIVE. Avoiding the largest levels is not the mechanism in general: on K2 the
    accepting chain reaches ×3 and C-rule's ×4 chain also passes its domain component.
  - Run-to-run variance over the three complete LLM runs (C-llm, C-llm-r2, C-llm-r3; `reports/benchmark_tables.md`,
    "LLM run-to-run variance"): the verdict is identical in 15 of 17 cases, and the two disagreements are exactly
    these ACCEPTs, each reached in 1 of 3 runs; the experiment sequence is identical in 6 of 17. Every case flawed in
    the mitigated view (A1, B1, B2, D1, F1, H1, I1) is REJECTed in all three runs; C2, flawed on point estimates
    only, is INCONCLUSIVE in all three. Correct acceptance on the 5 point-estimate-credible cases: C-llm 0/5
    (one-sided 95 % upper bound 0.451), C-llm-r2 and C-llm-r3 1/5 each (0.657); C-rule, C-rule-prereg and Bexh 0/5.
    The repeats reuse simulations from the shared store, so they measure the variance of the planner's choices, not
    of the simulations.
- **REFINE_MESH keeps Δt when the parent's max Courant number exceeds 1** (§4; run.json note "parent max Co …
  already exceeds 1.0; time step kept so that only the mesh changes"). This is a design defect of the primitive.
  - On C1 (root max Co 3.42) and C2 (2.92), every refinement of the root diverged: ×1.3, ×√2 and ×2 on each root.
    All ended with returncode −8 (floating-point exception) and a recorded max Co between 9.2 × 10¹⁰² and
    9.2 × 10¹⁰⁴. The last of them, C2's ×1.3 (`C2_euler_large_timestep.m1.3-53f0c75d4a04`, launched by C-llm-r2
    at 07:52 on 2026-10-20), was recorded as failed at 12:29 UTC.
  - Refinements of a REDUCE_TIME_STEP child completed, but they are not members of the root's mesh family (§3).
  - A refinement of either root keeps its Δt. On both roots even the smallest allowed factor (×1.3; `primitives.py`
    range 1.3–2.0) diverged, and larger factors raise the Courant number further. The mesh component of the C1 and
    C2 roots therefore cannot be measured with the current primitives, and no adaptive system can ACCEPT C1
    (credible in the point-estimate view).
- **A diverged refinement is reported as missing evidence.** `RunGraph.factor_family` drops failed children. Every
  adaptive result for C1 and C2 (C-rule, C-rule-prereg, C-llm, C-llm-r2, C-llm-r3 and Bexh) contains at least one
  diverged refinement of the root, and all of them give the mesh reason
  "no REFINE_MESH experiment has been run; mesh error of … is unknown", although refinements ran and diverged.
  The reason text is wrong, and the divergence does not appear in the verdict.
- **Bexh refines diverged parents.** Its fixed protocol (REFINE_MESH √2 twice) launched the second refinement from
  the diverged √2 run on both cases (`C1_large_timestep.m2-a3ed547121c5`, `C2_euler_large_timestep.m2-4c431502ff02`).
  Both started fresh because the parent had no periodic state, ran for 46 and 13 minutes, and diverged
  (returncode −8).
- **`physics_regime` is evaluated on the root only, but the rule planner runs the root longer for it.**
  - `verify` evaluates the static checks on the root's evidence and re-evaluates only averaging and statistics on
    the longest continuation, so no RUN_LONGER can change `physics_regime`. Since 10f8b80, the rule planner
    requests RUN_LONGER whenever that check is INCONCLUSIVE (§5).
  - In the C-rule results 13 continuations were requested with the regime reason, with 3.98 × 10⁹ cell-steps,
    16 % of C-rule's experiment cell-steps over all 17 cases: F1 4 (2.7× root), G1 4 (10.0× root) and G2 5
    (8.3× root).
  - One of them (G1's first) would have been requested anyway by the pre-registered averaging/statistics step,
    which asks for the same RUN_LONGER on the same parent and was discharged by it. The rule's own cost is 12
    continuations, 3.67 × 10⁹ cell-steps (15 %): F1 4, G1 3 (7.5× root), G2 5.
  - `physics_regime` stayed INCONCLUSIVE in all three final verdicts. On F1 and G2 the next request was refused
    by the end-time limit (600 D/U), and on G1 by the compute budget. F1 then reached REJECT through REFINE_MESH;
    G1 and G2 ended INCONCLUSIVE on their compute and experiment budgets.
  - Because `physics_regime` is a gate check (no error-budget component) without a discharge path in `aggregate`,
    a root on which it is INCONCLUSIVE can never be ACCEPTed, whatever experiments run.
- **The rule planner as pre-registered (C-rule-prereg, `scripts/run_rule_prereg.py`).** It runs the §19 order
  only, without the unreliable-member and regime RUN_LONGER rules (§5; §6, item 2), with the same loop, validator,
  budgets and decision code (`6406c53bb2011ef5`); simulations already in the store are reused.
  - On 14 of 17 cases it builds exactly C-rule's run graph. It differs on F1, G1 and G2, the three cases where the
    regime rule had fired first in C-rule. Verdicts are identical on 16 of 17 cases; G1 and G2 end INCONCLUSIVE in
    both.
  - **F1 differs.** C-rule REJECTs it (St mesh change 6.74 % > τ). C-rule-prereg ends INCONCLUSIVE with the compute
    budget exhausted, after 5 experiments and 11.40× root: REFINE_MESH √2 twice (a third refused by the 2×
    refinement limit), REDUCE_TIME_STEP three times (a fourth refused by the Δt limit), then an EXPAND_DOMAIN
    refused for budget.
  - The obstacle is the root itself. It has 10 stationary cycles and statistical uncertainties of 1.07 % (Cd) and
    1.47 % (St). That is within τ/2, so the statistics component PASSes and the pre-registered order (statistics
    first) never asks for RUN_LONGER. It is above the member-reliability limit (Fs₂ · u ≤ τ/2 with Fs₂ = 3; R6,
    R28), so every mesh and time study, which contains the root as a member, stays INCONCLUSIVE ("family member(s)
    not statistically reliable … run them longer first").
  - The verifier does not evaluate a family with an unreliable member at all, so even its FAIL test is skipped.
    C-rule-prereg's two refinements changed St by 11.8 % (root 0.1258 → ×2 0.1426, relative to the ×2 value;
    computed for this document from the runs' evidence), more than τ after the 2 × noise deduction (2 × 1.47 %).
  - What this shows about the post-hoc rules. The unreliable-member rule (1df98b8) requests RUN_LONGER on a member
    the verifier lists as unreliable, which is the step F1's root needs; the LLM planner took that step on its own
    (REFINE_MESH ×2, then RUN_LONGER on the root: St change 11.45 %, REJECT). In C-rule's own F1 run the regime
    rule fired first, and its four continuations made the root reliable before the first refinement. So the
    pre-registered order has a gap that one deterministic RUN_LONGER rule closes; that the unreliable-member rule
    alone would close it is inferred from what it requests, since C-rule with only that rule was not run. The regime
    rule's cost is in the previous item.
  - Effect on criterion 5b: F1 is the whole accuracy difference in the sensitivity analysis (§8, "Decision rule for
    success criterion 5b", Results).
- **Tests of the LLM acceptance review (post hoc, `scripts/posthoc_review_tests.py`).** The review (C-llm-v1+review)
  is veto-only and is called only on a deterministic ACCEPT. None occurred in the attacks or in the first C-llm run,
  so it was never exercised there (`results/attacks/review-on-benchmark/`: "no ACCEPT to review" on all 17 cases).
  - Method. The script rebuilds each review's evidence package exactly as the loop builds it and stores it with its
    sha256 (`results/posthoc/review-on-accepts/*.package.txt`, `*.package_meta.json`). The stored review outputs
    (2026-10-20 14:14–14:16 UTC) were produced by the same code run inline before the script existed. LLM outputs
    are not deterministic, so a new run with `--call` can differ.
  - On the two real ACCEPTs (C-llm-r2 on K2, C-llm-r3 on the baseline) the review concurs: no false veto.
  - Counterfactual X1 ACCEPT: the verdict the combined-only rule V1 (`scripts/posthoc_acceptance_rule.py`) would
    give, made consistent by setting the checks that are INCONCLUSIVE only because U > τ/2 to PASS. On the
    C-llm-v1 graph the review concurs, which would be a false acceptance of a +5.98 % drag error. Its package
    contains the measured cylinder extent, 0.0105 m against D = 0.01 m, 12 times; the review wrote "D is 0.01 m"
    and "No recorded field shows a mismatch with the question that would invalidate the result". On the C-rule-v1
    graph it vetoes, for numerical reasons (domain not converged, observed order 0.85, domain U 1.92 % above τ/2;
    the enlarged-domain runs fail checkMesh; few stationary cycles), not because of the geometry: it too wrote "No
    spec mismatch in geometry, inlet or boundary-condition types is visible", although its package contains the
    measured extent 0.0105 m 10 times.
  - So one of two counterfactual false ACCEPTs is blocked, for the wrong reason, and neither review noticed the
    geometry. L-judge, given the same field,
    did REJECT X1, citing the 0.0105 m patch extent: an LLM given this field may or may not notice the flaw. The
    review is not a substitute for the v2 consistency checks (`geometry_consistency`, `inlet_uniformity`), which
    REJECT X1 and X2 under every acceptance-rule variant and change none of the 17 benchmark verdicts
    (`results/attacks/B-v2-on-benchmark/`).
- **Calibration of the verifier's uncertainty (not a pre-registered metric; `scripts/analyze_benchmark.py`).** For
  every result whose mesh, time and domain components all carry an estimate, each quantity's U (averaging bias +
  RSS of the components, §3) is compared with its error against T.
  - Counting: each distinct run graph once. A result whose graph equals an earlier row's (for example the 14
    C-rule-prereg graphs equal to C-rule's, or a repeat that rebuilt a graph) is not repeated; the repeats' new
    graphs are included (`reports/benchmark_tables.md`, "Calibration").
  - Benchmark: U covers the error in 64 of 66 quantity rows (one-sided 95 % lower bound 0.908; rows share cases and
    runs, so they are not independent). The two misses are Bexh H1 St (6.05 % against U 3.01 %; H1 solves
    Re = 83.3) and Bexh I1 Cd (11.05 % against 4.21 %; wrong force normalisation). These are set-up errors, which U
    does not estimate by construction: U covers averaging, statistics, mesh, time and domain for the problem as
    set up. Both cases are REJECTed by static checks.
  - Attacks: 4 of 10 rows covered; the six misses are all X1 (a cylinder 5 % too large), a set-up departure of the
    same kind.
  - U and T come from the same Richardson machinery and partly from the same runs, so coverage is consistency, not
    independent confirmation.
- **Per-iteration check outputs are not stored.** A result keeps the final verdict with all its checks. For each
  iteration it keeps only the verdict, the missing components, the planner's output and the outcome (`history`), so
  the reason an intermediate verdict was INCONCLUSIVE is not on record. Example: after C-llm's first experiment on F1
  (REFINE_MESH ×2), the mesh check did not decide. The only record of why (the root was not statistically
  reliable) is the critic's own text in iteration 2. `scripts/replay_verdicts.py` replays only the final verdict.
- **Compute figures are stand-alone costs.** Each result counts the cell-steps and wall time of every experiment
  run it used, including runs that another system had already computed in the shared content-addressed store
  (§6).
  - In the final benchmark results, 74 of 156 distinct experiment runs appear in more than one system's result.
    For example, `B2_moderate_domain.D2x-44c88f366919` is counted by Bexh, C-llm, C-llm-r2, C-llm-r3, C-rule and
    C-rule-prereg. Summing compute across systems double counts.
  - Wall time is also contaminated by CPU oversubscription and queueing. The baseline and I1 roots (30 580 cells ×
    15 000 steps each) took 1442 s and 4804 s. C-llm's E1 result reports 10 759 s of experiment wall time inside a
    7 421 s loop.
  - Cell-steps relative to the root are therefore the primary cost metric (criterion 5b, above).
- **Abandoned attempts are not kept in the run store.** The store keeps one record per run id.
  - When `RunStore.get_or_run` finds a 'running' record whose owner process is gone, it adopts the run if its
    solver output is complete (R20, R30). Otherwise it deletes the directory and runs the configuration again under
    the same run id. A record that failed with failure kind `final_state` is also deleted and re-run.
  - The current record therefore shows only the last attempt. The creation time, owner, launcher, partial output
    and compute of earlier attempts are not in the store. Their only record is the git history of the `results/`
    snapshots, which holds an attempt only if it was committed before it was replaced.
  - Example: the current record of `A1_coarse_mesh.m0.707-a67b9e3443d4` was created at 08:25 on 2026-10-19. Git
    holds two earlier attempts under the same id, created at 07:25 (0ce5d5e) and 07:35 (6133c4a), both last
    committed as 'running'.
  - `scripts/audit_runs.py` lists the earlier attempts it can recover from git (§9). An attempt that started and
    was removed between two commits leaves no trace, so compute taken from git is a lower bound.

## 9. Reproducibility and integrity checks

Case A1 was re-run from scratch inside the container (`docker/Dockerfile`, image built from the pinned
`openfoam2412=2412.260127-1` package and `requirements.lock`) with an empty run store, and compared with the host run:
same content-addressed run id (`A1_coarse_mesh-8db269c22d05`), and mean Cd, St and Cl rms identical to all printed
digits (relative difference 0.0). Files: `results/reproducibility/`. Single-core OpenFOAM runs with identical inputs
and binaries are bitwise deterministic here; parallel (decomposed) runs would not be expected to be.

**Integrity tools.** None of them runs a simulation or changes a run record or a stored result; each writes only its
own report. Their final outputs were written at about 19:12 UTC on 2026-10-20, after the last result was stored and
with no live owner process.
- `scripts/replay_verdicts.py` re-runs the current verifier on the stored run graph of every result with a verifier
  verdict and requires the verdict, the failed checks and every component status and uncertainty to match (E11).
  Final output: 137 of 137 match (benchmark B, C-rule, C-rule-prereg, C-llm, C-llm-r2, C-llm-r3, Bexh; the attack
  systems except L-judge). Output: `results/analysis/replay.json`.
- `scripts/audit_runs.py` compares the run store with the stored results and the git history: runs no result names,
  orphaned 'running' records, failed runs, records without the R19 hashes, superseded loop attempts and earlier
  attempts under a current run id (§8, "Observations"). Final output: 214 run records (198 completed, 9 failed,
  7 'running' with no live owner); 11 are named by no stored result. Output: `results/analysis/run_audit.{json,md}`.
- `scripts/dump_untraced.py` lists every number in LLM-written text that the numeric audit could not trace, with its
  context and a mechanical triage (convention, leakage-check, other). Final output: 251 untraced tokens, against 205
  at 15:31 UTC; the 46 added since are all in C-llm-r3 text. Output: `results/analysis/untraced_numbers.{json,md}`;
  the per-token reading of the tokens is in `results/analysis/untraced_classification.{json,md}`.

**Post-hoc analysis scripts** (not part of the §19 protocol; §6, item 7). None edits the decision code:
`run_rule_prereg.py` and `posthoc_allgeometry.py` apply their variants by replacing or wrapping functions inside the
script, and `posthoc_acceptance_rule.py` re-aggregates copies of the replayed checks with the decision code's own
`aggregate()`.
- `scripts/posthoc_acceptance_rule.py` replays the verifier on the stored run graphs and re-aggregates the component
  checks under two looser acceptance rules (V1 combined U only; V2 no τ/2 limit on the domain component), to show
  what blocks acceptance. No simulation. Output: `results/posthoc/acceptance_rule.{json,md}`.
- `scripts/posthoc_review_tests.py` tests the LLM acceptance review on the two real ACCEPTs and on a counterfactual
  X1 ACCEPT (§8, "Observations"). By default it only rebuilds and hashes the review packages; `--call` asks the LLM
  again. No simulation. Output: `results/posthoc/review-on-accepts/`.
- `scripts/run_rule_prereg.py` runs the rule planner exactly as pre-registered (C-rule-prereg) through the normal
  loop, for the 5b sensitivity analysis. It reuses runs from the store and runs new simulations where none exist.
  Output: `results/benchmark/C-rule-prereg/`.
- `scripts/posthoc_allgeometry.py` evaluates the `-allGeometry` variant for J1: statically on every benchmark case
  (no simulation; `results/posthoc/B-allgeo/`) and, with `--adaptive`, with the rule planner on the cases whose
  static verdict changes, which runs simulations (`results/posthoc/C-rule-allgeo/`).
