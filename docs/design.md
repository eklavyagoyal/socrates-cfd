# Technical design

Status: as-built design. Decisions measured during development are marked
**[measured]**. Items a CFD researcher should review are marked **EXPERT REVIEW**.
Section numbers follow the 20 items requested in the brief. Sources are in
`docs/research.md`.

---

## 1. Selected Reynolds-number regime

- **Choice:** unbounded 2D circular cylinder at **Re = U D/ν = 100**: periodic laminar vortex shedding.
- **Why:**
  - It is about 2× the shedding onset (Re_c ≈ 47) and about 0.53× the 3D mode-A onset (188.5), so strictly 2D periodic flow is the physical state.
  - Reference data are dense and independent (research §2).
  - Every requested failure mode occurs naturally.
- **Engineering framing (`configs/problem_cylinder_re100.yaml`):** a 10 mm rod in 0.15 m/s air (ν = 1.5×10⁻⁵ m²/s). Estimate mean Cd and St, each to ±3 %, unbounded stream.

## 2. Governing equations

Incompressible Navier–Stokes with constant ν (research §1.3), solved for the
velocity and kinematic pressure.

- **Cd** = F_x/(½ρU²A_ref), with A_ref = D × span.
- **St** = f D/U, with f the lift (Cl) oscillation frequency.

## 3. Physical assumptions

- **2D.** Valid for Re < 188.5.
- **Laminar.** No turbulence model.
- **Incompressible.** Ma ≈ 4×10⁻⁴.
- **Newtonian, isothermal, constant properties.**
- **Unbounded uniform stream.** Represented by a finite domain, whose truncation error is a numerical error to be measured.
- **Smooth, rigid, fixed cylinder.**
- **Not modelled:** free-stream turbulence, end effects, vortex-induced vibration.

## 4. OpenFOAM solver and baseline case

- **Version:** OpenFOAM **v2412** (ESI), Ubuntu package `openfoam2412=2412.260127-1`.
  - Mature line with several patch releases.
  - Its `forceCoeffs` and `solverInfo` behaviour was verified against source (research §4).
- **Solver:** `pimpleFoam`, laminar, in PISO mode (nOuterCorrectors 1, nCorrectors 2). A transient solver is required because the quantity of interest is a time mean of a periodic flow.

| Item | Baseline value | Why |
|---|---|---|
| Geometry | D = 0.01 m; one cell thick, span 1 D | standard pseudo-2D |
| Domain | inlet 30 D, outlet 50 D, sides ±40 D | blockage 1.25 %. Qu et al.: ~+1 % Cd at 1–1.7 % blockage. Inlet > 20 D (Posdziech & Grundmann). Outlet ≫ 14.5 D (Tezduyar & Shih) |
| Mesh | structured: 2-layer O-grid + 8 H-blocks, 30 580 hexes (`src/socrates/case_generation/blockmesh.py`) | geometric similarity under refinement (needed for Richardson) |
| Wall resolution | 160 cells around; first cell 0.005 D | ≈ 20 cells inside the boundary layer (δ ~ D/√Re = 0.1 D) |
| Near wake | 0.125 D cells to ±2.5 D; streamwise growth 1.9 %/cell to the outlet | |
| Mesh quality [measured] | max non-orthogonality 43°, skewness 0.53, aspect ratio 12.6 | |
| Boundary conditions | inlet U fixed (0.15, 0) / p zeroGradient; outlet p = 0 / U inletOutlet; sides symmetryPlane (free slip); cylinder noSlip | `inletOutlet` prevents backflow instability when vortices exit; free slip is the standard far-field side condition (Behr et al. "slip walls") |
| Fluid | ν = 1.5×10⁻⁵ m²/s, ρ = 1.2 (ρ cancels in coefficients) | air at ~20 °C |
| Schemes | `backward` in time (2nd order); `Gauss linearUpwind grad(U)` for convection (2nd order); `Gauss linear` gradient; `corrected` Laplacian | JFE policy: ≥ 2nd order |
| Pressure/velocity solvers | GAMG p: tolerance 1e-7, relTol 0.01; final corrector relTol 0. U: smoothSolver, tolerance 1e-8 | |
| Non-orthogonal correctors | 0 [measured]: Cd identical to 5 digits and Cl_rms within 0.02 % compared with 1 corrector | |
| Time step | Δt = 0.01 D/U; max Co ≈ 0.75 [measured]; ≈ 600 steps per shedding period | PISO needs Co < 1 (OpenFOAM User Guide) |
| Start-up | asymmetric initial velocity patch (setFields) to trigger shedding immediately | identical for all fresh runs; removed by transient detection |
| Duration and averaging | 150 D/U; declared averaging window 75–150 D/U (≈ 12 cycles) | [measured] the cycle-mean Cd error halves every cycle: −0.97 % at t = 28, −0.06 % at 53, < 0.005 % by 78 D/U |
| Forces | `forceCoeffs` every step; magUInf = U; Aref = D × span | |
| Completion criteria | solver reaches endTime and prints `End`; final pressure solve at tolerance; checkMesh OK | **Not sufficient for credibility.** Credibility is established in `reports/baseline_validation.md` |

