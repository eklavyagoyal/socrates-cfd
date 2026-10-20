# Handoff: socrates-cfd, autonomous CFD verification prototype (final state, 2026-10-20)

You are a senior scientific-software engineer with expertise in CFD, OpenFOAM, Python, numerical verification,
reproducible scientific computing and agentic systems. You are taking over a research prototype whose planned work is
**complete**: every simulation has finished (last result stored 2026-10-20 19:11 UTC), no process is running, and the
final reports are written. This document follows the structure of the original specification (sections 1–42). For each
section it says what was built, where it lives, and its final state. It ends with the deviations from the
pre-registration, the integrity checks, the open problems and recommended next steps, how to run everything, and the
pitfalls. The authoritative account of the results is `reports/final_report.md`; where this file and that report
differ, the report is right and this file is stale.

Repository: `eklavyagoyal/socrates-cfd`, on the prototype branch (the only branch on `origin` besides `main`;
`git branch --show-current` in the working copy). Working copy: `/home/user/socrates-cfd`. 152 commits; the last,
3e18205 (2026-10-20 19:13 UTC), is pushed. Text revisions made after it (reports, docs, the untraced-number
classification, this file) may still be uncommitted: check `git status` first. Do not open a PR unless asked. Do not
put AI model names or identifiers in commits or files; end each commit message with the attribution lines your
session instructions specify.

## Goal

The long-term vision: a user asks an engineering question; the system runs simulations, decides whether there is
enough numerical and physical evidence to trust the answer, requests more simulations when needed, and returns a
quantitative result with an auditable evidence trail.

This prototype tests whether the core loop is feasible:

> problem → OpenFOAM simulation → deterministic evidence → checks (PASS/FAIL/INCONCLUSIVE) → planner → validated
> experiment → new simulation → new evidence → verdict (ACCEPT/REJECT/INCONCLUSIVE)

The LLM is never a source of numerical truth. It sees recorded evidence only, may only pick one of four validated
experiment primitives, and has no ACCEPT/REJECT authority; every number it writes is audited.

**Status in one paragraph.**
- All phases (research, design, baseline, evidence engine, verifier, adversarial cases, primitives, LLM critic and
  loop, benchmark, attacks, ablations, post-hoc analyses, final reports) are complete.
- 9 benchmark systems × 17 cases = 153 results, all stamped with the final decision-code fingerprint; 21 attack
  results; 214 run records. Nothing is pending.
- Headline (details in §39 and `reports/final_report.md`): as a *filter* the system works on this benchmark (all 7
  robustly flawed cases rejected by C-rule and by all three LLM runs; no case-level false acceptance by any
  verifier-based system on the benchmark or the attacks; one quantity-level false acceptance, X1 St under C-rule-v1);
  as a *certifier* it works only sometimes and not reproducibly (2 correct case-level ACCEPTs, both in LLM repeats,
  each in 1 of 3 runs). Criterion 5b (does the LLM planner beat the rule planner?) is **not met**
  under the committed decision rule.

**Terms used below.**
- *Verification*: were the equations solved accurately enough? *Validation*: were they the right equations?
- *Root run*: the finished simulation under verification. *Child*: an experiment run derived from it. *Mapped child*:
  a child started from its parent's field interpolated onto the new mesh (runs 80 D/U).
- *D/U*: the convective time unit, diameter divided by stream speed.
- *τ*: the requested tolerance, 3 % on each quantity. *Cd*: time-mean drag coefficient. *St*: Strouhal number
  (dimensionless shedding frequency).
- *Component U*: the estimated relative uncertainty from one source (statistics, mesh, time step, domain size).
  *Combined U*: averaging bias plus the root-sum-square of the components.
- *Richardson extrapolation / Celik procedure*: estimate the zero-spacing answer from runs at known refinement ratios,
  assuming error ∝ spacing^p; with three levels the observed order p is measured, and a safety factor Fs = 1.25 is
  applied if p lies within 0.5–2× the formal order, otherwise Fs = 3 (two levels: Fs = 3).
- *False acceptance*: ACCEPT of a flawed case. *Detection*: REJECT of a flawed case. *Correct acceptance* / *false
  rejection*: ACCEPT / REJECT of a credible case. INCONCLUSIVE is safe but undecided.
- *Case level*: both quantities; *quantity level*: one quantity.
- *Two label views*: *point estimate* (the §19 rule applied to the error against the reference T) and *mitigation*
  (also ambiguous when e ± U(T) straddles τ or τ/2). *Robustly flawed*: flawed in both views.
- *Bounds*: one-sided 95 % Clopper–Pearson limits (exact binomial limits on a true rate given k events in n trials;
  for 0/n the upper limit is 1 − 0.05^(1/n)).

---

## 1. Initial benchmark: done

- 2D incompressible laminar flow past a circular cylinder at **Re = 100**, unbounded stream. D = 0.01 m,
  U = 0.15 m/s, ν = 1.5e-5 m²/s, ρ = 1.2 kg/m³ (`configs/problem_cylinder_re100.yaml`).
- Requested outputs: time-mean drag coefficient and Strouhal number, each to **τ = 3 %**. r.m.s. lift is reported
  for validation only.
- Why Re = 100: periodic shedding (above Re_c ≈ 47) and still two-dimensional (below mode A at ≈ 188.5). It is
  well documented.
- Sources and verified reference data: `docs/research.md` §1–§2.
  - Primary source: Qu et al. 2013, J. Fluids Struct. 39:347.
  - Recommended bands: Cd 1.31–1.33, St 0.164–0.166, Cl′ (rms) 0.222–0.235.
  - Forced-steady Cd 1.058 (Fornberg 1980).
  - Blockage data from Behr et al. 1995 and Qu et al.
  - Unverified items are marked `UNVERIFIED`.

## 2. Architecture: done

Python package `src/socrates/` orchestrating OpenFOAM v2412 (ESI, package `openfoam2412=2412.260127-1`, sourced from
`/usr/lib/openfoam/openfoam2412/etc/bashrc`, overridable with `SOCRATES_OPENFOAM_BASHRC`).

| module | role |
|---|---|
| `case_generation/` | `spec.py` (ProblemSpec, CaseConfig; `content_hash` is stable when new fields are at their defaults), `blockmesh.py` (parametric O-grid + far field, systematic refinement keeping expansion ratios), `writer.py` (case dictionaries), `catalog.py` (cases as YAML diffs against the baseline) |
| `openfoam/` | `runner.py` (blockMesh → checkMesh -allGeometry -allTopology → setFields → solver; restart/mapFields), `parsers.py` (checkMesh, solver logs, `.dat` series; checkMesh always exits 0, so its log is parsed) |
| `evidence/` | `extract.py` (evidence JSON sections), `signals.py` (MSER, cycle statistics, two St estimates) |
| `checks/` | `static.py` (single-run checks), `sensitivity.py` (Richardson/Celik), `verifier.py` (RunGraph, families, aggregation) |
| `experiments/primitives.py` | REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN, RUN_LONGER: validation, limits, planning |
| `critic/` | `prompt.py` (blind, anonymised evidence package), `backends.py` (headless LLM command-line client, no tools, JSON schema), `schema.py`, `audit.py` (numeric audit), `rule_based.py` |
| `orchestration/` | `store.py` (content-addressed run store, CPU slots, orphan adoption), `loop.py` (adaptive loop, planners, authority, acceptance review), `systems.py` (benchmark systems, decision-code fingerprint), `truth.py` (reference and labels), `evaluation.py` (result staleness, infrastructure-error classification; not fingerprinted) |
| `reporting/report.py` | per-case reports with evidence graphs |
| `cli.py` | `socrates run-case`, `socrates verify` |

## 3. Structured problem specification: done

`configs/problem_cylinder_re100.yaml` holds:
- the question text;
- geometry, operating conditions and fluid;
- the requested outputs;
- the per-quantity tolerance (3 %);
- `reference_mode: blind`: reference values are never shown to the verifier or the critic.

## 4. Credible baseline case: done (report final)

**Case** (`cases/baseline/baseline.yaml`):
- Domain: 30 D upstream, 50 D downstream, ±40 D laterally (blockage 1.25 %).
- Mesh: 30,580 hex cells, 160 around the cylinder, first cell 0.005 D (about 12 cells inside D/√Re).
- Solver and schemes: pimpleFoam in PISO mode (1 outer, 2 correctors), backward time scheme, `linearUpwind`.
- Time: dt = 0.01 D/U (max Courant 0.73), 150 D/U, declared averaging window 75–150 D/U (11 cycles).
- Boundaries: free-slip sides; a setFields perturbation triggers shedding.

