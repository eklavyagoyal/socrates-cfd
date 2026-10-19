# Baseline validation: 2D cylinder, Re = 100

This report asks two questions:
- Is the baseline case a credible answer to the engineering question?
- What is the in-house converged reference ("truth") used to label every benchmark case?

Numbers come from `results/runs/` via `scripts/make_baseline_report.py`. The full generated tables are in
[`baseline_generated.md`](baseline_generated.md); the reference and its chains are in `results/baseline/truth.json`.
An adversarial fact-check of an earlier draft (43 issues) led to the second study stage described in §3 and to
corrections throughout.

**Question** (`configs/problem_cylinder_re100.yaml`): the time-mean drag coefficient and the Strouhal number of a
10 mm rod in a uniform 0.15 m/s air stream (Re = 100), per unit span, to within 3 % each. The stream is to be treated
as unbounded.

## 1. Summary

| | mean Cd | St |
|---|---|---|
| baseline, stationary window (250 D/U continuation) | 1.3312 | 0.1634 |
| in-house reference T (unbounded, h → 0, dt → 0) | **1.3046 ± 1.15 %** | **0.1638 ± 0.28 %** |
| baseline error vs T | **+2.04 %** | −0.24 % |
| literature band (research.md §2.3, finite domains) | 1.31–1.33 | 0.164–0.166 |
| Qu et al. (2013) domain series, extrapolated to an unbounded domain the same way | 1.302 | 0.1644 |

- **The baseline is not credible at τ = 3 % for drag; it is ambiguous.** Its drag error (+2.04 %) lies between
  τ/2 = 1.5 % and τ. Its St error (−0.24 %) is small. The drag error is almost entirely the finite domain:
  - the domain correction is −2.05 %;
  - the mesh (+0.58 %) and time-step (−0.52 %) corrections nearly cancel each other.

  The baseline was designed to be credible. The design used the literature drag band, but that band comes from
  finite domains, and the 40 D lateral distance turned out to be too small for a 1.5 % drag target.
- **The reference is consistent with the literature once domain size is accounted for.** It is within 0.23 % (Cd)
  and 0.36 % (St) of Qu et al.'s own domain series extrapolated to an unbounded domain. At matched domain size this
  work agrees with Posdziech & Grundmann (§5).
- **Success criterion 2a (pre-registered) is met:** the baseline's stationary Cd and St lie within the literature
  band widened by τ.
- **Criterion 2b is met as worded:** the baseline's verification bounds the numerical uncertainty below τ, or the
  report explains why not. Combining the verifier's component estimates by hand gives 2.8 % (Cd) and 1.86 % (St).
  The pre-registered verifier still returns INCONCLUSIVE for drag, because its per-component rule (U ≤ τ/2) fails
  for the domain component (U = 2.62 %). St reaches ACCEPT. That INCONCLUSIVE is consistent with the baseline's
  ambiguous label (§6).

## 2. Case set-up

| item | choice | note |
|---|---|---|
| domain | 30 D upstream, 50 D downstream, ±40 D laterally (blockage 1.25 %) | Posdziech & Grundmann: inlet > 20 D. Behr et al. (1995): laterals ≥ 8 D (+1 % Cd relative to 16 D). The domain study below shows 40 D laterals still leave about 2 % drag error relative to an unbounded stream. |
| mesh | 30,580 hexahedra; O-grid with 160 cells around the cylinder; first cell 0.005 D, radial growth 1.07 | about 12 cells inside D/√Re = 0.1 D |
| solver | `pimpleFoam` in PISO mode (1 outer, 2 pressure correctors) | transient, incompressible, laminar |
| schemes | backward (BDF2) time; `linearUpwind` convection; linear gradients and Laplacian | second-order formal accuracy |
| time step | 0.01 D/U (max Courant number 0.73; about 612 steps per shedding period) | PISO needs Co < 1 |
| run length | 150 D/U, declared averaging window 75–150 D/U (11 cycles) | |
| boundary conditions | uniform inlet; `inletOutlet` velocity and fixed pressure at the outlet; free-slip (`symmetryPlane`) sides; no-slip cylinder | |
| shedding trigger | `setFields` cross-flow perturbation in the near wake | |

