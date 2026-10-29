"""Core contracts shared by every layer: backend, grid, specs, results, provenance, run store."""

from physis.core.backend import Backend, configure_threads, get_backend, resolve_device
from physis.core.grid import Grid
from physis.core.result import SolverResult
from physis.core.spec import Spec

__all__ = [
    "Backend",
    "Grid",
    "SolverResult",
    "Spec",
    "configure_threads",
    "get_backend",
    "resolve_device",
]
