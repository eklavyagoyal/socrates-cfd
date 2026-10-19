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


def test_llm_package_is_blind_to_case_names():
    """Regression (review finding): run ids embed case names such as 'B1_small_domain'."""
    import json
    from pathlib import Path

    from socrates.case_generation.spec import CaseConfig, ProblemSpec
    from socrates.checks.verifier import RunGraph, RunNode, verify
    from socrates.critic.prompt import alias_map, anonymize, build_package, render_user_prompt

    spec = ProblemSpec.from_yaml("configs/problem_cylinder_re100.yaml")
    runs = sorted(Path("results/runs").glob("B1_small_domain-*/run.json"))
    if not runs:
        import pytest
        pytest.skip("stored B1 run not available")
    prov = json.loads(runs[0].read_text())
    ev = json.loads((runs[0].parent / "evidence.json").read_text())
    rid = prov["run_id"]
    g = RunGraph([RunNode(rid, CaseConfig.model_validate(prov["case_config"]), ev)], rid)
    v = verify(g, spec)
    history = [{"outcome": f"executed -> {rid}", "next_experiment": {"parent_run": rid}}]
    menu = [{"action": "REFINE_MESH", "estimated_wall_seconds_by_parent": {rid: 100}}]
    text = render_user_prompt(anonymize(build_package(spec, g, v, history, menu, {}), alias_map(g)))
    for leak in (rid, "B1_", "small_domain", "small domain", "adversarial"):
        assert leak not in text, leak
    assert "R0" in text


def test_audit_printed_precision_and_no_percent_laundering():
    pkg = {"strouhal_frequency_resolution": 0.013333, "domain": 20.0, "cd": 1.2951,
           "previous_critic_decisions": [{"reasoning_summary": ["literature Cd 1.33"]}]}
    a = audit_numbers(["literature Cd = 1.33 (Williamson 1996)", "domain 20 D", "Cd 1.30", "1.3% resolution"], pkg)
    toks = sorted(u["token"] for u in a["untraced"])
    assert toks == ["1.33", "1996"], toks  # 1.30 matches 1.2951 at printed precision; 1.3% = 100*0.013333
