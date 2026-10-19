"""Structured critic output (validated; anything else is rejected)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..experiments.primitives import ACTION_SPECS


class NextExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["REFINE_MESH", "REDUCE_TIME_STEP", "EXPAND_DOMAIN", "RUN_LONGER"]
    parameters: dict[str, float] = Field(default_factory=dict)
    parent_run: str
    reason: str
    expected_outcome: str = ""


class Hypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hypothesis: str
    test: str


class CriticDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["ACCEPT", "REJECT", "MORE_EVIDENCE"]
    confidence: Literal["LOW", "MEDIUM", "HIGH"]
    reasoning_summary: list[str]
    missing_evidence: list[str] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    next_experiment: NextExperiment | None = None


def json_schema() -> dict:
    """JSON schema handed to the LLM backend for constrained decoding."""
    actions = sorted(ACTION_SPECS)
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["decision", "confidence", "reasoning_summary", "missing_evidence", "hypotheses", "next_experiment"],
        "properties": {
            "decision": {"type": "string", "enum": ["ACCEPT", "REJECT", "MORE_EVIDENCE"]},
            "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
            "reasoning_summary": {"type": "array", "items": {"type": "string"}},
            "missing_evidence": {"type": "array", "items": {"type": "string"}},
            "hypotheses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["hypothesis", "test"],
                    "properties": {"hypothesis": {"type": "string"}, "test": {"type": "string"}},
                },
            },
            "next_experiment": {
                "anyOf": [
                    {"type": "null"},
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["action", "parameters", "parent_run", "reason", "expected_outcome"],
                        "properties": {
                            "action": {"type": "string", "enum": actions},
                            "parameters": {"type": "object", "additionalProperties": {"type": "number"}},
                            "parent_run": {"type": "string"},
                            "reason": {"type": "string"},
                            "expected_outcome": {"type": "string"},
                        },
                    },
                ]
            },
        },
    }
