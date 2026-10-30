# Weekend-5090 run — complete results & how to reuse them

> Branch: `physis/weekend-5090` (commit `e27d27c`). Run finished 2026-10-30 02:04 UTC+? on
> `gpu-5090-92` (NVIDIA RTX 5090, 31.3 GB). Exit code 0. Full output committed under
> `physis/runs/weekend-20261030-main/`.

This document is the full context for the first real GPU dataset + learned closure. It is
meant to be read by a fresh agent so it has everything without re-deriving it: what was run,
every number, the exact data format, and what the results do and do not support.

---

## 1. What was run

`scripts/weekend_5090.py` full pipeline on the RTX 5090, all stages:

| stage | result |
|---|---|
| preflight | GPU 5090, torch 2.11.0+cu128, CUDA 12.8, Triton 3.6.0 |
| selfcheck | **Triton D3Q19 kernel vs float64 torch reference: PASS** (max abs diff 1.517e-10, ref scale 3.603e-4) |
| gates | Poiseuille 3D **PASS**, Sangani–Acrivos sphere array **PASS** (pytest, CPU float64, 28 min) |
| resolution | one sphere structure at 64³→256³; 384³/512³ skipped (memory guard) |
| dataset | **600 samples** at 128³, all `ok`, all converged |
| train | Kozeny–Carman baseline vs MLP ensemble, 2 splits |
| forchheimer | inertia onset, 3 structures |
| cnn | 3D CNN on raw voxel volumes |
| report | `report.md` + parity plots |

**Timing:** dataset ~19 s/sample (600 samples ≈ 3.2 h); gates 28 min; everything else minutes.
Solver throughput ~9,300 MLUPS on the Triton path.

---

## 2. The headline result: learned closure vs Kozeny–Carman (target = log₁₀ K)

| split | model | R² | MAE (log₁₀ K) | max abs err | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.837 | 0.163 | 2.016 | 120 |
| random | mlp_ensemble | **0.984** | 0.039 | 0.694 | 120 |
| random | uncertainty↔error (Spearman) | 0.62 | | | |
| porosity band held out | kozeny_carman | **0.936** | 0.100 | 0.218 | 109 |
| porosity band held out | mlp_ensemble | 0.931 | 0.083 | 0.566 | 109 |
| porosity band held out | uncertainty↔error (Spearman) | 0.21 | | | |

**Interpretation (the honest physics answer):**
- The MLP strongly beats Kozeny–Carman *inside* the trained porosity range (interpolation).
- On a **held-out porosity band** (extrapolation) the MLP does **not** beat KC — it ties/edges
  out slightly (0.931 vs 0.936). The physics baseline generalizes; the neural net does not
  extrapolate. This is a real, meaningful result, not a bug.
- Uncertainty signal (Spearman 0.62 on random split) is predictive of error in-distribution
  but weak out-of-distribution (0.21).

**3D CNN on the raw voxel volume** (no hand features, input 32³ solid-fraction field):
- R² **0.979**, MAE 0.044, max err 0.924 (log₁₀ K), n_test=120.

So structure alone (raw voxels) carries almost all the permeability signal. The closure is
well-learnable; the open question is extrapolation beyond the training porosity band.

---

## 3. Dataset — exact contents

`runs/weekend-20261030-main/dataset.jsonl` — 600 lines, one JSON object per line. Summary:

- **families:** spheres 200, voids 200, gyroid 200
- **porosity range:** 0.209 – 0.846 (mean 0.554)
- **permeability (real, lu²):** 9.6e-7 – 9.6e-3
- **status:** 600/600 `ok`, 600/600 `converged`
- **impl:** 600/600 `triton` (fast path)
- **solver:** D3Q19 TRT, τ₊=1.5, periodic, force-driven, tol 1e-6, n=128³

Per-row keys (example, `index` 0):
`family, n, geometry{type,box,count,radius,radius_spread,seed,voids | type,periods,level},
porosity, specific_surface, hydraulic_diameter, kozeny_carman, force_lu, tau_plus, status,
permeability, permeability_lu, tortuosity_hydraulic, mach_max, reynolds_pore, steps,
converged, impl, wall_time_s, mlups, index`

- `permeability` = physical permeability (lu², box length 1). `permeability_lu` is the same
  quantity in lattice units (differently scaled; the resolution study uses it).
