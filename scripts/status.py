"""Compact progress overview: running solver jobs, run-store counts, benchmark results per system."""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
runs = REPO / "results" / "runs"
st = {}
for d in runs.iterdir():
    f = d / "run.json"
    if f.exists():
        s = json.loads(f.read_text())["status"]
        st[s] = st.get(s, 0) + 1
print("runs:", st)
for pid in os.listdir("/proc"):
    if pid.isdigit():
        try:
            if open(f"/proc/{pid}/comm").read().strip().endswith("Foam"):
                cwd = os.readlink(f"/proc/{pid}/cwd")
                log = sorted(Path(cwd).glob("log.*Foam*"))[-1]
                with open(log, "rb") as fh:
                    fh.seek(max(0, log.stat().st_size - 4000))
                    tail = fh.read().decode(errors="replace")
                t = [ln for ln in tail.splitlines() if ln.startswith("Time = ")]
                cfg = json.loads((Path(cwd) / "case_config.json").read_text())
                tc = cfg["physical"]["diameter"] / cfg["physical"]["inlet_velocity"]
                now = float(t[-1].split("=")[1].strip().rstrip("s")) / tc if t else 0
                print(f"  running {Path(cwd).parent.name:45s} t*={now:6.1f}/{cfg['time']['end_time']}")
        except (OSError, IndexError, ValueError, KeyError):
            pass
bench = REPO / "results" / "benchmark"
for s in ["A", "B", "L-judge", "C-rule", "C-llm", "Bexh"]:
    d = bench / s
    if d.exists():
        res = {f.stem: json.loads(f.read_text()) for f in d.glob("*.json") if not f.stem.endswith(".partial")}
        print(f"{s:8s}", " ".join(f"{k.split('_')[0]}:{(v.get('final_verdict') or v.get('verdict'))[:3]}" for k, v in sorted(res.items())))
