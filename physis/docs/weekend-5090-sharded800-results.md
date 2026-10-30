# Weekend-5090 run #2 — 800-sample sharded dataset (results summary)

> Branch: `physis/weekend-5090`, commit `ea62463`. Run finished 2026-10-30 ~19:02.
> **800 unique samples** across **7 GPUs** (2× RTX 5090 + 5× RTX 5080), merged on nc-9-1-3.
> Data committed under `physis/runs/weekend-20261030-sharded800/`.

## What was run

Parallel shards via `--sample-offset` (no monkeypatch — this is the fixed root-cause
sharding): 5090s ×150 (offsets 0, 150), 5080s ×100 (offsets 300–700) = 800 disjoint global
indices. Each shard ran `--stages dataset` detached (`setsid nohup`, survives SSH drops).
A collector on nc-9-1-3 waited for all 7 shards, pulled them via scp, ran
`merge_shards.py`, then `train,forchheimer,cnn,report` (no preflight/selfcheck needed).

**Merge result:** 800 samples, **798 ok** / 1 not_converged / 1 not_percolating. Zero
duplicate indices — sharding verified correct.

## Dataset

- families: spheres 267, gyroid 266, voids 265 (balanced)
- porosity 0.209 – 0.849 (mean ~0.55)
- permeability 9.6e-7 – 9.6e-3 (lu², box length 1)
- solver: D3Q19 TRT, τ₊=1.5, periodic, force-driven, 128³, Triton path
- volumes: 798 × 32³ float16 solid-fraction fields (`volumes/*.npy`) — CNN inputs

## Results (target = log₁₀ K)

| split | model | R² | MAE | max err | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.880 | 0.153 | 1.926 | 159 |
| random | mlp_ensemble | **0.976** | 0.041 | 1.205 | 159 |
| random | unc↔err Spearman | 0.59 | | | |
| porosity held-out | kozeny_carman | 0.944 | 0.090 | 0.209 | 165 |
| porosity held-out | mlp_ensemble | **0.988** | 0.036 | 0.190 | 165 |
| porosity held-out | unc↔err Spearman | 0.24 | | | |
| 3D CNN (voxels) | cnn | **0.983** | 0.038 | — | 159 |

**Headline (corrected after independent re-check):** the single-run 0.988 was a favorable
seed. Re-running the MLP with 3 seeds on the held-out porosity band gives 0.965 / 0.967 /
0.960 (KC 0.944) — consistently better than KC, but the margin is within seed noise, and the
earlier claim that more data "fixed" out-of-distribution extrapolation was overclaimed.

**Important limitation (unseen structure types):** the MLP one-hot-encodes the family, so it
has no geometric information for a family it never saw. Train on two families, test on the
third (CPU re-check, same data):

| held-out family | KC R² | MLP R² (2 seeds) |
|---|---|---|
| spheres | 0.868 | 0.72 / 0.82 |
| voids | 0.434 | 0.28 / 0.29 |
| gyroid | 0.944 | **−35 / −17** |

On a genuinely new structure type the learned model is far worse than Kozeny–Carman (gyroid:
orders of magnitude wrong). The closure is trustworthy **only for known families inside the
trained porosity range**; it is not general.

**Full generalization eval (multi-seed, CNN vs KC vs MLP on identical splits):** ran on a free
5090, 3 seeds per trainable model, R² = min–max over seeds. See
`runs/eval-generalization-20261030-194912/` and `scripts/eval_generalization.py`.

| split | KC R² | MLP R² | CNN R² |
|---|---|---|---|
| random | 0.880 | 0.973–0.974 | 0.983–0.988 |
| porosity band held-out | 0.944 | 0.954–0.962 | 0.750–0.849 |
| unseen spheres | 0.868 | 0.718–0.834 | 0.644–0.805 |
| unseen voids | 0.434 | 0.276–0.311 | 0.200–0.309 |
| unseen gyroid | 0.944 | −35…−16 | 0.853–0.920 |

Honest reading:
- **No learned model beats Kozeny–Carman on a genuinely new structure type.** That is the
  answer to the headline question, and it settles the overclaim for good.
- The CNN sees voxel geometry, so it survives the unseen-gyroid case (0.85–0.92 vs KC 0.944;
  MLP collapses to −16…−35 because its family one-hot is all-zero for an unseen family).
  On unseen spheres/voids, KC still wins.
- Porosity-band extrapolation (known families, new porosity): KC is best (0.944); the CNN is
  notably worse (0.75–0.85). The earlier "0.988" was seed noise (real MLP band: 0.954–0.962).
- Unseen voids is the hardest case for everyone (KC 0.434, all models ~0.2–0.3): these sit
  near the percolation threshold where 128³ passages may be a few voxels wide and the
  training targets themselves are least reliable.

The dataset itself (800 unique structures, 798 ok, no duplicates) is sound and reproducible;
the limitation is in what the learned model claims to do.

## Forchheimer (inertia onset)

| family | K_darcy (lu²) | K_fit (lu²) | F = β√K | Re max |
|---|---|---|---|---|
| spheres | 7.395 | 7.608 | 0.268 | 12.6 |
| voids | 2.300 | 2.400 | 0.965 | 5.3 |
| gyroid | 14.032 | 15.128 | 0.342 | 29.4 |

Deterministic, matches run #1 to ≤0.1%.

## Files

- `runs/weekend-20261030-sharded800/dataset.jsonl` — 800 rows (main artifact)
- `runs/weekend-20261030-sharded800/volumes/*.npy` — 798 CNN inputs
- `runs/weekend-20261030-sharded800/report.md` — 1-page report
- `runs/weekend-20261030-sharded800/parity_{random,porosity_band_held_out}.png`
- `runs/weekend-20261030-sharded800/stage_{dataset,train,forchheimer,cnn,report}.json`

Reproduction: `weekend_5090.py --stages dataset --samples N --sample-offset X` per shard,
then `merge_shards.py runs/merged runs/shard-*`, then
`weekend_5090.py --out runs/merged --stages train,cnn,report`.

## Notes / caveats

- Downstream ran on a partly-shared 5090; train/forchheimer were fast (<1 min), cnn ~seconds
  with 150 epochs. Nothing memory-limited.
- `report.md` shows `? / None` for GPU/torch because preflight/selfcheck weren't run on the
  merged folder (stages skipped) — dataset values are unaffected.
- 1 not_percolating + 1 not_converged samples are expected edge cases (drop them with
  `_ok_rows` filter, already used by train/cnn).
