"""The systems compared in the benchmark (see docs/design.md, pre-registered protocol).

A       OpenFOAM diagnostics only (what a user gets from the solver itself)
B       static deterministic verifier on the single submitted run
C       adaptive: verifier + LLM critic + experiment primitives (strict authority)
C-rule  adaptive with the deterministic rule-based planner (no LLM)
B+exh   fixed exhaustive experiment protocol, then the verifier (no planner)
L-judge LLM judgement on static evidence, no experiments, no deterministic gating
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from ..case_generation.spec import ProblemSpec
from ..checks.base import load_config
from ..checks.verifier import RunGraph, RunNode, verify
from ..critic.audit import audit_numbers
from ..critic.backends import ClaudeCLIBackend
from ..critic.prompt import alias_map, anonymize, build_package, render_user_prompt
from ..experiments.primitives import ActionRejected, plan_experiment
from .loop import LLMPlanner, RuleBasedPlanner, run_adaptive
from .store import RunStore


def system_a(ev: dict) -> dict:
    """Ordinary solver diagnostics: completion, checkMesh, steady residual convergence."""
    sol = ev.get("solver") or {}
    cm = ((ev.get("mesh") or {}).get("checkMesh") or {})
    reasons = []
    if not sol.get("completed"):
        reasons.append("solver did not complete")
    if not cm.get("mesh_ok"):
        reasons.append("checkMesh failed")
    if (ev.get("configuration") or {}).get("solver") == "simpleFoam" and sol.get("steady_converged_iteration") is None:
        reasons.append("steady residualControl not satisfied")
    return {"verdict": "REJECT" if reasons else "ACCEPT", "reasons": reasons or ["solver completed; checkMesh OK"]}


def _root_graph(store: RunStore, root: str) -> RunGraph:
    r = store.load(root)
    return RunGraph([RunNode(root, r.config, r.evidence or {}, ok=r.ok)], root)


def system_b(store: RunStore, spec: ProblemSpec, root: str) -> dict:
    v = verify(_root_graph(store, root), spec, load_config())
    return v.to_dict()


def system_c(store: RunStore, spec: ProblemSpec, root: str, planner: str = "llm", **kw) -> dict:
    p = LLMPlanner() if planner == "llm" else RuleBasedPlanner()
    return run_adaptive(root, store, spec, p, **kw).to_dict()


def review_only(store: RunStore, spec: ProblemSpec, result: dict, vcfg: dict | None = None) -> dict:
    """Apply the LLM acceptance review to a finished adaptive result (same runs, no new simulations)."""
    from .loop import graph_for

    g = graph_for(store, result["root_run"], result["runs"])
    v = verify(g, spec, vcfg or load_config())
    if v.verdict != "ACCEPT":
        return {"verdict": v.verdict, "review": None, "note": "no ACCEPT to review"}
    rv = LLMPlanner().review(spec, g, v, result.get("history") or [])
    if rv.get("failure"):
        verdict = "INCONCLUSIVE"
    else:
        verdict = "ACCEPT" if rv.get("concur") else "INCONCLUSIVE"
    return {"verdict": verdict, "review": rv}


EXHAUSTIVE_PROTOCOL = [
    ("RUN_LONGER", {}, "root"),
    ("REFINE_MESH", {}, "root"),
    ("REFINE_MESH", {}, "last_mesh"),
    ("REDUCE_TIME_STEP", {}, "root"),
    ("EXPAND_DOMAIN", {}, "root"),
]


def system_b_exhaustive(store: RunStore, spec: ProblemSpec, root: str) -> dict:
    graph = _root_graph(store, root)
    root_node = graph.nodes[root]
    log, last_mesh = [], root
    for action, params, parent_key in EXHAUSTIVE_PROTOCOL:
        parent = root if parent_key == "root" else last_mesh
        pn = graph.nodes[parent]
        try:
            plan = plan_experiment(action, params, parent_run=parent, parent_cfg=pn.config, parent_ev=pn.evidence,
                                   root_cfg=root_node.config)
        except ActionRejected as exc:
            log.append({"action": action, "parent": parent, "rejected": str(exc)})
            continue
        res = store.get_or_run(plan.child_config, spec, init=plan.init, parent_run=parent,
                               reason=f"exhaustive protocol: {action}", experiment=plan.to_dict(), launched_by="exhaustive")
        graph.nodes[res.run_id] = RunNode(res.run_id, res.config, res.evidence or {}, parent=parent, action=action, ok=res.ok)
        if action == "REFINE_MESH":
            last_mesh = res.run_id
        log.append({"action": action, "parent": parent, "run_id": res.run_id, "status": res.status,
                    "cell_steps": ((res.evidence or {}).get("cost") or {}).get("cell_steps"),
                    "wall_seconds": res.provenance.get("wall_seconds")})
    v = verify(graph, spec, load_config())
    return {"verdict": v.verdict, "verifier": v.to_dict(), "experiments": log, "runs": list(graph.nodes)}


JUDGE_SYSTEM_PROMPT = """You are an expert CFD reviewer. You are given the recorded evidence of ONE completed simulation
and the results of deterministic checks on it. No further simulations can be run.
Decide whether the requested quantities from this simulation can be trusted to the requested relative tolerance:
ACCEPT (trustworthy), REJECT (not trustworthy), or INCONCLUSIVE (cannot tell from this evidence).
Rules: reason only from the recorded evidence; do not use remembered literature or textbook values of any quantity
for this problem; every number you write must appear in the evidence. Output JSON matching the schema."""


class JudgeDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["ACCEPT", "REJECT", "INCONCLUSIVE"]
    confidence: Literal["LOW", "MEDIUM", "HIGH"]
    reasoning_summary: list[str]


JUDGE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["decision", "confidence", "reasoning_summary"],
    "properties": {
        "decision": {"type": "string", "enum": ["ACCEPT", "REJECT", "INCONCLUSIVE"]},
        "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
        "reasoning_summary": {"type": "array", "items": {"type": "string"}},
    },
}


def llm_judge(store: RunStore, spec: ProblemSpec, root: str, backend=None) -> dict:
    backend = backend or ClaudeCLIBackend()
    graph = _root_graph(store, root)
    v = verify(graph, spec, load_config())
    pkg = anonymize(build_package(spec, graph, v, history=[], menu=[], budget={"note": "no experiments possible"}),
                    alias_map(graph))
    pkg.pop("experiment_menu", None)
    pkg.pop("budget", None)
    pkg.pop("previous_critic_decisions", None)
    call = backend.complete(JUDGE_SYSTEM_PROMPT, render_user_prompt(pkg), JUDGE_SCHEMA)
    out = {"backend": backend.describe(), "ok": call.ok, "latency_s": call.latency_s, "cost_usd": call.cost_usd,
           "errors": call.errors}
    out["model_fingerprint"] = getattr(call, "model_fingerprint", None)
    try:
        if not call.ok:
            raise ValueError("LLM call failed")
        d = JudgeDecision.model_validate(call.output)
        out.update(verdict=d.decision, confidence=d.confidence, reasoning_summary=d.reasoning_summary,
                   numeric_audit=audit_numbers(d.reasoning_summary, pkg))
    except Exception as exc:  # noqa: BLE001 -- recorded as ERROR, counted as undecided
        out.update(verdict="ERROR", error=repr(exc))
    return out
