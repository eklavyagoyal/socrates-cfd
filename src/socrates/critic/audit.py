"""Audit critic text for numbers that are not traceable to the evidence package.

Each numeric token is matched at its *printed precision*: "1.33" matches a
package value v only if |v - 1.33| <= 0.005; "5.88e-05" uses half a unit of its
last mantissa digit.  Percent tokens are compared with 100 x package values;
plain tokens only with package values (no percent expansion, which made
almost any 3-digit number 'traceable').  The pool of known numbers excludes
the critic's own previous decisions, so a value it invented earlier cannot
become 'traced' by repetition.

Limitations: a fabricated or remembered value that happens to coincide with a
recorded value at printed precision is not detected; the audit detects
untraceable numbers, it does not prove the reasoning right.
"""

from __future__ import annotations

import json
import math
import re

_NUM = re.compile(r"(?<![\w.])[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?%?")
EXCLUDED_KEYS = {"previous_critic_decisions"}


def _collect_numbers(obj, out: list[float]) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        if math.isfinite(obj):
            out.append(float(obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in EXCLUDED_KEYS:
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


def _half_unit(token: str) -> float:
    """Half a unit in the last printed digit of a numeric token."""
    t = token.rstrip("%").lstrip("+-")
    mant, _, exp = t.partition("e") if "e" in t else t.partition("E")
    decimals = len(mant.split(".")[1]) if "." in mant else 0
    e = int(exp) if exp else 0
    return 0.5 * 10.0 ** (e - decimals)


def audit_numbers(texts: list[str], package: dict, rel_tol: float | None = None) -> dict:
    known: list[float] = []
    _collect_numbers(package, known)
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
            tol = _half_unit(tok) * (1 + 1e-9)
            pool = [100.0 * k for k in known] if is_pct else known
            if any(abs(abs(v) - abs(k)) <= tol for k in pool):
                traced += 1
            else:
                untraced.append({"token": tok, "context": t[max(0, m.start() - 60): m.end() + 40]})
    return {"traced": traced, "untraced": untraced, "n_untraced": len(untraced)}


def package_size(package: dict) -> int:
    return len(json.dumps(package))