- `kozeny_carman` = the KC baseline prediction for the same structure.
- `geometry` fully specifies the structure. **The dataset is exactly reproducible** from
  `geometry.seed` (rng seed = `10_007 * (index + 1) + seed_offset`) — no need to keep volumes
  for correctness, only for speed.

**Voxel volumes** `runs/weekend-20261030-main/volumes/{index:05d}.npy` — 600 × 32³ float16
solid-fraction fields, one per sample. **These are the CNN inputs** (the CNN loads exactly
these files; see `weekend_5090.py` stage_cnn around line 315). If your agent wants to retrain
or extend the CNN, point it at these files — recomputing them costs ~19 s/sample on the GPU.

---

## 4. Resolution study (is 128³ enough?)

One sphere structure, K vs grid size:

| n | K | rel to 256³ | steps |
|---|---|---|---|
| 64³ | 7.523e-4 | +0.59% | 500 |
| 96³ | 7.440e-4 | −0.53% | 1008 |
| 128³ | 7.433e-4 | −0.62% | 1990 |
| 192³ | 7.458e-4 | −0.29% | 4032 |
| 256³ | 7.479e-4 | +0.00% | 7164 |
| 384³/512³ | skipped_memory (needs 9.3 / 22.1 GB) | | |

128³ is within ~0.6% of 256³ — resolution-converged to well under 1%. The 600-sample dataset
at 128³ is a defensible compromise (256³×8 voxels ≈ 3 h → ~24 h for 600).

---

## 5. Forchheimer (inertia onset — the transpiration-cooling design point)

Darcy + quadratic fit K = K_darcy/(1 + F·Re), where F = β√K:

| structure | porosity | K_darcy (lu²) | K_fit (lu²) | **F = β√K** | Re range |
|---|---|---|---|---|---|
| spheres | 0.608 | 7.39 | 7.61 | **0.27** | 0.29–12.6 |
| voids | 0.595 | 2.30 | 2.40 | **0.97** | 0.12–5.3 |
| gyroid | 0.582 | 14.03 | 15.13 | **0.34** | 0.40–29.4 |

Inertia is small at F ≤ 1; Darcy dominates below Re ≈ 1. Full force/u/Re/mach tables are in
`stage_forchheimer.json`.

---

## 6. Files committed (all under `physis/`)

- `runs/weekend-20261030-main/report.md` — 1-page summary (the intended "send this folder back")
- `runs/weekend-20261030-main/dataset.jsonl` — the 600-sample dataset (the main artifact)
- `runs/weekend-20261030-main/volumes/*.npy` — CNN inputs (600 × 32³)
- `runs/weekend-20261030-main/stage_*.json` — every stage's full numbers
- `runs/weekend-20261030-main/parity_random.png`, `parity_porosity_band_held_out.png`
- `runs/weekend-20261030-main/run.log` — full live log
- `docs/weekend-5090-results.md` — this document
- `scripts/weekend_5090.py` — runner (now with `--sample-offset` for parallel shards)
- `scripts/run_weekend_nohup.sh` — detached launcher

`runs/` is gitignored by default; this run folder was explicitly un-ignored so the data is in
the repo (`!.gitignore` negation in `.gitignore`).

---

## 7. Caveats & what's next

- **Dataset is 600 unique samples, not 1200.** The overnight "shard" on a second node
  duplicated samples 0–599 (the index-shift monkeypatch never crossed the subprocess
  boundary). Root cause fixed: `weekend_5090.py` now takes `--sample-offset N` so a shard
  `--samples 600 --sample-offset 600` produces genuinely distinct samples. It has **not** been
  re-run — the 600-sample set is the current deliverable.
- **Extrapolation is the open research question.** In-band closure is solved (R² 0.98, CNN
  R² 0.98). Out-of-band the MLP doesn't beat KC. Candidates: train on a wider porosity sweep
  (`--samples` with wider family sampling), physics-informed features, or domain-decomposition
  of the porosity axis.
- Triton kernel was written on a Mac and validated against float64 torch reference on the GPU;
  it passes at 1.5e-10. Safe to trust for future runs.
- To rerun everything: `physis/scripts/weekend_5090.py --force` (GPU + ~4 h) or
  `--quick` for a smoke test.
