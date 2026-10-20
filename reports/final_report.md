# Final report: autonomous verification of CFD results (prototype)

> **Status: 2026-10-20, about 12:15 UTC; counts updated to 12:31 where stated. Some results are provisional.**
>
> **Final:**
> - the baseline validation and the reference T;
> - systems A, B, L-judge and C-rule on all 17 benchmark cases;
> - all 21 attack results;
> - C-llm on 16 of 17 cases.
>
> **Where the numbers come from.** The generated files were regenerated at 11:19 UTC: `reports/benchmark_tables.md`, `results/benchmark/metrics.json`, `results/posthoc/acceptance_rule.md` and `results/analysis/run_audit.md`. Four results landed later: C-llm-r2 E1 (11:27) and G2 (11:56), both INCONCLUSIVE, then F1 (12:23, REJECT) and C2 (12:30, INCONCLUSIVE). Counts that include them say so. Figures marked "computed for this report" were computed from the stored result files.
>
> **Pending:**
> - **C-llm on K2** is on its 6th and last allowed experiment (since 12:26). K2 is credible on point estimates. A C-llm ACCEPT would make criterion 5b *met*, and it would also be the first case-level ACCEPT by any verifier-based system, changing the answers to Q1, Q7.1 and Q10 and the C4 caveat that nothing was accepted. The C-llm-r2 K2 repeat could do the same. K2 is not flawed in either label view, so no false-acceptance figure can change.
> - **Bexh** is running A1, B1, F1, H1 and J1. Its rates rest on 12 of 17 cases, and these results decide whether a fixed protocol matches adaptivity (Q5).
> - **C-llm-r2** has 16 of 17 results; K2 is running. Its F1 repeat (12:23) REJECTed with the same ×2 refinement, which bears on criterion 3; its C2 repeat (12:30) is INCONCLUSIVE.
> - **Stale integrity files:** the strict replay (`results/analysis/replay.json`, 05:01, 62 results) and the untraced-number triage (`results/analysis/untraced_numbers.md`, 03:44). The run audit is an 11:19 snapshot taken while processes were live.
>
> **Not run:**
> - the post-hoc adaptive J1 variant;
> - the benchmark extensions (verifier v2 and the LLM acceptance review on the benchmark), so v2's false-rejection rate is unmeasured;
> - a third LLM repeat.
>
> Figures marked *(provisional)* can change.

## Summary

**Terms.**
- **Verification and validation.** Verification asks whether the equations were solved accurately enough. Validation asks whether they were the right equations. This project does *solution verification* of one finished simulation, the **root run**.
- **Tolerance and quantities.** The tolerance is **τ = 3 %**, applied to the mean drag coefficient **Cd** and to the Strouhal number **St**, the dimensionless shedding frequency.
- **Outcomes.**
  - **False acceptance**: ACCEPT of a flawed case.
  - **Detection**: REJECT of a flawed case.
  - **Correct acceptance**: ACCEPT of a credible case.
  - **False rejection**: REJECT of a credible case.
  - **INCONCLUSIVE** is safe but undecided.
- **Case level and quantity level.** A case verdict covers both quantities. A quantity verdict covers Cd or St alone.
- **Benchmark and attacks.** The 17 benchmark cases and the 3 attacks are scored separately.
- **Label views.** Rates are given in two views, the *mitigation view* and the *point-estimate view*, defined in "Benchmark and labels". A case is *robustly flawed* when it is flawed in both.
- **Small-n bounds.** For 0 events in n trials, the one-sided 95 % Clopper–Pearson upper bound is 1 − 0.05^(1/n): 0.348 for n = 7, 0.312 for n = 8, 0.632 for n = 3.

**Answers to the brief, one line each.**

- **Q1 Does it work?** As a filter that rejects numerically flawed results, yes on this benchmark: 7 of 7 robustly flawed cases rejected and none accepted. As a certifier, no, so far: no verifier-based system has accepted any case (0 of 96 results at 12:31) *(provisional: the C-llm K2 run and its C-llm-r2 repeat, both on a point-estimate-credible case, are still running)*.
- **Q2 Which failures does it detect?**
  - Statically: wrong Re (H1), wrong force normalisation (I1) and a steady solver (D1).
  - With experiments: coarse mesh (A1), small domain (B1, B2), first-order convection (F1) and compensating errors (attack X3).
  - Missed safely by the pre-registered (v1) systems: C2 (flawed on point estimates only), and the wrong-problem attacks X1 and X2 (X2 is flawed only under the set-up reading).
- **Q3 What do OpenFOAM's diagnostics detect?** Only D1: 1 of 7 flawed cases (1 of 8 on point estimates). They accepted the other 6 (7 with C2 on point estimates), on a benchmark built from runs that complete.
- **Q4 What does the deterministic verifier add?** From one run and at no simulation cost, it turns A's 6 false acceptances into 2 REJECTs and 4 safe INCONCLUSIVEs. It cannot accept anything from one run.
- **Q5 What does the adaptive system add?**
  - It resolves the 4 robustly flawed cases the static verifier leaves open (A1, B1, B2, F1), all by REJECT, at 0.78–6.94× the root's compute. It does not resolve C2 (flawed on point estimates only).
  - Over a fixed exhaustive protocol it adds one REJECT so far (B2, on a thin margin) *(provisional)*.
- **Q6 Does the LLM add value?** Not measurably, by the §19 criterion under a decision rule fixed after 15 of 17 C-llm results *(provisional)*.
  - Its verdicts equal the rule planner's on 16 of 16 cases.
  - Compute is level (77.06× vs 77.55× root, p = 0.18), plus USD 4.47 in fees.
  - It targets the right first experiment more often (4/4 vs 1/4), on small n.
- **Q7 What failures remain?**
  - Acceptance never works.
  - Wrong-problem errors are invisible.
  - Two experiment primitives are defective: EXPAND_DOMAIN coarsens the far field, and REFINE_MESH diverges at high Courant number and is then reported as "not run".
  - One false rejection comes from a mesh heuristic (J1).
  - A gate check cannot be cleared.
  - Records are incomplete.
- **Q8 What is the false-acceptance rate?**
  - System C: 0/7 in the mitigation view and 0/8 on point estimates (upper bounds 0.35 and 0.31).
  - Attacks: 0/2 or 0/3, depending on the reading of X2 (upper bounds 0.78 and 0.63).
  - One quantity-level false acceptance, in the rule-planner ablation (X1 St).
  - System A: 6/7.
  - The case-level zeros follow automatically from the fact that no verifier-based system accepted any case. They show the system is safe here, not that it accepts precisely.
- **Q9 What is the compute overhead?**
  - A REJECT costs 0 (static) to 6.94× the root.
  - Undecided cases cost up to 11.95× (24.41× for the uncapped fixed protocol).
  - The cost of an ACCEPT is unknown.
- **Q10 What is needed for trust?**
  - Demonstrated correct ACCEPTs.
  - Fixed primitives.
  - A blind flaw set by another author.
  - An independent reference.
  - Complete replay and provenance.
  - Outside expert review.
- **Q11 Is there a product?** Not yet. What exists is a conservative rejection gate for one flow, with no demand evidence.
- **Q12 What to build next?** In order:
  1. A set-up consistency gate.
  2. A far-field-preserving domain primitive, shipped only with the gate.
  3. A blind held-out benchmark.
  4. A pre-registered acceptance rule.
  5. A Courant-holding mesh refinement.
  6. A discharge path for the regime gate, and one mesh-quality rule for roots and children.
  7. Integrity plumbing.
- **Q13 What not to build?**
  - LLM-issued verdicts.
  - A cleverer planner.
  - More geometries.
  - The acceptance review as designed.
  - Exhaustive protocols as the default.
  - Benchmark-tuned heuristics.
  - Platform features.

**The five pre-registered success criteria** (`docs/design.md` §19):

