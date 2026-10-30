# physis weekend run — 2026-10-30 13:23

## Machine and solver path

- GPU: NVIDIA GeForce RTX 5090 (31.3 GB), torch 2.11.0+cu128, CUDA 12.8, Triton 3.6.0
- **Triton self-check: PASS** max abs diff 1.517e-10 (reference scale 3.603e-04)
- Path used: **triton**, 9279 MLUPS

## Validation gates

- `None` → return code None

## Resolution study (one structure, box length 1)

| n | K | rel. to finest | steps | s |
|---|---|---|---|---|
| 64³ | 7.5230e-04 | +0.19% | 500 | 0 |
| 96³ | 7.4396e-04 | -0.92% | 1008 | 0 |
| 128³ | 7.4327e-04 | -1.01% | 1791 | 1 |
| 192³ | 7.4575e-04 | -0.68% | 4032 | 3 |
| 256³ | 7.4791e-04 | -0.40% | 7164 | 14 |
| 384³ | 7.5088e-04 | +0.00% | 16128 | 99 |
| 512³ | skipped_memory | | | |

## Dataset

- 100 samples at 128³, status: {'ok': 100}

## Learned closure vs Kozeny–Carman (log10 K)

| split | model | R² | MAE | max error | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.894 | 0.162 | 0.690 | 20 |
| random | mlp_ensemble | 0.994 | 0.038 | 0.145 | 20 |
| random | uncertainty↔error (Spearman) | 0.35 | | | |
| porosity_band_held_out | kozeny_carman | 0.948 | 0.088 | 0.185 | 23 |
| porosity_band_held_out | mlp_ensemble | 0.963 | 0.058 | 0.273 | 23 |
| porosity_band_held_out | uncertainty↔error (Spearman) | 0.55 | | | |

Plots: `parity_random.png`, `parity_porosity_band_held_out.png`

## Forchheimer (inertia onset)

- spheres: K Darcy 7.395 lu², K fit 7.608 lu², F = β√K = 0.268, Re up to 12.6
- voids: K Darcy 2.300 lu², K fit 2.400 lu², F = β√K = 0.965, Re up to 5.3
- gyroid: K Darcy 14.032 lu², K fit 15.128 lu², F = β√K = 0.342, Re up to 29.4

## 3D CNN on the voxel structure

- R² 0.989, MAE 0.053 (log10 K), test n = 20
