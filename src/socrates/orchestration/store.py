"""Content-addressed run store with provenance.

A run is identified by the hash of (numerical configuration, initialisation).
Requesting the same run twice returns the stored result instead of
re-running OpenFOAM; this keeps benchmark comparisons between systems
consistent (they literally share the same simulations) and saves compute.

Layout::

    <root>/<run_id>/
        case/            OpenFOAM case (fields of intermediate times pruned)
        run.json         provenance record
        evidence.json    extracted evidence
        series.npz       force-coefficient time series (t, cd, cl)
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import fcntl
import gzip
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from ..case_generation.spec import CaseConfig, ProblemSpec, diff_configs
from ..case_generation.writer import write_case
from ..evidence.extract import extract_evidence
from ..openfoam.runner import RunFailure, openfoam_version_info, prune_time_dirs, run_case

_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()
_VERSION_CACHE: dict | None = None


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extractor_fingerprint() -> dict:
    """Identity of the code that turns raw outputs into evidence (for re-extraction provenance)."""
    src = Path(__file__).resolve().parents[1]
    h = hashlib.sha256()
    for f in sorted([*(src / "evidence").glob("*.py"), src / "openfoam" / "parsers.py"]):
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return {"extractor_sha256": h.hexdigest()[:16], "git_commit": software_versions().get("socrates_git_commit"),
            "time": _now()}


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(f.relative_to(root)): _sha256(f) for f in sorted(root.rglob("*")) if f.is_file()}


def software_versions() -> dict:
    global _VERSION_CACHE
    if _VERSION_CACHE is None:
        import scipy

        try:
            repo = Path(__file__).resolve().parents[3]
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, timeout=10).stdout.strip()
            dirty = bool(subprocess.run(["git", "status", "--porcelain", "src"], cwd=repo, capture_output=True, text=True, timeout=10).stdout.strip())
        except (subprocess.SubprocessError, OSError):
            commit, dirty = None, None
        _VERSION_CACHE = {
            "openfoam": openfoam_version_info(),
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "socrates_git_commit": commit,
            "socrates_src_dirty": dirty,
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
        }
    return _VERSION_CACHE


@dataclass
class Initialisation:
    """How a run's initial fields are produced."""

    kind: str  # "fresh" | "map" | "restart"
    source_run: str | None = None
    consistent: bool = True

    def key(self) -> str:
        return f"{self.kind}:{self.source_run or ''}:{int(self.consistent)}"


@dataclass
class RunResult:
    run_id: str
    run_dir: Path
    status: str
    provenance: dict
    evidence: dict | None
    config: CaseConfig

    @property
    def ok(self) -> bool:
        return self.status == "completed"

    def series(self) -> dict[str, np.ndarray]:
        f = self.run_dir / "series.npz"
        if not f.exists():
            return {}
        with np.load(f) as z:
            return {k: z[k] for k in z.files}


class CpuSlots:
    """Machine-wide CPU slots shared by all processes using the same store.

    Each slot is an fcntl lock on a file; a run holds one slot while OpenFOAM
    executes, so concurrent benchmark processes never oversubscribe cores.
    """

    def __init__(self, directory: Path, n: int):
        self.dir = directory
        self.dir.mkdir(parents=True, exist_ok=True)
        self.n = n

    @contextlib.contextmanager
    def acquire(self, poll_s: float = 5.0):
        while True:
            for i in range(self.n):
                fh = open(self.dir / f"slot{i}.lock", "w")
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    fh.close()
                    continue
                try:
                    yield i
                finally:
                    fcntl.flock(fh, fcntl.LOCK_UN)
                    fh.close()
                return
            time.sleep(poll_s)


