# socrates-cfd — autonomous CFD verification (research prototype)

> **Status: final, 2026-10-20.** All simulations are complete (last result 19:11 UTC) and nothing is pending. The
> generated tables and analysis files were regenerated at about 19:12 UTC; the final report is
> [`reports/final_report.md`](reports/final_report.md). Every number below comes from that report or from the files
> it cites.

## What this is

**Question this repository answers empirically:** can an adaptive system that *requests additional simulations*
detect meaningful CFD failures that ordinary solver diagnostics and static (single-run) verification do not? And
does an LLM planner add anything over a deterministic one?

The loop is:

> problem → OpenFOAM simulation → deterministic evidence → checks → planner → validated experiment →
> new simulation → new evidence → verdict

The LLM is **never a source of numerical truth**:
- it sees only recorded evidence (an evidence package with opaque run names and no reference values);
- it can only pick one of four validated experiment primitives (RUN_LONGER, REFINE_MESH, REDUCE_TIME_STEP,
  EXPAND_DOMAIN);
- ACCEPT and REJECT come from the deterministic verifier alone;
- every number in its text is checked against its evidence package; numbers that cannot be traced are counted and
  reported (they are not blocked).

**Benchmark:** 2D laminar flow past a circular cylinder at Reynolds number Re = 100 (periodic vortex shedding). The
question is whether a finished simulation gives the mean drag coefficient **Cd** and the Strouhal number **St**
(dimensionless shedding frequency) to within **τ = 3 %**. There are 17 benchmark cases (the baseline and 16 variants,
each a documented change) and 3 attack cases (X1–X3, not pre-registered) built to try to make the verifier accept a
wrong answer.

### Terms used below

- *Verification* asks whether the equations were solved accurately enough (not whether they were the right
  equations). The **root run** is the simulation under verification.
- Verdicts: **ACCEPT** (every check passed and both quantities shown to be within τ), **REJECT** (a check failed),
  **INCONCLUSIVE** (safe but undecided). *False acceptance* = ACCEPT of a flawed case; *detection* = REJECT of one;
  *correct acceptance* / *false rejection* = ACCEPT / REJECT of a credible case. *Case-level* verdicts cover both
  quantities, *quantity-level* verdicts one.
- **U** is the verifier's estimated relative uncertainty of a quantity, built from components (statistics, mesh,
  time step, domain size) plus an averaging bias; an ACCEPT needs each component ≤ τ/2 = 1.5 % (the bias ≤ τ) and
  bias plus the root-sum-square of the components ≤ τ. Mesh, time and domain components come from Richardson
  extrapolation of runs at known ratios (Celik procedure), with a safety factor **Fs** = 1.25 when the observed order
  of convergence is within 0.5–2× the formal order, otherwise 3. A domain level ×k is a domain k times the root's
  half-height; time is in D/U, the time the stream takes to pass one diameter.
- **Labels** compare each case's error with an in-house reference T (Cd 1.3155 ± 0.94 %, St 0.1639 ± 0.46 %), in two
  views given equal weight. *Point-estimate view* (the pre-registered rule): 8 flawed, 5 credible (baseline, A2, C1,
  J1, K2), 4 ambiguous. *Mitigation view* (also ambiguous when the reference's own uncertainty straddles a limit):
  7 flawed, 0 credible, 10 ambiguous. *Robustly flawed* = flawed in both views (A1, B1, B2, D1, F1, H1, I1).
- **Systems:** **A** OpenFOAM's own diagnostics; **B** the static deterministic verifier on the root run; **L-judge**
  an LLM judging the evidence alone; **C-llm** (*System C*) the adaptive loop with the LLM planner, with independent
  repeats **C-llm-r2** and **C-llm-r3**; **C-rule** the same loop with a rule planner (two RUN_LONGER rules added after
  the first results); **C-rule-prereg** the rule planner exactly as pre-registered; **Bexh** a fixed protocol of five
  experiments with no compute cap. On the attacks, **v1** is the pre-registered verifier and **v2** adds two set-up
  checks (geometry, inlet) written after the attacks were defined.
- Bounds are one-sided 95 % Clopper–Pearson bounds: exact binomial limits on a true rate given k events in n trials
  (for 0/n the upper bound is 1 − 0.05^(1/n), e.g. 0.348 for n = 7).

## Headline results

**Bottom line.** As a *filter* for the flawed results planted here the system works on this benchmark; as a
*certifier* it works only sometimes, and not reproducibly. Details, caveats and sources:
[`reports/final_report.md`](reports/final_report.md) (Summary, Q1–Q13).

- **Filter.** C-rule and all three LLM runs REJECTed all 7 robustly flawed cases (7/7, lower bound 0.652). No
  verifier-based system made a case-level false acceptance in any of its 137 results (119 benchmark, 18 attack): per
  system 0/7 robustly flawed (upper bound 0.348), 0/8 flawed on point estimates (0.312), 0/2–0/3 attacks (0.776,
  0.632). OpenFOAM's diagnostics (A) falsely accepted 6/7 (7/8 on point estimates) and detected only D1 (steady
  solver). L-judge matched the 7/7 detection with no simulations (USD 0.54), but gives no numerical bound and three of
  its ACCEPTs have errors between τ/2 and τ.