**Run** `baseline-408129116207`:
- reported (declared window) Cd 1.3313, St 0.1634, Cl rms 0.2296; stationary-window Cd 1.3311, Cl rms 0.2286;
- checkMesh OK, 12 stationary cycles;
- 1,442 s wall time (458.7 × 10⁶ cell-steps).

**Verification study** (`scripts/baseline_study.py`, `scripts/farfield_resolution_test.py`; results in
`results/baseline/`; write-up `reports/baseline_validation.md` §3–§4, final after three fact-checks):

| stage | added | why |
|---|---|---|
| 1 | mesh f = √2, 2; dt/2, dt/4; domain ×2, ×4; baseline +100 D/U | pre-registered one-factor chains |
| 2 | domain ×2 → 180 D/U and ×4 → 280 D/U; dt/8 | domain levels had not reached a limit cycle in 80 D/U; St time behaviour unresolved |
| 3 | domain ×3 (half-height 120 D) → 200 D/U | test the conditioning of the domain extrapolation |
| 4 | ×4 and ×1 domains with outer-block cell counts ×1.5 | the four-level domain chain did not converge like a power law |

Run ids of the study: mesh `baseline.m1.41-807cdf343a51`, `baseline.m2-93c9ab8d6f2d`; time `baseline.dt0.005-693742b868bc`,
`baseline.dt0.0025-f1e9eaf0cd2a`, `baseline.dt0.00125-f6325a72e9cd`; domain `baseline.D2x-efba395f6c27` (×2),
`baseline.D2x-4312d7d8fec3` (×4: child names record only the step's own factor), `baseline.D1.5x-ed421affd588` (×3,
first run by an LLM planner and reused), continuations `baseline.long180-94a31bca23fd` (×2),
`baseline.long280-3b986ef1d905` (×4), `baseline.long200-a7dac050dbe5` (×3); refined far field
`baseline.D4x.ff1.5-949b19f791f0`; longer root `baseline.long250-8b585d987e4c`.

**Reference ("truth")** (`scripts/make_baseline_report.py` → `results/baseline/truth.json`,
`reports/baseline_generated.md`):
- T = baseline + Σ per-factor Celik corrections (additive one-factor model), with p = min(observed, formal) and
  Fs = 3 outside the band (review corrections R4/E1; the pre-registered text said "formal order").
- Every member's value comes from its longest continuation; the time chain uses its finest three levels (0.005,
  0.0025, 0.00125); the domain chain uses ×1, ×2 and the far-field-refined ×4 member.
- Mesh levels are shifted to the baseline dt with the time chain's error model C·dt^p (REFINE_MESH ran them at a
  smaller dt); the shift's full effect (+0.30 % on Cd) is carried as a model-form term.

**Final values (stage 4): Cd T = 1.3155 ± 0.94 %, St T = 0.1639 ± 0.46 %.** U(T) is dominated by a far-field
model-form term (0.82 % of Cd: the refined ×4 chain against the standard chain).

| factor | observed order (Cd / St) | correction to the baseline (Cd / St) |
|---|---|---|
| mesh (after the time-overlap shift) | 2.69 / 2.88 | +0.58 % / +0.92 % |
| time (finest three of four levels) | 1.03 / 1.00 | −0.52 % / +0.21 % |
| domain (×4 with refined far field) | 1.20 / 1.30 | −1.24 % / −0.81 % |

History of T_Cd (committed label versions, 10-19): 1.3133 (stage 1, 11:03) → 1.3134 (12:42) → 1.3046 (stage 2, 13:25)
→ 1.3155 (stage 4, 16:43). The stage-3 estimate 1.290 ± 6.3 % (14:26) was never committed as labels.

**Main baseline findings (final):**
- **Domain size is the largest correction** (−1.24 % on Cd with the refined far field; −2.0 % with the standard
  chain, the difference carried in U(T)). Inlet, outlet and sides were scaled together, so blockage is not isolated.
- **EXPAND_DOMAIN coarsens the far field** as the domain grows (last wake cell about 1.0 D at ×1, 2.0 D at ×2,
  3.9 D at ×4); refining the ×4 far field raised Cd by 0.16 % against 0.03 % on the ×1 domain. This confounds every
  domain study in the benchmark.
- **Mesh refinement raises St and Cl rms.** The raw Cd mesh chain is flat after one refinement (1.3349 → 1.3349), so
  the Cd mesh order (2.69) and correction (+0.58 %) are implied by the time-overlap shift; only the net mesh + time
  correction (+0.06 % for Cd) is robust.
- **Time convergence is first order** (observed 1.0–1.1 for Cd, St and Cl rms), not the scheme's formal second
  order; the cause is not identified (candidates: the lagged convecting flux and the ddtCorr flux correction). The
  dt trends are opposite to Qu et al.'s; unexplained.
- **On the full-study graph (baseline + 11 study runs) the pre-registered verifier does not ACCEPT the baseline's
  drag:** the Cd domain component is U = 2.62 % > τ/2 (the Cd components add up to 2.83 % < τ; what fails is the
  per-component τ/2 limit). St is ACCEPTed (combined U 1.86 %).
- **The baseline is plausibly credible, not demonstrably:** Cd error +1.20 % (interval 0.27–2.14 % with U(T)),
  St −0.31 %. Point-estimate label credible; with the mitigation ambiguous.
- In the benchmark, one planner graph (C-llm-r3) did ACCEPT the baseline (Cd U 1.87 %, St U 1.59 %); it does not
  reproduce (§39).

## 5. Adversarial simulations: done

All cases are YAML diffs on the baseline. `benchmark/manifest.yaml` is the pre-registered list: id, intended label,
expected expert judgement, revealing experiment. `cases/adversarial/DISCARDED.md` lists rejected candidates (for
example, a first C1 at Δt ×10 diverged and was replaced). Errors are e = (reported − T)/T against the final T
(`benchmark/labels.json`).

| case | change | intended | revealing primitive | Cd error | St error | label: point est. / mitigation |
|---|---|---|---|---|---|---|
| baseline | — | credible | — | +1.20 % | −0.31 % | credible / ambiguous |
| K1_central_scheme | central (Gauss linear) convection | credible | — | +1.90 % | −0.39 % | ambiguous / ambiguous |
| K2_fine_large | mesh ×1.25, dt 0.007, domain 40/60/±60 D | credible | — | +0.94 % | −0.07 % | credible / ambiguous |
| A1_coarse_mesh | mesh ×0.5 | flawed | REFINE_MESH | −1.55 % | −5.08 % | flawed / flawed |
| A2_moderate_mesh | mesh ×0.75 | ambiguous | REFINE_MESH | +0.51 % | −1.45 % | credible / ambiguous |
| B1_small_domain | domain 8/15/±4 D (blockage 12.5 %) | flawed | EXPAND_DOMAIN | +14.7 % | +9.57 % | flawed / flawed |
| B2_moderate_domain | domain 15/25/±10 D (blockage 5 %) | ambiguous | EXPAND_DOMAIN | +4.24 % | +1.89 % | flawed / flawed |
| C1_large_timestep | Δt ×5, 3 outer correctors (max Courant 3.42) | flawed | REDUCE_TIME_STEP | +0.64 % | −0.26 % | credible / ambiguous |
| C2_euler_large_timestep | Euler, Δt ×4, 2 outer correctors | flawed | REDUCE_TIME_STEP | −1.93 % | −3.33 % | flawed / ambiguous |
| D1_steady_solver | simpleFoam on a periodic flow | flawed | static | −17.0 % | not produced | flawed / flawed |
| E1_noslip_side_walls | no-slip lateral walls | flawed | EXPAND_DOMAIN | +1.89 % | +0.21 % | ambiguous / ambiguous |
| F1_upwind_convection | first-order upwind | flawed | REFINE_MESH | −3.55 % | −23.1 % | flawed / flawed |
| G1_premature_averaging | 40 D/U run, averaged from 10 D/U | flawed | RUN_LONGER | −1.47 % | −1.62 % | ambiguous / ambiguous |
| G2_average_from_start | 60 D/U run, averaged from t = 0 | flawed | static | +0.32 % | −1.52 % | ambiguous / ambiguous |
| H1_dynamic_viscosity | dynamic viscosity entered as ν (solves Re = 83.3) | flawed | static | +2.52 % | −6.05 % | flawed / flawed |
| I1_force_reference | stale force-reference velocity (0.16 vs 0.15 m/s) | flawed | static | −11.1 % | −0.31 % | flawed / flawed |
| J1_coarse_wake | wake streamwise cells ×0.3 | flawed | REFINE_MESH | +0.56 % | −1.11 % | credible / ambiguous |

- Point estimates: 8 flawed, 5 credible (baseline, A2, C1, J1, K2), 4 ambiguous. Mitigation: 7 flawed (C2 becomes
  ambiguous), 0 credible, 10 ambiguous.
