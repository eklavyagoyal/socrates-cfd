"""Deterministic analysis of force-coefficient time histories.

Methods (see docs/methodology.md for sources):

* Shedding cycles are delimited by upward zero crossings of the lift
  coefficient about its median, located by linear interpolation.
* The start-up transient is removed with the Marginal Standard Error Rule
  (MSER; White 1997, Simulation 69:323) applied to the per-cycle series
  (cycle-mean Cd and cycle lift amplitude).  Working on per-cycle values
  removes the periodic component, so MSER sees only the slow drift.
* Mean quantities are averaged over an integer number of complete cycles,
  which removes the bias of a partial period.
* Shedding frequency is computed two independent ways: mean period from
  zero crossings, and the peak of a Hann-windowed, zero-padded FFT with
  parabolic peak interpolation.  Their disagreement is itself evidence.
* Statistical uncertainty of a mean uses per-cycle values as batch means
  (cycle means of a limit-cycle oscillation are close to independent; the
  lag-1 autocorrelation is reported so this can be checked).
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def upcrossings(t: np.ndarray, x: np.ndarray, level: float = 0.0) -> np.ndarray:
    """Times at which ``x`` crosses ``level`` upwards (linear interpolation)."""
    y = x - level
    idx = np.nonzero((y[:-1] < 0.0) & (y[1:] >= 0.0))[0]
    if idx.size == 0:
        return np.empty(0)
    t0, t1 = t[idx], t[idx + 1]
    y0, y1 = y[idx], y[idx + 1]
    return t0 + (t1 - t0) * (-y0) / (y1 - y0)


def mser_truncation(y: np.ndarray, max_fraction: float = 0.5) -> int:
    """MSER truncation index d* = argmin_d  sum_{i>=d}(y_i - mean_d)^2 / (n-d)^2.

    The search is restricted to d <= max_fraction*n, as recommended because
    the statistic becomes unstable when few points remain.
    """
    n = len(y)
    if n < 4:
        return 0
    best_d, best = 0, np.inf
    for d in range(0, int(max_fraction * n) + 1):
        tail = y[d:]
        m = len(tail)
        if m < 2:
            break
        val = np.sum((tail - tail.mean()) ** 2) / m**2
        if val < best - 1e-18:
            best, best_d = val, d
    return best_d


def spectral_peak_frequency(t: np.ndarray, x: np.ndarray, pad_factor: int = 8) -> dict:
    """Dominant frequency of ``x(t)`` via Hann-windowed FFT (uniform resampling)."""
    if len(t) < 16 or t[-1] <= t[0]:
        return {"frequency": None, "resolution": None, "reason": "record too short"}
    n = len(t)
    tu = np.linspace(t[0], t[-1], n)
    xu = np.interp(tu, t, x)
    xu = xu - xu.mean()
    if np.allclose(xu, 0.0):
        return {"frequency": None, "resolution": 1.0 / (t[-1] - t[0]), "reason": "signal is constant"}
    w = np.hanning(n)
    nfft = int(2 ** np.ceil(np.log2(n * pad_factor)))
    spec = np.abs(np.fft.rfft(xu * w, nfft))
    freqs = np.fft.rfftfreq(nfft, d=tu[1] - tu[0])
    k = int(np.argmax(spec[1:]) + 1)
    if 1 <= k < len(spec) - 1:
        a, b, c = np.log(spec[k - 1] + 1e-300), np.log(spec[k] + 1e-300), np.log(spec[k + 1] + 1e-300)
        denom = a - 2 * b + c
        delta = 0.5 * (a - c) / denom if denom != 0 else 0.0
    else:
        delta = 0.0
    f = (k + delta) * (freqs[1] - freqs[0])
    return {"frequency": float(f), "resolution": float(1.0 / (t[-1] - t[0])), "reason": None}


def _t_quantile(n: int) -> float:
    return float(stats.t.ppf(0.975, max(n - 1, 1)))


def analyze_unsteady(
    t: np.ndarray,
    cd: np.ndarray,
    cl: np.ndarray,
    *,
    convective_time: float,
    declared_start: float | None,
    oscillation_rms_threshold: float = 1e-3,
) -> dict:
    """Full analysis of a transient force history (times in seconds).

    Returns a JSON-serialisable dict.  Nothing is filled with a default
    'good' value: absent quantities are None with a reason.
    """
    out: dict = {
        "record_start": float(t[0]) if len(t) else None,
        "record_end": float(t[-1]) if len(t) else None,
        "record_length_convective": float((t[-1] - t[0]) / convective_time) if len(t) else 0.0,
        "n_samples": int(len(t)),
    }
    if len(t) < 20:
        out["oscillating"] = None
        out["reason"] = "fewer than 20 force samples"
        return out

    # --- is there a sustained oscillation? --------------------------------
    # amplitude judged on the last quarter (is it still oscillating at the
    # end?), crossings counted on the last half (enough cycles to count)
    last = t >= t[0] + 0.75 * (t[-1] - t[0])
    half_rec = t >= t[0] + 0.5 * (t[-1] - t[0])
    cl_rms_last = float(np.std(cl[last]))
    n_cross_last = len(upcrossings(t[half_rec], cl[half_rec], float(np.median(cl[half_rec]))))
    oscillating = cl_rms_last > oscillation_rms_threshold and n_cross_last >= 3
    out.update(
        oscillating=bool(oscillating),
        cl_rms_last_quarter=cl_rms_last,
        upcrossings_last_half=int(n_cross_last),
        oscillation_rms_threshold=oscillation_rms_threshold,
    )

    # --- declared window (what the case author would report) -------------
    dec: dict = {"start": declared_start}
    if declared_start is not None and declared_start < t[-1]:
        m = t >= declared_start
        if m.sum() >= 2:
            tt, cdw, clw = t[m], cd[m], cl[m]
            # time-weighted averages (trapezoid), as a naive post-processing would do
            span = tt[-1] - tt[0]
            dec["mean_cd"] = float(np.trapezoid(cdw, tt) / span) if span > 0 else float(cdw.mean())
            dec["cl_rms"] = float(np.sqrt(np.trapezoid((clw - clw.mean()) ** 2, tt) / span)) if span > 0 else 0.0
            sp = spectral_peak_frequency(tt, clw)
            dec["frequency_fft"] = sp["frequency"]
            dec["frequency_resolution"] = sp["resolution"]
            dec["length_convective"] = float(span / convective_time)
            if oscillating:
                cr = upcrossings(tt, clw, float(np.median(clw)))
                dec["complete_cycles"] = int(max(len(cr) - 1, 0))
            else:
                dec["complete_cycles"] = 0
    else:
        dec["reason"] = "declared averaging start is missing or after the end of the record"
    out["declared_window"] = dec

    if not oscillating:
        # steady-wake or decayed solution: report the tail mean only
        tail = t >= t[0] + 0.5 * (t[-1] - t[0])
        out["stationary_window"] = {
            "method": "no oscillation detected; mean of second half of record",
            "mean_cd": float(np.mean(cd[tail])),
            "cl_rms": float(np.std(cl[tail])),
            "mean_cl": float(np.mean(cl[tail])),
            "frequency": None,
            "cd_relative_drift_second_half": float(
                (np.mean(cd[tail][len(cd[tail]) // 2 :]) - np.mean(cd[tail][: len(cd[tail]) // 2]))
                / max(abs(np.mean(cd[tail])), 1e-30)
            ),
        }
        return out

    # --- cycles over the whole record --------------------------------------
    level = float(np.median(cl[t >= t[0] + 0.5 * (t[-1] - t[0])]))
    cr = upcrossings(t, cl, level)
    cycles = []
    for a, b in zip(cr[:-1], cr[1:]):
        m = (t >= a) & (t <= b)
        if m.sum() < 4:
            continue
        tt = t[m]
        span = tt[-1] - tt[0]
        cycles.append(
            {
                "t_start": float(a),
                "t_end": float(b),
                "period": float(b - a),
                "mean_cd": float(np.trapezoid(cd[m], tt) / span),
                "cl_amplitude": float(0.5 * (cl[m].max() - cl[m].min())),
                "cd_amplitude": float(0.5 * (cd[m].max() - cd[m].min())),
            }
        )
    out["n_cycles_total"] = len(cycles)
    if len(cycles) < 4:
        out["stationary_window"] = {"reason": f"only {len(cycles)} complete cycles in record"}
        return out

    cyc_cd = np.array([c["mean_cd"] for c in cycles])
    cyc_amp = np.array([c["cl_amplitude"] for c in cycles])
    cyc_T = np.array([c["period"] for c in cycles])
    d_cd = mser_truncation(cyc_cd)
    d_amp = mser_truncation(cyc_amp)
    d_T = mser_truncation(cyc_T)
    d = max(d_cd, d_amp, d_T)
    stat_cycles = cycles[d:]
    n = len(stat_cycles)
    t_a, t_b = stat_cycles[0]["t_start"], stat_cycles[-1]["t_end"]
    m = (t >= t_a) & (t <= t_b)
    tt = t[m]
    span = tt[-1] - tt[0]
    mean_cd = float(np.trapezoid(cd[m], tt) / span)
    mean_cl = float(np.trapezoid(cl[m], tt) / span)
    cl_rms = float(np.sqrt(np.trapezoid((cl[m] - mean_cl) ** 2, tt) / span))
    periods = cyc_T[d:]
    f_zc = float(1.0 / periods.mean())
    sp = spectral_peak_frequency(tt, cl[m])

    cyc_cd_s = cyc_cd[d:]
    q = _t_quantile(n)
    se_cd = float(cyc_cd_s.std(ddof=1) / np.sqrt(n)) if n > 1 else None
    se_T = float(periods.std(ddof=1) / np.sqrt(n)) if n > 1 else None
    lag1 = float(np.corrcoef(cyc_cd_s[:-1], cyc_cd_s[1:])[0, 1]) if n > 3 and cyc_cd_s.std() > 0 else None
    # linear drift of cycle means across the window, expressed as total change / mean
    tc = np.array([0.5 * (c["t_start"] + c["t_end"]) for c in stat_cycles])
    slope = float(np.polyfit(tc, cyc_cd_s, 1)[0]) if n > 2 else 0.0
    drift_rel = float(slope * (t_b - t_a) / mean_cd)
    amp = cyc_amp[d:]
    amp_drift = float(np.polyfit(tc, amp, 1)[0] * (t_b - t_a) / max(amp.mean(), 1e-30)) if n > 2 else 0.0
    half = n // 2
    out["stationary_window"] = {
        "method": "MSER on per-cycle mean Cd, lift amplitude and period; integer cycles",
        "truncated_cycles": int(d),
        "mser_index": {"mean_cd": int(d_cd), "cl_amplitude": int(d_amp), "period": int(d_T)},
        "start": float(t_a),
        "end": float(t_b),
        "n_cycles": int(n),
        "length_convective": float((t_b - t_a) / convective_time),
        "mean_cd": mean_cd,
        "mean_cl": mean_cl,
        "cl_rms": cl_rms,
        "cl_amplitude_mean": float(amp.mean()),
        "cd_amplitude_mean": float(np.mean([c["cd_amplitude"] for c in stat_cycles])),
        "frequency_zero_crossing": f_zc,
        "frequency_fft": sp["frequency"],
        "frequency_fft_resolution": sp["resolution"],
        "period_cv": float(periods.std(ddof=1) / periods.mean()) if n > 1 else None,
        "mean_cd_ci95_halfwidth": float(q * se_cd) if se_cd is not None else None,
        "period_ci95_halfwidth": float(q * se_T) if se_T is not None else None,
        "cycle_mean_cd_lag1_autocorr": lag1,
        "mean_cd_relative_drift": drift_rel,
        "cl_amplitude_relative_drift": amp_drift,
        "mean_cd_half_difference_rel": float(
            (cyc_cd_s[half:].mean() - cyc_cd_s[:half].mean()) / mean_cd
        )
        if n >= 4
        else None,
    }
    out["cycle_table"] = {
        "t_start": [c["t_start"] for c in cycles],
        "mean_cd": cyc_cd.tolist(),
        "cl_amplitude": cyc_amp.tolist(),
        "period": cyc_T.tolist(),
    }
    return out


def analyze_steady(it: np.ndarray, cd: np.ndarray, cl: np.ndarray, window_fraction: float = 0.1) -> dict:
    """Steady (pseudo-time iteration) history: final values and their settling."""
    n = len(it)
    if n < 10:
        return {"reason": "fewer than 10 iterations recorded"}
    k = max(int(window_fraction * n), 5)
    tail_cd, tail_cl = cd[-k:], cl[-k:]
    return {
        "iterations": int(it[-1]),
        "final_cd": float(cd[-1]),
        "final_cl": float(cl[-1]),
        "tail_window_iterations": int(k),
        "tail_cd_relative_range": float((tail_cd.max() - tail_cd.min()) / max(abs(cd[-1]), 1e-30)),
        "tail_cl_range": float(tail_cl.max() - tail_cl.min()),
    }
