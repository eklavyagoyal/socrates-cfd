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
regenerated with `RunStore.reextract` after an extractor change. This was done once,
when a parser bug was found; see §7.

## 3. Deterministic checks (`checks/`)

- Every check returns **PASS / FAIL / INCONCLUSIVE** with value, threshold, threshold source, reason, the quantity it concerns, the error-budget component it estimates (if any), its uncertainty estimate, and the runs it used.
- **Missing evidence returns INCONCLUSIVE** (enforced by a test that feeds empty evidence to every check).

Thresholds come from three places (`configs/verification.yaml`):
1. **OpenFOAM defaults or guidance** (checkMesh limits, the Co < 1 PISO guideline);
2. **Literature** (regime boundaries; Roache/Celik safety factors);
3. **The user's tolerance τ**, via an explicit error budget:
   - each component's uncertainty must be ≤ τ/2 to PASS;
   - a demonstrated change > τ FAILs;
   - ACCEPT needs the root-sum-square of all components ≤ τ.

No physics threshold was invented. Where none is defensible, the check reports
the value and returns INCONCLUSIVE.

**Sensitivity (multi-run) analysis** (`checks/sensitivity.py`) estimates the
uncertainty of the *root* run's value from a one-factor refinement sequence:
- **Two levels:** Richardson with the assumed formal order, Fs = 3.
- **Three levels:** Celik observed order (fixed-point iteration), monotone/oscillatory classification, extrapolation. Fs = 1.25 if the observed order is within [0.5, 2]× formal, else Fs = 3 with the formal order.
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

**LLM critic.** Headless `claude -p` with:
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

**Numeric audit.** Every number in the critic's text is matched against the
numbers in its package (2 % tolerance, percentages allowed). Untraceable numbers are
counted and shown in reports. This catches fabricated values and memorised
literature values.

**Rule-based planner (ablation).** A fixed, pre-registered order:
averaging/statistics → mesh → time → domain, with default parameters, continuing
refinement families from their finest member.

**LLM transport.** Calls are bounded: 300 s timeout, ≤ 3 attempts with exponential
backoff and jitter. Every attempt, error, latency and cost is recorded.

## 6. Evaluation protocol

Pre-registered in `docs/design.md` §19 before any system was run.

**In-house reference.** From the baseline's one-factor chains (mesh f = 1, √2, 2;
Δt = 0.01, 0.005, 0.0025; domain ×1, ×2, ×4):
1. three-level Celik extrapolation per factor;
2. combined additively;
3. uncertainty by root-sum-square;
4. checked against the literature band.

**Labels.** Computed from each case's *reported* values versus the reference:
- **flawed** if max error > τ, a requested quantity is missing, or the set-up solves a different problem;
- **credible** if max error ≤ τ/2;
- **ambiguous** otherwise.

**Metrics.**
- Detection, false-acceptance, correct-acceptance and false-rejection rates.
- Inconclusive rate.
- Experiments and compute per case.
- LLM cost.
- First-experiment usefulness: whether the first executed primitive equals the manifest's pre-registered "revealing experiment".
- Authority violations.
- Untraceable numbers.

**Sharing runs.** All systems use the same run store. Identical experiment requests
reuse identical runs, so system differences are not run-to-run noise.

## 7. Development log of methodological corrections

Each correction was found on real solver output and made as a general rule, not
tuned to a case. All happened before any system evaluation.

1. **Oscillation detector.** It required ≥ 3 crossings in the last quarter of the record, which falsely reported "no oscillation" on 40–90 D/U records. Crossings are now counted on the last half.
2. **Linear-solver check.** It read `solverInfo`, which holds only the first p solve of each step, so it would have FAILed every valid run. It now parses the last p solve per step from the log. Evidence was re-extracted.
3. **checkMesh non-orthogonality > 70°** is a warning in OpenFOAM, not a failure. It now maps to INCONCLUSIVE, not FAIL.
4. **Averaging check.** It PASSed G1 by comparing the reported value with a stationary estimate that was itself transient-contaminated (3 cycles, 4 % drift). It now requires the reference estimate to satisfy the statistics criterion; otherwise INCONCLUSIVE.
5. **Scheme-order check.** It returned PASS when the scheme was not recorded. Caught by the missing-evidence test; now INCONCLUSIVE.
6. **Run-store race.** A second process requesting an in-flight run would have deleted it. The run store now tracks the owner PID and waits.

## 8. What the software tests do and do not establish

