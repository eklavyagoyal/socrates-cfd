"""Bookkeeping for the benchmark evaluation: result classification, staleness and stamps.

Nothing here changes a verdict, so this module is deliberately NOT part of the
decision-code fingerprint (`systems.decision_code_fingerprint`).  It supersedes
`systems.is_infrastructure_error`, which classified an LLM outage as a genuine
INCONCLUSIVE when an invalid proposal had preceded it.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path

from ..case_generation.catalog import load_case_definition
from ..case_generation.spec import CaseConfig
from .store import Initialisation, RunStore


def is_infrastructure_error(result: dict) -> bool:
    """True when a stored result reflects a failure of the harness, not a verification outcome.

    - an ERROR verdict (exception in the benchmark job, failed LLM judge call);
    - a verifier exception inside the adaptive loop;
    - an adaptive loop stopped by 'repeated planner failures': the loop sets that reason only when the
      event that exhausted the invalid-action budget was a planner (LLM call / schema) failure, whatever
      invalid proposals preceded it.
    """
    if (result.get("final_verdict") or result.get("verdict")) == "ERROR":
        return True
    reason = str(result.get("stop_reason") or "")
    return reason.startswith("verifier error") or reason == "repeated planner failures"


def evidence_digest(store: RunStore, run_id: str) -> str | None:
    f = store.root / run_id / "evidence.json"
    try:
        return hashlib.sha256(f.read_bytes()).hexdigest()[:16]
    except OSError:
        return None


def _evidence_time(store: RunStore, run_id: str) -> _dt.datetime | None:
    try:
        ev = json.loads((store.root / run_id / "evidence.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None
    t = (ev.get("extraction") or {}).get("time")
    return _dt.datetime.fromisoformat(t) if t else None


def result_runs(result: dict) -> list[str]:
    runs = list(result.get("runs") or [])
    if result.get("root_run") and result["root_run"] not in runs:
        runs.insert(0, result["root_run"])
    return runs


def make_stamp(store: RunStore, result: dict, decision_code: str, **extra) -> dict:
    return {"decision_code": decision_code,
            "created": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            "evidence_sha": {rid: evidence_digest(store, rid) for rid in result_runs(result)}, **extra}


def staleness(result: dict, result_file: Path, store: RunStore, decision_code: str, expected_root: str | None) -> str | None:
    """Why a stored result is not current, or None.

    Current = produced by the current decision code, for the case's current root run, and from the evidence
    files that exist now.  Results written before evidence digests were stamped are compared by time: stale
    if any run's evidence was (re-)extracted after the result was written.
    """
    st = result.get("stamp") or {}
    if st.get("decision_code") != decision_code:
        return f"decision code {st.get('decision_code')} != current {decision_code}"
    if expected_root and result.get("root_run") and result["root_run"] != expected_root:
        return f"root {result['root_run']} != current root {expected_root}"
    shas = st.get("evidence_sha")
    if shas:
        changed = [rid for rid, h in shas.items() if h != evidence_digest(store, rid)]
        return f"evidence changed since the result was computed: {changed}" if changed else None
    try:
        written = _dt.datetime.fromtimestamp(result_file.stat().st_mtime, _dt.timezone.utc)
    except OSError:
        return None
    newer = [rid for rid in result_runs(result) if (t := _evidence_time(store, rid)) and t > written]
    return f"evidence re-extracted after the result was written: {newer}" if newer else None


def current_root(store: RunStore, repo: Path, case: dict) -> str | None:
    """The content-addressed root run of a manifest case, independent of any system's result file."""
    path = repo / case["definition"]
    cfg = CaseConfig.from_yaml(path) if case["id"] == "baseline" else load_case_definition(path)[0]
    rid = store.existing_run_id(cfg, Initialisation("fresh"))
    if rid is None:
        return None
    return rid if store.load(rid).ok or store.load(rid).status == "failed" else None
