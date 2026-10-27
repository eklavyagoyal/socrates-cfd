# Hardware benchmark results

Same D3Q19 stream+collide kernel (152 B per cell update, float32) on every machine;
`bench_lbm_gpu.py` (Apple/Metal) and `bench_lbm_cuda.py` (NVIDIA/Triton). Every run passed
the built-in correctness check (max rel. error 6.1e-8, mass drift 2.2e-8).

| Machine | Spec bandwidth | Copy (measured) | Copy / spec | D3Q19 kernel | Kernel / copy | Plain PyTorch | Source |
|---|---|---|---|---|---|---|---|
| Mac mini, Apple M4 (10 GPU cores, 32 GB), torch 2.14.1 | 120 GB/s | 94 GB/s | 78 % | 592–612 MLUPS | 96–99 % | 88 MLUPS | `bench_Apple_M4_32GB_20261027-171132.json` |
| MacBook Pro, Apple M4 Pro (20 GPU cores, 48 GB), macOS 27.0.1, torch 2.14.1 | 273 GB/s | 210 GB/s | 77 % | 1,335–1,457 MLUPS | ~97 % (large grids) | 210 MLUPS | screenshot reported 2026-10-27 |
| NVIDIA RTX 5090 (170 SMs, 32 GB), driver 590.48.01, torch 2.11.0+cu128, Triton 3.6.0, block 512 | 1,792 GB/s | 1,526 GB/s | 85 % | 9,847–9,983 MLUPS (128³–512³) | 98–99 % | 1,753 MLUPS | terminal output reported 2026-10-27 |

Pre-registered expectations (stated before the runs): M4 Pro ≈ 1,400 MLUPS — met;
RTX 5090 copy 1,500–1,650 GB/s and ≥ 8,500 MLUPS — met.

## Model

Apple chips deliver ~77–78 % of spec bandwidth as copy bandwidth (two chips measured); the
fused kernel runs at 96–99 % of copy on all three machines. Hence for this kernel class:

    MLUPS ≈ copy bandwidth / 152 B ≈ 0.77 × spec bandwidth / 152 B   (Apple, single die)

Projection for Mac Studio M5 Ultra (1,228 GB/s spec): ≈ 945 GB/s copy, ≈ 6,000 MLUPS —
valid only if the multi-die Ultra scales like a single die (not yet measured; an M2/M3 Ultra
run would test that).

Custom kernels vs plain PyTorch: 5.7× (RTX 5090) to 7× (M4) on the same math.

## External cross-check: published FluidX3D table (D3Q19 SRT, FP32, 153 B/cell)

Numbers read from https://github.com/ProjectPhysX/FluidX3D (benchmark table only; no code used).

| Device | Bandwidth | MLUPS |
|---|---|---|
| RTX 5090 | 1,792 GB/s | 9,522 (ours: 9,983) |
| RTX 4090 | 1,008 GB/s | 5,624 |
| RTX 4070 | 504 GB/s | 2,646 |
| M1 Max 24CU / M1 Ultra 64CU | 400 / 800 GB/s | 2,369 / 4,519 (Ultra = 1.91× Max) |
| M2 Max 38CU / M2 Ultra 76CU | 400 / 800 GB/s | 2,405 / 4,629 (Ultra = 1.92× Max) |
| M3 Ultra 60CU | 819 GB/s | 4,438 |
| M5 10CU | 153 GB/s | 800 |

Findings: Apple Ultra chips scale ~1.9× over Max for lattice Boltzmann (the multi-die
question is answered for M1/M2); GPU core count barely matters at equal bandwidth
(M2 Ultra 76CU vs M1 Ultra 64CU: +2.4 %). Projection M5 Ultra (1,228 GB/s, 80–89 % of spec
as in the table, or 77 % as on our M4/M4 Pro): ≈ 6,200–7,100 MLUPS.
