"""Execute OpenFOAM utilities and solvers for a generated case.

Solver-specific: this module and ``parsers.py`` are the only places that
know OpenFOAM command names.  Each step's log is kept in the case
directory; failures raise ``RunFailure`` with the failing step and the log
tail (no swallowed errors).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_BASHRC = os.environ.get(
    "SOCRATES_OPENFOAM_BASHRC", "/usr/lib/openfoam/openfoam2412/etc/bashrc"
)


class RunFailure(RuntimeError):
    def __init__(self, step: str, returncode: int, log_tail: str):
        super().__init__(f"OpenFOAM step '{step}' failed (rc={returncode}):\n{log_tail}")
        self.step = step
        self.returncode = returncode
        self.log_tail = log_tail


@dataclass
class StepRecord:
    step: str
    command: str
    returncode: int
    wall_seconds: float
    log_file: str


@dataclass
class RunRecord:
    steps: list[StepRecord] = field(default_factory=list)

    @property
    def wall_seconds(self) -> float:
        return sum(s.wall_seconds for s in self.steps)


def openfoam_available(bashrc: str = DEFAULT_BASHRC) -> bool:
    return Path(bashrc).exists()


def _run(case_dir: Path, step: str, command: str, bashrc: str, timeout: float | None) -> StepRecord:
    log = case_dir / f"log.{step}"
    t0 = time.monotonic()
    with open(log, "w") as fh:
        try:
            proc = subprocess.run(
                ["bash", "-c", f"source {bashrc} >/dev/null 2>&1; {command}"],
                cwd=case_dir,
                stdout=fh,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc = -9
            fh.write(f"\n[socrates] step '{step}' killed after timeout of {timeout} s\n")
    rec = StepRecord(step, command, rc, time.monotonic() - t0, log.name)
    if rc != 0:
        tail = "".join(log.read_text(errors="replace").splitlines(keepends=True)[-30:])
        raise RunFailure(step, rc, tail)
    return rec


def openfoam_version_info(bashrc: str = DEFAULT_BASHRC) -> dict:
    """Version strings for provenance (best effort; missing values are None)."""
    info: dict = {"bashrc": bashrc}
    try:
        out = subprocess.run(
            ["bash", "-c", f"source {bashrc} >/dev/null 2>&1; echo $WM_PROJECT_VERSION; echo $WM_OPTIONS; foamVersion -patch 2>/dev/null || true"],
            capture_output=True, text=True, timeout=60,
        ).stdout.split("\n")
        info["WM_PROJECT_VERSION"] = out[0].strip() or None
        info["WM_OPTIONS"] = out[1].strip() if len(out) > 1 else None
    except (subprocess.SubprocessError, OSError) as exc:
        info["error"] = f"version query failed: {exc}"
    try:
        dpkg = subprocess.run(
            ["dpkg-query", "-W", "-f=${Version}", "openfoam2412"], capture_output=True, text=True, timeout=30
        )
        info["package_version"] = dpkg.stdout.strip() or None
    except (subprocess.SubprocessError, OSError):
        info["package_version"] = None
    return info


def run_case(
    case_dir: str | Path,
    solver: str,
    *,
    perturb: bool,
    map_from: str | Path | None = None,
    map_consistent: bool = True,
    restart: bool = False,
    bashrc: str = DEFAULT_BASHRC,
    solver_timeout: float | None = 6 * 3600,
) -> RunRecord:
    """Mesh, check, initialise and solve.

    * ``restart``: continue an existing case from its latest time (no meshing).
    * ``map_from``: initialise from the latest time of another case via mapFields.
    * ``perturb``: apply setFields perturbation (fresh unsteady starts only).
    """
    case_dir = Path(case_dir)
    rec = RunRecord()
    if not restart:
        rec.steps.append(_run(case_dir, "blockMesh", "blockMesh", bashrc, 600))
        rec.steps.append(_run(case_dir, "checkMesh", "checkMesh -allGeometry -allTopology", bashrc, 600))
        if map_from is not None:
            flag = "-consistent " if map_consistent else ""
            if not map_consistent:
                (case_dir / "system" / "mapFieldsDict").write_text(
                    "FoamFile { version 2.0; format ascii; class dictionary; object mapFieldsDict; }\n"
                    "patchMap ();\ncuttingPatches ();\n"
                )
            rec.steps.append(
                _run(case_dir, "mapFields", f"mapFields {Path(map_from).resolve()} {flag}-sourceTime latestTime", bashrc, 1800)
            )
        elif perturb:
            rec.steps.append(_run(case_dir, "setFields", "setFields", bashrc, 600))
    log_name = solver if not restart else f"{solver}.restart{len(list(case_dir.glob(f'log.{solver}*')))}"
    rec.steps.append(_run(case_dir, log_name, solver, bashrc, solver_timeout))
    return rec


def prune_time_dirs(case_dir: str | Path, keep_latest: bool = True) -> None:
    """Delete intermediate field directories (keeps 0/ and the latest time)."""
    case_dir = Path(case_dir)
    times = []
    for d in case_dir.iterdir():
        if d.is_dir():
            try:
                times.append((float(d.name), d))
            except ValueError:
                continue
    times.sort()
    for t, d in times[:-1] if keep_latest else times:
        if t != 0.0:
            shutil.rmtree(d)
