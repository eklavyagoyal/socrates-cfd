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

**Headline:** with 200 more samples than run #1, the MLP now **beats Kozeny–Carman even
out-of-distribution** (0.988 vs 0.944 on the held-out porosity band). Run #1 tied/lost there
(0.931 vs 0.936 on 600 samples). The learned closure generalizes beyond the training
porosity range once given enough data.

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
