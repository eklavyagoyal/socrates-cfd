"""Adaptive verification loop: simulation -> evidence -> checks -> critic -> experiment -> ...

Authority structure (strict mode):
* The deterministic verifier decides ACCEPT/REJECT.  When its verdict is
  decisive the loop stops without consulting the planner.
* While the verdict is INCONCLUSIVE the planner (LLM critic or rule-based)
  may only (a) request one validated experiment primitive or (b) give up.
  An ACCEPT/REJECT proposed against the deterministic verdict is recorded as
  an authority violation, fed back once, and never executed.
* Budgets bound experiments, planner calls and compute; exhausting any of
  them yields INCONCLUSIVE.
"""

from __future__ import annotations

import datetime as _dt
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Protocol

from ..case_generation.blockmesh import resolve_layout
from ..case_generation.spec import ProblemSpec
from ..checks.base import load_config
from ..checks.verifier import RunGraph, RunNode, Verdict, verify
from ..critic.audit import audit_numbers
from ..critic.backends import ClaudeCLIBackend
from ..critic.prompt import (
    REVIEW_SCHEMA,
    REVIEW_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
    build_package,
    menu_entries,
    render_user_prompt,
)
from ..critic.rule_based import rule_based_decision
from ..critic.schema import CriticDecision, json_schema
from ..experiments.primitives import ActionRejected, Limits, plan_experiment
from .store import RunStore


@dataclass
class Budget:
    max_experiments: int = 6
    max_planner_calls: int = 12
    max_cost_factor: float = 12.0  # total experiment cell-steps / root cell-steps
    max_invalid_actions: int = 3


class Planner(Protocol):
    name: str

    def decide(self, spec: ProblemSpec, graph: RunGraph, verdict: Verdict, history: list[dict],
               menu: list[dict], budget: dict, feedback: str | None) -> tuple[CriticDecision | None, dict]: ...


class RuleBasedPlanner:
    name = "rule_based"

    def decide(self, spec, graph, verdict, history, menu, budget, feedback):
        d = rule_based_decision(graph, verdict)
        # skip actions that were already rejected for this parent (limits/budget)
        rejected = {(h.get("next_experiment") or {}).get("action") for h in history if h.get("action_rejected")}
        if d.next_experiment and d.next_experiment.action in rejected:
            from ..critic.rule_based import candidate_actions

            alts = [c for c in candidate_actions(graph, verdict) if c.action not in rejected]
            d = d.model_copy(update={"next_experiment": alts[0] if alts else None})
        return d, {"planner": self.name}


class LLMPlanner:
    def __init__(self, backend=None, name: str = "llm_critic"):
        self.backend = backend or ClaudeCLIBackend()
        self.name = name

    def decide(self, spec, graph, verdict, history, menu, budget, feedback):
        package = build_package(spec, graph, verdict, history, menu, budget)
        prompt = render_user_prompt(package)
        if feedback:
            prompt += "\n\nFEEDBACK ON YOUR PREVIOUS ANSWER (it was not executed):\n" + feedback
        call = self.backend.complete(SYSTEM_PROMPT, prompt, json_schema())
        meta = {"planner": self.name, "backend": self.backend.describe(), "latency_s": call.latency_s,
                "cost_usd": call.cost_usd, "attempts": call.attempts, "errors": call.errors,
                "prompt_chars": len(prompt)}
        if not call.ok:
            meta["failure"] = "LLM call failed"
            return None, meta
        try:
            d = CriticDecision.model_validate(call.output)
        except Exception as exc:  # noqa: BLE001 -- recorded
            meta["failure"] = f"schema validation failed: {exc}"
            meta["raw_output"] = call.output
            return None, meta
        texts = list(d.reasoning_summary) + list(d.missing_evidence) + [h.hypothesis for h in d.hypotheses]
        if d.next_experiment:
            texts += [d.next_experiment.reason, d.next_experiment.expected_outcome]
        meta["numeric_audit"] = audit_numbers(texts, package)
        return d, meta

    def review(self, spec, graph, verdict, history) -> dict:
        """Acceptance review: may only concur or raise evidence-cited blocking concerns."""
        package = build_package(spec, graph, verdict, history, [], {"note": "review only; no experiments"})
        package.pop("experiment_menu", None)
        call = self.backend.complete(REVIEW_SYSTEM_PROMPT, render_user_prompt(package), REVIEW_SCHEMA)
        out = {"latency_s": call.latency_s, "cost_usd": call.cost_usd, "attempts": call.attempts, "errors": call.errors}
        if not call.ok or not isinstance(call.output, dict) or "concur" not in call.output:
            out["failure"] = "review call failed or malformed"
            return out
        o = call.output
        concerns = [c for c in o.get("blocking_concerns", []) if c.get("evidence_fields")]
        texts = list(o.get("reasoning_summary", [])) + [c["concern"] for c in concerns]
        out.update(concur=bool(o["concur"]) and not concerns, blocking_concerns=concerns,
                   reasoning_summary=o.get("reasoning_summary", []), numeric_audit=audit_numbers(texts, package))
        return out


