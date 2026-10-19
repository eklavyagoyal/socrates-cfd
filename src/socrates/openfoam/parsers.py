"""Parsers for OpenFOAM (ESI v2412) text output.

Each parser returns plain Python/numpy data and never guesses: a quantity
that is absent from the text is returned as ``None`` (so downstream checks
can report INCONCLUSIVE instead of silently passing).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

_FLOAT = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"

# --------------------------------------------------------------------------
# checkMesh
# --------------------------------------------------------------------------


def parse_checkmesh(text: str) -> dict:
    """Extract mesh statistics and the verdict of OpenFOAM's checkMesh."""

    def grab(pattern: str, cast=float):
        m = re.search(pattern, text)
        return cast(m.group(1)) if m else None

    out: dict = {
        "points": grab(r"\n\s*points:\s+(\d+)", int),
        "faces": grab(r"\n\s*faces:\s+(\d+)", int),
        "internal_faces": grab(r"\n\s*internal faces:\s+(\d+)", int),
        "cells": grab(r"\n\s*cells:\s+(\d+)", int),
        "hexahedra": grab(r"\n\s*hexahedra:\s+(\d+)", int),
        "max_aspect_ratio": grab(rf"Max aspect ratio = ({_FLOAT})"),
        "max_non_orthogonality": grab(rf"Mesh non-orthogonality Max: ({_FLOAT})"),
        "avg_non_orthogonality": grab(rf"Mesh non-orthogonality Max: {_FLOAT} average: ({_FLOAT})"),
        "max_skewness": grab(rf"Max skewness = ({_FLOAT})"),
        "min_volume": grab(rf"Min volume = ({_FLOAT})"),
        "max_volume": grab(rf"Max volume = ({_FLOAT})"),
        "total_volume": grab(rf"Total volume = ({_FLOAT})"),
        "geometric_directions": grab(r"Mesh has (\d+) geometric", int),
    }
    bb = re.search(rf"Overall domain bounding box \(({_FLOAT}) ({_FLOAT}) ({_FLOAT})\) \(({_FLOAT}) ({_FLOAT}) ({_FLOAT})\)", text)
    out["bounding_box"] = [[float(bb.group(i)) for i in (1, 2, 3)], [float(bb.group(i)) for i in (4, 5, 6)]] if bb else None
    m = re.search(r"Failed (\d+) mesh checks", text)
    out["failed_checks"] = int(m.group(1)) if m else 0
    out["mesh_ok"] = bool(re.search(r"^Mesh OK\.", text, re.M)) and out["failed_checks"] == 0
    # '***' lines are checkMesh errors; '*' (single) lines are informational warnings
    out["error_lines"] = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("***")]
    out["warning_lines"] = [
        ln.strip() for ln in text.splitlines() if re.match(r"^\s*\*[^*]", ln)
    ]
    out["completed"] = bool(re.search(r"^End\s*$", text, re.M))
    patches = {}
    bbre = rf"\(({_FLOAT}) ({_FLOAT}) ({_FLOAT})\) \(({_FLOAT}) ({_FLOAT}) ({_FLOAT})\)"
    for m in re.finditer(r"^\s+(\w+)\s+(\d+)\s+(\d+)\s+(ok[^(\n]*|multiply connected[^(\n]*)(.*)$", text, re.M):
        entry = {"faces": int(m.group(2)), "points": int(m.group(3)), "topology": m.group(4).strip()}
        b = re.search(bbre, m.group(5))
        if b:
            entry["bounding_box"] = [[float(b.group(i)) for i in (1, 2, 3)], [float(b.group(i)) for i in (4, 5, 6)]]
        patches[m.group(1)] = entry
    out["patches"] = patches
    return out


# --------------------------------------------------------------------------
# solver log
# --------------------------------------------------------------------------


