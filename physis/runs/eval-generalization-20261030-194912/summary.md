# Generalization evaluation — 20261030-194912

Dataset: `runs/merged-800` — 798 ok samples (families {'spheres': 267, 'voids': 265, 'gyroid': 266}), 3 seed(s) per trainable model, CNN 150 epochs, MLP 3000 epochs, device cuda.

Target = log10(K). R² reported as min–max over seeds (higher is better); KC is deterministic.

| split | KC R² | MLP R² (seeds) | CNN R² (seeds) |
|---|---|---|---|
| random | 0.880 | 0.973–0.974 | 0.983–0.988 |
| porosity_band_held_out | 0.944 | 0.954–0.962 | 0.750–0.849 |
| unseen_spheres | 0.868 | 0.718–0.834 | 0.644–0.805 |
| unseen_voids | 0.434 | 0.276–0.311 | 0.200–0.309 |
| unseen_gyroid | 0.944 | -35.106–-15.826 | 0.853–0.920 |

## Reading

- If the CNN beats KC on `unseen_*` splits, geometry (voxels) carries the generalization signal that the family one-hot MLP lacks.
- If the CNN also collapses on unseen families, the porosity band itself is not the only missing axis: the dataset lacks the *geometric diversity* needed.
- Report spread, not a single seed. A model that needs a lucky seed is not a model that generalizes.
