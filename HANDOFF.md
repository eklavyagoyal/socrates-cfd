# Handoff: socrates-cfd, autonomous CFD verification prototype (state as of 2026-10-19)

You are a senior scientific-software engineer with expertise in CFD, OpenFOAM, Python, numerical verification,
reproducible scientific computing and agentic systems. You are taking over a research prototype that is mostly built
and is in the middle of its benchmark phase. This document follows the structure of the original specification
(sections 1–42). For each section it says what was built, where it lives, its current state and what remains.
Work autonomously: do not stop to ask for approval, inspect → diagnose → fix → rerun, report negative results honestly.

Repository: `eklavyagoyal/socrates-cfd`, branch `claude/cfd-verification-prototype` (68+ commits, all pushed). Working
copy: `/home/user/socrates-cfd`. Commit and push regularly with `git push -u origin claude/cfd-verification-prototype`.
Do not open a PR unless asked. Do not put model names in commits or files. End each commit message with:

```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KH8h3QCU9QdRP5taVGvXgn
```

## Goal

The long-term vision: a user asks an engineering question; the system runs simulations, decides whether there is
enough numerical and physical evidence to trust the answer, requests more simulations when needed, and returns a
quantitative result with an auditable evidence trail.

This prototype tests whether the core loop is feasible:

> problem → OpenFOAM simulation → deterministic evidence → checks (PASS/FAIL/INCONCLUSIVE) → critic → validated
> experiment → new simulation → new evidence → verdict (ACCEPT/REJECT/INCONCLUSIVE)

The LLM is never a source of numerical truth. It sees recorded evidence only, may only pick one of four validated
experiment primitives, and has no ACCEPT/REJECT authority; every number it writes is audited.

**Status in one paragraph.**
- Phases 0–8 (research, design, baseline, evidence engine, deterministic verifier, adversarial cases, static
  evaluation, experiment primitives, LLM critic and loop) are complete, reviewed and tested (99 unit tests pass).
- Phase 9 is running in background processes on 4 cores:
  - the adaptive systems on 17 benchmark cases;
  - the fixed exhaustive protocol;
  - the attacks;
  - stage 2 of the baseline study (to finalise the reference values).
- Partial results already show the main findings (section 39).
- Still to do: finish the runs; recompute the reference and labels; rewrite `reports/baseline_validation.md` with the
  fact-check corrections; run the remaining ablations; write `reports/benchmark_results.md` and
  `reports/final_report.md` (13 questions + 5 pre-registered success criteria); update README and docs.

---

## 1. Initial benchmark: done

- 2D incompressible laminar flow past a circular cylinder at **Re = 100**, unbounded stream. D = 0.01 m,
  U = 0.15 m/s, ν = 1.5e-5 m²/s, ρ = 1.2 kg/m³.
- Requested outputs: time-mean drag coefficient and Strouhal number, each to **τ = 3 %**. r.m.s. lift is reported
  for validation only.
- Why Re = 100: periodic shedding (above Re_c ≈ 47) and still two-dimensional (below mode A at ≈ 188.5). It is
  well documented.
- Sources and verified reference data: `docs/research.md` §1–§2.
  - Primary source: Qu et al. 2013, J. Fluids Struct. 39:347.
  - Bands: Cd 1.31–1.33, St 0.164–0.166, Cl′ 0.222–0.235.
  - Forced-steady Cd 1.058 (Fornberg 1980).
  - Blockage data from Behr et al. 1995 and Qu et al.
  - Unverified items are marked `UNVERIFIED`.

## 2. Architecture: done

Python package `src/socrates/` orchestrating OpenFOAM v2412 (ESI, package `openfoam2412=2412.260127-1`, sourced from
`/usr/lib/openfoam/openfoam2412/etc/bashrc`).

| module | role |
|---|---|
| `case_generation/` | `spec.py` (ProblemSpec, CaseConfig; `content_hash` is stable when new fields are at their defaults), `blockmesh.py` (parametric O-grid + far field, systematic refinement keeping expansion ratios), `writer.py` (case dictionaries), `catalog.py` (cases as YAML diffs against the baseline) |
| `openfoam/` | `runner.py` (blockMesh → checkMesh -allGeometry -allTopology → setFields → solver; restart/mapFields), `parsers.py` (checkMesh, solver logs, `.dat` series; checkMesh always exits 0, so its log is parsed) |
| `evidence/` | `extract.py` (evidence JSON sections), `signals.py` (MSER, cycle statistics, two St estimates) |
| `checks/` | `static.py` (single-run checks), `sensitivity.py` (Richardson/Celik), `verifier.py` (RunGraph, families, aggregation) |
| `experiments/primitives.py` | REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN, RUN_LONGER: validation, limits, planning |
| `critic/` | `prompt.py` (blind, anonymised evidence package), `backends.py` (`claude -p`, no tools, JSON schema), `schema.py`, `audit.py` (numeric audit), `rule_based.py` |
| `orchestration/` | `store.py` (content-addressed run store, CPU slots, orphan adoption), `loop.py` (adaptive loop, planners, authority), `systems.py` (benchmark systems, decision-code fingerprint), `truth.py` (reference and labels), `evaluation.py` (result staleness, infrastructure-error classification; not fingerprinted) |
| `reporting/report.py` | per-case reports with evidence graphs |

