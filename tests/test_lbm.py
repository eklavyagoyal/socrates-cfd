"""LBM D3Q19 TRT: lattice constants, conservation, the Metal kernel against the torch reference."""

from __future__ import annotations

import pytest
import torch

from physis.solvers.lbm import PeriodicFlow, PeriodicFlowSpec, lattice, metal, trt
from physis.solvers.lbm.periodic import _reductions, bytes_needed, choose_impl

needs_metal = pytest.mark.skipif(not metal.available(), reason="needs an Apple GPU (MPS + compile_shader)")


def test_d3q19_lattice_moments():
    c = torch.tensor(lattice.C, dtype=torch.float64)
    w = torch.tensor(lattice.W, dtype=torch.float64)
    assert abs(float(w.sum()) - 1.0) < 1e-15
    assert torch.allclose(w @ c, torch.zeros(3, dtype=torch.float64))
    second = torch.einsum("q,qa,qb->ab", w, c, c)
    assert torch.allclose(second, lattice.CS2 * torch.eye(3, dtype=torch.float64))
    for i, o in enumerate(lattice.OPP):
        assert lattice.OPP[o] == i
        assert tuple(-x for x in lattice.C[i]) == lattice.C[o]
    for i in range(1, lattice.Q, 2):
        assert lattice.OPP[i] == i + 1  # opposite pairs are neighbours (kernel and docs rely on it)


def test_tau_minus_magic():
    tm = lattice.tau_minus(0.8)
    assert abs((0.8 - 0.5) * (tm - 0.5) - lattice.MAGIC) < 1e-15
    with pytest.raises(ValueError):
        lattice.tau_minus(0.5)


def _random_case(seed: int = 0, shape=(10, 9, 8), solid_fraction=0.25):
    gen = torch.Generator().manual_seed(seed)
    solid = torch.rand(shape, generator=gen) < solid_fraction
    h = 1e-3 * torch.randn(19, *shape, generator=gen, dtype=torch.float64)
    h[:, solid] = 0.0
    return solid, h


def test_reference_step_conserves_mass_and_keeps_rest(cpu64):
    solid, h = _random_case()
    lat = trt.Lattice(solid, cpu64)
    g = cpu64.tensor([0.0, 0.0, 0.0])
    out = h
    for _ in range(10):
        out = lat.step(out, g, 1 / 0.9, 1 / lattice.tau_minus(0.9))
    assert abs(float(out.sum() - h.sum())) < 1e-13
    rest = lat.step(lat.rest(), g, 1.0, 1.0)
    assert float(rest.abs().max()) == 0.0


def test_force_adds_exact_momentum(cpu64):
    solid = torch.zeros((6, 5, 4), dtype=torch.bool)
    lat = trt.Lattice(solid, cpu64)
    g = cpu64.tensor([1e-4, -2e-5, 3e-5])
    h = lat.step(lat.rest(), g, 1 / 1.2, 1 / lattice.tau_minus(1.2))
    rho, u = lat.macroscopic(h, g)
    # from rest, one step leaves u = (0 + F/2) / rho: the velocity of that step
    assert torch.allclose(u, (0.5 * g).view(3, 1, 1, 1).expand_as(u) / rho, atol=1e-15)


@needs_metal
def test_metal_kernel_matches_reference(cpu64):
    solid, h = _random_case(seed=3, shape=(12, 10, 9))
    lat = trt.Lattice(solid, cpu64)
    g = cpu64.tensor([1e-5, -2e-6, 3e-6])
    wp, wm = 1 / 0.9, 1 / lattice.tau_minus(0.9)
    ref = h
    for _ in range(25):
        ref = lat.step(ref, g, wp, wm)
    got = metal.MetalStepper(solid, h.float().to("mps")).run(25, g.tolist(), wp, wm).cpu().double()
    assert float((got - ref).abs().max()) < 1e-8 * max(1.0, float(ref.abs().max())) + 1e-9
    assert abs(float(got.sum() - h.sum())) < 1e-5  # float32 mass bookkeeping over 25 steps


def _sphere_spec(L: int, chi: float, **kw) -> PeriodicFlowSpec:
    return PeriodicFlowSpec(
        grid={"shape": [L, L, L], "spacing": 1.0, "origin": [0.0, 0.0, 0.0]},
        geometry={"type": "ball", "center": [L / 2, L / 2, L / 2], "radius": chi * L / 2},
        force=(1e-6, 0.0, 0.0), check_every=100, keep_fields=False, **kw)