| # | criterion | status | evidence |
|---|---|---|---|
| 1 | The loop runs autonomously on real OpenFOAM, with provenance for every run | **Partly met** | 195 real run records, 0 authority violations. Operator relaunches were needed after code fixes and two container restarts. 14 roots lack output hashes, and 7 records are orphaned. |
| 2 | Baseline credibility | **Partly met** | 2a met (Cd and St in the τ-widened literature band). 2b met only through its fallback "or the report explains why not": the verifier cannot bound the drag. |
| 3 | Primary demonstration | **Met** | 4 instances under C-llm (A1, B1, B2, F1), all repeated by C-llm-r2. Thin margin on B2; F1 needed two experiments. |
| 4 | Safety: System C false acceptance = 0 | **Met on the observed data; weak** | 0/7 and 0/8 on the benchmark, 0/2 to 0/3 on the attacks. Nothing was accepted, and a looser rule would have accepted X1. |
| 5a | C resolves a case that B leaves INCONCLUSIVE | **Met** | A1, B1, B2 and F1, all by correct REJECT |
| 5b | The LLM planner beats the rule planner on accuracy or cost | **Not met (provisional)** | Identical verdicts; cost sign test p = 0.18. Met only if C-llm ACCEPTs K2. |

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/metrics.json`; `results/posthoc/acceptance_rule.md` (92 verifier-based results at 11:19); `results/benchmark/C-llm-r2/{E1_noslip_side_walls,G2_average_from_start,F1_upwind_convection,C2_euler_large_timestep}.json` (landed later); `reports/baseline_validation.md` §1, §6; `results/analysis/run_audit.md`.

## What was built

**The question.** The prototype answers one question for one flow. Take a finished OpenFOAM simulation of a two-dimensional circular cylinder at Reynolds number Re = 100: a 10 mm rod in a 0.15 m/s air stream, treated as unbounded. Are its Cd and St within 3 % of the converged answer? The answer is ACCEPT, REJECT or INCONCLUSIVE.

**Time unit.** Time is measured in convective units D/U, the time the stream takes to travel one diameter.

| layer | what it does | where |
|---|---|---|
| Case generation, runner | Parametric OpenFOAM v2412 cases (pimpleFoam; simpleFoam for D1) with systematic refinement; runner and log parsers | `src/socrates/case_generation/`, `src/socrates/openfoam/` |
| Evidence extraction | Deterministic reading of checkMesh, solver logs, force histories and mass balance; cycle detection, transient removal, cycle statistics, two independent St estimates | `src/socrates/evidence/` |
| Deterministic verifier | 14 check types (19 entries per case), including the mesh, time-step and domain sensitivity checks; per quantity, the components are combined in an error budget | `src/socrates/checks/`, `configs/verification.yaml` |
| Experiment primitives | RUN_LONGER, REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN. Limits: refinement ≤ 2×, ≤ 160k cells, Δt ≥ root/8, domain ≤ 4×, end time ≤ 600 D/U | `src/socrates/experiments/primitives.py` |
| Run store, provenance | Content-addressed: a run's id hashes its full configuration, so an identical request reuses the run. Each `run.json` records parent, reason, launcher, configuration diff and software versions. A finished one also records raw-log hashes and, since correction R19, output and final-field hashes; 14 completed roots predate R19. | `src/socrates/orchestration/`, `results/runs/` |
| Planners, loop | A rule-based or LLM planner may only propose one validated experiment. It is consulted only while the verdict is INCONCLUSIVE. Budgets: ≤ 6 experiments, ≤ 12 planner calls, ≤ 12× root compute. | `src/socrates/critic/`, `src/socrates/orchestration/loop.py` |

**How the verifier decides.**
- **Components.** For each quantity, each uncertainty component (statistics, mesh, time, domain) has an estimated relative uncertainty U. It PASSes when U ≤ τ/2. The averaging bias PASSes up to τ.
- **ACCEPT** needs every gate check passed, every component PASSed, and bias + root-sum-square (RSS) of the other components ≤ τ.
- **REJECT** follows any FAIL. A sensitivity check FAILs when the demonstrated change between the root and the finest member of a study exceeds τ by more than twice the statistical noise.
- **INCONCLUSIVE** covers everything else. Missing evidence never passes.
- **Richardson extrapolation.** Mesh, time and domain uncertainties come from Richardson extrapolation, which estimates the zero-spacing limit from runs at known ratios, assuming error ∝ (spacing)^p. With three levels the **Celik procedure** measures p and applies a safety factor Fs (1.25 if p is plausible, 3 otherwise). With two levels it uses Fs = 3.

**Authority over the LLM.**
- **What it sees.** The LLM runs with no tools and must answer in schema-validated JSON. It sees an evidence package with opaque run names and no reference values.
- **No verdicts.** An ACCEPT or REJECT proposal from it is logged as an authority violation and not executed. None occurred.
- **Number audit.** Every number it writes is checked against the package.
- **Bounded calls.** Each call has a 300 s timeout and at most 3 attempts, with backoff and jitter.

| system | what it is | experiments |
|---|---|---|
| A | OpenFOAM's diagnostics: ACCEPT if the solver completed, checkMesh (as run, `-allGeometry -allTopology`) is OK, and steady residualControl is met | none |
| B | Static deterministic verifier on the submitted run | none |
| L-judge | An LLM judges the evidence alone, without deterministic gating | none |
| C-rule | Adaptive loop with the rule-based planner (ablation) | ≤ 6 |
| C-llm | Adaptive loop with the LLM planner: **System C** of §19 | ≤ 6 |
| Bexh | Fixed exhaustive protocol (RUN_LONGER, REFINE_MESH √2 twice, REDUCE_TIME_STEP, EXPAND_DOMAIN), no budget cap | 5 |
| C-llm-r2 | Independent repeat of C-llm, for variance | ≤ 6 |

**Attack variants.** The attacks ran with the pre-registered verifier (v1) and with three variants:
- **v2** adds two post-hoc set-up checks, geometry_consistency and inlet_uniformity;
- **+review** adds an LLM review that can only veto a deterministic ACCEPT;
- **L-judge**.

**Scale.**
- 195 run records at 11:19: 169 completed, 8 failed and 18 'running' (7 of them orphaned), all OpenFOAM v2412 (package 2412.260127-1).
- 112 benchmark results at 12:31 (including C-llm-r2 E1, G2, F1 and C2) and 21 attack results.
- 99 unit tests pass, with 8 OpenFOAM integration tests deselected. They test the code, not the physics.

```bash
docker build -t socrates-cfd -f docker/Dockerfile .          # pinned OpenFOAM v2412 + Python lockfile
python scripts/run_root_cases.py cases/adversarial/*.yaml    # adversarial roots (variant roots are created by run_benchmark.py; all reused if present)
python scripts/run_benchmark.py --systems A,B,L-judge,C-rule,C-llm,Bexh
python scripts/run_benchmark.py --systems C-llm-r2           # independent LLM repeat
python scripts/run_attacks.py                                # attacks X1–X3 under the attack systems
python scripts/analyze_benchmark.py                          # metrics.json, benchmark_tables.md
python scripts/replay_verdicts.py; python scripts/audit_runs.py; python scripts/posthoc_acceptance_rule.py
```

C-llm and L-judge need an LLM command-line client with credentials. The deterministic systems do not.

*Sources:* `docs/design.md` §13, §18, §19; `docs/methodology.md` §1–§5, §8–§9; `README.md`; `results/analysis/run_audit.md`; `pytest` run for this report.

## Benchmark and labels

### The reference T

A label needs a "true" answer. No published value is converged to τ/2 for this exact set-up, so an in-house reference was built from three refinement chains around the baseline: mesh, time step and domain size. Each chain was extrapolated with the Celik procedure, and the corrections were summed.

- **Result:** Cd = 1.3155 ± 0.94 %, St = 0.1639 ± 0.46 %.
- **What U(T) is made of.** U(T) is dominated by a far-field *model-form* term of 0.82 % of Cd, an uncertainty about the set-up rather than the discretisation. It is the gap between domain chains with and without a refined far field.
- **Agreement with the literature.** At matched domain size this work agrees with published values within −0.1 … +0.8 % (drag) and −0.2 … +0.3 % (St). About 1 % of scatter between codes remains, so the literature confirms T to about 1 %, not to τ/2.
- **T is not independent of the verifier.** It uses the same Richardson machinery and, for the baseline, the same runs.

### The cases

The baseline plus 16 variants, each a documented change. The author intended 3 to be credible, 2 borderline and 12 flawed (`benchmark/manifest.yaml`). The error is e = (reported − T)/T.

| case | change from the baseline | intended | Cd error | St error | max e/τ | point est. | mitigation |
|---|---|---|---|---|---|---|---|
| baseline | — (160 cells around, sides ±40 D, Δt 0.01 D/U) | credible | +1.20 % | −0.31 % | 0.40 | credible | ambiguous |
| K1 | central (Gauss linear) convection | credible | +1.90 % | −0.39 % | 0.63 | ambiguous | ambiguous |
| K2 | finer mesh, smaller Δt, larger domain | credible | +0.94 % | −0.07 % | 0.31 | credible | ambiguous |
| A1 | mesh ×0.5 | flawed | −1.55 % | −5.08 % | 1.69 | flawed | flawed |
| A2 | mesh ×0.75 | borderline | +0.51 % | −1.45 % | 0.48 | credible | ambiguous |
| B1 | domain 8/15/±4 D (blockage 12.5 %) | flawed | +14.7 % | +9.57 % | 4.90 | flawed | flawed |
| B2 | domain 15/25/±10 D (blockage 5 %) | borderline | +4.24 % | +1.89 % | 1.41 | flawed | flawed |
| C1 | Δt ×5, 3 outer correctors (max Courant 3.42) | flawed | +0.64 % | −0.26 % | 0.21 | credible | ambiguous |
| C2 | Euler time scheme, Δt ×4 | flawed | −1.93 % | −3.33 % | 1.11 | flawed | ambiguous |
| D1 | steady solver | flawed | −17.0 % | not produced | 5.66 | flawed | flawed |
| E1 | no-slip walls on the far-field sides | flawed | +1.89 % | +0.21 % | 0.63 | ambiguous | ambiguous |
| F1 | first-order upwind convection | flawed | −3.55 % | −23.1 % | 7.69 | flawed | flawed |
| G1 | 40 D/U run, averaged from 10 D/U | flawed | −1.47 % | −1.62 % | 0.54 | ambiguous | ambiguous |
| G2 | 60 D/U run, averaged from t = 0 | flawed | +0.32 % | −1.52 % | 0.51 | ambiguous | ambiguous |
| H1 | dynamic viscosity entered as ν (Re = 83.3) | flawed | +2.52 % | −6.05 % | 2.02 | flawed | flawed |
| I1 | stale force-reference velocity (0.16 vs 0.15 m/s) | flawed | −11.1 % | −0.31 % | 3.68 | flawed | flawed |
| J1 | wake streamwise cells ×0.3 | flawed | +0.56 % | −1.11 % | 0.37 | credible | ambiguous |

### Two label views, given equal weight

- **Point-estimate view (the §19 rule as written).**
  - Flawed if max e > τ or the set-up answers a different problem (D1 and H1 qualify on both counts).
  - Credible if max e ≤ τ/2; ambiguous otherwise.
  - This gives **8 flawed, 5 credible and 4 ambiguous** cases.
- **Mitigation view.**
  - A case is ambiguous when e ± U(T) straddles τ or τ/2, unless it is flawed for every T in that range.
  - This gives **7 flawed** (C2 becomes ambiguous), **0 credible** and **10 ambiguous** cases.
  - To be credible here, a case would need a Cd error below 0.565 % *and* an St error below 1.04 %. No case meets both, so correct acceptance and false rejection are undefined in this view.

**Which view is primary is contested.**
- The §19 text is the point-estimate rule.
- The mitigation comes from the pre-registered risk list ("label near-boundary cases ambiguous"). It was made concrete in review R18 (4639ddb, 10-19 08:24), before any T existed but after some verdicts.
- Commit 3d9f43c called the point-estimate view "secondary (post-hoc)", and 4776198 reframed both views as pre-registered.

### Three readings of the set-up clause

§19 calls a case flawed "if the set-up answers a different problem (wrong Re or regime)", and credible only "if … the set-up is consistent". It can be read three ways:
- **Narrow** (the `benchmark/labels.json` convention): only problems detected in the evidence count (wrong Re, steady formulation, missing quantity). Every other departure is judged by its error.
- **Literal:** any other departure from the problem statement makes a case ambiguous unless e > τ.
- **Set-up:** any departure makes the case flawed.

On the benchmark only E1 changes: under the set-up reading it becomes flawed, and A's and L-judge's ACCEPTs of it become false acceptances. On the attacks only X2 changes:

| attack | Cd error | St error | set-up | literal | narrow, point est. | narrow, mitigation |
|---|---|---|---|---|---|---|
| X1 cylinder 5 % too large | +5.98 % | −3.60 % | flawed | flawed | flawed | flawed |
| X2 sheared inlet | +1.20 % | −0.50 % | flawed | ambiguous | **credible** | ambiguous |
| X3 compensating mesh/domain errors | +5.81 % | +0.16 % | flawed | flawed | flawed | flawed |

### Many intended flaws are below τ

**Six of the 12 intended-flawed cases are not flawed in the mitigation view** (C1, C2, E1, G1, G2, J1), and five are not on point estimates. The planted defects are real departures from good practice, but their effect on Cd and St stays below τ, or, for C2, within U(T) of it:
- **G1 and G2.** The start-up transient decays fast; the cycle-mean Cd error halves every cycle.
- **C1.** Halving its Δt moved Cd by only −0.02 %.
- **C2.** Its St error is just above τ, and straddles τ once U(T) is included.

**The borderline and credible designs moved as well.**
- **B2**, intended borderline, is robustly flawed.
- **None of the intended-credible cases is robustly credible.** With the standard far-field chain, the baseline and K2 errors would be 2.04 % and 1.78 %.

**The consequence.** On this problem, the gap between "plausible but wrong" and "careful" is often smaller than the reference's own uncertainty. That limits what the benchmark can show about acceptance.

### How the reference moved

| version | commit (10-19) | Cd | St | basis |
|---|---|---|---|---|
| stage 1 | 3d9f43c 11:03 | 1.3133 ± 0.72 % | 0.1647 ± 1.06 % | pre-registered chains |
| stage 1, root continued | 3cff05d 12:42 | 1.3134 ± 0.71 % | 0.1648 ± 1.29 % | root from its 250 D/U continuation |
| stage 2 | 33d5ebf 13:25 | 1.3046 ± 1.15 % | 0.1638 ± 0.28 % | settled domain levels; Δt/8 added |
| stage 2, model-form terms (never used for labels) | 4776198 13:51 | 1.3046 ± 1.19 % | 0.1638 ± 0.48 % | time-overlap model-form and time-conditioning terms |
| stage 3 (never used for labels) | 26fee11 14:26 | 1.290 ± 6.3 % | 0.1641 ± 0.84 % | four-level domain chain, not asymptotic |
| **stage 4 (final)** | 021fc5a 16:43 | **1.3155 ± 0.94 %** | **0.1639 ± 0.46 %** | far-field-refined ×4 level |

**What stage 4 found.** EXPAND_DOMAIN keeps the per-cell growth rate, so the far field coarsens as the domain grows: the last wake cell is about 1.0 D at ×1 and 3.9 D at ×4. Refining the ×4 far field raised Cd by 0.16 %; the same refinement at ×1 raised it by 0.03 %.

**Robustness to these revisions.**
- **Flawed sets do not move.** The point-estimate flawed set {A1, B1, B2, C2, D1, F1, H1, I1} is the same under every committed T. So are the mitigation-view flawed set (the same without C2) and its empty credible set.
- **Hence false-acceptance and detection rates do not depend on the revisions.**
- **The point-estimate credible set does move:** {baseline, C1, K2} → {A2, C1, G2, J1} → {A2, C1, J1, K2, baseline}. Correct-acceptance and false-rejection rates in that view carry this caveat.

**Percentages.**
- Errors are relative to T.
- The verifier's sensitivity changes are relative to the finer member of a study.
- Loop-trace changes, relative to the parent run, appear only in parentheses. For example, one A1 refinement reads 3.28 % in the verifier and +3.39 % in the trace.

*Sources:* `benchmark/labels.json`; `benchmark/manifest.yaml`; `reports/baseline_validation.md` §1, §3–§5, §7; `docs/methodology.md` §6; `reports/benchmark_tables.md` (attack labels); git log.

## Q1. Does it work?

**As a detector of numerical flaws, yes on this benchmark. As a certifier, no: it never said yes.**

| system | false acceptance (mitig. / point) | detection (mitig. / point) | correct acceptance (point) | false rejection (point) | inconclusive |
|---|---|---|---|---|---|
| A (OpenFOAM diagnostics) | **6/7 / 7/8** | 1/7 / 1/8 | 4/5 | 1/5 | 0/17 |
| B (static verifier) | 0/7 / 0/8 | 3/7 / 3/8 | 0/5 | 1/5 | 13/17 |
| L-judge (LLM, evidence only) | 0/7 / 0/8 | 7/7 / 7/8 | 4/5 | 1/5 | 1/17 |
| C-rule | 0/7 / 0/8 | 7/7 / 7/8 | 0/5 | 1/5 | 9/17 |
| C-llm *(provisional, 16/17)* | 0/7 / 0/8 | 7/7 / 7/8 | 0/4 | 1/4 | 8/16 |
| Bexh *(provisional, 12/17)* | 0/3 / 0/4 | 2/3 / 2/4 | 0/4 | 0/4 | 10/12 |

**What works.**
- The adaptive systems rejected every robustly flawed case. Each experimental REJECT rests on a demonstrated change larger than τ.
- They detect 7/7 (7/8 on point estimates), against 3/7 for B and 1/7 for A. An LLM judging the evidence alone (L-judge) also detects 7/7, and it accepts 4/5 point-estimate-credible cases where C accepts none, with no simulations (Q6). One author wrote the cases, checks and attacks, so this shows consistency, not a blind test.
- Their one miss is C2, flawed only on point estimates, and they miss it safely.

**What does not work.**
- No verifier-based system issued a case-level ACCEPT: 0 of 92 results at 11:19 (74 benchmark, 18 attack), plus four C-llm-r2 results that landed later (E1, G2 and C2 INCONCLUSIVE, F1 REJECT).
- Correct acceptance is 0/5 for C-rule and 0/4 for C-llm. A rule that never says yes cannot falsely say yes, so the zero false acceptances say little about how precisely it accepts.
- The main blocker is the domain uncertainty component: on its own it blocks 17 of the 60 blocked quantities in benchmark results with experiments, and is among the blockers in 45. Far-field coarsening by the EXPAND_DOMAIN primitive inflates it: on the baseline study graph, a refined far field lowers it from 2.62 % to 1.56 %, still above τ/2 (Q7.1). The post-hoc looser rules accept some credible cases (V1: baseline, A2 and K2 under C-rule, baseline and A2 under C-llm, the baseline under C-llm-r2; V2: only the baseline), and both also accept the wrong-geometry attack X1 in all three v1 adaptive systems (Q8.5).

**Quantity level and calibration.**
- There are 4 quantity-level ACCEPTs on the benchmark, all inside INCONCLUSIVE cases and all with errors ≤ τ/2: C-rule baseline St, C-rule K2 Cd, C-llm A2 Cd and C-llm-r2 K1 St. The one on the attacks is false (X1 St; Q8.3).
- The verifier's U covered the true error in 36 of 37 benchmark entries, but in only 4 of 10 attack entries (Q7.6).

*Sources:* `reports/benchmark_tables.md` (verdict matrix, both views, calibration, per-quantity accuracy); `results/benchmark/metrics.json`; `results/posthoc/acceptance_rule.md`.

## Q2. Which failures does it detect?

| case and flaw | error (Cd, St) | label (mitig. / point) | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|---|---|
| D1 steady solver | −17.0 %, none | flawed / flawed | REJ | REJ | REJ | REJ | REJ | REJ |
| H1 Re = 83.3 | +2.52 %, −6.05 % | flawed / flawed | ACC ✗✗ | REJ | REJ | REJ | REJ | pending |
| I1 wrong force reference | −11.1 %, −0.31 % | flawed / flawed | ACC ✗✗ | REJ | REJ | REJ | REJ | REJ |
| A1 coarse mesh | −1.55 %, −5.08 % | flawed / flawed | ACC ✗✗ | INC | REJ | REJ | REJ | pending |
| B1 small domain | +14.7 %, +9.57 % | flawed / flawed | ACC ✗✗ | INC | REJ | REJ | REJ | pending |
| B2 moderate domain | +4.24 %, +1.89 % | flawed / flawed | ACC ✗✗ | INC | REJ | REJ | REJ | INC |
| F1 first-order upwind | −3.55 %, −23.1 % | flawed / flawed | ACC ✗✗ | INC | REJ | REJ | REJ | pending |
| C2 Euler, large Δt | −1.93 %, −3.33 % | ambiguous / **flawed** | ACC (✗✗ point) | INC | INC | INC | INC | INC |

✗✗ = false acceptance; INC = INCONCLUSIVE.

**How each detection was obtained.**

| case | decisive check | C-rule: path → decisive change (cost) | C-llm: path → decisive change (cost) |
|---|---|---|---|
| D1 | static: residualControl not met; steady solver above shedding onset | 0 experiments | 0 experiments |
| H1 | static: reynolds_consistency (Re 83.33 vs 100) | 0 | 0 |
| I1 | static: force_reference_consistency (0.16 vs 0.15 m/s) | 0 | 0 |
| A1 | mesh FAIL on St | REFINE_MESH √2 → 3.28 % (+3.39 %); 1.06× | REFINE_MESH ×2 → 4.78 % (+5.02 %); 2.14× |
| B1 | domain FAIL on Cd and St | 3 other experiments first, then EXPAND_DOMAIN ×2 → Cd 8.86 %, St 6.65 %; 6.16× | the same domain run first; 0.78× |
| B2 | domain FAIL on Cd (3.39 % − 2 × 0.081 % noise = 3.23 %, a 0.23-point margin; the decisive ×4 member is an 80 D/U run with a coarse far field, C3) | 3 other experiments, then two EXPAND_DOMAIN ×2 → Cd 3.39 %; 6.94× | the same two runs; 1.75× |
| F1 | mesh FAIL on St | 4 RUN_LONGER (St ≤ 0.36 %), then REFINE_MESH √2 → 6.74 % (+7.22 %); 3.90× | REFINE_MESH ×2, then RUN_LONGER on the root → 11.45 % (+13.34 %); 4.80× |

**The other systems.**
- **C-llm-r2** repeated A1 and B2 with the same runs. On B1 it used a ×3 domain (a new run) and also REJECTed. On F1 (12:23) it used the same ×2 refinement with a 300 D/U continuation of the root and also REJECTed.
- **Bexh**'s single domain step on B2 showed only a 2.37 % change, so it stayed INCONCLUSIVE (Q5).
- **L-judge** rejected all seven flawed cases from features visible in the configuration or evidence summary.

**Planted defects with errors near or below τ (and the intended-credible K1).**
- **No warning from B on E1 or K1.** The adaptive systems end INCONCLUSIVE on them; A and L-judge ACCEPT.
- **C1 and C2.** B flags the Courant number. Every root mesh refinement diverged, so their mesh error is never measured (Q7.3); the last of them, a C-llm-r2 ×1.3 refinement of the C2 root, failed at 12:29. On C2 the time studies show changes below τ (C-rule: Cd 2.17 %, St 2.77 %), so no FAIL fires.
- **G1 and G2.** On G1, B flags averaging, statistics and regime (3 stationary cycles; lift amplitude +25.8 %). On G2 it flags only the regime (lift amplitude +6.7 %). Its averaging and statistics checks PASS, with a measured averaging bias of 0.52 % (Cd) and 0.95 % (St). C-rule spent G1's whole budget on four continuations.
- **J1.** Every system with a J1 result REJECTs it; Bexh J1 is still running. A, B and the adaptive systems reject on the `-allGeometry` checkMesh flag. L-judge cites the failed checkMesh together with the 33-cell wake. On point estimates this is a false rejection (Q7.2).

**Attacks.**

| attack | B-v1 | C-rule-v1 | C-llm-v1 | C-llm-v1+review | L-judge | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|
| X1 cylinder +5 % | INC | INC (St ACCEPTed, error −3.60 %) | INC | INC | REJ | REJ | REJ |
| X2 sheared inlet | INC | INC | INC | INC | REJ | REJ | REJ |
| X3 compensating errors | INC | REJ (mesh FAIL on St, 4.36 %; 3.21×) | REJ (domain FAIL, Cd 5.14 %, St 3.83 %; 0.77×) | REJ | REJ | INC | REJ |

- **X1 and X2 are wrong-problem errors.** Refining a wrong problem converges consistently to the wrong answer, so solution verification cannot see them.
- **The v2 checks catch both statically.** They were written after the attacks were defined, so this is not a blind test.
- **X2's REJECTs** are correct only under the set-up reading; on narrow point estimates they are false rejections.
- **X3** is what adaptive verification is for, and every adaptive system rejected it. Under C-rule-v1 and C-rule-v2, however, the quantity-level REJECT falls on St, which is only +0.16 % from T, while the quantity that is really wrong, Cd (+5.81 %), stays INCONCLUSIVE. C-llm-v1 REJECTs both quantities (Q7.5).

*Sources:* `reports/benchmark_tables.md`; `reports/benchmark_results.md` (loop traces, L-judge text); `results/benchmark/*/*.json` (checks with values, noise, runs); `results/attacks/*/*.json`; `benchmark/manifest.yaml`.

## Q3. Which failures do OpenFOAM's own diagnostics detect?

**System A's rule.** System A stands in for a careful user reading OpenFOAM's output. It ACCEPTs when three things hold:
- the solver completed;
- checkMesh reports OK, run as `-allGeometry -allTopology`;
- for steady runs, residualControl is met.

**Results.** A ACCEPTed 15 of 17 cases.
- **D1, correct.** Its REJECT of D1 (residualControl not met) is its only detection: 1/7, or 1/8 on point estimates.
- **J1, incidental.** Its REJECT of J1 comes from the extended check's "Cells with small determinant (< 0.001) found, number of cells: 48", all at x ≈ 47 D next to the outlet. The default checkMesh prints "Mesh OK." on the same mesh (`results/posthoc/J1_checkMesh_default.log`, line 103). J1's errors are 0.56 % and 1.11 %, so this is a false rejection on point estimates, not a detection.
- **False acceptances.** A accepted A1, B1, B2, F1, H1 and I1 (6/7; 7/8 with C2).

**The rate reflects how the benchmark was built.**
- The brief required plausible, successfully executed cases. The one candidate that crashed (a first C1 with Δt ×10) was discarded (`cases/adversarial/DISCARDED.md`). So 6/7 is not an estimate for real use.
- What it does show: once the solver completes, completion plus checkMesh says nothing about discretisation error, domain size, force normalisation or Re.
- A was not run on the attacks. All three attack roots completed with checkMesh OK, so A would have accepted them (an inference).

**Divergence and B's checks.**
- OpenFOAM does flag divergence: all 8 failed runs in the store at 11:19 (9 by 12:29) are floating-point-exception crashes in the C1 and C2 families. But no benchmark root diverged.
- **B's checks read from OpenFOAM output:** solver completion, mesh quality, linear-solver convergence, Courant number and mass conservation.
- **B's comparisons of the configuration with the problem statement:** Re, force reference and scheme order. The regime check does both: steady solver against Re for D1, lift-amplitude drift for F1, G1 and G2. The averaging and statistics checks read the force histories.
- B's two extra static detections, H1 and I1, come from those comparisons.

*Sources:* `results/benchmark/{A,B}/*.json`; `results/posthoc/J1_checkMesh_*.log`, `flagged_cells.txt`; `cases/adversarial/DISCARDED.md`; `results/analysis/run_audit.md`; `docs/design.md` §15–§16.

## Q4. What does the deterministic verifier add?

**On a single run (B against A).**

| | A | B |
|---|---|---|
| flawed cases ACCEPTed (mitig. / point) | 6/7 / 7/8 | **0/7 / 0/8** |
| flawed cases REJECTed | D1 | D1, H1, I1 |
| flawed cases left INCONCLUSIVE | none | A1, B1, B2, F1 (and C2 on point estimates) |
| credible cases ACCEPTed (point) | 4/5 | 0/5 |

- **What B adds.**
  - Two detections (H1, I1) from set-up consistency checks. The checks (reynolds_consistency, force_reference_consistency) were committed five minutes before the cases by the same author (e27ac5b 07:00, 8d403aa 07:05), so these detections show consistency, not generalisation.
  - An honest "undecided" where nothing in one run shows the error. On A1, B1 and B2, 13 of 19 checks PASS, and only the six unmeasured mesh, time and domain components are INCONCLUSIVE.
  - Static warnings on F1, C1, C2, G1 and G2.
- **Its cost.** B cannot accept anything (13/17 INCONCLUSIVE), because one run cannot supply mesh, time and domain estimates.

**Inside the adaptive loop, three rules of the verifier carry the system.**
- **The FAIL rule** turns one or two well-chosen experiments into a REJECT. One suffices for A1 and B1 under C-llm and for X3 under C-llm-v1. Two are needed for B2 (two domain steps), for F1 (C-llm: a ×2 refinement and a continuation of the root) and for X3 under C-rule-v1 (two refinements).
- **The per-component τ/2 rule** prevents acceptance, and is also what kept X1 from a false acceptance (Q8.4).
- **Missing evidence never passes.**

**Defects found in the verifier** (Q7):
- diverged refinements are reported as "not run";
- the regime check is evaluated on the root only, so nothing can discharge it;
- mesh quality is checked on the root only, while children failing the same flag are used as evidence;
- per-iteration checks are not stored.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/B/*.json`; `docs/methodology.md` §3, §8.

## Q5. What does the adaptive system add?

**Over the static verifier: rejections, not acceptances.**
- Both adaptive systems turn B's four undecided flawed cases (A1, B1, B2, F1) into correct REJECTs. Their labels are flawed in both views and for every T within U(T).
- Detection rises from 3/7 to 7/7 (3/8 to 7/8 on point estimates), while false acceptance stays at 0.
- **They add nothing on non-flawed cases.** On the 9 paired ambiguous cases the adaptive verdicts equal B's.
- **Most compute changes nothing.** On the 16 paired cases, 77 % of C-rule's compute (59.49 of 77.55 root-units) and 88 % of C-llm's (67.59 of 77.06) went to the 8 ambiguous cases that ended INCONCLUSIVE.
- **Two caveats** (criterion 3): C-rule's A1 margin and the B2 margin are thin, and the F1 demonstration needed two experiments.

**On the attacks.**
- **X3.** Adaptivity catches compensating errors that B misses (X3, 0.77–3.21× root).
- **X1 and X2.** It does not catch wrong-problem errors: 5–6 experiments at 6.6–9.0× root, ending INCONCLUSIVE.
- **The only route to a false ACCEPT.** B can never accept. C-rule-v1 produced the one quantity-level false acceptance, and a looser rule would let all v1 adaptive systems accept X1 (Q8.5).

**Over the fixed exhaustive protocol (Bexh)** *(provisional, 12/17)*.
- **Its verdicts so far.** Bexh's verdicts equal B's on all 12 completed cases. Its detection is 2/3 (2/4 on point estimates).
- **B2: one extra domain level.**
  - Bexh's single EXPAND_DOMAIN ×2 changed Cd by 2.37 %, below τ. Its two-level estimate (Fs = 3) gave a domain U of 14.23 %, so it ended INCONCLUSIVE.
  - Both adaptive planners ran a second domain step, Cd 1.3713 → 1.3395 → 1.3263, a 3.39 % change, which FAILs.
  - A fixed protocol with two domain steps would also find it. Adaptivity spent the extra step where the evidence pointed: C-llm after 2 experiments (1.75×), C-rule after 5 (6.94×).
- **Budgets were not equal.** Experiments / root-units over each case set (computed for this report):

| case set | cases | Bexh | C-rule | C-llm |
|---|---|---|---|---|
| completed by all three | 11 | 53 / 89.22 | 45 / 66.43 | 42 / 69.34 |
| … without D1, I1 (Bexh runs its protocol after a static FAIL) | 9 | 45 / 77.60 | 45 / 66.43 | 42 / 69.34 |
| … also without G1, G2 (Bexh beyond C's 12× cap: 24.41×, 16.28×) | 7 | 35 / 36.91 | 35 / 45.01 | 36 / 47.61 |

On the 7 comparable cases Bexh spent *less* than either adaptive system, and reached the same verdict on 6; B2 is the exception.

**The design's falsification test.** The design says: "if … System B + a fixed exhaustive protocol is as accurate as System C at similar cost, then adaptivity adds nothing".
- So far C is more accurate on 1 of the 12 Bexh cases (11 for C-llm, which lacks K2): B2, margin 0.23 points. It is not cheaper on comparable cases.
- The claim that adaptivity adds something over a fixed protocol is therefore **weakly supported and provisional**.
- Bexh's protocol includes the ×2 domain step that moved B1's Cd by 8.86 %, so a Bexh REJECT of B1 is likely (not observed). If Bexh rejects A1, B1 and F1, the difference reduces to B2.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/{B,C-rule,C-llm,Bexh}/*.json`; `results/runs/*/evidence.json` (cell-steps); `docs/design.md` ("Smallest experiment that could falsify the idea").

## Q6. Does the LLM add value?

**Short answer.** By the §19 criterion, scored with a decision rule fixed after 15 of 17 C-llm results were known, no *(provisional on C-llm K2)*.
- **Verdicts.** The LLM planner changes no verdict relative to the rule planner.
- **Cost.** It picks better first experiments on flawed cases but spends more on ambiguous ones, ends level on compute, and costs money.
- **Authority.** It never tried to exceed its authority.

| 16 paired cases | C-rule | C-llm |
|---|---|---|
| verdicts | identical on 16/16 (and on the 3 v1 attacks) | |
| point estimates: correct / false acc. / false rej. | 7 / 0 / 1 (J1) | 7 / 0 / 1 (J1) |
| experiments | 55 | 46 |
| experiment compute (× root) | 77.55 | 77.06 (−0.6 %) |
| planner calls | 74 | 50 |
| proposals refused (limits, duplicates, budget) | 14 | 0 (1 more in the unfinished K2) |
| LLM cost | USD 0 | USD 4.47 |

**By label** (computed for this report):
- **Flawed cases.** The LLM planner is cheaper on the 7 flawed cases: 6 vs 15 experiments, 9.48 vs 18.06 root-units.
- **Ambiguous cases.** It is dearer on the 9 ambiguous ones: 67.59 vs 59.49 root-units, and USD 4.12 of its 4.47.
- **Per case.** It is cheaper by more than 5 % only on B1 (0.78× vs 6.16×) and B2 (1.75× vs 6.94×), and dearer on 7 cases.
- **Quantity level.** Quantity verdicts depend on the planner even when case verdicts agree. On the baseline, only C-rule accepts St; on A2, only C-llm accepts Cd.

**First-experiment targeting** is the one place where the LLM planner is visibly better.
- **Scores.** Its first experiment matched the manifest's revealing primitive on 4/4 flawed cases, against 1/4 for C-rule. On point estimates, with C2 added, it is 4/5 against 1/5.
- **Significance.** All 3 discordant cases favour the LLM; the exact paired test gives p = 0.25.
- **A late rule cost C-rule a hit.** Its F1 miss comes from a rule added after the first results. Under the pre-registered order it would have scored 2/4 (inference from the code).
- **The cues were visible to any planner.** The LLM cited configuration features ("blockage_ratio 0.125", "'Gauss upwind'"), which a rule could also read. No such rule was tested.

### Criterion 5b

§19 names no metric. The rule was committed at 10-20 09:17 (3ee09b1), after 15 of 17 C-llm results were known.
- **Accuracy.** The LLM planner must make more correct decisions in either label view, and no more false acceptances or rejections in either.
- **Cost.** Both must hold: (i) total paired cell-steps relative to the root are lower; (ii) an exact two-sided sign test over cases whose costs differ by more than 5 % gives p < 0.05 in its favour. LLM fees count against it, and wall time is excluded.

**Outcome.**
- Accuracy is tied in both views.
- Cost leg (i) holds narrowly (77.06 vs 77.55).
- Cost leg (ii) fails: 9 cases differ, 2 favour the LLM and 7 the rule, p = 0.18.
- **5b is not met.** K1, the first result after the rule, went against the LLM (10.06× vs 6.77×, both INCONCLUSIVE).
- **K2 is the only open case.** Only a C-llm ACCEPT of K2 can flip 5b: on accuracy, on one case that is ambiguous in the mitigation view. The cost leg cannot flip, because C-llm's four K2 experiments already cost 4.20× against C-rule's 3.74×.
- **An ACCEPT looks unlikely.** In the last recorded planner text (the state after four experiments, recorded at 12:25), Cd's domain component was 3.69 % and St's mesh and domain components 2.19 % and 2.24 %, all of which must fall to ≤ 1.5 %. The fifth experiment, a third domain level, finished at 12:25; the sixth and last, a REFINE_MESH ×1.3 of the root, started at 12:26.

**Is C-rule a fair opponent?** Only partly. Two RUN_LONGER rules were added after early results. One of them (for the regime check) cannot discharge its target, cost 15 % of C-rule's compute, and caused its F1 targeting miss. These deviations favour the LLM planner, which still does not win on cost. Neither C-rule exactly as written in §19 nor a rule informed by the static warnings was run.

### What the LLM costs

LLM spend at about 12:15 UTC (computed for this report from stored results):

| | calls | USD |
|---|---|---|
| C-llm benchmark (16 results) | 50 | 4.47 |
| C-llm-r2 repeat (14 results) | 44 | 4.11 |
| C-llm-v1 and C-llm-v1+review attacks | 13 + 13 | 1.25 + 1.29 |
| L-judge, benchmark and attacks | 17 + 3 | 0.54 + 0.09 |
| **final results** | 140 | **11.75** |
| unfinished loops (C-llm K2; C-llm-r2 C2, F1, K2) | 5 + 9 | 0.39 + 0.72 |
| superseded loop attempts after restarts and relaunches (lower bound) | ≥ 38 | ≥ 2.64 |
| **recorded total** | | **≥ 15.49** |

- **Per call.** A C-llm planner call costs USD 0.089 on average (0.050–0.141) and takes 28.5 s, 1.3 % of C-llm's experiment wall time.
- **Per case.** USD 0 on static REJECTs, 0.05–0.13 on REJECTs by experiment, and 0.31–0.60 on ambiguous cases.
- **Aborted loops.** The superseded attempts, and their 3.85 × 10⁹ cell-steps of unnamed runs, appear in no result.

### Reliability and audit

- **Authority was never tested under pressure.** All 134 recorded LLM planner decisions were MORE_EVIDENCE. There were 0 ACCEPT/REJECT proposals and 0 authority violations.
- **Untraceable numbers** (stored audit fields; the triage file is stale and lists 24 for C-llm):
  - benchmark: C-llm 46 (against 2,248 traced), L-judge 27, C-llm-r2 35 (14 results);
  - attacks: C-llm-v1 9, +review 10, L-judge 6.
- **What they are.** All were read: budget arithmetic, percent conversions and ratios. The three flagged as possible leakage are arithmetic on package values (for example 1.1699 × (0.16/0.15)² ≈ 1.33). The audit cannot show whether prior knowledge shaped the choice of experiment.
- **Run-to-run variance.**
  - The 12 complete repeat sets in the tables have identical verdicts in 12/12 and identical experiment sequences in 7/12; with E1, G2, F1 and C2, which landed later (by 12:30), 16/16 and 7/16.
  - Cost and quantity verdicts vary more than case verdicts: K1 costs 10.06× vs 8.25× (E1 6.50× vs 8.46×), cost differs by more than 5 % in 8 of 16 pairs, and 2 of 32 quantity verdicts differ (A2 Cd ACCEPT vs INCONCLUSIVE; K1 St INCONCLUSIVE vs ACCEPT) (computed for this report).
  - Repeats reuse stored runs, so they measure planner-choice variance only.

### What the LLM saw but could not act on

- **X2.** C-llm-v1 wrote: "the measured inlet is not uniform. The verifier did not flag this, so I cannot treat it as a FAIL." It then spent 8.97× root and ended INCONCLUSIVE.
- **X1.** Its package showed the cylinder extent as 0.0105 m against 0.01 m configured. Neither C-llm-v1 nor +review mentioned it. L-judge cited it as its first reason to REJECT.
- **The acceptance review never ran.** It acts only on a deterministic ACCEPT, and none occurred.

### L-judge: a strong baseline, and its limits

| benchmark | L-judge | C-llm |
|---|---|---|
| detection / false acceptance (mitigation) | 7/7 / 0/7 | 7/7 / 0/7 |
| ambiguous cases | 7 ACCEPT, 2 REJECT, 1 INC | 0 ACCEPT, 1 REJECT, 8 INC |
| correct acceptance / false rejection (point) | 4/5 / 1/5 | 0/4 / 1/4 |
| cost | USD 0.54, no simulations | USD 4.47, 77.06 root-units |

On the scored metrics L-judge matches or beats every verifier-based system. Its limits:
- **No numerical bound.** Its ACCEPTs come without one. On the baseline it notes that no refinement study exists and accepts anyway.
- **Errors between τ/2 and τ.** Three of its ACCEPTs fall in that band: K1 (Cd 1.90 %), E1 (1.89 %) and G2 (St 1.52 %).
- **A departure it noticed.** On E1 it noted that no-slip side walls do "not match 'unbounded'" and accepted. Under the set-up reading that is a false acceptance.
- **Visible flaws.** The benchmark flaws are visible in the configuration.
- **Attack fields.** Its X1 and X2 detections used extractor fields added together with the attacks (0ce5d5e 07:30; 8161f5c 07:40).
- **Hidden flaws untested.** Its rate on flaws hidden from both the configuration and the extractors is unmeasured.

*Sources:* `reports/benchmark_tables.md` (criterion 5b, variance); `results/benchmark/metrics.json`; `docs/methodology.md` §5, §6, §8 ("Decision rule for success criterion 5b"); `results/benchmark/{C-rule,C-llm,C-llm-r2,L-judge}/*.json` and `*.partial.json`; `results/attacks/*/*.json`; `results/analysis/run_audit.md`; git 0ce5d5e, 8161f5c, 10f8b80, 1df98b8, 3ee09b1.

## Q7. What failures remain?

**No verifier-based system accepted a wrong answer at case level, but none accepted anything.** The other failures cluster around that gap.

| | failure | consequence |
|---|---|---|
| 7.1 | no case-level ACCEPT from any verifier-based system | correct acceptance 0/5 (C-rule), 0/4 (C-llm) |
| 7.2 | J1 rejected for 48 stretched far-field cells | the only point-estimate false rejection |
| 7.3 | REFINE_MESH diverges on C1/C2, and the verdict says no refinement ran | mesh error never measured; C2 missed; the failure is hidden |
| 7.4 | wrong-problem errors invisible to v1 | X1, X2 undecided; one quantity-level false ACCEPT |
| 7.5 | quantity-level REJECT lands on the accurate quantity (X3) | misleading diagnosis |
| 7.6 | calibration holds only on the benchmark | U says nothing about set-up errors |
| 7.7 | a gate check that no experiment can clear | 13 continuations, 16 % of C-rule's compute (15 % from a late rule) |
| 7.8 | per-iteration checks not stored; abandoned attempts erased | provenance gaps |

### 7.1 What blocks acceptance

**The post-hoc analysis.** It was not pre-registered. It replayed every stored run graph and listed the components that did not PASS.
- **Benchmark systems with experiments:** 60 quantities are blocked. The domain component alone (U > τ/2) blocks 17, and appears among the blockers in 45 (summed from the table rows for this report).
- **Attacks with experiments:** the domain component blocks all 11 blocked quantities.

Three mechanisms combine.
1. **The per-component τ/2 rule.** On C-rule's baseline graph, Cd has mesh 1.15 %, time 1.10 % and domain 1.81 %. The combined U would be 2.42 %, within τ, and the true error is +1.20 %. The domain component alone keeps Cd INCONCLUSIVE.
2. **The domain primitive.**
   - The baseline's Cd domain component exceeds 1.5 % in every graph: C-rule 1.81 %, C-llm 1.74 %, C-llm-r2 1.88 %, Bexh 3.89 %, and the full 11-run study 2.62 %.
   - Far-field coarsening inflates it.
   - The adaptive values are lower than the study's mainly because their 80 D/U domain levels had not settled (100–150 D/U were needed); C-llm-r2's chain also stops at ×3, which alone keeps it below 2.62 %.
   - A far-field-refined chain would still give 1.56 %, and ×4 is the primitive's limit.
   - **With the current primitive and rule, the baseline drag cannot be accepted.**
3. **Other blockers:** mesh components above τ/2 on A2 and K2; unmeasurable mesh components on C1 and C2 (7.3); and gate checks with no discharge path (physics_regime on 10 results, courant_number on 5; 7.7).

Looser acceptance rules would accept the credible cases, and also X1 (Q8.5).

### 7.2 J1: a false rejection from a mesh heuristic

- **The case.** J1's errors are 0.56 % and 1.11 %. It is credible on point estimates; with the mitigation it is ambiguous, because St straddles τ/2.
- **The verdicts.** Every system with a J1 result REJECTs it. A, B and the adaptive systems do so on the `-allGeometry` "small determinant" flag for 48 cells at 47.3 D; L-judge cites the failed checkMesh together with the coarse wake and the missing refinement study. The default checkMesh says "Mesh OK".
- **Inconsistent application.** The rule is applied to roots only. Children failing the same flag are used as evidence: the baseline's ×2 and ×4 domain meshes (152 and 264 cells, 57.5–155.1 D) and B2's decisive ×4 member.
- **A post-hoc variant** treats such flags as INCONCLUSIVE. It moves J1 to INCONCLUSIVE and changes nothing else, but it covers only 13 of 17 cases, and its adaptive run was not done.
- **Bexh J1** is still running. A REJECT is expected, but that is a prediction.

### 7.3 Refinement diverges, and the verdict hides it

- **The defect.** REFINE_MESH keeps Δt when the parent's maximum Courant number exceeds 1. (The Courant number is how many cells the flow crosses per time step.) The C1 root is at 3.42 and the C2 root at 2.92, so a finer mesh raises it further.
- **What happened.**
  - Every root refinement that ran diverged: C1 at ×1.3, ×√2 and ×2; C2 at ×√2 and ×2. Each crashed with a floating-point exception at a Courant number of about 10¹⁰²–10¹⁰³. A C-llm-r2 ×1.3 refinement of the C2 root also crashed with a floating-point exception, at 12:29, after the run audit.
  - Bexh then refined the diverged runs, and those diverged too.
  - All 8 failed runs in the store at 11:19 are this family: 7 refinements plus the discarded C1 root. The C2 ×1.3 refinement makes it 9.
- **The hidden failure.** The verifier drops failed children, so its verdicts read "no REFINE_MESH experiment has been run; mesh error … is unknown". That text is false, and the divergence appears nowhere in the verdict. This breaks the "no hidden failures" rule.
- **Consequences.** C1 (credible on point estimates) cannot be accepted. C2 (flawed on point estimates) is missed by every system.

### 7.4 Wrong-problem errors

- **Accurate solutions of the wrong problem.** X1 and X2 solve a different problem accurately. Every v1 system ends INCONCLUSIVE with no failed check.
- **U misses X1.** On X1, U misses the error in all 6 rows. For example, under C-rule-v1 the St U is 1.62 % against a true error of −3.60 %, and that St was accepted.
- **What catches them.** Only the post-hoc v2 checks (measured cylinder 0.0105 m vs 0.01 m; inlet velocity 0.1125–0.1875 m/s around a uniform 0.15 m/s) and L-judge REJECT them.
- **Cost unmeasured.** v2's false-rejection rate on the benchmark is unmeasured.

### 7.5 A quantity-level REJECT can land on the accurate quantity

X3's errors partly cancel on St: Cd is +5.81 %, St +0.16 %.
- **C-rule-v1 and v2** REJECT St on a 4.36 % mesh change and leave Cd INCONCLUSIVE (mesh U 3.56 %).
- **The case verdict is right,** and St is genuinely not converged.
- **The diagnosis is not.** A user reading the per-quantity verdicts would be pointed at the wrong quantity.

### 7.6 Calibration is narrower than it looks

- **Benchmark coverage: 36 of 37.** The one miss is I1 under Bexh (Cd 11.05 % vs U 4.21 %), a normalisation error that no discretisation U is meant to see; Bexh rejects I1 statically.
- **Attack coverage: 4 of 10.** Every X1 row is missed.
- **U and T share the Richardson/Celik machinery,** and the baseline rows share runs.
- **Wide U values cover easily** (Bexh K1 Cd U 17.89 %).

### 7.7 A gate that cannot be cleared

- **The gate.** physics_regime is evaluated on the root only, so no continuation can change it.
- **The rule that chases it.** A rule added after the first results (10f8b80) has the rule planner request RUN_LONGER whenever the check is INCONCLUSIVE.
- **The cost.** C-rule made 13 continuations for this reason (F1 4, G1 4, G2 5): 3.98 × 10⁹ cell-steps, 16 % of its experiment compute. 12 of them, 15 %, are attributable to the rule.
- **G1.** C-rule spent its whole budget this way and never measured mesh, time or domain.

### 7.8 Record-keeping gaps

- **Per-iteration checks are not stored.** Intermediate reasons survive only in planner text (example: C-llm F1, criterion 3).
- **The run store keeps one record per run id.** It re-runs a dead owner's configuration under the same id.
- **The run audit**, rebuilt from git, gives lower bounds:
  - 96 earlier attempts;
  - 15 superseded LLM loop attempts (≥ USD 2.64, 38 iterations) that appear in no result;
  - 32 runs named by no stored result;
  - 7 orphaned 'running' records: 5 left by the two container restarts (10-20) and 2 by the code relaunches on 10-19 (08:25 and 09:08).

*Sources:* `results/posthoc/acceptance_rule.md` ("What blocks acceptance", "Gates"); `reports/benchmark_tables.md`; `reports/baseline_validation.md` §6; `docs/methodology.md` §8; `results/posthoc/` (J1 logs, `flagged_cells.txt`, `B-allgeo/`); `results/attacks/*/*.json`; `results/analysis/run_audit.md`.

## Q8. What is the false-acceptance rate?

**Short answer.**
- **Case level:** zero for every verifier-based system, on the benchmark and the attacks, in every view and reading. System A: 6/7 (7/8).
- **Quantity level:** one false acceptance (X1 St, C-rule-v1).
- **The zeros are weak evidence:**
  - n is small;
  - the cases share runs and an author;
  - nothing was accepted;
  - a looser rule would have accepted X1.

### 8.1 Benchmark, case level

| system | results | mitigation (7) | point est. (8) | set-up reading, mitig. (8: +E1) | set-up reading, point (9) |
|---|---|---|---|---|---|
| A | 17 | **6/7** | **7/8** | **7/8** | **8/9** |
| B, C-rule | 17 | 0/7 | 0/8 | 0/8 | 0/9 |
| L-judge | 17 | 0/7 | 0/8 | **1/8** (E1) | **1/9** (E1) |
| C-llm (System C) | 16 | 0/7 | 0/8 | 0/8 | 0/9 |
| Bexh *(provisional)* | 12 | 0/3 | 0/4 | 0/4 | 0/5 |
| C-llm-r2 *(provisional; incl. E1, G2)* | 14 | 0/6 | 0/6 | 0/7 | 0/7 |
| upper bound for 0/n | | 0.348 | 0.312 | 0.312 | 0.283 |

- **Set-up columns.** They follow from the generated note that only E1 changes label under that reading.
- **Smaller n.** For 0/3, 0/4, 0/5 and 0/6 the bounds are 0.632, 0.527, 0.451 and 0.393.
- **Unscored accepts of ambiguous cases.** A ACCEPTs C2, whose best-estimate error exceeds τ. L-judge ACCEPTs three cases between τ/2 and τ.

### 8.2 Attacks, case level

None of the 21 attack results is an ACCEPT; A was not run.

| reading | flawed attacks | false acceptances (each system) | upper bound |
|---|---|---|---|
| set-up | 3 | 0/3 | 0.632 |
| literal; narrow with mitigation (X2 ambiguous) | 2 | 0/2 | 0.776 |
| narrow, point estimates (X2 credible) | 2 | 0/2 | 0.776 |

### 8.3 Quantity level

| group | system | quantity verdicts | quantities with error > τ | of these ACCEPTed |
|---|---|---|---|---|
| benchmark | B / C-rule / C-llm | 33 / 33 / 31 | 10 each | 0 |
| benchmark | Bexh / C-llm-r2 (incl. E1, G2) | 23 / 27 | 4 / 7 | 0 |
| attacks | each system except C-rule-v1 | 6 | 3 | 0 |
| attacks | C-rule-v1 | 6 | 3 | **1** (X1 St) |

The column of quantities with error > τ was computed for this report from `labels.json` and the stored verdicts.

**The X1 St ACCEPT.**
- **The numbers.** All components were inside their limits: mesh 1.35 %, time 0.33 %, domain 0.84 %, combined U 1.62 %. The true error is −3.60 %.
- **Rate.** That is 1 of 3 for C-rule-v1 (one-sided 95 % Clopper–Pearson upper bound 0.865).
- **The cause.** The cause is the set-up error: the numerical uncertainty of the problem actually solved, a 10.5 mm cylinder, really is small. The verifier worked as designed, but a user would read "St is good to 3 %", and it is not.

### 8.4 Near misses: X1 under the pre-registered verifier

| system | X1 Cd components (mesh / time / domain) | X1 St | end of loop |
|---|---|---|---|
| C-rule-v1 | 0.57 / 1.09 / **1.92 %** (0.42 over 1.50 %) | ACCEPT | planner stopped, 5 experiments (6.63×); a further domain step refused at the ×4 limit |
| C-llm-v1 | 1.09 / 1.09 / **1.76 %** (0.26 over) | INC (domain 1.94 %) | experiment budget exhausted (8.04×) |
| C-llm-v1+review | 1.09 / 1.09 / **2.10 %** (0.60 over) | INC (domain 1.74 %) | budget exhausted (7.95×); review never invoked |

- **The margin.** A case-level false ACCEPT of X1 was prevented by domain components 0.42–0.60 points over their limit, taking the larger blocker in each system: C-rule-v1 Cd 1.92 %, C-llm-v1 St 1.94 % (its Cd is 1.76 %, 0.26 over) and C-llm-v1+review Cd 2.10 %.
- **Possible inflation.** That component is plausibly inflated by far-field coarsening: C-llm-v1's planner noted last wake cells of 1.97 and 2.93 D, against 1.02 D. This was not measured on X1.
- **Not detection.** Safety on X1 is a by-product of conservatism.

### 8.5 What a looser rule would accept (post hoc)

| rule | benchmark case ACCEPTs (all credible on point estimates) | attack case ACCEPTs (all false) | quantity ACCEPTs with error > τ |
|---|---|---|---|
| V0, pre-registered | 0 | 0 | 1 |
| V1, combined U only | 6: C-rule baseline, A2, K2; C-llm baseline, A2; C-llm-r2 baseline | 3: X1 in C-rule-v1, C-llm-v1, C-llm-v1+review | 6 |
| V2, no τ/2 limit on the domain | 3: the baseline in C-rule, C-llm, C-llm-r2 | 3: the same X1 results | 6 |

- **Benchmark side.** Under V1, none of the 21 benchmark quantity ACCEPTs has an error above τ/2. Point-estimate correct acceptance would become C-rule 3/5, C-llm 2/4 and C-llm-r2 1/4.
- **Attack side.** Every v1 adaptive system would falsely accept 1/2 flawed attacks (1/3 under the set-up reading). What the acceptance review would have done on those states is unknown.
- **The v2 checks.** B-v2 and C-rule-v2 reject X1 and X2 under every variant.
- **The practical point.** Relaxing the rule without a set-up check would turn today's acceptance failure into a false acceptance on X1. Fixing the domain primitive could do the same if it brings X1's domain components below τ/2, which was not measured. The analysis assumes the planners would have chosen the same experiments.

### 8.6 What the zeros are worth

- **Pooling C-llm's benchmark and attack results** gives 0/9 (bound 0.283) on narrow labels with mitigation, 0/10 (0.259) on narrow point estimates, and 0/11 (0.238) or 0/12 (0.221) under the set-up reading. These are optimistic, for three reasons:
  - **shared construction:** the benchmark and attack cases are variants of one base case, built by the same process, so they are not independent draws (runs shared across systems, 45 of 111 distinct experiment runs of C-rule, C-llm, Bexh and C-llm-r2 at 11:19, affect comparisons between systems, not this count; computed for this report);
  - **one author:** one author planted one flaw per case, in cases built to complete;
  - **repeats are not new trials:** C-llm-r2 measures planner-choice variance.
- **Robust to the T revisions.** Both views' flawed sets are unchanged under every committed T.
- **Reproducible.** The 11:19 re-run reproduced all 92 verifier verdicts. The strict replay is pending.

*Sources:* `reports/benchmark_tables.md`; `benchmark/labels.json`; `results/posthoc/acceptance_rule.md` ("Findings", V0–V2 tables); `results/attacks/{C-rule-v1,C-llm-v1,C-llm-v1+review}/X1_cylinder_geometry.json`; `docs/methodology.md` §6, §8.

## Q9. What is the compute overhead?

**Short answer.**
- Static verdicts cost nothing extra.
- An adaptive REJECT of a flawed case costs 0.8–6.9× the root run.
- An adaptive INCONCLUSIVE costs 2.7–12.0×, often the full budget.
- The cost of an ACCEPT is unknown.

The unit is the root run's cell-steps (cells × time steps). The 17 roots together hold 5.71 × 10⁹ cell-steps and took 9.00 h (computed for this report).

| system | cases | experiments | mean extra compute per case (× root) | range | experiment wall time | LLM |
|---|---|---|---|---|---|---|
| A, B, L-judge | 17 | 0 | 0 | 0 | 0 | L-judge USD 0.54 |
| C-rule | 17 | 59 | 4.78 | 0–11.42 | 31.73 h | — |
| C-llm | 16 | 46 | 4.82 | 0–11.95 | 30.31 h | USD 4.47 |
| Bexh | 12 | 57 | 7.73 | 2.53–24.41 | 33.66 h | — |

The means cover different case sets; paired comparisons are in Q5 and Q6. By outcome, on the 16 paired cases:
- **Static REJECT** (D1, H1, I1, J1): 0 for both adaptive systems. Bexh still spent 5.11× on D1 and 6.51× on I1.
- **REJECT by experiment** (A1, B1, B2, F1): C-llm 0.78–4.80× (mean 2.37×); C-rule 1.06–6.94× (mean 4.52×).
- **INCONCLUSIVE** (8 ambiguous cases): C-rule 2.72–11.42× (mean 7.44×); C-llm 4.81–11.95× (mean 8.45×).
- **Budget exhaustion.** Four C-llm results ended on the experiment budget. For C-rule, two ended on the experiment budget and one on compute.

**Cost of an ACCEPT.**
- **The design's expectation.** It expected "~5 extra runs", with "refined runs … 2–8× the root cost" each. The ambiguous cases used about 5 experiments costing 3–12× the root in total, less per run than the design assumed, and still did not reach ACCEPT.
- **An indication only.** Under the post-hoc combined-only rule, loops reach an ACCEPT state after 4–5 experiments at 3.7–7.4× (cost to that state computed for this report). That rule also accepts X1, so this is not the cost of a trustworthy ACCEPT.

**Wall time is contaminated** by CPU oversubscription.
- **Identical work, different times.** Two roots with identical cell-steps took 1,442 s and 4,804 s.
- **Queueing.** C-llm's B2 loop took 35,526 s for 1,962 s of experiments.
- **Consequence.** Latency to verdict cannot be reported for a dedicated machine.

**Shared-store accounting.**
- **Stand-alone costs.** Per-system figures count every run used, including runs another system computed.
- **Double counting.** Summing them over C-rule, C-llm, Bexh and C-llm-r2 at 11:19 gives 8.42 × 10¹⁰ cell-steps against 5.03 × 10¹⁰ in the distinct runs they name (computed for this report).
- **Aborted loops** are outside every figure.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/{C-rule,C-llm,Bexh}/*.json`; `results/runs/*/evidence.json`, `run.json`; `docs/methodology.md` §8; `docs/design.md` ("Major technical risks"); `results/posthoc/acceptance_rule.md`.

## Q10. What is needed for trust?

Here "trust" means an engineer could act on a verdict without redoing the study.

| precondition | state | evidence |
|---|---|---|
| A demonstrated correct ACCEPT | **unmet** | 0 case-level ACCEPTs in 96 results (12:31). Point-estimate correct acceptance 0/5 and 0/4 (bounds 0.45, 0.53); unmeasurable in the mitigation view. |
| No false acceptance | **met here, small n** | 0/7 and 0/8 (bounds 0.35, 0.31); attacks 0/2–0/3; one quantity-level false ACCEPT (X1 St, C-rule-v1) |
| Trustworthy REJECTs | **partly met** | 7 of 8 benchmark REJECTs are correct on point estimates for C-rule and for C-llm. The eighth (J1) is a false rejection from a mesh heuristic. v2's X2 REJECTs are false rejections under the narrow point-estimate reading. |
| An independent reference | **unmet** | U and T share machinery and runs; T needed four stages; the literature confirms it to about 1 %; no second code |
| Valid experiment primitives | **unmet** | EXPAND_DOMAIN coarsens the far field; REFINE_MESH keeps Δt when the parent's Courant number exceeds 1, and every such root refinement diverged (C1 at 3.42, C2 at 2.92); mapped children are unsettled at 80 D/U |
| Blind, held-out flaws | **unmet** | One author wrote the checks (07:00), the cases (07:05), the attacks (07:30) and the v2 checks (07:40), all on 10-19; H1 and I1 are caught by checks built for them |
| Independent review | **unmet** | 52 corrections logged: R1–R35 and E1–E11 from two adversarial reviews run inside the project (the first with independent reviewer agents), and 6 development-log items found during development on real solver output. No outside CFD expert review is recorded. |
| Reproducibility | **minimal** | 1 of 195 runs reproduced (the A1 root in a container: Cd, St and rms Cl identical to full double precision; no field or log hashes compared); no child run reproduced |
| Decision-code and run provenance | **partly met** | 112 benchmark results stamped (12:31), attacks unstamped; strict replay stale; 14 of 17 roots predate output hashing; abandoned attempts erased |
| Authority separation | **met, untested under pressure** | 0 authority violations, but all 134 recorded LLM planner decisions were MORE_EVIDENCE. No ACCEPT/REJECT proposal was ever made, so the refusal path was exercised only in unit tests. |

**Minimum steps before relying on a verdict:**
1. Fix the primitives and add the consistency gate.
2. Build a held-out set by another author, with robustly credible cases.
3. Compare against an independent reference.
4. Have an outside expert review the labels, the error-budget rule and the domain-error model.
5. Reproduce a sample of child runs.
6. Complete the strict replay over every result, stamp the attack results and close the provenance gaps (Q12 item 7).

Until then, a REJECT is evidence worth acting on, with one known failure mode: the J1 REJECT, from a mesh heuristic, is a false rejection on point estimates (1 of 8 REJECTs per adaptive system). A case-level ACCEPT has never been observed. Of the 5 quantity-level ACCEPTs, one is false (X1 St).

*Sources:* `reports/benchmark_tables.md`; `results/posthoc/acceptance_rule.md`; `results/analysis/run_audit.md`; `results/reproducibility/docker_A1_comparison.txt`; `docs/methodology.md` §6–§9; `reports/baseline_validation.md` §4–§6.

## Q11. Is there a product?

**Not yet.** What exists is a working detector of numerically flawed results, with a provenance trail, for one geometry at one Reynolds number.
- **What a buyer would pay for.** Most plausibly a trustworthy ACCEPT ("this number is good to 3 %"), and the verifier has never produced one.
- **No market data.** No data on demand or users were collected. Statements about users below are judgements.

What the measurements say:
- **The gap is real here.**
  - OpenFOAM's diagnostics accepted 6 of 7 flawed cases, on a benchmark built from runs that complete (Q3: not an estimate for real use).
  - External context: an LLM-based OpenFOAM agent (Foam-Agent, arXiv 2505.04997v3) executed 97 of the 110 FoamBench Basic cases. Only 46 (41.8 %) also matched an expert reference field to a normalised mean-square error ≤ 0.1, and 38 had an error > 0.3.
  - That is a different measure on different problems. It shows that "it ran" is not "it is right", not that this verifier would catch those cases.
- **Rejection is cheaper than indecision, but depends on the planner.** On the 7 flawed cases C-llm used 9.48× root in total and C-rule 18.06×. Three were rejected statically at no extra cost, and an experimental REJECT cost 0.78–6.94× per case.
- **Rigour on non-flawed cases is expensive and bought no decision** (on the 8 non-flawed cases that went to experiments: 7.4× for C-rule and 8.4× for C-llm on average, all INCONCLUSIVE; the ninth, J1, was REJECTed statically, a false rejection on point estimates).
- **The acceptance gap cannot be relaxed away**, because looser rules accept X1.
- **A cheap screen competes on detection.** L-judge matched the detection rate for USD 0.54. What the verifier adds is a quantified bound and a refusal to accept without one; here that showed up only as refusals.

**Plausible users** (judgement, untested):
- Teams running automated CFD pipelines, as a gate between "the run finished" and "the number is used". The REJECT side could be piloted on similar canonical flows with a human reviewing each REJECT. 1 of 8 REJECTs per adaptive system (J1) is a false rejection on point estimates, and the flaws were neither blind nor written by another author (Q10).
- Analysts who want the bookkeeping of solution verification automated, with acceptance left to a human.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/{C-rule,C-llm}/*.json`; `results/posthoc/acceptance_rule.md`; `docs/research.md` §5–§6.

