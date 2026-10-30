"""Weekend run on an NVIDIA GPU (RTX 5090): pore-scale data and the first learned closure.

Stages (in order; each writes ``<out>/stage_<name>.json`` and is skipped when that file
exists, so a crash never costs finished work; ``--force`` reruns):

    preflight    machine, GPU, memory, versions, disk
    selfcheck    Triton kernel against the float64 torch reference on the GPU; picks the path
    gates        validation gates (float64) for the LBM solver
    resolution   one structure at 64^3 ... 512^3: how fine must pores be resolved?
    dataset      N random structures (spheres, voids, gyroids): descriptors + permeability
    train        Kozeny–Carman baseline vs MLP ensemble (random split + held-out porosity band)
    forchheimer  inertia onset: velocity sweep on three structures      (optional)
    cnn          3D CNN on the voxel structure                         (optional)
    report       report.md + plots: send the whole output folder back

    python scripts/weekend_5090.py                       # everything
    python scripts/weekend_5090.py --quick               # ~2-5 min smoke test of every stage
    python scripts/weekend_5090.py --stages dataset,train --samples 1200
    python scripts/weekend_5090.py --stages dataset --samples 600 --sample-offset 600  # shard 2 of a parallel run
    python scripts/merge_shards.py runs/merged runs/shard-*                       # then: --out runs/merged --stages train,cnn,report
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physis.core.backend import get_backend  # noqa: E402
from physis.data import rve  # noqa: E402
from physis.data.porous_features import solid_fraction_field  # noqa: E402
from physis.core.grid import Grid  # noqa: E402
from physis.solvers.lbm import PeriodicFlow, PeriodicFlowSpec, lattice, triton_kernel  # noqa: E402
from physis.solvers.lbm.periodic import bytes_needed, choose_impl  # noqa: E402
from physis.surrogates import closure  # noqa: E402

STAGES = ["preflight", "selfcheck", "gates", "resolution", "dataset", "train", "forchheimer", "cnn", "report"]


# --------------------------------------------------------------------------- helpers

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def save(out: Path, name: str, data: dict) -> None:
    (out / f"stage_{name}.json").write_text(json.dumps(data, indent=1, default=str) + "\n")


def load(out: Path, name: str) -> dict | None:
    p = out / f"stage_{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def free_device_bytes(device: torch.device) -> int:
    if device.type == "cuda":
        # memory held in torch's cache by an earlier (smaller) run counts as used for the driver
        gc.collect()
        torch.cuda.empty_cache()
        return torch.cuda.mem_get_info(device)[0]
    if device.type == "mps":
        return int(torch.mps.recommended_max_memory() * 0.8)
    return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") * 0.5)


def sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize()
    elif device.type == "mps":
        torch.mps.synchronize()


# --------------------------------------------------------------------------- stages

def stage_preflight(ctx) -> dict:
    dev = ctx.backend.device
    info = {"python": platform.python_version(), "platform": platform.platform(), "torch": torch.__version__,
            "device": str(dev), "cpu_count": os.cpu_count(),
            "disk_free_gb": round(shutil.disk_usage(ctx.out).free / 2**30, 1),
            "triton": None, "triton_error": triton_kernel.TRITON_ERROR}
    if triton_kernel.HAVE_TRITON:
        import triton
        info["triton"] = triton.__version__
    if dev.type == "cuda":
        p = torch.cuda.get_device_properties(dev)
        free, total = torch.cuda.mem_get_info(dev)
        info.update({"gpu": p.name, "gpu_memory_gb": round(total / 2**30, 1), "gpu_free_gb": round(free / 2**30, 1),
                     "cuda": torch.version.cuda, "compute_capability": f"{p.major}.{p.minor}"})
    elif dev.type == "mps":
        info["gpu"] = "Apple GPU (MPS)"
    if info["disk_free_gb"] < 2:
        raise SystemExit("less than 2 GB free disk: free space first")
    return info


def stage_selfcheck(ctx) -> dict:
    dev = ctx.backend.device
    out = {"device": str(dev)}
    if dev.type == "cuda":
        ok, detail = triton_kernel.selfcheck(str(dev))
        out.update({"triton_selfcheck": "PASS" if ok else "FAIL", "detail": detail})
        log(f"Triton self-check: {'PASS' if ok else 'FAIL'} ({detail})")
    impl = choose_impl("auto", ctx.backend)
    out["impl"] = impl
    if dev.type == "cuda" and impl != "triton":
        out["warning"] = ("Triton kernel NOT used: the run continues on the slower torch path "
                          "(several times slower, and resolution capped at 192^3)")
        log("WARNING: " + out["warning"])
    # throughput on a realistic structure
    n = 32 if ctx.quick else 160
    geom = rve.random_structure(1, "spheres")
    grid = Grid((n, n, n), 1.0 / n, (0.0, 0.0, 0.0))
    spec = PeriodicFlowSpec(grid=grid.to_dict(), geometry=geom, force=(1e-6, 0, 0), tau_plus=1.5,
                            check_every=200, max_steps=400, tol=1e-30, impl="auto", keep_fields=False)
    PeriodicFlow().run(spec, ctx.backend)  # warm-up: the first call compiles the GPU kernel
    r = PeriodicFlow().run(spec, ctx.backend)
    out["mlups"] = r.diagnostics["mlups"]
    log(f"path {impl}: {out['mlups']:.0f} MLUPS at {n}^3")
    return out


def stage_gates(ctx) -> dict:
    if ctx.quick:
        cmd = [sys.executable, "-m", "pytest", "-q", "tests/test_lbm.py", "tests/test_porous_geometry.py"]
    else:
        cmd = [sys.executable, "-m", "pytest", "-q", "-m", "validation", "tests/test_validation_lbm.py",
               "-p", "no:cacheprovider"]
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    res = {"command": " ".join(cmd[2:]), "returncode": proc.returncode, "wall_s": round(time.time() - t0, 1),
           "tail": proc.stdout[-2000:] + proc.stderr[-1000:]}
    if not ctx.quick:
        res["records"] = {p.stem: json.loads(p.read_text())["status"]
                          for p in (ROOT / "validation" / "results").glob("lbm.*.json")}
    log(f"gates: return code {proc.returncode} ({res['wall_s']} s)")
    return res


def stage_resolution(ctx) -> dict:
    sc = load(ctx.out, "selfcheck")  # absent when this folder's run skipped the selfcheck stage
    impl = sc["impl"] if sc else choose_impl("auto", ctx.backend)
    sizes = [24, 32, 48] if ctx.quick else [64, 96, 128, 192, 256, 384, 512]
    if impl == "torch":
        sizes = [s for s in sizes if s <= 192]
    geom = rve.random_structure(0, "spheres", seed_offset=777)
    rows = []
    for n in sizes:
        need = bytes_needed((n, n, n), impl)
        free = free_device_bytes(ctx.backend.device)
        if need > 0.85 * free:
            log(f"resolution {n}^3: skipped (needs ~{need / 2**30:.1f} GB, {free / 2**30:.1f} GB free)")
            rows.append({"n": n, "status": "skipped_memory", "need_gb": need / 2**30})
            continue
        t0 = time.time()
        r = rve.run_rve(geom, n, ctx.backend)
        r["wall_total_s"] = time.time() - t0
        rows.append(r)
        log(f"resolution {n}^3: K = {r.get('permeability', float('nan')):.4e}, status {r['status']}, "
            f"{r['steps']} steps, {r['wall_total_s']:.1f} s")
        save(ctx.out, "resolution_partial", {"rows": rows})
    ok = [r for r in rows if r.get("status") == "ok"]
    finest = ok[-1]["permeability"] if ok else float("nan")
    for r in ok:
        r["rel_to_finest"] = r["permeability"] / finest - 1
    return {"geometry": geom, "rows": rows}


def _dataset_path(ctx) -> Path:
    return ctx.out / "dataset.jsonl"


def stage_dataset(ctx) -> dict:
    n = 32 if ctx.quick else ctx.size
    total = 30 if ctx.quick else ctx.samples
    path = _dataset_path(ctx)
    vol_dir = ctx.out / "volumes"
    vol_dir.mkdir(exist_ok=True)
    done = set()
    if path.exists():
        done = {json.loads(line)["index"] for line in path.read_text().splitlines() if line.strip()}
    log(f"dataset: {len(done)} of {total} samples already done, {n}^3 each")
    t_start, new = time.time(), 0
    with path.open("a") as fh:
        for k in range(total):
            i = ctx.offset + k  # global sample index: parallel shards get distinct seeds
            if i in done:
                continue
            geom = rve.random_structure(i)
            try:
                row = rve.run_rve(geom, n, ctx.backend)
            except Exception as exc:  # noqa: BLE001 - one failed sample must not stop the night
                row = {"family": rve.family_of(geom), "geometry": geom, "status": f"error: {type(exc).__name__}: {exc}"}
            row["index"] = i
            fh.write(json.dumps(row, default=float) + "\n")
            fh.flush()
            if row.get("status") == "ok":
                grid = Grid((n, n, n), 1.0 / n, (0.0, 0.0, 0.0))
                factor = max(1, n // 32)
                vol = solid_fraction_field(geom, grid, ctx.backend, factor).float().cpu().numpy().astype(np.float16)
                np.save(vol_dir / f"{i:05d}.npy", vol)
            new += 1
            if new in (3, 20) or new % 50 == 0:
                per = (time.time() - t_start) / new
                left = (total - len([d for d in done if ctx.offset <= d < ctx.offset + total]) - new) * per
                log(f"dataset: {len(done) + new}/{total}, {per:.1f} s/sample, ~{left / 3600:.1f} h left")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"n": n, "samples": len(rows), "status_counts": counts, "file": path.name}


def _ok_rows(ctx) -> list[dict]:
    rows = [json.loads(line) for line in _dataset_path(ctx).read_text().splitlines() if line.strip()]
    return [r for r in rows if r.get("status") == "ok" and r["specific_surface"] > 0]


def stage_train(ctx) -> dict:
    rows = _ok_rows(ctx)
    if len(rows) < 10:
        return {"skipped": f"only {len(rows)} usable samples"}
    rng = np.random.default_rng(0)
    order = rng.permutation(len(rows))
    n_test = max(2, len(rows) // 5)
    splits = {
        "random": ([rows[i] for i in order[n_test:]], [rows[i] for i in order[:n_test]]),
        "porosity_band_held_out": ([r for r in rows if r["porosity"] <= 0.68], [r for r in rows if r["porosity"] > 0.72]),
    }
    device = str(ctx.backend.device) if ctx.backend.device.type == "cuda" else "cpu"
    epochs = 300 if ctx.quick else 3000
    result = {}
    for name, (train, test) in splits.items():
        if len(train) < 5 or len(test) < 2:
            result[name] = {"skipped": f"train {len(train)}, test {len(test)}"}
            continue
        kc = closure.KozenyCarman().fit(train)
        y_te = closure.target(test)
        mlp = closure.MLPEnsemble(epochs=epochs, device=device).fit(closure.features(train), closure.target(train))
        mean, std = mlp.predict(closure.features(test))
        err = np.abs(mean - y_te)
        result[name] = {
            "train": len(train), "test": len(test),
            "kozeny_carman": {**closure.metrics(y_te, kc.predict(test)), "fitted_constant": 10 ** kc.log10_c},
            "mlp_ensemble": closure.metrics(y_te, mean),
            "uncertainty_vs_error_spearman": _spearman(std, err),
        }
        _parity_plot(ctx.out / f"parity_{name}.png", y_te, kc.predict(test), mean, std, name)
        log(f"train [{name}]: KC R2 {result[name]['kozeny_carman']['r2']:.3f} | "
            f"MLP R2 {result[name]['mlp_ensemble']['r2']:.3f}")
    return result


def _spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1]) if len(a) > 2 else float("nan")


def _parity_plot(path: Path, y, kc, mean, std, title) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    lo, hi = float(min(y.min(), kc.min(), mean.min())), float(max(y.max(), kc.max(), mean.max()))
    ax.plot([lo, hi], [lo, hi], "k--", lw=1)
    ax.scatter(y, kc, s=10, alpha=0.6, color="tab:orange", label="Kozeny–Carman")
    ax.errorbar(y, mean, yerr=std, fmt="o", ms=3, alpha=0.7, color="tab:blue", label="MLP ensemble (±1σ)")
    ax.set_xlabel("log10 K (LBM)")
    ax.set_ylabel("log10 K (predicted)")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def stage_forchheimer(ctx) -> dict:
    n = 32 if ctx.quick else min(ctx.size, 128)
    tau = 0.6
    nu = lattice.viscosity(tau)
    out = []
    for fam in rve.FAMILIES:
        geom = rve.random_structure(3, fam, seed_offset=4242)
        base = rve.run_rve(geom, n, ctx.backend, tau_plus=tau, target_velocity=2e-4)
        if base["status"] != "ok":
            out.append({"family": fam, "status": base["status"]})
            continue
        g0 = base["force_lu"]
        pts = []
        for factor in ([1, 10, 40] if ctx.quick else [1, 5, 20, 50, 100, 200, 350]):
            r = rve.run_rve(geom, n, ctx.backend, tau_plus=tau, force=g0 * factor)
            if r["status"] != "ok" or r["mach_max"] > 0.15:
                break
            u = r["permeability_lu"] * r["force_lu"] / nu  # superficial velocity
            pts.append({"force": r["force_lu"], "u": u, "re_pore": r["reynolds_pore"], "mach": r["mach_max"]})
        if len(pts) >= 3:
            u = np.array([p["u"] for p in pts])
            g = np.array([p["force"] for p in pts])
            a, b = np.linalg.lstsq(np.stack([u, u * u], 1), g, rcond=None)[0]  # g = (nu/K) u + beta u^2
            k_lu = nu / a
            out.append({"family": fam, "porosity": base["porosity"], "points": pts, "k_darcy_lu": base["permeability_lu"],
                        "k_fit_lu": k_lu, "beta_lu": b, "forchheimer_F": b * math.sqrt(k_lu)})
        else:
            out.append({"family": fam, "points": pts, "status": "too few points"})
        log(f"forchheimer [{fam}]: {len(pts)} points, Re up to {max([p['re_pore'] for p in pts], default=0):.2f}")
    return {"n": n, "tau_plus": tau, "results": out}


def stage_cnn(ctx) -> dict:
    rows = [r for r in _ok_rows(ctx) if (ctx.out / "volumes" / f"{r['index']:05d}.npy").exists()]
    if len(rows) < 20:
        return {"skipped": f"only {len(rows)} usable samples with volumes"}
    vols = np.stack([np.load(ctx.out / "volumes" / f"{r['index']:05d}.npy").astype(np.float32) for r in rows])
    y = closure.target(rows)
    rng = np.random.default_rng(0)
    order = rng.permutation(len(rows))
    n_test = max(4, len(rows) // 5)
    te, tr = order[:n_test], order[n_test:]
    device = str(ctx.backend.device) if ctx.backend.device.type in ("cuda", "mps") else "cpu"
    model, ymu, ysd = closure.train_cnn(vols[tr], y[tr], epochs=20 if ctx.quick else 150, device=device)
    pred = closure.predict_cnn(model, vols[te], ymu, ysd, device=device)
    res = {"train": len(tr), "test": len(te), "volume_shape": list(vols.shape[1:]),
           "cnn": closure.metrics(y[te], pred)}
    log(f"cnn: R2 {res['cnn']['r2']:.3f}, MAE {res['cnn']['mae_log10']:.3f} (log10 K)")
    return res


def stage_report(ctx) -> dict:
    s = {name: load(ctx.out, name) for name in STAGES if name != "report"}
    L = [f"# physis weekend run — {time.strftime('%Y-%m-%d %H:%M')}", ""]
    if ctx.quick:
        L += ["> **Quick smoke test:** tiny grids and a handful of samples. It shows that every stage runs;",
              "> the numbers below mean nothing physically.", ""]
    pf, sc = s["preflight"] or {}, s["selfcheck"] or {}
    L += ["## Machine and solver path", "",
          f"- GPU: {pf.get('gpu', '?')} ({pf.get('gpu_memory_gb', '?')} GB), torch {pf.get('torch')}, "
          f"CUDA {pf.get('cuda')}, Triton {pf.get('triton')}",
          f"- **Triton self-check: {sc.get('triton_selfcheck', 'n/a')}** {sc.get('detail', '')}",
          f"- Path used: **{sc.get('impl')}**, {sc.get('mlups', 0):.0f} MLUPS"]
    if sc.get("warning"):
        L.append(f"- ⚠ {sc['warning']}")
    g = s["gates"] or {}
    L += ["", "## Validation gates", "", f"- `{g.get('command')}` → return code {g.get('returncode')}" if g else
          "- not run in this folder (stage skipped); see `validation/results/` for the last recorded gates"]
    for k, v in (g.get("records") or {}).items():
        L.append(f"  - {k}: **{v}**")
    res = s["resolution"] or {}
    if res.get("rows"):
        L += ["", "## Resolution study (one structure, box length 1)", "", "| n | K | rel. to finest | steps | s |",
              "|---|---|---|---|---|"]
        for r in res["rows"]:
            if r.get("status") == "ok":
                L.append(f"| {r['n']}³ | {r['permeability']:.4e} | {r.get('rel_to_finest', 0):+.2%} | {r['steps']} | "
                         f"{r.get('wall_total_s', 0):.0f} |")
            else:
                L.append(f"| {r['n']}³ | {r.get('status')} | | | |")
    ds = s["dataset"] or {}
    L += ["", "## Dataset", "", f"- {ds.get('samples')} samples at {ds.get('n')}³, status: {ds.get('status_counts')}"]
    tr = s["train"] or {}
    if tr and "skipped" not in tr:
        L += ["", "## Learned closure vs Kozeny–Carman (log10 K)", "",
              "| split | model | R² | MAE | max error | n test |", "|---|---|---|---|---|---|"]
        for name, v in tr.items():
            if not isinstance(v, dict) or "skipped" in v:
                continue
            for model in ("kozeny_carman", "mlp_ensemble"):
                m = v[model]
                L.append(f"| {name} | {model} | {m['r2']:.3f} | {m['mae_log10']:.3f} | {m['max_abs_log10']:.3f} | {m['n']} |")
            L.append(f"| {name} | uncertainty↔error (Spearman) | {v['uncertainty_vs_error_spearman']:.2f} | | | |")
        L += ["", "Plots: `parity_random.png`, `parity_porosity_band_held_out.png`"]
    fo = s["forchheimer"] or {}
    if fo.get("results"):
        L += ["", "## Forchheimer (inertia onset)", ""]
        for r in fo["results"]:
            if "forchheimer_F" in r:
                L.append(f"- {r['family']}: K Darcy {r['k_darcy_lu']:.3f} lu², K fit {r['k_fit_lu']:.3f} lu², "
                         f"F = β√K = {r['forchheimer_F']:.3g}, Re up to {max(p['re_pore'] for p in r['points']):.1f}")
            else:
                L.append(f"- {r['family']}: {r.get('status')}")
    cn = s["cnn"] or {}
    if cn.get("cnn"):
        L += ["", "## 3D CNN on the voxel structure", "",
              f"- R² {cn['cnn']['r2']:.3f}, MAE {cn['cnn']['mae_log10']:.3f} (log10 K), test n = {cn['test']}"]
    failed = sorted(p.stem[len("stage_"):-len("_failed")] for p in ctx.out.glob("stage_*_failed.json"))
    failed = [f for f in failed if f != "report"]
    if failed:
        L += ["", "## Failed stages", ""] + [f"- {f}: {load(ctx.out, f + '_failed')['failed']}" for f in failed]
    (ctx.out / "report.md").write_text("\n".join(L) + "\n")
    log(f"report written: {ctx.out / 'report.md'} — send the whole folder {ctx.out} back")
    return {"report": "report.md"}


# --------------------------------------------------------------------------- main

class Ctx:
    pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None, help="output folder (default runs/weekend-<date>)")
    ap.add_argument("--quick", action="store_true", help="tiny sizes: smoke-test every stage in minutes")
    ap.add_argument("--stages", default=",".join(STAGES))
    ap.add_argument("--force", action="store_true", help="rerun stages that already have results")
    ap.add_argument("--samples", type=int, default=600)
    ap.add_argument("--sample-offset", type=int, default=0,
                    help="shift sample indices by this amount (parallel shards: distinct seeds per node)")
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()

    ctx = Ctx()
    ctx.quick, ctx.samples, ctx.size = args.quick, args.samples, args.size
    ctx.offset = args.sample_offset
    ctx.out = Path(args.out or ROOT / "runs" / f"weekend-{time.strftime('%Y%m%d')}{'-quick' if args.quick else ''}")
    ctx.out.mkdir(parents=True, exist_ok=True)
    ctx.backend = get_backend("fast", device=args.device)
    torch.manual_seed(0)
    wanted = [s.strip() for s in args.stages.split(",") if s.strip()]
    for name in STAGES:
        if name not in wanted:
            continue
        if name != "report" and not args.force and load(ctx.out, name) is not None:
            log(f"{name}: already done, skipping (use --force to rerun)")
            continue
        log(f"--- {name}")
        t0 = time.time()
        try:
            data = globals()[f"stage_{name}"](ctx)
        except Exception as exc:  # noqa: BLE001 - record and move on to the next stage
            log(f"{name} FAILED: {type(exc).__name__}: {exc}")
            save(ctx.out, f"{name}_failed", {"failed": f"{type(exc).__name__}: {exc}"})  # not marked done
            if name in ("preflight", "selfcheck"):
                return 1
            continue
        data["stage_wall_s"] = round(time.time() - t0, 1)
        save(ctx.out, name, data)
        (ctx.out / f"stage_{name}_failed.json").unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
