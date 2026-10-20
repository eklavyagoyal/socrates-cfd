"""Audit the run store against the stored results and the git history: runs and attempts no stored result shows.

Every simulation is a directory in results/runs/ with a provenance record (run.json). A run counts as used when a
stored result names it: any file under results/benchmark, results/attacks (final and *.partial.json),
results/baseline, results/posthoc or results/reproducibility that contains its run id. Runs launched by the baseline
study (launched_by 'baseline_study' or 'farfield_test') count as used by that study. The audit reports:

- every run by status and launcher;
- runs that no stored result names, with creation time, parent, experiment, failure and cost, whether a live
  process still uses them, and which files under cases/, docs/, reports/ or README.md mention them;
- 'running' records whose owner process is gone (orphaned): no owner_pid (or one a recovery cleared), no such
  process, not a Python process, or a process that started after the record was written (a pid reused after a
  container restart); for every 'running' record, whether its solver had started and how far it got;
- failed runs, with the failure kind and the results that name them;
- finalized runs without postProcessing/final-field hashes (written by code older than R19, docs/methodology.md);
- run-id-shaped strings in results that name no run in the store, and parents missing from the store;
- owner processes: when each one stopped writing records, and which later process took over its launcher on the
  same group of cases (benchmark or attacks), with the commits and launch markers in between;
- from the git history: earlier attempts under a current run id, records deleted outright, and loop attempts whose
  partial result a later attempt of the same system and case replaced, with the LLM cost (`cost_usd`) they recorded.

What it cannot see. The store keeps one record per run id: `RunStore.get_or_run` deletes a 'running' record whose
owner died and runs it again under the same id, and some records were deleted by hand. The git history recovers only
what was committed: an attempt that started and was removed between two commits, or loop iterations after a loop's
last committed partial result, leave no trace. Costs taken from the git history are therefore lower bounds, and the
share of cell-steps in unnamed runs covers current records only.

Read-only: no run record or result is changed. Live processes keep writing results, so the output is a snapshot.
Exit status 1 when the audit is incomplete (an unreadable run record or result file, a git query that failed) or a
result names a run id that is not in the store. It stops with an error when FINGERPRINTED no longer matches the files
`systems.decision_code_fingerprint` hashes.

    python scripts/audit_runs.py        # writes results/analysis/run_audit.{json,md}
"""

import datetime as dt
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
RUNS = RESULTS / "runs"
SOURCES = ["benchmark", "attacks", "baseline", "posthoc", "reproducibility"]
DOC_SOURCES = ["cases", "docs", "reports", "README.md"]  # mention a run without being a result
DOC_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".csv"}
STUDY_LAUNCHERS = {"baseline_study": "scripts/baseline_study.py",
                   "farfield_test": "scripts/farfield_resolution_test.py"}
LLM_LAUNCHER = re.compile(r"llm", re.I)
EXTRA_SYSTEMS = {("benchmark", "exhaustive"): {"Bexh"}}  # Bexh results carry no 'planner' field
# the files systems.decision_code_fingerprint hashes; check_fingerprint_list() fails if they drift apart
FINGERPRINTED = ["src/socrates/checks/*.py", "src/socrates/critic/*.py", "src/socrates/evidence/*.py",
                 "src/socrates/case_generation/*.py", "src/socrates/experiments/*.py",
                 "src/socrates/openfoam/parsers.py", "src/socrates/orchestration/loop.py",
                 "src/socrates/orchestration/systems.py", "src/socrates/orchestration/store.py",
                 "configs/verification.yaml", "configs/verification_v2.yaml", "configs/problem_cylinder_re100.yaml"]
FINGERPRINT_FN = ("/^def decision_code_fingerprint/,/^def /", "src/socrates/orchestration/systems.py")
RUN_ID = re.compile(r"(?<![A-Za-z0-9_.+-])[A-Za-z0-9_.+]+-[0-9a-f]{12}(?![0-9A-Za-z])")
MARKER = re.compile(r"^===\s*(?P<label>.*?)\s+(?P<time>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\s*(?:===)?$")
LOGGED = re.compile(r"(?P<system>\S+)\s+(?P<case>\S+)\s+->\s+(?P<verdict>ACCEPT|REJECT|INCONCLUSIVE|ERROR)")
RELAUNCH_SUBJECT = re.compile(r"relaunch|launched|resumed|container restart", re.I)
RELAUNCH_COMMIT_LAG = dt.timedelta(minutes=5)  # a relaunch commit is made just after the processes were started
LOG_TAIL_BYTES = 256 * 1024


def utc(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=120, check=True).stdout


def git_versions(*paths: str) -> list[dict]:
    """Every committed change to the files under `paths`, on any branch: commit (short), sha, time, path, blob,
    change (A/M/D)."""
    out, cur = [], None
    for line in git("log", "--all", "--format=C %H %cI", "--raw", "--no-abbrev", "--no-renames", "--",
                    *paths).splitlines():
        if line.startswith("C "):
            _, h, tm = line.split()
            cur = (h, tm)
        elif line.startswith(":"):
            meta, path = line.split("\t", 1)
            f = meta.split()
            out.append({"commit": cur[0][:7], "sha": cur[0], "time": cur[1], "path": path, "blob": f[3],
                        "change": f[4][0]})
    return sorted(out, key=lambda v: utc(v["time"]))


def git_objects(names: list[str]) -> dict[str, bytes | None]:
    """Contents of git objects (blob ids or '<commit>:<path>') from one `git cat-file --batch`; None if missing."""
    raw = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(n + "\n" for n in names).encode(),
                         capture_output=True, timeout=300, check=True).stdout
    out, i = {}, 0
    for name in names:  # the batch answers in input order
        nl = raw.index(b"\n", i)
        head = raw[i:nl].decode().split()
        if len(head) != 3:  # '<name> missing' or '<name> ambiguous'
            out[name], i = None, nl + 1
            continue
        size = int(head[2])
        out[name], i = raw[nl + 1:nl + 1 + size], nl + 2 + size
    return out