@dataclass
class SolverLog:
    application: str | None
    build: str | None
    n_procs: int | None
    host: str | None
    times: np.ndarray
    courant_mean: np.ndarray
    courant_max: np.ndarray
    cont_sum_local: np.ndarray  # last value per time step
    cont_global: np.ndarray
    cont_cumulative: np.ndarray
    execution_time: float | None
    clock_time: float | None
    completed: bool  # reached final 'End'
    fatal_errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    steady_converged_iteration: int | None = None  # simpleFoam residualControl
    max_solver_iterations_hit: int = 0
    n_steps: int = 0
    # final residual / iterations of the LAST pressure solve of each step
    # (solverInfo only records the first solve of a step, so this must come
    # from the log)
    p_last_final: np.ndarray = field(default_factory=lambda: np.empty(0))
    p_last_iters: np.ndarray = field(default_factory=lambda: np.empty(0))


_RE_TIME = re.compile(rf"^Time = ({_FLOAT})s?\s*$")
_RE_CO = re.compile(rf"^Courant Number mean: ({_FLOAT}) max: ({_FLOAT})")
_RE_CONT = re.compile(
    rf"^time step continuity errors : sum local = ({_FLOAT}), global = ({_FLOAT}), cumulative = ({_FLOAT})"
)
_RE_EXEC = re.compile(rf"^ExecutionTime = ({_FLOAT}) s\s+ClockTime = ({_FLOAT}) s")
_RE_ITERS = re.compile(r"No Iterations (\d+)")
_RE_PSOLVE = re.compile(rf"Solving for p, Initial residual = ({_FLOAT}), Final residual = ({_FLOAT}), No Iterations (\d+)")


def parse_solver_log(text: str, max_iter_limit: int = 1000) -> SolverLog:
    """Parse a pimpleFoam/simpleFoam log line by line.

    Courant numbers printed *before* a 'Time =' line belong to that step; we
    record one value per time step (the last printed before the step's
    'Time =' line) and one continuity error triple per step (the last
    pressure correction of the step).
    """
    times: list[float] = []
    co_mean: list[float] = []
    co_max: list[float] = []
    c_loc: list[float] = []
    c_glob: list[float] = []
    c_cum: list[float] = []
    pending_co: tuple[float, float] | None = None
    step_cont: tuple[float, float, float] | None = None
    p_fin: list[float] = []
    p_it: list[float] = []
    step_p: tuple[float, int] | None = None
    exec_t = clock_t = None
    fatal: list[str] = []
    warns: list[str] = []
    app = build = host = None
    nprocs = None
    steady_conv = None
    max_hits = 0
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("Exec "):
            app = ln.split(":", 1)[1].strip()
        elif ln.startswith("Build "):
            build = ln.split(":", 1)[1].strip()
        elif ln.startswith("Host "):
            host = ln.split(":", 1)[1].strip().strip('"')
        elif ln.startswith("nProcs "):
            try:
                nprocs = int(ln.split(":", 1)[1])
            except ValueError:
                pass
        m = _RE_CO.match(ln)
        if m:
            pending_co = (float(m.group(1)), float(m.group(2)))
        m = _RE_TIME.match(ln)
        if m:
            if times and step_cont is not None:
                c_loc.append(step_cont[0]); c_glob.append(step_cont[1]); c_cum.append(step_cont[2])
            elif times:
                c_loc.append(np.nan); c_glob.append(np.nan); c_cum.append(np.nan)
            if times:
                p_fin.append(step_p[0] if step_p else np.nan); p_it.append(step_p[1] if step_p else np.nan)
            step_cont = None
            step_p = None
            times.append(float(m.group(1)))
            if pending_co is not None:
                co_mean.append(pending_co[0]); co_max.append(pending_co[1])
            else:
                co_mean.append(np.nan); co_max.append(np.nan)
        m = _RE_CONT.match(ln)
        if m:
            step_cont = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
        mp = _RE_PSOLVE.search(ln)
        if mp:
            step_p = (float(mp.group(2)), int(mp.group(3)))
        m = _RE_EXEC.match(ln)
        if m:
            exec_t, clock_t = float(m.group(1)), float(m.group(2))
        if "FOAM FATAL" in ln:
            fatal.append(" ".join(l.strip() for l in lines[i : i + 6]))
        elif "FOAM Warning" in ln:
            warns.append(" ".join(l.strip() for l in lines[i : i + 4]))
        if "solution converged in" in ln:
            mm = re.search(r"converged in (\d+)", ln)
            if mm:
                steady_conv = int(mm.group(1))
        mi = _RE_ITERS.search(ln)
        if mi and int(mi.group(1)) >= max_iter_limit:
            max_hits += 1
        i += 1
    if times:
        if step_cont is not None:
            c_loc.append(step_cont[0]); c_glob.append(step_cont[1]); c_cum.append(step_cont[2])
        else:
            c_loc.append(np.nan); c_glob.append(np.nan); c_cum.append(np.nan)
        p_fin.append(step_p[0] if step_p else np.nan); p_it.append(step_p[1] if step_p else np.nan)
    completed = bool(re.search(r"^End\s*$", text, re.M)) and not fatal
    return SolverLog(
        application=app,
        build=build,
        n_procs=nprocs,
        host=host,
        times=np.asarray(times),
        courant_mean=np.asarray(co_mean),
        courant_max=np.asarray(co_max),
        cont_sum_local=np.asarray(c_loc),
        cont_global=np.asarray(c_glob),
        cont_cumulative=np.asarray(c_cum),
        execution_time=exec_t,
        clock_time=clock_t,
        completed=completed,
        fatal_errors=fatal,
        warnings=warns,
        steady_converged_iteration=steady_conv,
        max_solver_iterations_hit=max_hits,
        n_steps=len(times),
        p_last_final=np.asarray(p_fin, dtype=float),
        p_last_iters=np.asarray(p_it, dtype=float),
    )


