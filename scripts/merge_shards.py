"""Merge the dataset stages of parallel shards into one run folder for training.

    python scripts/merge_shards.py runs/merged runs/shard-00 runs/shard-01 ...
    python scripts/weekend_5090.py --out runs/merged --stages train,cnn,report

Rows are keyed by their global sample index (``--sample-offset`` keeps shards disjoint); a
duplicate index is an error, because it means two shards computed the same seeds.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    out, shards = Path(sys.argv[1]), [Path(p) for p in sys.argv[2:]]
    (out / "volumes").mkdir(parents=True, exist_ok=True)
    rows: dict[int, dict] = {}
    for shard in shards:
        path = shard / "dataset.jsonl"
        if not path.exists():
            print(f"skip {shard}: no dataset.jsonl")
            continue
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            i = row["index"]
            if i in rows:
                raise SystemExit(f"sample {i} appears in two shards ({shard}): offsets overlap")
            rows[i] = row
            vol = shard / "volumes" / f"{i:05d}.npy"
            if vol.exists():
                shutil.copy2(vol, out / "volumes" / vol.name)
    with (out / "dataset.jsonl").open("w") as fh:
        for i in sorted(rows):
            fh.write(json.dumps(rows[i]) + "\n")
    counts: dict[str, int] = {}
    for r in rows.values():
        counts[r.get("status", "?")] = counts.get(r.get("status", "?"), 0) + 1
    (out / "stage_dataset.json").write_text(json.dumps(
        {"n": next(iter(rows.values()))["n"] if rows else None, "samples": len(rows), "status_counts": counts,
         "file": "dataset.jsonl", "merged_from": [str(s) for s in shards]}, indent=1) + "\n")
    print(f"merged {len(rows)} samples from {len(shards)} shards into {out}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
