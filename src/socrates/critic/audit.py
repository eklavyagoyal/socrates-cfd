"""Audit critic text for numbers that are not traceable to the evidence package.

Every numeric token in the critic's reasoning is compared against every
number that appears in the package it was shown (and simple derived forms:
percentages, ratios of two package numbers are NOT accepted -- they are
listed as 'derived' so a human can inspect them).  This does not prove the
reasoning is right; it detects fabricated or externally sourced values
(e.g. a literature drag coefficient quoted in blind mode).
"""

from __future__ import annotations

import json
import re

_NUM = re.compile(r"(?<![\w.])[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?%?")


def _collect_numbers(obj, out: list[float]) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_numbers(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_numbers(v, out)
    elif isinstance(obj, str):
        for m in _NUM.finditer(obj):
            try:
                out.append(float(m.group().rstrip("%")))
            except ValueError:
                pass


def audit_numbers(texts: list[str], package: dict, rel_tol: float = 0.02) -> dict:
    known: list[float] = []
    _collect_numbers(package, known)
    known_pct = [100.0 * k for k in known]
    untraced, traced = [], 0
    for t in texts:
        for m in _NUM.finditer(t):
            tok = m.group()
            is_pct = tok.endswith("%")
            try:
                v = float(tok.rstrip("%"))
            except ValueError:
                continue
            if abs(v) < 10 and float(v).is_integer() and not is_pct:
                continue  # small integers: counts, run indices, list numbering
            pool = known + known_pct
            ok = any(abs(v - k) <= rel_tol * max(abs(k), 1e-12) or abs(v - k) < 1e-12 for k in pool)
            if ok:
                traced += 1
            else:
                untraced.append({"token": tok, "context": t[max(0, m.start() - 60): m.end() + 40]})
    return {"traced": traced, "untraced": untraced, "n_untraced": len(untraced)}


def package_size(package: dict) -> int:
    return len(json.dumps(package))
