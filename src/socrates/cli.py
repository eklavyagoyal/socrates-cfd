"""Command-line entry points.

    socrates run-case CASE.yaml [--spec SPEC.yaml] [--store DIR]
    socrates verify RUN_ID [--store DIR]
    socrates benchmark ...   (see socrates.orchestration.benchmark)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .case_generation.spec import CaseConfig, ProblemSpec
from .checks.verifier import RunGraph, RunNode, verify
from .orchestration.store import RunStore

REPO = Path(__file__).resolve().parents[2]
DEFAULT_SPEC = REPO / "configs" / "problem_cylinder_re100.yaml"
DEFAULT_STORE = REPO / "results" / "runs"


def _cmd_run_case(a: argparse.Namespace) -> None:
    spec = ProblemSpec.from_yaml(a.spec)
    cfg = CaseConfig.from_yaml(a.case)
    store = RunStore(a.store)
    res = store.get_or_run(cfg, spec, reason=a.reason, launched_by="cli")
    print(json.dumps({"run_id": res.run_id, "status": res.status,
                      "qoi": (res.evidence or {}).get("qoi")}, indent=2, default=str))


def _cmd_verify(a: argparse.Namespace) -> None:
    spec = ProblemSpec.from_yaml(a.spec)
    store = RunStore(a.store)
    r = store.load(a.run_id)
    v = verify(RunGraph([RunNode(r.run_id, r.config, r.evidence or {}, ok=r.ok)], r.run_id), spec)
    print(json.dumps(v.to_dict(), indent=2, default=str))


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="socrates")
    sub = p.add_subparsers(dest="cmd", required=True)
    rc = sub.add_parser("run-case", help="generate, run and extract evidence for one case")
    rc.add_argument("case")
    rc.add_argument("--spec", default=str(DEFAULT_SPEC))
    rc.add_argument("--store", default=str(DEFAULT_STORE))
    rc.add_argument("--reason", default="manual run")
    rc.add_argument("--slots", type=int, default=1)
    rc.set_defaults(func=_cmd_run_case)
    vf = sub.add_parser("verify", help="static verification of one stored run")
    vf.add_argument("run_id")
    vf.add_argument("--spec", default=str(DEFAULT_SPEC))
    vf.add_argument("--store", default=str(DEFAULT_STORE))
    vf.set_defaults(func=_cmd_verify)
    a = p.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
