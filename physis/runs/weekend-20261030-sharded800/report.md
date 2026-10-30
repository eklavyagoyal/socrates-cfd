# physis weekend run — 2026-10-30 19:02

## Machine and solver path

- GPU: ? (? GB), torch None, CUDA None, Triton None
- **Triton self-check: n/a** 
- Path used: **None**, 0 MLUPS

## Validation gates

- not run in this folder (stage skipped); see `validation/results/` for the last recorded gates

## Dataset

- 800 samples at 128³, status: {'ok': 798, 'not_converged': 1, 'not_percolating': 1}

## Learned closure vs Kozeny–Carman (log10 K)

| split | model | R² | MAE | max error | n test |
|---|---|---|---|---|---|
| random | kozeny_carman | 0.880 | 0.153 | 1.926 | 159 |
| random | mlp_ensemble | 0.976 | 0.041 | 1.205 | 159 |
| random | uncertainty↔error (Spearman) | 0.59 | | | |
| porosity_band_held_out | kozeny_carman | 0.944 | 0.090 | 0.209 | 165 |
| porosity_band_held_out | mlp_ensemble | 0.988 | 0.036 | 0.190 | 165 |
| porosity_band_held_out | uncertainty↔error (Spearman) | 0.24 | | | |

Plots: `parity_random.png`, `parity_porosity_band_held_out.png`

## Forchheimer (inertia onset)

- spheres: K Darcy 7.395 lu², K fit 7.608 lu², F = β√K = 0.268, Re up to 12.6
- voids: K Darcy 2.300 lu², K fit 2.400 lu², F = β√K = 0.965, Re up to 5.3
- gyroid: K Darcy 14.032 lu², K fit 15.128 lu², F = β√K = 0.342, Re up to 29.4

## 3D CNN on the voxel structure

- R² 0.983, MAE 0.038 (log10 K), test n = 159
