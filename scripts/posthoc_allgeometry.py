"""Post-hoc protocol deviation, reported separately from the pre-registered results.

Variant: a checkMesh failure that only `-allGeometry` reports is a mesh-quality *concern*, not a demonstrated
defect: `mesh_quality` becomes INCONCLUSIVE instead of FAIL, and is discharged when every requested quantity
has a mesh-sensitivity PASS (the same policy the pre-registered verifier applies to the convection-scheme
order concern).  Motivation: J1, whose mesh passes default checkMesh but fails the -allGeometry cell
determinant check (results/posthoc/J1_checkMesh_{default,allGeometry}.log).

Which checks are -allGeometry-only was determined by running both modes on the same J1 mesh: -allGeometry adds
"Cell determinant", "Face flatness", "Face interpolation weight" and "Face volume ratio".

    python scripts/posthoc_allgeometry.py [--adaptive]

Outputs results/posthoc/B-allgeo/<case>.json for every benchmark case (no new simulations) and, with
--adaptive, results/posthoc/C-rule-allgeo/<case>.json for the cases whose static verdict changes.
The pre-registered decision code is not modified: the variant is applied by wrapping two functions here.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import socrates.checks.static as static  # noqa: E402
import socrates.checks.verifier as verifier  # noqa: E402
from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.base import Status  # noqa: E402
from socrates.orchestration.loop import Budget, RuleBasedPlanner, run_adaptive  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402

ALLGEO_ONLY = ("small determinant", "flatness", "interpolation weight", "volume ratio")
TAG = "post-hoc variant: -allGeometry-only checkMesh failure"
OUT = REPO / "results" / "posthoc"

_orig_mesh_quality = static.check_mesh_quality
_orig_aggregate = verifier.aggregate


def mesh_quality_variant(ev, cfg):
    r = _orig_mesh_quality(ev, cfg)
    cm = (ev.get("mesh") or {}).get("checkMesh") or {}
    lines = cm.get("error_lines") or []
    if (r.status == Status.FAIL and lines and len(lines) == cm.get("failed_checks")
            and all(any(k in ln.lower() for k in ALLGEO_ONLY) for ln in lines)):
        r.status = Status.INCONCLUSIVE
        r.reason = f"{TAG} ({lines[0].strip('* ')}); discharged only by a mesh-sensitivity PASS"
        r.details = {**(r.details or {}), "posthoc_allgeometry": True}
    return r


def aggregate_variant(checks, spec):
    v = _orig_aggregate(checks, spec)
    flagged = [c for c in checks if c.check == "mesh_quality" and (c.details or {}).get("posthoc_allgeometry")]
    mesh_ok_all = all(q["component_status"].get("mesh") == "PASS" for q in v.per_qoi.values())
    if flagged and mesh_ok_all:
        for c in flagged:
            c.status = Status.PASS
            c.reason += " -> discharged: mesh sensitivity PASS for every requested quantity"
        v = _orig_aggregate(checks, spec)
    return v


static.check_mesh_quality = mesh_quality_variant
verifier.aggregate = aggregate_variant


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adaptive", action="store_true", help="also run C-rule under the variant where B changes")
    a = ap.parse_args()
    man = yaml.safe_load((REPO / "benchmark" / "manifest.yaml").read_text())
    spec = ProblemSpec.from_yaml(REPO / man["problem_spec"])
    store = RunStore(REPO / "results" / "runs")
    changed = []
    for case in man["cases"]:
        fb = REPO / "results" / "benchmark" / "B" / f"{case['id']}.json"
        if not fb.exists():
            print(f"{case['id']}: no System B result, skipped", flush=True)
            continue
        b = json.loads(fb.read_text())
        rid = b.get("root_run")
        if not rid:
            print(f"{case['id']}: System B result has no root run ({b.get('verdict')}), skipped", flush=True)
            continue
        r = store.load(rid)
        g = verifier.RunGraph([verifier.RunNode(rid, r.config, r.evidence or {}, ok=r.ok)], rid)
        v = verifier.verify(g, spec)
        out = OUT / "B-allgeo" / f"{case['id']}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"case": case["id"], "root_run": rid, "variant": TAG, "pre_registered_B": b.get("verdict"),
                                   **v.to_dict()}, indent=1, default=str))
        print(f"B-allgeo {case['id']:24s} {b.get('verdict')} -> {v.verdict}", flush=True)
        if v.verdict != b.get("verdict"):
            changed.append((case["id"], rid))
    if not a.adaptive:
        return
    for cid, rid in changed:
        res = run_adaptive(rid, store, spec, RuleBasedPlanner(), Budget(),
                           log_path=OUT / "C-rule-allgeo" / f"{cid}.partial.json").to_dict()
        res.update(case=cid, variant=TAG)
        (OUT / "C-rule-allgeo" / f"{cid}.json").write_text(json.dumps(res, indent=1, default=str))
        print(f"C-rule-allgeo {cid:24s} -> {res['final_verdict']} ({res['stop_reason']}; "
              f"{len(res['experiments'])} experiments)", flush=True)


if __name__ == "__main__":
    main()
