"""Human-readable verification reports and evidence graphs.

Every number printed here is read from stored evidence, check results or
provenance records; the report generator performs no new analysis.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..case_generation.spec import ProblemSpec
from ..checks.verifier import COMPONENTS
from ..orchestration.store import RunStore

COMPONENT_LABEL = {
    "averaging": "Averaging window (reported vs stationary value)",
    "statistics": "Temporal statistics (stationarity, cycles)",
    "mesh": "Spatial discretisation (mesh sensitivity)",
    "time": "Temporal discretisation (time-step sensitivity)",
    "domain": "Artificial boundaries (domain sensitivity)",
}


def _fmt(x, nd=4):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        return f"{x:.{nd}g}"
    return str(x)


def evidence_graph(verdict: dict, spec: ProblemSpec, root: str) -> dict:
    """Claims (one per requested quantity) supported by checks, each pointing to runs."""
    checks = verdict["checks"]
    gates = [c for c in checks if c.get("component") is None]
    graph = {"root_run": root, "verdict": verdict["verdict"], "claims": []}
    for q in spec.requested_outputs:
        pq = verdict["per_qoi"][q]
        claim = {
            "claim": f"{q} of run {root} is reliable to within {pq['tolerance']:.0%}",
            "status": pq["verdict"],
            "combined_uncertainty": pq["combined_uncertainty"],
            "support": [],
        }
        for g in gates:
            claim["support"].append({"evidence": g["check"], "status": g["status"], "runs": g.get("runs") or [root],
                                     "source": g.get("source", "")})
        for comp in COMPONENTS:
            cs = [c for c in checks if c.get("qoi") == q and c.get("component") == comp]
            c = cs[-1] if cs else None
            claim["support"].append({
                "evidence": COMPONENT_LABEL[comp],
                "status": c["status"] if c else "MISSING",
                "uncertainty": c.get("uncertainty") if c else None,
                "runs": (c.get("runs") if c else []) or [],
                "reason": c.get("reason") if c else "no evidence",
            })
        graph["claims"].append(claim)
    return graph


def render_graph_text(graph: dict) -> str:
    lines = []
    for cl in graph["claims"]:
        lines.append(f"CLAIM: {cl['claim']}  [{cl['status']}]")
        sup = cl["support"]
        for i, s in enumerate(sup):
            last = i == len(sup) - 1
            br = "└──" if last else "├──"
            u = f" U={_fmt(s.get('uncertainty'), 3)}" if s.get("uncertainty") is not None else ""
            lines.append(f"{br} {s['evidence']}: {s['status']}{u}")
            pre = "    " if last else "│   "
            for r in s.get("runs") or []:
                lines.append(f"{pre}└── {r}")
        lines.append("")
    return "\n".join(lines)


def _run_line(store: RunStore, rid: str) -> dict:
    r = store.load(rid)
    ev = r.evidence or {}
    q = ev.get("qoi") or {}
    return {"run": rid, "status": r.status, "parent": r.provenance.get("parent_run"),
            "experiment": r.provenance.get("experiment"), "reported": q.get("reported"), "stationary": q.get("stationary"),
            "cells": (ev.get("mesh") or {}).get("n_cells"), "dt": r.config.time.delta_t,
            "half_height": r.config.domain.half_height, "wall_s": r.provenance.get("wall_seconds"),
            "software": (r.provenance.get("software") or {}).get("openfoam"), "created": r.provenance.get("created")}


def render_case_report(store: RunStore, spec: ProblemSpec, result: dict, title: str = "") -> str:
    """Markdown report for one adaptive (or static) verification result."""
    verdict = result.get("verdict") or result.get("verifier")
    root = result.get("root_run") or verdict.get("root_run")
    final = result.get("final_verdict") or verdict["verdict"]
    root_info = _run_line(store, root)
    out = [f"# Verification report{': ' + title if title else ''}", ""]
    out += ["## QUESTION", "", spec.problem.question.strip(), "",
            f"Requested: {', '.join(spec.requested_outputs)}; tolerance "
            f"{', '.join(f'{k} {v:.0%}' for k, v in spec.verification.requested_tolerance.items())}.", ""]
    rep = root_info["reported"] or {}
    out += ["## RESULT (as reported by the submitted simulation)", ""]
    for q in spec.requested_outputs:
        out.append(f"- {q}: {_fmt(rep.get(q), 5)}")
    out += ["", f"## VERDICT: **{final}**", ""]
    if result.get("stop_reason"):
        out.append(f"Stop reason: {result['stop_reason']}.")
    out += ["", "## EVIDENCE", ""]
    for c in verdict["checks"]:
        tag = f"[{c['qoi']}] " if c.get("qoi") else ""
        out.append(f"- **{c['status']}** {c['check']} {tag}— {c['reason']}")
    out += ["", "### Evidence graph", "", "```", render_graph_text(evidence_graph(verdict, spec, root)), "```", ""]
    out += ["## EXPERIMENT HISTORY", "", f"Run {root}: submitted simulation "
            f"({_fmt(root_info['cells'])} cells, dt={_fmt(root_info['dt'])} D/U, half-height {_fmt(root_info['half_height'])} D).", ""]
    for h in result.get("history", []):
        out.append(f"**Critic iteration {h['iteration']}** (deterministic verdict {h['deterministic_verdict']}):")
        for s in h.get("reasoning_summary") or []:
            out.append(f"  - {s}")
        if h.get("next_experiment"):
            ne = h["next_experiment"]
            out.append(f"  - Requested: {ne['action']} {ne.get('parameters') or ''} on {ne['parent_run']} — {ne['reason']}")
        out.append(f"  - Outcome: {h.get('outcome')}")
        audit = (h.get("meta") or {}).get("numeric_audit")
        if audit and audit.get("n_untraced"):
            out.append(f"  - Numeric audit: {audit['n_untraced']} number(s) not traceable to evidence: "
                       + ", ".join(u['token'] for u in audit['untraced'][:5]))
        out.append("")
    for e in result.get("experiments", []) or []:
        rid = e.get("run_id")
        if not rid:
            continue
        info = _run_line(store, rid)
        st, pst = info["stationary"] or {}, (_run_line(store, e["parent_run"])["stationary"] or {})
        changes = ", ".join(f"{k}: {_fmt(v['from'])}→{_fmt(v['to'])}" for k, v in (e.get("changes") or {}).items())
        out.append(f"Run {rid}: {e['action']} from {e['parent_run']} ({changes}).")
        for q in spec.requested_outputs:
            a, b = pst.get(q), st.get(q)
            if a is not None and b is not None:
                out.append(f"  - Observation: {q} {_fmt(a, 5)} → {_fmt(b, 5)} ({(b - a) / a:+.2%}).")
        out.append("")
    out += ["## FINAL JUSTIFICATION", ""]
    if verdict["failed_checks"]:
        out.append("Failed checks (measured): " + ", ".join(verdict["failed_checks"]) + ".")
    for q, pq in verdict["per_qoi"].items():
        comp = ", ".join(f"{k}={v}" for k, v in pq["component_status"].items())
        out.append(f"- {q}: {pq['verdict']} (components: {comp}; combined uncertainty "
                   f"{_fmt(pq['combined_uncertainty'], 3)} vs tolerance {pq['tolerance']:.0%}).")
    out += ["", "## REMAINING LIMITATIONS", ""]
    missing = verdict.get("missing_components") or {}
    if missing:
        for q, comps in missing.items():
            out.append(f"- {q}: not established — {', '.join(comps)}.")
    out += ["- Model-form error (2D, laminar, incompressible) is not assessed; verification ≠ validation.",
            "- Domain-error order q = 1 and safety factors are modelling choices (see docs/design.md).", ""]
    out += ["## PROVENANCE", ""]
    runs = result.get("runs") or [root]
    for rid in runs:
        info = _run_line(store, rid)
        out.append(f"- `{rid}` status={info['status']} parent={info['parent']} created={info['created']} "
                   f"wall={_fmt(info['wall_s'])} s; record: results/runs/{rid}/run.json")
    sw = root_info.get("software") or {}
    out.append(f"- OpenFOAM {sw.get('WM_PROJECT_VERSION')} (package {sw.get('package_version')}); "
               "problem specification and full configuration embedded in each run.json.")
    if result.get("cost"):
        out.append(f"- Experiment cost: {json.dumps(result['cost'], default=str)}")
    return "\n".join(out) + "\n"


def write_case_report(path: Path, store: RunStore, spec: ProblemSpec, result: dict, title: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_case_report(store, spec, result, title))