- Six of the 12 intended-flawed cases are not flawed with the mitigation (C1, C2, E1, G1, G2, J1), five not on point
  estimates. B2, intended borderline, is robustly flawed.

Attack cases, built to defeat the verifier, live in `cases/attacks/`:
- **X1_cylinder_geometry:** meshed cylinder 5 % too large (1.05 D), so it solves a different problem. Cd +5.98 %,
  St −3.60 %: flawed in every reading.
- **X2_inlet_shear:** sheared inlet profile with the correct mean velocity. Cd +1.20 %, St −0.50 %: flawed only under
  the *set-up* reading of the §19 set-up clause; credible on narrow point estimates; ambiguous otherwise
  (`reports/benchmark_tables.md`, "Attack cases against the reference").
- **X3_compensating_errors:** coarse mesh plus a tight domain, with partly cancelling biases. Cd +5.81 %, St +0.16 %:
  flawed.

## 6. Evidence extraction: done

`evidence/extract.py` writes `results/runs/<id>/evidence.json` with these sections:
- mesh (checkMesh including patch bounding boxes, measured geometry, representative cell size h = √(A/N));
- domain, configuration, solver (completion, Courant number, last p-solve per step);
- residuals, conservation (boundary fluxes), inlet (measured profile);
- forces, temporal behaviour, cost (cells, steps, cell-steps, wall time);
- QoIs `reported` (declared window) and `stationary`.

Statistics (`evidence/signals.py`):
- MSER on per-cycle series. It hits its 50 % cap on most runs here (every 80 D/U mapped level of the baseline study;
  the 120–200 D/U far-field test runs did not), and this is reported as a cap flag; stationarity is judged by the
  drift and half-window measures.
- Integer cycles. St from zero crossings and from the FFT.
- Batch-means CI, drift and half-window difference; period drift for St.
- Non-finite or unbounded histories are reported as such.

The extractor fingerprint is stored in every evidence file. `RunStore.reextract(run_id)` rebuilds evidence from the
retained raw outputs.

## 7. Deterministic verification: done (pre-registered; frozen since 2026-10-19 09:06)

`checks/static.py` and `checks/sensitivity.py` provide 14 check types: solver_completion, mesh_quality,
mass_conservation, linear_solver_convergence, courant_number, reynolds_consistency, force_reference_consistency,
physics_regime, convection_scheme_order, averaging_window (a measured bias), statistical_uncertainty, and the
mesh, time and domain sensitivity checks. Verifier v2 only (`configs/verification_v2.yaml`): geometry_consistency
and inlet_uniformity.

`checks/sensitivity.py`, `assess_sequence`, works in this order:
1. FAIL first if the demonstrated change minus 2× noise exceeds τ (changes are relative to the finer member).
2. Two levels: Fs = 3 with the assumed order.
3. Three levels: Celik observed order (bracketed root, ∞ sentinel above p_max). Fs = 1.25 if the order is in
   [0.5, 2]× formal; otherwise p = min(observed, formal) with Fs = 3.
4. Oscillatory or noise-level sequences: range-based.
5. Monotone divergence, or a degenerate family: INCONCLUSIVE.

The domain error order is q = 1.

`checks/verifier.py`:
- Builds refinement families over continuation classes; each member counts with its longest RUN_LONGER continuation.
- Member-reliability gate: a member with too few cycles or Fs₂·u > frac·τ (3u > τ/2 here) is unreliable, which keeps
  the study INCONCLUSIVE and points the planner to RUN_LONGER.
- Aggregation:
  - A mesh, time, domain or statistics component passes if U ≤ τ/2; the averaging bias passes up to τ.
  - ACCEPT needs every component to pass, the averaging bias plus the RSS of the other components ≤ τ, and every
    gate check to pass or be discharged.
  - Any FAIL → REJECT.
  - Two policy concerns can be discharged: the Courant concern by a time PASS, the scheme-order concern by a mesh PASS.
- Every threshold and its source is in `configs/verification.yaml`.

## 8. Active experiments: done (two primitives are defective)

`experiments/primitives.py`:

| primitive | parameter range (default) |
|---|---|
| REFINE_MESH | factor 1.3–2.0 (√2) |
| REDUCE_TIME_STEP | factor 1.5–4 (2) |
| EXPAND_DOMAIN | factor 1.5–3 (2) |
| RUN_LONGER | 25–300 extra D/U (100) |

- Limits: cumulative refinement ≤ 2× root, ≤ 160k cells, dt ≥ root/8, domain ≤ 4× root, end time ≤ 600 D/U.
- REFINE_MESH keeps the predicted Courant number ≤ 0.9 by lowering dt, but only when the parent's maximum Courant
  number is at most 1; otherwise it keeps dt and records that.
- Initialisation: mapped children start from the parent's periodic state and run 80 D/U with averaging from 40.
  If the parent is not periodic, the child starts fresh. RUN_LONGER restarts from the actual latest time.
- Factors are canonicalised (snapped to the default within 0.1 %, otherwise rounded to 3 decimals), so identical
  requests reuse runs.
- **Defects found in the benchmark** (not fixed; decision code frozen):
  - EXPAND_DOMAIN keeps the per-cell growth rate, so the far field coarsens with each step (§4); every adaptive
    domain U inherits this, and its observed order varies with the levels a planner chose (§39).
  - REFINE_MESH from the C1 and C2 roots (max Courant 3.42 and 2.92) keeps dt; all six root refinements, and Bexh's
    refinements of two already-diverged runs, crashed with floating-point exceptions. The verifier drops failed
    children and reports "no REFINE_MESH experiment has been run", which hides the failure.
  - The menu wording of REFINE_MESH ("Multiply every mesh cell count by `factor`") allows a per-direction and a
    total-cell reading; two LLM calls used the wrong one (they proposed factor 2.0 anyway).
- **Run store** (`orchestration/store.py`):
  - Content-addressed: id = name + hash(config + initialisation).
  - Provenance in `run.json`; cache hits logged in `requests.jsonl`.
  - Cross-process CPU slots (fcntl locks in `results/runs/.slots`; `SOCRATES_CPU_SLOTS`) and per-run locks.
  - A run whose owner died is adopted if its own solver log completed with the right `Case:` header and its final
    state was written; otherwise its directory is deleted and the run is executed again under the same id (see
    Pitfalls).
  - Failed runs (solver or mesh failure) are cached as failures and returned on every later request.

## 9. Mesh-sensitivity experiment: done

This is the smallest falsification test (A1). Static verifier: INCONCLUSIVE. C-rule ran one REFINE_MESH √2 (1.06× root
compute): St changed by 3.28 % > τ (3.24 % after the 2 × noise deduction, a 0.24-point margin), so mesh sensitivity
FAILs and the verdict is REJECT. C-llm refined by ×2 instead (St 4.78 %, 2.14× root). The idea was not falsified by
this test.

## 10. LLM critic: done

- `critic/backends.py`: a headless LLM command-line client invoked with `-p`, no tools, no MCP servers, no settings
  files, JSON-schema output, effort "high", an empty working directory; environment variables that could change the
  model, effort or loaded context are filtered. It records the CLI version and a model *fingerprint* (a hash of the
  reported model identifiers, never the names) per call. Calls time out after 300 s, with at most 3 attempts and
  exponential backoff with jitter.
- `critic/prompt.py`:
  - System prompt.
  - Blind, anonymised package: run ids are replaced by R0, R1, …, including in dict keys, history and feedback.
  - Experiment menu with cost estimates.
  - Previous decisions with their meta-data stripped.
- `critic/schema.py`: pydantic `CriticDecision`.
- `critic/audit.py`: printed-precision numeric audit. The critic's own earlier statements are excluded from the
  pool of known numbers.
- Acceptance review (`REVIEW_SYSTEM_PROMPT`, `orchestration/loop.py`): veto-only, StrictBool; a concern blocks only if
  it cites evidence fields.

## 11. Authority boundaries: done and tested (but never tested under pressure)

- The LLM may only return MORE_EVIDENCE with one menu primitive, or stop. A proposed ACCEPT or REJECT is an authority
  violation: it is not executed and is fed back.
- Experiments are validated; invalid, duplicate or over-budget proposals are rejected with feedback.
- Budgets: 6 experiments, 12 planner calls, 12× root compute, 3 invalid actions.
- No shell access. The final verdict always comes from the deterministic verifier.
- Tests: `tests/test_loop_authority.py`.
- Outcome: 0 authority violations and 0 planner failures in the 57 adaptive results with the LLM planner; all 195
  recorded planner decisions were MORE_EVIDENCE, so the boundary was never challenged.

## 12. Provenance: done, with gaps

