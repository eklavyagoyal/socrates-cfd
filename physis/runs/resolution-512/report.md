# physis weekend run — 2026-10-30 20:20

## Machine and solver path

- GPU: NVIDIA GeForce RTX 5090 (31.3 GB), torch 2.11.0+cu128, CUDA 12.8, Triton 3.6.0
- **Triton self-check: PASS** max abs diff 1.517e-10 (reference scale 3.603e-04)
- Path used: **triton**, 9302 MLUPS

## Validation gates

- not run in this folder (stage skipped); see `validation/results/` for the last recorded gates

## Resolution study (one structure, box length 1)

| n | K | rel. to finest | steps | s |
|---|---|---|---|---|
| 64³ | 7.5230e-04 | -0.06% | 500 | 0 |
| 96³ | 7.4396e-04 | -1.17% | 1008 | 0 |
| 128³ | 7.4327e-04 | -1.26% | 1791 | 1 |
| 192³ | 7.4575e-04 | -0.93% | 4032 | 3 |
| 256³ | 7.4791e-04 | -0.64% | 7164 | 14 |
| 384³ | 7.5088e-04 | -0.25% | 16128 | 99 |
| 512³ | 7.5276e-04 | +0.00% | 28683 | 406 |

## Dataset

- None samples at None³, status: None