Diagnostics:
- checkMesh: Mesh OK (non-orthogonality 43°, skewness 0.53, aspect ratio 21).
- Final pressure solve converged in 100 % of steps; continuity errors 5e-14; boundary mass imbalance 8e-11.
- 12 stationary cycles; 95 % CI of mean Cd 2.3e-5.
- Running a further 100 D/U (`baseline.long250`, 23 cycles) changes the stationary Cd and St by 0.002 %.

![baseline force history](figures/baseline_forces.png)

## 3. Verification study: one factor at a time, two stages

How the study levels were run:
- Every level was initialised by mapping a periodic state. The mesh and time levels branch from the baseline; the
  ×4 domain level was mapped from the ×2 level, because one EXPAND_DOMAIN step is limited to ×3.
- Mapped levels run for 80 D/U. MSER hit its 50 % cap on every mapped level, so its stationary window is simply the
  second half of the record. Stationarity is judged from the drift and half-window measures.

**Stage 2** was added after the fact-check, before any benchmark label was used:
- The ×2 and ×4 domain levels had not reached a limit cycle within 80 D/U. Their cycle-mean drag was still falling,
  because the wake had not yet crossed the enlarged domain. Both were continued:
  - ×2 to 180 D/U (`baseline.long180-…`): drag settled at 1.32188 (it was 1.32259 at 80 D/U);
  - ×4 to 280 D/U (`baseline.long280-…`): drag settled at 1.31576 (it was 1.31789 at 80 D/U), with the per-cycle
    mean constant to 10⁻⁵ over the last 120 D/U.
- A fourth time level (dt/8) was added to resolve the St time behaviour.

The reference uses each member's longest continuation and the finest three time levels. The ×4 run is stored as
`baseline.D2x-4312d7d8fec3`, because child names record only the step's own factor.

| factor | values used (Cd) | values used (St) | observed order (Cd / St) | correction (Cd / St, relative to the baseline) |
|---|---|---|---|---|
| mesh, h = 0.457 → 0.323 → 0.229 D (30.6k → 61.4k → 122.3k cells) | 1.3312 → 1.3359 → 1.3377 (shifted, see below) | 0.1634 → 0.1644 → 0.1647 (shifted) | 2.69 / 2.88 | +0.58 % / +0.92 % |
| time, dt = 0.005 → 0.0025 → 0.00125 (dt = 0.01 is the baseline) | 1.3275 → 1.3258 → 1.3250 | 0.16356 → 0.16367 → 0.16372 | 1.03 / 1.00 | −0.52 % / +0.21 % |
| domain, half-height 40 → 80 → 160 D | 1.3312 → 1.3219 → 1.3158 | 0.1634 → 0.1627 → 0.1623 | 0.60 / 1.14 | −2.05 % / −0.89 % |

What the study shows, and what it does not:

- **The domain correction dominates the drag error.** It is −2.05 %, with a chain uncertainty of 1.14 % of T.
  - The observed order (0.60) is well below the assumed q = 1, which the design listed among its riskiest
    assumptions. With q = 1 the correction would be about −1.4 %.
  - EXPAND_DOMAIN scales the inlet, outlet and lateral distances together. Its cell counts preserve the growth
    ratio, so the far field coarsens: the representative cell size goes 0.457 → 0.794 → 1.397 D. The chain therefore
    does not isolate blockage from inlet/outlet distance or far-field resolution.
  - The ×2 and ×4 meshes fail checkMesh's `-allGeometry` determinant check (152 and 264 far-field cells). This is the
    same check that fails on case J1.
- **Mesh refinement raises Cd and St.** The coarse mesh is numerically diffusive. The St mesh chain converges with
  observed order 2.88. For Cd, the order (2.69) and the correction (+0.58 %) are implied by the time-overlap shift
  described next: the raw Cd chain is flat after one refinement (1.3349 → 1.3349).
- **Mesh–time overlap.** REFINE_MESH holds the Courant number, so the finer mesh levels also used a smaller dt (0.0087
  and 0.0061). Their raw values therefore contain part of the time correction. Before extrapolation, each mesh level
  is shifted to the baseline dt with the time chain's own error model, C·dt^p (p = 1.03).
  - The shift changes T by +0.30 % (Cd) and −0.16 % (St).
  - Without it, T_Cd would be 1.3007 and the baseline's drag error 2.34 %.
  - The shift assumes that the time error is independent of the mesh. It was added after reviewers identified the
    double counting.
