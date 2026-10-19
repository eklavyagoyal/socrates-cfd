"""Deterministic verifier: static checks + sensitivity checks + aggregation.

Input is a *run graph*: the root run (the simulation under verification)
plus any experiment runs launched from it.  The verifier never launches
runs; it only judges the evidence it is given.  Its verdict is
deterministic and is also used by the adaptive loop as a hard constraint
on the critic (the critic may not ACCEPT what the verifier cannot support,
nor ignore a FAIL).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..case_generation.spec import CaseConfig, ProblemSpec
from .base import CheckResult, Status, load_config
from .sensitivity import assess_sequence
from .static import run_static_checks, statistical_uncertainty

COMPONENTS = ("averaging", "statistics", "mesh", "time", "domain")
# which experiment primitive can produce evidence for which component
COMPONENT_TO_ACTION = {
    "averaging": "RUN_LONGER",
    "statistics": "RUN_LONGER",
    "mesh": "REFINE_MESH",
    "time": "REDUCE_TIME_STEP",
    "domain": "EXPAND_DOMAIN",
}
FACTOR_ACTIONS = {"mesh": "REFINE_MESH", "time": "REDUCE_TIME_STEP", "domain": "EXPAND_DOMAIN"}


@dataclass
class RunNode:
    run_id: str
    config: CaseConfig
    evidence: dict
    parent: str | None = None
    action: str | None = None  # experiment primitive that created it
    ok: bool = True


@dataclass
class Verdict:
    verdict: str  # ACCEPT | REJECT | INCONCLUSIVE
    checks: list[CheckResult]
    per_qoi: dict
    missing_components: dict = field(default_factory=dict)
    failed_checks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "per_qoi": self.per_qoi,
            "missing_components": self.missing_components,
            "failed_checks": self.failed_checks,
            "checks": [c.to_dict() for c in self.checks],
        }


def _formal_order_space(cfg: CaseConfig) -> float:
    s = cfg.numerics.div_U.replace("bounded", "").split()
    # 'Gauss upwind' is first order; linearUpwind/linear/limited* are (nominally) second
    return 1.0 if len(s) >= 2 and s[1] == "upwind" else 2.0


def _formal_order_time(cfg: CaseConfig) -> float | None:
    """Formal temporal order of the ddt scheme; None if not time-accurate / unknown."""
    toks = cfg.numerics.ddt.replace("bounded", "").split()
    if not toks:
        return None
    name = toks[0]
    if name == "Euler":
        return 1.0
    if name == "backward":
        return 2.0
    if name == "CrankNicolson":
        try:
            psi = float(toks[1])
        except (IndexError, ValueError):
            return None
        return 2.0 if psi >= 1.0 else 1.0  # psi < 1 blends in Euler: formally first order
    return None  # localEuler, steadyState, unknown: no temporal-accuracy claim possible


class RunGraph:
    def __init__(self, nodes: list[RunNode], root: str):
        self.nodes = {n.run_id: n for n in nodes}
        self.root = root

    def children(self, rid: str, action: str | None = None) -> list[RunNode]:
        return [n for n in self.nodes.values() if n.parent == rid and (action is None or n.action == action)]

    def longest_same_config(self, rid: str) -> RunNode:
        """Follow RUN_LONGER edges to the longest completed continuation."""
        best = self.nodes[rid]
        frontier = [best]
        while frontier:
            n = frontier.pop()
            for c in self.children(n.run_id, "RUN_LONGER"):
                if c.ok:
                    frontier.append(c)
                    if c.config.time.end_time > best.config.time.end_time:
                        best = c
        return best

    def same_config_class(self, rid: str) -> list[str]:
        """A run and all its completed RUN_LONGER continuations (one numerical set-up)."""
        out, frontier = [rid], [rid]
        while frontier:
            n = frontier.pop()
            for c in self.children(n, "RUN_LONGER"):
                if c.ok and c.run_id not in out:
                    out.append(c.run_id)
                    frontier.append(c.run_id)
        return out

    def factor_family(self, factor: str) -> list[RunNode]:
        """Root followed by runs reached via repeated ``factor`` primitives (ordered coarse->fine).

        Children of a RUN_LONGER continuation belong to the same level as its
        source (same numerical set-up), so traversal starts from the whole
        same-config class of every member.  Each member is represented by its
        longest continuation; members at an identical refinement level are
        collapsed (the most recent one is kept).
        """
        action = FACTOR_ACTIONS[factor]
        members = [self.longest_same_config(self.root)]
        frontier = list(self.same_config_class(self.root))
        seen = set(frontier)
        while frontier:
            rid = frontier.pop()
            for c in self.children(rid, action):
                if c.run_id in seen or not c.ok:
                    continue
                cls = self.same_config_class(c.run_id)
                seen.update(cls)
                members.append(self.longest_same_config(c.run_id))
                frontier.extend(cls)
        root = members[0]
        by_level: dict[float, RunNode] = {}
        for n in members[1:]:
            sz = _size(factor, n)
            if sz is None:
                continue
            key = round(sz, 9)
            if abs(key - round(_size(factor, root) or -1, 9)) < 1e-12:
                continue  # same level as the root: no information about this factor
            by_level[key] = n  # later members replace earlier ones at the same level
        rest = sorted(by_level.values(), key=lambda n: -(_size(factor, n) or 0.0))
        return [root] + rest


def _size(factor: str, n: RunNode) -> float | None:
    if factor == "mesh":
        return (n.evidence.get("mesh") or {}).get("representative_cell_size_D")
    if factor == "time":
        return n.config.time.delta_t
    return 1.0 / n.config.domain.half_height


def _stationary(n: RunNode, q: str):
    return ((n.evidence.get("qoi") or {}).get("stationary") or {}).get(q)


def sensitivity_checks(graph: RunGraph, spec: ProblemSpec, vcfg: dict) -> list[CheckResult]:
    out: list[CheckResult] = []
    root = graph.nodes[graph.root]
    for factor in ("mesh", "time", "domain"):
        fam = graph.factor_family(factor)
        for q in spec.requested_outputs:
            tau = spec.verification.requested_tolerance.get(q)
            if tau is None:
                continue
            name = f"{factor}_sensitivity"
            if len(fam) < 2:
                out.append(CheckResult(name, Status.INCONCLUSIVE,
                                       f"no {FACTOR_ACTIONS[factor]} experiment has been run; {factor} error of {q} is unknown",
                                       qoi=q, component=factor, runs=[root.run_id]))
                continue
            values = [_stationary(n, q) for n in fam]
            sizes = [_size(factor, n) for n in fam]
            # every member must itself be a statistically reliable estimate
            frac = vcfg["error_budget"]["component_pass_fraction"]
            min_cyc = vcfg["statistics"]["min_cycles"]
            unreliable = []
            for n in fam:
                sw = ((n.evidence.get("forces") or {}).get("stationary_window") or {})
                u, _ = statistical_uncertainty(n.evidence, q)
                if (sw.get("n_cycles") or 0) < min_cyc or u is None or u > frac * tau:
                    unreliable.append((n.run_id, sw.get("n_cycles"), u))
            if unreliable:
                out.append(CheckResult(name, Status.INCONCLUSIVE,
                                       f"family member(s) not statistically reliable for {q} "
                                       f"(run, cycles, uncertainty): {unreliable}; run them longer first",
                                       qoi=q, component=factor, runs=[n.run_id for n in fam],
                                       details={"unreliable_members": [u[0] for u in unreliable]}))
                continue
            noise = max((statistical_uncertainty(n.evidence, q)[0] or 0.0) for n in fam)
            notes = []
            if factor == "mesh":
                order = _formal_order_space(root.config)
                dts = {n.config.time.delta_t for n in fam}
                if len(dts) > 1:
                    notes.append(f"time step also varied across the mesh family: {sorted(dts)} (Courant control)")
            elif factor == "time":
                order = _formal_order_time(root.config)
                if order is None:
                    out.append(CheckResult(name, Status.INCONCLUSIVE,
                                           f"time scheme '{root.config.numerics.ddt}' has no known formal order of "
                                           "accuracy; temporal error cannot be estimated", qoi=q, component=factor,
                                           runs=[n.run_id for n in fam]))
                    continue
            else:
                order = vcfg["sensitivity"]["domain_error_order"]
                notes.append("domain-size error assumed ~ (D/H)^q with q=1 (EXPERT REVIEW)")
            if any(v is None for v in values):
                missing = [n.run_id for n, v in zip(fam, values) if v is None]
                out.append(CheckResult(name, Status.INCONCLUSIVE,
                                       f"{q} not available for runs {missing} (no stationary periodic state)",
                                       qoi=q, component=factor, runs=[n.run_id for n in fam]))
                continue
            out.append(assess_sequence(
                check=name, component=factor, qoi=q, values=values, sizes=sizes,
                run_ids=[n.run_id for n in fam], formal_order=order, tau=tau, cfg=vcfg,
                noise=noise, notes=notes, factor_label={"mesh": "h_D", "time": "dt_convective", "domain": "inverse_half_height"}[factor],
            ))
    return out


def best_static_evidence(graph: RunGraph) -> dict:
    """Root evidence, with statistics taken from its longest same-config continuation."""
    root = graph.nodes[graph.root]
    longest = graph.longest_same_config(graph.root)
    if longest.run_id == root.run_id:
        return root.evidence
    ev = dict(root.evidence)
    ev["forces"] = longest.evidence.get("forces")
    ev["temporal_behavior"] = dict(longest.evidence.get("temporal_behavior") or {})
    ev["temporal_behavior"]["declared_averaging_start_convective"] = root.config.averaging.start_time
    ev["qoi"] = {"reported": (root.evidence.get("qoi") or {}).get("reported"),
                 "stationary": (longest.evidence.get("qoi") or {}).get("stationary")}
    return ev


def verify(graph: RunGraph, spec: ProblemSpec, vcfg: dict | None = None, *, use_sensitivity: bool = True) -> Verdict:
    vcfg = vcfg or load_config()
    root = graph.nodes[graph.root]
    checks = run_static_checks(root.evidence, spec, vcfg)
    # statistics/averaging re-evaluated on the longest continuation if one exists
    longest = graph.longest_same_config(graph.root)
    if longest.run_id != root.run_id:
        ev = best_static_evidence(graph)
        from .static import check_averaging_window, check_statistics

        checks = [c for c in checks if c.component not in ("averaging", "statistics")]
        for c in check_averaging_window(ev, spec, vcfg) + check_statistics(ev, spec, vcfg):
            c.runs = [root.run_id, longest.run_id]
            checks.append(c)
    for c in checks:
        if not c.runs:
            c.runs = [root.run_id]
    if use_sensitivity:
        checks += sensitivity_checks(graph, spec, vcfg)
    return aggregate(checks, spec)


def aggregate(checks: list[CheckResult], spec: ProblemSpec) -> Verdict:
    failed = [f"{c.check}" + (f"[{c.qoi}]" if c.qoi else "") for c in checks if c.status == Status.FAIL]
    gates = [c for c in checks if c.component is None]
    per_qoi: dict = {}
    missing: dict = {}
    for q in spec.requested_outputs:
        tau = spec.verification.requested_tolerance.get(q)
        comp_res = {}
        for comp in COMPONENTS:
            cs = [c for c in checks if c.qoi == q and c.component == comp]
            comp_res[comp] = cs[-1] if cs else None
        statuses = {k: (v.status.value if v else "MISSING") for k, v in comp_res.items()}
        us = {k: v.uncertainty for k, v in comp_res.items() if v is not None and v.uncertainty is not None}
        need = [k for k, v in comp_res.items() if v is None or v.status != Status.PASS]
        # measured biases add linearly; independent uncertainties combine by root-sum-square
        bias = sum(us[k] for k, v in comp_res.items()
                   if v is not None and k in us and (v.details or {}).get("kind") == "bias")
        rss = math.sqrt(sum(us[k] ** 2 for k, v in comp_res.items()
                            if v is not None and k in us and (v.details or {}).get("kind") != "bias"))
        u_total = (bias + rss) if not need else None
        if any(v is not None and v.status == Status.FAIL for v in comp_res.values()):
            qv = "REJECT"
        elif not need and u_total is not None and u_total <= tau:
            qv = "ACCEPT"
        else:
            qv = "INCONCLUSIVE"
        per_qoi[q] = {"verdict": qv, "tolerance": tau, "component_status": statuses,
                      "component_uncertainty": us, "combined_uncertainty": u_total}
        if need:
            missing[q] = need
    mesh_ok_all = all(v["component_status"].get("mesh") == "PASS" for v in per_qoi.values())
    time_ok_all = all(v["component_status"].get("time") == "PASS" for v in per_qoi.values())

    def gate_pass(c: CheckResult) -> bool:
        if c.status == Status.PASS:
            return True
        # policy concerns that measured evidence can discharge
        if c.check == "courant_number" and c.status == Status.INCONCLUSIVE:
            return time_ok_all
        if c.check == "convection_scheme_order" and c.status == Status.INCONCLUSIVE:
            return mesh_ok_all
        return False

    gate_ok = all(gate_pass(c) for c in gates)
    if failed:
        verdict = "REJECT"
    elif gate_ok and all(v["verdict"] == "ACCEPT" for v in per_qoi.values()):
        verdict = "ACCEPT"
    else:
        verdict = "INCONCLUSIVE"
    return Verdict(verdict, checks, per_qoi, missing, failed)