Every run records:
- configuration and content hash;
- parent run, reason, requesting planner, experiment, config diff and initialisation;
- software versions and source git commit (with a dirty flag);
- commands, wall time;
- SHA-256 of logs, postProcessing outputs and final fields (R19);
- extractor fingerprint.

Every benchmark result is stamped with:
- the decision-code fingerprint, final value **`6406c53bb2011ef5`** (covers `checks/`, `critic/`, `evidence/`,
  `case_generation/`, `experiments/`, `openfoam/parsers.py`, `orchestration/{loop,systems,store}.py` and the three
  configs; recomputed from the working tree on 2026-10-20: unchanged);
- the evidence digest of every run it used;
- the benchmark git commit and a dirty flag.

Final state: 153/153 benchmark results carry `6406c53bb2011ef5` with `benchmark_src_dirty = false`. Gaps: the 21 attack
results carry no stamp (covered only by the replay, see "Integrity checks"); 14 roots created before R19 (commit
1df98b8, 10-19 08:20), the baseline and the A1, B1, B2, F1 roots among them, hash only their logs; 15 of the 17
benchmark roots were generated from an uncommitted source tree (`socrates_src_dirty = true`), so their recorded commit
does not pin the generating code (the generated case directories are stored); 7 orphaned 'running' records have no
hashes.

## 13. Evidence graph: done

`reporting/report.py` writes `reports/cases/<case>__<system>.md` (97 files): per-iteration decisions, experiments and
parent → child observations. Observation lines there are relative to the parent run; verifier sensitivity changes are
relative to the finer member, so the same experiment shows two different percentages (stated at the top of
`reports/benchmark_tables.md`).

## 14. Final report: done

`reports/final_report.md` (final, 2026-10-20) answers the 13 questions and evaluates the 5 pre-registered success
criteria (`docs/design.md` §19), with deviations, threats to validity, responses to the hostile review, integrity
checks and a glossary. Supporting reports: `reports/baseline_validation.md`, `reports/benchmark_results.md`
(generated by `scripts/make_reports.py`), `reports/benchmark_tables.md` (generated by `scripts/analyze_benchmark.py`).

## 15. Benchmark evaluation: done

- Pre-registered protocol: `docs/design.md`, "Pre-registered evaluation protocol" and §19 (commit dd548bc).
- Labels (`orchestration/truth.py::label_case`): e = |reported − T|/T.
  - flawed: e > τ, a requested quantity is missing, or the set-up solves another problem (narrow reading: wrong Re,
    steady formulation);
  - credible: e ≤ τ/2;
  - ambiguous: otherwise;
  - with the mitigation, also ambiguous when [e − U(T), e + U(T)] straddles τ or τ/2, unless the case is flawed for
    every T in the interval.
- Both label views are reported with equal weight; which is primary is contested (§19 is the point-estimate rule;
  the mitigation comes from the pre-registered risk list, made concrete in R18 after some verdicts). Three readings of
  the set-up clause are reported; on the benchmark only E1 changes (flawed under the set-up reading).
- Analysis (`scripts/analyze_benchmark.py` → `benchmark/labels.json`, `results/benchmark/metrics.json`,
  `reports/benchmark_tables.md`, `reports/figures/*.png`; final run 2026-10-20 19:12 UTC):
  - Root per case: the content-addressed run of the manifest definition.
  - Stale results (other decision code, other root, evidence changed) are listed and not counted: 0 in the final run.
  - ERROR results are excluded from rate denominators: 0 in the final run.
  - Ambiguous cases get neutral, unscored outcome classes.
  - Rates per label, false acceptance first; calibration table; per-quantity accuracy; LLM-variance table;
    criterion 5b and its sensitivity analysis; attack labels in three readings.
- `scripts/make_reports.py` assembles `reports/benchmark_results.md`.

## 16. Compare the systems: done

| system | definition |
|---|---|
| A | OpenFOAM diagnostics only: completed, checkMesh (`-allGeometry -allTopology`) OK, steady residualControl met |
| B | static deterministic verifier on the single run |
| L-judge | an LLM judges the static evidence only: no checks, no verdict, no experiments |
| C-llm (**System C** of §19) | adaptive: verifier + LLM planner + primitives; C-llm-r2 and C-llm-r3 are independent repeats |
| C-rule | adaptive with the rule planner (averaging/statistics → mesh → time → domain), plus two RUN_LONGER rules added after the first results (unreliable member, 1df98b8; INCONCLUSIVE physics_regime, 10f8b80) |
| C-rule-prereg | C-rule without those two rules, as §19 specifies it (`scripts/run_rule_prereg.py`; 5b sensitivity analysis) |
| Bexh | fixed protocol of 5 experiments (RUN_LONGER, REFINE_MESH √2 twice, REDUCE_TIME_STEP, EXPAND_DOMAIN), then verify; no compute cap |

Final verdicts (ACC/REJ/INC; `reports/benchmark_tables.md`, result files):

| case | label (point / mitig.) | A | B | L-judge | C-rule | C-rule-prereg | C-llm | C-llm-r2 | C-llm-r3 | Bexh |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | cred / amb | ACC | INC | ACC | INC | INC | INC | INC | **ACC** | INC |
| K1 | amb / amb | ACC | INC | ACC | INC | INC | INC | INC | INC | INC |
| K2 | cred / amb | ACC | INC | ACC | INC | INC | INC | **ACC** | INC | INC |
| A1 | fla / fla | ACC ✗✗ | INC | REJ | REJ | REJ | REJ | REJ | REJ | REJ |
| A2 | cred / amb | ACC | INC | ACC | INC | INC | INC | INC | INC | INC |
| B1 | fla / fla | ACC ✗✗ | INC | REJ | REJ | REJ | REJ | REJ | REJ | REJ |
| B2 | fla / fla | ACC ✗✗ | INC | REJ | REJ | REJ | REJ | REJ | REJ | INC |
| C1 | cred / amb | ACC | INC | ACC | INC | INC | INC | INC | INC | INC |
| C2 | fla / amb | ACC (✗✗ point) | INC | INC | INC | INC | INC | INC | INC | INC |
| D1 | fla / fla | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ |
| E1 | amb / amb | ACC | INC | ACC | INC | INC | INC | INC | INC | INC |
| F1 | fla / fla | ACC ✗✗ | INC | REJ | REJ | INC | REJ | REJ | REJ | REJ |
| G1 | amb / amb | ACC | INC | REJ | INC | INC | INC | INC | INC | INC |
| G2 | amb / amb | ACC | INC | ACC | INC | INC | INC | INC | INC | INC |
| H1 | fla / fla | ACC ✗✗ | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ |
| I1 | fla / fla | ACC ✗✗ | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ |
| J1 | cred / amb | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ | REJ |

✗✗ = false acceptance. Every J1 REJECT is a false rejection on point estimates (unscored with the mitigation).

Rates (case level; point-estimate view unless stated):

| system | false acceptance (mitig. / point) | detection (mitig. / point) | correct acceptance (point, of 5) | INCONCLUSIVE |
|---|---|---|---|---|
| A | **6/7 / 7/8** | 1/7 / 1/8 | 4/5 | 0/17 |
| B | 0/7 / 0/8 | 3/7 / 3/8 | 0/5 | 13/17 |
| L-judge | 0/7 / 0/8 | 7/7 / 7/8 | 4/5 | 1/17 |
| C-rule | 0/7 / 0/8 | 7/7 / 7/8 | 0/5 | 9/17 |
| C-rule-prereg | 0/7 / 0/8 | 6/7 / 6/8 | 0/5 | 10/17 |
| C-llm | 0/7 / 0/8 | 7/7 / 7/8 | 0/5 | 9/17 |
| C-llm-r2 | 0/7 / 0/8 | 7/7 / 7/8 | 1/5 (K2) | 8/17 |
| C-llm-r3 | 0/7 / 0/8 | 7/7 / 7/8 | 1/5 (baseline) | 8/17 |
| Bexh | 0/7 / 0/8 | 6/7 / 6/8 | 0/5 | 10/17 |

Bounds: 0/7 → upper 0.348; 0/8 → 0.312; 7/7 → lower 0.652; 0/5 → upper 0.451; 1/5 → upper 0.657. With the
mitigation no case is credible, so correct acceptance and false rejection are undefined in that view.

