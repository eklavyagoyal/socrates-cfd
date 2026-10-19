# Baseline validation: 2D cylinder, Re = 100

This report establishes whether the baseline case is a credible answer to the engineering question, and builds the
in-house converged reference ("truth") used to label every benchmark case. All numbers come from
`results/runs/` via `scripts/make_baseline_report.py`. The full generated tables are in
[`baseline_generated.md`](baseline_generated.md); the reference values and chains are in `results/baseline/truth.json`.

**Question** (`configs/problem_cylinder_re100.yaml`): time-mean drag coefficient and Strouhal number of a 10 mm rod
in a uniform 0.15 m/s air stream (Re = 100), per unit span, to within 3 % each, treating the stream as unbounded.

## 1. Summary

| | mean Cd | St |
|---|---|---|
| baseline, stationary window | 1.3311 | 0.1634 |
| in-house converged reference T | **1.3133 ± 0.72 %** | **0.1647 ± 1.06 %** |
| baseline error vs T | +1.36 % | −0.78 % |
| literature band (research.md §2.3) | 1.31–1.33 | 0.164–0.166 |
| Qu et al. (2013), H = 200 D, the widest domain in the literature set | 1.310 | 0.1647 |

- **The baseline is credible.** Its errors relative to the converged reference are within τ/2 = 1.5 % for both
  quantities (point estimates). The drag error is almost entirely domain blockage.
- **The reference agrees with the literature.** T lies inside the narrow literature band for both quantities. It is
  within 0.25 % (Cd) and 0.0 % (St) of the large-domain result of Qu et al. (2013).
- **Success criterion 2a (pre-registered) is met:** the baseline's stationary Cd and St lie within the literature
  band widened by τ. They are just outside the narrow band (Cd +0.08 % above 1.33, St 0.35 % below 0.164).
- **Success criterion 2b is met only in part.** The baseline's own verification bounds the combined numerical
  uncertainty below τ (root-sum-square 2.1 % for Cd, 2.3 % for St). However, the pre-registered verifier still returns
  INCONCLUSIVE for the baseline even with all seven study runs, because two components exceed the per-component limit
  τ/2. Section 6 explains why. This matters for the whole benchmark: a credible case built on the baseline's domain
  cannot be ACCEPTed by the pre-registered rule.

## 2. Case set-up

| item | choice | reason |
|---|---|---|
| domain | 30 D upstream, 50 D downstream, ±40 D laterally (blockage 1.25 %) | Posdziech & Grundmann: inlet > 20 D; Behr et al. 1995: laterals ≥ 8 D |
| mesh | 30,580 hexahedra; O-grid with 160 cells around the cylinder; first cell 0.005 D | ~20 cells inside the D/√Re boundary layer |
| solver | `pimpleFoam` in PISO mode (1 outer, 2 pressure correctors) | transient incompressible laminar |
| schemes | backward (BDF2) in time; `linearUpwind` convection; linear gradients and Laplacian | second-order formal accuracy |
| time step | 0.01 D/U (max Courant number 0.73; ~612 steps per shedding period) | PISO needs Co < 1 |
| run length | 150 D/U; declared averaging window 75–150 D/U (11 cycles) | transient decays by ~70 D/U |
| boundary conditions | uniform inlet, `inletOutlet`/fixed pressure outlet, free-slip (`symmetryPlane`) sides, no-slip cylinder | unbounded stream |
| shedding trigger | `setFields` cross-flow perturbation in the near wake | avoids a long symmetric transient |

Diagnostics:
- checkMesh: Mesh OK (max non-orthogonality 43°, skewness 0.53, aspect ratio 21).
- Final pressure solve: converged in 100 % of steps.
- Continuity errors: 5e-14.
- Boundary mass imbalance: 8e-11.
- Statistics: 12 stationary cycles, batch-means 95 % CI of mean Cd 2.3e-5.
- Run length: continuing the run for a further 100 D/U (`baseline.long250`, 23 cycles) changes Cd by 0.01 % and St by 0.0 %, so the averaging is converged.

![baseline force history](figures/baseline_forces.png)

## 3. Verification study: one factor at a time

Each level was initialised by mapping the baseline's periodic state and run for 80 D/U; statistics come from the
stationary window. The mesh and time levels branch from the baseline; the ×4 domain level was mapped from the ×2 level,
because one EXPAND_DOMAIN step is limited to ×3. That ×4 run is stored as `baseline.D2x-4312d7d8fec3`: child names
record only the step's own factor.