- **Time-step convergence is first order, not the formal second order**, for Cd, St and Cl rms alike (observed
  orders 1.0–1.1). The cause has not been identified. Candidates in a single-outer-corrector PISO step are the
  convecting face flux lagged from the old time level and the ddtCorr flux correction. A run with converged outer
  iterations at fixed dt would test this. Before dt/8 was added, the St differences barely shrank (apparent order
  0.25 from dt = 0.01 to 0.0025). A dt-independent error cannot cause that, because it cancels in differences.
  Competing first- and second-order terms can. Over the finest three levels St converges at order 1.0.
- **The time-step trends are opposite to the main literature source.** Here Cd and Cl rms fall and St rises as dt
  decreases. Qu et al. (Crank–Nicolson) report the opposite trend for all three. The time corrections in T depend on
  this solver-specific behaviour.

## 4. In-house reference T

T = baseline value + the sum of the per-factor corrections. This additive one-factor model is an assumption of this
work, in the style of Stern et al. (2001). Each chain is extrapolated with the Celik et al. (2008) procedure:
- Fs = 1.25 when the observed order lies within [0.5, 2]× the formal order;
- otherwise p = min(observed, formal) with Fs = 3. That rule comes from review corrections R4/E1, not from the
  pre-registered text, which used the formal order.

U(T) combines, by root-sum-square:
- each chain's discretisation uncertainty, Fs·|extrapolated − finest|;
- the statistical uncertainty of each chain's finest and middle members, carried through the extrapolation weights;
- the root's statistical uncertainty, once.

| | Cd | St |
|---|---|---|
| T | 1.3046 | 0.1638 |
| U(T) | 1.15 % | 0.28 % |
| largest term | domain extrapolation, 1.14 % | domain extrapolation 0.23 %, mesh 0.16 % |
| statistical part | 0.01 % (after the stage-2 continuations) | 0.02 % |

Before stage 2 the reference was Cd 1.3133 ± 0.72 %, St 0.1647 ± 1.06 %. The continued domain levels moved T_Cd by
−0.66 %, and the dt/8 level removed most of the St time uncertainty.

**Cl rms (not a requested quantity) has no converged reference.**
- Its domain chain is divergent (0.2286 → 0.2260 → 0.2199), so the generator fell back to the finest value.
- The time-overlap shift moves it by +2.5 %.
- The point value 0.2143 ± 4.1 % lies below the literature band (0.222–0.235), but T ± U overlaps the band.
- Cl rms is not used in any verdict or label.

## 5. Validation against the literature

The literature values come from finite domains, and Cd decreases as the domain grows. A like-for-like comparison
therefore evaluates this work's domain chain, a fit Cd = 1.3039 + 0.251·(1/half-height)^0.60 at the baseline mesh
and time step, at each source's domain size. The baseline's net mesh and time correction (+0.06 %) is then added, to
compare converged numerics with converged numerics.

| source | domain (full height) | source Cd | this work at the same domain | difference |
|---|---|---|---|---|
| Posdziech & Grundmann 2007 | H = 140 D | 1.325 | 1.324 | −0.1 % |
| Mittal 2005 (slip sides) | H = 100 D | 1.322 | 1.329 | +0.5 % |
| Qu et al. 2013, D3 / D2 / D1 (Dirichlet sides, Δt = 0.02) | H = 100 / 120 / 200 D | 1.317 / 1.315 / 1.310 | 1.329 / 1.326 / 1.320 | +0.9 / +0.8 / +0.8 % |
| Qu et al., series extrapolated to H → ∞ (same fit form; q = 0.88) | unbounded | 1.302 | T = 1.3046 | +0.2 % |
| Shi et al. 2004 | circle of diameter 300 D | 1.318 | — | — |

| St | value | vs T (0.1638) |
|---|---|---|
| Qu et al. D1 (H = 200 D) | 0.1647 | −0.5 % |
| Qu et al. series extrapolated to H → ∞ | 0.1644 | −0.4 % |
| Williamson 1989 fit (experiments) | 0.1643 | −0.3 % |

