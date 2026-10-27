"""Provenance: which code, environment and backend produced a result (ADR-0005).

The code fingerprint hashes the *source files* actually on disk, not the git commit, so a
result produced from an uncommitted tree is still traceable (and is flagged ``dirty``).
Solver runs are keyed by the fingerprint of their own subpackage, so editing the FEM
solver does not invalidate stored flow results.
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
from functools import lru_cache
from pathlib import Path

import torch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]  # src/physis
REPO_ROOT = PACKAGE_ROOT.parents[1]


@lru_cache(maxsize=None)
def source_fingerprint(subpackage: str = "") -> str:
    """sha256 over the .py sources of ``physis.<subpackage>`` (whole package if empty).

    Includes ``physis/core`` always, since every solver depends on it.
    """
    roots = [PACKAGE_ROOT / "core"]
    target = PACKAGE_ROOT / subpackage.replace(".", "/") if subpackage else PACKAGE_ROOT
    roots.append(target)
    files: set[Path] = set()
    for root in roots:
        if root.is_file():
            files.add(root)
        else:
            files.update(root.rglob("*.py"))
    h = hashlib.sha256()
    for f in sorted(files):
        h.update(str(f.relative_to(PACKAGE_ROOT)).encode())
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def clear_fingerprint_cache() -> None:
    source_fingerprint.cache_clear()


def git_state() -> dict:
    """Commit and dirty flag of the repository, if it is one."""
    try:
        rev = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain", "--", "src"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        return {"commit": rev, "dirty": dirty}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": None, "dirty": None}


def environment() -> dict:
    return {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "threads": torch.get_num_threads(),
    }