| factor | levels | Cd | St | observed order | correction to T (Cd / St) |
|---|---|---|---|---|---|
| mesh, h = 0.457 → 0.323 → 0.229 D | 30.6k → 61.4k → 122.3k cells | 1.3311 → 1.3349 → 1.3349 (raw) | 0.1634 → 0.1644 → 0.1649 | 2.66 / 2.77 (after the time-overlap shift) | +0.60 % / +0.96 % |
| time, dt = 0.01 → 0.005 → 0.0025 | | 1.3311 → 1.3275 → 1.3258 | 0.1634 → 0.1636 → 0.1637 | 1.13 / 0.25 | −0.51 % / +0.49 % |
| domain, half-height 40 → 80 → 160 D | | 1.3311 → 1.3226 → 1.3179 | 0.1634 → 0.1627 → 0.1625 | 0.86 / 1.55 | −1.43 % / −0.66 % |

What the study shows:

- **Domain blockage is the largest error in the baseline.** It accounts for 1.4 % of drag at 1.25 % blockage, and drag
  is still falling between half-heights of 80 D and 160 D. The observed domain order (0.86) is close to the assumed
  order q = 1, which the design listed among the assumptions most likely to be wrong. This is consistent with Qu et al.
  (2013): H = 60 D → 200 D lowers Cd by 1.2 %.
- **Mesh refinement raises Cd and St.** The coarse mesh is numerically diffusive, which lowers both drag and the
  shedding frequency. The same mechanism, much stronger, drives case F1 (first-order upwind: St −23 %).
- **The time-step error converges more slowly than the scheme order.**
  - Cd: observed order 1.1, not 2. A plausible cause is the splitting error of the non-iterative PISO
    pressure–velocity coupling, which is first order.
  - St: the change per halving of dt barely shrinks (observed order 0.25). The differences are real: 7–8 × 10⁻⁴,
    10–20× the runs' statistical noise. It looks like an error that does not scale with dt (for example the
    fixed linear-solver tolerance).
  - The pre-registered rule therefore extrapolates St with p = 0.25 and Fs = 3, giving the largest St uncertainty
    term (1.0 %).
- **Mesh–time overlap.** Each finer mesh level was run with a smaller dt (0.0087 and 0.0061), because REFINE_MESH holds
  the Courant number. Its raw value therefore also contains part of the time correction. Each mesh level is shifted
  back to the baseline dt with the time chain's own error model C·dt^p before extrapolation.
  - Without the shift, the raw mesh chain looks converged after one refinement: observed order "∞".
  - The shift changes T by +0.31 % (Cd) and −0.12 % (St).
  - This correction was added after the reviewers flagged the double counting, before any label was computed.

## 4. In-house reference T

T = baseline value + the sum of the per-factor Richardson corrections (additive one-factor model, Celik et al. 2008).
Its uncertainty combines, by root-sum-square:
- each chain's discretisation uncertainty (Fs·|extrapolated − finest|);
- the statistical uncertainty of every chain member, carried through the extrapolation weights.

| | Cd | St |
|---|---|---|
| T | 1.3133 | 0.1647 |
| U(T), relative | 0.72 % | 1.06 % |
| largest terms of U(T) | domain extrapolation 0.55 %; domain members' statistics 0.42 % | time extrapolation (p = 0.25, Fs = 3) 1.02 % |
| T vs the narrow literature band | inside (1.31–1.33) | inside (0.164–0.166) |

The ×2 and ×4 domain levels were still drifting by 0.16 % within their 6-cycle windows; the far field adapts slowly
after a non-consistent mapping. That drift is the main statistical contribution. Running those two levels longer would
reduce U(T) for drag. It would not change any conclusion below: see section 7.

**Not a requested quantity: Cl rms.** The reference for the r.m.s. lift (0.2149 ± 4.1 %) falls *below* the
literature band (0.222–0.235).
- Cl rms decreases as dt decreases here (0.2286 → 0.2225 → 0.2196). Qu et al. report the opposite trend: CL′
  increases as dt decreases.
- This discrepancy is unexplained. Cl rms is not used anywhere in the verdicts or labels, but it is a warning that
  the time integration is not in its asymptotic range for oscillation amplitudes.

## 5. Validation against the literature

| source | domain / set-up | Cd | St |
|---|---|---|---|
| **this work, T** | extrapolated to an unbounded domain, h → 0, dt → 0 | **1.313 ± 0.009** | **0.1647 ± 0.0017** |
| Qu et al. 2013, D1 | H = 200 D, Δt = 0.02 | 1.310 | 0.1647 |
| Qu et al. 2013, D2 | H = 120 D | 1.315 | 0.1650 |
| Posdziech & Grundmann 2007 | H = 140 D | 1.325 | 0.1644 |
| Mittal 2005 | H = 100 D, slip sides | 1.322 | 0.1644 |
| Williamson 1989 fit | experiment | — | 0.1643 |

