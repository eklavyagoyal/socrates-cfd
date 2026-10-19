"""Load the baseline and adversarial case definitions.

Adversarial cases are stored as *diffs* against the baseline, so exactly
what was modified is explicit and machine-readable.  When a diff changes
domain extents without giving far-field cell counts, the counts are
recomputed so that the near-field mesh stays identical to the baseline
(only cells are added/removed far away) -- otherwise a domain flaw would
be confounded with a resolution change.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .blockmesh import expanded_domain_counts
from .spec import CaseConfig

REPO = Path(__file__).resolve().parents[3]
BASELINE = REPO / "cases" / "baseline" / "baseline.yaml"
ADVERSARIAL_DIR = REPO / "cases" / "adversarial"


def load_baseline() -> CaseConfig:
    return CaseConfig.from_yaml(BASELINE)


def apply_case_diff(base: CaseConfig, changes: dict, name: str) -> CaseConfig:
    changes = dict(changes)
    dom_keys = {"domain.upstream", "domain.downstream", "domain.half_height"}
    count_keys = {"mesh.n_upstream", "mesh.n_downstream", "mesh.n_lateral"}
    if dom_keys & set(changes) and not (count_keys & set(changes)):
        d = base.domain
        new = (
            changes.get("domain.upstream", d.upstream),
            changes.get("domain.downstream", d.downstream),
            changes.get("domain.half_height", d.half_height),
        )
        changes.update(expanded_domain_counts(base, *new))
    return base.with_changes(changes, name=name)


def load_case_definition(path: str | Path) -> tuple[CaseConfig, dict]:
    meta = yaml.safe_load(Path(path).read_text())
    base = load_baseline()
    cfg = apply_case_diff(base, meta.get("changes", {}), meta["id"])
    cfg = cfg.model_copy(update={"description": meta.get("title", "")})
    return cfg, meta


def list_adversarial() -> list[Path]:
    return sorted(ADVERSARIAL_DIR.glob("*.yaml"))
