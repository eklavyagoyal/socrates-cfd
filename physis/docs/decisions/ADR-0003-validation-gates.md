# ADR-0003: Validation gates before capability claims

**Status:** accepted (2026-10-27)

## Context
Self-built solvers are only worth something if their accuracy is demonstrated. Socrates
showed that solver diagnostics alone accept wrong results.

## Decision
Each solver capability has gates: tests marked `validation` that compare against an
external reference (analytic solution or published benchmark, source cited) with
criteria fixed in the test before running. Each run writes `validation/results/<gate>.json`
with the source fingerprint; `scripts/validation_report.py` builds `docs/validation.md`
and marks results produced by other code as STALE. A capability is validated only while
its gate passes on current code. Gates of a solver pass before dependent solvers build on it.

## Consequences
Development is slower per feature and honest about scope; docs state "validated" vs
"prototype" per capability.
