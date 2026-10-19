"""Authority enforcement in the adaptive loop, with a scripted planner and a fake run store."""

from dataclasses import dataclass, field

import pytest

import socrates.orchestration.loop as loop_mod
from socrates.case_generation.catalog import load_baseline
from socrates.case_generation.spec import ProblemSpec
from socrates.checks.verifier import Verdict
from socrates.critic.schema import CriticDecision
from socrates.orchestration.loop import Budget, run_adaptive

SPEC = ProblemSpec.from_yaml("configs/problem_cylinder_re100.yaml")
EV = {"solver": {"log_found": True, "completed": True, "courant_max": 0.7},
      "temporal_behavior": {"oscillating": True}, "forces": {"stationary_window": {"n_cycles": 10}},
      "cost": {"cell_steps": 1e8, "wall_seconds": 100.0}}


@dataclass
class FakeRun:
    run_id: str
    config: object
    evidence: dict
    status: str = "completed"
    provenance: dict = field(default_factory=dict)

    @property
    def ok(self):
        return True


class FakeStore:
    def __init__(self):
        self.runs = {"root": FakeRun("root", load_baseline(), EV)}
        self.executed = []

    def load(self, rid):
        return self.runs[rid]

    def get_or_run(self, cfg, spec, **kw):
        rid = f"child{len(self.executed)}"
        self.executed.append((rid, kw.get("experiment", {}).get("action")))
        self.runs[rid] = FakeRun(rid, cfg, dict(EV, cost={"cell_steps": 1e8}), provenance={"wall_seconds": 1.0})
        return self.runs[rid]


class Scripted:
    name = "scripted"

    def __init__(self, decisions):
        self.decisions = list(decisions)
        self.feedback = []

    def decide(self, spec, graph, verdict, history, menu, budget, feedback):
        self.feedback.append(feedback)
        d = self.decisions.pop(0) if self.decisions else None
        return (CriticDecision.model_validate(d) if d else None), {"planner": self.name}


def _verdicts(seq):
    it = iter(seq)

    def fake_verify(graph, spec, vcfg=None, **kw):
        v = next(it, seq[-1])
        return Verdict(v, [], {}, {"mean_drag_coefficient": ["mesh"]} if v == "INCONCLUSIVE" else {}, [])

    return fake_verify


def _more(action="REFINE_MESH", params=None, parent="root"):
    return {"decision": "MORE_EVIDENCE", "confidence": "LOW", "reasoning_summary": ["x"],
            "next_experiment": {"action": action, "parameters": params or {}, "parent_run": parent,
                                "reason": "r", "expected_outcome": "o"}}


def test_decisive_verdict_stops_without_planner(monkeypatch):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["REJECT"]))
    p = Scripted([])
    res = run_adaptive("root", FakeStore(), SPEC, p, Budget(), vcfg={})
    assert res.final_verdict == "REJECT" and p.feedback == []


def test_unsupported_accept_is_not_executed(monkeypatch):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["INCONCLUSIVE", "INCONCLUSIVE", "ACCEPT"]))
    accept = {"decision": "ACCEPT", "confidence": "HIGH", "reasoning_summary": ["looks fine"]}
    store = FakeStore()
    p = Scripted([accept, _more()])
    res = run_adaptive("root", store, SPEC, p, Budget(), vcfg={})
    assert len(res.authority_violations) == 1
    assert "ACCEPT" in (p.feedback[1] or "")  # feedback given on the second call
    assert store.executed == [("child0", "REFINE_MESH")]
    assert res.final_verdict == "ACCEPT"  # reached only through the deterministic verdict


def test_invalid_action_rejected_with_feedback(monkeypatch):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["INCONCLUSIVE"]))
    store = FakeStore()
    p = Scripted([_more(params={"factor": 9.0}), _more(parent="nope"), _more(params={"factor": 1.0})])
    res = run_adaptive("root", store, SPEC, p, Budget(max_invalid_actions=3), vcfg={})
    assert store.executed == []
    assert res.final_verdict == "INCONCLUSIVE" and "invalid" in res.stop_reason
    assert "rejected by the validator" in (p.feedback[1] or "")


def test_experiment_budget_gives_inconclusive(monkeypatch):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["INCONCLUSIVE"]))
    store = FakeStore()
    p = Scripted([_more("REDUCE_TIME_STEP", {"factor": 2}), _more("EXPAND_DOMAIN", {"factor": 2}), _more()])
    res = run_adaptive("root", store, SPEC, p, Budget(max_experiments=2), vcfg={})
    assert len(store.executed) == 2
    assert res.final_verdict == "INCONCLUSIVE" and res.stop_reason == "experiment budget exhausted"


def test_planner_may_give_up(monkeypatch):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["INCONCLUSIVE"]))
    stop = {"decision": "MORE_EVIDENCE", "confidence": "LOW", "reasoning_summary": ["nothing affordable"],
            "next_experiment": None}
    res = run_adaptive("root", FakeStore(), SPEC, Scripted([stop]), Budget(), vcfg={})
    assert res.final_verdict == "INCONCLUSIVE" and res.stop_reason == "planner stopped"


@pytest.mark.parametrize("review,expected", [({"concur": True}, "ACCEPT"),
                                             ({"concur": False, "blocking_concerns": [{"concern": "x"}]}, "INCONCLUSIVE"),
                                             ({"failure": "boom"}, "INCONCLUSIVE")])
def test_acceptance_review_can_only_downgrade(monkeypatch, review, expected):
    monkeypatch.setattr(loop_mod, "verify", _verdicts(["ACCEPT"]))
    p = Scripted([])
    p.review = lambda *a, **k: review
    res = run_adaptive("root", FakeStore(), SPEC, p, Budget(), vcfg={}, acceptance_review=True)
    assert res.final_verdict == expected
