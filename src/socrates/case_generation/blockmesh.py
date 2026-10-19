r"""blockMeshDict generator for a 2D circular cylinder in a rectangular domain.

Topology (cylinder centre at the origin, all lengths in units of D)::

    y=+H  +---------+-----------+--------------------------+
          | c(0,2)  |   (1,2)   |          (2,2)           |
    y=+a  +---------S2---------S1--------------------------+
          |         | \ ringB / |                          |
          | (0,1)   |  ringA    |   (2,1)  wake block      |
          |  inlet  | / (cyl) \ |                          |
    y=-a  +---------S3---------S0--------------------------+
          | (0,0)   |   (1,0)   |          (2,0)           |
    y=-H  +---------+-----------+--------------------------+
        x=-Lu     x=-a        x=+a                       x=+Ld

* ring A: polar O-grid between the cylinder (r=0.5) and a circle r=r_mid,
  4 blocks, wall-normal grading set by ``first_cell``;
* ring B: from the circle r=r_mid to the square |x|,|y| <= a, 4 blocks;
* 8 rectangular far-field blocks, graded so cell size is continuous at the
  square and grows towards the far-field boundaries.

Systematic refinement: every cell count is multiplied by ``refinement``
while every block's total expansion ratio is held fixed, so all cell sizes
scale approximately by 1/refinement (geometric similarity, as required for
Richardson-type error estimation; Celik et al. 2008, J. Fluids Eng. 130).
Expansion ratios are computed once from the *base* (refinement=1) counts.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .spec import CaseConfig


def first_cell_from_ratio(length: float, n: int, ratio: float) -> float:
    """First cell size for ``n`` cells over ``length`` with total expansion ratio (last/first)."""
    if n == 1 or abs(ratio - 1.0) < 1e-12:
        return length / n
    g = ratio ** (1.0 / (n - 1))
    return length * (g - 1.0) / (g**n - 1.0)


def ratio_from_first_cell(length: float, n: int, first: float) -> float:
    """Total expansion ratio (last/first) giving first cell ``first`` for ``n`` cells over ``length``.

    Solved by bisection on the per-cell growth factor g.  Raises if the
    request is impossible (first cell larger than length).
    """
    if first <= 0 or first >= length:
        raise ValueError(f"first cell {first} incompatible with length {length}")
    if n == 1:
        return 1.0
    uniform = length / n

    def total(g: float) -> float:
        if abs(g - 1.0) < 1e-14:
            return first * n
        return first * (g**n - 1.0) / (g - 1.0)

    lo, hi = (1.0, 10.0) if first < uniform else (1e-6, 1.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (total(mid) < length) == (first < uniform):
            lo = mid
        else:
            hi = mid
    g = 0.5 * (lo + hi)
    return g ** (n - 1)


@dataclass(frozen=True)
class BlockLayout:
    """Resolved geometry, counts and gradings (all lengths in D)."""

    R: float
    r_mid: float
    a: float
    Lu: float
    Ld: float
    H: float
    span: float
    nq: int
    nra: int
    nrb: int
    nup: int
    ndn: int
    nlat: int
    E_ra: float
    E_rb: float
    E_up: float  # last/first going +x from inlet to -a  (< 1: fine at -a)
    E_dn: float  # going +x from +a to outlet (> 1)
    E_lat: float  # going outward from +a to +H (> 1)

    @property
    def n_cells(self) -> int:
        ring = 4 * self.nq * (self.nra + self.nrb)
        far = (self.nup + self.nq + self.ndn) * (2 * self.nlat + self.nq) - self.nq * self.nq
        return ring + far


def _scaled(n: int, f: float) -> int:
    return max(2, int(round(n * f)))


def resolve_layout(cfg: CaseConfig) -> BlockLayout:
    m, d = cfg.mesh, cfg.domain
    R = 0.5
    a = m.square_half
    if not (R < m.r_mid < a):
        raise ValueError(f"need 0.5 < r_mid ({m.r_mid}) < square_half ({a})")
    if min(d.upstream, d.downstream, d.half_height) <= a:
        raise ValueError("domain boundaries must lie outside the near-field square")

    # ---- expansion ratios from BASE counts (refinement = 1) -------------
    nq0 = m.n_quadrant
    E_ra = ratio_from_first_cell(m.r_mid - R, m.n_ring_inner, m.first_cell)
    last_ra = m.first_cell * E_ra
    E_rb = ratio_from_first_cell(a - m.r_mid, m.n_ring_outer, last_ra)
    ds_square = 2.0 * a / nq0  # tangential spacing along the square sides
    ndn0 = max(2, int(round(m.n_downstream * m.wake_factor)))
    E_dn = ratio_from_first_cell(d.downstream - a, ndn0, ds_square)
    E_lat = ratio_from_first_cell(d.half_height - a, m.n_lateral, ds_square)
    E_up = 1.0 / ratio_from_first_cell(d.upstream - a, m.n_upstream, ds_square)

    f = m.refinement
    return BlockLayout(
        R=R,
        r_mid=m.r_mid,
        a=a,
        Lu=d.upstream,
        Ld=d.downstream,
        H=d.half_height,
        span=m.span,
        nq=_scaled(nq0, f),
        nra=_scaled(m.n_ring_inner, f),
        nrb=_scaled(m.n_ring_outer, f),
        nup=_scaled(m.n_upstream, f),
        ndn=_scaled(ndn0, f),
        nlat=_scaled(m.n_lateral, f),
        E_ra=E_ra,
        E_rb=E_rb,
        E_up=E_up,
        E_dn=E_dn,
        E_lat=E_lat,
    )


def counts_preserving_growth(length_old: float, n_old: int, first: float, length_new: float) -> int:
    """Cell count over ``length_new`` that keeps the first cell and per-cell growth of the old block.

    Used when a domain is enlarged: the near-field cell distribution stays
    identical and cells are only added further out, so a domain study does
    not also change the resolution.
    """
    E = ratio_from_first_cell(length_old, n_old, first)
    g = E ** (1.0 / (n_old - 1))
    if abs(g - 1.0) < 1e-12:
        return max(2, int(round(length_new / first)))
    return max(2, int(round(math.log(1.0 + length_new * (g - 1.0) / first) / math.log(g))))


def expanded_domain_counts(cfg: CaseConfig, upstream: float, downstream: float, half_height: float) -> dict[str, int]:
    """Base (refinement=1) far-field counts for a larger domain with unchanged near-field mesh."""
    m, d = cfg.mesh, cfg.domain
    a = m.square_half
    ds = 2.0 * a / m.n_quadrant
    ndn0 = max(2, int(round(m.n_downstream * m.wake_factor)))
    ndn_new = counts_preserving_growth(d.downstream - a, ndn0, ds, downstream - a)
    return {
        "mesh.n_upstream": counts_preserving_growth(d.upstream - a, m.n_upstream, ds, upstream - a),
        "mesh.n_downstream": max(2, int(round(ndn_new / m.wake_factor))),
        "mesh.n_lateral": counts_preserving_growth(d.half_height - a, m.n_lateral, ds, half_height - a),
    }


def _fmt(x: float) -> str:
    return f"{x:.10g}"


def render_blockmesh_dict(cfg: CaseConfig) -> tuple[str, BlockLayout]:
    """Return blockMeshDict text (physical units via ``scale D``) and the layout."""
    L = resolve_layout(cfg)
    D = cfg.physical.diameter
    z0, z1 = 0.0, L.span

    verts: list[tuple[float, float]] = []
    index: dict[str, int] = {}

    def add(name: str, x: float, y: float) -> None:
        index[name] = len(verts)
        verts.append((x, y))

    angles = [-45.0, 45.0, 135.0, 225.0]
    for k, th in enumerate(angles):
        t = math.radians(th)
        add(f"P{k}", L.R * math.cos(t), L.R * math.sin(t))
        add(f"Q{k}", L.r_mid * math.cos(t), L.r_mid * math.sin(t))
    xs = [-L.Lu, -L.a, L.a, L.Ld]
    ys = [-L.H, -L.a, L.a, L.H]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            add(f"G{i}{j}", x, y)
    # the square corners S0..S3 coincide with grid points G21, G22, G12, G11
    square = {0: "G21", 1: "G22", 2: "G12", 3: "G11"}

    nv = len(verts)

    def hexv(names: list[str]) -> str:
        ids = [index[n] for n in names]
        return " ".join(str(i) for i in ids + [i + nv for i in ids])

    blocks: list[str] = []
    # ring A and ring B: (inner_k, outer_k, outer_k+1, inner_k+1) -> radial x CCW = +z
    for k in range(4):
        k1 = (k + 1) % 4
        blocks.append(
            f"    hex ({hexv([f'P{k}', f'Q{k}', f'Q{k1}', f'P{k1}'])}) cylRingA "
            f"({L.nra} {L.nq} 1) simpleGrading ({_fmt(L.E_ra)} 1 1)"
        )
    for k in range(4):
        k1 = (k + 1) % 4
        blocks.append(
            f"    hex ({hexv([f'Q{k}', square[k], square[k1], f'Q{k1}'])}) cylRingB "
            f"({L.nrb} {L.nq} 1) simpleGrading ({_fmt(L.E_rb)} 1 1)"
        )
    nx = [L.nup, L.nq, L.ndn]
    ny = [L.nlat, L.nq, L.nlat]
    gx = [L.E_up, 1.0, L.E_dn]
    gy = [1.0 / L.E_lat, 1.0, L.E_lat]
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            names = [f"G{i}{j}", f"G{i+1}{j}", f"G{i+1}{j+1}", f"G{i}{j+1}"]
            blocks.append(
                f"    hex ({hexv(names)}) farField ({nx[i]} {ny[j]} 1) "
                f"simpleGrading ({_fmt(gx[i])} {_fmt(gy[j])} 1)"
            )

    edges: list[str] = []
    for k in range(4):
        k1 = (k + 1) % 4
        mid = math.radians(angles[k] + 45.0)
        for rad, pre in ((L.R, "P"), (L.r_mid, "Q")):
            mx, my = rad * math.cos(mid), rad * math.sin(mid)
            for z, off in ((z0, 0), (z1, nv)):
                edges.append(
                    f"    arc {index[f'{pre}{k}'] + off} {index[f'{pre}{k1}'] + off} "
                    f"({_fmt(mx)} {_fmt(my)} {_fmt(z)})"
                )

    def quad(names: list[str]) -> str:
        """Face (a b b' a') from an edge a->b in the front plane."""
        a_, b_ = index[names[0]], index[names[1]]
        return f"({a_} {b_} {b_ + nv} {a_ + nv})"

    cyl_faces = [quad([f"P{(k + 1) % 4}", f"P{k}"]) for k in range(4)]
    inlet_faces = [quad([f"G0{j + 1}", f"G0{j}"]) for j in range(3)]
    outlet_faces = [quad([f"G3{j}", f"G3{j + 1}"]) for j in range(3)]
    top_faces = [quad([f"G{i + 1}3", f"G{i}3"]) for i in range(3)]
    bottom_faces = [quad([f"G{i}0", f"G{i + 1}0"]) for i in range(3)]

    lateral_type = {
        "symmetryPlane": "symmetryPlane",
        "slip": "patch",
        "noSlipWall": "wall",
        "zeroGradientPatch": "patch",
    }[cfg.boundaries.lateral]

    vlines = "\n".join(f"    ({_fmt(x)} {_fmt(y)} {_fmt(z0)})" for x, y in verts)
    vlines += "\n" + "\n".join(f"    ({_fmt(x)} {_fmt(y)} {_fmt(z1)})" for x, y in verts)

    def patch(name: str, ptype: str, faces: list[str]) -> str:
        fl = "\n".join(f"            {f}" for f in faces)
        return f"    {name}\n    {{\n        type {ptype};\n        faces\n        (\n{fl}\n        );\n    }}"

    text = f"""/*  Generated by socrates.case_generation.blockmesh -- do not edit by hand  */
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

// lengths below are in units of D; scale converts to metres
scale   {_fmt(D)};

vertices
(
{vlines}
);

blocks
(
{chr(10).join(blocks)}
);

edges
(
{chr(10).join(edges)}
);

boundary
(
{patch("cylinder", "wall", cyl_faces)}
{patch("inlet", "patch", inlet_faces)}
{patch("outlet", "patch", outlet_faces)}
{patch("top", lateral_type, top_faces)}
{patch("bottom", lateral_type, bottom_faces)}
);

defaultPatch
{{
    name frontAndBack;
    type empty;
}}

mergePatchPairs
(
);
"""
    return text, L