- **One quantity-level false acceptance:** X1 (cylinder 5 % too large) St under C-rule-v1, true error −3.60 % against
  U 1.62 %. The case stayed INCONCLUSIVE.
- **Certifier.** Exactly two case-level ACCEPTs, both by LLM repeats: C-llm-r2 on K2 (Cd U 1.54 % vs true error
  +0.94 %; St U 1.69 % vs −0.07 %) and C-llm-r3 on the baseline (Cd U 1.87 % vs +1.20 %; St U 1.59 % vs −0.31 %).
  Both are correct on point estimates (U covers the true error); with the mitigation both cases are ambiguous, so
  both ACCEPTs are unscored there. That is 2 of the 35 verifier-based results on the 5 point-estimate-credible cases.
  The first C-llm run, C-rule, C-rule-prereg, B and Bexh accepted no case (C-llm 0/5, upper bound 0.451; the three
  LLM runs pooled 2/15, bounds 0.024–0.363, not independent).
- **Why acceptance depends on the planner.** The drag domain component depends on its observed order, which depends
  on which domain levels the planner ran and how far they had settled; the order sets the extrapolated error and,
  outside the band, switches Fs from 1.25 to 3. K2: order 1.06 in C-llm-r2 (U 1.27 %, ACCEPT); 1.51 under C-rule
  (U 1.02 %, PASS, but C-rule was blocked by a two-level St mesh estimate); 2.79 under C-llm and 7.66 under C-llm-r3
  (Fs 3, U 2.38 % and 1.87 %, INCONCLUSIVE). Baseline: 1.55 in C-llm-r3 (U 1.23 %, ACCEPT) against 0.82–0.94 in every
  other planner graph (U 1.74–1.88 %). Both ACCEPTs rest on an unsettled 80 D/U ×2 domain run; with that run's
  longer continuation in its place, the accepting chains give a drag domain U of 1.97 % and 2.61 %: INCONCLUSIVE.
- **Run-to-run variance** over the three complete LLM runs: identical verdict in 15/17 cases (lower bound 0.674); the
  two disagreements are exactly the two ACCEPTs (each accepted in 1 of 3 runs); identical experiment sequence in 6/17.
  Every robustly flawed case is REJECTed in all three runs; C2 (flawed on point estimates only) is INCONCLUSIVE in all
  three.
- **Does the LLM add value (criterion 5b)?** Under the committed decision rule (`docs/methodology.md`, commit
  3ee09b1: first C-llm run against C-rule) **not met**: identical verdicts on 17/17 cases (7 correct each in both
  views), 83.06 against 81.29 root-units of compute (+2.2 %), the LLM cheaper in 2 of 10 cases whose costs differ by
  more than 5 % (sign test p = 0.109), USD 5.13 in fees. As the pre-registration requires: **the LLM planner adds no
  measurable value on this benchmark.** Sensitivity analysis against the rule planner exactly as pre-registered
  (C-rule-prereg): 5b is met on accuracy by one case, F1 (7 against 6 correct in both views), not on cost (83.06 vs
  90.45, p = 0.549). C-rule-prereg leaves F1 INCONCLUSIVE because, without the unreliable-member RUN_LONGER rule added
  to C-rule after the first results, its mesh study never gets a statistically reliable member. That "win" exposes a
  gap in the rule planner that one deterministic rule closes, not an ability of the LLM. Had either repeat been the
  scored run, its ACCEPT would have met the accuracy leg (8 vs 7 on point estimates; 7 vs 7 with the mitigation), so
  the outcome also depends on which run is scored. The repeats' two correct ACCEPTs, from parameter and level choices
  the rule planner does not make, are a separate descriptive advantage that did not reproduce.