@dataclass
class LoopResult:
    root_run: str
    planner: str
    final_verdict: str
    stop_reason: str
    verdict: dict
    history: list[dict]
    runs: list[str]
    experiments: list[dict]
    cost: dict
    authority_violations: list[dict] = field(default_factory=list)
    started: str = ""
    finished: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _node(store: RunStore, rid: str, parent: str | None = None, action: str | None = None) -> RunNode:
    r = store.load(rid)
    return RunNode(rid, r.config, r.evidence or {}, parent=parent, action=action, ok=r.ok)


def _cell_steps(node: RunNode) -> float:
    c = (node.evidence or {}).get("cost") or {}
    return float(c.get("cell_steps") or 0.0)


def make_estimator(store: RunStore, graph: RunGraph, root_cfg, root_ev):
    """Wall-time estimates per (action, candidate parent) from measured throughput of the root run."""
    rc = root_ev.get("cost") or {}
    sec_per_cell_step = (rc.get("wall_seconds") or 0) / max(rc.get("cell_steps") or 1, 1)

    def estimate(action: str) -> dict:
        out = {}
        for rid, n in graph.nodes.items():
            try:
                plan = plan_experiment(action, None, parent_run=rid, parent_cfg=n.config, parent_ev=n.evidence,
                                       root_cfg=root_cfg)
                out[rid] = round(plan.estimated_cell_steps * sec_per_cell_step)
            except ActionRejected as exc:
                out[rid] = f"not allowed: {exc}"
        return out

    return estimate


