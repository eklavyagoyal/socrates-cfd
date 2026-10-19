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
from socrates.checks.static import statistical_uncertainty  # noqa: E402
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


def fmt(x, spec=".4f"):
    return "—" if x is None else format(x, spec)


def sta(store, rid):
    return (store.load(rid).evidence.get("qoi") or {}).get("stationary") or {}


def sta_c(store, rid, cont):
    """Stationary values of the longest continuation of a study member."""
    return sta(store, cont.get(rid, rid))


def main() -> None:
    spec = ProblemSpec.from_yaml(REPO / "configs" / "problem_cylinder_re100.yaml")
    store = RunStore(REPO / "results" / "runs")
    study = json.loads((REPO / "results" / "baseline" / "study.json").read_text())
    root = study["root"]
    ch = {k: [root] + [e["run_id"] for e in v] for k, v in study["chains"].items()}
    stage2 = study.get("stage2") or {}
    if stage2.get("time_level_4"):
        ch["time"].append(stage2["time_level_4"]["run_id"])
    # every member's value is taken from its longest continuation (as the verifier does for statistics)
    cont = dict(stage2.get("continuations") or {})
    if len(ch.get("longer", [])) > 1:
        cont[root] = ch["longer"][-1]
    rb = store.load(root)
    ev = rb.evidence

    def val_run(rid):
        return cont.get(rid, rid)

    def size(factor, rid):
        r = store.load(rid)
        if factor == "mesh":
            return r.evidence["mesh"]["representative_cell_size_D"]
        if factor == "time":
            return r.config.time.delta_t
        return 1.0 / r.config.domain.half_height

    truth, chains_out, overlap, skipped = {}, {}, {}, {}
    dt_root = rb.config.time.delta_t
    tau = spec.verification.requested_tolerance

    def u_stat_abs(rid, q):
        r = val_run(rid)
        u, _ = statistical_uncertainty(store.load(r).evidence or {}, q)
        v = sta(store, r).get(q)
        return (u or 0.0) * abs(v or 0.0)

    for q in QS:
        per = {}
        missing = [r for f in ("time", "mesh", "domain") for r in ch[f] if sta_c(store, r, cont).get(q) is None]
        if missing:
            skipped[q] = f"stationary value missing in {missing}"
            print(f"{q}: no reference computed ({skipped[q]})", flush=True)
            continue
        for factor, order in (("time", 2.0), ("mesh", 2.0), ("domain", 1.0)):
            rids = ch[factor][-3:]  # the finest three levels (the time chain has four after stage 2)
            vals = [sta_c(store, r, cont).get(q) for r in rids]
            if factor == "mesh":
                # The mesh chain also lowers dt (Courant control), so its raw values contain part of the
                # time error that the time chain already corrects for (double counting).  Shift every mesh
                # level to the baseline dt with the time chain's own error model e(dt) = C dt^p.
                tc = per["time"]
                p_t = tc.get("order_used") or 2.0  # the order the time extrapolation actually used
                c_t = (sta_c(store, root, cont)[q] - tc["extrapolated"]) / dt_root ** p_t
                dts = [store.load(r).config.time.delta_t for r in rids]
                shift = [c_t * (dt ** p_t - dt_root ** p_t) for dt in dts]
                raw = extrapolate_chain(vals, [size(factor, r) for r in rids], order)
                vals = [v - sh for v, sh in zip(vals, shift)]
                overlap[q] = {"mesh_level_dt": dts, "time_error_model": {"C": c_t, "p": p_t},
                              "shift_applied": shift, "mesh_extrapolated_without_shift": raw["extrapolated"]}
            per[factor] = extrapolate_chain(vals, [size(factor, r) for r in rids], order)
            per[factor]["runs"] = rids
        root_v = sta_c(store, root, cont)[q]
        # statistical uncertainty of the members, carried through the extrapolation weights (the root's once)
        stat = {"root": u_stat_abs(root, q)}
        for factor, c in per.items():
            fin, mid = c["runs"][-1], c["runs"][-2]
            stat[factor] = ((c["weights"]["finest"] * u_stat_abs(fin, q)) ** 2
                            + (c["weights"]["middle"] * u_stat_abs(mid, q)) ** 2) ** 0.5
        truth[q] = combine_truth(root_v, per, statistical=stat)
        truth[q]["root_value"] = root_v
        if q in overlap:
            no_shift = dict(per, mesh=dict(per["mesh"], extrapolated=overlap[q]["mesh_extrapolated_without_shift"]))
            overlap[q]["truth_without_shift"] = combine_truth(root_v, no_shift, statistical=stat)["value"]
            truth[q]["time_overlap_correction"] = overlap[q]
        chains_out[q] = per
        lo, hi = LIT[q]["band"]
        truth[q]["literature_band"] = [lo, hi]
        truth[q]["in_band"] = lo <= truth[q]["value"] <= hi
        t = tau.get(q)
        if t is not None:  # pre-registered criterion 2 (design.md section 19): band widened by tau
            truth[q]["literature_band_widened_by_tau"] = [lo * (1 - t), hi * (1 + t)]
            truth[q]["in_widened_band"] = lo * (1 - t) <= truth[q]["value"] <= hi * (1 + t)
    (REPO / "results" / "baseline" / "truth.json").write_text(
        json.dumps({"truth": truth, "chains": chains_out, "root": root, "skipped": skipped}, indent=1, default=float))

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
    L.append("Criterion 2 (pre-registered, design.md §19) uses the band widened by τ; the narrow band is shown for information.\n")
    L.append("| quantity | reported (declared window) | stationary | literature band | in band | band widened by τ | **in widened band** |\n|---|---|---|---|---|---|---|")
    rep = ev["qoi"]["reported"]
    st = ev["qoi"]["stationary"]
    for q in QS:
        lo, hi = LIT[q]["band"]
        t = tau.get(q)
        x = st.get(q)
        wide = f"{lo * (1 - t):.4f}–{hi * (1 + t):.4f}" if t is not None else "— (not a requested quantity)"
        inw = (lo * (1 - t) <= x <= hi * (1 + t)) if (t is not None and x is not None) else "—"
        L.append(f"| {q} | {fmt(rep.get(q))} | {fmt(x)} | {lo}–{hi} | {(lo <= x <= hi) if x is not None else '—'} | "
                 f"{wide} | {inw} |")
    L.append("\n### One-factor-at-a-time verification study\n")
    L.append("Values used for the reference are those of each member's longest continuation (rows marked ↳). "
             "The time chain is extrapolated from its finest three levels.\n")
    L.append("| factor | run | size | run length (D/U) | Cd | St | Cl rms |\n|---|---|---|---|---|---|---|")
    for factor in ("mesh", "time", "domain"):
        for rid in ch[factor]:
            for i, r in enumerate([rid] + ([cont[rid]] if rid in cont else [])):
                x = sta(store, r)
                L.append(f"| {factor} | {'↳ ' if i else ''}`{r}` | {size(factor, rid):.4g} | "
                         f"{store.load(r).config.time.end_time:g} | {fmt(x.get('mean_drag_coefficient'))} | "
                         f"{fmt(x.get('strouhal_number'))} | {fmt(x.get('rms_lift_coefficient'))} |")

    L.append("\n**Statistical reliability of every study member** (same measures as the verifier's statistics check; "
             "the truth uncertainty carries these through the extrapolation weights):\n")
    L.append("| run | stationary cycles | MSER at cap | u_stat Cd | u_stat St | Cd drift in window |\n|---|---|---|---|---|---|")
    seen = []
    for factor in ("mesh", "time", "domain", "longer"):
        for rid in ch[factor] + [cont[r] for r in ch[factor] if r in cont]:
            if rid in seen:
                continue
            seen.append(rid)
            e = store.load(rid).evidence or {}
            sw_ = (e.get("forces") or {}).get("stationary_window") or {}
            ucd, _ = statistical_uncertainty(e, "mean_drag_coefficient")
            ust, _ = statistical_uncertainty(e, "strouhal_number")
            L.append(f"| `{rid}` | {sw_.get('n_cycles')} | {(e.get('temporal_behavior') or {}).get('mser_hit_cap')} | "
                     f"{fmt(ucd, '.2e')} | {fmt(ust, '.2e')} | {fmt(sw_.get('mean_cd_relative_drift'), '+.2e')} |")
    L.append("\n### Richardson extrapolation per factor and combined in-house reference\n")
    L.append("| quantity | factor | method | extrapolated | correction vs baseline |\n|---|---|---|---|---|")
    QT = [q for q in QS if q in truth]
    for q, why in skipped.items():
        L.append(f"| {q} | — | not computed: {why} | — | — |")
    for q in QT:
        for factor, c in chains_out[q].items():
            L.append(f"| {q} | {factor} | {c['method']} | {c['extrapolated']:.5f} | {truth[q]['corrections'][factor]:+.5f} |")
    L.append("\nMesh levels were run with dt = " + ", ".join(f"{d:.5g}" for d in overlap[QT[0]]["mesh_level_dt"])
             + " (Courant control), so each mesh level is shifted to the baseline dt with the time chain's error model "
               "C·dt^p before extrapolation (otherwise part of the time error would be counted twice):\n")
    L.append("| quantity | p (time) | shifts applied to mesh levels | T without the shift | T with the shift | difference |\n|---|---|---|---|---|---|")
    for q in QT:
        o = overlap[q]
        L.append(f"| {q} | {o['time_error_model']['p']:.2f} | " + ", ".join(f"{x:+.2e}" for x in o["shift_applied"])
                 + f" | {o['truth_without_shift']:.5f} | {truth[q]['value']:.5f} | "
                 f"{(truth[q]['value'] - o['truth_without_shift']) / truth[q]['value']:+.3%} |")
    L.append("\n| quantity | baseline (stationary) | in-house reference T | uncertainty of T (of which statistical) | "
             "literature band | T in band | T in band widened by τ |\n|---|---|---|---|---|---|---|")
    for q in QT:
        tq = truth[q]
        stat_rel = sum(u**2 for u in tq["statistical_terms"].values()) ** 0.5 / abs(tq["value"])
        L.append(f"| {q} | {tq['root_value']:.4f} | **{tq['value']:.4f}** | ±{tq['uncertainty_rel']:.2%} ({stat_rel:.2%}) | "
                 f"{tq['literature_band'][0]}–{tq['literature_band'][1]} | {tq['in_band']} | {tq.get('in_widened_band', '—')} |")
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
