"""Re-run stored voids geometries at higher resolutions; append one durable row per run.

Use disjoint --indices and output files for parallel cards. Reusing an output file
resumes completed (index, n) pairs; failed runs are recorded and retried on resume.
K_relative_to_128 is K(n) / K(128); null means the baseline is zero or unavailable.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physis.core.backend import get_backend  # noqa: E402
from physis.data import rve  # noqa: E402
from physis.solvers.lbm import triton_kernel  # noqa: E402
from physis.solvers.lbm.periodic import bytes_needed  # noqa: E402

INDICES = [583, 325, 682, 148, 220, 436, 667, 790]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", type=Path,
                    default=ROOT / "runs/weekend-20261030-sharded800/dataset.jsonl")
    ap.add_argument("--out", type=Path, default=ROOT / "runs/percolation-resolution/results.jsonl")
    ap.add_argument("--indices", type=int, nargs="+", default=INDICES)
    ap.add_argument("--include-384", action="store_true")
    args = ap.parse_args()
    if len(set(args.indices)) != len(args.indices) or not set(args.indices) <= set(INDICES):
        ap.error("indices must be distinct members of the eight requested voids samples")
    source = {r["index"]: r for line in args.dataset.read_text().splitlines()
              if line.strip() for r in [json.loads(line)]}
    for index in args.indices:
        if index not in source or source[index]["family"] != "voids":
            ap.error(f"sample {index} is missing or is not voids")
    previous = [json.loads(line) for line in args.out.read_text().splitlines() if line.strip()] \
        if args.out.exists() else []
    for row in previous:
        if row["index"] not in source or row["geometry"] != source[row["index"]]["geometry"]:
            ap.error("output contains a different stored geometry")
    completed = {(r["index"], r["n"]): r for r in previous
                 if r["status"] not in ("error", "skipped_memory")}
    backend = get_backend("fast", device="cuda")
    ok, detail = triton_kernel.selfcheck(str(backend.device))
    if not ok:
        raise RuntimeError(f"Triton selfcheck failed: {detail}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    failures = 0
    with args.out.open("a") as fh:
        for n in [128, 192, 256] + ([384] if args.include_384 else []):
            for index in args.indices:
                if (index, n) in completed:
                    continue
                if n != 128 and (index, 128) not in completed:
                    print(f"sample {index}, {n}³: deferred until the 128³ baseline succeeds", flush=True)
                    continue
                geometry = source[index]["geometry"]
                max_steps = 400_000 if n == 128 else 800_000
                row = {"index": index, "n": n, "geometry": geometry,
                       "max_steps": max_steps, "porosity": None, "K": None,
                       "steps": None, "K_relative_to_128": None}
                gc.collect()
                torch.cuda.empty_cache()
                free, _ = torch.cuda.mem_get_info(backend.device)
                start = time.monotonic()
                if bytes_needed((n, n, n), "triton") > 0.85 * free:
                    row.update(status="skipped_memory", free_memory_bytes=free)
                    failures += 1
                else:
                    try:
                        result = rve.run_rve(geometry, n, backend, impl="triton", max_steps=max_steps)
                        row.update(porosity=result["porosity"], K=result.get("permeability"),
                                   steps=result.get("steps"), status=result["status"],
                                   converged=result.get("converged"), impl=result.get("impl"))
                    except Exception as exc:
                        row.update(status="error", error=f"{type(exc).__name__}: {exc}")
                        failures += 1
                row["wall_time_s"] = time.monotonic() - start
                baseline = row if n == 128 else completed.get((index, 128))
                if baseline and baseline["K"] and row["K"] is not None:
                    row["K_relative_to_128"] = row["K"] / baseline["K"]
                fh.write(json.dumps(row, allow_nan=False) + "\n")
                fh.flush()
                os.fsync(fh.fileno())
                print(json.dumps(row), flush=True)
                if row["status"] not in ("error", "skipped_memory"):
                    completed[index, n] = row
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
