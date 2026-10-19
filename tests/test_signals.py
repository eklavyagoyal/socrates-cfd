"""Signal analysis: synthetic signals with known answers + a real force history."""

from pathlib import Path

import numpy as np

from socrates.evidence.signals import analyze_unsteady, mser_truncation, spectral_peak_frequency, upcrossings

FX = Path(__file__).parent / "fixtures"


def synthetic(f=2.5, T=40.0, dt=0.002, cd0=1.3, amp=0.3, tau_grow=3.0, drift=0.0):
    t = np.arange(0.0, T, dt)
    env = 1.0 - np.exp(-t / tau_grow)
    cl = amp * env * np.sin(2 * np.pi * f * t)
    cd = cd0 * (1 - 0.1 * np.exp(-t / tau_grow)) + 0.01 * env * np.sin(4 * np.pi * f * t) + drift * t
    return t, cd, cl


def test_upcrossings_exact_for_sine():
    t = np.linspace(0, 10, 100001)
    x = np.sin(2 * np.pi * 1.0 * t)
    cr = upcrossings(t, x)
    assert np.allclose(np.diff(cr), 1.0, atol=1e-6)


def test_mser_finds_initial_bias():
    rng = np.random.default_rng(0)
    y = np.concatenate([np.linspace(5, 1, 20), 1 + 0.01 * rng.standard_normal(80)])
    d = mser_truncation(y)
    assert 15 <= d <= 25


def test_fft_peak_interpolated_beyond_bin_resolution():
    t = np.arange(0, 6.0, 0.001)
    sp = spectral_peak_frequency(t, np.sin(2 * np.pi * 2.37 * t))
    assert sp["resolution"] > 0.1
    assert abs(sp["frequency"] - 2.37) < 0.01


def test_analyze_recovers_known_frequency_and_mean():
    t, cd, cl = synthetic()
    r = analyze_unsteady(t, cd, cl, convective_time=0.1, declared_start=1.0)
    sw = r["stationary_window"]
    assert r["oscillating"]
    assert abs(sw["frequency_zero_crossing"] - 2.5) / 2.5 < 1e-4
    assert abs(sw["frequency_fft"] - 2.5) / 2.5 < 1e-3
    assert abs(sw["mean_cd"] - 1.3) / 1.3 < 1e-3
    assert abs(sw["cl_rms"] - 0.3 / np.sqrt(2)) < 1e-3
    # declared window starts inside the transient -> biased low
    assert r["declared_window"]["mean_cd"] < sw["mean_cd"]


def test_no_oscillation_reported_honestly():
    t = np.arange(0, 20, 0.01)
    r = analyze_unsteady(t, 1.1 + 0 * t, 1e-6 * np.sin(t), convective_time=0.1, declared_start=5.0)
    assert r["oscillating"] is False
    assert r["stationary_window"]["frequency"] is None


def test_real_coarse_mesh_history():
    z = np.load(FX / "A1_series_decimated.npz")
    tc = 0.01 / 0.15
    r = analyze_unsteady(z["t"], z["cd"], z["cl"], convective_time=tc, declared_start=75 * tc)
    sw = r["stationary_window"]
    assert r["oscillating"]
    st = sw["frequency_zero_crossing"] * 0.01 / 0.15
    assert 0.14 < st < 0.17
    assert abs(sw["frequency_fft"] - sw["frequency_zero_crossing"]) / sw["frequency_zero_crossing"] < 2e-3
    assert sw["n_cycles"] >= 8