## 3. Structured problem specification: done

`configs/problem_cylinder_re100.yaml` holds:
- the question text;
- geometry, operating conditions and fluid;
- the requested outputs;
- the per-quantity tolerance (3 %);
- `reference_mode: blind`: reference values are never shown to the verifier or the critic.

## 4. Credible baseline case: done (report under revision)

**Case** (`cases/baseline/baseline.yaml`):
- Domain: 30 D upstream, 50 D downstream, ±40 D laterally (blockage 1.25 %).
- Mesh: 30,580 hex cells, 160 around the cylinder, first cell 0.005 D.
- Solver and schemes: pimpleFoam in PISO mode (1 outer, 2 correctors), backward time scheme, `linearUpwind`.
- Time: dt = 0.01 D/U (Co 0.73), 150 D/U, averaging from 75 D/U.
- Boundaries: free-slip sides; a setFields perturbation triggers shedding.

**Run** `baseline-408129116207`:
- stationary Cd 1.3311, St 0.1634, Cl rms 0.2286;
- checkMesh OK, 12 stationary cycles;
- 1,441 s wall time.

**Verification study** (`scripts/baseline_study.py`; results in `results/baseline/`):

| chain | levels | run ids |
|---|---|---|
| mesh | f = √2, 2, both mapped from the root | `baseline.m1.41-807cdf343a51`, `baseline.m2-93c9ab8d6f2d` |
| time | dt/2, dt/4, from the root | `baseline.dt0.005-693742b868bc`, `baseline.dt0.0025-f1e9eaf0cd2a` |
| domain | ×2 from the root, ×4 from ×2 | `baseline.D2x-efba395f6c27`, `baseline.D2x-4312d7d8fec3` (the ×4 run is named `D2x` because child names record only the step's own factor) |
| longer | root continued to 250 D/U | `baseline.long250-8b585d987e4c` |

**Stage 2 is complete.** The reviewers found that the ×2 and ×4 domain levels had not reached a limit
cycle in 80 D/U: drag was still falling and the wake had not crossed the enlarged domain. Stage 2:
- continues ×2 to 180 D/U (`baseline.long180-94a31bca23fd`, done: Cd settled at 1.32188, versus 1.32259 at 80 D/U);
- continues ×4 to 280 D/U (`baseline.long280-3b986ef1d905`, done: Cd settled at 1.31576, versus 1.31789 at 80 D/U);
- adds a fourth time level, dt/8 (`baseline.dt0.00125-f6325a72e9cd`, done).

`results/baseline/study.json` now has a `stage2` key; the stage-1 record is `results/baseline/study_stage1.json`.

**Reference ("truth")** (`scripts/make_baseline_report.py` → `results/baseline/truth.json`,
`reports/baseline_generated.md`):
- T = baseline + Σ per-factor Richardson corrections (additive one-factor model).
- Each chain is extrapolated with Celik's procedure, with p = min(observed, formal) and Fs = 3 outside the band.
- Every member's value comes from its longest continuation; the time chain uses its finest three levels.
- Mesh levels are shifted to the baseline dt with the time chain's error model C·dt^p. This removes the double
  counting from Courant-controlled dt in the mesh chain; the shift moved T_Cd by +0.31 %.
- Members' statistical uncertainties are carried through the extrapolation weights.

**Final values (stage 4): Cd T = 1.3155 ± 0.94 %, St T = 0.1639 ± 0.46 %.**
- Stage 3 added a ×3 domain level (half-height 120 D; `baseline.D1.5x` continued to 200 D/U as `baseline.long200-…`).
  It showed the standard domain chain is not asymptotic.
- Stage 4 (`scripts/farfield_resolution_test.py` → `results/baseline/farfield_test.json`) re-ran the ×4 domain with
  far-field counts ×1.5 (`baseline.D4x.ff1.5-949b19f791f0`): Cd +0.16 %.
- So EXPAND_DOMAIN's far-field coarsening confounds the domain chain. The reference uses the refined ×4 member
  (domain order 1.20, correction −1.24 %) and carries the difference from the standard chain (0.82 % of Cd) as a
  far-field model-form term.
- Other U(T) terms:
  - time-overlap model form: the finest-mesh dt pair shows the shift's mesh dependence;
  - time conditioning: the finest three versus the coarser three time levels.
- History of T_Cd: 1.3133 (stage 1) → 1.3046 (stage 2) → 1.290 ± 6 % (stage 3, four-level standard chain) →
  1.3155 (stage 4).
- The full write-up is `reports/baseline_validation.md` (final, after two fact-checks; a third is running).

**Main baseline findings so far:**
- **Domain size is the largest error component** (−1.4 % on Cd).
- **Mesh refinement raises Cd and St.**
- **Time convergence is slower than the scheme's formal order.**
  - Cd converges at observed order ≈ 1.1, not 2. The cause is not identified; candidates are the lagged convecting
    flux and the ddtCorr flux correction.
  - St changes by an almost constant step per dt halving (apparent order 0.25). The dt/8 level tests this.
  - Qu et al. report the opposite dt trend for Cd, St and Cl′; this is unexplained.
- **The pre-registered verifier cannot ACCEPT the baseline's drag, even with all 10 study runs.** The Cd domain U
  is 2.62 % > τ/2. St reaches ACCEPT (combined U 1.86 %).
- **The baseline is plausibly credible:** its drag error is +1.20 % (interval 0.27–2.14 % with U(T)).

**Open (task #14):** `reports/baseline_validation.md` is a draft. An adversarial fact-check found 43 issues; the
corrections to apply are listed in section "Open tasks" below.

## 5. Adversarial simulations: done

All cases are YAML diffs on the baseline. `benchmark/manifest.yaml` is the pre-registered list: id, intended label,
expected expert judgement, revealing experiment. `cases/adversarial/DISCARDED.md` lists rejected candidates (for
example, C1 at dt = 0.1 diverged and was replaced).

| case | change | intended | revealing primitive |
|---|---|---|---|
| baseline | — | credible | — |
| K1_central_scheme | central differencing | credible | — |
| K2_fine_large | mesh ×1.25, dt 0.007, domain 40/60/±60 D | credible | — |
| A1_coarse_mesh | mesh ×0.5 | flawed | REFINE_MESH |
| A2_moderate_mesh | mesh ×0.75 | ambiguous | REFINE_MESH |
| B1_small_domain | 8/15/±4 D domain | flawed | EXPAND_DOMAIN |
| B2_moderate_domain | smaller domain | ambiguous | EXPAND_DOMAIN |
| C1_large_timestep | dt 0.05, nOuter 3 | flawed | REDUCE_TIME_STEP |
| C2_euler_large_timestep | Euler, large dt | flawed | REDUCE_TIME_STEP |
| D1_steady_solver | simpleFoam on a periodic flow | flawed | static |
| E1_noslip_side_walls | no-slip lateral walls | flawed | EXPAND_DOMAIN |
| F1_upwind_convection | first-order upwind | flawed | REFINE_MESH |
| G1_premature_averaging | averaging during the transient | flawed | RUN_LONGER |
| G2_average_from_start | averaging from t = 0 | flawed | static |
| H1_dynamic_viscosity | ν entered as μ (solves Re = 83.3) | flawed | static |
| I1_force_reference | wrong force reference values | flawed | static |
| J1_coarse_wake | wake cells ×0.3 | flawed | REFINE_MESH |

Attack cases, built to defeat the verifier, live in `cases/attacks/`:
- **X1_cylinder_geometry:** meshed cylinder 5 % too large, so it effectively solves a different problem.
- **X2_inlet_shear:** sheared inlet profile with the correct mean velocity.
- **X3_compensating_errors:** coarse mesh plus a tight domain, with partly cancelling biases.

## 6. Evidence extraction: done

`evidence/extract.py` writes `results/runs/<id>/evidence.json` with these sections:
- mesh (checkMesh including patch bounding boxes, measured geometry, representative cell size h = √(A/N));
- domain, configuration, solver (completion, Courant number, last p-solve per step);
- residuals, conservation (boundary fluxes), inlet (measured profile);
- forces, temporal behaviour, cost;
- QoIs `reported` (declared window) and `stationary`.

Statistics (`evidence/signals.py`):
- MSER on per-cycle series. It hits its 50 % cap on every run here, and this is reported as a cap flag.
- Integer cycles. St from zero crossings and from the FFT.
- Batch-means CI, drift and half-window difference; period drift for St.
- Non-finite or unbounded histories are reported as such.

The extractor fingerprint is stored in every evidence file. `RunStore.reextract(run_id)` rebuilds evidence from the
retained raw outputs.

## 7. Deterministic verification: done (pre-registered; frozen during the benchmark)

`checks/static.py` checks:
- solver completion, mesh quality, mass conservation, linear solvers, Courant number;
- Reynolds number, force reference, physics regime, scheme order;
- averaging window (a measured bias), statistics;
- in verifier v2 only (`configs/verification_v2.yaml`): geometry consistency and inlet uniformity.

`checks/sensitivity.py`, `assess_sequence`, works in this order:
1. FAIL first if the demonstrated change minus 2× noise exceeds τ.
2. Two levels: Fs = 3 with the assumed order.
3. Three levels: Celik observed order (bracketed root, ∞ sentinel above p_max). Fs = 1.25 if the order is in
   [0.5, 2]× formal; otherwise p = min(observed, formal) with Fs = 3.
4. Oscillatory or noise-level sequences: range-based.
5. Monotone divergence, or a degenerate family: INCONCLUSIVE.

The domain error order is q = 1.

`checks/verifier.py`:
- Builds refinement families over continuation classes.
- Member-reliability gate: Fs₂·u > frac·τ makes a member unreliable, which points to RUN_LONGER.
- Aggregation:
  - A component passes if U ≤ τ/2.
  - ACCEPT needs every component to pass, the averaging bias plus the RSS of the other components ≤ τ, and every
    gate to pass.
  - Any FAIL → REJECT.
  - Two policy concerns can be discharged: the Courant concern by a time PASS, the scheme-order concern by a mesh PASS.
- Every threshold and its source is in `configs/verification.yaml`.

## 8. Active experiments: done

`experiments/primitives.py`:

| primitive | parameter range (default) |
|---|---|
| REFINE_MESH | factor 1.3–2.0 (√2) |
| REDUCE_TIME_STEP | factor 1.5–4 (2) |
| EXPAND_DOMAIN | factor 1.5–3 (2) |
| RUN_LONGER | 25–300 extra D/U (100) |

- Limits: cumulative refinement ≤ 2× root, ≤ 160k cells, dt ≥ root/8, domain ≤ 4× root, end time ≤ 600 D/U.
- REFINE_MESH keeps the predicted Courant number ≤ 0.9 by lowering dt, and records the change.
- Initialisation: mapped children start from the parent's periodic state and run 80 D/U with averaging from 40.
  If the parent is not periodic, the child starts fresh. RUN_LONGER restarts from the actual latest time.
- Factors are canonicalised (snapped to the default within 0.1 %, otherwise rounded to 3 decimals), so identical
  requests reuse runs.
- **Run store** (`orchestration/store.py`):
  - Content-addressed: id = name + hash(config + initialisation).
  - Provenance in `run.json`; cache hits logged in `requests.jsonl`.
  - Cross-process CPU slots (fcntl locks; `SOCRATES_CPU_SLOTS`) and per-run locks.
  - A run whose owner died is adopted if its own solver log completed with the right `Case:` header and its final
    state was written; otherwise it is deleted and re-run.

## 9. Mesh-sensitivity experiment: done

This is the smallest falsification test (A1). Static verifier: INCONCLUSIVE. C-rule ran one REFINE_MESH (1.06× root
compute): St changed by 3.28 % > τ, so mesh sensitivity FAILs and the verdict is REJECT. The idea was not falsified
by this test.

## 10. LLM critic: done

- `critic/backends.py`: ClaudeCLIBackend (`claude -p`, no tools, JSON-schema output, effort "high"). It filters the
  environment and records the CLI version and a model fingerprint per call.
- `critic/prompt.py`:
  - System prompt.
  - Blind, anonymised package: run ids are replaced by R0, R1, …, including in dict keys, history and feedback.
  - Experiment menu with cost estimates.
  - Previous decisions with their meta-data stripped.
- `critic/schema.py`: pydantic `CriticDecision`.
- `critic/audit.py`: printed-precision numeric audit. The critic's own earlier statements are excluded from the
  pool of known numbers.
- Acceptance review (`REVIEW_SYSTEM_PROMPT`): veto-only, StrictBool; a concern blocks only if it cites evidence fields.

## 11. Authority boundaries: done and tested

- The LLM may only return MORE_EVIDENCE with one menu primitive, or stop. A proposed ACCEPT or REJECT is an authority
  violation: it is not executed and is fed back.
- Experiments are validated; invalid, duplicate or over-budget proposals are rejected with feedback.
- Budgets: 6 experiments, 12 planner calls, 12× root compute, 3 invalid actions.
- No shell access. The final verdict always comes from the deterministic verifier.
- Tests: `tests/test_loop_authority.py`.

## 12. Provenance: done

Every run records:
- configuration and content hash;
- parent run, reason, requesting planner, experiment, config diff and initialisation;
- software versions and git commit;
- commands, wall time;
- SHA-256 of logs, postProcessing outputs and final fields;
- extractor fingerprint.

Every benchmark result is stamped with:
- the decision-code fingerprint, currently **`6406c53bb2011ef5`** (covers `checks/`, `critic/`, `evidence/`,
  `case_generation/`, `experiments/`, `openfoam/parsers.py`, `orchestration/{loop,systems,store}.py` and the three
  configs);
- the evidence digest of every run it used (new results);
- the benchmark git commit and a dirty flag.

## 13. Evidence graph: done

`reporting/report.py` writes `reports/cases/<case>__<system>.md`: per-iteration decisions, experiments and parent →
child observations.

## 14. Final report: not yet written

Per-case reports exist. `reports/final_report.md` must answer the 13 questions (section 40) and evaluate the 5
pre-registered success criteria (`docs/design.md` §19).

## 15. Benchmark evaluation: implemented, results pending

- Pre-registered protocol: `docs/design.md`, "Pre-registered evaluation protocol" and §19.
- Labels (`orchestration/truth.py::label_case`): e = |reported − T|/T.
  - flawed: e > τ, a requested quantity is missing, or the set-up solves another problem (wrong Re, steady formulation);
  - credible: e ≤ τ/2;
  - ambiguous: otherwise;
  - ambiguous also when [e − U(T), e + U(T)] straddles τ or τ/2, unless the case is flawed for every T in the interval.
- Analysis (`scripts/analyze_benchmark.py` → `benchmark/labels.json`, `results/benchmark/metrics.json`,
  `reports/benchmark_tables.md`, `reports/figures/*.png`):
  - Root per case: the content-addressed run of the manifest definition.
  - Stale results (other decision code, other root, evidence changed) are listed and not counted.
  - ERROR results are excluded from rate denominators.
  - Ambiguous cases get neutral, unscored outcome classes.
  - Rates are per label, false acceptance first.
  - Secondary post-hoc view with point-estimate labels.
  - Calibration table: the verifier's U against the error versus T.
  - LLM-variance table.
- `scripts/make_reports.py` assembles `reports/benchmark_results.md`.

**Labels with the final reference (stage 4).** Both views are pre-registered: the §19 rule verbatim, and the risk
mitigation as operationalised in R18.
- With the mitigation:
  - flawed: A1, B1, B2, D1, F1, H1, I1;
  - ambiguous: the other 10;
  - credible: none.
- §19 verbatim:
  - credible: baseline (Cd +1.20 %), K2, A2, C1, J1;
  - flawed: the 7 above plus C2;
  - ambiguous: K1, E1, G1, G2.
- Several intended-flawed cases are not flawed at τ = 3 % (C1, J1, G1, G2, E1).

## 16. Compare three systems: running

| system | definition |
|---|---|
| A | OpenFOAM diagnostics only: completed, checkMesh OK, steady residualControl met |
| B | static deterministic verifier on the single run |
| C-llm (the "C" system) | adaptive: verifier + LLM critic + primitives |
| C-rule | adaptive with the pre-registered rule-based planner: averaging/statistics → mesh → time → domain; RUN_LONGER on unreliable members |
| Bexh | fixed exhaustive protocol: RUN_LONGER, REFINE ×2, REDUCE_TIME_STEP, EXPAND_DOMAIN, then verify |
| L-judge | LLM judging the static evidence only: no checks, no verdict, no experiments |

Verdicts so far (`python3 scripts/status.py`):

| case | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| baseline | ACC | INC | ACC | INC | … | INC |
| K1 / K2 | ACC / ACC | INC / INC | ACC / ACC | … | … | … |
| A1 | ACC | INC | REJ | REJ | … | … |
| A2 | ACC | INC | ACC | … | … | … |
| B1 | ACC | INC | REJ | … | **REJ** | … |
| B2 | ACC | INC | REJ | … | … | … |
| C1 / C2 | ACC / ACC | INC / INC | ACC / INC | … | … | … |
| D1 | REJ | REJ | REJ | REJ | REJ | REJ |
| E1 | ACC | INC | ACC | … | … | … |
| F1 | ACC | INC | REJ | … | … | … |
| G1 / G2 | ACC / ACC | INC / INC | REJ / ACC | … | … | … |
| H1 / I1 | ACC / ACC | REJ / REJ | REJ / REJ | REJ / REJ | REJ / REJ | … |
| J1 | REJ | REJ | REJ | REJ | REJ | … |

## 17. Repository: done

See the map in `README.md`. Top level: `benchmark/`, `cases/`, `configs/`, `docker/`, `docs/`, `references/`,
`reports/`, `results/` (runs, benchmark, attacks, baseline, posthoc, logs), `scripts/`, `src/`, `tests/`.
Generated meshes and fields are gitignored; the case dictionaries, evidence, series and provenance are committed.

## 18. Reproducibility: done

- `docker/Dockerfile` pins the OpenFOAM package; Python packages are pinned in `requirements.lock`.
- `docs/methodology.md` §9: A1 was re-run from scratch in the container and reproduced bitwise, with the same run id.
- Single-core runs are deterministic.

## 19. Testing: done

`pytest -q` runs 99 unit tests. `pytest -m openfoam` runs 8 integration tests that need OpenFOAM; `pyproject.toml`
deselects them by default. Fixtures come from real v2412 output. Coverage:
- parsers, signals, every check's status logic;
- the Richardson/Celik mathematics and regression cases from the reviews;
- primitives and limits;
- critic blindness and the numeric audit;
- loop authority, outage classification and result staleness.

## 20. Development phases

| phase | status |
|---|---|
| 0 research, 1 design (incl. pre-registration) | done (`docs/research.md`, `docs/design.md`) |
| 2 baseline | done; stage 2 of its study is running; report under revision |
| 3 evidence, 4 verifier, 5 cases, 6 static test, 7 primitives, 8 critic and loop | done |
| 9 benchmark, attacks, ablations | running |
| final deliverables | partially done (section 40) |

## 21. Explicitly out of scope

Unchanged from the specification: no UI, no multi-solver support, no cloud platform, no turbulence, no 3D. The README
states that this is a single-benchmark research prototype.

## 22. Primary success criterion: demonstrated on B1 (C-llm)

B1 (small domain):
- the solver completes;
- A ACCEPTs, and B is INCONCLUSIVE with no failed checks;
- the LLM critic chose EXPAND_DOMAIN ×2 as its first and only experiment (0.78× root compute);
- Cd changed by 8.86 % and St by 6.65 %, so domain sensitivity FAILs and the verdict is REJECT.

A1 under C-rule is a second instance (section 9).

## 23. Scientific development rules: followed

- Every threshold has a source in `configs/verification.yaml`.
- Every correction found in review is logged in `docs/methodology.md` §7:
  - R1–R25: two adversarial code-review rounds;
  - R26–R35: the fix-verification round;
  - E1–E10: the evaluation-pipeline review.
- All of these were found before any result was used.
- Observations logged without changing the pre-registered verifier: J1's `-allGeometry` determinant failure.

## 24–25. Autonomous execution and decision authority

Continue without approval. Design decisions are logged in `docs/design.md` (decision log).

Rule: **do not edit any fingerprinted file (section 12) while benchmark processes are running.** It changes the
decision-code fingerprint, and every stored result, LLM calls included, would be recomputed on the next invocation.
Evaluation-only code can be changed freely: `scripts/`, `orchestration/{truth,evaluation}.py`, `reporting/`.
Fix a real bug in the decision code anyway, then accept the recompute.

## 26–34. Phases 0–8

Done; see sections 1–13 and `docs/methodology.md`. Reviews were run as multi-agent adversarial workflows; their
findings were verified individually before fixing.

## 35. Autonomous verification loop: done

`orchestration/loop.py::run_adaptive`:
1. verify the current graph;
2. if the deterministic verdict is ACCEPT or REJECT, stop;
3. otherwise ask the planner for one primitive and validate it (unknown parent, validator, duplicate, budget);
4. execute it through the run store and repeat.

With `acceptance_review=True`, a deterministic ACCEPT is first shown to an LLM reviewer, which may only downgrade it
to INCONCLUSIVE. `LoopResult` records the history, experiments, cost, authority violations, `n_planner_failures` and
`n_invalid_events`.

## 36. Phase 9: benchmark (running)

Background processes (kill only by PID: `pkill -f` once killed the agent's own shell):

| PID | command | slots | log |
|---|---|---|---|
| 10692 | `run_benchmark.py --systems A,B,L-judge,C-rule,C-llm --workers 64` | 3 | `results/logs/benchmark.log` |
| 19152 | `run_benchmark.py --systems A,B,L-judge,Bexh --workers 24` | 3 | `results/logs/benchmark_bexh.log` |
| 10959 | `run_attacks.py --workers 12` | 3 | `results/logs/attacks.log` |

- The scripts are resumable: completed runs and current results are reused, stale or ERROR results are recomputed.
  A process that dies leaves its solvers running; they are adopted later.
- Monitor with `python3 scripts/status.py` (runs and verdict summary) and the logs.
- The remaining compute is large: on the order of 10–20 h of machine time on 4 cores. Bexh runs its full protocol
  even on statically rejected cases, as pre-registered.
- If the container restarts: relaunch the four commands above with the same `SOCRATES_CPU_SLOTS`. The benchmark and
  attacks use 3 slots, leaving slot 3 free for the study.

Stage 2 is done. `make_baseline_report.py` and `analyze_benchmark.py` have been run on it; rerun the analysis after
every batch of results. Still to do: rewrite `reports/baseline_validation.md` (task #14).

## 37. Attack your own system: running

Systems:
- B-v1, C-rule-v1, C-llm-v1: the pre-registered verifier;
- C-llm-v1+review: the same, with the LLM acceptance review;
- B-v2, C-rule-v2: verifier v2, which adds geometry consistency (measured cylinder diameter from the patch bounding
  box) and inlet uniformity;
- L-judge: added because it is a strong baseline on the benchmark.

Results go to `results/attacks/<system>/`.

Status:
- X2 roots are done: B-v1 INCONCLUSIVE, B-v2 REJECT. The adaptive variants are running.
- X1 and X3 roots are queued.
- The running attack process predates the addition of L-judge. Rerun `scripts/run_attacks.py` after it finishes;
  existing results are skipped. Then run `--benchmark-extensions` to measure false vetoes from the review and false
  rejections from v2 on the benchmark cases.

## 38. Ablation tests

| ablation | status |
|---|---|
| C-rule vs C-llm | running |
| Bexh | running |
| L-judge | done (K1 recomputed on corrected evidence) |
| acceptance review | in the attacks |
| LLM run-to-run variance | to do: `run_benchmark.py --systems C-llm-r2,C-llm-r3` after C-llm finishes; analysed by the variance table |
| post-hoc J1 variant | to do: `scripts/posthoc_allgeometry.py --adaptive`. The static part is done: J1 moves REJECT → INCONCLUSIVE, no other case changes (`results/posthoc/`). It is a protocol deviation and must be reported separately |

## 39. Scientific falsification: findings so far (not final)

1. **OpenFOAM diagnostics (A) accept 6 of the 7 robustly flawed cases** (all but D1). The adversarial cases are not
   trivial for ordinary tools.
2. **The static verifier (B) never falsely accepts,** but it detects only the configuration-level errors (D1, H1, I1).
   Everything else is INCONCLUSIVE.
3. **The evidence-only LLM judge (L-judge) is the strongest no-experiment system.** It detects 7 of 7 robustly flawed
   cases from configuration smells and accepts all point-estimate-credible ones. However:
   - its ACCEPTs rest on no demonstrated numerical accuracy;
   - it also ACCEPTs cases whose St error is 1.9–2 % (A2, G2).
   The attacks test whether it can be fooled by a clean-looking configuration.
4. **Adaptive verification works when a flaw is exposed by a primitive** (A1, B1), at about 1× root compute. However:
   - it cannot ACCEPT the credible baseline, even with every component measured: the per-component τ/2 rule fails on
     the real 1.4 % domain error;
   - accepting credible cases costs about 7× root compute and may still end INCONCLUSIVE.
5. **Several intended flaws are not flaws at τ = 3 %:** C1, E1, G1, G2, J1. J1 is rejected by every system through
   the checkMesh `-allGeometry` determinant check, although its error is ~1.5 %.
6. **Calibration:** in every result so far where all components were measured, the verifier's U covered the error
   against T. These come from the same Richardson machinery as T, so this is not fully independent.
7. The pre-registered value tests (C resolves a case B leaves INCONCLUSIVE; the LLM beats the rule planner on
   accuracy or cost) still need the finished C-rule/C-llm/Bexh results. If the LLM adds no measurable value, the
   report must say so.

## 40. Final deliverables: checklist

| deliverable | status |
|---|---|
| `README.md` | exists; add a results section at the end |
| `docs/research.md`, `docs/design.md` | done (update the implementation-plan status table in `design.md`) |
| `docs/methodology.md` | done up to E1–E10; add stage 2, the time-overlap correction, J1 post-hoc and the calibration table |
| baseline case, adversarial cases | done |
| evidence extraction, verifier, experiment engine, critic, loop | done |
| benchmark manifest, tests | done |
| raw results | accumulating in `results/` |
| plots/tables comparing A/B/C | generated by `analyze_benchmark.py`; final run pending |
| `reports/baseline_validation.md` | draft; rewrite needed (task #14) |
| `reports/benchmark_results.md` | `make_reports.py`; final run pending |
| `reports/final_report.md` | to write. Answer: 1. Does the prototype work? 2. Which CFD failures can it detect? 3. Which can ordinary OpenFOAM diagnostics already detect? 4. What does the deterministic verifier add? 5. What does the adaptive system add? 6. Does the LLM add measurable value? 7. What failures remain? 8. How often are bad simulations falsely accepted? 9. What is the compute overhead? 10. What would need to improve before researchers could trust this? 11. Is there evidence for a defensible product? 12. What should be built next? 13. What should NOT be built next? Also evaluate the 5 success criteria of `docs/design.md` §19 |

## 41–42. Continuation rule and final principle

Do not stop because a phase is done or something failed: inspect → diagnose → fix → rerun. Do not protect the
hypothesis. Negative results are valid. Report false acceptances first.

---

## Open tasks (in order)

1. **Let the processes finish;** commit result snapshots regularly (`git add -A results reports`).
2. **After stage 2:** run `make_baseline_report.py`, then `analyze_benchmark.py`. Check whether the ×4 domain level
   (`baseline.long280-…`) reached a limit cycle (per-cycle mean Cd flat) and whether dt/8 changes the St behaviour.
3. **Rewrite `reports/baseline_validation.md`** with these corrections:
   - Wording and attribution:
     - Call the baseline "plausibly credible": its pre-registered label is ambiguous.
     - The domain chain scales inlet, outlet and laterals together and coarsens the far field, so it does not isolate
       blockage. The ×2/×4 meshes fail the checkMesh determinant check (152/264 far-field cells).
     - The Cd mesh order (2.66) is implied by the time-overlap shift: the raw Cd mesh chain is flat after one
       refinement. Without the shift, the baseline e_Cd is 1.68 % instead of 1.36 %.
     - St time behaviour: a dt-independent error cannot cause it, because it cancels in differences. Competing
       first- and second-order terms can: an a·dt + b·dt² fit gives a +0.23 % correction against +0.49 % with
       p = 0.25. Three levels cannot separate the two (hence dt/8).
     - Do not attribute the first-order time convergence to PISO splitting.
     - The verifier's U exceeds T's corrections by construction (U = Fs × the same correction), so this is not
       independent evidence that the estimates are correct.
     - The RSS 2.1 %/2.3 % was combined by hand, and the components overlap.
     - Neither blocking component is the pre-registered "two-level Fs = 3" risk.
     - K2 passing the domain component is untested.
     - p = min(observed, formal) is a review correction (R4/E1), not the pre-registered text.
     - Criterion 2b is met as written; the INCONCLUSIVE comes from the separate τ/2 rule.
     - Cl rms has no converged reference: its domain chain is divergent and T ± U overlaps the literature band.
   - Literature comparison:
     - Compare at matched domain size: Posdziech & Grundmann agrees at about 1.325; Qu et al. are about 0.9 % lower.
     - Shi et al. 2004 (300 D circle) is wider than Qu's H = 200 D.
     - The literature table is a subset: Park and Li also lie above T + U.
   - Numbers:
     - ~12 cells inside D/√Re, not 20.
     - Cd 0.09 % above the band; domain statistical term 0.43 %; baseline interval upper bound 2.08 %.
     - St differences 6.5–7.7 × 10⁻⁴ relative (10–12× noise).
     - The 250 D/U continuation changes Cd by 0.002 %.
     - Domain drifts 0.16 % (×2) and 0.17 % (×4).
   - Method description:
     - Statistical terms use the finest and middle members plus the root once.
     - The label instability rule has the A1/B2 exception (a case clearly flawed in one quantity stays flawed).
4. **K1:** if the analysis flags the C-rule/C-llm K1 results as stale (root evidence re-extracted at 09:33:50 UTC,
   after those loops may have started), delete them and run
   `run_benchmark.py --systems C-rule,C-llm --cases K1_central_scheme` once the main process has exited.
5. **After C-llm finishes:**
   - `run_benchmark.py --systems C-llm-r2,C-llm-r3`;
   - `scripts/posthoc_allgeometry.py --adaptive`;
   - `scripts/run_attacks.py` (fills in L-judge), then `--benchmark-extensions`.
6. **Final reports:** run `analyze_benchmark.py` and `make_reports.py`; write `reports/final_report.md`.
   - Primary results use the pre-registered labels; the secondary point-estimate view and post-hoc variants go in
     separate sections.
   - Discuss: the cost of rigour (no credible case acceptable at τ = 3 % with this domain); L-judge's strength and
     what the attacks show about it; the LLM's value against C-rule and Bexh at equal accuracy (cost, experiments);
     classify the untraced numbers in LLM text (mostly derived arithmetic, e.g. 0.30641/√2).
7. Update the README results section and `methodology.md`/`design.md`; commit and push.

## Pitfalls and gotchas

- **checkMesh** always exits 0: parse the log. Non-orthogonality > 70° is only a warning.
- **solverInfo** records only the first p-solve: the last p-solve per step is parsed from the log.
- **OpenFOAM**:
  - `exprFixedValue` needs `valueExpr`.
  - A restart counts `writeInterval` from the start time, so the writer uses the segment length.
  - forceCoeffs columns are read by header name (they are alphabetical in v2412).
- **Run names:** a child's name records only the step's own factor. The ×4 domain level is `baseline.D2x-4312…`; the
  domain continuations are `baseline.long180-…` (×2) and `baseline.long280-…` (×4).
- **Duplicate-looking runs:** two f = 2 baseline meshes exist. `baseline.m2-93c9ab8d6f2d` is mapped from the root
  (study and LLM); `baseline.m2-476115cbbf20` is mapped from √2 (the rule planner and Bexh). Different
  initialisation means a different run id.
- **Old-code runs:** roots finalized by older code lack an `extraction` fingerprint (K1 was re-extracted; C1/C2 too).
  `evaluation.staleness` compares the root's evidence time with a loop's `started` time.
- **Slot accounting:** orphan solvers run outside the CPU slots, so load can exceed 4 for a while.
- **Wall-time metrics** are contaminated by oversubscription. Use cell-steps for compute comparisons.
