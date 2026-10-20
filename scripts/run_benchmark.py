"""Run the benchmark systems on every manifest case (resumable).

    python scripts/run_benchmark.py --systems A,B,C-rule,C-llm,Bexh,L-judge [--cases id1,id2] [--workers 6]
    (C-llm-r2, C-llm-r3, ...: independent repeats of C-llm for run-to-run variance)

Results: results/benchmark/<system>/<case>.json; per-case reports for the
adaptive systems in reports/cases/.
"""

import argparse
import json
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.catalog import load_case_definition  # noqa: E402
from socrates.case_generation.spec import CaseConfig, ProblemSpec  # noqa: E402
from socrates.orchestration.evaluation import is_infrastructure_error, make_stamp, staleness  # noqa: E402
from socrates.orchestration.loop import Budget  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.systems import (  # noqa: E402
    decision_code_fingerprint,
    llm_judge,
    system_a,
    system_b,
    system_b_exhaustive,
    system_c,
)
from socrates.reporting.report import write_case_report  # noqa: E402

OUT = REPO / "results" / "benchmark"


def root_for(store: RunStore, spec: ProblemSpec, case: dict):
    path = REPO / case["definition"]
    if case["id"] == "baseline":
        cfg = CaseConfig.from_yaml(path)
    else:
        cfg, _ = load_case_definition(path)
    return store.get_or_run(cfg, spec, reason=f"benchmark root case {case['id']}", launched_by="benchmark")


FINGERPRINT = decision_code_fingerprint()


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=30, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


BENCH_COMMIT = _git("rev-parse", "HEAD")
_porcelain = _git("status", "--porcelain", "--", "src", "configs")
BENCH_SRC_DIRTY = None if _porcelain is None else bool(_porcelain)  # None: git unavailable, state unknown


def stamp(store: RunStore, res: dict, root) -> dict:
    return make_stamp(store, res, FINGERPRINT, root_config_hash=root.provenance.get("config_hash"),
                      benchmark_git_commit=BENCH_COMMIT, benchmark_src_dirty=BENCH_SRC_DIRTY,
                      root_git_commit=(root.provenance.get("software") or {}).get("socrates_git_commit"))


def run_one(system: str, case: dict, store: RunStore, spec: ProblemSpec, budget: Budget) -> dict:
    f = OUT / system / f"{case['id']}.json"
    root = root_for(store, spec, case)
    if f.exists():
        old = json.loads(f.read_text())
        why = staleness(old, f, store, FINGERPRINT, root.run_id)
        if not is_infrastructure_error(old) and why is None:
            return old
        # stale (other decision code, other root, or evidence changed since) or a recorded error: recompute
        print(f"{system:8s} {case['id']:24s} recomputing: {why or 'infrastructure error'}", flush=True)
    if system == "A":
        res = system_a(root.evidence or {})
    elif system == "B":
        res = system_b(store, spec, root.run_id)
    elif system == "C-rule":
        res = system_c(store, spec, root.run_id, planner="rule", budget=budget)
    elif system == "C-llm" or system.startswith("C-llm-r"):  # C-llm-r2, -r3: independent repeats (LLM variance)
        res = system_c(store, spec, root.run_id, planner="llm", budget=budget,
                       log_path=OUT / system / f"{case['id']}.partial.json")
    elif system == "Bexh":
        res = system_b_exhaustive(store, spec, root.run_id)
    elif system == "L-judge":
        res = llm_judge(store, spec, root.run_id)
    else:
        raise ValueError(system)
    res["case"] = case["id"]
    res["root_run"] = root.run_id
    res["stamp"] = stamp(store, res, root)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(res, indent=1, default=str))
    if system in ("C-rule", "C-llm", "Bexh") or system.startswith("C-llm-r"):
        rep = REPO / "reports" / "cases" / f"{case['id']}__{system}.md"
        try:
            view = res
            if system == "Bexh":  # Bexh experiments name their parent `parent`; the report expects `parent_run`
                view = {"verdict": res.get("verifier"), "root_run": root.run_id, "runs": res.get("runs"),
                        "final_verdict": res.get("verdict"),
                        "experiments": [{**e, "parent_run": e["parent"]} for e in res.get("experiments") or []
                                        if e.get("run_id")]}
            write_case_report(rep, store, spec, view, title=f"{case['id']} ({system})")
        except Exception:  # noqa: BLE001 -- a report failure must not discard the stored result
            rep.with_suffix(".report_error.txt").write_text(traceback.format_exc())
            print(f"report for {case['id']} {system} failed; see {rep.with_suffix('.report_error.txt')}", flush=True)
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", default="A,B")
    ap.add_argument("--cases", default="all")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = ProblemSpec.from_yaml(REPO / man["problem_spec"])
    cases = man["cases"] if a.cases == "all" else [c for c in man["cases"] if c["id"] in a.cases.split(",")]
    store = RunStore(REPO / "results" / "runs")
    budget = Budget()
    jobs = [(s, c) for s in a.systems.split(",") for c in cases]

    def go(job):
        s, c = job
        try:
            r = run_one(s, c, store, spec, budget)
            v = r.get("final_verdict") or r.get("verdict")
            print(f"{s:8s} {c['id']:24s} -> {v}", flush=True)
        except Exception:  # noqa: BLE001 -- persisted as ERROR (retried on resume), the batch continues
            tb = traceback.format_exc()
            f = OUT / s / f"{c['id']}.json"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps({"case": c["id"], "verdict": "ERROR", "error": tb,
                                     "stamp": {"decision_code": FINGERPRINT}}, indent=1))
            print(f"{s:8s} {c['id']:24s} -> ERROR\n{tb}", flush=True)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(go, jobs))


if __name__ == "__main__":
    main()
