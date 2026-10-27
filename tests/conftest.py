"""Shared fixtures: thread limits, backends, validation-gate recorder."""

from __future__ import annotations

import os

import pytest

from physis.core.backend import configure_threads, get_backend
from physis.verification.gates import Gate

# Parallel test processes must not oversubscribe the CPU (see core/backend.py).
configure_threads(int(os.environ.get("PHYSIS_THREADS", "3")))


@pytest.fixture
def cpu64():
    """float64 on CPU: the validation backend."""
    return get_backend("validation", device="cpu")


@pytest.fixture
def cpu32():
    return get_backend("fast", device="cpu")


@pytest.fixture
def gate():
    """Factory for validation-gate records; writes an ERROR record if the test dies first."""
    made: list[Gate] = []

    def make(name: str, *, capability: str, reference: dict, code_subpackage: str = "",
             backend: dict | None = None) -> Gate:
        g = Gate(name=name, capability=capability, reference=reference,
                 code_subpackage=code_subpackage, backend=backend or {})
        made.append(g)
        return g

    yield make
    for g in made:
        if not g.finished:
            g.write(status="ERROR", error="test ended before gate.finish()")
