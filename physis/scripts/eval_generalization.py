"""Honest generalization evaluation of the learned closure on the 800-sample dataset.

Motivation (2026-10-30): the run report's headline ("MLP beats Kozeny–Carman out of
distribution") was overclaimed — it was a single seed, and the descriptor MLP
one-hot-encodes the family, so it has no geometric information for a family it never saw.
This script answers, with multiple seeds and identical splits across models:

1. random split                 — in-distribution sanity check
2. porosity band held out       — extrapolation within known families
3. unseen family (×3)           — train on 2 families, test on the 3rd

Models, all evaluated on the SAME train/test rows:
- Kozeny–Carman (physics baseline, constant fitted on train) — deterministic
- MLP ensemble (porosity, log specific surface, family one-hot) — the current descriptor
  model. NB: on unseen-family splits the one-hot is all-zero -> the model sees a family it
  was never trained on; that is exactly the failure mode we are measuring.
- 3D CNN on the raw 32^3 voxel field (no family label) — the candidate that should
  generalize, because it sees geometry rather than a family tag.

Discipline: every trainable model is run with multiple seeds and the spread is reported
(min/max), never a single number. Splits are constructed once with a fixed RNG so every
model sees identical test rows.

Usage:
    python scripts/eval_generalization.py                      # full run (GPU or CPU)
    python scripts/eval_generalization.py --quick --device cpu # smoke test, 1 seed, few epochs
Output:
    runs/eval-generalization-<date>/results.json + summary.md
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physis.surrogates import closure  # noqa: E402


def load_dataset(out: Path) -> tuple[list[dict], np.ndarray]:
    rows = [json.loads(l) for l in (out / "dataset.jsonl").read_text().splitlines() if l.strip()]
    ok = [r for r in rows if r.get("status") == "ok" and r["specific_surface"] > 0]
    vols = np.stack([np.load(out / "volumes" / f"{r['index']:05d}.npy").astype(np.float32) for r in ok])
    return ok, vols


def make_splits(rows: list[dict]) -> dict[str, tuple[list[int], list[int]]]:
    """Fixed split construction (reproducible) -> {name: (train_idx, test_idx)}."""
    rng = np.random.default_rng(0)
    idx = np.arange(len(rows))
    splits = {}
    # 1) random split
    order = rng.permutation(len(rows))
    n_test = len(rows) // 5
    splits["random"] = (order[n_test:], order[:n_test])
    # 2) porosity band held out (>0.72), like the report
    lo = [i for i in idx if rows[i]["porosity"] <= 0.68]
    hi = [i for i in idx if rows[i]["porosity"] > 0.72]
    splits["porosity_band_held_out"] = (lo, hi)
    # 3) unseen family: train on 2, test on the 3rd
    for fam in ("spheres", "voids", "gyroid"):
        tr = [i for i in idx if rows[i]["family"] != fam]
        te = [i for i in idx if rows[i]["family"] == fam]
        splits[f"unseen_{fam}"] = (tr, te)
    return splits


def kc_score(rows, tr, te):
    kc = closure.KozenyCarman().fit([rows[i] for i in tr])
    return closure.metrics(closure.target([rows[i] for i in te]), kc.predict([rows[i] for i in te]))


def mlp_score(rows, tr, te, seed, epochs):
    m = closure.MLPEnsemble(epochs=epochs, seed=seed, device="cpu").fit(
        closure.features([rows[i] for i in tr]), closure.target([rows[i] for i in tr]))
    mean, _ = m.predict(closure.features([rows[i] for i in te]))
    return closure.metrics(closure.target([rows[i] for i in te]), mean)


def cnn_score(vols, rows, tr, te, seed, epochs, device):
    y = closure.target(rows)
    model, ymu, ysd = closure.train_cnn(vols[tr], y[tr], epochs=epochs, device=device, seed=seed)
    pred = closure.predict_cnn(model, vols[te], ymu, ysd, device=device)
    return closure.metrics(y[te], pred)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None, help="dataset run folder (default runs/weekend-20261030-sharded800)")
    ap.add_argument("--quick", action="store_true", help="smoke test: 1 seed, few epochs")
    ap.add_argument("--seeds", type=int, default=3, help="training seeds per model/split (default 3)")
    ap.add_argument("--epochs", type=int, default=150, help="CNN epochs (default 150)")
    ap.add_argument("--mlp-epochs", type=int, default=3000, help="MLP epochs (default 3000)")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--splits", default="all", help="comma list of splits or 'all'")
    args = ap.parse_args()

    data_root = Path(args.out) if args.out else ROOT / "runs" / "weekend-20261030-sharded800"
    rows, vols = load_dataset(data_root)
    n_seeds = 1 if args.quick else args.seeds
    cnn_epochs = 5 if args.quick else args.epochs
    mlp_epochs = 300 if args.quick else args.mlp_epochs
    device = "cpu" if args.device == "auto" or args.quick else args.device

    splits = make_splits(rows)
    if args.splits != "all":
        splits = {k: v for k, v in splits.items() if k in args.splits.split(",")}

    stamp = time.strftime("%Y%m%d-%H%M%S")
    outdir = ROOT / "runs" / f"eval-generalization-{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)

    results: dict = {"splits": {}, "meta": {
        "dataset": str(data_root), "n_ok": len(rows), "seeds": n_seeds,
        "cnn_epochs": cnn_epochs, "mlp_epochs": mlp_epochs, "device": device,
        "families": dict(Counter(r["family"] for r in rows))}}

    for name, (tr, te) in splits.items():
        print(f"\n=== {name}: train {len(tr)}, test {len(te)} ===", flush=True)
        entry = {}
        # KC (deterministic)
        entry["kozeny_carman"] = kc_score(rows, tr, te)
        print(f"  KC      R2 {entry['kozeny_carman']['r2']:.3f}", flush=True)
        # MLP (multiple seeds)
        mlp_rs = []
        for s in range(n_seeds):
            mlp_rs.append(mlp_score(rows, tr, te, seed=s, epochs=mlp_epochs))
            print(f"  MLP s{s}  R2 {mlp_rs[-1]['r2']:.3f}", flush=True)
        entry["mlp_ensemble"] = {k: [r[k] for r in mlp_rs] for k in ("r2", "mae_log10", "max_abs_log10")}
        # CNN (multiple seeds) — only when enough train samples and volumes exist
        if len(tr) >= 20 and len(te) >= 4:
            cnn_rs = []
            for s in range(n_seeds):
                cnn_rs.append(cnn_score(vols, rows, tr, te, seed=s, epochs=cnn_epochs, device=device))
                print(f"  CNN s{s}  R2 {cnn_rs[-1]['r2']:.3f}", flush=True)
            entry["cnn"] = {k: [r[k] for r in cnn_rs] for k in ("r2", "mae_log10", "max_abs_log10")}
        else:
            entry["cnn"] = {"skipped": f"train {len(tr)}, test {len(te)}"}
        results["splits"][name] = entry

    (outdir / "results.json").write_text(json.dumps(results, indent=1) + "\n")

    # summary.md
    L = [f"# Generalization evaluation — {stamp}", "",
         f"Dataset: `{data_root}` — {results['meta']['n_ok']} ok samples "
         f"(families {results['meta']['families']}), {n_seeds} seed(s) per trainable model, "
         f"CNN {cnn_epochs} epochs, MLP {mlp_epochs} epochs, device {device}.", "",
         "Target = log10(K). R² reported as min–max over seeds (higher is better); "
         "KC is deterministic.", "",
         "| split | KC R² | MLP R² (seeds) | CNN R² (seeds) |", "|---|---|---|---|"]
    for name, e in results["splits"].items():
        def cell(x, k):
            if isinstance(x, dict) and "skipped" in x:
                return "skipped"
            v = x[k]
            return f"{min(v):.3f}–{max(v):.3f}" if isinstance(v, list) else f"{v:.3f}"
        L.append(f"| {name} | {e['kozeny_carman']['r2']:.3f} | {cell(e['mlp_ensemble'], 'r2')} | "
                 f"{cell(e['cnn'], 'r2')} |")
    L += ["", "## Reading", "",
          "- If the CNN beats KC on `unseen_*` splits, geometry (voxels) carries the "
          "generalization signal that the family one-hot MLP lacks.",
          "- If the CNN also collapses on unseen families, the porosity band itself is not "
          "the only missing axis: the dataset lacks the *geometric diversity* needed.",
          "- Report spread, not a single seed. A model that needs a lucky seed is not a "
          "model that generalizes."]
    (outdir / "summary.md").write_text("\n".join(L) + "\n")
    print(f"\nresults: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
