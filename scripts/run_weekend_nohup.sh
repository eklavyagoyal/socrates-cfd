#!/usr/bin/env bash
# Run the physis weekend-5090 job detached from any SSH session, so it survives
# connection drops and finishes overnight. Usage:
#   nohup bash scripts/run_weekend_nohup.sh <out_dir> > <logfile> 2>&1 &
# Output: results in <out_dir>, plain-text log appended to the redirect target.

set -u

cd "$(dirname "$0")/.."               # physis/
OUT_DIR="${1:-runs/weekend-$(date +%Y%m%d)}"
mkdir -p "$OUT_DIR"

echo "[$(date '+%F %T')] starting physis weekend run -> $OUT_DIR"
echo "[$(date '+%F %T')] python: $(command -v python3 || echo none)"
echo "[$(date '+%F %T')] nvidia: $(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null | head -1)"

# `python -u` so every line flushes to the nohup log immediately; unbuffered output
# survives a crash and lets us tail progress live.
python3 -u scripts/weekend_5090.py --out "$OUT_DIR"
rc=$?

echo "[$(date '+%F %T')] weekend run finished, exit code $rc"
exit $rc
