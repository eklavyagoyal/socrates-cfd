"""Core contracts: grid, backend, specs, run store, solver registry, gate records."""

from __future__ import annotations

import json
import math

import pytest
import torch

from physis.core.backend import get_backend
from physis.core.grid import Grid
from physis.core.result import SolverResult
from physis.core.spec import Spec
from physis.core.store import RunStore
from physis.solvers import base
from physis.verification.convergence import observed_order
from physis.verification.gates import Gate, GateFailure


def test_grid_centers_and_bounds(cpu64):
    g = Grid((4, 2), 0.5, (1.0, -1.0))
    c = g.centers(cpu64)
    assert c.shape == (4, 2, 2)
    assert c[0, 0].tolist() == [1.25, -0.75]
    assert c[3, 1].tolist() == [2.75, -0.25]
    assert g.upper == (3.0, 0.0)
    assert g.index_of((2.9, -0.1)) == (3, 1)
    assert g.refined(2).shape == (8, 4) and g.refined(2).spacing == 0.25


def test_grid_from_bounds_rejects_non_multiple():
    Grid.from_bounds((0.0, 0.0), (2.2, 0.41), 0.01)
    with pytest.raises(ValueError):
        Grid.from_bounds((0.0, 0.0), (1.0, 1.0), 0.3)


def test_backend_policy():
    v = get_backend("validation")
    assert v.dtype == torch.float64 and v.device.type in ("cpu", "cuda")
    f = get_backend("fast", device="cpu")
    assert f.dtype == torch.float32
    if torch.backends.mps.is_available():
        with pytest.raises(ValueError):
            get_backend("validation", device="mps")


class _Spec(Spec):
    n: int
    x: float


def test_spec_digest_is_canonical():
    assert _Spec(n=1, x=0.5).digest() == _Spec(x=0.5, n=1).digest()
    assert _Spec(n=1, x=0.5).digest() != _Spec(n=2, x=0.5).digest()
    with pytest.raises(Exception):
        _Spec(n=1, x=0.5, extra=3)


def _result(cpu64, value: float) -> SolverResult:
    g = Grid((3, 3), 1.0, (0.0, 0.0))
    return SolverResult(
        kind="test.dummy",
        grid=g,
        fields={"u": cpu64.ones(3, 3) * value},
        scalars={"cd": value},
        series={"t": cpu64.arange(5)},
        diagnostics={"steps": 5, "residual": torch.tensor(1e-9)},
        units={"cd": "1"},
    )


def test_store_roundtrip_reuse_and_failure(tmp_path, cpu64):
    store = RunStore(tmp_path)
    calls = []

    def compute():
        calls.append(1)
        return _result(cpu64, 2.0)

    rid, res = store.run("test.dummy", _Spec(n=1, x=0.5), compute, code_subpackage="core")
    assert res.scalars["cd"] == 2.0
    rid2, res2 = store.run("test.dummy", _Spec(n=1, x=0.5), compute, code_subpackage="core")
    assert rid2 == rid and len(calls) == 1
    assert torch.allclose(res2.fields["u"].double(), torch.full((3, 3), 2.0, dtype=torch.float64))
    rec = store.record(rid)
    assert rec["status"] == "completed" and rec["code"]["fingerprint"]

    def boom():
        raise RuntimeError("diverged")

    with pytest.raises(RuntimeError):
        store.run("test.dummy", _Spec(n=2, x=0.5), boom, code_subpackage="core")
    failed = [r for r in store.records() if r["status"] == "failed"]
    assert len(failed) == 1 and "diverged" in failed[0]["error"]


def test_solver_registry_and_run_stored(tmp_path, cpu64):
    @base.register
    class Dummy:
        kind = "test.registry_dummy"
        spec_type = _Spec

        def run(self, spec, backend):
            return SolverResult(kind=self.kind, grid=None, scalars={"y": spec.x * 2})

    assert base.get("test.registry_dummy") is Dummy
    rid, res = base.run_stored(Dummy(), _Spec(n=1, x=1.5), cpu64, RunStore(tmp_path))
    assert rid and res.scalars["y"] == 3.0


def test_observed_order():
    hs = [0.1, 0.05, 0.025]
    errs = [3 * h**2 for h in hs]
    assert observed_order(hs, errs) == pytest.approx(2.0)


def test_gate_record(tmp_path, monkeypatch):
    import physis.verification.gates as gates

    monkeypatch.setattr(gates, "RESULTS_DIR", tmp_path)
    g = Gate(name="unit.example", capability="test", reference={"source": "none"})
    g.metric("e", 0.01)
    assert g.check("e_small", 0.01, "<=", 0.02)
    g.finish()
    rec = json.loads((tmp_path / "unit.example.json").read_text())
    assert rec["status"] == "PASS" and rec["checks"][0]["pass"]

    bad = Gate(name="unit.bad", capability="test", reference={})
    bad.check("nan_is_fail", math.nan, "<=", 1.0)
    with pytest.raises(GateFailure):
        bad.finish()
    assert json.loads((tmp_path / "unit.bad.json").read_text())["status"] == "FAIL"
