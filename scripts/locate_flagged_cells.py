"""Locate the cells that checkMesh -allGeometry flags as having a small determinant.

    python scripts/locate_flagged_cells.py <case dir with constant/polyMesh/sets/underdeterminedCells>

Run `checkMesh -allGeometry` on a copy of the case first (it writes the cell set). Prints the distance of the
flagged cells from the cylinder axis in diameters. Used for docs/methodology.md (J1 and the domain-study meshes).
"""

import re, sys, numpy as np
from pathlib import Path

def body(path):
    t = Path(path).read_text(errors="replace")
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"FoamFile\s*\{.*?\}", "", t, flags=re.S)
    return t

def read_list(path):
    t = body(path)
    m = re.search(r"(\d+)\s*\(", t)
    n, start = int(m.group(1)), m.end()
    return n, t[start:]

def points(path):
    n, t = read_list(path)
    arr = np.array(re.findall(r"\(([^()]+)\)", t)[:n], dtype=object)
    return np.array([list(map(float, a.split())) for a in arr])

def faces(path):
    n, t = read_list(path)
    return [list(map(int, f.split())) for f in re.findall(r"\d+\(([^()]*)\)", t)[:n]]

def labels(path):
    n, t = read_list(path)
    return np.array(t.split(")")[0].split(), dtype=int)[:n]

d = Path(sys.argv[1]) / "constant" / "polyMesh"
P, F = points(d / "points"), faces(d / "faces")
own, nei = labels(d / "owner"), labels(d / "neighbour")
cells = labels(d / "sets" / "underdeterminedCells")
ncell = own.max() + 1
cf = [[] for _ in range(ncell)]
for i, c in enumerate(own):
    cf[c].append(i)
for i, c in enumerate(nei):
    cf[c].append(i)
D = 0.01
cent = np.array([P[sorted({p for f in cf[c] for p in F[f]})].mean(axis=0) for c in cells]) / D
r = np.hypot(cent[:, 0], cent[:, 1])
print(f"{Path(sys.argv[1]).name}: {len(cells)} flagged cells; distance from the cylinder axis (D): min {r.min():.1f}, median {np.median(r):.1f}, max {r.max():.1f}; x range {cent[:,0].min():.1f}..{cent[:,0].max():.1f}, |y| range {np.abs(cent[:,1]).min():.1f}..{np.abs(cent[:,1]).max():.1f}")
