"""Solver results: one container for every solver, so verification, storage, datasets
and the platform layer treat flow, heat and structure the same way."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch

from physis.core.grid import Grid


@dataclass
class SolverResult:
    """What a solver returns.

    - ``fields``: arrays on ``grid`` (e.g. ``ux``, ``uy``, ``p``, ``T``, ``disp_x``), shape
      ``grid.shape`` (vector fields as separate components).
    - ``scalars``: derived quantities of interest (``cd``, ``cl``, ``dp``, ``nu``,
      ``tip_deflection``...), in the units stated in ``units``.
    - ``series``: time or iteration histories, each a 1D array; ``series["t"]`` is the
      time axis for transient runs.
    - ``diagnostics``: steps, wall time, convergence flags, residuals, warnings. Never used
      as a quantity of interest.
    - ``units``: unit string per scalar/field name ("1" for dimensionless).
    """

    kind: str
    grid: Grid | None
    fields: dict[str, torch.Tensor] = field(default_factory=dict)
    scalars: dict[str, float] = field(default_factory=dict)
    series: dict[str, torch.Tensor] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    units: dict[str, str] = field(default_factory=dict)

    def arrays(self, *, field_dtype: np.dtype = np.float32) -> dict[str, np.ndarray]:
        """Flatten to named numpy arrays for storage.

        Fields are stored in ``field_dtype`` (float32 by default: storage, not
        computation); series keep float64 because convergence and frequency analysis
        read them.
        """
        out: dict[str, np.ndarray] = {}
        for name, t in self.fields.items():
            out[f"field/{name}"] = t.detach().cpu().numpy().astype(field_dtype, copy=False)
        for name, t in self.series.items():
            out[f"series/{name}"] = t.detach().cpu().numpy().astype(np.float64, copy=False)
        return out

    def meta(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "grid": self.grid.to_dict() if self.grid is not None else None,
            "scalars": {k: float(v) for k, v in self.scalars.items()},
            "diagnostics": _jsonable(self.diagnostics),
            "units": dict(self.units),
            "fields": sorted(self.fields),
            "series": sorted(self.series),
        }

    @classmethod
    def from_stored(cls, meta: dict[str, Any], arrays: dict[str, np.ndarray]) -> SolverResult:
        grid = Grid.from_dict(meta["grid"]) if meta.get("grid") else None
        fields = {k.split("/", 1)[1]: torch.from_numpy(v) for k, v in arrays.items() if k.startswith("field/")}
        series = {k.split("/", 1)[1]: torch.from_numpy(v) for k, v in arrays.items() if k.startswith("series/")}
        return cls(
            kind=meta["kind"],
            grid=grid,
            fields=fields,
            scalars=dict(meta.get("scalars", {})),
            series=series,
            diagnostics=dict(meta.get("diagnostics", {})),
            units=dict(meta.get("units", {})),
        )


def _jsonable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, torch.Tensor):
        return obj.detach().cpu().tolist()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    return obj