def processes() -> tuple[dict[int, tuple[float | None, str | None]], dict[str, list[str]], list[int]]:
    """Live processes: pid -> (start time, command line), both None if unreadable; working directory -> commands
    running there; pids whose working directory could not be read."""
    boot = next(float(x.split()[1]) for x in Path("/proc/stat").read_text().splitlines() if x.startswith("btime"))
    tick = os.sysconf("SC_CLK_TCK")
    procs, in_dir, no_cwd = {}, defaultdict(list), []
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            cmd = (p / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
            start = boot + int((p / "stat").read_text().rsplit(")", 1)[1].split()[19]) / tick
        except PermissionError:
            procs[int(p.name)] = (None, None)  # the process exists but cannot be inspected
            continue
        except (OSError, ValueError, IndexError):
            continue  # exited while being read
        procs[int(p.name)] = (start, cmd)
        try:
            in_dir[os.readlink(p / "cwd")].append(Path(cmd.split()[0]).name if cmd else p.name)
        except PermissionError:
            no_cwd.append(int(p.name))
        except OSError:
            pass  # exited while being read
    return procs, in_dir, no_cwd


def owner_state(rec: dict, procs: dict) -> tuple[str, str | None]:
    pid = rec.get("owner_pid")
    if pid is None:
        return ("owner_pid cleared" if rec.get("stale_owner_pid_cleared") else "no owner_pid"), None
    if pid not in procs:
        return "no such process", None
    start, cmd = procs[pid]
    if cmd is None:
        return "owner state unknown (permission denied)", None
    if "python" not in cmd:
        return "pid reused (not Python)", cmd
    if start > utc(rec["created"]).timestamp() + 1:  # `created` is truncated to seconds
        return "pid reused (process started after the record)", cmd
    return "alive", cmd


def owner_of(rec: dict) -> int | None:
    """The process that created the record, also after a recovery cleared its owner_pid."""
    return rec.get("owner_pid") or (rec.get("stale_owner_pid_cleared") or {}).get("old_owner_pid")


def case_of(rid: str) -> str:
    return rid.rsplit("-", 1)[0].split(".")[0]  # child configs are named '<root case>.<suffix>'


def scan_references(ids: set[str]) -> tuple[dict, dict, list, dict, dict]:
    """Run id -> files naming it; unknown run-id-shaped tokens -> files; unreadable JSON; parsed JSON and text per
    file (paths relative to results/)."""
    odd = {i for i in ids if not RUN_ID.fullmatch(i)}  # ids the pattern cannot find: matched as plain substrings
    refs, dangling, unreadable, docs, texts = defaultdict(set), defaultdict(set), [], {}, {}
    for src in SOURCES:
        for f in sorted(p for p in (RESULTS / src).rglob("*") if p.is_file()):
            rel = str(f.relative_to(RESULTS))
            texts[rel] = text = f.read_bytes().decode("utf-8", "replace")
            if f.suffix == ".json":
                try:
                    docs[rel] = json.loads(text)
                except json.JSONDecodeError as e:
                    unreadable.append({"file": rel, "error": str(e)})  # still scanned as text below
            for tok in set(RUN_ID.findall(text)):
                (refs if tok in ids else dangling)[tok].add(rel)
            for rid in odd:
                if rid in text:
                    refs[rid].add(rel)
    return refs, dangling, unreadable, docs, texts


def scan_docs(ids: set[str]) -> dict[str, set[str]]:
    """Run id -> files under DOC_SOURCES that mention it (paths relative to the repository)."""
    odd = {i for i in ids if not RUN_ID.fullmatch(i)}
    out = defaultdict(set)
    for src in DOC_SOURCES:
        root = REPO / src
        for f in sorted([root] if root.is_file() else (p for p in root.rglob("*") if p.is_file())):
            if f.suffix not in DOC_SUFFIXES:
                continue
            text, rel = f.read_text(errors="replace"), str(f.relative_to(REPO))
            for rid in (set(RUN_ID.findall(text)) & ids) | {i for i in odd if i in text}:
                out[rid].add(rel)
    return out


def check_fingerprint_list() -> str:
    """Hash FINGERPRINTED the way systems.decision_code_fingerprint hashes its files; stop if the two differ."""
    sys.path.insert(0, str(REPO / "src"))
    from socrates.orchestration.systems import decision_code_fingerprint  # read-only: hashes files, writes nothing

    h = hashlib.sha256()
    for f in sorted({f for pat in FINGERPRINTED for f in REPO.glob(pat)}):
        h.update(str(f.relative_to(REPO)).encode())
        h.update(f.read_bytes())
    mine, theirs = h.hexdigest()[:16], decision_code_fingerprint()
    if mine != theirs:
        raise SystemExit(f"FINGERPRINTED in scripts/audit_runs.py hashes to {mine}, decision_code_fingerprint() is "
                         f"{theirs}: the file lists differ; update FINGERPRINTED before trusting the event list")
    return theirs


def fingerprint_commits(errors: list[str]) -> list[tuple[dt.datetime, str]]:
    """The commits that added or changed `systems.decision_code_fingerprint`, oldest first."""
    try:
        return sorted((utc(t), h) for h, t in (x.split("\t") for x in git(
            "log", "--format=%h%x09%cI", "-s", "-L", ":".join(FINGERPRINT_FN)).splitlines() if x.strip()))
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        errors.append(f"git log of decision_code_fingerprint failed: {e!r}")
        return []


def events(since: dt.datetime, fp: list[tuple[dt.datetime, str]], errors: list[str]) -> list[dict]:
    """Decision-code commits, relaunch commits and the launch markers in results/logs, from `since` on."""
    out = {}
    try:
        log = git("log", "--all", "--format=%h%x09%cI%x09%s", "--", *FINGERPRINTED)
        out.update({(t, h): {"time": utc(t), "kind": "decision-code commit", "label": f"commit {h}: {s[:90]}",
                             "fingerprint": next((f"{c} definition" for tm, c in sorted(fp, reverse=True)
                                                  if tm <= utc(t)), "none yet" if fp else "unknown"),
                             "sources": ["git log"]}
                    for h, t, s in (x.split("\t", 2) for x in log.splitlines())})
        log = git("log", "--all", "--format=%h%x09%cI%x09%s")
        for h, t, s in (x.split("\t", 2) for x in log.splitlines()):
            if RELAUNCH_SUBJECT.search(s):
                e = out.setdefault((t, h), {"time": utc(t), "kind": "relaunch commit", "label": f"commit {h}: {s[:90]}",
                                            "fingerprint": None, "sources": ["git log"]})
                if e["kind"] != "relaunch commit":
                    e["kind"] += " + relaunch commit"
    except (OSError, subprocess.SubprocessError) as e:
        errors.append(f"git log for events failed: {e!r}")
    for f in sorted((RESULTS / "logs").glob("*.log")):
        for line in f.read_text(errors="replace").splitlines():
            m = MARKER.match(line.strip())
            if m:
                e = out.setdefault((m["time"], m["label"]), {"time": utc(m["time"]), "kind": "launch marker",
                                                             "label": m["label"], "fingerprint": None, "sources": []})
                e["sources"].append(f"logs/{f.name}")
    return sorted((e for e in out.values() if e["time"] >= since), key=lambda e: e["time"])


def logged_results() -> list[dict]:
    """Every '<system> <case> -> <verdict>' line in results/logs, with the launch marker of its section."""
    rows = []
    for f in sorted((RESULTS / "logs").glob("*.log")):
        label, start = "start of file (launch time not logged)", None
        for line in f.read_text(errors="replace").splitlines():
            m = MARKER.match(line.strip())
            if m:
                label, start = m["label"], utc(m["time"])
                continue
            rows += [{"file": f"logs/{f.name}", "section": label, "section_start": start, **r.groupdict()}
                     for r in LOGGED.finditer(line)]
    return rows


def r19_commit(errors: list[str]) -> tuple[str, dt.datetime] | None:
    """The commit that introduced the postProcessing hashes into the run store (R19)."""
    try:
        first = git("log", "--reverse", "-S", "postprocessing_sha256", "--format=%h%x09%cI", "--",
                    "src/socrates/orchestration/store.py").splitlines()
    except (OSError, subprocess.SubprocessError) as e:
        errors.append(f"git log for the R19 commit failed: {e!r}")
        return None
    if not first:
        errors.append("no commit adds postprocessing_sha256 to store.py: R19 commit unknown")
        return None
    h, t = first[0].split("\t")
    return h, utc(t)


def signal_name(rc) -> str:
    if isinstance(rc, int) and rc < 0:
        try:
            return f"{rc} ({signal.Signals(-rc).name})"
        except ValueError:
            return str(rc)
    return str(rc)


def solver_log(rid: str, rec: dict) -> dict:
    """The run's own solver log: for a restart, logs copied from the source case do not count
    (as in RunStore._adopt_orphan). Last 'Time =' and 'ClockTime =' from its tail."""
    case = RUNS / rid / "case"
    solver = ((rec.get("case_config") or {}).get("numerics") or {}).get("solver") or "pimpleFoam"
    logs = sorted(case.glob(f"log.{solver}*")) if case.is_dir() else []
    init = rec.get("initialisation") or {}
    if init.get("kind") == "restart" and init.get("source_run"):
        copied = {x.name for x in (RUNS / init["source_run"] / "case").glob(f"log.{solver}*")}
        logs = [lp for lp in logs if lp.name not in copied]
    if not logs:
        return {"solver_started": False}
    try:
        lp = max(logs, key=lambda x: x.stat().st_mtime)
        with open(lp, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            fh.seek(max(0, fh.tell() - LOG_TAIL_BYTES))
            tail = fh.read().decode(errors="replace")
        times, clock = re.findall(r"^Time = (\S+)", tail, re.M), re.findall(r"ClockTime = ([\d.eE+-]+) s", tail)
        return {"solver_started": True, "solver_logs": [x.name for x in logs], "solver_log": lp.name,
                "last_time_s": float(times[-1]) if times else None,
                "clock_time_s": float(clock[-1]) if clock else None,
                "log_modified": dt.datetime.fromtimestamp(lp.stat().st_mtime, dt.timezone.utc).isoformat(
                    timespec="seconds")}
    except (OSError, ValueError) as e:  # removed or rewritten while read: say so instead of guessing
        return {"solver_started": None, "solver_logs": [x.name for x in logs], "solver_log_error": repr(e)}


def describe(rid: str, rec: dict, runs: dict, procs: dict, in_dir: dict) -> dict:
    """The facts the audit tables need about one run."""
    ev_file, cost = RUNS / rid / "evidence.json", None
    if ev_file.exists():
        try:
            cost = (json.loads(ev_file.read_text()).get("cost") or {}).get("cell_steps")
        except json.JSONDecodeError as e:
            cost = f"evidence.json unreadable: {e}"
    root, missing = rid, None
    for _ in range(len(runs)):
        parent = runs[root].get("parent_run")
        if not parent:
            break
        if parent not in runs:
            missing = parent
            break
        root = parent
    req, hits, bad_hits = RUNS / rid / "requests.jsonl", [], 0
    for line in (req.read_text().splitlines() if req.exists() else []):
        if not line.strip():
            continue
        try:
            hits.append(json.loads(line))
        except json.JSONDecodeError:
            bad_hits += 1  # a line being appended while read; counted, not dropped silently
    exp, fail = rec.get("experiment") or {}, rec.get("failure") or {}
    state, cmd = owner_state(rec, procs)
    return {
        "run_id": rid, "status": rec.get("status"), "launched_by": rec.get("launched_by"),
        "created": rec.get("created"), "finished": rec.get("finished"), "parent_run": rec.get("parent_run"),
        "root_run": root if missing is None else None, "root_case": runs[root]["case_config"].get("name"),
        "missing_ancestor": missing,
        "action": exp.get("action"), "params": exp.get("params"), "launch_reason": rec.get("launch_reason"),
        "failure_kind": rec.get("failure_kind"), "failure_step": fail.get("step"),
        "failure_returncode": fail.get("returncode"),
        "cell_steps": cost, "wall_seconds": rec.get("wall_seconds"),
        "owner_pid": rec.get("owner_pid"), "owner": owner_of(rec), "owner_state": state, "owner_command": cmd,
        "stale_owner_pid_cleared": rec.get("stale_owner_pid_cleared"),
        "adopted_orphan": bool(rec.get("adopted_orphan")),
        "processes_in_case_dir": in_dir.get(str((RUNS / rid / "case").resolve()), []),
        "cache_hits": len(hits), "requests": [{"time": h.get("time"), "launched_by": h.get("launched_by")}
                                              for h in hits],
        "unreadable_request_lines": bad_hits,
        "has_postprocessing_sha256": "postprocessing_sha256" in rec,
        "has_final_fields_sha256": "final_fields_sha256" in rec,
        **(solver_log(rid, rec) if rec.get("status") == "running" else {}),
    }


def store_history(errors: list[str]) -> tuple[dict[str, dict], dict[str, list]]:
    """Committed versions of results/runs/*/run.json: run id -> {created -> attempt}; run id -> deleting commits."""
    try:
        vs = git_versions("results/runs/*/run.json")
        blobs = git_objects(sorted({v["blob"] for v in vs if v["change"] != "D"}))
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        errors.append(f"git history of results/runs/*/run.json unavailable: {e!r}")
        return {}, {}
    attempts, deleted = defaultdict(dict), defaultdict(list)
    for v in vs:
        rid = v["path"].split("/")[2]
        if v["change"] == "D":
            deleted[rid].append({"commit": v["commit"], "time": v["time"]})
            continue
        try:
            rec = json.loads(blobs[v["blob"]])
        except (TypeError, json.JSONDecodeError) as e:
            errors.append(f"{v['path']} at commit {v['commit']} unreadable: {e!r}")
            continue
        a = attempts[rid].setdefault(rec.get("created"), {"run_id": rid, "created": rec.get("created"),
                                                          "first_commit": v["commit"], "owner": None})
        a.update(last_commit=v["commit"], last_sha=v["sha"], last_commit_time=v["time"], status=rec.get("status"),
                 launched_by=rec.get("launched_by"), finished=rec.get("finished"),
                 adopted=bool(rec.get("adopted_orphan")), failure_kind=rec.get("failure_kind"))
        a["owner"] = a["owner"] or owner_of(rec)
        if rec.get("stale_owner_pid_cleared") and "pid_cleared" not in a:
            a["pid_cleared"] = {"commit": v["commit"], "time": v["time"],
                                "reason": rec["stale_owner_pid_cleared"].get("reason")}
    return attempts, deleted


def result_history(errors: list[str]) -> dict[str, list[dict]]:
    """Committed versions of each file under results/benchmark and results/attacks (paths relative to results/)."""
    try:
        vs = git_versions("results/benchmark", "results/attacks")
        blobs = git_objects(sorted({v["blob"] for v in vs if v["change"] != "D"}))
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        errors.append(f"git history of results/benchmark and results/attacks unavailable: {e!r}")
        return {}
    files = defaultdict(list)
    for v in vs:
        raw = None if v["change"] == "D" else blobs[v["blob"]]
        if v["change"] != "D" and raw is None:
            errors.append(f"{v['path']} at commit {v['commit']}: blob missing")
            continue
        text, doc = None if raw is None else raw.decode("utf-8", "replace"), None
        if text is not None and v["path"].endswith(".json"):
            try:
                doc = json.loads(text)
            except json.JSONDecodeError as e:
                errors.append(f"{v['path']} at commit {v['commit']} unreadable: {e}")
        files[v["path"].removeprefix("results/")].append({"commit": v["commit"], "time": v["time"], "text": text,
                                                         "doc": doc})
    return files


def history_of(doc) -> list | None:
    return doc.get("history") if isinstance(doc, dict) and isinstance(doc.get("history"), list) else None


def llm_cost(history: list) -> float:
    return sum(float((e.get("meta") or {}).get("cost_usd") or 0) for e in history if isinstance(e, dict))


def loop_attempts(files: dict, docs: dict, texts: dict, ids: set[str]) -> list[dict]:
    """Split the versions of each partial result (committed, then the working tree) into loop attempts.

    A version continues the attempt when its history extends the previous version's history; anything else is a
    new attempt of the same system and case (the loop started again from the root). An earlier attempt is
    'completed' when some version of the final result carries its history, otherwise 'aborted'."""
    out = []
    for rel in sorted(r for r in set(files) | set(docs) if r.endswith(".partial.json")):
        group, system, name = rel.split("/")
        vers = files.get(rel, []) + ([{"commit": "working tree", "time": None, "text": texts[rel], "doc": docs[rel]}]
                                     if rel in docs else [])
        final_rel = rel.removesuffix(".partial.json") + ".json"
        current_final = history_of(docs.get(final_rel))
        finals = [h for h in (history_of(v["doc"]) for v in files.get(final_rel, [])) if h] + (
            [current_final] if current_final else [])
        attempts, prev = [], None
        for v in vers:
            h = history_of(v["doc"])
            if h is None:
                prev = None  # deleted or unreadable version: the next one starts a new attempt
                continue
            if prev is not None and h[:len(prev)] == prev:
                attempts[-1].append(v)
            else:
                attempts.append([v])
            prev = h
        for i, vs in enumerate(attempts):
            h = history_of(vs[-1]["doc"])
            done = [f for f in finals if h and f[0] == h[0]]
            if i < len(attempts) - 1:
                status = "completed, result later recomputed" if done else "aborted"
            else:
                status = "current, final result" if h and current_final and current_final[0] == h[0] else \
                    "current, no final result"
            out.append({"group": group, "system": system, "case": name.removesuffix(".partial.json"), "file": rel,
                        "commits": [v["commit"] for v in vs], "last_time": vs[-1]["time"],
                        "n_iterations": max([len(h)] + [len(f) for f in done]),
                        "cost_usd": max([llm_cost(h)] + [llm_cost(f) for f in done]), "status": status,
                        "superseded_in": attempts[i + 1][0]["commit"] if i < len(attempts) - 1 else None,
                        "runs_named": sorted({tok for v in vs for tok in RUN_ID.findall(v["text"] or "")} & ids)})
    return out


def owner_processes(acts: list[dict], case_group: dict, procs: dict, evs: list[dict]) -> dict[int, dict]:
    """Per owner pid, over its current and committed records: launchers, groups of cases, first record (`created`)
    and last record (`created`, or `finished` written by the owner itself: an adopted record's finish time is the
    adopter's), its state now and, for a process that is gone, the first later process with a shared launcher on a
    shared group, with the events in between."""
    o = {}
    for a in acts:
        if a["pid"] is None or not a["created"]:
            continue
        d = o.setdefault(a["pid"], {"pid": a["pid"], "launchers": set(), "groups": set(), "records": set(),
                                    "first": None, "last": None})
        c = utc(a["created"])
        d["launchers"].add(a["launched_by"])
        d["groups"].add(case_group.get(case_of(a["run_id"])))
        d["records"].add((a["run_id"], a["created"]))
        d["first"] = c if d["first"] is None else min(d["first"], c)
        d["last"] = max(([d["last"]] if d["last"] else []) + [c] +
                        ([utc(a["finished"])] if a["finished"] and not a["adopted"] else []))
    for d in o.values():
        d["state"], d["command"] = owner_state({"owner_pid": d["pid"], "created": d["first"].isoformat()}, procs)
        d["successor"], d["events_between"] = None, []
        if d["state"] == "alive":
            continue
        later = [q for q in o.values() if q["first"] > d["last"] and q["launchers"] & d["launchers"]
                 and q["groups"] & d["groups"]]
        if later:
            q = min(later, key=lambda q: q["first"])
            d["successor"] = {"pid": q["pid"], "first_record": q["first"]}
            d["events_between"] = [e for e in evs if d["last"] < e["time"] <= q["first"] or (
                "relaunch commit" in e["kind"] and q["first"] < e["time"] <= q["first"] + RELAUNCH_COMMIT_LAG)]
    return o


def last_named(rid: str, rfiles: dict, texts: dict) -> dict | None:
    """The last committed result version that names `rid`, and the version of that file that dropped it."""
    best = None
    for rel, vs in rfiles.items():
        for i, v in enumerate(vs):
            if v["text"] and rid in v["text"] and (best is None or utc(v["time"]) > utc(best[2]["time"])):
                best = (rel, i, v)
    if best is None:
        return None
    rel, i, v = best
    nxt = rfiles[rel][i + 1]["commit"] if i + 1 < len(rfiles[rel]) else (
        "working tree" if rid not in texts.get(rel, "") else None)
    return {"file": rel, "commit": v["commit"], "time": v["time"], "removed_in": nxt}


def table(headers: list[str], rows: list[list]) -> list[str]:
    def cell(c) -> str:
        return "-" if c is None or c == "" else str(c).replace("|", "\\|")

    return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] + \
           ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]


