# Weekend run on the RTX 5090

What it does: computes pore-scale permeability for hundreds of random porous structures with
the physis LBM solver, checks how fine the voxels must be, and trains the first learned
closure (structure → permeability) against the Kozeny–Carman baseline (ADR-0008, ADR-0009).

## Before you start
- Linux or WSL2 with an NVIDIA driver (the hardware benchmark ran with driver 590, torch 2.11
  + cu128, Triton 3.6). Native Windows has no Triton: everything still runs, but on the slower
  torch path.
- Python 3.11+, about 5 GB free disk.

## Setup
```bash
git clone https://github.com/eklavyagoyal/socrates-cfd.git
cd socrates-cfd && git checkout physis/weekend-5090 && cd physis
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cu128
.venv/bin/pip install -e '.[dev]'
```

## Run
```bash
.venv/bin/python scripts/weekend_5090.py --quick   # smoke test of every stage, a few minutes
.venv/bin/python scripts/weekend_5090.py           # the real run
```
Results land in `runs/weekend-<date>/`. Send that whole folder back; `report.md` in it is the
summary.

## Read this first in the output
- **Triton self-check.** The NVIDIA kernel passed its self-check against the float64 reference on
  an RTX 5090 (max abs diff 1.5e-10, 2026-10-29). The `selfcheck` stage still runs first on every
  machine; only on PASS is the kernel used. On FAIL the run continues on the torch path, slower
  and capped at 192³ for the resolution study, and the report says so at the top.
- Every stage writes `stage_<name>.json` and is skipped on the next start, so after a crash just
  start the same command again. `--force` reruns finished stages, `--stages a,b` picks stages.

## Several GPUs in parallel
Every sample is independent, so a large dataset splits across cards. Give each card its own
`--sample-offset` (disjoint seeds) and output folder, then merge and train once:
```bash
# on card k (k = 0..19), 1000 samples each
.venv/bin/python scripts/weekend_5090.py --stages preflight,selfcheck,dataset --samples 1000 \
    --sample-offset $((k * 1000)) --out runs/shard-$(printf %02d $k)
# afterwards, on one machine with all shard folders
.venv/bin/python scripts/merge_shards.py runs/merged runs/shard-*
.venv/bin/python scripts/weekend_5090.py --out runs/merged --stages train,cnn,report
```
`scripts/run_weekend_nohup.sh` starts a run detached from the SSH session.

## Measured on the RTX 5090 (run of 2026-10-29/30)
Triton path 9,377 MLUPS median at 128³; the validation gates took 28 min on that machine's CPU.
The first run spent 3.2 h on the dataset because of a convergence-check bug (fixed since, see
`docs/weekend-5090-results.md` on the branch); with the fix 600 samples at 128³ should take about
10–15 min.

## Stages and rough time on the 5090 (first estimates)
| stage | what | time |
|---|---|---|
| preflight, selfcheck | machine info, kernel check, throughput | 1 min |
| gates | float64 validation gates (runs on the CPU) | 10–20 min |
| resolution | one structure at 64³ … 512³ (512³ needs ~24 GB) | ~30 min |
| dataset | 600 structures at 128³ (`--samples`, `--size`) | ~30 min |
| train | Kozeny–Carman vs MLP ensemble, random split + held-out porosity band | 1–2 min |
| forchheimer | inertia onset on three structures | ~5 min |
| cnn | 3D CNN on the voxel structure (optional) | ~5 min |

Overnight variant with more data: `--samples 3000` (about 2–3 h more).
