"""Validated experiment primitives.

The adaptive critic (LLM or rule-based) can only *name* one of these actions
with parameters.  Each primitive is deterministic code that derives a child
CaseConfig from its parent, validates it against hard limits and the
remaining budget, and records exactly what changed.  No primitive edits
OpenFOAM files directly; the case writer regenerates the whole case from the
child config.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from ..case_generation.blockmesh import expanded_domain_counts, resolve_layout
from ..case_generation.spec import CaseConfig, diff_configs
from ..orchestration.store import Initialisation

# parameter name -> (min, max, default)
ACTION_SPECS: dict[str, dict[str, tuple[float, float, float]]] = {
    "REFINE_MESH": {"factor": (1.3, 2.0, math.sqrt(2.0))},
    "REDUCE_TIME_STEP": {"factor": (1.5, 4.0, 2.0)},
    "EXPAND_DOMAIN": {"factor": (1.5, 3.0, 2.0)},
    "RUN_LONGER": {"additional_convective_times": (25.0, 300.0, 100.0)},
}

ACTION_DESCRIPTIONS = {
    "REFINE_MESH": "Multiply every mesh cell count by `factor` (all block expansion ratios fixed: a geometrically similar, "
                   "systematically refined mesh). Time step is kept unless the predicted max Courant number would exceed "
                   "the PISO limit, in which case it is reduced and the change is recorded. Estimates spatial discretisation error.",
    "REDUCE_TIME_STEP": "Divide the time step by `factor` on the identical mesh. Estimates temporal discretisation error.",
    "EXPAND_DOMAIN": "Multiply the inlet, outlet and lateral boundary distances by `factor`; the near-field mesh is unchanged "
                     "(cells are added only further out). Estimates truncation/blockage error of the artificial boundaries.",
    "RUN_LONGER": "Continue the same simulation for `additional_convective_times` D/U. Gives more shedding cycles: checks "
                  "whether the transient had ended and reduces statistical uncertainty.",
}


class ActionRejected(ValueError):
    """The requested action is invalid or violates limits/budget."""


@dataclass
class Limits:
    max_mesh_refinement_vs_root: float = 2.0  # cumulative factor on cell counts per direction
    max_cells: int = 160_000
    min_dt_fraction_of_root: float = 1.0 / 8.0
    max_domain_factor_vs_root: float = 4.0
    max_end_time: float = 600.0
    co_limit: float = 1.0
    co_target: float = 0.9
    # D/U for children initialised from a mapped periodic state: an already
    # periodic start adjusts faster than a fresh start; MSER may still discard
    # up to half, leaving >= 6 cycles
    mapped_run_length: float = 80.0
    mapped_averaging_start: float = 40.0


@dataclass
class PlannedExperiment:
    action: str
    params: dict[str, float]
    parent_run: str
    child_config: CaseConfig
    init: Initialisation
    changes: dict[str, Any]
    notes: list[str] = field(default_factory=list)
    estimated_cell_steps: float = 0.0

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "params": self.params,
            "parent_run": self.parent_run,
            "changes": self.changes,
            "notes": self.notes,
            "initialisation": {"kind": self.init.kind, "source_run": self.init.source_run},
            "estimated_cell_steps": self.estimated_cell_steps,
        }


def normalise_params(action: str, params: dict | None) -> dict[str, float]:
    if action not in ACTION_SPECS:
        raise ActionRejected(f"unknown action {action!r}; allowed: {sorted(ACTION_SPECS)}")
    spec = ACTION_SPECS[action]
    params = dict(params or {})
    extra = set(params) - set(spec)
    if extra:
        raise ActionRejected(f"{action}: unknown parameter(s) {sorted(extra)}; allowed {sorted(spec)}")
    out = {}
    for name, (lo, hi, default) in spec.items():
        v = params.get(name, default)
        try:
            v = float(v)
        except (TypeError, ValueError) as exc:
            raise ActionRejected(f"{action}.{name} must be a number, got {v!r}") from exc
        if not (lo <= v <= hi) or not math.isfinite(v):
            raise ActionRejected(f"{action}.{name}={v} outside allowed range [{lo}, {hi}]")
        # canonicalise so that numerically equivalent requests map to one run
        # (e.g. 1.4142 and sqrt(2)): snap to the default within 0.1 %, else 3 decimals
        v = default if abs(v - default) <= 1e-3 * default else round(v, 3)
        out[name] = v
    return out


def _periodic(ev: dict) -> bool:
    sw = ((ev.get("forces") or {}).get("stationary_window") or {})
    return bool((ev.get("temporal_behavior") or {}).get("oscillating")) and "n_cycles" in sw


def _cell_steps(cfg: CaseConfig, duration: float) -> float:
    if cfg.numerics.solver == "simpleFoam":
        return resolve_layout(cfg).n_cells * cfg.numerics.steady_iterations
    return resolve_layout(cfg).n_cells * duration / cfg.time.delta_t


def plan_experiment(
    action: str,
    params: dict | None,
    *,
    parent_run: str,
    parent_cfg: CaseConfig,
    parent_ev: dict,
    root_cfg: CaseConfig,
    limits: Limits | None = None,
) -> PlannedExperiment:
    """Validate an action and derive the child configuration (no execution)."""
    lim = limits or Limits()
    p = normalise_params(action, params)
    notes: list[str] = []
    if (parent_ev.get("solver") or {}).get("log_found") is False:
        raise ActionRejected(f"parent run {parent_run} has no solver output")
    periodic = _periodic(parent_ev)
    steady_parent = parent_cfg.numerics.solver == "simpleFoam"
    changes: dict[str, Any] = {}
    init = Initialisation("fresh")
    name_suffix = ""

    if action == "RUN_LONGER":
        if steady_parent:
            raise ActionRejected("RUN_LONGER is meaningless for a steady (simpleFoam) run")
        if not (parent_ev.get("solver") or {}).get("completed"):
            raise ActionRejected("cannot continue a run that did not complete")
        new_end = parent_cfg.time.end_time + p["additional_convective_times"]
        if new_end > lim.max_end_time:
            raise ActionRejected(f"end time {new_end} exceeds limit {lim.max_end_time}")
        changes["time.end_time"] = new_end
        init = Initialisation("restart", parent_run)
        duration = p["additional_convective_times"]
        name_suffix = f"long{int(new_end)}"
    else:
        if action == "REFINE_MESH":
            new_ref = parent_cfg.mesh.refinement * p["factor"]
            if new_ref / root_cfg.mesh.refinement > lim.max_mesh_refinement_vs_root * 1.0001:
                raise ActionRejected(
                    f"cumulative refinement {new_ref / root_cfg.mesh.refinement:.2f} exceeds limit {lim.max_mesh_refinement_vs_root}")
            changes["mesh.refinement"] = new_ref
            co = (parent_ev.get("solver") or {}).get("courant_max")
            if not steady_parent and co is not None:
                co_pred = co * p["factor"]
                if co <= lim.co_limit and co_pred > lim.co_target:
                    new_dt = parent_cfg.time.delta_t * lim.co_target / co_pred
                    changes["time.delta_t"] = new_dt
                    notes.append(f"time step reduced {parent_cfg.time.delta_t:g} -> {new_dt:.4g} D/U to keep predicted "
                                 f"max Co ({co_pred:.2f}) <= {lim.co_target} (parent Co {co:.2f})")
                elif co > lim.co_limit:
                    notes.append(f"parent max Co {co:.2f} already exceeds {lim.co_limit}; time step kept so that only the mesh changes")
            name_suffix = f"m{new_ref:.3g}"
        elif action == "REDUCE_TIME_STEP":
            if steady_parent:
                raise ActionRejected("REDUCE_TIME_STEP is meaningless for a steady (simpleFoam) run")
            new_dt = parent_cfg.time.delta_t / p["factor"]
            if new_dt < root_cfg.time.delta_t * lim.min_dt_fraction_of_root * 0.9999:
                raise ActionRejected(f"time step {new_dt:g} below limit {root_cfg.time.delta_t * lim.min_dt_fraction_of_root:g}")
            changes["time.delta_t"] = new_dt
            if parent_cfg.time.adjust_time_step:
                changes["time.max_co"] = parent_cfg.time.max_co / p["factor"]
            name_suffix = f"dt{new_dt:.3g}"
        elif action == "EXPAND_DOMAIN":
            f = p["factor"]
            d = parent_cfg.domain
            new = (d.upstream * f, d.downstream * f, d.half_height * f)
            if new[2] / root_cfg.domain.half_height > lim.max_domain_factor_vs_root * 1.0001:
                raise ActionRejected(f"cumulative domain factor exceeds limit {lim.max_domain_factor_vs_root}")
            changes.update({"domain.upstream": new[0], "domain.downstream": new[1], "domain.half_height": new[2]})
            changes.update(expanded_domain_counts(parent_cfg, *new))
            name_suffix = f"D{f:g}x"
        # initialisation: map from a periodic parent, otherwise a fresh perturbed start
        if periodic and not steady_parent:
            init = Initialisation("map", parent_run, consistent=(action != "EXPAND_DOMAIN"))
            changes["time.end_time"] = lim.mapped_run_length
            changes["averaging.start_time"] = lim.mapped_averaging_start
            duration = lim.mapped_run_length
            notes.append(f"initialised by mapping the parent's final periodic state; run {lim.mapped_run_length:g} D/U")
        else:
            duration = parent_cfg.time.end_time
            notes.append("parent has no periodic stationary state: fresh perturbed start with the parent's run length "
                         "(mapping a non-shedding field could suppress shedding the child would develop)")

    child_name = f"{root_cfg.name}.{name_suffix}"
    child = parent_cfg.with_changes(changes, name=child_name)
    child = child.model_copy(update={"description": f"{action} {p} from {parent_run}"})
    n_cells = resolve_layout(child).n_cells
    if n_cells > lim.max_cells:
        raise ActionRejected(f"child mesh has {n_cells} cells > limit {lim.max_cells}")
    return PlannedExperiment(
        action=action,
        params=p,
        parent_run=parent_run,
        child_config=child,
        init=init,
        changes=diff_configs(parent_cfg, child),
        notes=notes,
        estimated_cell_steps=_cell_steps(child, duration),
    )
