# Phase 0 — Research

This document records the research the design rests on. **Label convention:**
**[V]** = checked against a fetched primary source or the OpenFOAM v2412 source
code; **[S]** = from a secondary source that quotes the primary; **UNVERIFIED** = not
confirmed against any fetched source (must not be relied on without checking).
Verification URLs are given inline. Items needing review by a CFD researcher are
marked **EXPERT REVIEW**.

---

## 1. Benchmark selection

### 1.1 Candidates considered

| Candidate | Reference quality | Domain definition | Cost per run | Fit to the adversarial programme |
|---|---|---|---|---|
| **Unbounded cylinder, Re = 100** (2D, periodic) | Many independent DNS results in a ~2 % band; empirical St–Re fits from experiments | Artificial far-field boundaries must be chosen → domain size is part of the numerical error | ~20 min on 1 core at 30k cells | All failure modes are natural, including domain size and steady assumption |
| Schäfer & Turek DFG 2D-2 (channel, Re = 100) | Very precise (FeatFlow, 4–5 digits) | Fully specified channel (blockage 24 %) | cheaper | The domain is part of the *problem*, so the "domain too small" failure doesn't apply; a confined, asymmetric flow is less representative of an engineering "unbounded" question |
| DFG 2D-1 (Re = 20, steady) | Extremely precise | Fully specified | cheap | No unsteadiness → no time-step, averaging or steady-assumption failures |
| Unbounded, Re = 200 | Good | Artificial | similar | 2D is physically questionable (3D mode A at Re ≈ 188.5) |

**Decision: unbounded 2D cylinder at Re = 100.** It is the canonical laminar periodic
bluff-body flow. Its reference data are independent, well cited and agree closely.
It is genuinely 2D. And every failure mode the brief asks about (mesh, domain, time
step, steady assumption, boundary conditions, averaging, Reynolds-number and
force-normalisation errors) occurs naturally rather than being forced.

Its weakness is a reference band of about 2 % (not 0.01 %), caused by differences in
domain and resolution between studies. The project handles this by (i) setting the
requested tolerance at 3 %, (ii) building an in-house converged solution (fine mesh,
large domain, small Δt) and checking it against the literature band, and
(iii) labelling benchmark cases by their error relative to that converged solution.

Schäfer–Turek 2D-2 is noted as a future **code-verification** add-on (§9).

### 1.2 Physical regime (is 2D valid at Re = 100?)

- **Onset of periodic shedding.** Re_c ≈ 47 (Hopf bifurcation).
  - Qu et al. 2013 [V] use Re_c ≈ 47.4, citing Norberg 1994 and Kumar & Mittal 2006.
  - A compilation (arXiv 2509.07192, Table 5) [S] spans 46.2–47.9: Jackson 1987 46.2; Williamson 1989 47.9; Kumar & Mittal 2006 46.9.
  - Provansal, Mathis & Boyer 1987 (JFM 182:1, DOI 10.1017/S0022112087002222): abstract [V], exact Re_c value UNVERIFIED.
- **Onset of 3D wake instability.** Barkley & Henderson 1996 (JFM 322:215, DOI 10.1017/S0022112096002777) [V abstract] put mode A at **Re = 188.5 ± 1.0**, wavelength 3.96 D. Williamson 1989 (JFM 206:579) [V] identifies the Strouhal discontinuity near Re ≈ 180 as the end of the laminar regime.
- **Conclusion.** Re = 100 ≈ 2.1 Re_c ≈ 0.53 Re_3D. Strictly two-dimensional periodic laminar shedding is the physical state, and a 2D laminar incompressible model is appropriate (Mach ≈ 4×10⁻⁴ for 0.15 m/s air).

### 1.3 Governing equations

Incompressible Navier–Stokes, constant ν, no body force:
∇·u = 0, ∂u/∂t + (u·∇)u = −∇p + ν∇²u,
with p the kinematic pressure. This is what OpenFOAM's `pimpleFoam` and `simpleFoam`
solve with a laminar momentum-transport model.

---

## 2. Reference data at Re = 100 (unbounded)

### 2.1 Primary: Qu, Norberg, Davidson, Peng & Wang (2013)

J. Fluids Struct. 39:347–370, DOI 10.1016/j.jfluidstructs.2013.02.007.
[V] Author version: http://publications.lib.chalmers.se/records/fulltext/180053/local_180053.pdf (Tables 1–3).