## 5. Canonical reference data

See research §2.3. Mean Cd 1.31–1.33 (wider 1.30–1.35); St 0.164–0.166; Cl′ 0.222–0.235.

**Blind mode (default):** reference values are hidden from the verifier and the
critic. They are used only for validation of the baseline and to label the benchmark.

## 6. Computational domain

See §4. Domain changes always **preserve the near-field mesh**: the first cell
and per-cell growth rate are held, and cells are only added or removed far away
(`expanded_domain_counts`). Domain studies are therefore not confounded with
resolution.

## 7. Boundary conditions

See §4. **EXPERT REVIEW:** free slip on the sides versus a free-stream Dirichlet
condition (Qu et al.) changes the blockage correction slightly. With 1.25 %
blockage the difference is expected to be below 1 %.

## 8. Meshing strategy and systematic refinement

Every block's cell count is multiplied by a factor `f` while each block's total
expansion ratio is held fixed. All cell sizes then scale by about 1/f.

- The representative size is h = (A/N)^½, using the in-plane area (Celik).
- **REFINE_MESH** uses r = √2 by default (cells × 2), which satisfies r > 1.3.
- The family is capped at f = 2 relative to the root (limits in `experiments/primitives.py`).

## 9. Numerical schemes

See §4.

- **Formal orders used in Richardson analysis:**
  - space: 2, or 1 if the convection scheme is `Gauss upwind`;
  - time: 2 for backward / Crank–Nicolson, 1 for Euler.
- **EXPERT REVIEW:** `linearUpwind` is second order on smooth flow but its effective order on this stretched mesh is unknown. The observed order from three-level studies is reported, not assumed.

## 10. Time-stepping strategy

- Fixed Δt; no adaptive time stepping in the baseline, which makes temporal-refinement studies clean.
- **REDUCE_TIME_STEP** halves Δt on the identical mesh.
- **REFINE_MESH** keeps Δt **unless** the predicted max Co (parent Co × r) would exceed 0.9 while the parent was below 1. In that case Δt is reduced to keep Co ≤ 0.9, and the change is recorded and reported with the mesh-sensitivity result. With the baseline Δt the temporal error is expected to be negligible; this is checked by REDUCE_TIME_STEP.

## 11. Quantities of interest

- **Requested:** time-mean drag coefficient and Strouhal number, each with tolerance τ = 3 % (relative).
- **Also extracted:** Cl_rms, lift amplitude, drag amplitude, cycle statistics.

**How quantities are computed:**
- **"Reported" value of a run:** what the case author's set-up would report. That is the time-weighted mean over the *declared* averaging window, and St from the FFT peak of Cl over the same window.
- **"Stationary" value:** the system's own robust estimate. MSER-truncated, an integer number of cycles, St from zero crossings, cross-checked by FFT.

Sensitivity studies compare stationary values, which separates discretisation error from averaging error.

## 12. Deterministic evidence available from OpenFOAM

From `src/socrates/evidence/extract.py`:
- **checkMesh:** counts, non-orthogonality, skewness, aspect ratio, failed checks, bounding box.
- **Solver log:** completion, fatal errors/warnings, per-step Courant number, continuity errors (last per step), final pressure-solve residual of each step, iteration-limit hits, steady convergence message.
- **Function objects:** `forceCoeffs` histories, `solverInfo`, and boundary flux sums (mass balance).
- **Derived:** cycles, transient end (MSER), integer-cycle statistics, two frequency estimates, statistical-uncertainty measures, steps per period, representative cell size, blockage, configured Re, force-reference consistency.

## 13. Deterministic checks (`src/socrates/checks/`)

