"""Evidence package and instructions for the critic.

The package is the critic's *only* source of facts.  It is built from
recorded evidence and deterministic check results; in blind mode it
contains no reference/literature values for the requested quantities.
"""

from __future__ import annotations

import json

from ..case_generation.spec import ProblemSpec
from ..checks.verifier import RunGraph, Verdict
from ..experiments.primitives import ACTION_DESCRIPTIONS, ACTION_SPECS

SYSTEM_PROMPT = """You are the critic in an automated CFD solution-verification system.

Your job: decide whether the recorded evidence is sufficient to trust the requested quantities of ONE simulation
(the "root" run) at the requested tolerance, and if it is not, choose the single most informative next experiment
from a fixed menu of validated experiment primitives.

AUTHORITY RULES (hard constraints)
1. The evidence package is your only source of facts. Never use remembered literature or textbook values of any
   quantity for this problem as evidence, and never quote such values. Reason only from recorded measurements.
2. Never invent or estimate a measurement that is not in the package. Every number you write must appear in the package.
3. A deterministic FAIL is a measured fact. You may not overrule it. You may explain it.
4. Deterministic checks marked INCONCLUSIVE mean the evidence is missing; absence of evidence is never a pass.
5. Decisions:
   - ACCEPT only if the deterministic verifier verdict is ACCEPT (all uncertainty components measured and within budget).
   - REJECT if the deterministic verifier has a FAIL that invalidates the requested quantities of the root run.
   - MORE_EVIDENCE otherwise, with exactly one next_experiment chosen from the menu, applied to a listed run_id.
   If the remaining budget cannot afford any useful experiment, answer MORE_EVIDENCE with next_experiment null;
   the system will then report INCONCLUSIVE.
6. You cannot run commands, edit files or change the simulation in any other way than the menu.

HOW TO CHOOSE AN EXPERIMENT
- Prefer the experiment most likely to expose a flaw that would change the answer by more than the tolerance,
  using the recorded configuration and evidence (e.g. resolution, domain extents, time step, Courant number,
  run length, scheme order) to form hypotheses.
- Consider cost: each menu entry lists its estimated cost; the budget is limited.
- Experiments are compared against their parent: choose parent_run deliberately (usually the root, or the finest
  run of the same refinement family to continue a refinement sequence).
- State the hypothesis the experiment tests and what outcome would confirm or refute it.

OUTPUT: a single JSON object matching the provided schema. reasoning_summary: short factual bullet points that cite
run ids and recorded values. missing_evidence: what is still unmeasured."""


def _r(x, n=5):
    if isinstance(x, float):
        return float(f"{x:.{n}g}")
    return x


def _round_tree(o, n=5):
    if isinstance(o, dict):
        return {k: _round_tree(v, n) for k, v in o.items()}
    if isinstance(o, list):
        return [_round_tree(v, n) for v in o]
    return _r(o, n)


def run_summary(graph: RunGraph, rid: str) -> dict:
    n = graph.nodes[rid]
    ev = n.evidence or {}
    conf = ev.get("configuration", {})
    mesh = ev.get("mesh", {})
    md = mesh.get("design", {})
    cm = mesh.get("checkMesh") or {}
    sol = ev.get("solver", {})
    tb = ev.get("temporal_behavior", {})
    q = ev.get("qoi", {})
    sw = (ev.get("forces") or {}).get("stationary_window") or {}
    return _round_tree({
        "run_id": rid,
        "parent_run": n.parent,
        "created_by": n.action or "submitted simulation (root)" if rid == graph.root else n.action,
        "completed": n.ok,
        "configuration": {
            "solver": conf.get("solver"),
            "time_scheme": conf.get("ddt_scheme"),
            "convection_scheme": conf.get("convection_scheme"),
            "pimple": conf.get("pimple"),
            "time_step_convective_units": conf.get("time_step_convective"),
            "end_time_convective_units": conf.get("end_time_convective"),
            "declared_averaging_start_convective_units": conf.get("declared_averaging_start_convective"),
            "configured_reynolds": conf.get("configured_reynolds"),
            "force_reference_used": conf.get("force_reference"),
            "domain_D": ev.get("domain"),
            "inlet_velocity_measured": ev.get("inlet"),
        },
        "mesh": {
            "cells": mesh.get("n_cells"),
            "representative_cell_size_D": mesh.get("representative_cell_size_D"),
            "cells_around_cylinder": md.get("cells_around_cylinder"),
            "wall_first_cell_D": md.get("wall_normal_first_cell_D"),
            "wake_cells_streamwise": md.get("wake_cells_streamwise"),
            "wake_last_cell_D": md.get("wake_last_cell_D"),
            "checkMesh_ok": cm.get("mesh_ok"),
            "cylinder_patch_extent_x_m": (mesh.get("measured_geometry") or {}).get("cylinder_diameter_x_m"),
            "cylinder_patch_extent_y_m": (mesh.get("measured_geometry") or {}).get("cylinder_diameter_y_m"),
            "max_non_orthogonality_deg": cm.get("max_non_orthogonality"),
            "max_skewness": cm.get("max_skewness"),
        },
        "solver_diagnostics": {
            "completed": sol.get("completed"),
            "max_courant": sol.get("courant_max"),
            "time_steps": sol.get("n_steps"),
            "steady_converged_iteration": sol.get("steady_converged_iteration"),
            "mass_imbalance_max": (ev.get("conservation") or {}).get("relative_imbalance_max"),
        },
        "temporal_behavior": {
            "oscillating": tb.get("oscillating"),
            "record_length_convective": tb.get("record_length_convective"),
            "transient_end_detected_convective": tb.get("transient_end_time_convective"),
            "stationary_cycles": tb.get("stationary_cycles"),
            "steps_per_shedding_period": tb.get("steps_per_period"),
        },
        "quantities_reported_by_submitted_setup": {k: v for k, v in (q.get("reported") or {}).items() if k != "basis"},
        "quantities_stationary_window": q.get("stationary"),
        "cl_amplitude_mean": sw.get("cl_amplitude_mean"),
        "cost_wall_seconds": (ev.get("cost") or {}).get("wall_seconds"),
    })


