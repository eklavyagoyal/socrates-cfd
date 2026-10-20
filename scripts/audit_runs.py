"""Audit the run store against the stored results, so that no failed or abandoned run is hidden.

Every simulation is a directory in results/runs/ with a provenance record (run.json). A run counts as used when a
stored result names it: any file under results/benchmark, results/attacks (final and *.partial.json),
results/baseline, results/posthoc or results/reproducibility that contains its run id. Runs launched by the baseline
study (launched_by 'baseline_study' or 'farfield_test') count as used by that study. The audit reports:

- every run by status and launcher;
- runs that no stored result names, with creation time, parent, experiment, failure and cost;
- 'running' records whose owner process is gone (orphaned): no owner_pid, no such process, not a Python process, or a
  process that started after the record was written (a pid reused after a container restart);
- failed runs, with the failure kind and the results that name them;
- finalized runs without postProcessing/final-field hashes (written by code older than R19, docs/methodology.md);
- run-id-shaped strings in results that name no run in the store, and parents missing from the store.

Unnamed runs launched by the LLM planner are placed against the events that restart LLM loops: commits that changed
fingerprinted decision code (git log over the files `systems.decision_code_fingerprint` hashes) and the relaunch
markers in results/logs/*.log. A restarted loop starts again from the root and rewrites the case's partial and final
result. The planner call that proposed a run is recorded only in its loop's history, so when no stored result names
the run, that call and its LLM cost are in no stored result.

Read-only: no run record or result is changed. Live processes keep writing results, so the output is a snapshot.

    python scripts/audit_runs.py        # writes results/analysis/run_audit.{json,md}
"""

import datetime as dt
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
STUDY_LAUNCHERS = {"baseline_study": "scripts/baseline_study.py",
                   "farfield_test": "scripts/farfield_resolution_test.py"}
LLM_LAUNCHER = re.compile(r"llm", re.I)
EXTRA_SYSTEMS = {("benchmark", "exhaustive"): {"Bexh"}}  # Bexh results carry no 'planner' field
# the files systems.decision_code_fingerprint hashes: a change to any of them changes the fingerprint
FINGERPRINTED = ["src/socrates/checks/*.py", "src/socrates/critic/*.py", "src/socrates/evidence/*.py",
                 "src/socrates/case_generation/*.py", "src/socrates/experiments/*.py",
                 "src/socrates/openfoam/parsers.py", "src/socrates/orchestration/loop.py",
                 "src/socrates/orchestration/systems.py", "src/socrates/orchestration/store.py",
                 "configs/verification.yaml", "configs/verification_v2.yaml", "configs/problem_cylinder_re100.yaml"]
RUN_ID = re.compile(r"(?<![A-Za-z0-9_.+-])[A-Za-z0-9_.+]+-[0-9a-f]{12}(?![0-9A-Za-z])")
MARKER = re.compile(r"^===\s*(?P<label>.*?)\s+(?P<time>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\s*(?:===)?$")
LOGGED = re.compile(r"(?P<system>\S+)\s+(?P<case>\S+)\s+->\s+(?P<verdict>ACCEPT|REJECT|INCONCLUSIVE|ERROR)")


def utc(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=60, check=True).stdout