Cost (`reports/final_report.md` Q9; × root = experiment cell-steps divided by the root run's cell-steps):

| system | experiments | mean extra compute (× root) | range | LLM fees |
|---|---|---|---|---|
| C-rule | 59 | 4.78 | 0–11.42 | — |
| C-rule-prereg | 55 | 5.32 | 0–11.94 | — |
| C-llm | 52 | 4.89 | 0–11.95 | USD 5.13 |
| C-llm-r2 | 55 | 4.81 | 0–10.77 | USD 5.30 |
| C-llm-r3 | 51 | 4.69 | 0–10.36 | USD 5.03 |
| Bexh | 82 | 7.31 | 2.53–24.41 | — |

L-judge cost USD 0.54 on the benchmark. Wall time is contaminated by CPU oversubscription; do not use it for cost.

## 17. Repository: done

See the map in `README.md`. Top level: `benchmark/`, `cases/`, `configs/`, `docker/`, `docs/`, `references/`,
`reports/`, `results/` (runs, benchmark, attacks, baseline, posthoc, analysis, reproducibility, logs), `scripts/`,
`src/`, `tests/`. Generated meshes and fields are gitignored; the case dictionaries, evidence, series and provenance
are committed. `results/benchmark/*/<case>.partial.json` are loop checkpoints; the result is `<case>.json`. The
`results/*.log` files at the top of `results/` are early batch logs; the current logs are in `results/logs/`.

## 18. Reproducibility: done (narrow)

- `docker/Dockerfile` pins the OpenFOAM package; Python packages are pinned in `requirements.lock`.
- `docs/methodology.md` §9: the A1 root was re-run from scratch in the container and reproduced bitwise (same run id,
  Cd, St and Cl rms identical to all digits; `results/reproducibility/docker_A1_comparison.txt`).
- Single-core runs are deterministic. That is 1 of 214 runs reproduced; no child run was reproduced.
- See "Integrity checks" below for the replay, run audit and untraced-number checks.

## 19. Testing: done

`pytest -q` collects 99 of 107 tests and runs the 99 unit tests (83 test functions, some parametrised); all 99
passed when re-run on 2026-10-20 at 20:40 UTC (1.4 s). `pytest -m openfoam` runs the 8 integration tests (5 functions
in `tests/test_integration_openfoam.py`) that need OpenFOAM; `pyproject.toml` deselects them by default; they were not
re-run at the end. Fixtures come from real v2412 output. Coverage:
- parsers, signals, every check's status logic and the missing-evidence rule;
- the Richardson/Celik mathematics and regression cases from the reviews;
- case generation, primitives and limits;
- critic blindness and the numeric audit;
- loop authority, outage classification and result staleness;
- with OpenFOAM: root-run provenance and caching, every primitive, orphan adoption and restart cost.

The tests establish that the code does what it says, not that any simulation is physically right.

## 20. Development phases

| phase | status |
|---|---|
| 0 research, 1 design (incl. pre-registration) | done (`docs/research.md`, `docs/design.md`) |
| 2 baseline | done; four study stages; `reports/baseline_validation.md` final |
| 3 evidence, 4 verifier, 5 cases, 6 static test, 7 primitives, 8 critic and loop | done |
| 9 benchmark, attacks, ablations, post-hoc analyses | done (last result 2026-10-20 19:11 UTC) |
| final deliverables | done (§40) |

## 21. Explicitly out of scope

Unchanged from the specification: no UI, no multi-solver support, no cloud platform, no turbulence, no 3D. The README
states that this is a single-benchmark research prototype.

## 22. Primary success criterion (criterion 3): met

B1 (small domain) under C-llm:
- the solver completes;
- A ACCEPTs, and B is INCONCLUSIVE with no failed checks;
- the LLM critic chose EXPAND_DOMAIN ×2 as its first and only experiment (0.78× root compute);
- Cd changed by 8.86 % and St by 6.65 % (relative to the finer member), so domain sensitivity FAILs and the verdict
  is REJECT.

A1, B1, B2 and F1 each meet every condition under C-llm (0.78–4.80× root, USD 0.05–0.13 each), and all four are
flawed in both views. Caveats: thin margins on A1 under C-rule (0.24 points) and B2 (3.39 % − 2 × 0.081 % noise = 3.23 %,
0.23 points, from an 80 D/U ×4 member with a coarse far field; B2's label is robust at 4.24 % ± 0.94 %); why F1's first
experiment did not decide survives only in planner text (per-iteration checks are not stored).

## 23. Scientific development rules: followed, with documented deviations

- Every threshold has a source in `configs/verification.yaml`.
- Every methodological correction is logged in `docs/methodology.md` §7: 52 in total, 46 from adversarial reviews and
  6 found during development:
  - R1–R25: two adversarial code-review rounds;
  - R26–R35: the fix-verification round;
  - E1–E11: the evaluation-pipeline review (E1–E10 before any number was reported; E11, the verdict replay, added on
    10-20).
- The decision code changed after some early verdicts were known; all reported benchmark results carry the final
  fingerprint (see "Deviations from pre-registration").
- Observations logged without changing the pre-registered verifier: J1's `-allGeometry` determinant failure, the
  unclearable regime gate, diverged refinements reported as "not run", far-field coarsening (`docs/methodology.md` §8,
  "Observations").

## 24–25. Autonomous execution and decision authority

Continue without approval. Design decisions are logged in `docs/design.md` (decision log).

Rule: **do not edit any fingerprinted file (§12) unless you intend to recompute every benchmark result.** A changed
fingerprint makes every stored benchmark result stale; the next `run_benchmark.py` invocation recomputes them, LLM
calls included (fees, and different LLM verdict paths because the LLM is not deterministic). Evaluation-only code can
be changed freely: `scripts/`, `orchestration/{truth,evaluation}.py`, `reporting/`. A real bug in the decision code
should still be fixed, followed by a full recompute and a new replay.

## 26–34. Phases 0–8

Done; see sections 1–13 and `docs/methodology.md`. Reviews were run in-project as multi-agent adversarial workflows;
their findings were verified individually before fixing. No outside CFD expert has reviewed the work.

## 35. Autonomous verification loop: done

`orchestration/loop.py::run_adaptive`:
1. verify the current graph;
2. if the deterministic verdict is ACCEPT or REJECT, stop;
3. otherwise ask the planner for one primitive and validate it (unknown parent, validator, duplicate, budget);
4. execute it through the run store and repeat.

With `acceptance_review=True`, a deterministic ACCEPT is first shown to an LLM reviewer, which may only downgrade it
to INCONCLUSIVE. `LoopResult` records the history, experiments, cost, authority violations, `n_planner_failures` and
`n_invalid_events`. Per-iteration verifier checks are not stored (only the final verdict and the planner's text).

## 36. Phase 9: benchmark (complete)

- All 9 systems have 17/17 current, non-error results, stamped `6406c53bb2011ef5` (153 results). No owner process is
  alive (run audit, 19:12 UTC).
- Launch history (from `results/logs/` and git): main benchmark and attacks from 10-19 09:08; two container restarts
  (10-20 01:15, 03:41) killed in-flight runs and required relaunches; Bexh relaunched 06:49; C-llm-r2 07:50;
  C-rule-prereg 12:53; the post-hoc J1 adaptive variant 12:57; C-llm-r3 14:11.
- The scripts are resumable: completed runs and current results are reused; stale or ERROR results are recomputed.
- `reports/baseline_validation.md` is final (stage 4 reference; three fact-checks).

## 37. Attack your own system: complete

Systems (`scripts/run_attacks.py`, results in `results/attacks/<system>/`):
- B-v1, C-rule-v1, C-llm-v1: the pre-registered verifier;
- C-llm-v1+review: the same, with the LLM acceptance review;
- B-v2, C-rule-v2: verifier v2, adding geometry consistency (measured cylinder diameter from the patch bounding
  box) and inlet uniformity (written after the attacks were defined, before any ran: not a blind test);
- L-judge.

| attack | B-v1 | C-rule-v1 | C-llm-v1 | C-llm-v1+review | L-judge | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|
| X1 cylinder +5 % | INC | INC (5 exp., 6.63×; St ACCEPTed, error −3.60 %) | INC (6 exp., 8.04×) | INC (6 exp., 7.95×) | REJ | REJ | REJ |
| X2 sheared inlet | INC | INC (6 exp., 7.65×) | INC (6 exp., 8.97×) | INC (6 exp., 8.97×) | REJ | REJ | REJ |
| X3 compensating errors | INC | REJ (mesh FAIL on St, 4.36 %; 3.21×) | REJ (domain FAIL, Cd 5.14 %, St 3.83 %; 0.77×) | REJ | REJ | INC | REJ |

- No attack result is a case-level ACCEPT. The one quantity-level false ACCEPT is X1 St under C-rule-v1 (U 1.62 %:
  mesh 1.35 %, time 0.33 %, domain 0.84 %, against a true error of −3.60 %).
- **Near miss:** on X1 the v1 adaptive systems were held back only by domain components 0.42–0.60 points above
  their 1.5 % limit (the larger excess per system) — safety by conservatism, not detection.
- X2's v2 and L-judge REJECTs are correct only under the set-up reading; under the narrow reading on point estimates
  they are false rejections (unscored under the literal reading and with the mitigation).
- X3's St REJECTs land on the accurate quantity (St +0.16 %); the wrong quantity, Cd, stays INCONCLUSIVE under
  C-rule-v1 and -v2. The case verdict is right, the quantity verdict is not.
- The review was never invoked on a stored result (no deterministic ACCEPT reached it).
- Benchmark extensions (`--benchmark-extensions`): B-v2 on the 17 benchmark roots changes 0 verdicts (0/17, bound
  0.162; only tests the tolerances, as no root departs from the specified geometry or inlet);
  `results/attacks/review-on-benchmark/` has nothing to review (no ACCEPT in the first C-llm run).

## 38. Ablation tests: complete

| ablation | result |
|---|---|
| C-rule vs C-llm (criterion 5b) | identical verdicts on 17/17 cases; LLM 83.06 vs 81.29 root-units, sign test p = 0.109, USD 5.13: **not met** |
| C-rule-prereg (sensitivity) | C-rule's verdict on 16/17; F1 INCONCLUSIVE (5 exp., 11.40×); against it 5b is met on accuracy by F1 only (7 vs 6 correct), not on cost (p = 0.549) |
| Bexh | C's verdicts on 16/17; misses B2 (one domain step, two-level estimate with Fs = 3, U 14.23 %); no compute cap (up to 24.41× on G1); runs its protocol after static REJECTs (5.11–6.51× on D1, H1, I1, J1) |
| L-judge | detection 7/7, false acceptance 0/7 on the benchmark; correct acceptance 4/5 on point estimates (REJECTs J1); 3 ACCEPTs with errors between τ/2 and τ (K1, E1, G2); no numerical bound |
| acceptance review | never invoked on stored results; post-hoc tests in §39 item 8 |
| LLM run-to-run variance | 3 complete runs: same verdict in 15/17 (lower bound 0.674); the 2 disagreements are the 2 ACCEPTs; same experiment sequence in 6/17 |
| post-hoc J1 `-allGeometry` variant | static on all 17 cases: only J1 changes (REJECT → INCONCLUSIVE); adaptive (C-rule-allgeo): INCONCLUSIVE after 5 experiments, 6.54× (St mesh 2.17 %, domain Cd 1.64 %, St 2.28 %): false rejection removed, no acceptance |
| post-hoc acceptance-rule variants | V0 2 ACCEPTs (both correct); V1 18 (14 correct of 41 credible-case results, 3 false: X1 in every v1 adaptive system); V2 10 (7/41 correct, the same 3 false) |

## 39. Scientific falsification: final findings

Consistent with `reports/final_report.md` (read it for sources and caveats):

1. **OpenFOAM diagnostics (A) falsely accept 6 of the 7 robustly flawed cases** (7 of 8 on point estimates); their one
   detection is D1. The rate reflects how the cases were built (plausible cases that run), not real-world use.
2. **The static verifier (B) never falsely accepts** and adds REJECTs of H1 and I1 (set-up consistency checks, written
   by the same author minutes before the cases), but it accepts nothing (13/17 INCONCLUSIVE).
3. **Adaptivity adds REJECTs of A1, B1, B2 and F1** (0.78–6.94× root), detection 3/7 → 7/7; most compute (78 % of
   C-rule's, 89 % of C-llm's) goes to the 9 mitigation-ambiguous cases that end INCONCLUSIVE. Over the fixed protocol
   Bexh it adds only B2 in the scored comparison (0.23-point margin); on the 11 comparable cases the three cost the
   same within 4 %. That adaptivity beats a fixed protocol is weakly supported.
4. **Exactly 2 case-level ACCEPTs by any verifier-based system**, both correct on point estimates (true errors within
   the stated U) and both unscored (ambiguous) with the mitigation:
   - C-llm-r2 on K2: Cd U 1.54 % vs +0.94 %, St U 1.69 % vs −0.07 %; 5 experiments, 5.37×, USD 0.45.
   - C-llm-r3 on the baseline: Cd U 1.87 % vs +1.20 %, St U 1.59 % vs −0.31 %; 5 experiments, 7.12× (all runs already
     in the store), USD 0.42.
   - No ACCEPT by C-llm (first run), C-rule, C-rule-prereg, Bexh or B. Each case was accepted in 1 of 3 LLM runs:
     not reproducible. 2/35 verifier-based benchmark results on point-estimate-credible cases (bounds 0.010–0.169);
     pooled LLM runs 2/15 (bounds 0.024–0.363). These results share cases and stored runs, so they are not
     independent trials.
5. **Why acceptance depends on the planner:** the Cd domain component's observed order, and with it the Celik safety
   factor, differs between runs of the same case, depending on which domain levels were run and how far they had
   settled. K2 Cd orders: C-rule 1.51 (Fs 1.25, U 1.02 % PASS; C-rule was blocked instead by a two-level mesh estimate
   because its next mesh step needed 216,220 cells > 160,000), C-llm 2.79 (outside the band: Fs 3, U 2.38 %), C-llm-r2
   1.06 (U 1.27 %, ACCEPT), C-llm-r3 7.66 (Fs 3, U 1.87 %). Baseline: orders 0.82–0.94 in the non-accepting runs
   (U 1.74–1.88 %) against 1.55 in C-llm-r3 (U 1.23 %, ACCEPT), all with Fs = 1.25. With settled members both ACCEPTs
   disappear (baseline 1.97 %; K2 2.61 %). It is not "accepting runs avoid large levels": C-llm-r2's K2 chain reached
   ×3.
6. **No case-level false acceptance** by any verifier-based system on the benchmark or the attacks, in any view or
   reading; one quantity-level false acceptance (X1 St under C-rule-v1). Weak evidence: 0/7 and 0/8 allow true rates
   up to 0.348 and 0.312; pooling C-llm with C-llm-v1 gives 0/9–0/12 (bounds 0.283–0.221), still optimistic.
7. **Criterion 5b: not met under the committed decision rule** (`docs/methodology.md` §8, commit 3ee09b1; C-llm first
   run against C-rule): tied accuracy, higher compute, p = 0.109. As §19 requires: the LLM planner adds no measurable
   value on this benchmark. The sensitivity analysis against C-rule-prereg meets 5b on accuracy by one case, F1, which
   C-rule-prereg leaves INCONCLUSIVE because, without the post-hoc unreliable-member RUN_LONGER rule, its mesh study
   on F1 never gets a statistically reliable member; that "win" exposes a gap in the rule planner that one
   deterministic rule closes (inferred: that rule alone was not run). The repeats' two correct ACCEPTs are a separate,
   descriptive advantage from parameter and level choices, not reproducible; had either repeat been scored, the
   accuracy leg would have been met (8 vs 7 on point estimates).
8. **The LLM acceptance review is no safety gate** (post-hoc tests, `scripts/posthoc_review_tests.py`,
   `results/posthoc/review-on-accepts/`, 4 calls, USD 0.48): it concurs with both real ACCEPTs; on a counterfactual X1
   ACCEPT it concurs on the C-llm-v1 graph (its package, stored with sha256, contains the measured extent 0.0105 m
   12 times; it wrote "D is 0.01 m … No recorded field shows a mismatch") and vetoes on the C-rule-v1 graph for
   numerical reasons, not geometry: 0 of 2 geometry detections (bound 0.776).
9. **Wrong-problem errors (X1, X2) are invisible to solution verification**; only the post-hoc v2 checks and L-judge
   catch them. v2 changes 0 verdicts on the 17 benchmark cases and rejects X1 and X2 under every acceptance-rule
   variant; V1 and V2 would each accept X1 in all three v1 adaptive systems.
10. **Calibration** (benchmark, each distinct run graph once, repeats included): U covers the error in 64/66 quantity
    rows (lower bound 0.908; rows not independent). The 2 misses are set-up errors that U does not estimate by
    construction, in cases REJECTed statically: Bexh H1 St (6.05 % vs U 3.01 %; H1 solves Re = 83.3) and Bexh I1 Cd
    (11.05 % vs 4.21 %; wrong force normalisation). Attacks: 4/10 covered (all misses X1). U and T share machinery and
    runs, so this is not independent.
11. **J1 is a false rejection on point estimates** (Cd +0.56 %, St −1.11 %), REJECTed by every system for 48 stretched
    cells at about 47 D next to the outlet that only `checkMesh -allGeometry` flags; default checkMesh says "Mesh OK".
12. **L-judge** (USD 0.54) matches the adaptive systems' detection without simulations, but gives no bound, accepts
    three cases with errors between τ/2 and τ, and accepted E1 after noting its walls do not match "unbounded".
13. **Untraced numbers in LLM text:** 251 of 9,757 audited numbers (2.6 %); 205 come from the 15:31 UTC snapshot
    (classified at 15:44: 180 derived arithmetic, 15 restated threshold or convention, 9 rounded package values,
    1 unclear), and the 46 new tokens (all C-llm-r3) are all derived arithmetic. Totals: 226 derived, 15 conventions, 9 rounded, 1 unclear (a
    wrong number: C-llm-r2 on C2 wrote 0.42 % for a 0.37 % Cd change), 0 possible external knowledge (0 of 93 calls,
    bound 0.032). The audit cannot exclude remembered values that equal package values.

## 40. Final deliverables: checklist

| deliverable | status |
|---|---|
| `README.md` | revised in the final pass (status note, terms, headline results; in the working tree after 3e18205): check it against the final report before committing |
| `docs/research.md`, `docs/design.md` | done (§20 status table updated) |
| `docs/methodology.md` | done (corrections R1–R35, E1–E11; 5b decision rule and results; observations; integrity tools) |
| baseline case, adversarial cases, attack cases | done |
| evidence extraction, verifier, experiment engine, critic, loop | done |
| benchmark manifest, tests | done |
| raw results | `results/` (final) |
| plots/tables comparing the systems | `reports/benchmark_tables.md`, `reports/figures/*.png` (19:12 UTC) |
| `reports/baseline_validation.md` | final |
| `reports/benchmark_results.md` | final (19:12 UTC) |
| `reports/final_report.md` | final (13 questions, 5 success criteria) |
| `reports/status_brief.html`, `.pdf` | **stale** (10-19 17:36; e.g. it predates both ACCEPTs and the final 5b outcome): regenerate or delete |

Success criteria (§19), as rated in the final report: C1 infrastructure and provenance **partly met**; C2 baseline
credibility **partly met** (2a met; 2b not met on the full-study graph, met on one non-reproducing benchmark graph);
C3 primary demonstration **met**; C4 System C false acceptance = 0 **met on the observed data, weakly**; C5a **met**;
C5b **not met** under the committed rule (met by one case in the sensitivity analysis).

## 41–42. Continuation rule and final principle

Do not stop because a phase is done or something failed: inspect → diagnose → fix → rerun. Do not protect the
hypothesis. Negative results are valid. Report false acceptances first.

---

## Deviations from pre-registration

Pre-registration = `docs/design.md` §19 as committed in dd548bc (10-19 07:13 UTC). Full list:
`reports/final_report.md` ("Deviations…") and `docs/methodology.md` §6.

1. **Timeline.** First roots 07:00–07:02, protocol committed 07:13; of ten decision-code commits up to 09:06, one
   (07:18) fixed the averaging check after it had passed G1, and six (07:35–09:06) followed the first committed
   verdicts (07:30). Early results were discarded; all benchmark results carry the final fingerprint.
2. **Rule planner.** Two RUN_LONGER rules were added after the first results (08:20, 08:59), so C-rule is not exactly
   the pre-registered ablation; C-rule-prereg (launched 10-20 12:53) runs it as specified.
3. **Reference T** was built differently from §19, in four committed versions (11:03–16:43), after the A, B, L-judge
   and some C results. The flawed sets are unchanged under every version, so false-acceptance and detection rates
   are robust; point-estimate correct-acceptance and false-rejection rates are not.
4. **Labels.** The mitigation was made concrete at 08:24, after some verdicts; the set-up clause is read narrowly;
   both views and three readings are reported.
5. **The 5b decision rule** was fixed after 15 of 17 C-llm results (10-20 09:17), before C-llm's K1 and K2 results and
   any analysis of the repeats.
6. **v2 checks and the review** were committed at 07:40, after the attacks were defined and before any ran; not blind.
7. **Post-hoc analyses** (J1 variant, V0/V1/V2, review tests, v2 and the review on the benchmark roots, calibration,
   C-rule-prereg) do not touch scored rates.
8. **Mapped-child duration** was cut from 100 to 80 D/U (07:23, before the first child run); these unsettled members
   lie behind B2's margin, every adaptive domain U and both ACCEPTs.
9. **Systems added by hand:** C-llm-r2 (10-20 07:50), C-rule-prereg (12:53), C-llm-r3 (14:11); the repeats never enter
   the 5b comparison or System C's scored rates.

## Integrity checks

None of these changes a result. Final outputs were written at about 19:12 UTC on 2026-10-20, after the last result
(19:11) and with no live owner process.

| check | tool | coverage | result |
|---|---|---|---|
| decision-code stamp | result stamps | 153/153 benchmark results; 0/21 attack results | all `6406c53bb2011ef5`, clean tree |
| strict replay: verdict, failed checks, every component status and U | `scripts/replay_verdicts.py` → `results/analysis/replay.json` | 137 = B, C-rule, C-rule-prereg, C-llm, C-llm-r2, C-llm-r3, Bexh (17 each) + 18 attack results; A and L-judge have no verifier verdict | 137/137 match |
| post-hoc V0 re-run | `scripts/posthoc_acceptance_rule.py` | the same 137 | 137/137 match |
| run audit | `scripts/audit_runs.py` → `results/analysis/run_audit.{md,json}` | 214 records | 198 completed, 9 failed (all floating-point exceptions), 7 'running' (all orphaned), 11 named by no stored result |
| untraced numbers | `scripts/dump_untraced.py`, then classified by reading (`results/analysis/untraced_classification.{md,json}`) | 9,757 audited numbers in stored LLM text | 251 untraced, all classified (§39 item 13); the stored untraced lists reproduce for all 178 rebuilt calls |
| container reproduction | `results/reproducibility/` | A1 root | identical |
| software tests | `pytest -q` | 99 unit tests | 99 passed (20:40 UTC); 8 integration tests not re-run |

Run-audit details worth knowing: at least 96 earlier attempts were erased by the store (they appear only in
committed run.json versions); 15 superseded LLM loop attempts recorded at least USD 2.64 over 38 planner iterations
that no current result holds; 10 runs launched by the LLM planner are named by no result (7 of them orphaned 'running'
records), holding 2.25 × 10⁹ cell-steps (2.1 % of the store's recorded cell-steps); one orphan's 764 s of solver time
is recorded only in its log.

## Open problems and recommended next steps

Open problems (`reports/final_report.md` Q7):
1. **Acceptance depends on the planner's choice of levels** (§39 item 5): not reproducible and steerable.
2. **Wrong-problem errors** (X1, X2) are invisible to the pre-registered verifier; X1 was held back from a case-level
   false ACCEPT only by domain components 0.42–0.60 points above their limit.
3. **Two defective primitives** (far-field coarsening in EXPAND_DOMAIN; REFINE_MESH divergence on Courant > 1 parents,
   hidden as "not run").
4. **J1 false rejection** from a mesh heuristic applied to roots only (children with the same flag still count,
   including members of both accepting chains).
5. **An unclearable gate:** physics_regime must pass before any ACCEPT but is evaluated on the root only; the late
   rule-planner rule (10f8b80) chases it with continuations (13 on F1, G1 and G2; 16 % of C-rule's experiment
   compute).
6. **Record-keeping gaps:** per-iteration checks are not stored; the store erases abandoned attempts; orphaned
   'running' records; unstamped attack results; 14 roots without R19 hashes.
7. **Small, non-independent n:** one geometry, one Re, one author for cases, checks and attacks, cases built to run.

Recommended next steps (`reports/final_report.md` Q12; items 3 and 4 make acceptance easier and ship only behind
item 1; item 2 makes it harder):
1. **Deterministic set-up consistency checks (v2) as a mandatory gate** (geometry, inlet profile, boundary-condition
   types, force reference, fluid properties against the problem statement; FAIL on mismatch). Only the geometry and
   inlet checks are new (v2); force reference and Re are already checked in v1 (I1, H1); a boundary-condition-type
   check (which E1 would fail) is not yet written. C-rule-v2 was not run on the benchmark. First settle the reading of
   the set-up clause, under whose narrow reading the X2 REJECT is a false rejection.
2. **Acceptance independent of the planner's level choices:** a minimum extent for the largest domain member,
   settled members, and the most conservative estimate over all available three-member sub-chains.
3. **An EXPAND_DOMAIN that keeps far-field resolution**, with 100–150 D/U of settling.
4. **A REFINE_MESH that scales Δt to hold the Courant number**, records failures as evidence and never launches a
   child of a failed run.
5. **A held-out evaluation set:** robustly credible cases (Cd error < 0.565 %, St < 1.04 %), flaws written blind by
   someone else, attacks with a clean configuration or one wrong quantity, an independent reference.
6. **A pre-registered acceptance rule tested on item 5** and shipped with items 1–2 (V1 and V2 both accept X1).
7. **A discharge for the regime gate, one mesh-quality rule for roots and children, and the unreliable-member
   RUN_LONGER rule in any rule planner.**
8. **Integrity plumbing:** store per-iteration checks and each LLM call's package; stamp attack results; mark
   orphaned records failed; account for aborted loops; re-hash or flag the pre-R19 roots; word the REFINE_MESH factor
   unambiguously.

Do **not** build next (Q13): LLM-issued verdicts; the LLM acceptance review as a safety gate; a planner tuned to reach
acceptance before acceptance stops depending on the planner; more geometries or Reynolds numbers before the primitives
are fixed; a fixed exhaustive protocol as the default; heuristics or relaxed rules tuned on this benchmark (J1,
V1/V2); platform features while there is no reproducible ACCEPT and no demand data.

Cheapest informative experiment not yet run: one EXPAND_DOMAIN ×1.5 of the X1 root (about 0.6× root) under v1, to
test whether the ×1, ×1.5, ×2 levels that accepted the baseline would also accept X1 (an inference in the final
report, untested).

## How to run everything

Environment (either):
- Container: `docker build -t socrates-cfd -f docker/Dockerfile .`, then run scripts inside it with `results/`
  mounted (see `README.md`; behind a TLS-intercepting proxy pass the CA as a build secret).
- Host (Ubuntu 24.04): install `openfoam2412=2412.260127-1`, then `pip install -r requirements.lock && pip install -e .`.

Set `SOCRATES_CPU_SLOTS` (default: the CPU count, 4 here) to the same value for every process that shares
`results/runs/`. Each OpenFOAM run is single-core and holds one slot. The LLM systems (C-llm*, L-judge, the review)
need the LLM command-line client that `critic/backends.py` invokes on PATH, with credentials; all deterministic
systems run without it.

Order of a full reproduction (every script is resumable and reuses completed runs from the content-addressed store):

```bash
pytest -q                                                      # 99 unit tests (pytest -m openfoam: 8 integration tests)
python scripts/run_root_cases.py cases/baseline/baseline.yaml cases/adversarial/*.yaml cases/variants/*.yaml
python scripts/baseline_study.py                               # stages 1-3 of the baseline study
python scripts/farfield_resolution_test.py                     # stage 4 (x4 far field); add --level x1 for the control
python scripts/make_baseline_report.py                         # truth.json, baseline_generated.md
python scripts/run_benchmark.py --systems A,B,L-judge,C-rule,C-llm,Bexh --workers 6
python scripts/run_benchmark.py --systems C-llm-r2,C-llm-r3    # LLM repeats
python scripts/run_rule_prereg.py                              # C-rule-prereg (5b sensitivity)
python scripts/run_attacks.py                                  # 7 attack systems x 3 attacks
python scripts/run_attacks.py --benchmark-extensions           # B-v2 and the review on the benchmark roots
python scripts/posthoc_allgeometry.py --adaptive               # J1 variant, static on 17 cases + adaptive on J1
python scripts/analyze_benchmark.py                            # labels, metrics, tables, figures
python scripts/make_reports.py                                 # reports/benchmark_results.md
python scripts/posthoc_acceptance_rule.py                      # V0/V1/V2
python scripts/posthoc_review_tests.py                         # rebuilds review packages; --call re-asks the LLM (fees)
python scripts/replay_verdicts.py                              # exit 1 on any mismatch
python scripts/audit_runs.py
python scripts/dump_untraced.py
python scripts/status.py                                       # progress overview at any time
```

Single cases: `socrates run-case <case.yaml>`, `socrates verify <run_id>`, `run_benchmark.py --cases id1,id2`.
After any new result: rerun `analyze_benchmark.py`, `make_reports.py`, `replay_verdicts.py`, `audit_runs.py` and
`dump_untraced.py` before quoting a number, and regenerate `posthoc_acceptance_rule.py` if graphs changed.
Commit result snapshots regularly (`git add -A results reports`).

## Pitfalls and gotchas

- **Container restarts and stale owner PIDs.** A restart kills every solver and launcher; records stay 'running'
  with the dead process's `owner_pid`. PID numbers restart low after a restart, and `RunStore._running_elsewhere`
  treats any live process with that PID as the owner, so a reused PID can make `get_or_run` wait indefinitely (it
  polls every 30 s). Recovery used here (8225c78, c0aadc9): with no launcher running, check each 'running' record's
  `owner_pid` against `ps`; if it is not the launcher that created the record, set `owner_pid` to null and record
  `"stale_owner_pid_cleared": {"old_owner_pid": <pid>, "reason": "container restart"}` in its `run.json`; then
  relaunch the same commands with the same `SOCRATES_CPU_SLOTS`, write a launch marker in the log, and commit a
  snapshot. Expect superseded loop attempts and their LLM fees to drop out of the results (15 superseded attempts
  over all relaunches here).
- **Run-store erasure of abandoned attempts.** `get_or_run` adopts an orphan only if its own solver log completed with
  the right `Case:` header and its final state was written; otherwise it deletes the directory and re-runs the
  configuration under the same run id, and `_execute` deletes any existing directory first. The earlier attempt then
  survives only in git history (`scripts/audit_runs.py`, "Earlier attempts in git history": 96 here). An aborted
  loop's planner calls and cost survive only in committed `*.partial.json` versions. Commit before relaunching if you
  need that history.
- **Failures are cached.** A run that failed in the solver or mesh step is returned as failed on every later request;
  re-requesting does not retry it. The verifier drops failed children silently (C1/C2: "no REFINE_MESH experiment has
  been run").
- **CPU slots.** Slots are fcntl locks `slot0 … slot{N−1}` in `results/runs/.slots`; a process with
  `SOCRATES_CPU_SLOTS=3` uses only slots 0–2, so mixing values reserves or over-commits cores. A solver whose Python
  owner died keeps running outside the slots, so load can exceed the core count for a while. `--workers` sets loop
  threads, not solver processes.
- **Kill only by PID.** `pkill -f` once killed the agent's own shell.
- **LLM backend.** The client must be on PATH with credentials, or `LLMUnavailable` is raised. Calls are
  nondeterministic (repeats gave 15/17 identical verdicts and 6/17 identical experiment sequences), cost about
  USD 0.09 and 28 s per planner call, and time out at 300 s with 3 attempts. A loop that stops only because every
  planner call failed is an infrastructure error (excluded from rates, recomputed on resume), not an INCONCLUSIVE.
  Model names are deliberately kept out of all artefacts; only a fingerprint is recorded.
- **Decision-code fingerprint and stamps.** Editing any fingerprinted file (§12), prompt text in `critic/` included,
  makes all 153 benchmark results stale; the next `run_benchmark.py` recomputes them, LLM calls included. A
  long-running process keeps the modules it loaded at start, so a result written after a commit is not proof it used
  that code: use `scripts/replay_verdicts.py`. Results are also stale when a root's evidence is re-extracted (evidence
  digests; the K1 incident, E3). Attack results carry no stamp at all; only the replay protects them. Stamps record a
  dirty flag: commit before launching.
- **Two percentage conventions.** Verifier sensitivity changes are relative to the finer member (A1 St 3.28 %); case
  reports and loop traces are relative to the parent (A1 St +3.39 %). Say which one you quote.
- **checkMesh** always exits 0: parse the log. Non-orthogonality > 70° is only a warning. Roots run
  `checkMesh -allGeometry -allTopology`, which is stricter than default checkMesh (J1).
- **solverInfo** records only the first p-solve: the last p-solve per step is parsed from the log.
- **OpenFOAM**:
  - `exprFixedValue` needs `valueExpr`.
  - A restart counts `writeInterval` from the restart time, so the writer uses the segment length.
  - forceCoeffs columns are read by header name (they are alphabetical in v2412).
- **Run names:** a child's name records only the step's own factor. The ×4 domain level is `baseline.D2x-4312…`; the
  domain continuations are `baseline.long180-…` (×2) and `baseline.long280-…` (×4). Domain levels are counted
  cumulatively (×1.5 applied to a ×2 run gives ×3).
- **Duplicate-looking runs:** two f = 2 baseline meshes exist. `baseline.m2-93c9ab8d6f2d` is mapped from the root
  (study and LLM); `baseline.m2-476115cbbf20` is mapped from √2 (the rule planner and Bexh). Different
  initialisation means a different run id.
- **Old-code runs:** roots finalized by older code lack an `extraction` fingerprint or R19 hashes; 15 benchmark roots
  were generated from a dirty tree. `evaluation.staleness` compares the root's evidence time with a loop's `started`
  time.
- **Shared-store accounting.** Each system's compute counts every run it used, including runs another system computed
  (C-llm-r3's baseline ACCEPT is charged 7.12× although all its runs existed); summing across systems double counts.
- **Wall-time metrics** are contaminated by oversubscription (two roots with identical cell-steps took 1,442 s and
  4,804 s). Use cell-steps for compute comparisons.
