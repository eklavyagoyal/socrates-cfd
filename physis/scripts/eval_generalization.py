"""Honest generalization evaluation of the learned closure on the 800-sample dataset.

Compare KC, descriptor MLP ensembles and a voxel CNN on fixed identical splits.
The low/high porosity splits test descriptor extrapolation; unseen-family splits
also include an MLP without family flags. Each repetition uses base seed s * 1000
so the five-member MLP ensembles do not share member seeds.

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
    splits["low_porosity"] = (
        [i for i in idx if rows[i]["porosity"] >= 0.50],
        [i for i in idx if rows[i]["porosity"] < 0.45],
    )
    # 3) unseen family: train on 2, test on the 3rd
    for fam in ("spheres", "voids", "gyroid"):
        tr = [i for i in idx if rows[i]["family"] != fam]
        te = [i for i in idx if rows[i]["family"] == fam]
        splits[f"unseen_{fam}"] = (tr, te)
    return splits


def kc_score(rows, tr, te):
    kc = closure.KozenyCarman().fit([rows[i] for i in tr])
    return closure.metrics(closure.target([rows[i] for i in te]), kc.predict([rows[i] for i in te]))


def mlp_score(rows, tr, te, seed, epochs, *, noflag=False):
    x = closure.features(rows)
    if noflag:
        x = x[:, :2]
    m = closure.MLPEnsemble(epochs=epochs, seed=seed, device="cpu").fit(
        x[tr], closure.target([rows[i] for i in tr]))
    mean, _ = m.predict(x[te])
    return closure.metrics(closure.target([rows[i] for i in te]), mean)


def cnn_score(vols, rows, tr, te, seed, epochs, device):
    y = closure.target(rows)
    model, ymu, ysd = closure.train_cnn(vols[tr], y[tr], epochs=epochs, device=device, seed=seed)
    pred = closure.predict_cnn(model, vols[te], ymu, ysd, device=device)
    return closure.metrics(y[te], pred)


def write_summary(outdir: Path, results: dict, stamp: str) -> None:
    meta = results["meta"]
    lines = [f"# Generalization evaluation — {stamp}", "",
             f"Dataset: `{meta['dataset']}`; {meta['n_ok']} ok samples; "
             f"{meta['seeds']} seeds per trainable model ({meta['base_seeds']}). "
             f"CNN {meta['cnn_epochs']} epochs; MLP {meta['mlp_epochs']} epochs; "
             f"device {meta['device']}.", "",
             "Target = log10(K). R², MAE and maximum absolute error are min–max over "
             "seeds; KC is deterministic. Errors are in log10(K).", "",
             "| split | train / test | model | R² | MAE | max error |",
             "|---|---|---|---|---|---|"]
    for name, entry in results["splits"].items():
        for model in ("kozeny_carman", "mlp_ensemble", "mlp_noflag", "cnn"):
            if model not in entry:
                continue
            score = entry[model]
            if "skipped" in score:
                cells = f"skipped: {score['skipped']} | — | —"
            else:
                values = []
                for key in ("r2", "mae_log10", "max_abs_log10"):
                    v = score[key]
                    values.append(f"{min(v):.3f}–{max(v):.3f}" if isinstance(v, list)
                                  else f"{v:.3f}")
                cells = " | ".join(values)
            lines.append(f"| {name} | {entry['train']} / {entry['test']} | {model} | {cells} |")
    (outdir / "summary.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None, help="dataset run folder (default runs/weekend-20261030-sharded800)")
    ap.add_argument("--quick", action="store_true", help="smoke test: 1 seed, few epochs")
    ap.add_argument("--seeds", type=int, default=5, help="training seeds per model/split (default 5)")
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
        "base_seeds": [s * 1000 for s in range(n_seeds)],
        "cnn_epochs": cnn_epochs, "mlp_epochs": mlp_epochs, "device": device,
        "families": dict(Counter(r["family"] for r in rows))}}

    for name, (tr, te) in splits.items():
        print(f"\n=== {name}: train {len(tr)}, test {len(te)} ===", flush=True)
        entry = {"train": len(tr), "test": len(te)}
        # KC (deterministic)
        entry["kozeny_carman"] = kc_score(rows, tr, te)
        print(f"  KC      R2 {entry['kozeny_carman']['r2']:.3f}", flush=True)
        for model_name in (["mlp_ensemble", "mlp_noflag"] if name.startswith("unseen_")
                           else ["mlp_ensemble"]):
            scores = []
            for s in range(n_seeds):
                seed = s * 1000
                scores.append(mlp_score(rows, tr, te, seed=seed, epochs=mlp_epochs,
                                        noflag=model_name == "mlp_noflag"))
                print(f"  {model_name} seed {seed}: {scores[-1]}", flush=True)
            entry[model_name] = {k: [r[k] for r in scores]
                                 for k in ("r2", "mae_log10", "max_abs_log10")}
        # CNN (multiple seeds) — only when enough train samples and volumes exist
        if len(tr) >= 20 and len(te) >= 4:
            cnn_rs = []
            for s in range(n_seeds):
                cnn_rs.append(cnn_score(vols, rows, tr, te, seed=s * 1000, epochs=cnn_epochs, device=device))
                print(f"  CNN seed {s * 1000}: {cnn_rs[-1]}", flush=True)
            entry["cnn"] = {k: [r[k] for r in cnn_rs] for k in ("r2", "mae_log10", "max_abs_log10")}
        else:
            entry["cnn"] = {"skipped": f"train {len(tr)}, test {len(te)}"}
        results["splits"][name] = entry
        (outdir / "results.json").write_text(json.dumps(results, indent=1) + "\n")

    write_summary(outdir, results, stamp)
    print(f"\nresults: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