def run_adaptive(
    root_run: str,
    store: RunStore,
    spec: ProblemSpec,
    planner: Planner,
    budget: Budget | None = None,
    limits: Limits | None = None,
    vcfg: dict | None = None,
    log_path: Path | None = None,
    acceptance_review: bool = False,
) -> LoopResult:
    budget = budget or Budget()
    limits = limits or Limits()
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
    vcfg = vcfg or load_config()
    started = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    root = _node(store, root_run)
    graph = RunGraph([root], root_run)
    root_cost = max(_cell_steps(root), 1.0)
    history: list[dict] = []
    experiments: list[dict] = []
    violations: list[dict] = []
    spent = 0.0
    calls = 0
    invalid = 0
    feedback: str | None = None
    stop_reason = ""
    final = "INCONCLUSIVE"
    t0 = time.monotonic()

    while True:
        verdict = verify(graph, spec, vcfg)
        if verdict.verdict == "ACCEPT" and acceptance_review and hasattr(planner, "review"):
            rv = planner.review(spec, graph, verdict, history)
            calls += 1
            history.append({"iteration": calls, "deterministic_verdict": "ACCEPT", "review": rv,
                            "outcome": "acceptance review"})
            if rv.get("failure"):
                final, stop_reason = "INCONCLUSIVE", "acceptance review failed (fail-safe: no unreviewed ACCEPT)"
            elif rv.get("concur"):
                final, stop_reason = "ACCEPT", "deterministic ACCEPT; acceptance review concurred"
            else:
                final, stop_reason = "INCONCLUSIVE", "acceptance review raised blocking concern(s): human review required"
            break
        if verdict.verdict in ("ACCEPT", "REJECT"):
            final, stop_reason = verdict.verdict, "deterministic verifier verdict is decisive"
            break
        if calls >= budget.max_planner_calls:
            stop_reason = "planner-call budget exhausted"
            break
        if len(experiments) >= budget.max_experiments:
            stop_reason = "experiment budget exhausted"
            break
        bud = {"experiments_used": len(experiments), "max_experiments": budget.max_experiments,
               "compute_used_relative_to_root": round(spent / root_cost, 2),
               "max_compute_relative_to_root": budget.max_cost_factor}
        menu = menu_entries(graph, make_estimator(store, graph, root.config, root.evidence))
        decision, meta = planner.decide(spec, graph, verdict, history, menu, bud, feedback)
        calls += 1
        feedback = None
        entry = {"iteration": calls, "deterministic_verdict": verdict.verdict,
                 "missing_components": verdict.missing_components, "meta": meta}
        if decision is None:
            entry["outcome"] = "planner failure"
            history.append(entry)
            invalid += 1
            if invalid >= budget.max_invalid_actions:
                stop_reason = "repeated planner failures"
                break
            continue
        entry.update(decision=decision.decision, confidence=decision.confidence,
                     reasoning_summary=decision.reasoning_summary, missing_evidence=decision.missing_evidence,
                     hypotheses=[h.model_dump() for h in decision.hypotheses],
                     next_experiment=decision.next_experiment.model_dump() if decision.next_experiment else None)
        if decision.decision in ("ACCEPT", "REJECT"):
            v = {"iteration": calls, "proposed": decision.decision, "deterministic": verdict.verdict}
            violations.append(v)
            entry["outcome"] = "authority violation: decision not supported by deterministic verdict; not executed"
            history.append(entry)
            invalid += 1
            feedback = (f"You proposed {decision.decision}, but the deterministic verdict is {verdict.verdict} with "
                        f"missing components {verdict.missing_components}. Only MORE_EVIDENCE is allowed now.")
            if invalid >= budget.max_invalid_actions:
                stop_reason = "repeated unsupported decisions"
                break
            continue
        ne = decision.next_experiment
        if ne is None:
            entry["outcome"] = "planner chose to stop (no useful affordable experiment)"
            history.append(entry)
            stop_reason = "planner stopped"
            break
        if ne.parent_run not in graph.nodes:
            entry["outcome"] = f"rejected: unknown parent_run {ne.parent_run}"
            entry["action_rejected"] = True
            history.append(entry)
            invalid += 1
            feedback = f"parent_run must be one of {list(graph.nodes)}"
            if invalid >= budget.max_invalid_actions:
                stop_reason = "repeated invalid actions"
                break
            continue
        parent = graph.nodes[ne.parent_run]
        try:
            plan = plan_experiment(ne.action, ne.parameters, parent_run=ne.parent_run, parent_cfg=parent.config,
                                   parent_ev=parent.evidence, root_cfg=root.config, limits=limits)
        except ActionRejected as exc:
            entry["outcome"] = f"rejected by validator: {exc}"
            entry["action_rejected"] = True
            history.append(entry)
            invalid += 1
            feedback = f"Your experiment was rejected by the validator: {exc}"
            if invalid >= budget.max_invalid_actions:
                stop_reason = "repeated invalid actions"
                break
            continue
        if spent + plan.estimated_cell_steps > budget.max_cost_factor * root_cost:
            entry["outcome"] = (f"rejected: estimated cost {plan.estimated_cell_steps / root_cost:.1f}x root exceeds "
                                f"remaining budget {(budget.max_cost_factor * root_cost - spent) / root_cost:.1f}x")
            entry["action_rejected"] = True
            history.append(entry)
            invalid += 1
            feedback = entry["outcome"]
            if invalid >= budget.max_invalid_actions:
                stop_reason = "compute budget exhausted"
                break
            continue
        res = store.get_or_run(plan.child_config, spec, init=plan.init, parent_run=ne.parent_run,
                               reason=ne.reason, experiment=plan.to_dict(), launched_by=planner.name)
        node = _node(store, res.run_id, parent=ne.parent_run, action=ne.action)
        if res.run_id in graph.nodes:
            entry["outcome"] = f"duplicate experiment: {res.run_id} already in the graph"
            invalid += 1
        else:
            graph.nodes[res.run_id] = node
            spent += _cell_steps(node)
            experiments.append({**plan.to_dict(), "run_id": res.run_id, "status": res.status,
                                "cell_steps": _cell_steps(node), "wall_seconds": res.provenance.get("wall_seconds")})
            entry["outcome"] = f"executed -> {res.run_id} ({res.status})"
        history.append(entry)
        if log_path:
            log_path.write_text(json.dumps({"partial": True, "history": history}, indent=1, default=str))

    final_v = verify(graph, spec, vcfg)
    res = LoopResult(
        root_run=root_run, planner=planner.name, final_verdict=final, stop_reason=stop_reason,
        verdict=final_v.to_dict(), history=history, runs=list(graph.nodes), experiments=experiments,
        cost={"experiment_cell_steps": spent, "relative_to_root": spent / root_cost,
              "experiment_wall_seconds": sum((e.get("wall_seconds") or 0) for e in experiments),
              "n_experiments": len(experiments), "planner_calls": calls,
              "planner_cost_usd": sum((h.get("meta") or {}).get("cost_usd") or 0 for h in history),
              "loop_wall_seconds": time.monotonic() - t0},
        authority_violations=violations, started=started,
        finished=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    )
    if log_path:
        log_path.write_text(json.dumps(res.to_dict(), indent=1, default=str))
    return res


def graph_for(store: RunStore, root_run: str, run_ids: list[str]) -> RunGraph:
    """Rebuild a RunGraph for stored runs using their provenance (parent + experiment action)."""
    nodes = []
    for rid in run_ids:
        r = store.load(rid)
        exp = r.provenance.get("experiment") or {}
        nodes.append(RunNode(rid, r.config, r.evidence or {}, parent=r.provenance.get("parent_run") if rid != root_run else None,
                             action=exp.get("action") if rid != root_run else None, ok=r.ok))
    return RunGraph(nodes, root_run)


def estimate_root_cells(cfg) -> int:
    return resolve_layout(cfg).n_cells
