import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace


spec = importlib.util.spec_from_file_location(
    "percolation_resolution", Path(__file__).resolve().parents[1] / "scripts/percolation_resolution.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_stored_geometry_steps_and_resume_after_failure(tmp_path, monkeypatch):
    geometry = {"type": "periodic_spheres", "seed": 123, "voids": True}
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text(json.dumps({"index": 583, "family": "voids", "geometry": geometry}) + "\n")
    out = tmp_path / "results.jsonl"
    monkeypatch.setattr(sys, "argv", ["percolation_resolution.py", "--dataset", str(dataset),
                                     "--out", str(out), "--indices", "583"])
    monkeypatch.setattr(study, "get_backend", lambda *a, **kw: SimpleNamespace(device="cuda:0"))
    monkeypatch.setattr(study.triton_kernel, "selfcheck", lambda _: (True, "pass"))
    monkeypatch.setattr(study.torch.cuda, "empty_cache", lambda: None)
    monkeypatch.setattr(study.torch.cuda, "mem_get_info", lambda _: (32 * 2**30, 32 * 2**30))
    calls = []

    def run(geom, n, backend, *, impl, max_steps):
        assert geom == geometry and impl == "triton"
        assert max_steps == (400_000 if n == 128 else 800_000)
        calls.append(n)
        if n == 192 and calls.count(192) == 1:
            raise RuntimeError("injected solver failure")
        return {"porosity": 0.4, "permeability": 1e-6 * n / 128,
                "steps": 100, "status": "ok", "converged": True, "impl": impl}

    monkeypatch.setattr(study.rve, "run_rve", run)
    assert study.main() == 1
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert len(rows) == 3 and rows[1]["status"] == "error"
    assert "injected solver failure" in rows[1]["error"]
    assert rows[2]["K_relative_to_128"] == 2.0
    assert study.main() == 0
    assert calls == [128, 192, 256, 192]
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert rows[-1]["n"] == 192 and rows[-1]["K_relative_to_128"] == 1.5
    assert study.main() == 0
    assert len(out.read_text().splitlines()) == 4


def test_failed_baseline_defers_higher_resolutions_until_resume(tmp_path, monkeypatch):
    geometry = {"type": "periodic_spheres", "seed": 456, "voids": True}
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text(json.dumps({"index": 583, "family": "voids", "geometry": geometry}) + "\n")
    out = tmp_path / "results.jsonl"
    monkeypatch.setattr(sys, "argv", ["percolation_resolution.py", "--dataset", str(dataset),
                                     "--out", str(out), "--indices", "583"])
    monkeypatch.setattr(study, "get_backend", lambda *a, **kw: SimpleNamespace(device="cuda:0"))
    monkeypatch.setattr(study.triton_kernel, "selfcheck", lambda _: (True, "pass"))
    monkeypatch.setattr(study.torch.cuda, "empty_cache", lambda: None)
    monkeypatch.setattr(study.torch.cuda, "mem_get_info", lambda _: (32 * 2**30, 32 * 2**30))
    calls = []

    def run(geom, n, backend, **kwargs):
        calls.append(n)
        if calls == [128]:
            raise RuntimeError("baseline failed")
        return {"porosity": 0.4, "permeability": 1e-6 * n / 128,
                "steps": 100, "status": "ok", "converged": True, "impl": "triton"}

    monkeypatch.setattr(study.rve, "run_rve", run)
    assert study.main() == 1
    assert calls == [128]
    assert study.main() == 0
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [r["K_relative_to_128"] for r in rows[1:]] == [1.0, 1.5, 2.0]
    assert calls == [128, 128, 192, 256]
