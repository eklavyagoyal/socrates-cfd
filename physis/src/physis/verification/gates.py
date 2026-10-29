"""Validation gates (ADR-0003).

A *gate* compares a solver capability against an external reference (analytic solution,
published benchmark) with criteria fixed before the run. Every gate run writes
``validation/results/<gate>.json``; ``scripts/validation_report.py`` turns them into
``docs/validation.md``. A capability counts as validated only while its gate passes on
the current code (the record carries the source fingerprint, so a stale PASS is visible).

Usage (inside a ``@pytest.mark.validation`` test, via the ``gate`` fixture)::

    g = gate("lbm.poiseuille2d", capability="lbm.d2q9.bounce_back",
             reference={"source": "analytic plane Poiseuille", "values": {...}})
    g.metric("l2_error", e)
    g.check("observed_order", p, ">=", 1.8)
    g.finish()   # writes the record; fails the test if any check failed
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from physis.core.provenance import REPO_ROOT, environment, git_state, source_fingerprint

RESULTS_DIR = REPO_ROOT / "validation" / "results"

_OPS = {
    "<=": lambda v, lim: v <= lim,
    "<": lambda v, lim: v < lim,
    ">=": lambda v, lim: v >= lim,
    ">": lambda v, lim: v > lim,
    "==": lambda v, lim: v == lim,
}


class GateFailure(AssertionError):
    pass


@dataclass
class Gate:
    name: str
    capability: str
    reference: dict[str, Any]
    code_subpackage: str = ""
    backend: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    checks: list[dict[str, Any]] = field(default_factory=list)
    started: float = field(default_factory=time.time)
    finished: bool = False

    def metric(self, name: str, value: Any) -> None:
        self.metrics[name] = _clean(value)

    def note(self, text: str) -> None:
        self.notes.append(text)

    def check(self, name: str, value: float, op: str, limit: float) -> bool:
        if op not in _OPS:
            raise ValueError(f"unknown op {op!r}")
        v = float(value)
        ok = bool(math.isfinite(v) and _OPS[op](v, float(limit)))
        self.checks.append({"name": name, "value": v, "op": op, "limit": float(limit), "pass": ok})
        return ok

    @property
    def passed(self) -> bool:
        return bool(self.checks) and all(c["pass"] for c in self.checks)

    def record(self, status: str | None = None, error: str | None = None) -> dict[str, Any]:
        return {
            "gate": self.name,
            "capability": self.capability,
            "status": status or ("PASS" if self.passed else "FAIL"),
            "reference": self.reference,
            "metrics": self.metrics,
            "checks": self.checks,
            "notes": self.notes,
            "error": error,
            "backend": self.backend,
            "code": {
                "subpackage": self.code_subpackage,
                "fingerprint": source_fingerprint(self.code_subpackage),
                **git_state(),
            },
            "environment": environment(),
            "wall_time_s": round(time.time() - self.started, 3),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }

    def write(self, status: str | None = None, error: str | None = None) -> Path:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        path = RESULTS_DIR / f"{self.name}.json"
        path.write_text(json.dumps(self.record(status, error), indent=1, sort_keys=False, allow_nan=True) + "\n")
        return path

    def finish(self) -> None:
        self.finished = True
        self.write()
        if not self.passed:
            failed = [c for c in self.checks if not c["pass"]]
            raise GateFailure(f"gate {self.name} failed: {failed}" if failed else f"gate {self.name} has no checks")


def _clean(v: Any) -> Any:
    if isinstance(v, dict):
        return {str(k): _clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_clean(x) for x in v]
    if hasattr(v, "item") and callable(v.item) and getattr(v, "ndim", 1) == 0:
        return v.item()
    if hasattr(v, "tolist"):
        return v.tolist()
    return v
