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

`tests/` (61+ tests) cover:
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

### Observations logged during the evaluation (not changed in the pre-registered verifier)

- **J1 (coarse wake):** `checkMesh -allGeometry` reports "Cells with small determinant (< 0.001): 48", which OpenFOAM counts as a failed check, so `mesh_quality` FAILs and every system REJECTs J1. Its reported Cd/St are within ~1 % of the baseline, so if the measured label is *credible*, this is a false rejection caused by an extended-geometry quality heuristic rather than by an accuracy problem. A post-hoc variant that treats `-allGeometry`-only failures as INCONCLUSIVE (to be discharged by mesh refinement) is evaluated separately and reported as a protocol deviation.

## 9. Reproducibility check

Case A1 was re-run from scratch inside the container (`docker/Dockerfile`, image built from the pinned
`openfoam2412=2412.260127-1` package and `requirements.lock`) with an empty run store, and compared with the host run:
same content-addressed run id (`A1_coarse_mesh-8db269c22d05`), and mean Cd, St and Cl rms identical to all printed
digits (relative difference 0.0). Files: `results/reproducibility/`. Single-core OpenFOAM runs with identical inputs
and binaries are bitwise deterministic here; parallel (decomposed) runs would not be expected to be.
