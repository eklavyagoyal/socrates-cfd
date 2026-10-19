"""Check result types and configuration loading."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "configs" / "verification.yaml"


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass
class CheckResult:
    check: str
    status: Status
    reason: str
    value: Any = None
    threshold: Any = None
    source: str = ""
    qoi: str | None = None
    # error-budget component this check estimates (None for gate checks)
    component: str | None = None
    # estimated relative uncertainty of the *root* run's reported value
    uncertainty: float | None = None
    runs: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d


def load_config(path: str | Path | None = None) -> dict:
    return yaml.safe_load(Path(path or DEFAULT_CONFIG).read_text())


def thr(cfg: dict, *keys: str):
    """Fetch a threshold value (handles {value:, source:} entries)."""
    node: Any = cfg
    for k in keys:
        node = node[k]
    if isinstance(node, dict) and "value" in node:
        return node["value"], node.get("source", "")
    return node, ""