**Set-up:** second-order FV, Crank–Nicolson; square domain with Xu = Xd = H/2; free-stream
Dirichlet laterals; convective outlet; ≥ 80 cycles averaged; St from FFT of lift.
CL′ is r.m.s.

| Case | H (blockage) | Δt | CD | CL′ (rms) | −Cpb | St |
|---|---|---|---|---|---|---|
| D1 | 200 (0.5 %) | 0.02 | 1.310 | 0.2151 | 0.697 | 0.1647 |
| D2 | 120 (0.83 %) | 0.02 | 1.315 | 0.2163 | 0.703 | 0.1650 |
| D3 | 100 (1 %) | 0.02 | 1.317 | 0.2169 | 0.706 | 0.1652 |
| D4 | 60 (1.67 %) | 0.02 | 1.326 | 0.2191 | 0.719 | 0.1660 |
| D9 | 120 | 0.005 | 1.319 | 0.2253 | 0.709 | 0.1648 |
| D10 | 120 | 0.01 | 1.317 | 0.2224 | 0.707 | 0.1649 |
| D11 | 120 | 0.04 | 1.309 | 0.2031 | 0.696 | 0.1652 |

### 2.2 Other results (as compiled in Qu et al. Table 1 [V], plus fetched sources)

| Study | CD | St | CL′ | Domain |
|---|---|---|---|---|
| Park, Kwon & Choi 1998 (KSME Int. J. 12:1200, DOI 10.1007/BF02942594) | 1.33 | 0.165 | 0.235 | C-grid, far field ~50 D |
| Kravchenko & Moin 1998 | 1.32 | 0.164 | 0.222 | O-mesh, outer diameter 120 D |
| Shi et al. 2004 | 1.318 | 0.1640 | – | circle of diameter 300 D |
| Mittal 2005 (IJNMF 49:1147) | 1.322 | 0.1644 | 0.226 | H = 100, slip sides |
| Stålberg et al. 2006 | 1.32 | 0.166 | 0.233 | far field 40 D |
| Posdziech & Grundmann 2007 (JFS 23:479, DOI 10.1016/j.jfluidstructs.2006.09.004) | 1.325 | 0.1644 | 0.228 | H = 140 |
| Li et al. 2009 (LBM) | 1.336 | 0.164 | – | H = 100, periodic sides |
| Henderson 1995 (Phys. Fluids 7:2102) | 1.35 [S] | – | – | primary not accessible |

**Empirical fits:**
- **Williamson 1989** (JFM 206:579, DOI 10.1017/S0022112089002429) [V]: parallel-shedding fit St = −3.3265/Re + 0.1816 + 1.6×10⁻⁴ Re over Re 49–178, mean error 0.06 %. This gives **St(100) = 0.1643**.
- **Norberg's r.m.s.-lift formula** CL′ = (ε/30 + ε²/90)^½, with ε = (Re − 47.4)/47.4: 0.2251 at Re = 100 (via Qu et al. [V]).
- Fey, König & Eckelmann 1998 coefficients: UNVERIFIED.

### 2.3 Recommended reference band (used only for validation and ground-truth labelling)

| Quantity | Band | Notes |
|---|---|---|
| Mean CD | **1.31–1.33** (wider 1.30–1.35) | values above ~1.36 indicate blockage or numerical diffusion |
| St | **0.164–0.166** | Williamson fit 0.1643 |
| CL′ (rms) | 0.222–0.235 | amplitude 0.31–0.33; very sensitive to Δt |

### 2.4 The forced-steady (unstable symmetric) branch

- Fornberg 1980 (JFM 98:819, DOI 10.1017/S0022112080000419) [V, Table 6]: **steady CD = 1.058 ± 0.001** at Re = 100.
- Dennis & Chang 1970: 1.056 [V via Fornberg].
- A forced-steady computation therefore under-predicts the time-mean drag by about **20 %**.

### 2.5 Domain size and blockage (central to adversarial case B and to the baseline domain)