Every literature value in the table lies within T ± U(T), except the Cd of Posdziech & Grundmann (1.325, 0.9 % above
T). Their domain (H = 140 D) is smaller than the unbounded limit T is extrapolated to, and a smaller domain raises Cd.
The baseline itself (Cd 1.331, St 0.1634) sits at the upper edge of the drag band, which is what a 1.25 % blockage
domain should give.

## 6. What the deterministic verifier concludes about the baseline

| evidence available | verdict | blocking components |
|---|---|---|
| baseline run only (System B) | INCONCLUSIVE | mesh, time, domain not measured |
| baseline + the 7 study runs | **INCONCLUSIVE** | Cd domain U = 1.81 % > τ/2; St time U = 1.68 % > τ/2 |

The pre-registered error budget requires **each** component uncertainty to be ≤ τ/2 = 1.5 %, and their combination
≤ τ. With the full study:

| component | Cd: U | St: U |
|---|---|---|
| averaging, statistics | PASS | PASS |
| mesh | 0.85 % PASS | 1.33 % PASS |
| time | 0.64 % PASS | **1.68 % INCONCLUSIVE** |
| domain | **1.81 % INCONCLUSIVE** | 0.83 % PASS |
| root-sum-square of all components | 2.1 % (< τ) | 2.3 % (< τ) |

So the verifier refuses to accept a run whose actual errors (+1.36 %, −0.78 %) are within τ/2. The reasons are honest:

- **Cd, domain.** The baseline's domain error really is 1.4 %, close to τ/2. The Celik safety factor (1.25) turns that
  into an uncertainty of 1.8 %. A larger domain would pass. K2 (half-height 60 D, blockage 0.83 %) tests this in the
  benchmark.
- **St, time.** The observed time order is far below the formal order, so the conservative rule (p = observed,
  Fs = 3) applies. A further dt halving (dt/8) would show whether St converges.

The verifier's uncertainty estimates do bound the errors estimated from the reference:
- Cd: domain U 1.81 % against an estimated domain error of 1.43 %;
- St: time U 1.68 % against an estimated time error of 0.49 %.

In that sense the uncertainty estimates are correct and the rule is merely conservative. This is the risk the design
pre-registered as "two-level Fs = 3 is very conservative, so credible cases may stay INCONCLUSIVE within budget". At
τ = 3 %, the per-component τ/2 rule and this baseline domain make "credible and acceptable" a very narrow target. Any
post-hoc relaxation (for example an RSS-only rule) is reported separately in the final report and is not used for
the pre-registered results.

## 7. Consequences for the benchmark labels

Labels use the pre-registered rule e = |reported − T|/T: flawed if > τ (or the set-up solves another problem),
credible if ≤ τ/2, ambiguous otherwise. The pre-registered mitigation adds that a case is ambiguous when the
interval [e − U(T), e + U(T)] straddles τ or τ/2.

- U(T) is 0.72 % (Cd) and 1.06 % (St). Every case whose error lies within about 0.7–1.1 % of 1.5 % or 3 % is
  therefore ambiguous.
- That includes the baseline itself: e_Cd = 1.37 %, interval [0.65 %, 2.09 %].
- So **no benchmark case is robustly credible** under the pre-registered labels. Correct-acceptance and
  false-rejection rates are undefined on the primary labels.
- The analysis therefore also reports a secondary, post-hoc view with point-estimate labels (baseline, K2 and C1
  credible). It is clearly separated from the primary results.

Running the ×2 and ×4 domain levels longer would cut the statistical term, but would not bring U(T) for St below
1 %; that term comes from the time chain. The labels would not change.

## 8. Limitations

- The truth assumes that mesh, time and domain errors are additive and independent. It is built from one-factor
  chains around a single point, not from a full factorial study.
- The time-overlap shift uses the time error model measured at the baseline mesh.
- Mapped initialisation was assumed to reach the same limit cycle as a fresh start. The 250 D/U continuation agrees
  with the 150 D/U fresh run to 0.01 %; the mapped levels' stationarity is documented in the reliability table of
  `baseline_generated.md`.
- The domain chain uses free-slip lateral boundaries. Other side conditions converge at a different rate.
- Single-core runs are bitwise reproducible (methodology §9); the reference has not been reproduced with a second
  code.