def paren(items) -> str:
    return "" if not items else " (" + "; ".join(items) + ")"


def event(e: dict) -> str:
    return f"{e['label']} ({t(e['time'].isoformat())})"


def short_event(e: dict) -> str:
    return (e["label"].split(":")[0] if e["kind"] != "launch marker" else f"'{e['label']}'") + \
        f" {e['time'].strftime('%H:%M')}"


def t(s) -> str:
    return "-" if not s else str(s)[:16].replace("T", " ")


def files(n: int) -> str:
    return f"{n} file" + ("" if n == 1 else "s")


def run_ids(n: int) -> str:
    return f"{n} run id" + ("" if n == 1 else "s")


def num(x) -> str:
    return f"{x:.3g}" if isinstance(x, (int, float)) else ("-" if x is None else str(x))


def usd(x: float) -> str:
    return f"{x:.3f}"


def action(d: dict) -> str:
    if not d["action"]:
        return "-"
    return d["action"] + ("" if not d["params"] else " " + ",".join(f"{k}={v}" for k, v in d["params"].items()))


def takeover(p: dict | None) -> str | None:
    if p is None:
        return None
    if p["state"] == "alive":
        return f"pid {p['pid']} alive"
    s = p["successor"]
    return f"pid {p['pid']} last record {t(p['last'].isoformat())}; " + (
        "no later process" if s is None else f"pid {s['pid']} from {t(s['first_record'].isoformat())}")


