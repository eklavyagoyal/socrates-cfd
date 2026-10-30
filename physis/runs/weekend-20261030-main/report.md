# physis weekend run — 2026-10-30 02:04

## Machine and solver path

- GPU: NVIDIA GeForce RTX 5090 (31.3 GB), torch 2.11.0+cu128, CUDA 12.8, Triton 3.6.0
- **Triton self-check: PASS** max abs diff 1.517e-10 (reference scale 3.603e-04)
- Path used: **triton**, 677 MLUPS

## Validation gates

- `pytest -q -m validation tests/test_validation_lbm.py -p no:cacheprovider` → return code 0
  - lbm.poiseuille3d: **PASS**
  - lbm.sc_sphere_array: **PASS**

## Resolution study (one structure, box length 1)

| n | K | rel. to finest | steps | s |
|---|---|---|---|---|
| 64³ | 7.5230e-04 | +0.59% | 500 | 0 |
| 96³ | 7.4396e-04 | -0.53% | 1008 | 0 |
| 128³ | 7.4327e-04 | -0.62% | 1990 | 1 |
| 192³ | 7.4575e-04 | -0.29% | 4032 | 3 |
| 256³ | 7.4791e-04 | +0.00% | 7164 | 14 |
| 384³ | skipped_memory | | | |
| 512³ | skipped_memory | | | |

## Dataset

- 600 samples at 128³, status: {'ok': 600}

## Learned closure vs Kozeny–Carman (log10 K)

| split | model | R² | MAE | max error | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.837 | 0.163 | 2.016 | 120 |
| random | mlp_ensemble | 0.984 | 0.039 | 0.694 | 120 |
| random | uncertainty↔error (Spearman) | 0.62 | | | |
| porosity_band_held_out | kozeny_carman | 0.936 | 0.100 | 0.218 | 109 |
| porosity_band_held_out | mlp_ensemble | 0.931 | 0.083 | 0.566 | 109 |
| porosity_band_held_out | uncertainty↔error (Spearman) | 0.21 | | | |

Plots: `parity_random.png`, `parity_porosity_band_held_out.png`

## Forchheimer (inertia onset)

- spheres: K Darcy 7.395 lu², K fit 7.608 lu², F = β√K = 0.268, Re up to 12.6
- voids: K Darcy 2.300 lu², K fit 2.400 lu², F = β√K = 0.965, Re up to 5.3
- gyroid: K Darcy 14.032 lu², K fit 15.128 lu², F = β√K = 0.342, Re up to 29.4

## 3D CNN on the voxel structure

- R² 0.979, MAE 0.044 (log10 K), test n = 120