All checks return PASS, FAIL or INCONCLUSIVE with value, threshold, source and reason.
**Missing evidence never yields PASS (unit-tested).**

| Check | PASS / FAIL rule | Threshold provenance |
|---|---|---|
| solver_completion | `End` printed, no FATAL | — |
| mesh_quality | checkMesh `Mesh OK` → PASS; `***` → FAIL; `*` warnings → INCONCLUSIVE | OpenFOAM defaults |
| mass_conservation | boundary-flux imbalance ≤ τ/20 | derived from τ (an imbalance ε perturbs Cd by ~2ε) |
| linear_solver_convergence | last pressure solve of ≥ 99 % of steps reaches the configured tolerance; steady: residualControl satisfied | configured tolerance |
| courant_number | PISO: max Co < 1 → PASS, > 1 → FAIL; PIMPLE with outer correctors → INCONCLUSIVE until a Δt study | OpenFOAM User Guide; Issa 1986 |
| reynolds_consistency | \|Re_case − Re_spec\|/Re_spec ≤ 1e-3 | consistency (rounding level) |
| force_reference_consistency | magUInf = inlet U; Aref = D × mesh span (span measured from the checkMesh bounding box) | consistency |
| physics_regime | 47 < Re < 188.5 requires sustained oscillation and a transient solver | Provansal 1987; Williamson 1996; Barkley & Henderson 1996. **Qualitative regime knowledge for this geometry (EXPERT REVIEW for generalisation)** |
| convection_scheme_order | first-order upwind → INCONCLUSIVE until mesh sensitivity PASSes | JFE policy |
| averaging_window (per quantity) | b = \|reported − stationary\|/stationary, only against a statistically reliable stationary estimate: > τ FAIL, otherwise PASS as a *measured bias* (no experiment can change the root's declared-window value) | error budget |
| statistical_uncertainty (per quantity) | max(CI95, drift, half-difference) ≤ τ/2 → PASS, else INCONCLUSIVE | error budget |
| mesh / time / domain sensitivity (per quantity) | sequence analysis (below) | Roache; Celik et al. |

### Sensitivity analysis (`checks/sensitivity.py`)

The quantity estimated is always the uncertainty of the **root** (submitted) run.

- **Two levels:** U = 3 · δ · r^p/(r^p − 1).
- **Three levels:** observed p (Celik iteration). Fs = 1.25 if 0.5 p_f ≤ p ≤ 2 p_f; otherwise Fs = 3 with the formal order. Oscillatory or noise-level sequences use U = 3 × range.
- **Monotone divergence** (|ε21| ≥ |ε32|, Eça & Hoekstra 2014) is never extrapolated: FAIL if the change exceeds τ, else INCONCLUSIVE.
- **Decision:**
  - **FAIL** if the demonstrated root-to-finest change exceeds τ (by more than twice the statistical noise of the two runs);
  - **PASS** if U ≤ τ/2;
  - otherwise **INCONCLUSIVE**.
- **Domain error model:** |e| ∝ (D/H)^q with q = 1, the slowest classical blockage scaling (**EXPERT REVIEW**).

### Error budget and aggregation

- **ACCEPT** requires all of the following:
  1. every gate check PASSes (policy INCONCLUSIVEs can be discharged by measured evidence: Courant by a time-step study, scheme order by a mesh study);
  2. every component (averaging, statistics, mesh, time, domain) PASSes for every requested quantity;
  3. the measured averaging bias **plus** the root-sum-square of the independent uncertainty components (statistics, mesh, time, domain) is ≤ τ. A known, signed bias adds linearly; only independent uncertainties combine by RSS (ASME V&V 20 style).
- **REJECT** when any check FAILs.
- **INCONCLUSIVE** otherwise.

ACCEPT is therefore expensive (it needs mesh, time and domain studies). That is intentional: **rejecting a flawed result needs one demonstrating experiment, while trusting a result needs all error sources bounded.**

## 14. Adversarial failure cases

Defined as diffs against the baseline in `cases/adversarial/*.yaml`, with flaw,
plausibility and expected mechanism recorded. Each was run, inspected and kept or
discarded (`cases/adversarial/DISCARDED.md`). Measured outcomes are in
`reports/benchmark_results.md`.

| id | Flaw | Expected first detector |
|---|---|---|
| A1 | mesh ×0.5 | REFINE_MESH |
| B1 | inlet 8 D, outlet 15 D, sides 4 D (12.5 % blockage) | EXPAND_DOMAIN |
| C1 | Δt ×5, 3 PIMPLE outer correctors (Co ≈ 3.7) | REDUCE_TIME_STEP (Courant INCONCLUSIVE) |
| C2 | Euler time stepping, Δt ×4, 2 outer correctors | REDUCE_TIME_STEP |
| D1 | steady simpleFoam | static: physics_regime + steady convergence |
| E1 | no-slip walls on the far-field sides | EXPAND_DOMAIN (wall boundary layers scale with the domain) |
| F1 | first-order upwind convection | REFINE_MESH (scheme-order INCONCLUSIVE) |
| G1 | 40 D/U run, averaged from 10 D/U | static averaging check / RUN_LONGER |
| H1 | dynamic viscosity entered as ν (Re = 83) | static reynolds_consistency |
| I1 | stale magUInf (0.16 vs 0.15) | static force_reference_consistency |
| J1 | wake streamwise cells ×0.3 | REFINE_MESH |

## 15. Failures that existing OpenFOAM diagnostics detect

- Divergence: the C1 v0 candidate (Δt ×10) crashed, so it was discarded.
- checkMesh errors.
- Steady non-convergence of residuals (if the user checks it).

## 16. Failures that existing diagnostics may miss

Everything in §14 except the crash: discretisation error, domain error, temporal
error, averaging bias, wrong Re, wrong force normalisation, and wrong regime. In
these cases the solver completes and checkMesh passes.

## 17. Where expert judgement is still required

See research §7. In summary:
- choice of error model for the domain;
- the qualitative regime map;
- whether a boundary-condition *type* is right;
- model-form questions (2D/laminar);
- what tolerance is appropriate.

## 18. Active experiments (`src/socrates/experiments/primitives.py`)

| Primitive | Parameters (range, default) | Initialisation | Records |
|---|---|---|---|
| REFINE_MESH | factor [1.3, 2.0], √2 | mapFields from parent if periodic, else fresh | config diff, Courant-driven Δt change |
| REDUCE_TIME_STEP | factor [1.5, 4], 2 | mapFields (same mesh) | config diff |
| EXPAND_DOMAIN | factor [1.5, 3], 2 | non-consistent mapFields if periodic | config diff, preserved near-field |
| RUN_LONGER | additional [25, 300] D/U, 100 | restart from latest time | new end time |

- **Hard limits:** cumulative refinement ≤ 2; ≤ 160 k cells; Δt ≥ root/8; domain ≤ 4× root; end time ≤ 600 D/U.
- **Every child run is stored** with its parent, reason, requesting planner, config diff, initialisation and provenance (content-addressed; identical requests reuse the stored run).
- **Mapped children:** run 80 D/U, with the transient removed by MSER. An already-periodic start adjusts faster than a fresh start; this was reduced from 100 D/U for compute before any child was run.
- **Fresh starts** (if the parent has no periodic state) use the parent's duration. Mapping a non-shedding field could suppress shedding that the child would develop.

## 19. Success criteria for the prototype (fixed before evaluation)

1. **Infrastructure:** the full loop runs autonomously on real OpenFOAM simulations, with provenance for every run.
2. **Baseline credibility:**
   - the baseline's stationary Cd and St lie within the literature band widened by τ;
   - its own verification (mesh, time and domain studies) bounds the numerical uncertainty below τ, or the report explains why not.
3. **Primary demonstration (brief §22):** at least one case where
   - the solver completes,
   - OpenFOAM diagnostics see nothing wrong,
   - the static verifier returns INCONCLUSIVE,
   - the adaptive system requests an experiment that exposes the flaw quantitatively,
   - and the final verdict is REJECT.
4. **Safety:** System C false acceptance rate on flawed cases = 0. Any false acceptance is reported and diagnosed.
5. **Value test (falsifiable):**
   - System C must resolve (ACCEPT/REJECT correctly) at least one case that System B leaves INCONCLUSIVE. Otherwise active experiments add nothing.
   - The LLM planner must beat the pre-registered rule-based planner on accuracy or cost. **Otherwise the report must state that the LLM adds no measurable value.**

### Pre-registered evaluation protocol

- **Ground truth.** The in-house converged solution T for each quantity is the finest/largest/smallest-Δt run with Richardson extrapolation where available, checked against the literature band.
  - error e_q = |reported_q − T_q|/T_q;
  - **flawed** if max_q e_q > τ, or if the set-up answers a different problem (wrong Re or regime); the rationale is recorded;
  - **credible** if max e_q ≤ τ/2 and the set-up is consistent;
  - **ambiguous** otherwise.
- **Systems:**
  - **A** — OpenFOAM diagnostics only: ACCEPT if the solver completed, checkMesh is OK, and (steady) residualControl is satisfied; otherwise REJECT.
  - **B** — static deterministic verifier, one run.
  - **C** — adaptive: deterministic verifier + LLM critic + experiments, strict authority.
  - **Ablations:**
    - **C-rule:** adaptive with the rule-based planner. Fixed order: statistics/averaging → mesh → time → domain; default parameters; continue refinement families from their finest member.
    - **B+exh:** exhaustive non-adaptive protocol: RUN_LONGER, REFINE_MESH √2 twice, REDUCE_TIME_STEP, EXPAND_DOMAIN, then verify.
    - **L-judge:** LLM judge on static evidence without experiments and without deterministic gating.
- **Budgets for C and C-rule:** ≤ 6 experiments, ≤ 12 planner calls, total experiment compute ≤ 12× the root run.
- **Metrics:**
  - correct-acceptance rate;
  - detection (REJECT) rate on flawed cases;
  - false acceptance rate;
  - false rejection rate;
  - inconclusive rate;
  - number of experiments;
  - experiment cell-steps and wall time;
  - LLM cost;
  - first-experiment usefulness (did the first experiment target the true flaw, per the §14 mapping);
  - authority violations;
  - untraceable numbers in critic text.

## 20. Implementation plan (two weeks; executed in compressed form)

| Days | Work | Status |
|---|---|---|
| 1–2 | Research; parametric generator; runner; parsers tested on real output | done |
| 3–4 | Baseline run and validation; evidence engine | done |
| 5–6 | Static verifier; adversarial cases run and screened | done |
| 7–8 | Experiment primitives with provenance; mesh/time/domain studies on baseline | done; the reference needed three further stages (methodology §8) |
| 9–10 | Critic and loop; rule-based planner | done |
| 11–12 | Benchmark A/B/C + ablations | A, B, L-judge complete; C-rule, C-llm, Bexh and LLM repeats running |
| 13–14 | Attacks on the verifier; final reports | attacks mostly complete; baseline report final; benchmark and final reports pending |

---

## Major technical risks

1. **Compute.** Accepting a result needs ~5 extra runs, and refined runs are 2–8× the root cost. Mitigations: mapped initialisation, run cache, budgets.
2. **The in-house truth could itself carry ~1 % error**, which matters for cases near the τ boundary. Mitigation: label such cases "ambiguous".
3. **Two-level Fs = 3 is very conservative**, so credible cases may stay INCONCLUSIVE within budget. That would be a real finding about the cost of rigour, not a bug.
4. **The LLM critic may use prior knowledge** of cylinder drag (leakage despite blind mode). Mitigations: numeric audit, and an authority structure in which the LLM never decides acceptance.
5. **Single benchmark, ~15 cases.** Rates have wide confidence intervals; results are indicative only.

## Assumptions most likely to be wrong

- The domain-error order q = 1.
- Mapped initialisation gives the same limit cycle as a fresh start. Believed true for this regime, not verified for every case.
- The free-slip versus Dirichlet side condition is immaterial at 1.25 % blockage.
- That an LLM can be kept from using memorised reference values.

## What a CFD researcher should validate

- Baseline set-up and its validation (`reports/baseline_validation.md`).
- The error-budget rule (τ/2 per component, RSS ≤ τ).
- Fs choices and the domain-error model.
- Whether each adversarial case's "flaw" label is fair.
- Whether the regime check is an acceptable form of prior knowledge.

## Smallest experiment that could falsify the idea

Take A1 (coarse mesh) and run the static verifier and one REFINE_MESH.

- **The idea is falsified** if either:
  - the static verifier alone already REJECTs A1 (static checks would suffice); or
  - the refinement does not move St by more than τ (the "flaw" is not real at this tolerance).
- **The idea is supported** if the static verifier returns INCONCLUSIVE and one refinement demonstrates a > 3 % change. That costs one extra run (~1 h).

More generally, if on the full benchmark System B + a fixed exhaustive protocol is as accurate as System C at similar cost, then *adaptivity* adds nothing. If C-rule matches C, then *the LLM* adds nothing.