Agreement:
- This work agrees with Posdziech & Grundmann at matched domain size.
- It sits about 0.8 % above Qu et al. at matched domain size, although both studies extrapolate to nearly the same
  unbounded limit. The two domain series converge at different rates: q = 0.60 here (inlet, outlet and sides scaled
  together, with far-field coarsening) against 0.88 for Qu's square domains.
- About 1 % scatter between codes at fixed domain size remains. The table is a subset of research.md §2.2. Park et al.
  (1.33, far field ~50 D) and Li et al. (1.336, periodic sides) also lie above T + U(T); both used small or periodic
  domains.

## 6. What the deterministic verifier concludes about the baseline

| evidence available | Cd | St |
|---|---|---|
| baseline run only (System B) | INCONCLUSIVE (mesh, time, domain not measured) | INCONCLUSIVE |
| baseline + 10 study runs (stage 1 + 2) | **INCONCLUSIVE**: domain U = 2.62 % > τ/2 | **ACCEPT** (combined U 1.86 %) |

Component uncertainties with the full study:

| component | Cd | St |
|---|---|---|
| averaging, statistics | PASS | PASS |
| mesh | 0.85 % PASS | 1.33 % PASS |
| time | 0.65 % PASS | 0.67 % PASS |
| domain | **2.62 % INCONCLUSIVE** | 1.12 % PASS |

Reading this:
- **The drag INCONCLUSIVE is consistent with the label.** The estimated domain error is 2.05 %, above τ/2, and the
  verifier's domain uncertainty (2.62 % = 1.25 × the extrapolated change) cannot be below τ/2. The baseline's drag is
  ambiguous relative to T, so withholding acceptance is correct, not over-conservative.
- **No experiment within the limits can ACCEPT this drag.** The domain limit is 4× the root.
- **The verifier's U exceeding the corrections in T is not independent evidence.** The verifier and the reference use
  the same runs and the same Richardson procedure, so U = Fs × correction holds by construction. Independent evidence
  of calibration needs cases whose reference does not come from their own chains; the benchmark analysis reports such
  a calibration table.

This is not the "two-level, Fs = 3" risk the design pre-registered:
- the drag domain component uses a three-level estimate with Fs = 1.25;
- it fails because the domain error itself exceeds τ/2.

## 7. Consequences for the benchmark labels

Labels use the pre-registered rule, e = |reported − T|/T:
- flawed if e > τ, or if the set-up solves another problem;
- credible if e ≤ τ/2;
- ambiguous otherwise;
- also ambiguous if the interval [e − U(T), e + U(T)] straddles τ or τ/2, unless another quantity is clearly beyond
  τ. That exception is why A1 and B2 are flawed.

| label (pre-registered) | cases |
|---|---|
| flawed | A1, B1, B2, D1, F1, H1, I1 |
| ambiguous | baseline, K1, K2, A2, C1, C2, E1, G1, J1, G2 |
| credible | none |

Point-estimate labels are a secondary, post-hoc view:
- credible: A2, C1, J1, G2;
- ambiguous: baseline, K1, K2, E1, G1;
- flawed: the 7 above plus C2.

So the cases intended to be credible carry the baseline's ~2 % domain error in drag, and several intended-flawed cases
lie within τ/2. On this benchmark, the difference between "plausible but wrong" and "careful" is smaller than the
error of the shared domain. The analysis reports the primary and secondary views separately.

## 8. Limitations

- The reference assumes additive, independent mesh, time and domain errors. It is built from one-factor chains
  around a single point, not from a factorial study. The time-overlap shift uses the time error model of the
  baseline mesh.
- The domain chain does not isolate blockage (far-field coarsening, inlet and outlet scaled together). Its observed
  order of 0.60 sets the largest term of U(T).
- Mapped initialisation was assumed to reach the same limit cycle as a fresh start. The 250 D/U continuation is a
  restart, not a mapping, so it does not test this. The stage-2 continuations show that mapped domain levels need
  well over 80 D/U to settle.
- The time convergence is first order for reasons not yet identified, with dt trends opposite to Qu et al.
- Single-core runs are bitwise reproducible (methodology §9). The reference has not been reproduced with a second
  code.