- **Behr, Hastreiter, Mittal & Tezduyar 1995** (CMAME 123:309, DOI 10.1016/0045-7825(94)00736-7) [V full text]. Relative to lateral boundaries at 16 D:
  - at 4.5 D (11.1 % blockage): **CD +6.2 %, St +5.4 %**, lift amplitude +6.5 %;
  - at 6.25 D: +2.4 % / +2.1 %;
  - at 8 D: +1.0 % / +1.0 %;
  - at 12 D: +0.17 % / 0 %.
  - Their recommendation: lateral boundaries at least 8 D away.
- **Qu et al. 2013** [V]: H = 60 vs 200 → CD +1.2 %, St +0.8 %.
- **Tezduyar & Shih 1991** (J. Eng. Mech. 117:854) [V abstract]: outlet at 14.5 D gives no visible change; at ≤ 2.6 D the flow becomes steady.
- **Posdziech & Grundmann 2007** (as reported by Qu): CD depends strongly on domain size, St much less; inlet should be > 20 D. Exact effect sizes UNVERIFIED (paper paywalled).
- **Kumar & Mittal 2006** (IJNMF 50:987) [V abstract]: Re_c and the onset frequency vary with blockage.

### 2.6 Time-step sensitivity

- Qu et al. [V]: going from Δt = 0.005 to 0.04 (in D/U) lowers **CL′ by 9.8 %** but CD by only 0.8 % and St by < 0.3 %. The lift amplitude is the most time-step-sensitive quantity.
- Behr et al. 1995 [V]: St is "significantly affected by the dissipation introduced by the time-integration scheme".

---

## 3. Verification and validation methodology

### 3.1 Terminology (ASME V&V 20-2009, via Coleman's overview [V])

- **Code verification:** the code solves its equations correctly (e.g. manufactured solutions).
- **Solution verification:** estimate the numerical uncertainty u_num of *this* calculation.
- **Validation:** comparison error E = S − D, and u_val = (u_D² + u_num² + u_input²)^½. If |E| ≫ u_val then δ_model ≈ E; if |E| ≤ u_val the model error is lost in the noise.

**This project is about solution verification.** Validation against reference data is
used only to (a) show the baseline is credible and (b) label the benchmark.

### 3.2 Grid convergence (Celik et al. 2008, J. Fluids Eng. 130:078001, DOI 10.1115/1.2960953) [V]

1. **Representative size.** In 2D, h = [(1/N) Σ ΔA_i]^½. For a one-cell-thick OpenFOAM mesh, use the in-plane area; V^(1/3) would bias the apparent order by a factor of 1.5.
2. **Three grids.** Refinement ratio r > 1.3 ("based on experience"). Refine systematically, ideally with geometric similarity.
3. **Apparent order.** p = |ln|ε32/ε21| + q(p)| / ln r21, with q(p) = ln[(r21^p − s)/(r32^p − s)] and s = sign(ε32/ε21). Solve by fixed-point iteration. ε32/ε21 < 0 means oscillatory convergence.
4. **Extrapolated value.** φ_ext = (r21^p φ1 − φ2)/(r21^p − 1).
5. **Fine-grid GCI.** GCI_fine = 1.25 e_a/(r^p − 1).
6. Iterative error should be at least 10× smaller than discretisation error.

**Factor of safety** (Roache 1994, J. Fluids Eng. 116:405; Roache 1998 book; NASA NPARC tutorial https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html [V]):
- **Fs = 3** for two-grid studies with an assumed order;
- **Fs = 1.25** for three or more grids whose observed order is in the asymptotic range.

**Eça & Hoekstra 2014** (J. Comput. Phys. 262:104, DOI 10.1016/j.jcp.2014.01.006) [V]:
least-squares fits on ≥ 4 grids; convergence classes from R = (φ1−φ2)/(φ2−φ3);
Fs = 1.25 only when convergence is monotone with 0.5 ≤ p < 2.1, otherwise Fs = 3. For
well-behaved data the method reduces to the GCI.

### 3.3 Temporal convergence for unsteady flows

- JFE numerical-accuracy policy [V]: temporal accuracy must be demonstrated.
- **Eça, Vaz, Toxopeus & Hoekstra 2019** (J. Verif. Valid. Uncert. Quantif. 4:021001, DOI 10.1115/1.4043975) [V abstract]: refinement at a constant Courant number mixes space and time error. Designs that refine Δt on a fixed grid and the grid at a fixed Δt separate them.
- **This project refines one factor at a time.** REFINE_MESH holds Δt fixed except where the Courant limit forces a recorded change; REDUCE_TIME_STEP holds the mesh fixed.

