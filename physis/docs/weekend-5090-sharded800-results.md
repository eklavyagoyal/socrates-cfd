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
- permeability 9.6e-7 – 9.6e-3 (box-length², box length 1)
- solver: D3Q19 TRT, τ₊=1.5, periodic, force-driven, 128³, Triton path
- volumes: 798 × 32³ float16 solid-fraction fields (`volumes/*.npy`) — CNN inputs

## Original single-fit results (target = log₁₀ K)

Historical downstream fits; the independent five-seed evaluation below supersedes
their generalization claims.

| split | model | R² | MAE | max err | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.880 | 0.153 | 1.926 | 159 |
| random | mlp_ensemble | **0.976** | 0.041 | 1.205 | 159 |
| random | unc↔err Spearman | 0.59 | | | |
| porosity held-out | kozeny_carman | 0.944 | 0.090 | 0.209 | 165 |
| porosity held-out | mlp_ensemble | **0.988** | 0.036 | 0.190 | 165 |
| porosity held-out | unc↔err Spearman | 0.24 | | | |
| 3D CNN (voxels) | cnn | **0.983** | 0.038 | — | 159 |

## Corrected five-seed evaluation (2026-10-30)

Ran on nc-9-1-3 (RTX 5090), using the existing 798 eligible samples from the
800-row dataset, with identical fixed train/test rows for every model. MLP ensembles
use five members and 3,000 epochs; the CNN uses 150 epochs. Base seeds are
`0, 1000, 2000, 3000, 4000` for both models, with MLP member seeds `base + m`.
`mlp_noflag` uses only porosity and log10(surface) on every unseen-family split.
`low_porosity` trains on porosity >= 0.50 and tests below 0.45.

R², MAE and maximum absolute error below are min–max over five seeds; KC is
deterministic. Errors are in log10(K). Full per-seed values and the generated summary:
[`runs/eval-generalization-20261030-202010/`](../runs/eval-generalization-20261030-202010/summary.md).

| split | train / test | model | R² | MAE | max error |
|---|---|---|---|---|---|
| random | 639 / 159 | kozeny_carman | 0.880 | 0.153 | 1.926 |
| random | 639 / 159 | mlp_ensemble | 0.973–0.977 | 0.040–0.041 | 1.191–1.281 |
| random | 639 / 159 | cnn | 0.980–0.987 | 0.035–0.050 | 0.830–1.040 |
| porosity_band_held_out | 564 / 165 | kozeny_carman | 0.944 | 0.090 | 0.209 |
| porosity_band_held_out | 564 / 165 | mlp_ensemble | 0.912–0.984 | 0.040–0.103 | 0.232–0.311 |
| porosity_band_held_out | 564 / 165 | cnn | 0.716–0.848 | 0.117–0.172 | 0.569–0.820 |
| low_porosity | 490 / 221 | kozeny_carman | 0.618 | 0.238 | 2.070 |
| low_porosity | 490 / 221 | mlp_ensemble | 0.683–0.932 | 0.104–0.267 | 1.178–1.856 |
| low_porosity | 490 / 221 | cnn | 0.805–0.879 | 0.129–0.199 | 1.442–1.589 |
| unseen_spheres | 531 / 267 | kozeny_carman | 0.868 | 0.205 | 0.421 |
| unseen_spheres | 531 / 267 | mlp_ensemble | 0.599–0.939 | 0.118–0.295 | 0.461–1.333 |
| unseen_spheres | 531 / 267 | mlp_noflag | 0.069–0.158 | 0.411–0.441 | 1.394–2.391 |
| unseen_spheres | 531 / 267 | cnn | 0.636–0.801 | 0.222–0.296 | 0.796–1.032 |
| unseen_voids | 533 / 265 | kozeny_carman | 0.434 | 0.329 | 2.138 |
| unseen_voids | 533 / 265 | mlp_ensemble | 0.104–0.330 | 0.374–0.458 | 2.129–2.307 |
| unseen_voids | 533 / 265 | mlp_noflag | 0.366–0.382 | 0.362–0.367 | 2.105–2.153 |
| unseen_voids | 533 / 265 | cnn | 0.166–0.309 | 0.460–0.513 | 1.991–2.139 |
| unseen_gyroid | 532 / 266 | kozeny_carman | 0.944 | 0.123 | 0.173 |
| unseen_gyroid | 532 / 266 | mlp_ensemble | -35.237–-6.306 | 1.165–2.184 | 2.648–9.438 |
| unseen_gyroid | 532 / 266 | mlp_noflag | -360.687–-3.134 | 0.844–6.335 | 2.627–28.713 |
| unseen_gyroid | 532 / 266 | cnn | 0.688–0.933 | 0.115–0.263 | 0.373–0.837 |

What this measured:

- **No learned model reliably beats KC on an unseen family in these tests:** three
  families, 800 dataset rows (798 eligible), five independent base seeds per model.
  On unseen spheres, two MLP seeds exceed KC in R², while three fall below it;
  no learned model exceeds KC in R² for every tested seed on any unseen-family split.
- On the held-out high-porosity band, MLP R² spans **0.912–0.984**, versus KC 0.944.
  MLP R² falls above and below KC across seeds.
  KC's maximum error is lower than every MLP seed's on this split (0.209 versus
  0.232–0.311). The old **0.954–0.962 spread was understated by overlapping seeds**:
  base seeds 0, 1 and 2 shared three of their five ensemble members across all three runs.
- On this low-porosity split, both learned models exceed KC in R² in all five seeds.
  MLP MAE does not improve uniformly: its worst seed is 0.267, versus KC 0.238.
