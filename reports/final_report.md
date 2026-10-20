# Final report: autonomous verification of CFD results (prototype)

> **Status: 2026-10-20, about 15:45 UTC.** Figures come from the sources regenerated at 15:31 UTC (`reports/benchmark_tables.md`, `results/benchmark/metrics.json`, `results/posthoc/acceptance_rule.md`, `results/analysis/`); "computed for this report" marks figures computed from the stored result files. Results stored after 15:31 are not counted.
>
> **Final:** the baseline validation and the reference T; A, B, L-judge, C-rule, C-llm and its repeat C-llm-r2 on all 17 benchmark cases; all 21 attack results; v2 and the LLM acceptance review applied to the benchmark roots; the post-hoc analyses; the strict replay (105/105 match), the classification of all 205 untraced numbers and the run audit. Criterion 5b under the committed rule is final: not met.
>
> **In progress, not waited for** (dependent figures are marked *provisional*): **C-llm-r3**, a third LLM repeat (3 of 17 cases: baseline ACCEPT, A1 REJECT, K1 INCONCLUSIVE); **C-rule-prereg F1 and G1** (5b sensitivity analysis only); **Bexh H1** (REJECT certain, as a static check FAILs; cost pending); **the adaptive J1 run** of the post-hoc `-allGeometry` variant.

## Summary

**Terms.** *Verification* asks whether the equations were solved accurately enough, *validation* whether they were the right ones. This project verifies one finished simulation, the **root run**, for the mean drag coefficient **Cd** and the Strouhal number **St** (dimensionless shedding frequency), at a tolerance **τ = 3 %**. *False acceptance* is an ACCEPT of a flawed case, *detection* a REJECT of one; *correct acceptance* and *false rejection* are an ACCEPT and a REJECT of a credible case; INCONCLUSIVE is safe but undecided. *Case-level* verdicts cover both quantities, *quantity-level* verdicts one. The 17 benchmark cases and 3 attacks are scored separately, in two label views (*mitigation*, *point estimate*); *robustly flawed* means flawed in both. **A** is OpenFOAM's own diagnostics, **B** the static deterministic verifier, **System C** (C-llm) the adaptive loop in which an LLM planner proposes experiments and the verifier alone decides, **C-rule** the same loop with a rule planner. Bounds are one-sided 95 % Clopper–Pearson (for 0 events in n trials, 1 − 0.05^(1/n): 0.348 for n = 7, 0.312 for n = 8).

**Bottom line.** As a *filter* for numerically flawed results the system works on this benchmark: both adaptive planners rejected all 7 robustly flawed cases, and no verifier-based system accepted a flawed case in 120 results. As a *certifier* it works only sometimes. Two repeats of System C issued the only case-level ACCEPTs (K2 and the baseline), both correct on point estimates, but neither reproduces: the baseline was accepted in 1 of 3 LLM runs, K2 in 1 of 2, and the rule planner never accepts. Acceptance depends on which domain sizes the planner happened to run. That freedom gave only correct ACCEPTs here, but on the wrong-geometry attack X1 the pre-registered verifier was held back only by domain components above their limit, by 0.42–0.60 points. Protection against such wrong-problem errors comes from deterministic set-up checks (v2, post hoc), which reject X1 and X2 and changed no benchmark verdict; an LLM review of ACCEPTs is no substitute.

**Answers to the brief.**
- **Q1** As a filter, yes here (7/7 robustly flawed cases rejected, none accepted); as a certifier, not reliably (2 correct ACCEPTs in 120 verifier-based results, neither reproduced).
- **Q2** Detected statically: wrong Re, force normalisation, steady solver; by experiment: coarse mesh, small domains, first-order convection, compensating errors (X3). Missed, safely: C2 and, under v1, the wrong-problem attacks X1 and X2.
- **Q3** OpenFOAM's diagnostics detect only D1 (1/7; 1/8).
- **Q4** The static verifier adds 2 REJECTs and 4 safe INCONCLUSIVEs where A falsely accepts 6, but no ACCEPTs; its post-hoc v2 checks catch X1 and X2.
- **Q5** Adaptivity adds REJECTs of A1, B1, B2 and F1 (0.78–6.94× root); over a fixed exhaustive protocol, only B2.
- **Q6** By criterion 5b the LLM adds no measurable value (17/17 identical verdicts; 83.06 vs 81.29 root-units, p = 0.109; USD 5.13); outside 5b, its repeats made the only two ACCEPTs.
- **Q7** Planner-dependent acceptance; wrong-problem errors invisible to v1; two defective primitives; J1 falsely rejected; an unclearable gate; incomplete records.
- **Q8** System C false acceptance 0/7 and 0/8 (bounds 0.348, 0.312), attacks 0/2–0/3; one quantity-level false acceptance (X1 St, ablation); System A 6/7.
- **Q9** REJECT 0–6.94× root, ACCEPT 5.37× and 7.12×, undecided up to 11.95×.
- **Q10–Q13** Trust needs reproducible, planner-independent ACCEPTs and a deterministic set-up gate; there is no product yet; build the gate first; do not build LLM verdicts or rely on the LLM review.

**Pre-registered success criteria** (§19; "Success criteria"): 1, autonomous loop with provenance, **partly met**; 2, baseline credibility, **partly met**; 3, primary demonstration, **met**; 4, System C false acceptance = 0, **met on the observed data, weakly**; 5a, adaptivity resolves a case B leaves open, **met**; 5b, the LLM planner beats the rule planner, **not met**.

*Sources:* `reports/benchmark_tables.md` (verdicts, both views, criterion 5b and its sensitivity analysis, variance); `results/benchmark/metrics.json`; `results/posthoc/acceptance_rule.md`; `results/benchmark/{C-llm,C-llm-r2,C-llm-r3}/{baseline,K2_fine_large}.json`; `results/attacks/`; `results/posthoc/review-on-accepts/`; `results/analysis/{replay.json,run_audit.md}`; `reports/baseline_validation.md` §1, §6.

## What was built

**The question.** Take a finished OpenFOAM simulation of a two-dimensional circular cylinder at Reynolds number Re = 100 (a 10 mm rod in a 0.15 m/s air stream, treated as unbounded). Are its Cd and St within 3 % of the converged answer: ACCEPT, REJECT or INCONCLUSIVE? Time is in convective units D/U, the time the stream takes to travel one diameter.