class RunStore:
    def __init__(self, root: str | Path, cpu_slots: int | None = None):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        n = cpu_slots or int(os.environ.get("SOCRATES_CPU_SLOTS", os.cpu_count() or 1))
        self.cpu = CpuSlots(self.root / ".slots", n)

    # ------------------------------------------------------------------
    def run_id_for(self, cfg: CaseConfig, init: Initialisation) -> str:
        h = hashlib.sha256((cfg.content_hash() + "|" + init.key()).encode()).hexdigest()[:12]
        return f"{cfg.name}-{h}"

    def _find_existing(self, cfg: CaseConfig, init: Initialisation) -> Path | None:
        h = hashlib.sha256((cfg.content_hash() + "|" + init.key()).encode()).hexdigest()[:12]
        for d in self.root.glob(f"*-{h}"):
            if (d / "run.json").exists():
                return d
        return None

    def existing_run_id(self, cfg: CaseConfig, init: Initialisation) -> str | None:
        d = self._find_existing(cfg, init)
        return d.name if d is not None else None

    def load(self, run_id: str) -> RunResult:
        d = self.root / run_id
        prov = json.loads((d / "run.json").read_text())
        ev_file = d / "evidence.json"
        ev = json.loads(ev_file.read_text()) if ev_file.exists() else None
        return RunResult(run_id, d, prov["status"], prov, ev, CaseConfig.model_validate(prov["case_config"]))

    def reextract(self, run_id: str) -> RunResult:
        """Recompute evidence from the retained raw outputs (after extractor changes)."""
        d = self.root / run_id
        prov = json.loads((d / "run.json").read_text())
        cfg = CaseConfig.model_validate(prov["case_config"])
        spec = ProblemSpec.model_validate(prov["problem_spec"])
        ev, series = extract_evidence(d / "case", cfg, spec)
        old = json.loads((d / "evidence.json").read_text()) if (d / "evidence.json").exists() else {}
        ev["run_id"] = run_id
        ev["cost"] = old.get("cost", {})
        ev["extraction"] = {**extractor_fingerprint(), "reextracted": True}
        if series:
            np.savez_compressed(d / "series.npz", **{k: v.astype(np.float64) for k, v in series.items()})
        (d / "evidence.json").write_text(json.dumps(ev, indent=2, default=_json_default))
        return self.load(run_id)

    def list_runs(self) -> list[str]:
        return sorted(d.name for d in self.root.iterdir() if (d / "run.json").exists())

    # ------------------------------------------------------------------
    def get_or_run(
        self,
        cfg: CaseConfig,
        spec: ProblemSpec,
        *,
        init: Initialisation | None = None,
        parent_run: str | None = None,
        reason: str = "",
        experiment: dict | None = None,
        launched_by: str = "user",
    ) -> RunResult:
        init = init or Initialisation("fresh")
        existing = self._find_existing(cfg, init)
        key = existing.name if existing else self.run_id_for(cfg, init)
        with _LOCKS_GUARD:
            lock = _LOCKS.setdefault(key, threading.Lock())
        # thread lock (same process) + fcntl lock (other processes) for the whole
        # find-or-execute, so an identical run is never executed twice concurrently
        lock_dir = self.root / ".locks"
        lock_dir.mkdir(exist_ok=True)
        h = key.rsplit("-", 1)[-1]
        with lock, open(lock_dir / f"{h}.lock", "w") as lfh:
            fcntl.flock(lfh, fcntl.LOCK_EX)
            existing = self._find_existing(cfg, init)
            while existing is not None and self._running_elsewhere(existing):
                time.sleep(30)  # another process owns this run: wait for it
            if existing is not None:
                res = self.load(existing.name)
                if res.ok or res.provenance.get("failure_kind") in ("solver", "mesh"):
                    self._record_request(existing, launched_by, reason, parent_run, experiment)
                    return res
                if res.status == "running":  # owner died: adopt a completed orphan if possible
                    adopted = self._adopt_orphan(existing)
                    if adopted is not None:
                        self._record_request(existing, launched_by, reason, parent_run, experiment)
                        return adopted
                shutil.rmtree(existing)  # owner died mid-run (infrastructure failure): retry cleanly
            return self._execute(key, cfg, spec, init, parent_run, reason, experiment, launched_by)

    @staticmethod
    def _running_elsewhere(d: Path) -> bool:
        try:
            prov = json.loads((d / "run.json").read_text())
        except (OSError, json.JSONDecodeError):
            return False
        if prov.get("status") != "running":
            return False
        pid = prov.get("owner_pid")
        if pid is None or pid == os.getpid():
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    def _record_request(self, d: Path, launched_by: str, reason: str, parent: str | None, experiment: dict | None) -> None:
        """Append a cache-hit request to the run's request log (audit of reuse)."""
        with open(d / "requests.jsonl", "a") as fh:
            fh.write(json.dumps({"time": _now(), "launched_by": launched_by, "reason": reason,
                                 "parent_run": parent, "experiment": experiment, "cache_hit": True}) + "\n")

    def _execute(self, run_id, cfg, spec, init, parent_run, reason, experiment, launched_by) -> RunResult:
        d = self.root / run_id
        if d.exists():
            shutil.rmtree(d)
        case = d / "case"
        parent_cfg = self.load(parent_run).config if parent_run else None
        prov: dict[str, Any] = {
            "run_id": run_id,
            "status": "running",
            "owner_pid": os.getpid(),
            "created": _now(),
            "problem_spec": spec.model_dump(mode="json"),
            "case_config": cfg.model_dump(mode="json"),
            "config_hash": cfg.content_hash(),
            "parent_run": parent_run,
            "launch_reason": reason,
            "launched_by": launched_by,
            "experiment": experiment,
            "config_changes_from_parent": diff_configs(parent_cfg, cfg) if parent_cfg else None,
            "initialisation": {"kind": init.kind, "source_run": init.source_run, "consistent": init.consistent},
            "software": software_versions(),
        }
        d.mkdir(parents=True)
        (d / "run.json").write_text(json.dumps(prov, indent=2))

        if init.kind == "restart":
            src = self.root / init.source_run / "case"
            shutil.copytree(src, case, ignore=shutil.ignore_patterns("log.*"))
            # regenerate system/ and constant/ from the new config (e.g. endTime)
            tmp = d / "_gen"
            write_case(cfg, tmp, segment_start=self.load(init.source_run).config.time.end_time)
            # replace dictionaries only; constant/polyMesh (the mesh) must be kept
            shutil.rmtree(case / "system")
            shutil.copytree(tmp / "system", case / "system")
            for f in (tmp / "constant").iterdir():
                if f.is_file():
                    shutil.copy(f, case / "constant" / f.name)
            shutil.copy(tmp / "case_config.json", case / "case_config.json")
            shutil.rmtree(tmp)
            # keep the source logs so the parsed history is complete
            for lp in (src).glob(f"log.{cfg.numerics.solver}*"):
                shutil.copy(lp, case / lp.name)
            for lp in (src).glob("log.checkMesh"):
                shutil.copy(lp, case / lp.name)
        else:
            write_case(cfg, case)

        prov["started"] = _now()
        failure: RunFailure | None = None
        with self.cpu.acquire():
            try:
                rec = run_case(
                    case,
                    cfg.numerics.solver,
                    perturb=(cfg.perturbation.enabled and cfg.numerics.solver == "pimpleFoam" and init.kind == "fresh"),
                    map_from=(self.root / init.source_run / "case") if init.kind == "map" else None,
                    map_consistent=init.consistent,
                    restart=(init.kind == "restart"),
                )
                prov["commands"] = [s.__dict__ for s in rec.steps]
                prov["wall_seconds"] = rec.wall_seconds
            except RunFailure as exc:
                failure = exc
        prov["finished"] = _now()
        if failure is None and cfg.numerics.solver == "pimpleFoam":
            failure = _check_final_state_written(case, cfg)
        offset = 0
        if init.kind == "restart":
            src_ev = self.load(init.source_run).evidence or {}
            offset = int((src_ev.get("solver") or {}).get("n_steps") or 0)
        return self._finalize(d, run_id, case, cfg, spec, prov, failure, steps_offset=offset)

    def _finalize(self, d: Path, run_id: str, case: Path, cfg: CaseConfig, spec: ProblemSpec, prov: dict,
                  failure: RunFailure | None, steps_offset: int = 0) -> RunResult:
        """Extract evidence, hash/compress raw logs, prune fields, write the provenance record."""
        if failure is not None:
            prov["status"] = "failed"
            prov["failure_kind"] = "solver" if failure.step not in ("blockMesh", "checkMesh") else "mesh"
            prov["failure"] = {"step": failure.step, "returncode": failure.returncode, "log_tail": failure.log_tail}
        else:
            prov["status"] = "completed"

        # evidence is extracted even for failed runs (partial evidence is evidence)
        try:
            ev, series = extract_evidence(case, cfg, spec)
        except Exception as exc:  # noqa: BLE001 -- recorded, never swallowed
            ev, series = {"extraction_error": repr(exc)}, {}
            prov["evidence_extraction_error"] = repr(exc)
        ev["run_id"] = run_id
        ev["extraction"] = extractor_fingerprint()
        n_steps_total = ev.get("solver", {}).get("n_steps")
        n_steps = (n_steps_total - steps_offset) if n_steps_total is not None else None
        ev["cost"] = {
            "wall_seconds": prov.get("wall_seconds"),
            "n_cells": ev.get("mesh", {}).get("n_cells"),
            # steps computed BY THIS RUN (a restart's history includes its parent's steps)
            "n_steps": n_steps,
            "n_steps_including_restart_history": n_steps_total,
        }
        if ev["cost"]["n_cells"] and n_steps:
            ev["cost"]["cell_steps"] = ev["cost"]["n_cells"] * n_steps
        if series:
            np.savez_compressed(d / "series.npz", **{k: v.astype(np.float64) for k, v in series.items()})
        (d / "evidence.json").write_text(json.dumps(ev, indent=2, default=_json_default))

        # raw output hashes + compressed logs; prune bulky intermediate fields
        raw = {}
        for lp in sorted(case.glob("log.*")):
            raw[lp.name] = _sha256(lp)
            with open(lp, "rb") as src_fh, gzip.open(d / f"{lp.name}.gz", "wb") as dst:
                shutil.copyfileobj(src_fh, dst)
        prov["raw_output_sha256"] = raw
        prune_time_dirs(case)
        # function-object outputs (source of every Cd/St) and the retained final fields
        # (initial condition of mapped/restarted children) are hashed too
        if (case / "postProcessing").exists():
            prov["postprocessing_sha256"] = _hash_tree(case / "postProcessing")
        latest = max((x for x in case.iterdir() if x.is_dir() and _is_time(x.name)), key=lambda x: float(x.name),
                     default=None)
        if latest is not None:
            prov["final_fields_sha256"] = {"time": latest.name, "files": _hash_tree(latest)}
        (d / "run.json").write_text(json.dumps(prov, indent=2, default=_json_default))
        return RunResult(run_id, d, prov["status"], prov, ev, cfg)

    def _adopt_orphan(self, d: Path) -> RunResult | None:
        """A run whose owning process died: wait for its solver, then finalize it if it completed.

        Returns None when there is nothing usable (the caller then re-runs it).
        """
        case = d / "case"
        if not case.exists():
            return None

        def solver_alive() -> bool:
            for pid in os.listdir("/proc"):
                if pid.isdigit():
                    try:
                        if os.readlink(f"/proc/{pid}/cwd") == str(case.resolve()):
                            return True
                    except OSError:
                        continue
            return False

        while solver_alive():
            time.sleep(30)
        prov = json.loads((d / "run.json").read_text())
        cfg = CaseConfig.model_validate(prov["case_config"])
        spec = ProblemSpec.model_validate(prov["problem_spec"])
        logs = sorted(case.glob(f"log.{cfg.numerics.solver}*"))
        if not logs:
            return None
        text = logs[-1].read_text(errors="replace")
        if not re.search(r"^End\s*$", text, re.M):
            return None
        m = re.findall(r"ExecutionTime = ([\d.eE+-]+) s\s+ClockTime = ([\d.eE+-]+) s", text)
        prov["wall_seconds"] = float(m[-1][1]) if m else None
        prov["adopted_orphan"] = {"note": "owner process died; solver output completed and was finalized", "time": _now()}
        prov["finished"] = _now()
        offset = 0
        init = prov.get("initialisation") or {}
        if init.get("kind") == "restart":
            src_ev = self.load(init["source_run"]).evidence or {}
            offset = int((src_ev.get("solver") or {}).get("n_steps") or 0)
        return self._finalize(d, prov["run_id"], case, cfg, spec, prov, None, steps_offset=offset)


def _is_time(name: str) -> bool:
    try:
        float(name)
        return True
    except ValueError:
        return False


def _check_final_state_written(case: Path, cfg: CaseConfig) -> RunFailure | None:
    """Children restart from / map the latest time directory: it must be endTime."""
    times = []
    for d in case.iterdir():
        try:
            if d.is_dir():
                times.append(float(d.name))
        except ValueError:
            continue
    end = cfg.time.end_time * cfg.convective_time
    latest = max(times) if times else None
    if latest is None or abs(latest - end) > 1e-6 * max(end, 1e-12):
        return RunFailure("final_state_write", -1, f"latest written time {latest} != endTime {end}")
    return None


def _json_default(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(f"not JSON serialisable: {type(o)}")