- The old unseen-family scaling was incorrect: a training-constant one-hot column
  received sd = 1e-9, so an unseen flag of 1 entered the net as **1e9**. Columns with
  std < 1e-6 now use sd = 1; a regression test covers constant and nearly constant inputs.
  Gyroid collapse also occurs without the family flag (R² −360.687 to −3.134), so the flag
  does not by itself explain it. The **likely cause is descriptor extrapolation**:
  gyroid includes samples outside the training range in porosity and surface. Training
  on spheres + voids covers porosity 0.309–0.849 and surface 3.628–21.017; 46 of 266
  gyroids fall below that porosity range and 144 below that surface range. This is a
  likely explanation, not an isolated causal test.

These results describe these fixed splits, families and seeds. They do not establish
behavior on additional structure families. Dataset uniqueness was checked at merge;
the resolution measurements below also show that several selected voids labels change
substantially when re-solved above 128³.

Reproduce the corrected evaluation with
`CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python scripts/eval_generalization.py --device cuda`.

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
- The 1 not_percolating + 1 not_converged rows retain their 128³ solver statuses.
  The training filter excludes them; the resolution follow-up includes both explicitly.

## Resolution measurement through 512³ (2026-10-30)

Ran `weekend_5090.py --out runs/resolution-512 --stages preflight,selfcheck,resolution,report`
on nc-9-2-3, CUDA card 0 (RTX 5090). `nvidia-smi` showed 31,676 MiB free before launch;
preflight reported 30.4 GiB free after CUDA initialization. Triton self-check passed
(max absolute difference 1.517e-10); every requested resolution returned `ok` and converged.
The run exited 0. Validation gates, dataset generation and model training were not requested
in this folder. Raw records: [`stage_resolution.json`](../runs/resolution-512/stage_resolution.json).

One stored spheres geometry, box length 1; K is in box-length-squared units.

| n | K | difference from K(512) | steps | wall s | status |
|---|---|---|---|---|---|
| 64³ | 7.5230049e-04 | -0.061% | 500 | 0.0 | ok |
| 96³ | 7.4395570e-04 | -1.170% | 1008 | 0.1 | ok |
| 128³ | 7.4327015e-04 | -1.261% | 1791 | 0.5 | ok |
| 192³ | 7.4575127e-04 | -0.931% | 4032 | 3.5 | ok |
| 256³ | 7.4790883e-04 | -0.645% | 7164 | 13.6 | ok |
| 384³ | 7.5087787e-04 | -0.250% | 16128 | 98.6 | ok |
| 512³ | 7.5276142e-04 | +0.000% | 28683 | 405.8 | ok |

For this geometry, K(128) is 1.26% below K(512), and K(384) is 0.25% below K(512).
The 64³ value happens to be close to K(512), while 96³ and 128³ are lower; the sequence
is not monotonic over all tested resolutions. This measures one geometry and does not
establish a resolution tolerance for the near-percolation voids samples.

## Selected voids resolution measurements (2026-10-30)

Used the eight rows’ stored `geometry` specs, without regenerating structures.
Triton, 400k steps at 128³ and 800k at 192³ / 256³. Every required pair has a
saved row, including non-converged and non-percolating outcomes.

| index | K(128) | K(192) | K(256) | K(192) / K(128) | K(256) / K(128) | status at 128 / 192 / 256 |
|---|---|---|---|---|---|---|
| 583 | 9.6218909e-07 | 3.5142911e-07 | 1.7199165e-07 | 0.3652 | 0.1788 | ok / ok / ok |
| 325 | 1.3048045e-06 | 5.6029432e-07 | 2.4713027e-07 | 0.4294 | 0.1894 | ok / ok / ok |
| 682 | 2.3925598e-06 | 1.9125104e-06 | 1.8262436e-06 | 0.7994 | 0.7633 | ok / ok / ok |
| 148 | 4.2095606e-06 | 3.2790047e-06 | 2.9104971e-06 | 0.7789 | 0.6914 | ok / ok / ok |
| 220 | 8.1837438e-06 | 6.3757068e-06 | 6.0491062e-06 | 0.7791 | 0.7392 | ok / ok / ok |
| 436 | 3.5141117e-06 | 2.3649687e-06 | 1.8499938e-06 | 0.6730 | 0.5264 | ok / ok / ok |
| 667 | 5.2228650e-08 | 1.1163886e-09 | 8.7217743e-10 | 0.0214 | 0.0167 | not_converged / not_converged / not_converged |
| 790 | -1.6877483e-10 | -3.7967840e-11 | -2.2012214e-10 | 0.2250 | 1.3042 | not_percolating / not_percolating / not_percolating |


Six samples converge at every resolution; their K(256) / K(128) ranges from
0.1788 to 0.7633. This selected set therefore has material resolution dependence.
Sample **790 remains solver-classified `not_percolating`** at all three resolutions.
Its tiny negative K values are numerical residuals; the signed ratios are audit
values, not physical permeability ratios. Sample **667 remains `not_converged`**
at all three limits, so its decreasing positive K does not establish a steady
permeability or a percolation classification.

Optional 384³: sample 220 converged at K = 5.3863135e-6, or 0.6582 of K(128).
The other seven samples were not completed at 384³; required coverage and the
step-limit cases took priority.

Full porosity, K, steps, status, wall time, ratio, host and raw checkpoint provenance:
[`percolation-resolution/summary.md`](../runs/percolation-resolution/summary.md) and
[`results.jsonl`](../runs/percolation-resolution/results.jsonl). Restart details and
replicas are recorded there. Several in-flight attempts were interrupted to relaunch
with `nohup setsid`; completed rows were retained. A redundant 790/256 run remains
active on nc-12-2-5 at collection time and was left running as requested. The table
uses the completed 5090 result for that pair.