### 3.4 Statistics of time averages

- **MSER** (White 1997, Simulation 69:323, DOI 10.1177/003754979706900601 [V Crossref]; definition per Sánchez & White, WSC 2011 [V]): d* = argmin_d Σ_{i>d}(Y_i − Ȳ_d)²/(n−d)². The search is usually restricted to the first half of the record.
- **Oliver, Malaya, Ulerich & Moser 2014** (Phys. Fluids 26:035101, DOI 10.1063/1.4866813) [V]: effective sample size N/T0 from the autocorrelation.
- **For a periodic limit cycle the autocorrelation of the raw signal does not decay**, so these estimators cannot be applied to Cl(t) directly. This project therefore:
  - applies MSER to *per-cycle* quantities (cycle-mean Cd, lift amplitude, period);
  - averages over an integer number of cycles (the bias of a partial cycle is ≤ A/(πN) for a sinusoid);
  - takes the statistical uncertainty conservatively as the maximum of the batch-means CI, the linear drift and the half-window difference. Measured lag-1 autocorrelation of cycle means is 0.99 during the slow approach to the limit cycle, so naive batch-mean CIs would be invalid alone.
- **Strouhal extraction.** FFT bin width is 1/T_record, so 1 % resolution needs ~100 cycles without interpolation. We use zero up-crossings of Cl with linear interpolation as the primary estimate and a Hann-windowed, zero-padded FFT with parabolic peak interpolation as an independent cross-check. Cd oscillates at 2f, so St is taken from Cl.

---

## 4. What OpenFOAM v2412 already provides (source-verified)

The OpenFOAM source was read from the official GitLab mirror (`gitlab.com/openfoam/core/openfoam`, tag `OpenFOAM-v2412`).

| Facility | What it gives | Pitfall found |
|---|---|---|
| `checkMesh` | Topology/geometry checks. Defaults (`primitiveMeshCheck.C`): non-orthogonality 70°, skewness 4, aspect ratio 1000, closedness 1e-6 | **Always exits 0.** The verdict must be parsed ("Mesh OK." / "Failed N mesh checks"). Non-orthogonality > 70° is only a `*` warning; `***` items are failures |
| Continuity line (`continuityErrs.H`) | sum local = Δt·⟨\|∇·φ\|⟩_V; global = Δt·⟨∇·φ⟩_V; cumulative | Printed after every pressure corrector; take the last per step |
| Courant line (`CourantNo.H`) | max = 0.5·max(Σ\|φ\|/V)·Δt | Printed before the `Time =` line |
| `forceCoeffs` | Cd, Cl, Cm… with CofR/liftDir/dragDir, magUInf, lRef, Aref | **Column order changed in v2206+** (alphabetical: `Cd Cd(f) Cd(r) Cl …`); parse by header. In 2D, Aref = D × span. `rho rhoInf` is required for incompressible flow. The etc `forces.cfg` sets writeControl writeTime (would ruin St) |
| `solverInfo` | Residuals per field | **Records only the first solve of each time step** (`sp.first()`), so it cannot show whether the final pressure solve converged; the log must be parsed |
| `foamLog` | Residual/continuity/Courant histories from logs | — |
| PIMPLE `residualControl` | Outer-loop convergence | `outerCorrectorResidualControl` is Foundation syntax, not ESI v2412 |
| `runTimeControl` | Stop when an average settles | Not used: stopping on a settled average is precisely a "misleading convergence criterion" risk |

### What these diagnostics cannot tell you

They establish that the mesh is valid, the linear systems were solved, mass is
conserved and the run finished. **None of them estimates discretisation error,
domain-truncation error, temporal error, or averaging bias**, and none checks
whether the configured problem (Re, force reference values, solver type) matches the
question. Those judgements are left to the expert. They are what this project automates.

---

## 5. Known failure modes (literature)

