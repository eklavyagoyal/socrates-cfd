"""Replay the deterministic verifier on every stored result and compare with the stored verdict.

A stored adaptive result records the runs it used and the verifier's verdict on them. Re-running the *current*
verifier on the *current* evidence of those runs must reproduce that verdict exactly. This checks, without any new
simulation, that a result was not produced by older decision code (a long-running process keeps the modules it
loaded at start), and that no evidence file changed underneath it. Attack results carry no decision-code stamp,
so for them this replay is the only such check.

The LLM's choices are not replayed (they are not deterministic); only the verdict on the graph it produced is.

    python scripts/replay_verdicts.py        # writes results/analysis/replay.json; exit 1 on any mismatch
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.base import load_config  # noqa: E402
from socrates.checks.verifier import verify  # noqa: E402
from socrates.orchestration.evaluation import is_infrastructure_error  # noqa: E402
from socrates.orchestration.loop import graph_for  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402

V1 = load_config(REPO / "configs" / "verification.yaml")
V2 = load_config(REPO / "configs" / "verification_v2.yaml")
GROUPS = {"benchmark": ["B", "C-rule", "C-rule-prereg", "C-llm", "Bexh"], "attacks": ["B-v1", "B-v2", "C-rule-v1", "C-rule-v2",
                                                                     "C-llm-v1", "C-llm-v1+review"]}
REL_TOL = 1e-9


def stored(system: str, r: dict) -> tuple[dict, list[str]]:
    """The stored deterministic verdict dict and the runs it was computed on."""
    if system.startswith("B") and system != "Bexh":
        return r, [r["root_run"]]
    if system == "Bexh":
        return r["verifier"], list(r.get("runs") or [r["root_run"]])
    runs = list(r.get("runs") or [])
    return r["verdict"], ([r["root_run"]] + [x for x in runs if x != r["root_run"]])


def u_values(v: dict) -> dict:
    """Every number and status the verdict rests on: combined and per-component uncertainty, component status."""
    out = {}
    for q, d in (v.get("per_qoi") or {}).items():
        d = d or {}
        out[f"{q}.combined"] = d.get("combined_uncertainty")
        for comp, u in (d.get("component_uncertainty") or {}).items():
            out[f"{q}.{comp}"] = u
        for comp, st in (d.get("component_status") or {}).items():
            out[f"{q}.{comp}.status"] = st
    return out


def main() -> int:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    rows, bad = [], []
    for group, systems in GROUPS.items():
        base = REPO / "results" / group
        extra = sorted(p.name for p in base.glob("C-llm-r*") if p.is_dir()) if group == "benchmark" else []
        for system in systems + extra:
            for f in sorted((base / system).glob("*.json")) if (base / system).is_dir() else []:
                if f.name.endswith(".partial.json"):
                    continue
                r = json.loads(f.read_text())
                if is_infrastructure_error(r):
                    rows.append({"group": group, "system": system, "case": f.stem, "status": "skipped (error)"})
                    continue
                old, runs = stored(system, r)
                vcfg = V2 if system.endswith("v2") else V1
                try:
                    new = verify(graph_for(store, r["root_run"], runs), spec, vcfg).to_dict()
                except Exception as e:  # noqa: BLE001 -- a replay failure is itself a finding
                    rows.append({"group": group, "system": system, "case": f.stem, "status": f"replay error: {e!r}"})
                    bad.append(rows[-1])
                    continue
                diffs = []
                if new["verdict"] != old.get("verdict"):
                    diffs.append(f"verdict {old.get('verdict')} -> {new['verdict']}")
                if sorted(new.get("failed_checks") or []) != sorted(old.get("failed_checks") or []):
                    diffs.append(f"failed checks {old.get('failed_checks')} -> {new.get('failed_checks')}")
                uo, un = u_values(old), u_values(new)
                for q in sorted(set(uo) | set(un)):
                    a, b = uo.get(q), un.get(q)
                    if isinstance(a, str) or isinstance(b, str):
                        if a != b:
                            diffs.append(f"{q} {a} -> {b}")
                    elif (a is None) != (b is None) or (a is not None and abs(a - b) > REL_TOL * max(abs(a), 1e-12)):
                        diffs.append(f"U[{q}] {a} -> {b}")
                rows.append({"group": group, "system": system, "case": f.stem, "verdict": new["verdict"],
                             "status": "match" if not diffs else "MISMATCH", "diffs": diffs})
                if diffs:
                    bad.append(rows[-1])
    out = REPO / "results" / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    (out / "replay.json").write_text(json.dumps(rows, indent=1))
    n_match = sum(r["status"] == "match" for r in rows)
    print(f"replayed {len(rows)} results: {n_match} match, {len(bad)} mismatch/error, "
          f"{sum(r['status'].startswith('skipped') for r in rows)} skipped (infrastructure errors)")
    for b in bad:
        print("  ", b["group"], b["system"], b["case"], b["status"], "; ".join(b.get("diffs") or []))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