# --------------------------------------------------------------------------
# function-object .dat files
# --------------------------------------------------------------------------


def parse_dat(path: str | Path) -> tuple[list[str], dict[str, np.ndarray]]:
    """Parse a function-object table with a '# Time ...' header line.

    Returns (column_names, columns).  Numeric columns become float arrays;
    non-numeric columns (solver names, booleans) are kept as object arrays.
    Duplicate time rows (from restarts) keep the *last* occurrence.
    """
    header: list[str] | None = None
    rows: list[list[str]] = []
    with open(path) as fh:
        for ln in fh:
            if ln.startswith("#"):
                parts = ln[1:].strip().split()
                if parts and parts[0] == "Time":
                    header = parts
                continue
            s = ln.strip()
            if s:
                rows.append(s.split())
    if header is None:
        raise ValueError(f"{path}: no '# Time' header found")
    ncol = len(header)
    rows = [r for r in rows if len(r) == ncol]
    cols: dict[str, np.ndarray] = {}
    for j, name in enumerate(header):
        raw = [r[j] for r in rows]
        try:
            cols[name] = np.asarray([float(x) for x in raw])
        except ValueError:
            cols[name] = np.asarray(raw, dtype=object)
    if "Time" in cols and len(cols["Time"]):
        t = cols["Time"]
        # keep last occurrence of each time (restart overlap)
        _, idx_rev = np.unique(t[::-1], return_index=True)
        keep = np.sort(len(t) - 1 - idx_rev)
        cols = {k: v[keep] for k, v in cols.items()}
    return header, cols


def concat_time_dirs(post_dir: str | Path, filename: str) -> dict[str, np.ndarray]:
    """Concatenate ``postProcessing/<fo>/<startTime>/<filename>`` across restarts."""
    post_dir = Path(post_dir)
    if not post_dir.exists():
        return {}
    subdirs = sorted(
        (d for d in post_dir.iterdir() if d.is_dir() and re.fullmatch(_FLOAT, d.name)),
        key=lambda d: float(d.name),
    )
    merged: dict[str, list[np.ndarray]] = {}
    for d in subdirs:
        f = d / filename
        if not f.exists():
            continue
        _, cols = parse_dat(f)
        for k, v in cols.items():
            merged.setdefault(k, []).append(v)
    out = {k: np.concatenate(v) for k, v in merged.items()}
    if "Time" in out and len(out["Time"]):
        t = out["Time"]
        _, idx_rev = np.unique(t[::-1], return_index=True)
        keep = np.sort(len(t) - 1 - idx_rev)
        out = {k: v[keep] for k, v in out.items()}
    return out