@pytest.mark.slow
@needs_metal
def test_metal_and_float64_reference_agree_on_permeability(cpu64):
    """The documented float32-vs-float64 check of ADR-0001 for this solver."""
    from physis.core.backend import get_backend

    fast = get_backend("fast", device="mps")
    k64 = PeriodicFlow().run(_sphere_spec(20, 0.7, tol=1e-10, impl="torch"), cpu64).scalars["permeability_lu"]
    k32 = PeriodicFlow().run(_sphere_spec(20, 0.7, tol=1e-8, impl="metal"), fast).scalars["permeability_lu"]
    assert abs(k32 / k64 - 1) < 1e-4


def test_spec_rejects_bad_input():
    with pytest.raises(ValueError):
        _sphere_spec(8, 0.5, tau_plus=0.5)
    with pytest.raises(ValueError):
        PeriodicFlowSpec(grid={"shape": [4, 4, 4], "spacing": 1.0, "origin": [0, 0, 0]}, force=(0.0, 0.0, 0.0))


def test_generated_triton_kernel_logic_matches_reference(cpu64):
    """The generated Triton kernel, run through a CPU emulation of the Triton subset it uses.
    Checks indexing, periodic wrap, bounce-back and the TRT pair update; GPU compilation is
    checked on CUDA machines by ``triton_kernel.selfcheck``."""
    from triton_shim import load_emulated_kernel_module

    mod = load_emulated_kernel_module()
    mod.BLOCK = 128
    solid, h = _random_case(seed=5, shape=(7, 6, 5), solid_fraction=0.3)
    g = (1e-5, -2e-6, 3e-6)
    wp, wm = 1 / 0.9, 1 / lattice.tau_minus(0.9)
    lat = trt.Lattice(solid, cpu64)
    ref = h
    for _ in range(4):
        ref = lat.step(ref, cpu64.tensor(g), wp, wm)
    st = mod.TritonStepper.__new__(mod.TritonStepper)
    st.solid, st.shape = solid.to(torch.uint8).contiguous(), tuple(solid.shape)
    st.n = st.solid.numel()
    st.a, st.b = h.float().contiguous(), torch.empty(h.shape, dtype=torch.float32)
    got = st.run(4, g, wp, wm).double()
    assert float((got - ref).abs().max()) < 1e-5 * float(ref.abs().max()) + 1e-9


def test_reductions_match_full_macroscopic(cpu64):
    solid, h = _random_case(seed=9)
    lat = trt.Lattice(solid, cpu64)
    g = (2e-5, 0.0, -1e-5)
    rho, u = lat.macroscopic(h, cpu64.tensor(g))
    norm = (g[0] ** 2 + g[2] ** 2) ** 0.5
    d = (g[0] / norm, 0.0, g[2] / norm)
    r = _reductions(h, cpu64.tensor(lattice.C), g, d, ~solid, speed=True)
    assert abs(r["ud"] - float((u[0] * d[0] + u[2] * d[2]).mean())) < 1e-15
    assert abs(r["umax"] - float(torch.linalg.vector_norm(u, dim=0).max())) < 1e-15


def test_impl_choice_and_memory_estimate(cpu64, cpu32):
    assert choose_impl("auto", cpu64) == "torch"
    assert choose_impl("auto", cpu32) == "torch"
    with pytest.raises(ValueError):
        choose_impl("triton", cpu32)
    assert bytes_needed((512, 512, 512), "triton") < 32 * 2**30 * 0.8  # fits a 32 GB card
    assert bytes_needed((512, 512, 512), "torch") > bytes_needed((512, 512, 512), "triton")


def test_short_last_window_is_not_convergence(cpu64):
    """max_steps that is not a multiple of check_every leaves a short last window; the tiny
    change over it must not be reported as convergence (seen on the RTX 5090 run)."""
    spec = _sphere_spec(16, 0.6, tol=1e-12, max_steps=410, impl="torch")  # windows of 100, last one 10 steps
    r = PeriodicFlow().run(spec, cpu64)
    assert r.diagnostics["steps"] == 410
    assert r.diagnostics["converged"] is False
