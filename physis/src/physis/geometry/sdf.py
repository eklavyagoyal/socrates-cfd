"""Signed-distance-field geometry, evaluated in torch (ADR-0002, ADR-0004).

Sign convention (same as Volyra): ``d < 0`` inside the solid, ``d = 0`` on the surface,
``d > 0`` outside. Points are tensors of shape ``(..., ndim)``; the result has shape
``(...)``. Every node is a pure function of its inputs, so evaluation works on any
device/dtype and is differentiable with autograd (shape gradients for optimisation).

Nodes serialise to plain dicts (``to_spec``) and back (``from_spec``) so a geometry can
be stored, hashed and sent over the API/MCP boundary.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, ClassVar

import torch

Tensor = torch.Tensor

_NODE_TYPES: dict[str, type[SDF]] = {}


def register_node(cls: type[SDF]) -> type[SDF]:
    name = cls.type_name
    if name in _NODE_TYPES and _NODE_TYPES[name] is not cls:
        raise ValueError(f"SDF node type {name!r} registered twice")
    _NODE_TYPES[name] = cls
    return cls


def from_spec(spec: dict[str, Any]) -> SDF:
    """Rebuild a geometry from ``to_spec`` output."""
    t = spec["type"]
    if t not in _NODE_TYPES:
        raise KeyError(f"unknown SDF node type {t!r}; known: {sorted(_NODE_TYPES)}")
    return _NODE_TYPES[t].from_spec(spec)


class SDF:
    """Base node. Subclasses implement ``eval``, ``to_spec``, ``from_spec`` and
    (where cheap) ``bounds``."""

    type_name: ClassVar[str] = ""
    ndim: int

    def __call__(self, p: Tensor) -> Tensor:
        if p.shape[-1] != self.ndim:
            raise ValueError(f"{self.type_name} is {self.ndim}D, got points of dim {p.shape[-1]}")
        return self.eval(p)

    def eval(self, p: Tensor) -> Tensor:
        raise NotImplementedError

    def bounds(self) -> tuple[tuple[float, ...], tuple[float, ...]] | None:
        """Conservative axis-aligned bounds of the solid, or None if unbounded/unknown."""
        return None

    def to_spec(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> SDF:
        raise NotImplementedError

    # --- composition sugar -----------------------------------------------------------

    def __or__(self, other: SDF) -> SDF:
        return Union([self, other])

    def __and__(self, other: SDF) -> SDF:
        return Intersection([self, other])

    def __sub__(self, other: SDF) -> SDF:
        return Difference(self, other)

    def translate(self, offset: Sequence[float]) -> SDF:
        return Translate(self, offset)


def _check_dim(children: Sequence[SDF]) -> int:
    dims = {c.ndim for c in children}
    if len(dims) != 1:
        raise ValueError(f"cannot combine geometries of different dimension {sorted(dims)}")
    return dims.pop()


def _vec(v: Sequence[float], n: int, name: str) -> tuple[float, ...]:
    t = tuple(float(x) for x in v)
    if len(t) != n:
        raise ValueError(f"{name} must have {n} components, got {len(t)}")
    return t


# --- primitives -------------------------------------------------------------------------


@register_node
class Ball(SDF):
    """Disc (2D) or sphere (3D)."""

    type_name = "ball"

    def __init__(self, center: Sequence[float], radius: float):
        self.center = tuple(float(c) for c in center)
        self.ndim = len(self.center)
        if self.ndim not in (2, 3):
            raise ValueError("ball center must be 2D or 3D")
        if not radius > 0:
            raise ValueError("radius must be > 0")
        self.radius = float(radius)

    def eval(self, p: Tensor) -> Tensor:
        c = p.new_tensor(self.center)
        return torch.linalg.vector_norm(p - c, dim=-1) - self.radius

    def bounds(self):
        return (tuple(c - self.radius for c in self.center), tuple(c + self.radius for c in self.center))

    def to_spec(self):
        return {"type": self.type_name, "center": list(self.center), "radius": self.radius}

    @classmethod
    def from_spec(cls, s):
        return cls(s["center"], s["radius"])


@register_node
class Box(SDF):
    """Axis-aligned box (rectangle in 2D) given by centre and half extents."""

    type_name = "box"

    def __init__(self, center: Sequence[float], half_extents: Sequence[float]):
        self.center = tuple(float(c) for c in center)
        self.ndim = len(self.center)
        self.half = _vec(half_extents, self.ndim, "half_extents")
        if any(h <= 0 for h in self.half):
            raise ValueError("half extents must be > 0")

    def eval(self, p: Tensor) -> Tensor:
        q = (p - p.new_tensor(self.center)).abs() - p.new_tensor(self.half)
        outside = torch.linalg.vector_norm(q.clamp(min=0), dim=-1)
        inside = q.max(dim=-1).values.clamp(max=0)
        return outside + inside

    def bounds(self):
        return (
            tuple(c - h for c, h in zip(self.center, self.half)),
            tuple(c + h for c, h in zip(self.center, self.half)),
        )

    def to_spec(self):
        return {"type": self.type_name, "center": list(self.center), "half_extents": list(self.half)}

    @classmethod
    def from_spec(cls, s):
        return cls(s["center"], s["half_extents"])


# --- booleans ---------------------------------------------------------------------------


class _NAry(SDF):
    reduce: ClassVar[Callable[[Tensor], Tensor]]

    def __init__(self, children: Sequence[SDF]):
        if len(children) < 1:
            raise ValueError(f"{self.type_name} needs at least one child")
        self.children = list(children)
        self.ndim = _check_dim(self.children)

    def to_spec(self):
        return {"type": self.type_name, "children": [c.to_spec() for c in self.children]}

    @classmethod
    def from_spec(cls, s):
        return cls([from_spec(c) for c in s["children"]])


@register_node
class Union(_NAry):
    type_name = "union"

    def eval(self, p):
        return torch.stack([c(p) for c in self.children], dim=0).min(dim=0).values

    def bounds(self):
        bs = [c.bounds() for c in self.children]
        if any(b is None for b in bs):
            return None
        lo = tuple(min(b[0][i] for b in bs) for i in range(self.ndim))
        hi = tuple(max(b[1][i] for b in bs) for i in range(self.ndim))
        return lo, hi


@register_node
class Intersection(_NAry):
    type_name = "intersection"

    def eval(self, p):
        return torch.stack([c(p) for c in self.children], dim=0).max(dim=0).values

    def bounds(self):
        bs = [b for b in (c.bounds() for c in self.children) if b is not None]
        if not bs:
            return None
        lo = tuple(max(b[0][i] for b in bs) for i in range(self.ndim))
        hi = tuple(min(b[1][i] for b in bs) for i in range(self.ndim))
        return lo, hi


@register_node
class Difference(SDF):
    """``base`` minus ``cut``: ``max(d_base, -d_cut)``."""

    type_name = "difference"

    def __init__(self, base: SDF, cut: SDF):
        self.base, self.cut = base, cut
        self.ndim = _check_dim([base, cut])

    def eval(self, p):
        return torch.maximum(self.base(p), -self.cut(p))

    def bounds(self):
        return self.base.bounds()

    def to_spec(self):
        return {"type": self.type_name, "base": self.base.to_spec(), "cut": self.cut.to_spec()}

    @classmethod
    def from_spec(cls, s):
        return cls(from_spec(s["base"]), from_spec(s["cut"]))


# --- transforms -------------------------------------------------------------------------


@register_node
class Translate(SDF):
    type_name = "translate"

    def __init__(self, child: SDF, offset: Sequence[float]):
        self.child = child
        self.ndim = child.ndim
        self.offset = _vec(offset, self.ndim, "offset")

    def eval(self, p):
        return self.child(p - p.new_tensor(self.offset))

    def bounds(self):
        b = self.child.bounds()
        if b is None:
            return None
        return (
            tuple(x + o for x, o in zip(b[0], self.offset)),
            tuple(x + o for x, o in zip(b[1], self.offset)),
        )

    def to_spec(self):
        return {"type": self.type_name, "child": self.child.to_spec(), "offset": list(self.offset)}

    @classmethod
    def from_spec(cls, s):
        return cls(from_spec(s["child"]), s["offset"])