def processes() -> tuple[dict[int, tuple[float, str]], dict[str, list[str]]]:
    """Live processes: pid -> (start time, command line); working directory -> commands running there."""
    boot = next(float(x.split()[1]) for x in Path("/proc/stat").read_text().splitlines() if x.startswith("btime"))
    tick = os.sysconf("SC_CLK_TCK")
    procs, in_dir = {}, defaultdict(list)
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            cmd = (p / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
            start = boot + int((p / "stat").read_text().rsplit(")", 1)[1].split()[19]) / tick
        except (OSError, ValueError, IndexError):
            continue  # exited while being read
        procs[int(p.name)] = (start, cmd)
        try:
            in_dir[os.readlink(p / "cwd")].append(Path(cmd.split()[0]).name if cmd else p.name)
        except OSError:
            pass  # working directory unreadable: the process still counts as an owner candidate
    return procs, in_dir


def owner_state(rec: dict, procs: dict) -> tuple[str, str | None]:
    pid = rec.get("owner_pid")
    if pid is None:
        return "no owner_pid", None
    if pid not in procs:
        return "no such process", None
    start, cmd = procs[pid]
    if "python" not in cmd:
        return "pid reused (not Python)", cmd
    if start > utc(rec["created"]).timestamp() + 1:  # `created` is truncated to seconds
        return "pid reused (process started after the record)", cmd
    return "alive", cmd


def scan_references(ids: set[str]) -> tuple[dict, dict, list, dict]:
    """Run id -> files naming it; unknown run-id-shaped tokens -> files; unreadable JSON; parsed JSON per file."""
    odd = {i for i in ids if not RUN_ID.fullmatch(i)}  # ids the pattern cannot find: matched as plain substrings
    refs, dangling, unreadable, docs = defaultdict(set), defaultdict(set), [], {}
    for src in SOURCES:
        for f in sorted(p for p in (RESULTS / src).rglob("*") if p.is_file()):
            rel = str(f.relative_to(RESULTS))
            text = f.read_bytes().decode("utf-8", "replace")
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
    return refs, dangling, unreadable, docs


def events(since: dt.datetime) -> tuple[list[dict], list[str]]:
    """Decision-code commits and launch markers in results/logs, from `since` on, in time order."""
    out, errors = {}, []
    try:
        log = git("log", "--format=%h%x09%cI%x09%s", "--", *FINGERPRINTED)
    except (OSError, subprocess.SubprocessError) as e:
        log = ""
        errors.append(f"git log over fingerprinted files failed: {e!r}")
    for line in log.splitlines():
        h, t, subject = line.split("\t", 2)
        out[(t, h)] = {"time": utc(t), "kind": "decision-code commit", "label": f"commit {h}: {subject[:90]}",
                       "sources": ["git log"]}
    for f in sorted((RESULTS / "logs").glob("*.log")):
        for line in f.read_text(errors="replace").splitlines():
            m = MARKER.match(line.strip())
            if m:
                e = out.setdefault((m["time"], m["label"]), {"time": utc(m["time"]), "kind": "log marker",
                                                             "label": m["label"], "sources": []})
                e["sources"].append(f"logs/{f.name}")
    return sorted((e for e in out.values() if e["time"] >= since), key=lambda e: e["time"]), errors


def is_restart(e: dict) -> bool:
    return e["kind"] == "decision-code commit" or "restart" in e["label"]


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


def r19_commit() -> tuple[str, dt.datetime] | None:
    """The commit that introduced the postProcessing hashes into the run store (R19)."""
    try:
        first = git("log", "--reverse", "-S", "postprocessing_sha256", "--format=%h%x09%cI", "--",
                    "src/socrates/orchestration/store.py").splitlines()
    except (OSError, subprocess.SubprocessError):
        return None
    if not first:
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
        "owner_pid": rec.get("owner_pid"), "owner_state": state, "owner_command": cmd,
        "stale_owner_pid_cleared": rec.get("stale_owner_pid_cleared"),
        "adopted_orphan": bool(rec.get("adopted_orphan")),
        "openfoam_in_case_dir": in_dir.get(str((RUNS / rid / "case").resolve()), []),
        "cache_hits": len(hits), "cache_hits_by": dict(Counter(h.get("launched_by") for h in hits)),
        "unreadable_request_lines": bad_hits,
        "has_postprocessing_sha256": "postprocessing_sha256" in rec,
        "has_final_fields_sha256": "final_fields_sha256" in rec,
    }


def table(headers: list[str], rows: list[list]) -> list[str]:
    def cell(c) -> str:
        return "-" if c is None or c == "" else str(c).replace("|", "\\|")

    return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] + \
           ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]


def paren(items) -> str:
    return "" if not items else " (" + "; ".join(items) + ")"


def event(e: dict) -> str:
    return f"{e['label']} ({t(e['time'].isoformat())})"


def t(s) -> str:
    return "-" if not s else str(s)[:16].replace("T", " ")


def files(n: int) -> str:
    return f"{n} file" + ("" if n == 1 else "s")


def num(x) -> str:
    return f"{x:.3g}" if isinstance(x, (int, float)) else ("-" if x is None else str(x))


