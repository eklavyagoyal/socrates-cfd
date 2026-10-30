import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


spec = importlib.util.spec_from_file_location(
    "eval_generalization", Path(__file__).resolve().parents[1] / "scripts/eval_generalization.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


def test_low_porosity_split_has_requested_boundaries():
    rows = [{"porosity": p, "family": "voids"} for p in (0.44, 0.45, 0.49, 0.50, 0.6)]
    train, test = evaluation.make_splits(rows)["low_porosity"]
    assert train == [3, 4]
    assert test == [0]


def test_default_seeds_noflag_and_all_summary_metrics(tmp_path, monkeypatch):
    rows = [{"porosity": p, "family": family}
            for family in ("spheres", "voids", "gyroid")
            for p in (0.4, 0.6, 0.8) for _ in range(5)]
    monkeypatch.setattr(evaluation, "ROOT", tmp_path)
    monkeypatch.setattr(evaluation, "load_dataset", lambda _: (rows, np.zeros((len(rows), 1))))
    mlp_calls, cnn_calls = [], []

    def scores(seed):
        return {"r2": seed / 10000, "mae_log10": seed / 20000,
                "max_abs_log10": seed / 4000}

    def mlp(rows, tr, te, seed, epochs, *, noflag=False):
        mlp_calls.append((seed, noflag))
        return scores(seed)

    def cnn(vols, rows, tr, te, seed, epochs, device):
        cnn_calls.append(seed)
        return scores(seed)

    monkeypatch.setattr(evaluation, "mlp_score", mlp)
    monkeypatch.setattr(evaluation, "cnn_score", cnn)
    monkeypatch.setattr(evaluation, "kc_score", lambda *_: scores(0))
    monkeypatch.setattr(sys, "argv", ["eval_generalization.py"])
    assert evaluation.main() == 0
    expected = [0, 1000, 2000, 3000, 4000]
    assert [seed for seed, noflag in mlp_calls if not noflag] == expected * 6
    assert [seed for seed, noflag in mlp_calls if noflag] == expected * 3
    assert cnn_calls == expected * 6
    out = next((tmp_path / "runs").iterdir())
    result = json.loads((out / "results.json").read_text())
    assert result["meta"]["base_seeds"] == expected
    for name, entry in result["splits"].items():
        assert ("mlp_noflag" in entry) == name.startswith("unseen_")
    summary = (out / "summary.md").read_text()
    assert "0.000–0.400 | 0.000–0.200 | 0.000–1.000" in summary
    assert "low_porosity" in summary and "mlp_noflag" in summary


def test_noflag_uses_only_porosity_and_log_surface_for_fit_and_predict(monkeypatch):
    rows = [{"porosity": p, "specific_surface": surface, "family": family,
             "permeability": 1e-4 * (i + 1)}
            for i, (p, surface, family) in enumerate(
                [(0.4, 10, "spheres"), (0.5, 100, "gyroid"),
                 (0.6, 1000, "voids"), (0.7, 10000, "gyroid")])]
    inputs = {}

    class Ensemble:
        def __init__(self, **kwargs):
            pass

        def fit(self, x, y):
            inputs["fit"] = x
            return self

        def predict(self, x):
            inputs["predict"] = x
            return np.zeros(len(x)), np.zeros(len(x))

    monkeypatch.setattr(evaluation.closure, "MLPEnsemble", Ensemble)
    evaluation.mlp_score(rows, [0, 2], [1, 3], seed=0, epochs=1, noflag=True)
    np.testing.assert_allclose(inputs["fit"], [[0.4, 1], [0.6, 3]])
    np.testing.assert_allclose(inputs["predict"], [[0.5, 2], [0.7, 4]])
