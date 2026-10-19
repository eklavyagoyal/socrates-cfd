"""Critic schema, numeric audit, authority enforcement in the loop (with a scripted fake LLM)."""

import pytest
from pydantic import ValidationError

from socrates.critic.audit import audit_numbers
from socrates.critic.schema import CriticDecision, json_schema


def test_schema_accepts_valid_decision():
    d = CriticDecision.model_validate({
        "decision": "MORE_EVIDENCE", "confidence": "LOW",
        "reasoning_summary": ["mesh independence not shown"], "missing_evidence": ["mesh"], "hypotheses": [],
        "next_experiment": {"action": "REFINE_MESH", "parameters": {"factor": 1.5}, "parent_run": "r0",
                            "reason": "x", "expected_outcome": "y"}})
    assert d.next_experiment.action == "REFINE_MESH"


@pytest.mark.parametrize("bad", [
    {"decision": "MAYBE", "confidence": "LOW", "reasoning_summary": []},
    {"decision": "ACCEPT", "confidence": "LOW", "reasoning_summary": [], "extra": 1},
    {"decision": "MORE_EVIDENCE", "confidence": "LOW", "reasoning_summary": [],
     "next_experiment": {"action": "RUN_SHELL", "parameters": {}, "parent_run": "r", "reason": "x"}},
])
def test_schema_rejects_invalid(bad):
    with pytest.raises(ValidationError):
        CriticDecision.model_validate(bad)


def test_json_schema_menu_is_closed():
    s = json_schema()
    enum = s["properties"]["next_experiment"]["anyOf"][1]["properties"]["action"]["enum"]
    assert set(enum) == {"REFINE_MESH", "REDUCE_TIME_STEP", "EXPAND_DOMAIN", "RUN_LONGER"}


def test_audit_flags_untraceable_numbers():
    pkg = {"runs": [{"cd": 1.2951, "st": 0.15561}]}
    a = audit_numbers(["Cd is 1.2951 and St 0.1556", "literature gives 1.33"], pkg)
    assert a["n_untraced"] == 1 and a["untraced"][0]["token"] == "1.33"


def test_audit_accepts_percentages_of_package_fractions():
    a = audit_numbers(["change of 2.5%"], {"change": 0.025})
    assert a["n_untraced"] == 0
