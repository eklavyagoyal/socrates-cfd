"""Solver contract and registry.

A solver is a class with a ``kind`` (e.g. ``"lbm.channel2d"``), a spec type and a
``run(spec, backend) -> SolverResult`` method. It must:

- allocate only through the given :class:`~physis.core.backend.Backend`
  (no hard-coded device/dtype);
- be deterministic for a given spec, backend and code;
- report stability problems (NaN, divergence, Mach/CFL limits exceeded) in
  ``diagnostics`` *and* raise :class:`SolverDivergence` when the result is unusable,
  so a failed run is recorded as failed and never used as evidence (Socrates lesson:
  a diverged refinement must not be hidden as "not run").
"""

from __future__ import annotations

from typing import ClassVar, Protocol, TypeVar

from physis.core.backend import Backend
from physis.core.result import SolverResult
from physis.core.spec import Spec
from physis.core.store import RunStore


class SolverDivergence(RuntimeError):
    """The solver produced an unusable state (NaN/Inf, blow-up, stability limit violated)."""


class Solver(Protocol):
    kind: ClassVar[str]
    spec_type: ClassVar[type[Spec]]

    def run(self, spec: Spec, backend: Backend) -> SolverResult: ...


S = TypeVar("S", bound=type)

_REGISTRY: dict[str, type] = {}


def register(cls: S) -> S:
    kind = getattr(cls, "kind", None)
    if not kind:
        raise TypeError(f"{cls.__name__} has no 'kind'")
    if kind in _REGISTRY and _REGISTRY[kind] is not cls:
        raise ValueError(f"solver kind {kind!r} registered twice")
    _REGISTRY[kind] = cls
    return cls


def get(kind: str) -> type:
    return _REGISTRY[kind]


def kinds() -> list[str]:
    return sorted(_REGISTRY)


def run_stored(solver: Solver, spec: Spec, backend: Backend, store: RunStore | None = None,
               *, reuse: bool = True) -> tuple[str | None, SolverResult]:
    """Run through the store (content-addressed reuse) or directly if ``store`` is None."""
    if store is None:
        return None, solver.run(spec, backend)
    subpackage = type(solver).__module__.removeprefix("physis.").rsplit(".", 1)[0]
    return store.run(
        solver.kind,
        spec,
        lambda: solver.run(spec, backend),
        code_subpackage=subpackage,
        backend_info=backend.describe(),
        reuse=reuse,
    )