**Components** (`src/socrates/`): OpenFOAM v2412 case generation and runner; deterministic evidence extraction; the verifier (14 check types); four experiment primitives, RUN_LONGER, REFINE_MESH, REDUCE_TIME_STEP and EXPAND_DOMAIN (refinement ≤ 2×, ≤ 160k cells, Δt ≥ root/8, domain ≤ 4×; a *mapped* child starts from its parent's field interpolated onto the new mesh and runs 80 D/U); a content-addressed run store (identical requests reuse runs; each `run.json` records parent, reason, launcher, configuration diff, versions and hashes); and the loop, in which a planner proposes one validated experiment at a time while the verdict is INCONCLUSIVE (≤ 6 experiments, ≤ 12 planner calls, ≤ 12× root compute).

**How the verifier decides.** Per quantity, each uncertainty component (statistics, mesh, time, domain) has an estimated relative uncertainty U and PASSes at U ≤ τ/2; the averaging bias PASSes up to τ. **ACCEPT** needs every gate check passed or discharged, every component PASSed, and bias + root-sum-square (RSS) of the others ≤ τ. **REJECT** follows any FAIL, for a sensitivity check a change between the root and the finest member of a study exceeding τ by more than twice the statistical noise. Everything else, including missing evidence, is **INCONCLUSIVE**. Mesh, time and domain U come from **Richardson extrapolation**, which estimates the zero-spacing answer from runs at known ratios, assuming error ∝ spacing^p. With three levels (the root and the two finest members) the **Celik procedure** measures the observed order p and applies a safety factor Fs = 1.25 if p is within 0.5–2× the formal order, otherwise Fs = 3; two levels use Fs = 3. Each member counts with its longest RUN_LONGER continuation.

**Authority over the LLM.** No tools, schema-validated JSON only, and an evidence package with opaque run names and no reference values; an ACCEPT or REJECT from the LLM would be logged as an authority violation and not executed (none in 81 adaptive results). Calls time out after 300 s, with at most 3 attempts (backoff and jitter).

| system | what it is |
|---|---|
| A | OpenFOAM's diagnostics: ACCEPT if the solver completed, checkMesh (`-allGeometry -allTopology`) is OK and steady residualControl is met |
| B | static deterministic verifier on the submitted run |
| L-judge | an LLM judges the evidence alone, without deterministic gating |
| C-llm | **System C** of §19: adaptive loop with the LLM planner; C-llm-r2 and C-llm-r3 are independent repeats |
| C-rule | adaptive loop with the rule planner (ablation), with two RUN_LONGER rules added after the first results |
| C-rule-prereg | C-rule without those two rules, as §19 specifies it (5b sensitivity analysis) |
| Bexh | fixed protocol of 5 experiments (RUN_LONGER, REFINE_MESH √2 twice, REDUCE_TIME_STEP, EXPAND_DOMAIN), no compute cap |
| …-v1, …-v2, +review | attack variants: the pre-registered verifier; v2, with two set-up checks written after the attacks were defined; an LLM review that may only veto a deterministic ACCEPT |

**Scale** (15:31): 206 run records (185 completed, 9 failed, 12 'running'), all OpenFOAM v2412; 136 benchmark results, all stamped with decision-code fingerprint `6406c53bb2011ef5`; 21 attack results, unstamped; 99 unit tests (of the code, not the physics). `README.md` describes the Docker build and the scripts behind every result; C-llm and L-judge also need an LLM command-line client with credentials.

*Sources:* `docs/design.md` §13, §18, §19; `docs/methodology.md` §1–§5, §8; `README.md`; `results/analysis/run_audit.md`; result stamps (computed for this report).

## Benchmark and labels

### The reference T

No published value is converged to τ/2 for this exact set-up, so an in-house reference was built from three refinement chains around the baseline (mesh, time step, domain), each extrapolated with the Celik procedure: **T = Cd 1.3155 ± 0.94 %, St 0.1639 ± 0.46 %.** The ± is U(T), the reference's own uncertainty, dominated by a far-field *model-form* term (0.82 % of Cd: how the domain meshes are built, not discretisation). Published values at matched domain size agree to about 1 %, not to τ/2. T shares the verifier's machinery and, for the baseline, its runs.

### The cases

The baseline plus 16 variants, each a documented change (`benchmark/manifest.yaml`); the author intended 3 to be credible (baseline, K1, K2), 2 borderline (A2, B2) and 12 flawed. The error is e = (reported − T)/T.

| case | change from the baseline | Cd error | St error | point est. | mitigation |
|---|---|---|---|---|---|
| baseline | — (160 cells around, sides ±40 D, Δt 0.01 D/U) | +1.20 % | −0.31 % | credible | ambiguous |
| K1 | central (Gauss linear) convection | +1.90 % | −0.39 % | ambiguous | ambiguous |
| K2 | finer mesh, smaller Δt, larger domain | +0.94 % | −0.07 % | credible | ambiguous |
| A1 | mesh ×0.5 | −1.55 % | −5.08 % | flawed | flawed |
| A2 | mesh ×0.75 | +0.51 % | −1.45 % | credible | ambiguous |
| B1 | domain 8/15/±4 D (blockage 12.5 %) | +14.7 % | +9.57 % | flawed | flawed |
| B2 | domain 15/25/±10 D (blockage 5 %) | +4.24 % | +1.89 % | flawed | flawed |
| C1 | Δt ×5, 3 outer correctors (max Courant 3.42) | +0.64 % | −0.26 % | credible | ambiguous |
| C2 | Euler time scheme, Δt ×4 | −1.93 % | −3.33 % | flawed | ambiguous |
| D1 | steady solver | −17.0 % | not produced | flawed | flawed |
| E1 | no-slip walls on the far-field sides | +1.89 % | +0.21 % | ambiguous | ambiguous |
| F1 | first-order upwind convection | −3.55 % | −23.1 % | flawed | flawed |
| G1 | 40 D/U run, averaged from 10 D/U | −1.47 % | −1.62 % | ambiguous | ambiguous |
| G2 | 60 D/U run, averaged from t = 0 | +0.32 % | −1.52 % | ambiguous | ambiguous |
| H1 | dynamic viscosity entered as ν (Re = 83.3) | +2.52 % | −6.05 % | flawed | flawed |
| I1 | stale force-reference velocity (0.16 vs 0.15 m/s) | −11.1 % | −0.31 % | flawed | flawed |
| J1 | wake streamwise cells ×0.3 | +0.56 % | −1.11 % | credible | ambiguous |

### Two label views, given equal weight

- **Point-estimate view (§19 as written):** flawed if max e > τ or the set-up answers a different problem (D1, H1); credible if max e ≤ τ/2; otherwise ambiguous. **8 flawed, 5 credible (baseline, A2, C1, J1, K2), 4 ambiguous.**
- **Mitigation view:** also ambiguous when e ± U(T) straddles τ or τ/2, unless flawed for every T in that range. **7 flawed (C2 becomes ambiguous), 0 credible, 10 ambiguous.** Credible would need a Cd error below 0.565 % *and* an St error below 1.04 %, so correct acceptance and false rejection are undefined in this view.
- **Which view is primary is contested:** §19 is the point-estimate rule; the mitigation comes from the pre-registered risk list ("label near-boundary cases ambiguous"), made concrete (4639ddb, 10-19 08:24) before any T existed but after some verdicts.

### Three readings of the set-up clause

§19 calls a case flawed "if the set-up answers a different problem (wrong Re or regime)" and credible only "if … the set-up is consistent". The **narrow** reading (used by `benchmark/labels.json`) counts only set-up problems detected in the evidence (wrong Re, steady formulation, missing quantity); the **literal** reading makes any other departure ambiguous unless e > τ; the **set-up** reading makes it flawed. On the benchmark only E1 changes (flawed under the set-up reading, which makes A's and L-judge's ACCEPTs of it false); on the attacks only X2:

| attack | Cd error | St error | set-up | literal | narrow, point est. | narrow, mitigation |
|---|---|---|---|---|---|---|
| X1 cylinder 5 % too large | +5.98 % | −3.60 % | flawed | flawed | flawed | flawed |
| X2 sheared inlet | +1.20 % | −0.50 % | flawed | ambiguous | **credible** | ambiguous |
| X3 compensating mesh/domain errors | +5.81 % | +0.16 % | flawed | flawed | flawed | flawed |

### Designed and measured labels differ; how the reference moved

Six of the 12 intended-flawed cases are not flawed with the mitigation (C1, C2, E1, G1, G2, J1), five not on point estimates: real defects, small effects. B2, intended borderline, is robustly flawed; no intended-credible case is robustly credible. The gap between "plausible but wrong" and "careful" is often smaller than U(T), which limits what the benchmark can show about acceptance.

T was committed in four versions on 10-19 (Cd 1.3133, 1.3134, 1.3046, 1.3155; 11:03–16:43). The last stage found that EXPAND_DOMAIN keeps the per-cell growth rate, so the far field coarsens as the domain grows (last wake cell about 1.0 D at ×1, 3.9 D at ×4); refining the ×4 far field raised Cd by 0.16 %, against 0.03 % at ×1. The verifier's domain component inherits this (Q1). The flawed sets are identical under every committed T, so false-acceptance and detection rates do not depend on the revisions; the point-estimate credible set moved ({baseline, C1, K2} → {A2, C1, G2, J1} → the current five), so correct-acceptance and false-rejection rates, including the two ACCEPTs, carry this caveat. Sensitivity changes are relative to the finer member of a study.

*Sources:* `benchmark/labels.json`; `benchmark/manifest.yaml`; `reports/baseline_validation.md` §1, §3–§5, §7; `docs/methodology.md` §6; `reports/benchmark_tables.md` (attack labels); git log.

## Q1. Does it work?

**As a filter for numerically flawed results, yes on this benchmark. As a certifier, sometimes, but not reproducibly.**

| system | results | false acceptance (mitig. / point) | detection (mitig. / point) | correct acceptance (point) | false rejection (point) | INCONCLUSIVE |
|---|---|---|---|---|---|---|
| A (OpenFOAM diagnostics) | 17 | **6/7 / 7/8** | 1/7 / 1/8 | 4/5 | 1/5 | 0/17 |
| B (static verifier) | 17 | 0/7 / 0/8 | 3/7 / 3/8 | 0/5 | 1/5 | 13/17 |
| L-judge (LLM, evidence only) | 17 | 0/7 / 0/8 | 7/7 / 7/8 | 4/5 | 1/5 | 1/17 |
| C-rule | 17 | 0/7 / 0/8 | 7/7 / 7/8 | 0/5 | 1/5 | 9/17 |
| C-rule-prereg *(F1, G1 pending)* | 15 | 0/6 / 0/7 | 6/6 / 6/7 | 0/5 | 1/5 | 8/15 |
| C-llm (System C) | 17 | 0/7 / 0/8 | 7/7 / 7/8 | 0/5 | 1/5 | 9/17 |
| C-llm-r2 (repeat) | 17 | 0/7 / 0/8 | 7/7 / 7/8 | **1/5** (K2) | 1/5 | 8/17 |
| C-llm-r3 (repeat) *(provisional)* | 3 | 0/1 / 0/1 | 1/1 / 1/1 | **1/1** (baseline) | 0/1 | 1/3 |
| Bexh (fixed protocol) *(H1 pending)* | 16 | 0/6 / 0/7 | 5/6 / 5/7 | 0/5 | 1/5 | 10/16 |

With the mitigation no case is credible, so correct acceptance and false rejection are undefined there; every false rejection is J1 (Q7.2). L-judge matches the adaptive systems' detection without simulations, but with no numerical bound (Q6). One author wrote the cases, checks and attacks: consistency, not a blind test.

**Acceptance happened, but does not reproduce.** Two of the 120 verifier-based results (102 benchmark, 18 attack) are case-level ACCEPTs, both by repeats of System C:
- **C-llm-r2 on K2:** Cd U 1.54 % against a true error of +0.94 %, St U 1.69 % against −0.07 %; 5 experiments, 5.37× root, USD 0.45.
- **C-llm-r3 on the baseline:** Cd U 1.87 % against +1.20 %, St U 1.59 % against −0.31 %; 5 experiments, 7.12× root (all five runs were already in the store), USD 0.42.
- **Both are right:** every component PASSed and U covers the true error: correct acceptances on point estimates. With the mitigation both cases are unscored (ambiguous), but their Cd errors stay below τ for every T within U(T) (0.27–2.14 % and 0.01–1.88 %), so neither is a false acceptance in any view.
- **Neither reproduces:** the baseline was accepted in 1 of 3 LLM runs, K2 in 1 of 2 (a third K2 run is in progress); C-rule, C-rule-prereg and Bexh accepted neither. Correct acceptance per run: C-llm 0/5 (upper bound 0.451), C-llm-r2 1/5 (0.657), C-llm-r3 1/1 so far.

**Why the verdict depends on the planner.** The domain component is estimated from the root and the two largest domain levels the planner happened to run. Levels are multiples of the root's half-height, counted cumulatively (×1.5 applied to a ×2 run gives ×3); a component passes at U ≤ 1.5 %.

| case | system | domain levels run | observed order; Fs | Cd domain U | case verdict |
|---|---|---|---|---|---|
| baseline | C-llm-r3 | ×1, ×1.5, ×2 | 1.55; 1.25 | 1.23 % | **ACCEPT** |
| baseline | C-llm | ×1, ×2, ×3, ×4 | 0.94; 1.25 | 1.74 % | INCONCLUSIVE (St domain 1.85 %) |
| baseline | C-llm-r2 | ×1, ×1.5, ×2, ×3 | 0.82; 1.25 | 1.88 % | INCONCLUSIVE (St domain 1.59 %) |
| baseline | C-rule, C-rule-prereg | ×1, ×2, ×4 | 0.86; 1.25 | 1.81 % | INCONCLUSIVE |
| K2 | C-llm-r2 | ×1, ×2, ×3 | 1.06; 1.25 | 1.27 % | **ACCEPT** |
| K2 | C-llm | ×1, ×2 (continued to 180 D/U), ×4 | 2.79, outside the band; 3 | 2.38 % | INCONCLUSIVE |
| K2 | C-rule, C-rule-prereg | ×1, ×2, ×4 | 1.51; 1.25 | 1.02 % (PASS) | INCONCLUSIVE (St mesh 2.17 %, two levels) |

Against the first C-llm run on the same case, only the domain members differ; mesh and time components are essentially unchanged.
- **Baseline:** C-llm-r2's graph holds the accepting graph's domain runs plus a ×3 member, which raised the Cd domain component from 1.23 % to 1.88 %; every baseline graph that reached ×3 or ×4 is INCONCLUSIVE, plausibly because EXPAND_DOMAIN coarsens the far field (Q7.1).
- **K2:** coarsening did not decide; the accepting chain reached ×3 and C-rule's ×4 chain passes too. C-llm ran its ×2 member longer, the verifier counts each member's longest continuation, and the observed order fell outside the band, which tripled the safety factor.
- **The rule planner never accepts.** Its ×2 steps, continued from the finest member, take the baseline to ×4. On K2 its next mesh step (×√2 from its finest mesh) needs 216,220 cells against the 160,000 limit, so St keeps a two-level mesh estimate; both LLM runs instead refined the root again (C-llm-r2 by ×1.65).
- **Both ACCEPTs use domain members that fail checkMesh `-allGeometry`**, the check that REJECTs J1 when it fails on a root (Q7.2).
- **Safety.** Here the freedom produced only correct ACCEPTs. On X1 (Cd error +5.98 %) the v1 adaptive systems were held back only by domain components above 1.5 %, and another choice of levels could plausibly have brought them below (Q8.3; an inference).

*Sources:* `reports/benchmark_tables.md` (verdict matrix, both views, calibration, per-quantity accuracy, variance); `results/benchmark/metrics.json`; `results/benchmark/{C-rule,C-rule-prereg,C-llm,C-llm-r2,C-llm-r3}/{baseline,K2_fine_large}.json` (domain checks); `results/runs/*/run.json`, `evidence.json` (domain extents, checkMesh); `results/posthoc/acceptance_rule.md`.

## Q2. Which failures does it detect?

| flawed case (errors in the case table) | A | B | L-judge | C-rule | C-llm | Bexh |
|---|---|---|---|---|---|---|
| D1 steady solver | REJ | REJ | REJ | REJ | REJ | REJ |
| H1 Re = 83.3 | ACC ✗✗ | REJ | REJ | REJ | REJ | *pending (REJ certain)* |
| I1 wrong force reference | ACC ✗✗ | REJ | REJ | REJ | REJ | REJ |
| A1 coarse mesh | ACC ✗✗ | INC | REJ | REJ | REJ | REJ |
| B1 small domain | ACC ✗✗ | INC | REJ | REJ | REJ | REJ |
| B2 moderate domain | ACC ✗✗ | INC | REJ | REJ | REJ | INC |
| F1 first-order upwind | ACC ✗✗ | INC | REJ | REJ | REJ | REJ |
| C2 Euler, large Δt (flawed on point estimates only) | ACC (✗✗ point) | INC | INC | INC | INC | INC |

✗✗ = false acceptance; INC = INCONCLUSIVE. C-rule-prereg and C-llm-r2 match C-rule and C-llm wherever they have finished; C-llm-r3 REJECTs A1. L-judge's REJECTs cite features visible in the configuration or the evidence summary.

D1, H1 and I1 FAIL static checks (residualControl and a steady solver above shedding onset; reynolds_consistency, Re 83.33 vs 100; force_reference_consistency, 0.16 vs 0.15 m/s). The other four need experiments:

| case | decisive check | C-rule: path → change (cost) | C-llm: path → change (cost) |
|---|---|---|---|
| A1 | mesh FAIL on St | REFINE_MESH √2 → 3.28 %; 1.06× | REFINE_MESH ×2 → 4.78 %; 2.14× |
| B1 | domain FAIL on Cd and St | 3 other experiments, then EXPAND_DOMAIN ×2 → 8.86 %, 6.65 %; 6.16× | the same domain run first; 0.78× |
| B2 | domain FAIL on Cd: 3.39 % − 2 × 0.081 % noise, a 0.23-point margin, from an 80 D/U ×4 member | 3 other experiments, then two EXPAND_DOMAIN ×2; 6.94× | the same two runs; 1.75× |
| F1 | mesh FAIL on St | 4 RUN_LONGER (St ≤ 0.36 %), then REFINE_MESH √2 → 6.74 %; 3.90× | REFINE_MESH ×2, then RUN_LONGER on the root → 11.45 %; 4.80× |

C-rule's detours on B1 and B2 come from the pre-registered order (C-rule-prereg takes the same paths). C-llm-r2 repeated A1, B2 and F1 with the same refinements and REJECTed B1 through a new ×3 domain run (0.95×). Bexh REJECTs A1, B1 and F1 but not B2 (Q5).

**Planted defects with errors near or below τ.** On E1 and K1 B gives no warning, the adaptive systems end INCONCLUSIVE, and A and L-judge ACCEPT. On C1 and C2 B flags the Courant number, but every refinement of either root diverged (Q7.3). On G1 and G2 B flags the averaging or the regime. J1 is REJECTed everywhere on a flag that only `checkMesh -allGeometry` raises (Q7.2).

**Attacks.**

| attack | B-v1 | C-rule-v1 | C-llm-v1 | C-llm-v1+review | L-judge | B-v2 | C-rule-v2 |
|---|---|---|---|---|---|---|---|
| X1 cylinder +5 % | INC | INC (St ACCEPTed, error −3.60 %) | INC | INC | REJ | REJ | REJ |
| X2 sheared inlet | INC | INC | INC | INC | REJ | REJ | REJ |
| X3 compensating errors | INC | REJ (mesh FAIL on St, 4.36 %; 3.21×) | REJ (domain FAIL, Cd 5.14 %, St 3.83 %; 0.77×) | REJ | REJ | INC | REJ |

X1 and X2 are wrong-problem errors: refining a wrong problem converges to the wrong answer, so solution verification cannot see them (Q7.4). The v2 checks catch both statically but were written after the attacks were defined, and X2's REJECTs are correct only under the set-up reading. X3 is what adaptive verification is for, and every adaptive system rejected it (Q7.5).

*Sources:* `reports/benchmark_tables.md`; `reports/benchmark_results.md` (loop traces, L-judge text); `results/benchmark/*/*.json` (checks with values, noise, runs); `results/attacks/*/*.json`; `results/posthoc/B-allgeo/`; `benchmark/manifest.yaml`.

## Q3. Which failures do OpenFOAM's own diagnostics detect?

**System A**, a careful user reading OpenFOAM's output, ACCEPTed 15 of 17 cases. **Its one detection is D1** (residualControl not met): 1/7, or 1/8 on point estimates. It falsely accepted A1, B1, B2, F1, H1 and I1 (6/7; 7/8 with C2). Its J1 REJECT is incidental, from the extended check ("Cells with small determinant (< 0.001) found, number of cells: 48", all at x ≈ 47 D next to the outlet); default checkMesh prints "Mesh OK." on the same mesh (`results/posthoc/J1_checkMesh_default.log`, line 103).

The rate reflects how the benchmark was built (plausible cases that execute; the one candidate that crashed, a first C1 with Δt ×10, was discarded: `cases/adversarial/DISCARDED.md`), so 6/7 is not an estimate for real use. It does show that completion plus checkMesh says nothing about discretisation error, domain size, force normalisation or Re. A was not run on the attacks; all three roots completed with checkMesh OK, so A would have accepted them (an inference). OpenFOAM does flag divergence: all 9 failed runs in the store crashed with floating-point exceptions.

*Sources:* `results/benchmark/{A,B}/*.json`; `results/posthoc/J1_checkMesh_*.log`, `flagged_cells.txt`; `cases/adversarial/DISCARDED.md`; `results/analysis/run_audit.md` (failed runs); `docs/design.md` §15–§16.

## Q4. What does the deterministic verifier add?

On a single run, B accepts no flawed case (0/7; 0/8), REJECTs D1, H1 and I1 where A REJECTs only D1, and leaves A1, B1, B2 and F1 (and C2) INCONCLUSIVE where A falsely accepts them. The price: it accepts nothing (13/17 INCONCLUSIVE).
- **The extra static detections (H1, I1)** come from set-up consistency checks committed five minutes before the cases by the same author (e27ac5b 07:00, 8d403aa 07:05): consistency, not generalisation.
- **An honest "undecided":** on A1, B1 and B2, 13 of 19 checks PASS and only the six unmeasured mesh, time and domain components are INCONCLUSIVE; static warnings flag F1, C1, C2, G1 and G2.
- **The v2 set-up checks** PASS on all 17 benchmark roots and change no verdict (0/5 credible cases rejected, upper bound 0.451). They catch X1 and X2, but are post hoc and do not flag E1 (no-slip side walls), flawed under the set-up reading. An LLM review of ACCEPTs is no substitute (Q6).

Inside the adaptive loop the same rules decide: a FAIL turns one or two well-chosen experiments into a REJECT, and the per-component τ/2 rule blocks most acceptances, including X1's (Q8.3).

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/B/*.json`; `results/attacks/{B-v2,B-v2-on-benchmark}/`; `results/posthoc/review-on-accepts/`; `docs/methodology.md` §3, §8.

## Q5. What does the adaptive system add?

**Rejections, not acceptances.** The adaptive systems REJECT four flawed cases that B leaves undecided; their first runs ACCEPT nothing, and the only ACCEPTs came from LLM repeats (Q6).
- **Over B:** A1, B1, B2 and F1, flawed in both views and for every T within U(T), go from INCONCLUSIVE to REJECT under both C-rule and C-llm. Detection rises from 3/7 to 7/7 (3/8 to 7/8 on point estimates); false acceptance stays 0/7. Margins are thin on two (C3): C-rule's A1 FAIL is 3.28 % against τ = 3 %, the B2 FAIL 3.23 % after the noise deduction.
- **Most compute goes to cases that stay undecided:** 78 % of C-rule's and 89 % of C-llm's went to the 9 ambiguous cases that ended INCONCLUSIVE.
- **On the attacks,** adaptivity catches X3 (0.77–3.21× root) but not X1 and X2 (6.6–9.0× root, INCONCLUSIVE), and under v1 it is the only route to a false ACCEPT (Q8.3).

**Over a fixed exhaustive protocol.** Bexh (16 of 17 cases; H1 pending) gives C's verdicts on 15 of 16, including REJECTs of A1, B1 and F1 (5.66–6.82× root): detection 5/6 (5/7 on point estimates). **B2 is the exception:** Bexh's one EXPAND_DOMAIN ×2 changed Cd by 2.37 % (< τ), and the two-level estimate (Fs = 3) gave a domain U of 14.23 %: INCONCLUSIVE. Both planners added a second domain step (Cd 1.3713 → 1.3395 → 1.3263, a 3.39 % change: FAIL), C-llm after 2 experiments (1.75×), C-rule after 5 (6.94×). A protocol with two fixed domain steps was not tested.

| experiments / root-units (computed for this report) | cases | Bexh | C-rule | C-llm |
|---|---|---|---|---|
| all cases with a Bexh result | 16 | 77 / 118.03 | 59 / 81.29 | 52 / 83.06 |
| without D1, I1, J1 (Bexh runs its protocol after a static FAIL) and G1, G2 (Bexh beyond C's 12× cap: 24.41×, 16.28×) | 11 | 54 / 59.28 | 49 / 59.88 | 46 / 61.33 |

On the 11 comparable cases the three cost the same within 4 % and agree on 10 verdicts, so the design's falsification test ("if … System B + a fixed exhaustive protocol is as accurate as System C at similar cost, then *adaptivity* adds nothing") is nearly met: C is more accurate on 1 of 16 cases (B2, margin 0.23 points). That adaptivity beats a fixed protocol is **weakly supported**.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/metrics.json`; `results/benchmark/{B,C-rule,C-llm,Bexh}/*.json` (`cost`, `verifier.checks`); `results/attacks/*/X*.json`; `docs/design.md` ("Smallest experiment that could falsify the idea").

## Q6. Does the LLM add value?

**Short answer.** Criterion 5b as committed is **not met (final)**: the first LLM run gives the rule planner's verdict on all 17 cases, with 2.2 % more compute and USD 5.13 of fees. As §19 requires: **the LLM planner adds no measurable value on this benchmark.** Yet only LLM runs certified anything: two repeats correctly ACCEPTed K2 and the baseline (Q1), not reproducibly and through the planner's choice of levels, a freedom that could yield a false ACCEPT of X1 under v1 (Q8.3). The LLM acceptance review does not close that gap.

### Criterion 5b

C-rule and C-llm's first run give identical verdicts on all 17 paired cases (and on the 3 v1 attacks): 7 correct decisions each in both views, no false acceptance, one false rejection each on point estimates (J1). C-rule used 59 experiments (81.29× root) and 80 planner calls, 15 of its proposals refused by the validator; C-llm used 52 experiments (83.06×, +2.2 %), 57 calls, 1 refused, and USD 5.13.

**Rule** (methodology §8; 3ee09b1, 10-20 09:17, after 15 of 17 C-llm results were known): the first LLM run against C-rule. Accuracy: more correct decisions in either label view and no more false ones in either. Cost: lower total compute **and** an exact two-sided sign test over cases differing by more than 5 %, p < 0.05 in the LLM's favour; fees count against it, wall time is excluded.

**Outcome: not met.** Accuracy is tied; compute is higher, and only 2 of 10 differing cases favour the LLM (B1, B2), p = 0.109. K1 and K2, the results after the rule was fixed, both went against it (10.06× vs 6.77×; 6.00× vs 3.74×). It is cheaper on the 7 flawed cases (9.48 vs 18.06 root-units) and dearer on the 10 ambiguous ones (73.58 vs 63.23; computed for this report).

**Sensitivity: the rule planner as literally pre-registered** (C-rule-prereg; Deviations, item 2). On its 15 finished cases it gives C-rule's verdicts, and the LLM fails 5b against it too (accuracy tied at 6; 68.47 vs 67.92 root-units; p = 0.18) *(provisional)*. **F1 can flip the accuracy leg:** replaying the verifier on C-rule-prereg's partial F1 graph leaves every sensitivity component unmeasured, because the root is "not statistically reliable" and the literal order never runs it longer (computed for this report). If F1 ends INCONCLUSIVE, the LLM meets 5b in this analysis (7 vs 6 correct); the committed result stands either way.

**Qualifications.** Scored instead of the first run, C-llm-r2 would meet the accuracy leg on point estimates (8 vs 7, via K2): the outcome depends on which LLM run is scored. A rule planner that reads B's static warnings was not run. The first run's one visible edge is **first-experiment targeting** (4/4 flawed cases against 1/4 for C-rule; exact p = 0.25), from cues ("blockage_ratio 0.125", "'Gauss upwind'") a rule could read too. **The two ACCEPTs** came from choices the rule planner does not make: C-llm-r3 took a ×1.5 domain step from the baseline root, reasoning that the ×2 member "is confounded by checkMesh_ok=false and a coarser far-field mesh"; on K2 both LLM runs refined the root again for a third mesh level (C-llm-r2 by ×1.65, "about 148000 cells"). With 1 accepting run of 3, the 95 % bounds on the baseline's acceptance rate are 0.017 and 0.87: it is unmeasured.

### Variance, cost and authority

- **Run-to-run variance.** C-llm vs C-llm-r2: same verdict in 16 of 17 cases (lower bound 0.75), same experiment sequence in 7, cost differing by more than 5 % in 9, 3 of 34 quantity verdicts different (computed for this report); C-llm-r3 so far: 2/3 and 1/3. Repeats reuse stored runs, so they measure planner choice only.
- **Spend.** 176 stored LLM calls cost USD 15.17, plus at least USD 2.64 in superseded loop attempts; a planner call averages USD 0.090 and 28.2 s.
- **Authority was never tested under pressure:** all 152 recorded LLM planner decisions were MORE_EVIDENCE.

### Untraced numbers, classified

An *untraced number* is a number in LLM-written text that the numeric audit could not match, at its printed precision, to the evidence package that call received. **205 of 7,758 audited numbers (2.6 %) are untraced, and all were classified.** For each of the 135 calls concerned the package was rebuilt; re-running the audit on it reproduces the stored untraced lists for 135 of 135 calls, and every derivation's operands were checked against that package or the same output.

| system (phase) | untraced | derived arithmetic | restated convention | rounded package value | unclear |
|---|---|---|---|---|---|
| C-llm (benchmark) | 59 | 56 | 2 | 1 | 0 |
| C-llm-r2 (benchmark) | 86 | 83 | 2 | 0 | 1 |
| C-llm-r3 (benchmark, 3 of 17) | 8 | 8 | 0 | 0 | 0 |
| L-judge (benchmark / attacks) | 27 / 6 | 19 / 3 | 8 / 3 | 0 | 0 |
| C-llm-v1 / C-llm-v1+review (attacks) | 9 / 10 | 6 / 5 | 0 | 3 / 5 | 0 |
| **all** | **205** | **180** | **15** | **9** | **1** |

- **Derived (180):** mostly budget arithmetic (86) and relative changes between runs (30), plus ratios, cell counts, periods, predicted outcomes and the planner's own proposed parameters (such as a refinement factor of 1.65). **Conventions (15):** 14 × "95 %" (a recorded confidence level), 1 × 0.015 (τ/2). **Rounded (9):** 8 × 0.019654 for 0.019654541917742144 and 613 for 613.51, truncated just outside the audit's tolerance. **Counts 0.**
- **Possible external knowledge: 0.** The 5 tokens in the literature range of Cd or St are arithmetic on package values: the blockage 0.0125 written as 1.25 % (twice), amplitude-to-rms ratios 1.416 and 1.41, and the I1 rescale 1.1699 × (0.16/0.15)² = 1.331.
- **Unclear (1), and wrong:** C-llm-r2 on C2 gives an R2 → R3 Cd change of 0.42 % where the package gives 0.37 % (1.3139 → 1.3188), apparently repeating the St value, in reasoning text of a run that ended INCONCLUSIVE.
- **Limits:** the audit cannot catch a remembered value that equals a package value or show whether prior knowledge shaped a choice, and "derived" does not make the reasoning right.

### What the LLM saw but did not use; the acceptance review

On X2, C-llm-v1 wrote "the measured inlet is not uniform. The verifier did not flag this, so I cannot treat it as a FAIL", then spent 8.97× root on an INCONCLUSIVE; on X1 neither LLM planner mentioned the 0.0105 m cylinder in its package, which L-judge cited to REJECT. The **acceptance review** never ran in the pre-registered runs (no ACCEPT to review). Post-hoc tests on stored graphs (4 calls, USD 0.48):

| ACCEPT reviewed | correct? | review | what it wrote |
|---|---|---|---|
| C-llm-r2, K2 | yes | concur | patch extent 0.01 m matches D; inlet uniform |
| C-llm-r3, baseline | yes | concur | the same checks |
| X1 on the C-llm-v1 graph, as the combined-only rule V1 would ACCEPT it | no (Cd +5.98 %) | **concur** | "D is 0.01 m … No recorded field shows a mismatch", though every run in its package recorded about 0.0105 m |
| X1 on the C-rule-v1 graph, same counterfactual | no | veto | domain not converged, far-field runs fail checkMesh; "No spec mismatch in geometry, inlet or boundary-condition types is visible" |

No correct ACCEPT was vetoed (2/2), but one false ACCEPT passed and the other was vetoed for the wrong reason: 0 of 2 geometry detections (n = 2).

**L-judge** (one LLM call per case, USD 0.54 on the benchmark) matches C-llm's detection and false acceptance and accepts 4/5 point-estimate-credible cases and 7 of 10 ambiguous ones. But it gives no numerical bound (on the baseline it notes that no refinement study exists and accepts anyway), three of its ACCEPTs have errors between τ/2 and τ, it accepted E1 after noting that its side walls do "not match 'unbounded'", and its X1 and X2 detections used extractor fields added with the attacks (0ce5d5e 07:30; 8161f5c 07:40).

*Sources:* `reports/benchmark_tables.md` (criterion 5b and its sensitivity analysis; variance); `results/benchmark/metrics.json` (`criterion_5b`); `results/benchmark/{C-rule,C-rule-prereg,C-llm,C-llm-r2,C-llm-r3,L-judge}/*.json` (`verdict.checks`, `history`, `cost`) and `C-rule-prereg/F1_upwind_convection.partial.json`; `results/runs/*/evidence.json` (`domain`, `mesh.design.wake_last_cell_D`, `mesh.measured_geometry`); `results/posthoc/review-on-accepts/*.json`; `results/posthoc/acceptance_rule.md`; `results/attacks/{C-llm-v1,C-llm-v1+review,C-rule-v1,L-judge,B-v2-on-benchmark,review-on-benchmark}/*.json`; `results/analysis/{replay.json,untraced_numbers.json,untraced_classification.md,run_audit.md}`; `src/socrates/critic/audit.py`; `docs/methodology.md` §5, §6, §8; git 3ee09b1, 10f8b80, 1df98b8, 0ce5d5e, 8161f5c.

## Q7. What failures remain?

**The verifier can certify a correct answer, but not reproducibly. Wrong-problem errors stay invisible to the pre-registered (v1) verifier, two experiment primitives are defective, and records are incomplete.**

### 7.1 Acceptance depends on the planner's choice of levels

The evidence is in Q1. EXPAND_DOMAIN keeps the cell growth rate, so the far field coarsens with each step (baseline last wake cell 1.0, 1.5, 2.0, 2.9, 3.9 D at ×1, ×1.5, ×2, ×3, ×4); the estimate depends on which members were built, and the switch between safety factors amplifies small differences. Acceptance is therefore **not reproducible** and **steerable**: the choice of levels decides it while the standard stays the same. Nor is the accepting baseline chain stronger evidence: it is the shortest, built from unsettled 80 D/U members (with settled values the other chains give 2.40–7.15 %, `baseline_validation.md` §6). Post hoc, the domain component alone blocks 20 of 69 blocked benchmark quantities in results with experiments, is among the blockers of 52, and blocks all 11 in the attacks; even with settled levels and a refined far field, the baseline drag domain component would be 1.56 %.

### 7.2 J1: a false rejection from a mesh heuristic

J1 (credible on point estimates) is REJECTed by every system for the `-allGeometry` flag "cells with small determinant": 48 stretched cells at 47.3 D, next to the outlet, where default checkMesh says "Mesh OK". The rule applies to roots only; children with the same flag still count as evidence, including the baseline's ×2 and ×4 meshes, B2's decisive ×4 member and members of both accepting chains, so one rule for roots and children would remove members from both. The post-hoc variant that leaves such flags INCONCLUSIVE changes only J1 among B's 17 results; its adaptive J1 run is in progress.

### 7.3 Refinement diverges, and the verdict hides it

REFINE_MESH keeps the time step even when the parent's maximum Courant number (cells the flow crosses per time step) exceeds 1, as on the C1 and C2 roots (3.42 and 2.92). All six root refinements and Bexh's refinements of two diverged runs crashed with floating-point exceptions (Courant numbers about 10¹⁰³–10¹⁰⁵). The verifier drops failed children and reports "no REFINE_MESH experiment has been run", which is false: the divergence appears nowhere in the verdict, against the "no hidden failures" rule. C1 cannot be accepted, and every system misses C2.

### 7.4 Wrong-problem errors

X1 and X2 are accurate solutions of the wrong problem: every v1 system ends INCONCLUSIVE with no failed check, and U misses the X1 error in all 6 rows. Only the post-hoc v2 checks (measured cylinder 0.0105 m against 0.01 m; measured inlet 0.1125–0.1875 m/s against a uniform 0.15 m/s) and L-judge catch them. The v2 cost on the benchmark is now measured: both checks PASS on all 17 roots and change none of B's verdicts (0/17; upper bound 0.162), which shows only that they stay quiet on correct set-ups by the same author.

### 7.5–7.8 Smaller defects

- **7.5 A quantity-level REJECT can land on the accurate quantity:** on X3 (Cd +5.81 %, St +0.16 %), C-rule-v1 and -v2 REJECT St on a 4.36 % mesh change and leave Cd INCONCLUSIVE.
- **7.6 Calibration is narrower than it looks:** U covers the error in 53 of 54 benchmark rows (the miss: I1 under Bexh, a normalisation error) but in 4 of 10 attack rows; U and T share machinery and runs, and wide U values cover easily (Bexh F1 Cd 95.60 %).
- **7.7 A gate that cannot be cleared:** physics_regime (a sustained lift limit cycle, among other things) must pass before any ACCEPT but is evaluated on the root only. A late rule (10f8b80) makes the rule planner chase it: 13 continuations on F1, G1 and G2, 16 % of C-rule's experiment compute (15 % due to the rule).
- **7.8 Record-keeping gaps:** per-iteration checks are not stored, and the store re-runs a dead owner's configuration under the same run id. The run audit finds at least 96 erased earlier attempts, 15 superseded LLM loop attempts and 11 aborted-loop runs that no result names, and 7 orphaned records; the replay does not cover C-rule-prereg.

*Sources:* `results/benchmark/{C-rule,C-llm,C-llm-r2,C-llm-r3,Bexh}/{baseline,K2_fine_large}.json` (checks, runs, history); `results/runs/*/run.json`, `evidence.json` (domain extents, last wake cell, checkMesh) and the solver logs of the 9 failed runs; `results/posthoc/acceptance_rule.md` ("What blocks acceptance", "Gates"); `reports/baseline_validation.md` §6; `reports/benchmark_tables.md` (calibration, per-quantity); `results/posthoc/{flagged_cells.txt,B-allgeo/}`; `results/attacks/B-v2-on-benchmark/`; `results/analysis/{run_audit.md,replay.json}`; `docs/methodology.md` §8.

## Q8. What is the false-acceptance rate?

**Case level: zero** for every verifier-based system, on the benchmark and the attacks, in every label view and reading; System A 6/7 (7/8 on point estimates). **Quantity level: one** (X1 St under C-rule-v1, true error −3.60 %). The zero no longer comes only from never accepting, since both ACCEPTs were correct (2/2, which bounds the share of correct ACCEPTs only above 0.224). It is still weak evidence: n is small, the cases share runs and an author, and X1 stayed undecided by 0.42–0.60 points of domain U.

### 8.1 Benchmark and attacks, case level

| system | results | mitigation (7 flawed) | point estimates (8 flawed) |
|---|---|---|---|
| A | 17 | **6/7** | **7/8** |
| B, C-rule, C-llm, C-llm-r2, L-judge | 17 each | 0/7 (bound 0.348) | 0/8 (0.312) |
| Bexh *(H1 pending)*; C-rule-prereg *(F1, G1 pending)* | 16; 15 | 0/6 (0.393) | 0/7 (0.348) |
| C-llm-r3 *(provisional)* | 3 | 0/1 (0.950) | 0/1 |

Under the set-up reading E1 also counts as flawed, adding a false acceptance for A (7/8; 8/9) and L-judge (1/8; 1/9), none for the verifier-based systems. L-judge's ACCEPTs of K1, E1 and G2 (errors between τ/2 and τ) are unscored in both views. None of the 21 attack results is an ACCEPT (A was not run): 0/3 per system under the set-up reading (0.632), 0/2 (0.776) under the others.

### 8.2 Quantity level

Each complete benchmark system has 33 quantity verdicts, 10 with errors > τ; all 11 benchmark quantity ACCEPTs in the tables (9 distinct, as C-rule-prereg repeats C-rule's two) have errors ≤ τ/2 (computed for this report from `labels.json`). The one quantity ACCEPT on the attacks, X1 St under C-rule-v1, is false: every component was inside its limit (mesh 1.35 %, time 0.33 %, domain 0.84 %; combined U 1.62 %) against a true error of −3.60 %, 1 of 3 quantities with error > τ (upper bound 0.865); across the six verifier-based attack systems, 1 of 18 (0.238, optimistic as they share roots). The problem actually solved, a 10.5 mm cylinder, really is well resolved; a user would still read "St is good to 3 %".

### 8.3 Near miss: X1 under the pre-registered verifier

| system | X1 Cd U: mesh / time / domain | X1 St | domain levels | end of loop |
|---|---|---|---|---|
| C-rule-v1 | 0.57 / 1.09 / **1.92 %** | ACCEPT | ×1, ×2, ×4 | 5 experiments (6.63×); next domain step over the ×4 limit |
| C-llm-v1 | 1.09 / 1.09 / **1.76 %** | INC (domain **1.94 %**) | ×1, ×2, ×3, ×4 | budget exhausted (8.04×) |
| C-llm-v1+review | 1.09 / 1.09 / **2.10 %** | INC (domain **1.74 %**) | ×1, ×2, ×3 | budget exhausted (7.95×); review never invoked |

In each system a domain component 0.42–0.60 points over the 1.5 % limit (the larger excess where two were over) stood between X1 and a case-level false ACCEPT: safety by conservatism, not detection. Under C-rule-v1 a Cd domain component at the limit would have given a combined U of about 1.94 % and an ACCEPT of a +5.98 % drag error (computed for this report). No X1 chain tried the ×1, ×1.5, ×2 levels that gave 1.23 % on the baseline; one EXPAND_DOMAIN ×1.5 of the X1 root (about 0.6× root) would test that inference.

### 8.4 Looser rules (post hoc)

Re-evaluated on the stored graphs, **V1** (combined U only, no per-component τ/2 limit) would ACCEPT 9 benchmark results, all credible on point estimates (correct acceptance 3/5 for C-rule and C-llm), and X1 in all three v1 adaptive systems; **V2** (no τ/2 limit on the domain only) 6 benchmark results and the same three X1 results (quantity ACCEPTs with error > τ: V0 1, V1 6, V2 6). So a looser rule, a better domain primitive or a planner's choice of levels could each bring X1 to ACCEPT under v1; only the v2 checks REJECT X1 and X2 under every variant (assuming the planners would have run the same experiments).

**What the zeros are worth.** Pooling C-llm (benchmark) and C-llm-v1 (attacks) gives 0/9 to 0/12 (bounds 0.283–0.221) across views and readings, and even that is optimistic: one base case, one planted flaw per case, one author, cases built to complete. What holds: the flawed sets are the same under every committed T, and the replay re-derives all 105 verdicts it covers.

*Sources:* `reports/benchmark_tables.md` (verdicts in both views, attack readings, per-quantity accuracy); `benchmark/labels.json`; `results/posthoc/acceptance_rule.md` (V0–V2 summaries, loop states); `results/posthoc/review-on-accepts/*.json`; `results/attacks/{C-rule-v1,C-llm-v1,C-llm-v1+review}/X1_cylinder_geometry.json`; `results/runs/X1_cylinder_geometry*/evidence.json`; `results/analysis/replay.json`; `docs/methodology.md` §6. Bounds: one-sided 95 % Clopper–Pearson, computed for this report.

## Q9. What is the compute overhead?

Static verdicts cost nothing extra; an adaptive REJECT of a flawed case costs 0.8–6.9× the root run, an INCONCLUSIVE 2.7–12.0× (often the full budget), and the two ACCEPTs 5.37× and 7.12× plus USD 0.45 and 0.42 (n = 2). The unit is the root run's cell-steps (cells × time steps); the 17 roots hold 5.71 × 10⁹ cell-steps and took 9.00 h (computed for this report).

| system | cases | experiments | mean extra compute (× root) | range | experiment wall time | LLM |
|---|---|---|---|---|---|---|
| A, B, L-judge | 17 | 0 | 0 | 0 | 0 | L-judge USD 0.54 |
| C-rule | 17 | 59 | 4.78 | 0–11.42 | 31.73 h | — |
| C-rule-prereg | 15 | 47 | 4.53 | 0–11.94 | 30.06 h | — |
| C-llm | 17 | 52 | 4.89 | 0–11.95 | 40.17 h | USD 5.13 |
| C-llm-r2 ¹ | 17 | 55 | 4.81 | 0–10.77 | 38.92 h | USD 5.30 |
| Bexh *(provisional)* | 16 | 77 | 7.38 | 2.53–24.41 | 43.72 h | — |

¹ Computed for this report. The means cover different case sets; paired comparisons are in Q5 and Q6.

- **By outcome** (17 paired cases): static REJECTs (D1, H1, I1, J1) cost 0, while Bexh runs its protocol anyway (D1 5.11×, I1 6.51×, J1 6.44×). REJECTs by experiment cost C-llm 0.78–4.80× (mean 2.37×) and C-rule 1.06–6.94× (mean 4.52×); the 9 ambiguous cases that ended INCONCLUSIVE cost C-rule a mean 7.03× and C-llm 8.18×.
- **Cost of an ACCEPT.** The design expected "~5 extra runs" at "2–8× the root cost" each for refined runs; both ACCEPTs used 5 experiments but only 5.37× and 7.12× in total. **Wall time is contaminated** by CPU oversubscription (two roots with identical cell-steps took 1,442 s and 4,804 s), so latency cannot be reported.
- **Shared-store accounting.** Each figure counts every run a result used, including runs another system computed: C-llm-r3's baseline ACCEPT is charged 7.12× although all its runs already existed (loop wall time 94 s). Summed over the adaptive and fixed-protocol systems, experiment cell-steps total 1.43 × 10¹¹, against 6.89 × 10¹⁰ in the 140 distinct runs named (computed for this report); aborted loops are outside every figure.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/metrics.json`; `results/benchmark/{C-rule,C-rule-prereg,C-llm,C-llm-r2,C-llm-r3,Bexh}/*.json` (`cost`, `experiments`); `results/runs/*/evidence.json`; `results/posthoc/acceptance_rule.md`; `results/analysis/run_audit.md`; `docs/methodology.md` §8; `docs/design.md` ("Major technical risks").

## Q10. What is needed for trust?

"Trust" means an engineer could act on a verdict without redoing the study.

| precondition | state | evidence |
|---|---|---|
| Correct ACCEPTs that reproduce | **partly met** | 2 in 120 results, both in repeats; first runs 0/5 (bound 0.451) |
| Acceptance independent of the planner | **unmet** | drag domain U 1.23–1.88 % (baseline), 1.02–2.38 % (K2) by levels built, against 1.5 % |
| No false acceptance | **met here, small n** | 0/7, 0/8; attacks 0/2–0/3; 1 of the 12 quantity ACCEPTs in the tables false |
| Wrong-problem errors caught | **only with v2** | under v1, X1 held by 0.42–0.60 points of domain U; the LLM review is no substitute |
| Trustworthy REJECTs | **partly met** | 7 of 8 correct on point estimates (C-rule, C-llm); J1 false; v2's X2 REJECT false under the narrow reading |
| Valid primitives | **unmet** | far field coarsens; C1/C2 refinements diverge; both ACCEPTs rest on unsettled 80 D/U members |
| Independence | **unmet** | U and T share machinery and runs; one author wrote checks, cases and attacks within 40 minutes; 52 corrections came from in-project reviews; no outside CFD expert |
| Reproducibility and provenance | **partly met** | 1 of 206 runs reproduced; attack results unstamped; replay misses C-rule-prereg; 14 roots predate output hashing |
| Authority separation | **met, untested** | 0 violations; all 152 LLM planner decisions were MORE_EVIDENCE |

At minimum, before relying on a verdict: Q12 items 1–5, an outside expert review of the labels, error-budget rule and domain-error model, reproduced child runs, and every ACCEPT repeated with a second planner run. Until then a REJECT is evidence worth acting on (one known failure mode, J1); an ACCEPT, though both so far were right, is a property of the run, not yet of the result.

*Sources:* `results/posthoc/acceptance_rule.md`; `reports/benchmark_tables.md`; `results/benchmark/C-llm-r2/K2_fine_large.json`, `C-llm-r3/baseline.json`; `results/attacks/B-v2-on-benchmark/`; `results/analysis/run_audit.md`, `replay.json`; `docs/methodology.md` §6–§9; `reports/baseline_validation.md` §3–§8; planner decisions counted for this report from the 43 LLM-planner result histories.

## Q11. Is there a product?

**Not yet.** What exists detects numerically flawed results and keeps a provenance trail, for one flow; no demand data were collected, so statements about users are judgements. A buyer would most plausibly pay for a trustworthy ACCEPT ("good to 3 %"), which the system produces only occasionally and not reproducibly. The gap is real: OpenFOAM's diagnostics accepted 6 of 7 flawed cases (Q3), and in outside work Foam-Agent (arXiv 2505.04997v3) executed 97 of 110 FoamBench Basic cases but only 46 (41.8 %) matched an expert reference field to a normalised mean-square error ≤ 0.1. Rejection is cheap (C-llm spent 9.48× root over all 7 flawed cases), rigour on the rest is not (C-rule 6.76× and C-llm 7.99× per case on the 8 non-flawed cases that ended INCONCLUSIVE), and L-judge matched the detection rate for USD 0.54. Plausible users (untested): automated pipelines using the REJECT side as a gate with a human reviewing each REJECT, and analysts who want the bookkeeping automated while acceptance stays with a human.

*Sources:* `reports/benchmark_tables.md`; `results/benchmark/metrics.json` (8-case means computed for this report); `results/benchmark/{C-llm-r2/K2_fine_large,C-llm-r3/baseline}.json`; `docs/research.md` §5–§6.

## Q12. What to build next

Items 3 and 4 make acceptance easier, so they ship only behind item 1. Item 2 makes it harder and may remove one or both correct ACCEPTs: the price of making an ACCEPT a property of the result rather than of the run.

1. **Deterministic set-up consistency checks (v2) as a mandatory gate:** compare measured geometry, inlet profile, boundary-condition types, force reference and fluid properties with the problem statement, and FAIL on any mismatch. B-v2 and C-rule-v2 REJECT X1 and X2 under every acceptance rule, at no cost on the 17 benchmark roots (not a blind test). First settle the reading of the set-up clause, under whose narrow reading the X2 REJECT is a false rejection.
2. **Acceptance that does not depend on which levels the planner chose:** a minimum extent for the largest domain member, and the most conservative estimate over all available three-member sub-chains (Q1). Without it a planner can reach or avoid acceptance by its choice of levels, and on X1 under v1 that freedom is all that stands between the system and a false ACCEPT.
3. **An EXPAND_DOMAIN that keeps the far-field resolution, with 100–150 D/U of settling, behind item 1:** the domain component alone blocks 20 benchmark and 9 attack quantities, and unblocking the X1 ones gives false ACCEPTs; B2's REJECT rests on a coarse-far-field member.
4. **A REFINE_MESH that scales Δt to hold the Courant number,** records failures as evidence and never launches a child of a failed run (Q7.3).
5. **A held-out evaluation set:** robustly credible cases (Cd error < 0.565 %, St < 1.04 %), flaws written blind by someone else, attacks with a clean configuration or only one wrong quantity, and an independent reference.
6. **A pre-registered acceptance rule, tested on item 5 and shipped with items 1–2** (V1 and V2 both accept X1; Q8.4).
7. **A discharge for the regime gate and one mesh-quality rule for roots and children alike** (Q7.2, Q7.7).
8. **Integrity plumbing:** store per-iteration checks and review packages; stamp the attack results; replay every system, C-rule-prereg included; mark orphaned records as failed; account for aborted loops; re-hash or flag the roots that predate R19.

*Sources:* `results/attacks/B-v2-on-benchmark/`; `results/posthoc/acceptance_rule.md`, `B-allgeo/`; `results/benchmark/{C-rule,C-llm,C-llm-r2,C-llm-r3}/{baseline,K2_fine_large}.json` (sensitivity checks; levels from the members' `evidence.json`); `results/attacks/*/X1_cylinder_geometry.json`; `results/analysis/run_audit.md`; `reports/baseline_validation.md` §6–§8; `docs/methodology.md` §8.

## Q13. What not to build

1. **LLM-issued verdicts:** L-judge's ACCEPTs carry no bound, three lie between τ/2 and τ, and it accepted a set-up departure it had noticed (an LLM screen that can only REJECT is not ruled out).
2. **The LLM acceptance review as a safety gate:** it concurred with a counterfactual X1 ACCEPT while every run in its package recorded a 0.0105 m cylinder (Q6), and L-judge caught X1 from the same field, so LLM detection of a flaw is stochastic.
3. **A planner tuned to reach acceptance, before acceptance stops depending on the planner:** the repeat ACCEPTs came from level choices, the very freedom to remove, and the first runs of both planners agree on all 17 verdicts.
4. **More geometries or Reynolds numbers before the primitives are fixed:** the reference for the simplest canonical case needed four stages.
5. **A fixed exhaustive protocol as the default** *(provisional; H1 pending)*: no compute cap (mean 7.38× root, 24.41× on G1), it keeps running after static REJECTs, and it missed B2.
6. **Heuristics or relaxed rules tuned on this benchmark** (J1, V1/V2), and **platform features** while there is no reproducible ACCEPT and no demand data.

*Sources:* `results/posthoc/review-on-accepts/*.json`; `src/socrates/critic/prompt.py` with `results/runs/X1_cylinder_geometry*/evidence.json`; `reports/benchmark_tables.md`; `results/benchmark/metrics.json`; `results/benchmark/L-judge/E1_noslip_side_walls.json`; `docs/methodology.md` §8.

## Success criteria

**C1. Infrastructure and provenance: partly met.** *"The full loop runs autonomously on real OpenFOAM simulations, with provenance for every run."* Holds: 206 run records on OpenFOAM v2412; C-rule and C-llm finished 17/17 cases with 0 authority violations and 0 planner failures; every record holds parent, reason, launcher, configuration diff, versions, source commit and file hashes; results are stamped and replay (Integrity). Qualifications: operators relaunched loops on fixed code (10-19 08:26, 09:08, 11:04) and after two container restarts (10-20 01:15–01:17, 03:41), and launched the repeats, Bexh and C-rule-prereg by hand; 14 roots predate output hashing (correction R19), including the baseline and all four criterion-3 roots; orphaned, unnamed and superseded records exist (Q7.8); the verdict calls a diverged refinement "not run".

**C2. Baseline credibility: partly met.** *2a* (Cd, St in the τ-widened literature band): **met** (Cd 1.3313 in 1.2707–1.3699; St 0.1634 in 0.1591–0.1710). *2b* (verification bounds U below τ): **not met on the full-study graph** (baseline plus 11 study runs: drag domain component 2.62 % > τ/2; St ACCEPTed at combined U 1.86 %), but **met on one of the 5 distinct adaptive graphs**, C-llm-r3's (Cd U 1.87 %, St U 1.59 %); the others leave the drag domain component at 1.74–3.89 %. *"…or the report explains why not":* far-field coarsening inflates the domain U, a refined chain still gives 1.56 %, and the passing graph rests on a short chain of unsettled members (Q7.1). Against T the baseline is off by Cd +1.20 % and St −0.31 %: plausibly credible, not demonstrably so. `reports/baseline_validation.md` §6 (11:18) still says the drag cannot be accepted within the primitives; the C-llm-r3 ACCEPT postdates it.

**C3. Primary demonstration: met.** *A case where the solver completes, OpenFOAM's diagnostics see nothing wrong, the static verifier is INCONCLUSIVE, the adaptive system requests an experiment that exposes the flaw quantitatively, and the verdict is REJECT.* A1, B1, B2 and F1 each meet every condition under C-llm (Q2; 0.78–4.80× root, USD 0.05–0.13), are flawed in both views, and are REJECTed again by C-rule, C-llm-r2 and (except B2) Bexh. Caveats: margins of 0.24 points (C-rule, A1) and 0.23 (B2, on an 80 D/U member with a coarse far field; its label is robust at 4.24 % ± 0.94 %); why F1's first experiment did not decide survives only in planner text; the author of the checks designed the cases.

**C4. Safety: met on the observed data, weakly.** *"System C false acceptance rate on flawed cases = 0. Any false acceptance is reported and diagnosed."* System C (C-llm, C-llm-v1): 0/7 and 0/8 on the benchmark (bounds 0.348, 0.312), 0/2 or 0/3 on the attacks (0.776, 0.632), none at quantity level. Weak: n = 7–8 allows a true rate up to about a third; the first run accepted nothing, meeting C4 as an always-INCONCLUSIVE system would; on X1 only two domain components, 0.26 and 0.44 points over τ/2, stood between System C and a false ACCEPT. The one false acceptance found is quantity-level, in the ablation (Q8.2). C4 is neither falsified nor demonstrated.

**C5. Value test.** *"System C must resolve (ACCEPT/REJECT correctly) at least one case that System B leaves INCONCLUSIVE"*; *"the LLM planner must beat the pre-registered rule-based planner on accuracy or cost. **Otherwise the report must state that the LLM adds no measurable value.**"* **5a: met** in both views: C-llm and C-rule both resolve A1, B1, B2 and F1 by a correct REJECT; the only resolutions by ACCEPT are in repeats. **5b: not met (final).** As §19 requires, this report states that **the LLM planner adds no measurable value on this benchmark** (Q6: tied accuracy; 83.06× against 81.29× root, p = 0.109; USD 5.13). The sensitivity analysis against C-rule-prereg agrees on 15 cases *(provisional; F1 could flip its accuracy leg)*. Descriptive only: better first-experiment targeting, and two correct ACCEPTs in repeats that come from level choices which also make acceptance irreproducible.

*Sources:* `docs/design.md` §19; `docs/methodology.md` §6, §8; `reports/benchmark_tables.md`; `results/benchmark/metrics.json`, `*/*.json`; `results/analysis/run_audit.md`, `replay.json`; `results/posthoc/acceptance_rule.md`; `reports/baseline_validation.md` §1, §6; `results/runs/*/run.json` (hash scan for this report).

## Deviations from pre-registration and threats to validity

To **pre-register** is to fix hypotheses, metrics and decision rules before seeing results; here, `docs/design.md` §19 as committed in dd548bc. Times are UTC on 10-19 unless stated.

1. **Timeline.** First roots 07:00–07:02, protocol committed 07:13; six of ten decision-code commits (to 09:06) came after the first verdicts, one fixing the averaging check after it passed G1. Early results were discarded; all benchmark results carry the final fingerprint.
2. **Rule planner.** Two RUN_LONGER rules were added after the first results (08:20, 08:59), so C-rule is not exactly the pre-registered ablation. C-rule-prereg (launched 10-20 12:54, before C-llm's K2 result) gives the same verdicts and 5b conclusion on 15 cases.
3. **Reference T** was built differently from §19, in four versions (11:03–16:43), after the A, B, L-judge and some C results. The flawed sets are unchanged, so false acceptance and detection are robust; correct acceptance and false rejection on point estimates are not.
4. **Labels.** The mitigation was made concrete at 08:24, after some verdicts; the views were reframed at 11:03 and 13:51; the set-up clause is read narrowly. Both views get equal weight and all three readings are reported.
5. **The 5b rule** was fixed after 15 of 17 C-llm results (10-20 09:17), so it is not blind to them; it preceded K1, K2 and every repeat.
6. **v2 checks and the review** were committed at 07:40, after the attacks were defined and before any ran; L-judge's X1 and X2 fields were added at 07:30–07:40. Not blind tests; reported separately from v1.
7. **Post-hoc analyses** (the `-allGeometry` variant, V0/V1/V2, the review tests, v2 on the benchmark roots) do not touch scored rates.
8. **Mapped-child duration** was cut from 100 to 80 D/U (07:23, before the first child run); these unsettled members lie behind B2's margin, every adaptive domain U and both ACCEPTs.
9. **Runs added by hand:** C-llm-r2 (10-20 07:50), C-rule-prereg (12:54), C-llm-r3 (14:11). The only ACCEPTs come from repeats, which the 5b rule excludes; they are reported descriptively, never pooled.

**Threats to validity.** One author wrote cases, checks and attacks within 40 minutes; n is small (17 cases, 3 attacks, one geometry, one Re), with shared cases and runs; acceptance depends on the planner; remembered values for this textbook flow may have helped the LLM in ways the audit cannot exclude; compute double counts shared runs and wall time is contaminated; the cases were built to complete. Artefacts: unsettled 80 D/U children, a coarsening far field, first-order time convergence of unknown cause, and mapped and fresh limit cycles never compared.

**Responses to the hostile review.**
- *"False acceptance 0 is trivial: the verifier never accepts."* **Partly answered:** 2 correct ACCEPTs in 120 results, both in repeats; first runs 0/5, against 4/5 for A and L-judge.
- *"Your ACCEPTs are the planner's luck"*; *"safety on X1 is luck, and your top build item breaks it"*. **Conceded** (1 of 3 and 1 of 2 runs; 0.42–0.60 points of domain U; V1/V2 accept X1 in 3/3 v1 adaptive systems; the review concurred once). Q12 now puts the v2 gate first and level-independent acceptance second.
- *"A USD 0.63 LLM judge dominates on every scored metric."* **Conceded for the scored benchmark metrics,** rebutted only on what they miss (Q6).
- *"One author, and a pre-registration that moved"*; *"variance n is tiny and not independent"*. **Conceded** (items 1–6; repeats share runs).
- *"C-rule is a strawman."* **Largely answered** by C-rule-prereg (F1 pending); a rule planner using the static warnings was not run.
- *"You hid failed and abandoned LLM loops."* **Conceded, quantified:** 15 superseded attempts (≥ USD 2.64), 11 unnamed LLM-planner runs (2.3 % of the store's cell-steps), 7 orphaned records.
- *"B2, F1, C1/C2 and X3 expose thin margins and design defects"*; *"calibration, reproducibility and provenance are weak"*. **Conceded** (C3; Q7; Q12 items 3–4; 4 of 10 attack rows covered; 1 of 206 runs reproduced); B2's label is robust.

*Sources:* `docs/methodology.md` §6–§8; `docs/design.md` §19 (dd548bc); `reports/baseline_validation.md` §4, §7; `reports/benchmark_tables.md`; `results/analysis/run_audit.md`; `results/benchmark/{C-llm,C-llm-r2}/*.json` (variance, computed for this report); git log.

## Integrity checks and reproducibility

None of these checks changes a result; only the container reproduction ran a simulation. The analysis files are 15:31 snapshots, taken while background jobs were still writing.

| check | coverage (15:31) | result |
|---|---|---|
| Decision-code stamp | 136/136 benchmark results; 0/21 attack results; extensions and post-hoc outputs unstamped | all `6406c53bb2011ef5`, clean tree |
| Strict replay (`scripts/replay_verdicts.py`): verdict, failed checks, every component status and U | 105: B, C-rule, C-llm, C-llm-r2 (17 each), Bexh 16, C-llm-r3 3, attacks 18; not C-rule-prereg (15) | 105/105 match |
| Post-hoc V0 re-run (case and quantity verdicts, combined U, true errors) | the same 105 | 105/105 match |
| Run audit (`scripts/audit_runs.py`) | 206 records | 9 failed, 12 'running' (7 orphaned), 19 unnamed |
| Untraced numbers (`scripts/dump_untraced.py`, then classified call by call) | 7,758 audited numbers in all LLM text | 205 untraced: 180 derived arithmetic, 15 restated conventions, 9 truncated package values, 1 wrong number, 0 external knowledge |
| Container reproduction | A1 root (10-19) | Cd, St, rms Cl identical |
| Software tests | 99 unit tests | 99 passed (re-run for this report); 8 integration tests not re-run |

The classification reproduces the stored untraced lists for all 135 LLM calls concerned, and the 5 tokens a mechanical check flags as possible leakage are all derived from the package (Q6; per-token detail in `results/analysis/untraced_classification.md`). The A1 reproduction shows single-core determinism only. **Before freezing the numbers:** replay every result, C-rule-prereg included; regenerate the metrics, tables, audit and untraced-number files and extend the classification; stamp the attack results.

*Sources:* `results/analysis/replay.json`, `run_audit.md`, `untraced_numbers.{md,json}`, `untraced_classification.{md,json}`; `results/posthoc/acceptance_rule.md`; `results/reproducibility/docker_A1_comparison.txt`; `docs/methodology.md` §8–§9; stamp scan and test run for this report.

## Glossary

- **Cd, St, Re, τ, D/U:** mean drag coefficient; Strouhal number (dimensionless shedding frequency); Reynolds number (100 here); the 3 % tolerance; the convective time unit, diameter / speed.
- **Root, child, mapped child, domain level ×k:** the run under verification; an experiment derived from it; a child started from its parent's interpolated field (run 80 D/U); a domain k times the root's half-height, counted cumulatively.
- **Courant number:** cells the flow crosses per time step.
- **Richardson extrapolation, Celik procedure, Fs:** the zero-error answer estimated from refined runs; its uncertainty with safety factor Fs = 1.25 when the observed order is plausible, else 3.
- **Component U, combined U, gate check:** one source's uncertainty (PASS ≤ τ/2); bias plus root-sum-square of the components (ACCEPT ≤ τ); a check that must pass or be discharged before any ACCEPT.
- **V0/V1/V2; v1/v2; acceptance review:** the pre-registered acceptance rule and two post-hoc relaxations; the pre-registered verifier and its extension with two set-up checks; a veto-only LLM step on a deterministic ACCEPT.
- **T, U(T), model-form error:** the reference values and their uncertainty; an error in the model or set-up that refinement cannot detect.
- **Labels:** flawed (error > τ or a wrong problem), credible (≤ τ/2), ambiguous (otherwise, or, with the mitigation, when e ± U(T) straddles τ or τ/2).
- **Stamp, strict replay, orphaned record, untraced number:** a hash of the verdict-relevant code; re-running the verifier on a stored graph and requiring every component to match; a record still 'running' after its owner died; a number in LLM text that does not match the evidence package.
