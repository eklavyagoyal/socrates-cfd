"""Deterministic planner used for ablations (no LLM).

Pre-registered policy (fixed before any benchmark run, see docs/design.md):
1. deterministic REJECT  -> REJECT; deterministic ACCEPT -> ACCEPT
2. otherwise take the first missing uncertainty component in the fixed order
       statistics/averaging -> mesh -> time -> domain
   and request the matching primitive with default parameters.  Refinement
   families are continued from their finest member.
3. if the chosen action is impossible (limits/budget), try the next component;
   if none is possible -> stop (INCONCLUSIVE).
"""

from __future__ import annotations

from ..checks.verifier import COMPONENT_TO_ACTION, RunGraph, Verdict
from .schema import CriticDecision, NextExperiment

ORDER = ("averaging", "statistics", "mesh", "time", "domain")


def candidate_actions(graph: RunGraph, verdict: Verdict) -> list[NextExperiment]:
    missing: set[str] = set()
    for comps in verdict.missing_components.values():
        missing.update(comps)
    out: list[NextExperiment] = []
    seen = set()
    # a sensitivity study blocked by a statistically unreliable member: lengthen that member first
    for c in verdict.checks:
        for rid in (c.details or {}).get("unreliable_members", []):
            if rid in graph.nodes and ("RUN_LONGER", rid) not in seen:
                seen.add(("RUN_LONGER", rid))
                parent = graph.longest_same_config(rid).run_id
                out.append(NextExperiment(action="RUN_LONGER", parameters={}, parent_run=parent,
                                          reason=f"refinement-family member {rid} is not statistically reliable",
                                          expected_outcome="a reliable stationary estimate for the sensitivity study"))
    for c in verdict.checks:
        if c.check == "physics_regime" and c.status.value == "INCONCLUSIVE" and ("RUN_LONGER", "regime") not in seen:
            seen.add(("RUN_LONGER", "regime"))
            out.append(NextExperiment(action="RUN_LONGER", parameters={}, parent_run=graph.longest_same_config(graph.root).run_id,
                                      reason="lift oscillation not yet a sustained limit cycle",
                                      expected_outcome="amplitude settles (sustained) or decays (no shedding)"))
    for comp in ORDER:
        if comp not in missing:
            continue
        action = COMPONENT_TO_ACTION[comp]
        if action in seen:
            continue
        seen.add(action)
        if action == "RUN_LONGER":
            parent = graph.longest_same_config(graph.root).run_id
        else:
            fam = graph.factor_family({"REFINE_MESH": "mesh", "REDUCE_TIME_STEP": "time", "EXPAND_DOMAIN": "domain"}[action])
            parent = fam[-1].run_id
        out.append(NextExperiment(action=action, parameters={}, parent_run=parent,
                                  reason=f"{comp} uncertainty component is unmeasured or not yet within budget",
                                  expected_outcome="quantifies the missing component"))
    return out


def rule_based_decision(graph: RunGraph, verdict: Verdict) -> CriticDecision:
    if verdict.verdict in ("ACCEPT", "REJECT"):
        return CriticDecision(decision=verdict.verdict, confidence="HIGH",
                              reasoning_summary=[f"deterministic verifier verdict is {verdict.verdict}"] +
                              [f"failed: {f}" for f in verdict.failed_checks])
    cands = candidate_actions(graph, verdict)
    missing = [f"{q}: {', '.join(c)}" for q, c in verdict.missing_components.items()]
    return CriticDecision(decision="MORE_EVIDENCE", confidence="LOW",
                          reasoning_summary=["deterministic verdict INCONCLUSIVE"],
                          missing_evidence=missing,
                          next_experiment=cands[0] if cands else None)
