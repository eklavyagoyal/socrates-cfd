"""Run benchmark root cases (baseline/adversarial definitions) through the run store in parallel.

    python scripts/run_root_cases.py cases/adversarial/A1_coarse_mesh.yaml ... [--slots 3]
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.catalog import load_case_definition  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="+")
    ap.add_argument("--slots", type=int, default=3)
    ap.add_argument("--store", default=str(REPO / "results" / "runs"))
    a = ap.parse_args()
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(a.store, cpu_slots=a.slots)

    def one(path: str):
        cfg, meta = load_case_definition(path)
        r = store.get_or_run(cfg, spec, reason=f"benchmark root case: {meta.get('title')}", launched_by="benchmark")
        q = (r.evidence or {}).get("qoi", {})
        return {"case": meta["id"], "run_id": r.run_id, "status": r.status,
                "reported": q.get("reported"), "stationary": q.get("stationary")}

    with ThreadPoolExecutor(max_workers=len(a.cases)) as ex:
        for res in ex.map(one, a.cases):
            print(json.dumps(res, default=str), flush=True)


if __name__ == "__main__":
    main()
