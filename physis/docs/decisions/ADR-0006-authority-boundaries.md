# ADR-0006: Authority boundaries for agents and LLMs

**Status:** accepted (2026-10-27)

## Context
Socrates (eklavyagoyal/socrates-cfd) measured that an LLM planner added no value over a
rule planner, LLM-issued verdicts carried no bounds, and an LLM review concurred with a
wrong geometry it had in its evidence.

## Decision
Agents (MCP clients, LLM planners) may create geometry, choose parameters and request
simulations through validated tools. Quantities of interest, verdicts, dataset labels and
accept/reject decisions come only from deterministic code. Every number an agent reports
must be traceable to a stored run.