- **Adaptivity.** The adaptive systems turn B's INCONCLUSIVE into a correct REJECT on A1, B1, B2 and F1
  (0.78–6.94× the root run's compute). Over the fixed protocol Bexh the scored gain is one case: Bexh REJECTs every
  robustly flawed case except B2 (INCONCLUSIVE); the repeats' two unreproduced ACCEPTs are also beyond it. An
  adaptive REJECT costs 0.8–6.9× root, an INCONCLUSIVE 2.7–12.0×, the two ACCEPTs 5.37× and 7.12×.
- **Wrong-problem errors.** X1 and X2 (sheared inlet) are accurate solutions of the wrong problem: every v1 system
  leaves them INCONCLUSIVE with no failed check, and on X1 the v1 adaptive systems were held back only by domain
  components above their 1.5 % limit (by 0.42–0.60 points, the larger excess in each system). The v2 set-up checks
  REJECT X1 and X2 and change none of the 17 benchmark verdicts (0/17, upper bound 0.162), but they are post hoc.
  The LLM acceptance review (post hoc, veto-only) concurred with both real ACCEPTs; on a counterfactual X1 ACCEPT it
  concurred on the C-llm-v1 graph, whose package recorded the measured 0.0105 m cylinder 12 times ("D is 0.01 m …
  No recorded field shows a mismatch"), and vetoed on the C-rule-v1 graph for numerical reasons, not geometry.
- **Looser acceptance rules (post hoc, on the stored graphs):** V0 (pre-registered) 2 case ACCEPTs, both correct;
  V1 (combined U only) 18: 14 correct on point estimates (14 of the 41 credible-case results), 1 on E1 (ambiguous
  in both views; false under the set-up reading of the label rule) and 3 false (X1 under every v1 adaptive system);
  V2 (no τ/2 limit on the domain component) 10: 7/41 correct and the same 3 false.
- **Calibration.** Counting each distinct run graph once, repeats included, U covers the true error in 64 of 66
  benchmark quantity rows (lower bound 0.908; rows not independent). Both misses are set-up errors that U does not
  estimate by construction, in cases REJECTed statically: Bexh H1 St (6.05 % vs U 3.01 %; H1 solves Re = 83.3) and
  Bexh I1 Cd (11.05 % vs 4.21 %; wrong force normalisation). On the attacks U covers 4 of 10 rows (all misses X1).
- **Other defects found.** J1 (credible on point estimates) is falsely REJECTed by every system on a
  `checkMesh -allGeometry` flag; a post-hoc variant makes it INCONCLUSIVE after 5 experiments, not ACCEPT.
  Refinements of the C1 and C2 roots diverged, and the verdict reports them as "not run".
- **Integrity.** All 137 stored verifier verdicts replay exactly under the current code. 251 of 9,757 audited numbers
  in LLM text are untraced: 226 derived arithmetic, 15 restated thresholds or conventions, 9 truncated package values,
  1 wrong number (0.42 % for 0.37 %), 0 possible external knowledge. The run store holds 214 records: 198 completed,
  9 failed, 7 orphaned 'running'; 11 are named by no result. One root run (A1) was reproduced in the container.

**Pre-registered success criteria** (`docs/design.md` §19): 1 infrastructure and provenance, partly met; 2 baseline
credibility, partly met; 3 primary demonstration, met; 4 System C false acceptance = 0, met on the observed data,
weakly; 5a adaptivity resolves a case B leaves open, met; 5b LLM planner beats the rule planner, not met under the
committed rule (met by one case in the sensitivity analysis).

## Map of documents and results

### Reports (read these)

| Path | Contents |
|---|---|
| [`reports/final_report.md`](reports/final_report.md) | **Start here.** Summary; answers to the brief (Q1–Q13); success criteria; deviations from pre-registration and threats to validity; integrity checks; glossary |
| [`reports/benchmark_tables.md`](reports/benchmark_tables.md) | Generated by `scripts/analyze_benchmark.py`: verdict matrix in both label views, calibration, LLM run-to-run variance, attack labels in three readings, per-quantity accuracy, criterion 5b and its sensitivity analysis |
| [`reports/benchmark_results.md`](reports/benchmark_results.md) | Generated by `scripts/make_reports.py`: reference and labels, per-system verdicts, loop traces, L-judge text |
| [`reports/baseline_validation.md`](reports/baseline_validation.md) | Baseline verification study (four stages), the in-house reference T, literature comparison, the verifier's verdict on each system's baseline graph (§6), consequences for the labels, limitations; generated tables in [`reports/baseline_generated.md`](reports/baseline_generated.md) |
| [`reports/cases/`](reports/cases/) | Per-case reports with evidence graphs: `<case>__<system>.md` for C-rule, C-llm, C-llm-r2, C-llm-r3 and Bexh (17 each) and the adaptive attack systems (3 each) |
| [`reports/figures/`](reports/figures/) | Verdict matrix, rates, cost against detection (regenerated with the tables), baseline force histories |
| [`reports/status_brief.pdf`](reports/status_brief.pdf) ([`.html`](reports/status_brief.html)) | Interim status brief of 2026-10-19 17:36 UTC, written while the benchmark was still running. Its results are partial and superseded by the final report; do not cite its numbers |

### Design and method

| Path | Contents |
|---|---|
| [`docs/research.md`](docs/research.md) | Phase 0 research: benchmark choice, reference data at Re = 100, V&V methods, what OpenFOAM v2412 provides (source-checked), known failure modes, related automated and LLM-based CFD systems |
| [`docs/design.md`](docs/design.md) | Technical design (the 20 requested items), adversarial cases (§14), experiment primitives (§18), the **pre-registered evaluation protocol and success criteria** (§19), implementation status (§20), risks, falsification test |
| [`docs/methodology.md`](docs/methodology.md) | How evidence is extracted and judged; planners and authority (§5); evaluation protocol and deviations from pre-registration (§6); development log of corrections (§7); what the tests establish, the criterion-5b decision rule and observations (§8); reproducibility and integrity checks (§9) |
| [`HANDOFF.md`](HANDOFF.md) | Working hand-over notes as of 2026-10-19; several numbers in it are stale. Superseded by the reports above |

### Inputs and code

| Path | Contents |
|---|---|
| [`configs/problem_cylinder_re100.yaml`](configs/problem_cylinder_re100.yaml) | The engineering question as a machine-readable spec |
| [`configs/verification.yaml`](configs/verification.yaml), [`configs/verification_v2.yaml`](configs/verification_v2.yaml) | Every threshold with its provenance (v1, pre-registered); v2 adds the geometry and inlet consistency checks |
| [`cases/baseline/baseline.yaml`](cases/baseline/baseline.yaml) | The baseline case |
| [`cases/adversarial/`](cases/adversarial/), [`cases/variants/`](cases/variants/), [`cases/attacks/`](cases/attacks/) | Flawed, borderline/credible and attack cases, as diffs against the baseline; [`DISCARDED.md`](cases/adversarial/DISCARDED.md) lists rejected candidates |
| [`benchmark/manifest.yaml`](benchmark/manifest.yaml), [`benchmark/labels.json`](benchmark/labels.json) | Pre-registered case list and expectations; measured labels in both views (generated) |
| `src/socrates/case_generation/` | Parametric blockMesh/case writer with systematic refinement |
| `src/socrates/openfoam/` | Runner and parsers (the only OpenFOAM-specific code besides the writer) |
| `src/socrates/evidence/` | Evidence extraction (MSER transient removal, cycle statistics, two independent St estimates) |
| `src/socrates/checks/` | Deterministic checks, sensitivity (Richardson/GCI) analysis, verdict aggregation |
| `src/socrates/experiments/` | REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN, RUN_LONGER |
| `src/socrates/critic/` | LLM planner (tool-less, schema-constrained), rule-based planner, numeric audit |
| `src/socrates/orchestration/` | Content-addressed run store with provenance, adaptive loop, benchmark systems, truth and labels |
| `src/socrates/reporting/` | Per-case reports with evidence graphs |
| [`scripts/`](scripts/) | One script per result (see Reproduce); each script's docstring states its inputs and outputs |
| [`tests/`](tests/) | 99 unit tests and 8 OpenFOAM integration tests (of the code, not the physics) |
| [`docker/Dockerfile`](docker/Dockerfile) | Pinned environment (Ubuntu 24.04, OpenFOAM v2412, `requirements.lock`) |

### Results

| Path | Contents |
|---|---|
| `results/runs/<run_id>/` | Every simulation: `run.json` (provenance), `evidence.json`, `series.npz`, `case/` (dictionaries; meshes and fields can be regenerated). Read-only record |
| [`results/baseline/`](results/baseline/) | Baseline study (`study*.json`), reference T (`truth.json`), summary, far-field resolution tests |
| [`results/benchmark/`](results/benchmark/) | `<system>/<case>.json` for A, B, L-judge, C-rule, C-rule-prereg, C-llm, C-llm-r2, C-llm-r3 and Bexh (17/17 each; `*.partial.json` are loop logs) and [`metrics.json`](results/benchmark/metrics.json) |
| [`results/attacks/`](results/attacks/) | `<system>/X*.json`: 21 attack results (B-v1, B-v2, C-rule-v1, C-rule-v2, C-llm-v1, C-llm-v1+review, L-judge × X1–X3); `B-v2-on-benchmark/` and `review-on-benchmark/` apply v2 and the review to the 17 benchmark cases |
| [`results/posthoc/`](results/posthoc/) | Not pre-registered: [`acceptance_rule.md`](results/posthoc/acceptance_rule.md) (V0/V1/V2, what blocks acceptance); `B-allgeo/` and `C-rule-allgeo/` (the J1 `-allGeometry` variant, static and adaptive); `review-on-accepts/` (the four review tests, with each rebuilt package and its sha256); J1 checkMesh logs and flagged cells |
| [`results/analysis/`](results/analysis/) | Integrity outputs: [`replay.json`](results/analysis/replay.json), [`run_audit.md`](results/analysis/run_audit.md), [`untraced_numbers.md`](results/analysis/untraced_numbers.md) and the per-token [`untraced_classification.md`](results/analysis/untraced_classification.md) (each with a `.json`) |
| [`results/reproducibility/`](results/reproducibility/) | Container re-run of the A1 root and its comparison with the host run |
| [`results/logs/`](results/logs/) | Launcher logs (the `results/*.log` files are from the first hours on 2026-10-19) |

## Reproduce

### Option A — container (recommended)

```bash
docker build -t socrates-cfd -f docker/Dockerfile .
docker run --rm -v "$PWD/results:/work/results" socrates-cfd pytest -q
docker run --rm -v "$PWD/results:/work/results" socrates-cfd \
    python3 scripts/run_root_cases.py cases/adversarial/A1_coarse_mesh.yaml
```

Behind a TLS-intercepting proxy, add
`--secret id=extra_ca,src=<proxy-ca.crt> --build-arg https_proxy=...` to the build.
The CA is used at build time only and is not kept in the image.

### Option B — host (Ubuntu 24.04)

```bash
curl -fsSL https://dl.openfoam.com/add-debian-repo.sh -o add-repo.sh && sudo bash add-repo.sh
sudo apt-get install openfoam2412=2412.260127-1
pip install -r requirements.lock && pip install -e .
pytest -q                                              # 99 unit tests (software, not physics)
pytest -q -m openfoam                                  # 8 integration tests (real solver, slow)
socrates run-case cases/baseline/baseline.yaml         # one simulation + evidence
socrates verify <run_id>                               # static verification of a stored run
```

### The full pipeline, in order

```bash
# 1. Baseline study and reference T
python scripts/baseline_study.py                       # mesh/time/domain chains for the baseline (stages 1-3)
python scripts/farfield_resolution_test.py             # stage 4: far-field control on the x4 domain
python scripts/farfield_resolution_test.py --level x1  # the same refinement on the baseline-size domain
python scripts/make_baseline_report.py                 # results/baseline/truth.json, reports/baseline_generated.md

# 2. Benchmark
python scripts/run_root_cases.py cases/adversarial/*.yaml cases/variants/*.yaml
python scripts/run_benchmark.py --systems A,B,L-judge,C-rule,C-llm,Bexh
python scripts/run_benchmark.py --systems C-llm-r2,C-llm-r3          # LLM repeats (run-to-run variance)
SOCRATES_CPU_SLOTS=1 python scripts/run_rule_prereg.py               # C-rule-prereg (5b sensitivity analysis)

# 3. Attacks and benchmark extensions
python scripts/run_attacks.py --benchmark-extensions   # 7 systems x X1-X3, then v2 and the review on the benchmark

# 4. Post-hoc analyses (not pre-registered)
python scripts/posthoc_allgeometry.py --adaptive       # J1 -allGeometry variant; --adaptive runs simulations

# 5. Integrity check, tables and the post-hoc analyses that read the labels
python scripts/replay_verdicts.py                      # results/analysis/replay.json; exit 1 on any mismatch
python scripts/analyze_benchmark.py                    # labels.json, metrics.json, benchmark_tables.md, figures
python scripts/make_reports.py                         # reports/benchmark_results.md
python scripts/posthoc_acceptance_rule.py              # results/posthoc/acceptance_rule.{json,md}
python scripts/posthoc_review_tests.py                 # rebuild and hash the review packages (no LLM call)
python scripts/posthoc_review_tests.py --call          # also re-run the four reviews (LLM; not deterministic)
python scripts/audit_runs.py                           # results/analysis/run_audit.{json,md}
python scripts/dump_untraced.py                        # results/analysis/untraced_numbers.{json,md}
```

`analyze_benchmark.py` reads `replay.json` to decide whether each attack result is current, so the replay runs
first; `make_reports.py` and `posthoc_acceptance_rule.py` read `benchmark/labels.json`, so they run after
`analyze_benchmark.py`. The classification of the untraced numbers was done by reading each token
(`results/analysis/untraced_classification.{md,json}`); there is no script for it. Helpers:
`scripts/status.py` (progress overview) and `scripts/locate_flagged_cells.py <case dir>` (where the cells flagged by
`checkMesh -allGeometry` lie).

### Notes

- The LLM systems (C-llm and its repeats, L-judge, C-llm-v1, C-llm-v1+review, `posthoc_review_tests.py --call`) need a
  headless LLM command-line client with credentials; the call is made in `src/socrates/critic/backends.py`. All
  deterministic systems run without it.
- Runs are content-addressed: an identical request reuses the completed simulation.
- `run_benchmark.py` keeps an existing result while it is current (same decision code, root and evidence) and
  recomputes stale or ERROR results. LLM outputs are not deterministic: a new repeat under a new name (any `C-llm-r*`
  name runs the LLM planner) gives a new graph, not the stored one.
- `SOCRATES_CPU_SLOTS` limits concurrent OpenFOAM processes machine-wide; `SOCRATES_OPENFOAM_BASHRC` points at the
  OpenFOAM environment (default `/usr/lib/openfoam/openfoam2412/etc/bashrc`).
- Pinned versions: OpenFOAM v2412 (`openfoam2412=2412.260127-1`); Python packages in `requirements.lock`.
- Scale: the 17 roots took 9.00 h; each adaptive or fixed-protocol system used 31.7–47.9 h of experiment wall time
  (inflated by CPU oversubscription); the 219 stored LLM calls cost USD 19.11.

## Limitations

- One flow (2D cylinder, Re = 100): 17 cases and 3 attacks built from one base case; one author wrote the cases,
  checks and attacks; n is small and the cases share runs, so every rate has a wide bound (0/7 allows a true rate up
  to 0.348).
- Acceptance depends on the planner's choice of experiments and does not reproduce; the only two ACCEPTs came from
  LLM repeats and rest on an unsettled domain run.
- The pre-registered (v1) verifier cannot see wrong-problem errors (X1, X2); the v2 checks that catch them were written
  after the attacks were defined and have not been tested blind.
- Two experiment primitives are defective: EXPAND_DOMAIN coarsens the far field as the domain grows, and REFINE_MESH
  keeps the time step, so refinements of C1 and C2 diverged and the verdict hides it.
- The reference T shares machinery and runs with the verifier's U; which label view is primary is contested (with
  the mitigation no case is credible); no outside CFD expert has reviewed the labels or the error model.
- The protocol moved after some results (decision-code changes, two rules added to C-rule, the 5b rule fixed after
  15 of 17 C-llm results); all deviations are listed in the final report.
- Provenance gaps: attack results carry no decision-code stamp, 14 early roots lack output hashes, 15 benchmark roots
  were generated from an uncommitted source tree, 7 orphaned 'running' records remain, only 1 of 214 runs was
  reproduced, and wall time is contaminated by CPU oversubscription.

This is a single-benchmark research prototype, deliberately **not** a platform: no UI, no multi-solver support, no
cloud infrastructure. What should and should not be built next is in
[`reports/final_report.md`](reports/final_report.md) (Q12, Q13).
