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
- **Triton self-check.** The NVIDIA kernel was written on a Mac without an NVIDIA GPU. Its logic
  was checked there through a CPU emulation of Triton, but it has never been compiled or run on
  a real GPU. The `selfcheck` stage compares it with the float64 reference on the 5090 before
  anything else; only on PASS is it used. On FAIL the run continues on the torch path, slower
  and capped at 192³ for the resolution study, and the report says so at the top.
- Every stage writes `stage_<name>.json` and is skipped on the next start, so after a crash just
  start the same command again. `--force` reruns finished stages, `--stages a,b` picks stages.

## Stages and rough time on the 5090 (estimates, not measured)
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