## Q12. What to build next

**Shipping rule: a relaxed acceptance rule or a fixed domain primitive ships only with set-up consistency checks.**
- Under v1, both looser rules accept X1 (Cd +5.98 %, St −3.60 %) in all three v1 adaptive systems (for C-llm-v1+review this is the verifier's ACCEPT; the acceptance review was not run on it).
- A better domain primitive would lower U and would plausibly have the same effect: the domain components that blocked X1 were only 0.42–0.60 points above τ/2 in each system (not tested on X1).
- With the v2 checks, B-v2 and C-rule-v2 REJECT X1 and X2 under every variant (no LLM-planner system was run with v2; v2's benchmark false-rejection rate is unmeasured).

1. **A deterministic set-up consistency gate, with its false-rejection rate measured first.**
   - *What it checks:* measured geometry, inlet profile, force reference and fluid properties against the problem statement.
   - *Why:* no v1 check fails on X1: the adaptive loops end INCONCLUSIVE only on a domain component above τ/2, and C-rule-v1 ACCEPTs its St. The planner saw X2's inlet but could not act.
   - *First:* fix the reading of the set-up clause, because under the narrow point-estimate reading the X2 REJECT is itself a false rejection.
2. **A far-field-preserving EXPAND_DOMAIN with 100–150 D/U settling. Ships only with item 1.**
   - *Why:* the domain component alone blocks 17 benchmark quantities in INCONCLUSIVE adaptive results (26 in INCONCLUSIVE cases with the 9 attack quantities, where unblocking X1 is what produces false ACCEPTs; 29 over all 92 results, counting quantities in REJECTed cases). B2's REJECT rests on a coarse-far-field 80 D/U member, shorter than the 100–150 D/U the baseline's domain levels needed to settle.
   - *Limit:* alone it will not let the baseline drag pass, because a refined chain still gives 1.56 %.
3. **A held-out evaluation set.** It should contain:
   - robustly credible cases (Cd error < 0.565 %, St < 1.04 %);
   - flaws written blind by someone else (wrong reference area, wrong density, a hidden viscosity include);
   - clean-configuration attacks that no extractor field exposes;
   - attacks where only one quantity is wrong;
   - an independent reference.
4. **A pre-registered acceptance rule, tested on item 3, shipped with item 1.** V0 accepts nothing. V1 accepts 6 benchmark results that are credible on point estimates (ambiguous with the mitigation), and X1 in all three v1 adaptive systems.
5. **A REFINE_MESH that scales Δt to hold the Courant number, with failed experiments recorded as evidence.**
   - Never launch a child of a failed run.
   - Whether a divergence should count as a FAIL needs its own study.
6. **A discharge path for the regime gate,** and removal of the futile RUN_LONGER rule.
   - Apply the mesh-quality rule to roots and children alike, or adopt the post-hoc `-allGeometry` variant everywhere, and report the effect. J1 is REJECTed for a flag that B2's decisive ×4 member also fails (Q7.2).
7. **Integrity plumbing.**
   - Store every iteration's checks.
   - Stamp the attack results.
   - Run the strict replay automatically.
   - Mark orphaned records as failed.
   - Account for aborted loops.
   - Re-hash or flag the pre-R19 roots.

*Sources:* `results/posthoc/acceptance_rule.md`; `reports/benchmark_tables.md`; `results/attacks/C-rule-v1/X1_cylinder_geometry.json`, `results/attacks/C-llm-v1/X2_inlet_shear.json`; `reports/baseline_validation.md` §3, §6; `docs/methodology.md` §8.

## Q13. What not to build

1. **LLM-issued verdicts.**
   - L-judge scored well, but its ACCEPTs carry no bound, three fall between τ/2 and τ, and it accepted a set-up departure it had noticed.
   - The data do not rule out an LLM screen that can only REJECT.
2. **A more elaborate planner before acceptance works.**
   - The two planners agree on 16 of 16 verdicts.
   - The rule planner's extra cost comes from simple rules, not from a lack of intelligence. Its pre-registered order (mesh and time before domain) cost about 5 root-units each on B1 and B2, and a regime rule added late cost 15 % of its compute. Neither problem needs a cleverer planner.
   - No planner can pass a τ/2 domain blocker, the ×4 cap or a diverging refinement.
3. **More geometries or Reynolds numbers before the domain primitive is fixed.**
   - The reference for the simplest canonical case needed four stages.
   - The regime check is a literature map for this geometry only.
4. **The acceptance review as designed.**
   - It ran 0 times, and the planner never mentioned X1's wrong cylinder extent.
   - Run it offline on the stored states that V1 and V2 accept before building on it.
5. **A fixed exhaustive protocol as the default** *(provisional)*.
   - Its mean cost is the highest (7.73×; 24.41× on G1), but that reflects experiments after static REJECTs (D1 5.11×, I1 6.51×) and the lack of a 12× cap. On the 7 comparable cases it spent less than either adaptive system (36.91 vs 45.01 and 47.61 root-units; Q5).
   - It missed B2.
6. **Heuristics or relaxed rules tuned on this benchmark.** J1 and V1/V2 show the cost; each needs its own study on held-out cases.
7. **Platform features** (interface, multi-solver support, cloud). There is no verified ACCEPT and no demand data.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/metrics.json`; `results/posthoc/acceptance_rule.md`; `results/attacks/C-llm-v1+review/*.json`; `reports/baseline_validation.md` §3–§4; `docs/research.md` §7.

## Success criteria

### C1. Infrastructure and provenance: partly met

> "The full loop runs autonomously on real OpenFOAM simulations, with provenance for every run."

**What holds.**
- **The loop ran end to end on real OpenFOAM v2412.** There are 195 run records. C-rule finished 17/17 cases (59 experiments) and C-llm 16/17 (46). There were 0 authority violations and 0 planner failures.
- **Every run record holds parent, reason, launcher, configuration diff, initialisation, software versions and source commit; every finished record (177 of 195 at 11:19) also holds raw-log hashes.** The 18 'running' records, 7 of them orphaned, have none. Since correction R19 finished records also hold output and final-field hashes.
- **The decision code is fixed.** All 112 benchmark results (12:31) carry the same decision-code fingerprint from a clean tree.
- **One root (A1) reproduced its Cd, St and rms lift exactly** (relative difference 0); output files were not compared.

**What must be qualified.**

| claim | qualification |
|---|---|
| "autonomously" | Each loop decides without a human. The campaign needed operator relaunches: on fixed code (10-19 08:26, and again at 09:08 after the final decision-code commit b65bf88), after a staleness fix (11:04), after two container restarts (10-20 01:15–01:17 and 03:41), and manual launches of Bexh and C-llm-r2. An interrupted loop restarts from the root. |
| "provenance for every run" | 14 roots predate R19, including the baseline and all four criterion-3 roots. 7 'running' records are orphaned; one ran 764 s, recorded only in its log. 32 runs are named by no result. 15 superseded LLM attempts appear in no result. Per-iteration checks are not stored. |
| verdicts reproduce | The strict replay (05:01, 62 results) is stale. The 11:19 re-run reproduced case verdicts, quantity verdicts and combined U for all 92 results, but not every component. Attack results are unstamped. |
| failures visible | All failed runs (8 at 11:19, 9 by 12:29) are recorded, but the verdict text calls a diverged refinement "not run". |

### C2. Baseline credibility: partly met

| part | measured | outcome |
|---|---|---|
| 2a: stationary Cd and St in the τ-widened literature band | Cd 1.3313 (stationary 1.3311), St 0.1634; band Cd 1.2707–1.3699, St 0.1591–0.1710 | **met** (both lie outside the narrow band, Cd 1.31–1.33 and St 0.164–0.166) |
| 2b: verification bounds the uncertainty below τ… | pre-registered verifier, baseline plus 11 study runs | **not met for drag.** Domain component 2.62 % > τ/2 (mesh 0.85 %, time 0.65 %). St ACCEPTed (combined U 1.86 %). |
| …or the report explains why not | | Far-field coarsening inflates the domain U. A refined chain would give 1.56 %, still above τ/2, and ×4 is the primitive's limit (Q7.1). |

**How 2b turns on the τ/2 rule.** The 2b text does not name the per-component τ/2 rule. Combining the full-study Cd components as the verifier would gives about 2.83 % (computed for this report from `results/baseline/summary.json`), which is below τ. This report does not claim 2b's main clause on that basis: the pre-registered verifier is the test, and the figure uses the coarse-far-field chain.

**Is the baseline's answer right?**
- Its errors against T are Cd +1.20 % (0.27–2.14 % with U(T)) and St −0.31 %, both below τ for every T in the interval.
- It is credible on point estimates and ambiguous with the mitigation.
- So the baseline is plausibly credible, not demonstrably credible.

### C3. Primary demonstration: met

> At least one case where the solver completes, OpenFOAM diagnostics see nothing wrong, the static verifier is INCONCLUSIVE, the adaptive system requests an experiment that exposes the flaw quantitatively, and the final verdict is REJECT.

| condition | A1 coarse mesh | B1 small domain | B2 moderate domain | F1 first-order upwind |
|---|---|---|---|---|
| root completes; A ACCEPTs; B INCONCLUSIVE | yes | yes | yes | yes |
| C-llm's exposing experiment | REFINE_MESH ×2: St 4.78 % | EXPAND_DOMAIN ×2: Cd 8.86 %, St 6.65 % | 2 × EXPAND_DOMAIN ×2: Cd 3.39 % | REFINE_MESH ×2 + RUN_LONGER: St 11.45 % |
| C-llm verdict, cost | REJECT, 2.14×, USD 0.05 | REJECT, 0.78×, USD 0.05 | REJECT, 1.75×, USD 0.12 | REJECT, 4.80×, USD 0.13 |
| C-rule (ablation) | REJECT, 3.28 % (1.06×) | REJECT (6.16×) | REJECT (6.94×) | REJECT, 6.74 % (3.90×) |
| C-llm-r2 (repeat) | identical | REJECT via a ×3 domain | identical | REJECT: the same ×2 refinement plus a 300 D/U continuation, St 11.45 % (4.47×) |

All four cases are flawed in both views. A1 also passes the design's "smallest falsification test": B is INCONCLUSIVE, and one refinement shows a change above 3 %.

**Caveats.**
- **Thin margins.**
  - C-rule's A1 change is 3.28 %; after the noise deduction (2 × 0.021 %) its FAIL margin is 0.24 points. C-llm's ×2 refinement gives 4.78 % (margin 1.74 points).
  - B2's FAIL is 3.39 % − 2 × 0.081 % noise = 3.23 %, a margin of 0.23 points. It rests on an 80 D/U ×4 member with a coarse far field (last wake cell 1.99 D) that fails `-allGeometry`. The label is robust (Cd error 4.24 % ± 0.94 %), but the experimental margin is not. Refined, longer domain members would settle it.
- **F1 was not a one-step demonstration.** C-llm's refinement alone did not decide; the stored reason is only the planner's text ("R0 is 'not statistically reliable'"). The decisive comparison, a 350 D/U continuation against an 80 D/U refinement, gives 11.45 %, far above τ.
- **Not blind.** The cases were designed around their revealing primitive by the author of the checks.
- **Pending.** Bexh A1, B1 and F1. The C-llm-r2 F1 repeat (12:23) REJECTed with the same ×2 refinement and a 300 D/U continuation of the root (St 11.45 %, 4.47×).

### C4. Safety: met on the observed data, weakly

> "System C false acceptance rate on flawed cases = 0. Any false acceptance is reported and diagnosed."

| evidence | System C (C-llm / C-llm-v1) | upper bound | C-rule (ablation) |
|---|---|---|---|
| benchmark: mitigation / point estimates | 0/7 / 0/8 | 0.348 / 0.312 | 0/7 / 0/8 |
| attacks: narrow or literal / set-up reading | 0/2 / 0/3 | 0.776 / 0.632 | 0/2 / 0/3 |
| quantity level: benchmark / attacks | 0/10 / 0/3 | 0.259 / 0.632 | 0/10 / **1/3** |

- **Met** at case and quantity level, in every view and reading.
- **Provisional.** The strict replay is pending; the C-llm-r2 F1 and C2 repeats landed at 12:23 and 12:30 (REJECT and INCONCLUSIVE), and K2 cannot change the figure.
- **Weak.**
  - It is met the way a system that always answered INCONCLUSIVE would meet it.
  - n = 7–8 allows a true rate of up to about a third.
  - On X1, System C's case verdict was held by two domain components, Cd 0.26 and St 0.44 points over τ/2, and a looser rule would have accepted X1.
- **The diagnosis clause.** The one false acceptance found is quantity-level, in the ablation (C-rule-v1 X1 St). It is reported and diagnosed in Q8.3–Q8.4.

C4 has not been falsified. It has not been demonstrated either.

### C5. Value test

> "System C must resolve (ACCEPT/REJECT correctly) at least one case that System B leaves INCONCLUSIVE. Otherwise active experiments add nothing." "The LLM planner must beat the pre-registered rule-based planner on accuracy or cost. **Otherwise the report must state that the LLM adds no measurable value.**"

**5a: met, in both views.**
- C-llm correctly resolves A1, B1, B2 and F1, all by REJECT; C-rule resolves the same four.
- **Limits.**
  - There is no resolution by ACCEPT.
  - Two margins are thin.
  - The strict replay does not yet cover C-rule's B2 and F1 results (the 11:19 re-run does).
- The companion claim, that adaptivity beats a fixed protocol, rests on B2 alone *(provisional; Q5)*.

**5b: not met (provisional on C-llm K2).** As §19 requires, this report states that **the LLM planner adds no measurable value on this benchmark** (rule and outcome in Q6).
- The design's sharper line, "if C-rule matches C, then the LLM adds nothing", holds: 16/16 benchmark verdicts and 3/3 attacks match.
- Only a C-llm ACCEPT of K2 would change the result, on one case that is ambiguous in the mitigation view.
- **Two caveats cut in opposite directions.** The C-rule that ran departs from §19 in ways that favour the LLM. The LLM's targeting advantage uses cues that an untested rule could also use.

*Sources:* `docs/design.md` §19; `results/analysis/run_audit.md`; `results/runs/*/run.json`; `results/benchmark/*/*.json` (stamps, checks, cost); `results/posthoc/acceptance_rule.md`; `results/analysis/replay.json` (stale); `reports/baseline_validation.md` §1, §6; `reports/baseline_generated.md`; `reports/benchmark_tables.md`; `docs/methodology.md` §6, §8.

## Deviations from pre-registration and threats to validity

To **pre-register** is to fix hypotheses, metrics and decision rules before seeing results. Here, that is `docs/design.md` §19 as committed in dd548bc. Times are UTC on 10-19 unless stated.

| # | deviation | effect | robustness or mitigation |
|---|---|---|---|
| 1 | **Timeline.** The first roots were created 07:00–07:02 (the rest by 07:35), and A1 finished at 07:06; the protocol was committed at 07:13. The decision code changed in ten commits up to 09:06, six of them after the first committed verdicts (07:30). One fixed the averaging check after it passed G1. | Code shaped with some early verdicts in view | Early results discarded; all 112 benchmark results (12:31) carry the final fingerprint. Not done: replay of the pre-09:06 code. |
| 2 | **Rule planner.** Two RUN_LONGER rules were added after the first results (1df98b8 08:20; 10f8b80 08:59). | C-rule is not exactly the pre-registered ablation | The B1/B2 targeting misses come from the pre-registered order. 5b is not met despite C-rule's inflated cost. |
| 3 | **Reference T.** Built differently from the §19 text (summed one-factor corrections, p = min(observed, formal), model-form terms, a non-primitive ×4 member). Four committed versions from 11:03 to 16:43. All A, B and L-judge results existed before the first, as did 5 C-rule and 5 C-llm results (7 and 6 by the last version) and 2 Bexh results by 3cff05d. An interim interpretation was written at 13:13. | Labels | Flawed sets invariant, so false-acceptance and detection rates are robust. Point-estimate correct acceptance and false rejection carry a caveat. |
| 4 | **Label views.** The mitigation was made concrete at 08:24, after some verdicts. Views were reframed at 11:03 and 13:51. | Which view is the headline | Both views get equal weight here. |
| 5 | **Set-up clause.** Read narrowly in `labels.json`. | X2's label; E1's under the set-up reading | All three readings reported. |
| 6 | **5b rule.** Fixed after 15 of 17 C-llm results (10-20 09:17). | Not blind to those 15 | Fixed before K1 and K2. |
| 7 | **v2 checks and acceptance review.** Committed at 07:40, after the attacks were defined (07:30) and before any ran. L-judge's X1 field (measured cylinder geometry) was added at 07:30, and its X2 field (measured inlet uniformity) at 07:40. | Not blind tests | Reported separately from v1. |
| 8 | **Post-hoc analyses:** the J1 `-allGeometry` variant (13 of 17 cases) and V1/V2. | None: no scored rate | Labelled post hoc. |
| 9 | **Design text after dd548bc.** The mapped-child duration in §18 was cut from 100 to 80 D/U for compute (b8057b0, 07:23, before the first child run was created at 07:24). §13 was aligned with the corrected verifier (averaging bias, order below the band, FAIL noise rule, bias + RSS). | The 80 D/U children are the ones found unsettled (100–150 D/U needed), which affects B2's margin, the adaptive baseline domain U and F1 | The pre-registered text is the dd548bc version. Q12 item 2 asks for 100–150 D/U of settling. |

**Threats to validity.**
- **One author** wrote the cases, checks and attacks within 40 minutes. The detections show consistency, not generalisation.
- **Small n:** 17 cases, 3 attacks, one geometry, one Re. The systems share cases and runs, so pooling across them is invalid.
- **LLM prior knowledge.** The cylinder at Re = 100 is a textbook case with widely published Cd and St. The packages withhold reference values, but the audit cannot exclude that remembered values helped L-judge or the planner. Performance on unfamiliar flows is untested.
- **Shared runs.** Repeats measure planner choice only, per-system compute double counts, and wall time is contaminated.
- **Case selection.** The cases were built to complete, and A used the stricter `-allGeometry` checkMesh.
- **Designed and measured labels differ.**
  - B2 was designed borderline and is flawed (1.41 τ now, 1.007 τ under an earlier T).
  - Six designed-flawed cases are ambiguous with the mitigation.
  - No designed-credible case is credible in that view.
- **Artefacts.**
  - Mapped children are unsettled at 80 D/U.
  - The far field coarsens with the domain.
  - Time convergence is first order for reasons not identified.
  - Mapped versus fresh limit cycles were never compared.

**Responses to the hostile review.**

| point | response |
|---|---|
| "False acceptance 0 is trivial: the verifier never accepts." | **Conceded.** 0 ACCEPTs in 96 results (12:31); point-estimate correct acceptance 0/5 and 0/4, against 4/5 for A and L-judge. Both views get equal weight. V1 shows the verifier is close to accepting credible cases, but also accepts X1 (Q7.1, Q8.5). |
| "Safety on X1 is luck; your top build item breaks it." | **Conceded.** The binding domain component was 0.42–0.60 points over its limit (C-llm-v1 had two blockers, Cd 0.26 and St 0.44 over), and V1/V2 accept X1 in 3/3 v1 adaptive systems. Q12 ships the domain fix only with the consistency gate. |
| "A USD 0.63 LLM judge dominates on every scored metric." | **Conceded for the scored benchmark metrics.** Rebutted only on what scores miss: no bound, ACCEPTs between τ/2 and τ, an accepted set-up departure, attack detections via fields added with the attacks. On the attacks under the narrow point-estimate reading, its X2 REJECT is a false rejection that C-llm-v1 avoids (2/0/1 vs 1/0/0 of 3). Clean-configuration attacks not built (Q6). |
| "One author: detection is not generalisation." | **Conceded.** No blind set exists; v2's benchmark false rejections are unmeasured (Q12 item 3). |
| "Pre-registration is not verifiable; code and truth moved." | **Conceded on timing; quantified:** false acceptance and detection are invariant across T versions, while point-estimate correct acceptance and false rejection are not. Pre-09:06 code not replayed. |
| "C-rule is a strawman." | **Partly conceded.** Two rules were added late, and targeting rests on n = 4. The B1/B2 misses come from the pre-registered order. A §19-exact rule and a warning-informed rule were not run (Q6). |
| "B2 is a thin, artefact-prone call." | **Conceded on the margin** (0.23 points, coarse 80 D/U member). **Rebutted on the label** (4.24 % ± 0.94 %). Not rerun with refined members (C3). |
| "Variance n is tiny and not independent." | **Conceded.** 16 repeat sets at 12:31 (14 at 12:15), all with shared runs: verdicts 16/16, experiment sequences 7/16. Per-quantity verdicts differ in 2 of 32 quantity pairs (A2 Cd, K1 St), and cost differs by more than 5 % in 8 of 16 pairs (computed for this report). No third repeat. |
| "You hid failed and abandoned LLM loops." | **Conceded and quantified:** 15 superseded attempts (≥ USD 2.64), 12 unnamed LLM-planner runs with no live owner (3.85 × 10⁹ cell-steps, 4.4 % of the store's recorded cell-steps), 7 of them orphaned 'running' records, traced to two container restarts and code relaunches (Q7.8). |
| "The F1 demonstration is not clean; C1/C2 is a design defect." | **Conceded** (C3; Q7.3; Q12 items 5, 7). |
| "Calibration and reproducibility are circular." | **Conceded.** Shared machinery; 4/10 attack rows covered; 1 of 195 runs reproduced (Q7.6, Q10). |
| "X3's per-quantity REJECT hits the accurate quantity." | **Conceded.** Per-quantity accuracy is now scored separately (Q7.5). |
| "Provenance and replay have holes where it matters." | **Partly addressed.** The 11:19 re-run covers the two unreplayed attack results. The strict replay is still stale, 14 roots predate R19, and attacks are unstamped. |

*Sources:* `docs/methodology.md` §6 ("Deviations from pre-registration"), §7–§8; `docs/design.md` §19 (dd548bc); `reports/baseline_validation.md` §4; `reports/benchmark_tables.md`; `results/analysis/run_audit.md`; git log.

## Integrity checks and reproducibility

None of these checks changes a result, and only the container reproduction (the A1 root, 10-19) ran a simulation. The replay, re-run, audit and stamp scan are snapshots taken while background processes were writing.

| check | establishes | coverage | result | current? |
|---|---|---|---|---|
| Decision-code stamp | which code produced each verdict | 112/112 benchmark results; 0/21 attack results | all `6406c53bb2011ef5`, clean tree | 12:31 |
| Strict replay (`scripts/replay_verdicts.py`) | verdict, failed checks, every component status and uncertainty | 62 results | 62/62 match | **stale** (05:01): 34 of 96 replayable results uncovered at 12:31 (C-rule 7 incl. B2 and F1, C-llm 2, Bexh 7, C-llm-r2 16, attacks 2) |
| Post-hoc re-run (V0, `scripts/posthoc_acceptance_rule.py`) | case verdict, quantity verdicts, combined U | 92 results | 92/92 match | 11:19; misses C-llm-r2 E1, G2, F1 and C2; weaker than the strict replay |
| Run audit (`scripts/audit_runs.py`) | store vs results vs git history | 195 records | see Q7.8, C1 | 11:19 snapshot |
| Untraced-number triage | LLM numbers not traceable to the package | C-llm 24 of 46 | stored counts in Q6 | **stale** (03:44) |
| Container reproduction | same inputs and binaries give the same answer | A1 root | same run id; Cd, St, Cl rms identical | 10-19; not repeated |
| Software tests | parsers, check logic, Celik maths, aggregation, primitives, loop authority | 99 unit tests | 99 passed | re-run for this report; 8 integration tests not re-run |

**What the A1 reproduction covers.** It shows that single-core runs with identical inputs and binaries are deterministic here. It does not cover mapped or domain-expanded children, parallel runs, other hardware (not recorded) or another OpenFOAM version.

**To do before the numbers are frozen:**
- re-run the strict replay over every result;
- regenerate the untraced-number files, including C-llm-r2;
- re-run the run audit;
- regenerate `metrics.json` and the tables after the last result;
- stamp the attack results.

*Sources:* `results/analysis/replay.json`, `run_audit.md`, `untraced_numbers.md`; `results/posthoc/acceptance_rule.md`; `results/reproducibility/docker_A1_comparison.txt`; `docs/methodology.md` §8–§9; stamp scan and test run for this report.

## Glossary

- **Verification / validation.** Verification asks whether the equations were solved accurately enough. Validation asks whether they were the right equations for reality.
- **Cd, St, Re.** Cd is the mean drag coefficient. St is the Strouhal number, shedding frequency × diameter / speed. Re is the Reynolds number: 100 here, which gives laminar periodic shedding.
- **τ.** The requested tolerance: 3 % relative error on each of Cd and St.
- **D/U.** The convective time unit: diameter divided by free-stream speed.
- **Root run, child run.** The root is the simulation under verification. Experiments derived from it are children.
- **Primitive.** One of the four allowed experiments: RUN_LONGER, REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN.
- **Mapped initialisation.** Starting a child from the parent's flow field interpolated onto the new mesh. Mapped children run 80 D/U.
- **Courant number.** Cells crossed by the flow in one time step. Values above about 1 strain the solver.
- **Richardson extrapolation.** Estimating the zero-error answer from systematically refined runs, assuming error ∝ (step size)^p.
- **Observed and formal order.** The observed order p is measured from three levels. The formal order is what the scheme should give in theory.
- **Celik procedure, Fs.** A standard recipe (Celik et al. 2008) that turns the extrapolation into an uncertainty with a safety factor Fs: 1.25 when p is plausible, 3 otherwise.
- **Component U.** The verifier's uncertainty for one source: statistics, mesh, time or domain. It PASSes if ≤ τ/2. It FAILs if the demonstrated change minus twice the noise exceeds τ.
- **Combined U.** The averaging bias plus the root-sum-square of the other components. ACCEPT needs every component to PASS and the combined U to be ≤ τ.
- **Gate check.** A static check with no uncertainty budget (for example physics_regime). It must pass or be discharged before an ACCEPT.
- **Reference T, U(T).** The best estimate of the true Cd and St, and its uncertainty.
- **Model-form error.** An error in the model or set-up (for example a wrong geometry or inlet profile), not in the discretisation of the stated problem. Refining the mesh, time step or domain of the wrong set-up cannot detect it. In T, the 'far-field model-form term' is the gap between domain chains with and without a refined far field, which is an uncertainty about how the domain primitive builds its meshes.
- **Labels.** Flawed: error > τ or wrong problem. Credible: error ≤ τ/2. Ambiguous: otherwise.
- **Point-estimate and mitigation views.** The point-estimate view applies the §19 rule to best-estimate errors. The mitigation view also calls a case ambiguous when e ± U(T) straddles τ or τ/2, unless it is flawed for every T in that interval.
- **Set-up readings (narrow, literal, set-up).** Three readings of how a departure from the problem statement affects a label: narrow (only set-up problems detected in the evidence count: wrong Re, steady formulation, missing quantity), literal (any other departure makes the case ambiguous unless e > τ), set-up (any departure makes it flawed).
- **False acceptance / correct acceptance / detection / false rejection.** ACCEPT of a flawed case / ACCEPT of a credible case / REJECT of a flawed case / REJECT of a credible case.
- **Case level, quantity level.** A verdict on both quantities together, or on Cd or St alone.
- **Clopper–Pearson upper bound.** An exact binomial bound. For 0 events in n trials, the one-sided 95 % bound is 1 − 0.05^(1/n).
- **Cell-steps, × root.** Compute as cells × time steps. "× root" divides an experiment's compute by the root's.
- **Content-addressed run store.** Runs identified by a hash of their configuration, so identical requests reuse runs.
- **Provenance.** A run's recorded origin: parent, requester, configuration change, code version, file hashes.
- **Decision-code stamp.** A hash of every file that can affect a verdict, written into each benchmark result.
- **Replay.** Re-running the current verifier on a stored run graph to confirm the stored verdict.
- **Untraceable number.** A number in LLM text that the audit cannot match to the evidence package.
- **Pre-registration.** Fixing hypotheses, metrics and decision rules before results are seen.
- **`checkMesh -allGeometry`.** OpenFOAM's extended mesh check. Its "small determinant" test flags stretched far-field cells; it decides J1.