def action(d: dict) -> str:
    if not d["action"]:
        return "-"
    return d["action"] + ("" if not d["params"] else " " + ",".join(f"{k}={v}" for k, v in d["params"].items()))


def main() -> int:
    runs, bad_records = {}, []
    for d in sorted(p for p in RUNS.iterdir() if p.is_dir() and not p.name.startswith(".")):
        try:
            runs[d.name] = json.loads((d / "run.json").read_text())
        except (OSError, json.JSONDecodeError) as e:
            bad_records.append({"run_dir": d.name, "error": repr(e)})
    ids = set(runs)
    procs, in_dir = processes()
    refs, dangling, unreadable, docs = scan_references(ids)
    info = {rid: describe(rid, rec, runs, procs, in_dir) for rid, rec in runs.items()}
    for rid, d in info.items():
        d["referenced_by"] = sorted(refs.get(rid, ()))
        if not d["referenced_by"] and d["launched_by"] in STUDY_LAUNCHERS:
            d["referenced_by"] = [f"baseline study ({STUDY_LAUNCHERS[d['launched_by']]})"]
        d["referenced_only_by_partial"] = bool(refs.get(rid)) and all(f.endswith(".partial.json") for f in refs[rid])

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

    t0 = min(utc(r["created"]) for r in runs.values()) if runs else dt.datetime.now(dt.timezone.utc)
    evs, ev_errors = events(t0)
    restarts = [e for e in evs if is_restart(e)]
    logged = logged_results()
    llm_systems = set().union(*(v for (g, p), v in systems.items() if LLM_LAUNCHER.search(p)))
    for d in info.values():
        c = utc(d["created"])
        d["event_before"] = next((event(e) for e in reversed(evs) if e["time"] <= c), None)
        d["next_restart"] = next((event(e) for e in restarts if e["time"] > c), None)
        if LLM_LAUNCHER.search(d["launched_by"] or ""):
            later = {(r["system"], r["section"], t(r["section_start"].isoformat()), r["file"]) for r in logged
                     if r["system"] in llm_systems and r["case"] == d["root_case"] and r["section_start"]
                     and r["section_start"] > c}
            d["llm_results_logged_after_creation"] = [f"{s} after '{lab}' ({tm}, {f})" for s, lab, tm, f in sorted(
                later, key=lambda x: x[2])]

    unref = [d for d in info.values() if not d["referenced_by"]]
    for d in unref:  # an unnamed root: is another root of the same case name in use?
        if not d["parent_run"]:
            d["same_name_roots_in_use"] = sorted(o["run_id"] for o in info.values() if o["referenced_by"] and
                                                 not o["parent_run"] and o["root_case"] == d["root_case"])
    running = [d for d in info.values() if d["status"] == "running"]
    orphaned = [d for d in running if d["owner_state"] != "alive"]
    failed = [d for d in info.values() if d["status"] == "failed"]
    r19 = r19_commit()
    unhashed = [d for d in info.values() if d["status"] != "running"
                and not (d["has_postprocessing_sha256"] and d["has_final_fields_sha256"])]
    for d in unhashed:
        d["created_before_r19_commit"] = None if r19 is None else utc(d["created"]) < r19[1]
    llm_unref = [d for d in unref if LLM_LAUNCHER.search(d["launched_by"] or "")]
    llm_dead = [d for d in llm_unref if d["owner_state"] != "alive"]
    llm_live = [d for d in llm_unref if d["owner_state"] == "alive"]
    missing_parents = [{"run_id": d["run_id"], "missing_ancestor": d["missing_ancestor"]} for d in info.values()
                       if d["missing_ancestor"]]
    all_cost = sum(d["cell_steps"] for d in info.values() if isinstance(d["cell_steps"], (int, float)))
    unref_cost = Counter()
    for d in unref:
        if isinstance(d["cell_steps"], (int, float)):
            unref_cost[d["launched_by"]] += d["cell_steps"]

    by_status = Counter(d["status"] for d in info.values())
    by_launcher = defaultdict(Counter)
    for d in info.values():
        by_launcher[d["launched_by"]][d["status"]] += 1
    unref_groups = defaultdict(Counter)
    for d in unref:
        unref_groups[d["launched_by"]][d["status"]] += 1
    statuses = sorted(by_status)
    n_files = sum(1 for src in SOURCES for p in (RESULTS / src).rglob("*") if p.is_file())
    llm_supported = [d for d in llm_dead if d["next_restart"]]
    llm_logged = [d for d in llm_dead if d.get("llm_results_logged_after_creation")]
    unexplained = [d["run_id"] for d in llm_dead if not d["next_restart"]]
    note = (f"{len(llm_dead)} runs launched by the LLM planner are named by no stored result and have no live owner "
            f"process. {len(llm_supported)} of them were created before at least one event that restarts LLM loops "
            "(a commit to fingerprinted decision code: benchmark results stamped with an older fingerprint are "
            "recomputed when the benchmark script next runs; or a container restart, after which the benchmark and "
            f"attack scripts were relaunched); for {len(llm_logged)} "
            "of them, an LLM result for the same case in results/logs was written by a process launched after the "
            "run was created. "
            + ("They come from " if not unexplained else f"Those {len(llm_supported)} come from ")
            + "LLM loops that were aborted and restarted from the root; the restarted loop rewrote the case's partial "
            "and final result, which do not name these runs. "
            + ("" if not unexplained else f"No restart event explains {', '.join(unexplained)}. ")
            + "The planner calls that proposed them, and their LLM cost (`cost_usd` in a loop's history), are not "
            f"recorded in any stored result. Their simulation cost recorded in evidence.json is "
            f"{num(sum(d['cell_steps'] for d in llm_dead if isinstance(d['cell_steps'], (int, float))))} cell-steps; "
            "'running' records among them have no evidence file, so the compute they used before their owner died "
            f"is not recorded either. {len(llm_live)} further unnamed LLM-planner runs have a live owner: their loops "
            "are still running, and a loop names a run in its partial file once the run finishes.")

    out = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "sources": [f"results/{s}" for s in SOURCES], "n_source_files": n_files,
        "n_runs": len(runs), "by_status": dict(by_status),
        "by_launcher": {k: dict(v) for k, v in sorted(by_launcher.items(), key=lambda x: str(x[0]))},
        "unreadable_run_records": bad_records, "unreadable_result_files": unreadable,
        "dangling_references": {k: sorted(v) for k, v in sorted(dangling.items())},
        "missing_ancestors": missing_parents, "event_errors": ev_errors,
        "r19_commit": None if r19 is None else {"commit": r19[0], "time": r19[1].isoformat()},
        "events": [{**e, "time": e["time"].isoformat()} for e in evs],
        "cell_steps": {"all_runs": all_cost, "unreferenced_by_launcher": dict(unref_cost)},
        "unreferenced": sorted(d["run_id"] for d in unref),
        "unreferenced_by_launcher": {k: dict(v) for k, v in unref_groups.items()},
        "orphaned": sorted(d["run_id"] for d in orphaned),
        "failed": sorted(d["run_id"] for d in failed),
        "without_r19_hashes": sorted(d["run_id"] for d in unhashed),
        "referenced_only_by_partial": sorted(d["run_id"] for d in info.values() if d["referenced_only_by_partial"]),
        "llm_planner_unreferenced": {"note": note, "no_live_owner": sorted(d["run_id"] for d in llm_dead),
                                     "live_owner": sorted(d["run_id"] for d in llm_live)},
        "runs": info,
    }
    dest = RESULTS / "analysis"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "run_audit.json").write_text(json.dumps(out, indent=1, default=str))

    live = any(d["owner_state"] == "alive" for d in running)
    L = ["# Run store audit", "",
         f"Generated by `scripts/audit_runs.py` at {out['generated']}; see the script docstring for the rules. "
         "Read-only. " + ("Owner processes were still running (see 'Running records'), so this is a snapshot."
                          if live else "No owner process of a 'running' record was alive."), "",
         "## Runs by launcher and status", ""]
    L += table(["launched_by", *statuses, "total"],
               [[k, *(v[s] for s in statuses), sum(v.values())]
                for k, v in sorted(by_launcher.items(), key=lambda x: str(x[0]))] +
               [["**all**", *(by_status[s] for s in statuses), len(runs)]])
    n_study = sum(bool(d["referenced_by"]) and d["referenced_by"][0].startswith("baseline study (")
                  for d in info.values())
    n_ref = sum(bool(d["referenced_by"]) for d in info.values()) - n_study
    L += ["", "## References", "",
          f"- {n_files} files scanned under {', '.join(out['sources'])}.",
          f"- {n_ref} runs are named by a stored result; {len(out['referenced_only_by_partial'])} of them only by "
          f"`*.partial.json` files (listed at the end); {n_study} more are counted as used by the baseline study "
          "through their launcher.",
          f"- {len(unref)} runs are named by no stored result.",
          f"- Unreadable run records: {len(bad_records)}{paren([b['run_dir'] for b in bad_records])}; unreadable "
          f"JSON result files: {len(unreadable)}{paren([u['file'] for u in unreadable])}.",
          f"- Run-id-shaped strings in results that name no run in the store: {len(dangling)}"
          + paren([f"{k} in {', '.join(sorted(v))}" for k, v in sorted(dangling.items())]) + ".",
          f"- Runs whose parent chain leads to a run missing from the store: {len(missing_parents)}"
          + paren([f"{m['run_id']} -> {m['missing_ancestor']}" for m in missing_parents]) + "."]
    if ev_errors:
        L += [f"- Event list incomplete: {'; '.join(ev_errors)}."]
    u_cost = sum(unref_cost.values())
    L += [f"- Cell-steps recorded in evidence.json: {num(all_cost)} for all runs, {num(u_cost)} "
          f"({100 * u_cost / all_cost:.1f} %) for runs no result names"
          + paren([f"{k}: {num(v)}" for k, v in sorted(unref_cost.items())]) + "."
          if all_cost else "- No cell-steps recorded."]

    L += ["", "## Runs no stored result names", ""]
    ustat = sorted({d["status"] for d in unref})
    L += table(["launched_by", *ustat, "total"], [[k, *(v[s] for s in ustat), sum(v.values())]
                                                  for k, v in sorted(unref_groups.items(), key=lambda x: str(x[0]))])
    L += ["", "Owner: state of the process in `owner_pid` (see 'Running records'). Pending: systems of this launcher "
          "with no final result for the run's case yet; a pending system that requests the same configuration gets "
          "the stored run (cache hit) and names it in its result. Next restart: the first decision-code commit or "
          "relaunch marker after the run was created.", ""]
    for lb in sorted(unref_groups, key=str):
        L += [f"### {lb}", ""]
        rows = sorted((d for d in unref if d["launched_by"] == lb), key=lambda d: (d["status"], d["created"]))
        L += table(["run", "status", "created", "parent", "experiment", "failure", "cell-steps", "owner", "cache hits",
                    "pending", "next restart"],
                   [[d["run_id"], d["status"], t(d["created"]), d["parent_run"], action(d),
                     None if not d["failure_kind"] else
                     f"{d['failure_kind']}: {d['failure_step']} rc {signal_name(d['failure_returncode'])}",
                     num(d["cell_steps"]), d["owner_state"], d["cache_hits"],
                     ", ".join(d["systems_without_final_result"]), d["next_restart"]] for d in rows])
        L += [""] + [f"Root {d['run_id']} is unnamed; root runs of the same case name in use: "
                     f"{', '.join(d['same_name_roots_in_use']) or 'none'}.\n"
                     for d in rows if "same_name_roots_in_use" in d]

    L += ["## Running records", "",
          f"{len(running)} records have status 'running'; {len(orphaned)} are orphaned (no owner_pid, no such process, "
          "not a Python process, or a process that started after the record was written). A later request for the "
          "same configuration adopts an orphan whose solver finished, or deletes and re-runs it "
          "(`RunStore.get_or_run`); until then the record stays as it is. 'OpenFOAM in case' lists processes whose "
          "working directory is the run's case; a record with a live owner and none is waiting for a CPU slot or "
          "between steps.", ""]
    L += table(["run", "launched_by", "created", "owner_pid", "owner", "pid cleared", "OpenFOAM in case", "named by"],
               [[d["run_id"], d["launched_by"], t(d["created"]), d["owner_pid"], d["owner_state"],
                 None if not (c := d["stale_owner_pid_cleared"]) else
                 f"old pid {c.get('old_owner_pid')}: {c.get('reason')}",
                 ", ".join(d["openfoam_in_case_dir"]), len(d["referenced_by"])]
                for d in sorted(running, key=lambda d: (d["owner_state"] == "alive", d["created"]))])
    owners = sorted({(d["owner_pid"], d["owner_command"]) for d in running if d["owner_state"] == "alive"}, key=str)
    if owners:
        L += ["", "Live owners: " + "; ".join(f"pid {p}: `{c}`" for p, c in owners) + "."]

    L += ["", "## Failed runs", ""]
    L += table(["run", "launched_by", "created", "kind", "step", "returncode", "parent", "experiment", "named by"],
               [[d["run_id"], d["launched_by"], t(d["created"]), d["failure_kind"], d["failure_step"],
                 signal_name(d["failure_returncode"]), d["parent_run"], action(d),
                 files(len(d["referenced_by"]))
                 + paren(sorted({"/".join(f.split("/")[:2]) for f in d["referenced_by"]}))]
                for d in sorted(failed, key=lambda d: d["created"])])

    L += ["", "## Finalized runs without postProcessing and final-field hashes", "",
          "R19 (docs/methodology.md) added SHA-256 hashes of the postProcessing outputs and of the retained final "
          "fields to the run record when a run is finalized"
          + ("" if r19 is None else f" (commit {r19[0]}, {t(r19[1].isoformat())} UTC)") + ". A record without them "
          "that was created before that commit was written by older code (a long-running process keeps the code it "
          "loaded at start); code from that commit on omits them only when the run wrote no postProcessing output "
          "or no time directory.", ""]
    L += table(["run", "status", "launched_by", "root", "created", "finished", "created before R19 commit", "named by"],
               [[d["run_id"], d["status"], d["launched_by"], "yes" if not d["parent_run"] else "no", t(d["created"]),
                 t(d["finished"]), {True: "yes", False: "no"}.get(d["created_before_r19_commit"]),
                 files(len(d["referenced_by"]))]
                for d in sorted(unhashed, key=lambda d: d["created"])])

    L += ["", "## Unnamed runs launched by the LLM planner", "", note, ""]
    L += table(["run", "status", "created", "owner", "next restart", "LLM results for the case logged after creation"],
               [[d["run_id"], d["status"], t(d["created"]), d["owner_state"], d["next_restart"],
                 "; ".join(d.get("llm_results_logged_after_creation") or [])]
                for d in sorted(llm_unref, key=lambda d: (d["owner_state"] == "alive", d["created"]))])

    L += ["", "## Events", "", "Commits that changed fingerprinted decision code, and launch markers in results/logs.",
          ""]
    L += table(["time (UTC)", "event", "source"], [[t(e["time"].isoformat()), e["label"], ", ".join(e["sources"])]
                                                    for e in evs])

    L += ["", "## Runs named only by partial files", ""]
    L += table(["run", "status", "launched_by", "files"],
               [[d["run_id"], d["status"], d["launched_by"], ", ".join(d["referenced_by"])]
                for d in sorted(info.values(), key=lambda d: d["run_id"]) if d["referenced_only_by_partial"]])
    (dest / "run_audit.md").write_text("\n".join(L) + "\n")

    groups = ", ".join(f"{k}: {sum(v.values())}" for k, v in sorted(unref_groups.items(), key=lambda x: str(x[0])))
    print(f"{len(runs)} runs ({', '.join(f'{by_status[s]} {s}' for s in statuses)}); {len(unref)} named by no result "
          f"({groups}); {len(orphaned)} orphaned running records; {len(failed)} failed "
          f"({sum(1 for d in failed if not d['referenced_by'])} named by no result); "
          f"{len(unhashed)} without R19 hashes; {len(llm_dead)} unnamed LLM-planner runs without a live owner "
          f"({len(llm_supported)} created before a restart event), {len(llm_live)} in progress; "
          f"{len(dangling)} dangling references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
