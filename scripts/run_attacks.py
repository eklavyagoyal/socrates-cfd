"""Attack phase: try to make the verifier accept wrong answers, then test principled fixes.

    python scripts/run_attacks.py [--workers 6]

Systems (results/attacks/<system>/<case>.json):
  B-v1, C-rule-v1, C-llm-v1     pre-registered verifier (configs/verification.yaml)
  C-llm-v1+review               same, plus the LLM acceptance review (veto-only)
  B-v2, C-rule-v2               verifier v2 (configs/verification_v2.yaml: geometry + inlet consistency)
Also: review-only and B-v2 applied to every benchmark case, to measure false vetoes / false rejections
introduced by the extensions (no new simulations).
"""

import argparse
import json
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.catalog import load_case_definition  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.base import load_config  # noqa: E402
from socrates.checks.verifier import RunGraph, RunNode, verify  # noqa: E402
from socrates.orchestration.loop import Budget, LLMPlanner, RuleBasedPlanner, run_adaptive  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.systems import review_only  # noqa: E402
from socrates.reporting.report import write_case_report  # noqa: E402

OUT = REPO / "results" / "attacks"
V1 = load_config(REPO / "configs" / "verification.yaml")
V2 = load_config(REPO / "configs" / "verification_v2.yaml")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--benchmark-extensions", action="store_true",
                    help="also apply review-only and verifier v2 to the finished benchmark cases")
    a = ap.parse_args()
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    attacks = sorted((REPO / "cases" / "attacks").glob("*.yaml"))

    def root(path):
        cfg, meta = load_case_definition(path)
        r = store.get_or_run(cfg, spec, reason=f"attack root case {meta['id']}", launched_by="attacks")
        return meta["id"], r

    def save(system, cid, res):
        f = OUT / system / f"{cid}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(res, indent=1, default=str))

    def job(args):
        system, path = args
        cid = path.stem
        if (OUT / system / f"{cid}.json").exists():
            return
        try:
            _, r = root(path)
            if system in ("B-v1", "B-v2"):
                g = RunGraph([RunNode(r.run_id, r.config, r.evidence or {}, ok=r.ok)], r.run_id)
                res = verify(g, spec, V1 if system == "B-v1" else V2).to_dict()
            else:
                planner = LLMPlanner() if "llm" in system else RuleBasedPlanner()
                res = run_adaptive(r.run_id, store, spec, planner, Budget(), vcfg=V2 if system.endswith("v2") else V1,
                                   acceptance_review=system.endswith("+review"),
                                   log_path=OUT / system / f"{cid}.partial.json").to_dict()
                write_case_report(REPO / "reports" / "cases" / f"{cid}__{system}.md", store, spec, res, f"{cid} ({system})")
            res["case"], res["root_run"] = cid, r.run_id
            save(system, cid, res)
            print(f"{system:16s} {cid:28s} -> {res.get('final_verdict') or res.get('verdict')}", flush=True)
        except Exception:  # noqa: BLE001
            print(f"{system:16s} {cid:28s} -> ERROR\n{traceback.format_exc()}", flush=True)

    systems = ["B-v1", "B-v2", "C-rule-v1", "C-llm-v1", "C-llm-v1+review", "C-rule-v2"]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(job, [(s, p) for s in systems for p in attacks]))

    if not a.benchmark_extensions:
        print("done (attacks only)", flush=True)
        return
    # extensions applied to the benchmark cases (no new simulations)
    bench = REPO / "results" / "benchmark"
    for f in sorted((bench / "C-llm").glob("*.json")):
        if f.stem.endswith(".partial"):
            continue
        res = json.loads(f.read_text())
        out = OUT / "review-on-benchmark" / f.name
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"case": f.stem, **review_only(store, spec, res, V1)}, indent=1, default=str))
        g_root = store.load(res["root_run"])
        g = RunGraph([RunNode(g_root.run_id, g_root.config, g_root.evidence or {}, ok=g_root.ok)], g_root.run_id)
        out2 = OUT / "B-v2-on-benchmark" / f.name
        out2.parent.mkdir(parents=True, exist_ok=True)
        out2.write_text(json.dumps({"case": f.stem, **verify(g, spec, V2).to_dict()}, indent=1, default=str))
    print("done", flush=True)


if __name__ == "__main__":
    main()