def check_table(verdict: Verdict) -> list[dict]:
    rows = []
    for c in verdict.checks:
        rows.append(_round_tree({
            "check": c.check, "quantity": c.qoi, "status": c.status.value, "component": c.component,
            "value": c.value if not isinstance(c.value, (dict, list)) else c.value,
            "uncertainty_of_root": c.uncertainty, "runs": c.runs, "reason": c.reason,
        }, 4))
    return rows


def alias_map(graph: RunGraph) -> dict[str, str]:
    """Opaque, stable aliases for run ids (R0 = root, then in creation order).

    Run ids embed the case name (e.g. 'B1_small_domain-...'), which would tell
    the LLM what the flaw is.  Every LLM-facing text uses these aliases instead.
    """
    return {rid: f"R{i}" for i, rid in enumerate(graph.nodes)}


def anonymize(obj, aliases: dict[str, str]):
    """Replace every real run id (in strings and dict keys) by its alias."""
    order = sorted(aliases, key=len, reverse=True)

    def sub(x: str) -> str:
        for rid in order:
            if rid in x:
                x = x.replace(rid, aliases[rid])
        return x

    if isinstance(obj, str):
        return sub(obj)
    if isinstance(obj, dict):
        return {(sub(k) if isinstance(k, str) else k): anonymize(v, aliases) for k, v in obj.items()}
    if isinstance(obj, list):
        return [anonymize(v, aliases) for v in obj]
    return obj


def build_package(spec: ProblemSpec, graph: RunGraph, verdict: Verdict, history: list[dict],
                  menu: list[dict], budget: dict) -> dict:
    s = spec.model_dump(mode="json")
    return {
        "engineering_question": s["problem"]["question"],
        "problem_specification": {
            "geometry": s["geometry"], "operating_conditions": s["operating_conditions"],
            "fluid": s["problem"]["fluid"], "requested_outputs": s["requested_outputs"],
            "requested_relative_tolerance": s["verification"]["requested_tolerance"],
        },
        "root_run": graph.root,
        "runs": [run_summary(graph, rid) for rid in graph.nodes],
        "deterministic_verifier": {
            "verdict": verdict.verdict,
            "failed_checks": verdict.failed_checks,
            "per_quantity": _round_tree(verdict.per_qoi, 4),
            "missing_uncertainty_components": verdict.missing_components,
            "checks": check_table(verdict),
            "error_budget_rule": "each component must have estimated uncertainty <= 0.5*tolerance and the root-sum-square "
                                 "of all components <= tolerance; a demonstrated change > tolerance is a FAIL",
        },
        "previous_critic_decisions": [{k: v for k, v in h.items() if k != "meta"} for h in history],
        "experiment_menu": menu,
        "budget": budget,
    }


def menu_entries(graph: RunGraph, estimate) -> list[dict]:
    """Menu of primitives with descriptions, parameter ranges and cost estimates per candidate parent."""
    out = []
    for action, params in ACTION_SPECS.items():
        out.append({
            "action": action,
            "description": ACTION_DESCRIPTIONS[action],
            "parameters": {k: {"min": lo, "max": hi, "default": round(d, 4)} for k, (lo, hi, d) in params.items()},
            "estimated_wall_seconds_by_parent": estimate(action),
        })
    return out


def render_user_prompt(package: dict) -> str:
    return ("Evidence package (JSON). Decide according to the rules.\n\n" + json.dumps(package, indent=1, default=str))


REVIEW_SYSTEM_PROMPT = """You are the acceptance reviewer in an automated CFD verification system.

The deterministic verifier's verdict for the root run is ACCEPT: every numerical-uncertainty component it knows
about (averaging, statistics, mesh, time step, domain) was measured and is within the error budget.

Your task: look for any reason, visible in the recorded evidence, why the answer should still NOT be trusted that
the deterministic checks do not cover. In particular compare what was actually simulated with what the engineering
question and specification ask for (for example measured geometry, measured inlet conditions, boundary-condition
types, physical parameters, the requested quantities).

Rules:
- You cannot REJECT and you cannot request simulations. You can only concur, or raise blocking concerns that send the
  result to human review.
- Raise a blocking concern only if you can point to specific recorded evidence fields. Do not raise generic concerns
  (e.g. "2D laminar modelling", "tolerance choice") that apply to every simulation of this problem.
- Never use remembered literature values of any quantity for this problem. Every number you write must appear in the
  evidence package.
Output a single JSON object matching the schema."""

REVIEW_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["concur", "blocking_concerns", "reasoning_summary"],
    "properties": {
        "concur": {"type": "boolean"},
        "blocking_concerns": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["concern", "evidence_fields"],
            "properties": {"concern": {"type": "string"}, "evidence_fields": {"type": "array", "items": {"type": "string"}}}}},
        "reasoning_summary": {"type": "array", "items": {"type": "string"}},
    },
}
