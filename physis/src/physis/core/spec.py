"""Specs: immutable, validated, canonically serialisable problem descriptions.

Every simulation, geometry or dataset request is a :class:`Spec`. Its canonical JSON
(sorted keys, no whitespace, floats via ``repr``) is what gets hashed for the run store,
so two specs that mean the same thing hash the same.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(obj: Any) -> str:
    """sha256 hex of the canonical JSON of ``obj``."""
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


class Spec(BaseModel):
    """Base class for all specs: frozen, no unknown fields."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    def canonical(self) -> dict:
        return self.model_dump(mode="json")

    def digest(self) -> str:
        return digest(self.canonical())
