"""Content-addressed run store with provenance (ADR-0005).

Layout::

    <root>/<id[:2]>/<id>/run.json     status, spec, provenance, result meta
    <root>/<id[:2]>/<id>/arrays.npz   result arrays (compressed)

The run id is ``sha256(kind, spec digest, solver code fingerprint)``: an identical request
with identical solver code reuses the stored result; any change to the solver's source
produces a new id. Writes are atomic (temp dir + rename); failed runs are recorded as
``failed`` with the error, never silently dropped. The default root is ``$PHYSIS_STORE``
or ``<repo>/var/store`` (outside git).
"""

from __future__ import annotations

import fcntl
import json
import os
import shutil
import tempfile
import time
import traceback
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import numpy as np

from physis.core.provenance import REPO_ROOT, environment, git_state, source_fingerprint
from physis.core.result import SolverResult
from physis.core.spec import Spec, digest

STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def default_store_root() -> Path:
    env = os.environ.get("PHYSIS_STORE")
    return Path(env) if env else REPO_ROOT / "var" / "store"


class RunStore:
    def __init__(self, root: Path | str | None = None):
        self.root = Path(root) if root is not None else default_store_root()
        self.root.mkdir(parents=True, exist_ok=True)

    # --- ids and paths ------------------------------------------------------------

    @staticmethod
    def run_id(kind: str, spec: Spec, code_fingerprint: str) -> str:
        return digest({"kind": kind, "spec": spec.digest(), "code": code_fingerprint})

    def path(self, run_id: str) -> Path:
        return self.root / run_id[:2] / run_id

    @contextmanager
    def _lock(self) -> Iterator[None]:
        lock_path = self.root / ".lock"
        with open(lock_path, "a") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    # --- read ---------------------------------------------------------------------

    def record(self, run_id: str) -> dict[str, Any] | None:
        p = self.path(run_id) / "run.json"
        if not p.exists():
            return None
        return json.loads(p.read_text())

    def load(self, run_id: str) -> SolverResult:
        rec = self.record(run_id)
        if rec is None:
            raise KeyError(run_id)
        if rec["status"] != STATUS_COMPLETED:
            raise RuntimeError(f"run {run_id} is {rec['status']}: {rec.get('error', '')}")
        with np.load(self.path(run_id) / "arrays.npz") as z:
            arrays = {k: z[k] for k in z.files}
        return SolverResult.from_stored(rec["result"], arrays)

    def records(self, kind: str | None = None) -> Iterator[dict[str, Any]]:
        for p in sorted(self.root.glob("*/*/run.json")):
            rec = json.loads(p.read_text())
            if kind is None or rec.get("kind") == kind:
                yield rec

    # --- write --------------------------------------------------------------------

    def _write(self, run_id: str, record: dict[str, Any], arrays: dict[str, np.ndarray] | None) -> None:
        final = self.path(run_id)
        final.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=f".{run_id[:8]}-", dir=final.parent))
        try:
            if arrays is not None:
                np.savez_compressed(tmp / "arrays.npz", **arrays)
            (tmp / "run.json").write_text(json.dumps(record, indent=1, sort_keys=True, allow_nan=True))
            with self._lock():
                if final.exists():
                    shutil.rmtree(final)
                os.replace(tmp, final)
        finally:
            if tmp.exists():
                shutil.rmtree(tmp, ignore_errors=True)

    def run(
        self,
        kind: str,
        spec: Spec,
        compute: Callable[[], SolverResult],
        *,
        code_subpackage: str,
        backend_info: dict[str, Any] | None = None,
        reuse: bool = True,
    ) -> tuple[str, SolverResult]:
        """Return the stored result for (kind, spec, code) or compute and store it.

        A previously *failed* record is retried, not reused.
        """
        code = source_fingerprint(code_subpackage)
        run_id = self.run_id(kind, spec, code)
        if reuse:
            rec = self.record(run_id)
            if rec is not None and rec["status"] == STATUS_COMPLETED:
                return run_id, self.load(run_id)
        base = {
            "id": run_id,
            "kind": kind,
            "spec": spec.canonical(),
            "spec_digest": spec.digest(),
            "code": {"subpackage": code_subpackage, "fingerprint": code, **git_state()},
            "environment": environment(),
            "backend": backend_info or {},
            "started": time.time(),
        }
        try:
            result = compute()
        except Exception as exc:  # recorded, then re-raised
            self._write(
                run_id,
                {**base, "status": STATUS_FAILED, "finished": time.time(),
                 "error": f"{type(exc).__name__}: {exc}", "traceback": traceback.format_exc()},
                None,
            )
            raise
        self._write(
            run_id,
            {**base, "status": STATUS_COMPLETED, "finished": time.time(), "result": result.meta()},
            result.arrays(),
        )
        return run_id, result