def cells(x) -> float:
    return x if isinstance(x, (int, float)) else 0


def no_count_note(a: dict) -> str:
    """Why a finished earlier attempt has no cell-step count. An attempt adopted with 0 solver steps of its own ran no
    solver: its committed wall time and step count come from the log copied from its restart source."""
    ec = a.get("evidence_cost") or {}
    if ec.get("n_steps") == 0:
        return ("0 own solver steps; adopted without solver output of its own (wall time and steps in its evidence "
                "come from the log copied from its source)")
    return f"no cell-step count, wall {num(ec.get('wall_seconds'))} s"


def main() -> int:
    fingerprint = check_fingerprint_list()
    runs, bad_records = {}, []
    for d in sorted(p for p in RUNS.iterdir() if p.is_dir() and not p.name.startswith(".")):
        try:
            runs[d.name] = json.loads((d / "run.json").read_text())
        except (OSError, json.JSONDecodeError) as e:
            bad_records.append({"run_dir": d.name, "error": repr(e)})
    ids = set(runs)
    procs, in_dir, no_cwd = processes()
    refs, dangling, unreadable, docs, texts = scan_references(ids)
    mentions = scan_docs(ids)
    git_errors = []
    hist, deleted = store_history(git_errors)
    rfiles = result_history(git_errors)
    info = {rid: describe(rid, rec, runs, procs, in_dir) for rid, rec in runs.items()}
    children = defaultdict(list)
    for rid, d in info.items():
        d["referenced_by"] = sorted(refs.get(rid, ()))
        if not d["referenced_by"] and d["launched_by"] in STUDY_LAUNCHERS:
            d["referenced_by"] = [f"baseline study ({STUDY_LAUNCHERS[d['launched_by']]})"]
        d["referenced_only_by_partial"] = bool(refs.get(rid)) and all(f.endswith(".partial.json") for f in refs[rid])
        d["mentioned_in"] = sorted(mentions.get(rid, ()))
        d["pid_cleared_in"] = (hist.get(rid, {}).get(d["created"]) or {}).get("pid_cleared")
        if d["parent_run"]:
            children[d["parent_run"]].append(rid)

    # systems per (group, planner), and which cases have a final result per system
    systems, finals = defaultdict(set, {k: set(v) for k, v in EXTRA_SYSTEMS.items()}), defaultdict(set)
    for rel, doc in docs.items():
        parts = rel.split("/")
        if parts[0] in ("benchmark", "attacks") and len(parts) == 3 and not rel.endswith(".partial.json"):
            finals[(parts[0], parts[1])].add(Path(parts[2]).stem)
            if isinstance(doc, dict) and doc.get("planner"):
                systems[(parts[0], doc["planner"])].add(parts[1])
    case_group = {c: g for (g, _), cases in finals.items() for c in cases}
    for d in info.values():
        g = case_group.get(d["root_case"])
        d["systems_without_final_result"] = sorted(s for s in systems.get((g, d["launched_by"]), ())
                                                   if d["root_case"] not in finals[(g, s)])

    created_all = [utc(r["created"]) for r in runs.values() if r.get("created")] + \
                  [utc(c) for a in hist.values() for c in a if c]
    t0 = min(created_all) if created_all else dt.datetime.now(dt.timezone.utc)
    fp = fingerprint_commits(git_errors)
    evs = events(t0, fp, git_errors)
    r19 = r19_commit(git_errors)

    # owner processes over current and committed records
    acts = [{"pid": owner_of(r), "run_id": rid, "launched_by": r.get("launched_by"), "created": r.get("created"),
             "finished": r.get("finished"), "adopted": bool(r.get("adopted_orphan"))} for rid, r in runs.items()]
    acts += [{"pid": a["owner"], "run_id": a["run_id"], "launched_by": a["launched_by"], "created": a["created"],
              "finished": a["finished"], "adopted": a["adopted"]} for v in hist.values() for a in v.values()]
    owners = owner_processes(acts, case_group, procs, evs)
    live = {p: o for p, o in owners.items() if o["state"] == "alive"}

    # earlier attempts under a current run id, and records deleted outright (committed versions of run.json)
    earlier = {rid: sorted((a for c, a in v.items() if c != (runs.get(rid) or {}).get("created")),
                           key=lambda a: a["created"] or "") for rid, v in hist.items()}
    earlier = {rid: v for rid, v in earlier.items() if v}
    finished_earlier = [a for v in earlier.values() for a in v if a["status"] != "running"]
    if finished_earlier:
        try:
            evid = git_objects([f"{a['last_sha']}:results/runs/{a['run_id']}/evidence.json"
                                for a in finished_earlier])
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            evid = {}
            git_errors.append(f"committed evidence.json of replaced attempts unavailable: {e!r}")
        for a in finished_earlier:
            raw = evid.get(f"{a['last_sha']}:results/runs/{a['run_id']}/evidence.json")
            try:
                a["evidence_cost"] = None if raw is None else json.loads(raw).get("cost") or {}
                a["cell_steps"] = None if raw is None else a["evidence_cost"].get("cell_steps")
            except json.JSONDecodeError as e:
                a["cell_steps"] = f"committed evidence.json unreadable: {e}"
    for p, o in owners.items():
        o["earlier_attempts"] = sum(a["owner"] == p for v in earlier.values() for a in v)
    gone = {rid: v for rid, v in deleted.items() if rid not in runs}

    # loop attempts from the committed and current partial results
    attempts = loop_attempts(rfiles, docs, texts, ids)
    superseded = [a for a in attempts if not a["status"].startswith("current")]

    for d in info.values():
        o = owners.get(d["owner"])
        d["owner_process"] = None if o is None else {
            "pid": o["pid"], "state": o["state"], "last_record": o["last"].isoformat(),
            "successor": None if not o["successor"] else {
                "pid": o["successor"]["pid"], "first_record": o["successor"]["first_record"].isoformat()},
            "events_between": [event(e) for e in o["events_between"]]}

    unref = [d for d in info.values() if not d["referenced_by"]]
    for d in unref:
        if not d["parent_run"]:  # an unnamed root: is another root of the same case name in use?
            d["same_name_roots_in_use"] = sorted(o["run_id"] for o in info.values() if o["referenced_by"] and
                                                 not o["parent_run"] and o["root_case"] == d["root_case"])
        hit = next(((p, r["time"]) for r in d["requests"] for p, o in sorted(live.items())
                    if r.get("time") and r.get("launched_by") in o["launchers"]
                    and procs[p][0] is not None and utc(r["time"]).timestamp() >= procs[p][0]), None)
        child = next((c for c in children.get(d["run_id"], ()) if info[c]["owner_state"] == "alive"), None)
        d["in_use"] = "live owner" if d["owner_state"] == "alive" else (
            f"cache hit by live pid {hit[0]} at {t(hit[1])}" if hit else (
                f"parent of {child} (live owner)" if child else None))
        d["last_named_in_git"] = last_named(d["run_id"], rfiles, texts)
        if d["last_named_in_git"]:
            ln = d["last_named_in_git"]
            d["loop_attempt"] = next(({k: a[k] for k in ("system", "case", "status", "n_iterations", "cost_usd",
                                                          "superseded_in")}
                                      for a in attempts if a["file"] == ln["file"] and ln["commit"] in a["commits"]),
                                     None)
    running = [d for d in info.values() if d["status"] == "running"]
    orphaned = [d for d in running if d["owner_state"] != "alive"]
    orphan_ran = [d for d in orphaned if d.get("solver_started")]
    orphan_never = [d for d in orphaned if d.get("solver_started") is False]
    orphan_unknown = [d["run_id"] for d in orphaned if d.get("solver_started") is None]
    failed = [d for d in info.values() if d["status"] == "failed"]
    unhashed = [d for d in info.values() if d["status"] != "running"
                and not (d["has_postprocessing_sha256"] and d["has_final_fields_sha256"])]
    for d in unhashed:
        d["created_before_r19_commit"] = None if r19 is None else utc(d["created"]) < r19[1]
    straddle = [d for d in unhashed if r19 and d["created_before_r19_commit"] and d["finished"]
                and utc(d["finished"]) > r19[1]]
    llm_unref = [d for d in unref if LLM_LAUNCHER.search(d["launched_by"] or "")]
    llm_dead = [d for d in llm_unref if d["owner_state"] != "alive"]
    llm_live = [d for d in llm_unref if d["owner_state"] == "alive"]
    llm_named = [d for d in llm_dead if d["last_named_in_git"]]
    llm_taken = [d for d in llm_dead if (d["owner_process"] or {}).get("successor")]
    logged = logged_results()
    llm_systems = set().union(*(v for (g, p), v in systems.items() if LLM_LAUNCHER.search(p)))
    for d in llm_unref:
        c = utc(d["created"])
        later = {(r["system"], r["section"], t(r["section_start"].isoformat()), r["file"]) for r in logged
                 if r["system"] in llm_systems and r["case"] == d["root_case"] and r["section_start"]
                 and r["section_start"] > c}
        d["llm_results_logged_after_creation"] = [f"{s} after '{lab}' ({tm}, {f})" for s, lab, tm, f in sorted(
            later, key=lambda x: x[2])]
    missing_parents = [{"run_id": d["run_id"], "missing_ancestor": d["missing_ancestor"]} for d in info.values()
                       if d["missing_ancestor"]]

    all_cost = sum(cells(d["cell_steps"]) for d in info.values())
    unref_cost, idle_cost = Counter(), Counter()
    for d in unref:
        unref_cost[d["launched_by"]] += cells(d["cell_steps"])
        if not d["in_use"]:
            idle_cost[d["launched_by"]] += cells(d["cell_steps"])
    idle_doc = [d for d in unref if not d["in_use"] and d["mentioned_in"] and cells(d["cell_steps"])]
    earlier_cost = sum(cells(a.get("cell_steps")) for a in finished_earlier)
    llm_superseded = [a for a in superseded if LLM_LAUNCHER.search(a["system"])]
    named_attempts = {(a["file"], a["commits"][-1]): a for a in llm_superseded
                      if set(a["runs_named"]) & {d["run_id"] for d in llm_dead}}
    bad_req = sum(d["unreadable_request_lines"] for d in info.values())

    not_named = [d for d in llm_dead if not d["last_named_in_git"]]
    n_logged = sum(bool(d.get("llm_results_logged_after_creation")) for d in llm_dead)
    dead_running = [d for d in llm_dead if d["status"] == "running"]
    note = (f"{len(llm_dead)} runs launched by the LLM planner are named by no current result and have no live owner "
            f"process. For {len(llm_taken)} of them the store shows when the owner process stopped writing records and "
            "which later process took over the same launcher on the same group of cases (columns 'owner' and 'taken "
            "over by'; the commits and launch markers in between are under 'Owner processes'). "
            f"{len(llm_named)} of them are named by a committed version of a partial result that a later loop attempt "
            "of the same system and case replaced (columns 'last named in' and 'removed in'); "
            + (f"the other {len(not_named)} are 'running' records that never finished, and a loop names a run only "
               "after it has run. " if all(d["status"] == "running" for d in not_named) else
               f"no committed result names {', '.join(d['run_id'] for d in not_named)}. ")
            + f"For {n_logged} of the {len(llm_dead)}, a result for the same case was logged by a process launched "
            "after the run was created (run_audit.json, `llm_results_logged_after_creation`). "
            + ("They come from loop attempts that ended with their owner process, after which a later process ran "
               "the case again from the root. " if n_logged == len(llm_taken) == len(llm_dead) else
               "Where both the takeover and a later logged result are found, the run comes from a loop attempt that "
               "ended with its owner process and was run again from the root by a later process; for the others the "
               "store and the logs do not show this. ")
            + "The planner calls that proposed them, and their LLM cost, are not in any current result; lower "
            f"bounds for {len(llm_named)} of them are in committed partial files: "
            f"{usd(sum(a['cost_usd'] for a in named_attempts.values()))} USD over "
            f"{sum(a['n_iterations'] for a in named_attempts.values())} planner iterations in {len(named_attempts)} "
            "superseded attempts (all superseded loop attempts are listed under 'Superseded loop attempts'). Their "
            f"simulation cost recorded in evidence.json is {num(sum(cells(d['cell_steps']) for d in llm_dead))} "
            f"cell-steps. Of the {len(dead_running)} 'running' records among them, "
            f"{sum(d.get('solver_started') is False for d in dead_running)} never started their solver"
            + "".join(f"; {d['run_id']} ran it for {num(d.get('clock_time_s'))} s of wall time (log last written "
                      f"{t(d.get('log_modified'))}), recorded only in its solver log"
                      for d in dead_running if d.get("solver_started"))
            + f". {len(llm_live)} further unnamed LLM-planner runs have a live owner: their loops are still running, "
            "and a loop names a run in its partial file once the run has finished.")

    def jtime(o):
        return o.isoformat() if isinstance(o, dt.datetime) else (sorted(o, key=str) if isinstance(o, set) else str(o))

    out = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "decision_code_fingerprint": fingerprint,
        "sources": [f"results/{s}" for s in SOURCES], "n_source_files": len(texts),
        "doc_sources": DOC_SOURCES,
        "n_runs": len(runs), "by_status": dict(Counter(d["status"] for d in info.values())),
        "unreadable_run_records": bad_records, "unreadable_result_files": unreadable,
        "unreadable_request_lines": bad_req, "git_errors": git_errors,
        "processes_with_unreadable_cwd": no_cwd,
        "dangling_references": {k: sorted(v) for k, v in sorted(dangling.items())},
        "missing_ancestors": missing_parents,
        "r19_commit": None if r19 is None else {"commit": r19[0], "time": r19[1].isoformat()},
        "events": evs,
        "cell_steps": {"all_runs": all_cost, "unreferenced_by_launcher": dict(unref_cost),
                       "unreferenced_no_live_user_by_launcher": dict(idle_cost),
                       "replaced_finished_attempts_in_git": earlier_cost},
        "unreferenced": sorted(d["run_id"] for d in unref),
        "orphaned": sorted(d["run_id"] for d in orphaned),
        "failed": sorted(d["run_id"] for d in failed),
        "without_r19_hashes": sorted(d["run_id"] for d in unhashed),
        "referenced_only_by_partial": sorted(d["run_id"] for d in info.values() if d["referenced_only_by_partial"]),
        "llm_planner_unreferenced": {"note": note, "no_live_owner": sorted(d["run_id"] for d in llm_dead),
                                     "live_owner": sorted(d["run_id"] for d in llm_live)},
        "loop_attempts": attempts,
        "owner_processes": {str(p): o for p, o in sorted(owners.items())},
        "git_history": {"earlier_attempts": earlier, "deleted_records": deleted, "deleted_not_in_store": gone},
        "runs": info,
    }
    dest = RESULTS / "analysis"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "run_audit.json").write_text(json.dumps(out, indent=1, default=jtime))

    by_status = Counter(d["status"] for d in info.values())
    by_launcher, unref_groups = defaultdict(Counter), defaultdict(Counter)
    for d in info.values():
        by_launcher[d["launched_by"]][d["status"]] += 1
    for d in unref:
        unref_groups[d["launched_by"]][d["status"]] += 1
    statuses = sorted(by_status)
    L = ["# Run store audit", "",
         f"Generated by `scripts/audit_runs.py` at {out['generated']}; see the script docstring for the rules. "
         "Read-only. " + ("Owner processes were still running (see 'Running records'), so this is a snapshot."
                          if live else "No owner process of a 'running' record was alive.")
         + f" Decision-code fingerprint of the working tree: {fingerprint}.", "",
         "## Coverage", "",
         "- The store keeps one record per run id. `RunStore.get_or_run` deletes a 'running' record whose owner "
         "died and runs it again under the same id, and records were also deleted by hand; current records show "
         "neither. 'Earlier attempts in git history' lists what the committed versions of run.json show.",
         "- The git history holds committed snapshots only. An attempt that started and was removed between two "
         "commits, and loop iterations after a loop's last committed partial result, leave no trace, so costs "
         "taken from the git history are lower bounds.",
         "- Cell-steps come from evidence.json: current records, and the committed evidence of replaced attempts "
         "that had finished. A run that never finished has no evidence file; its compute is not recorded."]
    if git_errors:
        L += [f"- **Incomplete**: {'; '.join(git_errors)}."]
    L += ["", "## Runs by launcher and status", ""]
    L += table(["launched_by", *statuses, "total"],
               [[k, *(v[s] for s in statuses), sum(v.values())]
                for k, v in sorted(by_launcher.items(), key=lambda x: str(x[0]))] +
               [["**all**", *(by_status[s] for s in statuses), len(runs)]])
    n_study = sum(bool(d["referenced_by"]) and d["referenced_by"][0].startswith("baseline study (")
                  for d in info.values())
    n_ref = sum(bool(d["referenced_by"]) for d in info.values()) - n_study
    u_cost, i_cost = sum(unref_cost.values()), sum(idle_cost.values())
    L += ["", "## References", "",
          f"- {len(texts)} files scanned under {', '.join(out['sources'])}; mentions outside results looked up in "
          f"{', '.join(DOC_SOURCES)}.",
          f"- {n_ref} runs are named by a stored result; {len(out['referenced_only_by_partial'])} of them only by "
          f"`*.partial.json` files (listed at the end); {n_study} more are counted as used by the baseline study "
          "through their launcher.",
          f"- {len(unref)} runs are named by no stored result.",
          f"- Unreadable run records: {len(bad_records)}{paren([b['run_dir'] for b in bad_records])}; unreadable "
          f"JSON result files: {len(unreadable)}{paren([u['file'] for u in unreadable])}; unparsable "
          f"requests.jsonl lines: {bad_req}.",
          f"- Run-id-shaped strings in results that name no run in the store: {len(dangling)}"
          + paren([f"{k} in {', '.join(sorted(v))}" for k, v in sorted(dangling.items())]) + ".",
          f"- Runs whose parent chain leads to a run missing from the store: {len(missing_parents)}"
          + paren([f"{m['run_id']} -> {m['missing_ancestor']}" for m in missing_parents]) + "."]
    if all_cost:
        L += [f"- Cell-steps in the evidence.json of current records: {num(all_cost)} for all runs, {num(u_cost)} "
              f"({100 * u_cost / all_cost:.1f} %) for runs no result names"
              + paren([f"{k}: {num(v)}" for k, v in sorted(unref_cost.items())]) + ". "
              f"{num(u_cost - i_cost)} of that is in runs a live process uses (live owner, a cache hit by a live "
              f"process, or the parent of a run with a live owner) and {num(i_cost)} ({100 * i_cost / all_cost:.1f} "
              "% of all) in runs with no live user"
              + paren([f"{k}: {num(v)}" for k, v in sorted(idle_cost.items()) if v]) + "; "
              + ("; ".join(f"{d['run_id']} ({num(d['cell_steps'])}) is documented in {', '.join(d['mentioned_in'])}"
                           for d in idle_doc) or "none of it is documented outside results") + ".",
              f"- Replaced attempts that had finished, from their committed evidence.json: {num(earlier_cost)} "
              f"cell-steps over {sum(1 for a in finished_earlier if cells(a.get('cell_steps')))} attempts"
              + paren([f"{a['run_id']} created {t(a['created'])}: {no_count_note(a)}" for a in finished_earlier
                       if not cells(a.get("cell_steps"))])
              + " (see 'Earlier attempts in git history'). This is in addition to the figures above, which cover "
              "current records only."]
    else:
        L += ["- No cell-steps recorded."]

    L += ["", "## Runs no stored result names", ""]
    ustat = sorted({d["status"] for d in unref})
    L += table(["launched_by", *ustat, "total"], [[k, *(v[s] for s in ustat), sum(v.values())]
                                                  for k, v in sorted(unref_groups.items(), key=lambda x: str(x[0]))])
    L += ["", "Owner: state of the process in `owner_pid` (see 'Running records'). In use: the run has a live owner, "
          "a live process requested it after starting (cache hit), or it is the parent of a run with a live owner. "
          "Pending: systems of this launcher with no final result for the run's case yet; a pending system that "
          "requests the same configuration gets the stored run (cache hit) and names it in its result. Mentioned "
          "in: files outside results that name the run. Owner stopped: the owner's last record and the first record "
          "of the process that took over its launcher (see 'Owner processes').", ""]
    for lb in sorted(unref_groups, key=str):
        L += [f"### {lb}", ""]
        rows = sorted((d for d in unref if d["launched_by"] == lb), key=lambda d: (d["status"], d["created"]))
        L += table(["run", "status", "created", "parent", "experiment", "failure", "cell-steps", "owner", "in use",
                    "cache hits", "pending", "mentioned in", "owner stopped"],
                   [[d["run_id"], d["status"], t(d["created"]), d["parent_run"], action(d),
                     None if not d["failure_kind"] else
                     f"{d['failure_kind']}: {d['failure_step']} rc {signal_name(d['failure_returncode'])}",
                     num(d["cell_steps"]), d["owner_state"], d["in_use"] or "no", d["cache_hits"],
                     ", ".join(d["systems_without_final_result"]), ", ".join(d["mentioned_in"]),
                     takeover(owners.get(d["owner"]))] for d in rows])
        L += [""] + [f"Root {d['run_id']} is unnamed; root runs of the same case name in use: "
                     f"{', '.join(d['same_name_roots_in_use']) or 'none'}"
                     + (f"; documented in {', '.join(d['mentioned_in'])}" if d["mentioned_in"] else "") + ".\n"
                     for d in rows if "same_name_roots_in_use" in d]

    L += ["## Running records", "",
          f"{len(running)} records have status 'running'; {len(orphaned)} are orphaned (no owner_pid or a cleared one, "
          "no such process, not a Python process, or a process that started after the record was written). Of the "
          "orphaned records, "
          f"{len(orphan_never)} never started their solver (no solver log of their own; for a restart, "
          f"logs copied from the source case do not count) and {len(orphan_ran)} did"
          + paren([f"{d['run_id']}: ClockTime {num(d.get('clock_time_s'))} s, last Time {num(d.get('last_time_s'))} "
                   f"s, log last written {t(d.get('log_modified'))}" for d in orphan_ran])
          + ("; that compute is recorded only in the solver log" if orphan_ran else "")
          + ("" if not orphan_unknown else f"; the solver log of {', '.join(orphan_unknown)} could not be read")
          + ". A later request for the same configuration adopts "
          "an orphan whose solver finished, or deletes and re-runs it (`RunStore.get_or_run`); until then the "
          "record stays as it is. Pid cleared: the reason is the label written when the pid was cleared, and the "
          "commit is the first that shows it; the label is not the cause of the owner's death (see 'Owner "
          "processes'). Processes in case dir: processes whose working directory is the run's case directory."
          + (f" The working directory of pid {', '.join(map(str, no_cwd))} could not be read, so that column "
             "may be incomplete." if no_cwd else ""), ""]
    L += table(["run", "launched_by", "created", "owner_pid", "owner", "pid cleared", "own solver log",
                "last Time (s)", "ClockTime (s)", "log written", "processes in case dir", "named by"],
               [[d["run_id"], d["launched_by"], t(d["created"]), d["owner_pid"], d["owner_state"],
                 None if not (c := d["stale_owner_pid_cleared"]) else
                 f"old pid {c.get('old_owner_pid')}: '{c.get('reason')}'"
                 + ("" if not (pc := d["pid_cleared_in"]) else f" ({pc['commit']}, {t(pc['time'])})"),
                 d.get("solver_log") or ("unreadable" if d.get("solver_log_error") else "none"),
                 num(d.get("last_time_s")), num(d.get("clock_time_s")),
                 t(d.get("log_modified")), ", ".join(d["processes_in_case_dir"]), len(d["referenced_by"])]
                for d in sorted(running, key=lambda d: (d["owner_state"] == "alive", d["created"]))])
    lo = sorted({(d["owner_pid"], d["owner_command"]) for d in running if d["owner_state"] == "alive"}, key=str)
    if lo:
        L += ["", "Live owners: " + "; ".join(f"pid {p}: `{c}`" for p, c in lo) + "."]

    L += ["", "## Failed runs", ""]
    L += table(["run", "launched_by", "created", "kind", "step", "returncode", "parent", "experiment", "named by",
                "mentioned in"],
               [[d["run_id"], d["launched_by"], t(d["created"]), d["failure_kind"], d["failure_step"],
                 signal_name(d["failure_returncode"]), d["parent_run"], action(d),
                 files(len(d["referenced_by"]))
                 + paren(sorted({"/".join(f.split("/")[:2]) for f in d["referenced_by"]})),
                 ", ".join(d["mentioned_in"])]
                for d in sorted(failed, key=lambda d: d["created"])])

    L += ["", "## Finalized runs without postProcessing and final-field hashes", "",
          "R19 (docs/methodology.md) added SHA-256 hashes of the postProcessing outputs and of the retained final "
          "fields to the run record when a run is finalized"
          + ("" if r19 is None else f" (commit {r19[0]}, {t(r19[1].isoformat())} UTC)") + ". A record without them "
          "that was created before that commit was written by older code (a long-running process keeps the code it "
          "loaded at start); code from that commit on omits them only when the run wrote no postProcessing output "
          "or no time directory."
          + ("" if not straddle else " Created before the commit and finished after it: "
             + ", ".join(f"{d['run_id']} (finished {t(d['finished'])})" for d in straddle)
             + "; the processes that created them had started before the commit."), ""]
    L += table(["run", "status", "launched_by", "root", "created", "finished", "created before R19 commit", "named by"],
               [[d["run_id"], d["status"], d["launched_by"], "yes" if not d["parent_run"] else "no", t(d["created"]),
                 t(d["finished"]), {True: "yes", False: "no"}.get(d["created_before_r19_commit"]),
                 files(len(d["referenced_by"]))]
                for d in sorted(unhashed, key=lambda d: d["created"])])

    L += ["", "## Unnamed runs launched by the LLM planner", "", note, ""]
    L += table(["run", "status", "created", "owner", "taken over by", "own solver log", "last named in",
                "removed in", "that attempt: iterations, cost_usd"],
               [[d["run_id"], d["status"], t(d["created"]),
                 f"pid {d['owner']}, " + ("alive" if d["owner_state"] == "alive" else f"{d['owner_state']}") + (
                     "" if not (op := d["owner_process"]) or op["state"] == "alive" else
                     f"; last record {t(op['last_record'])}"),
                 None if not op or not op["successor"] else
                 f"pid {op['successor']['pid']} from {t(op['successor']['first_record'])}",
                 None if d["status"] != "running" else (d.get("solver_log") or "none"),
                 None if not (ln := d["last_named_in_git"]) else f"{ln['file']} at {ln['commit']}",
                 None if not ln else ln["removed_in"],
                 None if not (la := d.get("loop_attempt")) else
                 f"{la['n_iterations']}, {usd(la['cost_usd'])} ({la['status']})"]
                for d in sorted(llm_unref, key=lambda d: (d["owner_state"] == "alive", d["created"]))])

    L += ["", "## Superseded loop attempts", "",
          "Versions of a partial result (committed, then the working tree) are split into loop attempts: a version "
          "continues an attempt when its history extends the previous version's, otherwise a new attempt of the "
          "same system and case has started from the root. An attempt is 'completed' when a committed or current "
          "final result carries its history, otherwise 'aborted'. Iterations and cost_usd come from the attempt's "
          "last committed version (or the final result that carries it) and are lower bounds for an aborted "
          f"attempt. {len(llm_superseded)} superseded LLM loop attempts recorded "
          f"{usd(sum(a['cost_usd'] for a in llm_superseded))} USD over "
          f"{sum(a['n_iterations'] for a in llm_superseded)} planner iterations; no current result holds that cost. "
          f"{sum(1 for a in attempts if a['status'].startswith('current'))} attempts are current "
          f"({sum(a['status'] == 'current, final result' for a in attempts)} with a final result).", ""]
    unref_ids = {d["run_id"] for d in unref}
    L += table(["system", "case", "committed versions", "iterations", "cost_usd", "status", "superseded in",
                "runs named that no current result names"],
               [[a["system"], a["case"], (a["commits"][0] if len(a["commits"]) == 1 else
                                          f"{a['commits'][0]}..{a['commits'][-1]}") + f" ({t(a['last_time'])})",
                 a["n_iterations"], usd(a["cost_usd"]) if LLM_LAUNCHER.search(a["system"]) else "-", a["status"],
                 a["superseded_in"], ", ".join(sorted(set(a["runs_named"]) & unref_ids))]
                for a in sorted(superseded, key=lambda a: (a["group"], a["system"], a["case"], a["last_time"]))])

    L += ["", "## Owner processes", "",
          "Every pid that owns a current or committed run record. Last record: the latest `created`, or `finished` "
          "written by the owner itself (an adopted record's finish time is the adopter's). Taken over by: the first "
          "process that shares a launcher and a group of cases and whose first record is later than this one's last "
          f"record. Events: decision-code commits, relaunch commits and launch markers in that interval, and relaunch "
          f"commits up to {int(RELAUNCH_COMMIT_LAG.total_seconds() // 60)} min after the next process's first record "
          "(such a commit records a relaunch already made). A commit stops no process; a stored benchmark result "
          "stamped with another decision-code fingerprint is recomputed by the next process that runs the "
          "benchmark script" + (f" (the fingerprint and that resume check exist from commit {fp[0][1]}, "
                                f"{t(fp[0][0].isoformat())})" if fp else "") + ".", ""]
    L += table(["pid", "launchers", "cases", "records", "first record", "last record", "state now", "taken over by",
                "events in between", "earlier attempts in git", "unnamed current records"],
               [[p, ", ".join(sorted(map(str, o["launchers"]))), ", ".join(sorted(map(str, o["groups"]))),
                 len(o["records"]), t(o["first"].isoformat()), t(o["last"].isoformat()), o["state"],
                 None if not o["successor"] else
                 f"pid {o['successor']['pid']} from {t(o['successor']['first_record'].isoformat())}",
                 ", ".join(short_event(e) for e in o["events_between"]), o["earlier_attempts"],
                 sum(d["owner"] == p for d in unref)]
                for p, o in sorted(owners.items(), key=lambda x: x[1]["first"])])

    n_earlier = sum(len(v) for v in earlier.values())
    n_cur = sum(len(v) for rid, v in earlier.items() if rid in runs)
    L += ["", "## Earlier attempts in git history", "",
          f"Committed versions of run.json hold {n_earlier} attempts that are not the current record: {n_cur} under "
          f"{run_ids(sum(rid in runs for rid in earlier))} in the store (a `created` time different from the current "
          f"record's) and {n_earlier - n_cur} under {run_ids(sum(rid not in runs for rid in earlier))} no longer in "
          "the store. Their last committed status: "
          + ", ".join(f"{k} {v}" for k, v in sorted(Counter(a["status"] for v in earlier.values()
                                                             for a in v).items())) + ". "
          "`RunStore.get_or_run` has reused completed records in every committed version, and deletes and re-runs "
          "a 'running' record whose owner died (the current code first tries to adopt it); a replaced record whose "
          "last committed status is 'completed' was therefore removed outside get_or_run. A record last committed "
          "as 'running' may have finished before it was removed. Recorded cell-steps of replaced attempts that had "
          f"finished: {num(earlier_cost)}.", ""]
    L += table(["run", "current record", "earlier attempts: created, owner pid, launched_by, last committed status "
                "(commits)"],
               [[rid, None if rid not in runs else f"{t(runs[rid].get('created'))}, pid {owner_of(runs[rid])}",
                 "; ".join(f"{t(a['created'])}, " + ("no pid" if a["owner"] is None else f"pid {a['owner']}")
                           + f", {a['launched_by']}, {a['status']}" + (
                               f" ({num(a['cell_steps'])} cell-steps)" if cells(a.get("cell_steps")) else
                               f" ({no_count_note(a)})" if a.get("evidence_cost") is not None else "")
                           + f" ({a['first_commit']}" + ("" if a["first_commit"] == a["last_commit"] else
                                                          f"..{a['last_commit']}") + ")" for a in v)]
                for rid, v in sorted(earlier.items())])
    L += ["", f"Records deleted in a commit (the path is absent from that commit): {run_ids(len(deleted))}, "
          f"{len(gone)} of them not in the store now.", ""]
    L += table(["run", "deleted in", "in the store now"],
               [[rid, ", ".join(f"{x['commit']} ({t(x['time'])})" for x in v),
                 "no" if rid not in runs else f"yes, created {t(runs[rid].get('created'))}"]
                for rid, v in sorted(deleted.items())])

    L += ["", "## Events", "",
          "Commits that changed a file in today's fingerprinted set, relaunch commits (subject mentions a "
          "relaunch, a launch, a resume or a container restart) and launch markers in results/logs. Fingerprint: "
          "the `decision_code_fingerprint` definition in force at the commit ('none yet' before it existed).", ""]
    L += table(["time (UTC)", "kind", "event", "fingerprint", "source"],
               [[t(e["time"].isoformat()), e["kind"], e["label"], e["fingerprint"], ", ".join(e["sources"])]
                for e in evs])

    L += ["", "## Runs named only by partial files", ""]
    L += table(["run", "status", "launched_by", "files"],
               [[d["run_id"], d["status"], d["launched_by"], ", ".join(d["referenced_by"])]
                for d in sorted(info.values(), key=lambda d: d["run_id"]) if d["referenced_only_by_partial"]])
    (dest / "run_audit.md").write_text("\n".join(L) + "\n")

    groups = ", ".join(f"{k}: {sum(v.values())}" for k, v in sorted(unref_groups.items(), key=lambda x: str(x[0])))
    print(f"{len(runs)} runs ({', '.join(f'{by_status[s]} {s}' for s in statuses)}); {len(unref)} named by no result "
          f"({groups}; {num(i_cost)} cell-steps with no live user); {len(orphaned)} orphaned running records "
          f"({len(orphan_never)} never started their solver); {len(failed)} failed "
          f"({sum(1 for d in failed if not d['referenced_by'])} named by no result); "
          f"{len(unhashed)} without R19 hashes; {len(llm_dead)} unnamed LLM-planner runs without a live owner "
          f"({len(llm_named)} named in a superseded committed partial), {len(llm_live)} in progress; "
          f"{len(llm_superseded)} superseded LLM loop attempts in git (>= "
          f"{usd(sum(a['cost_usd'] for a in llm_superseded))} USD); {n_cur} earlier attempts under "
          f"{sum(rid in runs for rid in earlier)} current run ids in git, run ids deleted outright: {len(gone)}; "
          f"{len(dangling)} dangling references")
    problems = [f"{len(bad_records)} unreadable run records"] * bool(bad_records) + \
               [f"{len(unreadable)} unreadable result files"] * bool(unreadable) + \
               [f"{len(dangling)} dangling run-id references"] * bool(dangling) + git_errors
    if problems:
        print("audit incomplete or inconsistent: " + "; ".join(problems), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