`tests/` (95 unit tests plus 8 OpenFOAM integration tests, `pytest -m openfoam`) cover:
- parsers, on real OpenFOAM v2412 output fixtures, including a diverged run;
- signal analysis, on synthetic signals with known answers and a real history;
- every check's status logic and the missing-evidence rule;
- Richardson/Celik mathematics (observed order recovered exactly for known p);
- the aggregation and error-budget rules;
- case generation and systematic refinement;
- primitive validation, including rejection of invalid or out-of-range actions;
- the critic schema and the numeric audit.

**They do not establish** that any simulation is physically right. That is the job
of the verification evidence and of the validation against literature in
`reports/baseline_validation.md`.

### Corrections from the adversarial code review (before any system result was used)

A six-lens adversarial review (signal analysis, check logic, experiments/store/loop, LLM authority, CFD methodology,
evaluation validity) was run with independent reviewer agents while the first benchmark batch was in progress. The
findings below were each traced against the code before fixing. **All benchmark results produced before these fixes were
discarded and every system was re-run on the corrected code** (results now carry a decision-code fingerprint and are
recomputed automatically if that changes).

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

Second-round findings from the same review (latest lens to finish), also fixed before results were used:

| # | Defect | Fix |
|---|---|---|
| R21 | Monotone *divergence* (differences growing under refinement) passed as convergence: Celik's absolute value hides it | R = ε21/ε32 ≥ 1 → no extrapolation (FAIL if change > τ, else INCONCLUSIVE); same in the truth extrapolation |
| R22 | Averaging bias in (τ/2, τ] was "missing evidence", so the rule planner requested RUN_LONGER forever, although no experiment can change the root's declared-window value | Treated as a measured bias: PASS up to τ (reliable reference required), FAIL above |
| R23 | A known, signed bias was RSS-combined as if it were an independent random uncertainty | Bias adds linearly: ACCEPT needs bias + RSS(other components) ≤ τ |
| R24 | A decaying (or still growing) oscillation passed the regime check as "sustained shedding" | Amplitude drift > τ across the window → INCONCLUSIVE (→ RUN_LONGER) |
| R25 | MSER hits its 50 % cap on every run here (exponential approach to the limit cycle), so "transient end detected" overstated what was detected | Reported as "stationary-window start" with an explicit cap flag; stationarity is judged by the drift/half-difference measures |

The fixes were themselves re-reviewed by a second adversarial pass. That fix-verification pass found the following,
also fixed before any result was used (the benchmark was relaunched from scratch afterwards; the stamp of every
result records the decision-code fingerprint and the git commit it was produced with):

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

### Review of the evaluation pipeline (truth, labels, metrics, reports), before any number was reported

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

### Decision rule for success criterion 5b (fixed 2026-10-20 09:20 UTC)

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

### Observations logged during the evaluation (not changed in the pre-registered verifier)

- **J1 (coarse wake):** `checkMesh -allGeometry` reports "Cells with small determinant (< 0.001): 48", which OpenFOAM counts as a failed check, so `mesh_quality` FAILs and every system REJECTs J1. Its reported Cd/St are within ~1 % of the baseline, so if the measured label is *credible*, this is a false rejection caused by an extended-geometry quality heuristic rather than by an accuracy problem. A post-hoc variant that treats `-allGeometry`-only failures as INCONCLUSIVE (to be discharged by mesh refinement) is evaluated separately and reported as a protocol deviation.
  `scripts/locate_flagged_cells.py` places all 48 flagged cells at x ≈ 47 D, next to the outlet
  (`results/posthoc/flagged_cells.txt`); the enlarged-domain meshes of the baseline study fail the same check with
  cells 57–155 D from the cylinder. The flag reacts to stretched far-field cells, not to the wake region that sets
  the forces.
- **The in-house reference needed three stages beyond the pre-registered study** (details and numbers:
  `reports/baseline_validation.md` §3–4). Each change was made before any benchmark result was interpreted, and
  the version history of T is reported.
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
  - The same far-field coarsening inflates the verifier's own domain component (U = 2.62 % of Cd for the baseline),
    which is why no system can ACCEPT the baseline's drag. This is a property of the pre-registered EXPAND_DOMAIN
    primitive and was not changed.

## 9. Reproducibility check

Case A1 was re-run from scratch inside the container (`docker/Dockerfile`, image built from the pinned
`openfoam2412=2412.260127-1` package and `requirements.lock`) with an empty run store, and compared with the host run:
same content-addressed run id (`A1_coarse_mesh-8db269c22d05`), and mean Cd, St and Cl rms identical to all printed
digits (relative difference 0.0). Files: `results/reproducibility/`. Single-core OpenFOAM runs with identical inputs
and binaries are bitwise deterministic here; parallel (decomposed) runs would not be expected to be.