- **First-order convection.** JFE editorial policy [V] calls first-order numerical diffusion "devastating" and requires at least second-order schemes. Borthwick 1986 (IJNMF 6:275) [V abstract]: upwind artificial viscosity "damps the wake and suppresses vortex shedding".
- **Lateral boundaries too close.** Behr et al. 1995 (§2.5).
- **Outlet too close.** Tezduyar & Shih 1991 (§2.5).
- **Large time step.** Damps lift amplitude (Qu et al. D11; Behr et al.).
- **Steady formulation above Re_c.** Converges at best to the unstable symmetric branch (Fornberg 1980), about −20 % in drag.
- **Over-specified inlet (U and p fixed) and outlet backflow.** Standard OpenFOAM practice is `inletOutlet` at outlets [tutorial pattern V; literature citation UNVERIFIED].
- **Agents that "succeed" but are wrong.** Foam-Agent (arXiv 2505.04997v3) [V]: 38 of 110 cases ran but were wrong. ChatCFD (arXiv 2506.02019) [V]: wrong boundary conditions "rarely trigger convergence failures". This directly motivates the project.

---

## 6. Existing automated / LLM-based CFD systems

| System | Verifies results? |
|---|---|
| MetaOpenFOAM (arXiv 2407.21320) [V] | No; success = executes / reaches endTime |
| MetaOpenFOAM 2.0 (arXiv 2502.00498) [V] | No quantitative verification; an LLM "reviews" accuracy |
| OpenFOAMGPT (Phys. Fluids 37:035120, 2025) [V] | No; human oversight required |
| OpenFOAMGPT 2.0 (arXiv 2504.19338) [V] | Ran a 5-mesh study when asked, but no error estimator |
| Foam-Agent (arXiv 2505.04997v3) [V] | No; 88 % execute, 42 % correct |
| ChatCFD (arXiv 2506.02019v3) [V] | Qualitative 3-tier review only |
| NL2FOAM (TAML 15:100594, 2025) [V] | L2 error vs one reference run |
| CFDLLMBench (arXiv 2509.20374) [V] | Binary refinement-convergence metric, but only for LLM-written Python solvers |
| cfdverify (ORNL, 2025) [V] | GCI / Eça–Hoekstra library; **not connected to any agent** |

NASA CFD Vision 2030 (NASA/CR-2014-218178) [V] names "automated management of
errors and uncertainties" as a goal and lack of automation as a barrier.

**The gap:** no system closes the loop *evidence → missing evidence → targeted
refinement experiment → quantitative uncertainty → verdict* on solver output.

---

## 7. Which judgements remain expert judgements

| Judgement | Status in this project |
|---|---|
| Is the mesh fine enough for this quantity? | Automated via systematic refinement + Richardson/GCI (needs extra runs) |
| Is the domain large enough? | Automated via EXPAND_DOMAIN. Error model order q = 1 is an assumption (**EXPERT REVIEW**) |
| Is Δt small enough? | Automated via REDUCE_TIME_STEP |
| Has the transient ended; are there enough cycles? | Automated (MSER on per-cycle series; RUN_LONGER) |
| Is the configured problem the asked problem (Re, force reference)? | Automated, deterministic consistency checks |
| Is the flow regime right (steady vs periodic vs 3D)? | Literature regime map for *this* geometry (qualitative). Generalising needs a per-problem knowledge base (**EXPERT REVIEW**) |
| Is the physical model right (laminar, 2D, incompressible)? | Not automated beyond the regime check. Model-form error is out of scope |
| Is the boundary-condition *type* appropriate? | Only indirectly, via domain sensitivity. No general check exists |

---

## 8. Items not verified (do not rely on without checking)

- Posdziech & Grundmann primary values for large domains, and their fit coefficients
- Henderson 1995 primary values (1.35 is secondary)
- Exact Re_c and St_c of Provansal and of Jackson
- Fey et al. coefficients
- Norberg 2003 tables
- John 2004 2D-3 reference values
- Exact Mockett et al. 2010 formulas
- ERCOFTAC BPG editor names
- Exact conversion of GCI to a standard uncertainty

## 9. Possible future code-verification case: Schäfer & Turek 2D-2

Schäfer & Turek 1996 (NNFM 52:547, DOI 10.1007/978-3-322-89849-4_39) [V preprint]:
- channel 2.2 × 0.41, D = 0.1, centre (0.2, 0.2), parabolic inflow, Um = 1.5, Re = 100 based on Ū = 2/3 Um;
- 1996 intervals: cDmax [3.22, 3.24], cLmax [0.99, 1.01], St [0.295, 0.305];
- FeatFlow 2014 reference (derived from the raw series): max CD 3.22739, max CL 0.98657, St 0.3018. **max CL lies outside the 1996 interval**, so use the newer data.
