"""Baseline validation: evidence summary, solution verification, truth, literature comparison.

    python scripts/make_baseline_report.py
Writes results/baseline/truth.json, results/baseline/summary.json,
reports/figures/baseline_forces.png and reports/baseline_generated.md
(the data section included in reports/baseline_validation.md).
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from socrates.case_generation.spec import ProblemSpec  # noqa: E402
from socrates.checks.verifier import verify  # noqa: E402
from socrates.orchestration.loop import graph_for  # noqa: E402
from socrates.orchestration.store import RunStore  # noqa: E402
from socrates.orchestration.truth import combine_truth, extrapolate_chain  # noqa: E402

LIT = {  # research.md section 2.3 (reference band; NOT used by the verifier)
    "mean_drag_coefficient": {"band": (1.31, 1.33), "wide": (1.30, 1.35)},
    "strouhal_number": {"band": (0.164, 0.166), "wide": (0.162, 0.167)},
    "rms_lift_coefficient": {"band": (0.222, 0.235), "wide": (0.215, 0.235)},
}
QS = ["mean_drag_coefficient", "strouhal_number", "rms_lift_coefficient"]


def sta(store, rid):
    return (store.load(rid).evidence.get("qoi") or {}).get("stationary") or {}


def main() -> None:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    study = json.loads((REPO / "results" / "baseline" / "study.json").read_text())
    root = study["root"]
    ch = {k: [root] + [e["run_id"] for e in v] for k, v in study["chains"].items()}
    rb = store.load(root)
    ev = rb.evidence

    def size(factor, rid):
        r = store.load(rid)
        if factor == "mesh":
            return r.evidence["mesh"]["representative_cell_size_D"]
        if factor == "time":
            return r.config.time.delta_t
        return 1.0 / r.config.domain.half_height

    truth, chains_out, overlap = {}, {}, {}
    dt_root = rb.config.time.delta_t
    for q in QS:
        per = {}
        for factor, order in (("time", 2.0), ("mesh", 2.0), ("domain", 1.0)):
            rids = ch[factor]
            vals = [sta(store, r).get(q) for r in rids]
            if factor == "mesh":
                # The mesh chain also lowers dt (Courant control), so its raw values contain part of the
                # time error that the time chain already corrects for (double counting).  Shift every mesh
                # level to the baseline dt with the time chain's own error model e(dt) = C dt^p.
                tc = per["time"]
                p_t = tc["order"] if tc.get("order") and 0.5 * 2.0 <= tc["order"] <= 4.0 else 2.0
                c_t = (sta(store, root)[q] - tc["extrapolated"]) / dt_root ** p_t
                dts = [store.load(r).config.time.delta_t for r in rids]
                shift = [c_t * (dt ** p_t - dt_root ** p_t) for dt in dts]
                raw = extrapolate_chain(vals, [size(factor, r) for r in rids], order)
                vals = [v - sh for v, sh in zip(vals, shift)]
                overlap[q] = {"mesh_level_dt": dts, "time_error_model": {"C": c_t, "p": p_t},
                              "shift_applied": shift, "mesh_extrapolated_without_shift": raw["extrapolated"]}
            per[factor] = extrapolate_chain(vals, [size(factor, r) for r in rids], order)
            per[factor]["runs"] = rids
        root_v = sta(store, root)[q]
        truth[q] = combine_truth(root_v, per)
        truth[q]["root_value"] = root_v
        if q in overlap:
            no_shift = dict(per, mesh=dict(per["mesh"], extrapolated=overlap[q]["mesh_extrapolated_without_shift"]))
            overlap[q]["truth_without_shift"] = combine_truth(root_v, no_shift)["value"]
            truth[q]["time_overlap_correction"] = overlap[q]
        chains_out[q] = per
        lo, hi = LIT[q]["band"]
        truth[q]["literature_band"] = [lo, hi]
        truth[q]["in_band"] = lo <= truth[q]["value"] <= hi
    (REPO / "results" / "baseline" / "truth.json").write_text(
        json.dumps({"truth": truth, "chains": chains_out, "root": root}, indent=1, default=float))

    # full-study verification verdict of the baseline
    all_runs = [root] + [e["run_id"] for v in study["chains"].values() for e in v]
    g = graph_for(store, root, all_runs)
    v = verify(g, spec)
    static = verify(graph_for(store, root, [root]), spec)

    # ---------- figure ----------
    s = store.load(root).series()
    tc = rb.config.convective_time
    t = s["t"] / tc
    fig, axs = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True)
    axs[0].plot(t, s["cl"], lw=0.8, color="#2a78d6")
    axs[0].set_ylabel("Cl", fontsize=8.5)
    axs[0].set_ylim(-0.6, 0.6)
    axs[1].plot(t, s["cd"], lw=0.8, color="#2a78d6")
    axs[1].set_ylabel("Cd", fontsize=8.5)
    axs[1].set_ylim(1.2, 1.45)
    tb = ev["temporal_behavior"]
    for ax in axs:
        ax.axvspan(rb.config.averaging.start_time, t[-1], color="#e7e6e2", lw=0)
        ax.axvline(tb["transient_end_time_convective"], color="#52514e", lw=0.8, ls="--")
        ax.grid(color="#efeeea", lw=0.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axs[1].set_xlabel("t U / D", fontsize=8.5)
    axs[0].set_title("Baseline force history (shaded: declared averaging window; dashed: start of the stationary window)",
                     fontsize=8.5)
    fig.tight_layout()
    (REPO / "reports" / "figures").mkdir(parents=True, exist_ok=True)
    fig.savefig(REPO / "reports" / "figures" / "baseline_forces.png", dpi=160)
    plt.close(fig)

    # ---------- generated markdown ----------
    cm = ev["mesh"]["checkMesh"]
    sol = ev["solver"]
    sw = ev["forces"]["stationary_window"]
    L = []
    L.append(f"_Generated by `scripts/make_baseline_report.py` from run `{root}` and its study runs._\n")
    L.append("### Run diagnostics (baseline)\n")
    L.append("| item | value |\n|---|---|")
    L += [f"| cells | {cm['cells']} |",
          f"| checkMesh | {'Mesh OK' if cm['mesh_ok'] else 'FAILED'}; max non-orth {cm['max_non_orthogonality']:.1f}°, max skewness {cm['max_skewness']:.2f}, max aspect ratio {cm['max_aspect_ratio']:.1f} |",
          f"| representative cell size h | {ev['mesh']['representative_cell_size_D']:.4f} D |",
          f"| solver completed | {sol['completed']} ({sol['n_steps']} steps, {sol['execution_time_s']:.0f} s CPU) |",
          f"| max Courant number | {sol['courant_max']:.3f} |",
          f"| final p-solve converged | {100 * (1 - sol['p_last_solve_unconverged_fraction_1e-7']):.1f} % of steps |",
          f"| continuity error (sum local, max) | {sol['continuity_sum_local_max']:.2e} |",
          f"| boundary mass imbalance (max) | {ev['conservation']['relative_imbalance_max']:.2e} |",
          f"| stationary-window start (MSER{', at its 50 % cap' if tb.get('mser_hit_cap') else ''}) | "
          f"{tb['transient_end_time_convective']:.1f} D/U |",
          f"| stationary cycles | {sw['n_cycles']} |",
          f"| steps per shedding period | {tb['steps_per_period']:.0f} |",
          f"| Cd 95 % CI half-width (batch means) | {sw['mean_cd_ci95_halfwidth']:.2e} |"]
    L.append("\n### Quantities of interest vs literature (research.md §2.3)\n")
    L.append("| quantity | reported (declared window) | stationary | literature band | in band |\n|---|---|---|---|---|")
    rep = ev["qoi"]["reported"]
    st = ev["qoi"]["stationary"]
    for q in QS:
        lo, hi = LIT[q]["band"]
        L.append(f"| {q} | {rep.get(q):.4f} | {st.get(q):.4f} | {lo}–{hi} | {lo <= st[q] <= hi} |")
    L.append("\n### One-factor-at-a-time verification study\n")
    L.append("| factor | run | size | Cd | St | Cl rms |\n|---|---|---|---|---|---|")
    for factor in ("mesh", "time", "domain"):
        for rid in ch[factor]:
            x = sta(store, rid)
            L.append(f"| {factor} | `{rid}` | {size(factor, rid):.4g} | {x.get('mean_drag_coefficient', float('nan')):.4f} | "
                     f"{x.get('strouhal_number', float('nan')):.4f} | {x.get('rms_lift_coefficient', float('nan')):.4f} |")
    for rid in ch["longer"][1:]:
        x = sta(store, rid)
        L.append(f"| run longer (250 D/U) | `{rid}` | — | {x['mean_drag_coefficient']:.4f} | {x['strouhal_number']:.4f} | {x['rms_lift_coefficient']:.4f} |")
    L.append("\n### Richardson extrapolation per factor and combined in-house reference\n")
    L.append("| quantity | factor | method | extrapolated | correction vs baseline |\n|---|---|---|---|---|")
    for q in QS:
        for factor, c in chains_out[q].items():
            L.append(f"| {q} | {factor} | {c['method']} | {c['extrapolated']:.5f} | {truth[q]['corrections'][factor]:+.5f} |")
    L.append("\nMesh levels were run with dt = " + ", ".join(f"{d:.5g}" for d in overlap[QS[0]]["mesh_level_dt"])
             + " (Courant control), so each mesh level is shifted to the baseline dt with the time chain's error model "
               "C·dt^p before extrapolation (otherwise part of the time error would be counted twice):\n")
    L.append("| quantity | p (time) | shifts applied to mesh levels | T without the shift | T with the shift | difference |\n|---|---|---|---|---|---|")
    for q in QS:
        o = overlap[q]
        L.append(f"| {q} | {o['time_error_model']['p']:.2f} | " + ", ".join(f"{x:+.2e}" for x in o["shift_applied"])
                 + f" | {o['truth_without_shift']:.5f} | {truth[q]['value']:.5f} | "
                 f"{(truth[q]['value'] - o['truth_without_shift']) / truth[q]['value']:+.3%} |")
    L.append("\n| quantity | baseline (stationary) | in-house reference T | uncertainty of T | literature band | T in band |\n|---|---|---|---|---|---|")
    for q in QS:
        tq = truth[q]
        L.append(f"| {q} | {tq['root_value']:.4f} | **{tq['value']:.4f}** | ±{tq['uncertainty_rel']:.2%} | "
                 f"{tq['literature_band'][0]}–{tq['literature_band'][1]} | {tq['in_band']} |")
    L.append("\n### Deterministic verification of the baseline\n")
    L.append(f"- Static verifier (baseline run only): **{static.verdict}**; missing components: {static.missing_components}.")
    L.append(f"- With the full study ({len(all_runs) - 1} extra runs): **{v.verdict}**.")
    for q, pq in v.per_qoi.items():
        cu = pq["combined_uncertainty"]
        L.append(f"  - {q}: {pq['verdict']}; components {pq['component_status']}; combined uncertainty "
                 + ("n/a" if cu is None else f"{cu:.2%}"))
    for c in v.checks:
        if c.component in ("mesh", "time", "domain"):
            L.append(f"  - {c.status.value} {c.check} [{c.qoi}]: {c.reason}")
    (REPO / "reports" / "baseline_generated.md").write_text("\n".join(L) + "\n")
    (REPO / "results" / "baseline" / "summary.json").write_text(json.dumps(
        {"root": root, "static_verdict": static.to_dict(), "study_verdict": v.to_dict()}, indent=1, default=str))
    print("\n".join(L))


if __name__ == "__main__":
    main()
