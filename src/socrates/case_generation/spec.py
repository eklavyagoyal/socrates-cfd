"""Problem specification and solver case configuration.

Two layers are deliberately kept apart:

* ``ProblemSpec`` -- the engineering question, solver independent.  This is
  what the user asks and what every run must carry with it unchanged.
* ``CaseConfig`` -- one concrete numerical realisation of the problem
  (mesh, domain, boundary conditions, schemes, time control) for OpenFOAM.
  Adversarial cases and experiment primitives are expressed as changes to
  this object only, so every change is diffable and recorded.

Lengths in ``MeshConfig``/``DomainConfig`` are in units of the cylinder
diameter D; times in ``TimeConfig`` are in convective units D/U.  The case
writer converts them to physical units using the *configured* physical
parameters (which may intentionally disagree with the spec in an
adversarial case).
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------
# Problem specification (solver independent)
# --------------------------------------------------------------------------


class Fluid(_Strict):
    name: str
    kinematic_viscosity: float = Field(gt=0, description="m^2/s")
    density: float = Field(gt=0, description="kg/m^3")


class ProblemInfo(_Strict):
    id: str
    type: Literal["cylinder_external_flow"]
    dimensionality: Literal["2D"]
    question: str
    fluid: Fluid
    flow_regime_assumption: str = "laminar, incompressible"


class Geometry(_Strict):
    cylinder_diameter: float = Field(gt=0, description="m")
    unbounded: bool = True


class OperatingConditions(_Strict):
    inlet_velocity: float = Field(gt=0, description="m/s, uniform free stream")
    reynolds_number: float = Field(gt=0)


class Verification(_Strict):
    # relative tolerance per requested quantity (e.g. 0.03 == 3 %)
    requested_tolerance: dict[str, float]
    reference_mode: Literal["blind", "reference_informed"] = "blind"


QOI_NAMES = ("mean_drag_coefficient", "strouhal_number", "rms_lift_coefficient")


class ProblemSpec(_Strict):
    problem: ProblemInfo
    geometry: Geometry
    operating_conditions: OperatingConditions
    requested_outputs: list[str]
    verification: Verification

    @field_validator("requested_outputs")
    @classmethod
    def _known_outputs(cls, v: list[str]) -> list[str]:
        unknown = [q for q in v if q not in QOI_NAMES]
        if unknown:
            raise ValueError(f"unknown requested outputs {unknown}; known: {QOI_NAMES}")
        return v

    def reynolds_from_parameters(self) -> float:
        return (
            self.operating_conditions.inlet_velocity
            * self.geometry.cylinder_diameter
            / self.problem.fluid.kinematic_viscosity
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ProblemSpec":
        return cls.model_validate(yaml.safe_load(Path(path).read_text()))


# --------------------------------------------------------------------------
# OpenFOAM case configuration
# --------------------------------------------------------------------------


class MeshConfig(_Strict):
    """Structured O-grid + H-grid topology (see blockmesh.py).

    Counts are for refinement == 1; every count is multiplied by
    ``refinement`` while all block expansion ratios are held fixed, which
    gives a geometrically similar (systematically refined) mesh family.
    """

    refinement: float = Field(1.0, gt=0)
    n_quadrant: int = Field(40, ge=2, description="cells per 90 deg of circumference")
    n_ring_inner: int = Field(30, ge=2, description="radial cells, cylinder -> r_mid")
    n_ring_outer: int = Field(20, ge=2, description="radial cells, r_mid -> square")
    n_upstream: int = Field(30, ge=2)
    n_downstream: int = Field(100, ge=2)
    n_lateral: int = Field(35, ge=2)
    first_cell: float = Field(0.005, gt=0, description="wall-normal size of first cell, in D")
    r_mid: float = Field(1.0, gt=0.5, description="outer radius of polar ring, in D")
    square_half: float = Field(2.5, description="half-size of near-field square, in D")
    span: float = Field(1.0, gt=0, description="extrusion thickness, in D")
    # Optional extra multiplier applied only to downstream x-counts (wake
    # resolution study / adversarial under-resolved wake).
    wake_factor: float = Field(1.0, gt=0)


class DomainConfig(_Strict):
    upstream: float = Field(20.0, description="inlet distance from cylinder centre, in D")
    downstream: float = Field(40.0, description="outlet distance from cylinder centre, in D")
    half_height: float = Field(20.0, description="lateral boundary distance from centre, in D")


class PhysicalConfig(_Strict):
    """Physical parameters as *configured in the case* (may differ from spec)."""

    diameter: float
    inlet_velocity: float
    kinematic_viscosity: float
    density: float


class BoundaryConfig(_Strict):
    lateral: Literal["symmetryPlane", "slip", "noSlipWall", "zeroGradientPatch"] = "symmetryPlane"
    outlet_velocity: Literal["inletOutlet", "zeroGradient"] = "inletOutlet"
    outlet_pressure: Literal["fixedValue", "zeroGradient"] = "fixedValue"
    inlet_pressure: Literal["zeroGradient", "fixedValue"] = "zeroGradient"
    cylinder_velocity: Literal["noSlip", "slip"] = "noSlip"


class NumericsConfig(_Strict):
    solver: Literal["pimpleFoam", "simpleFoam"] = "pimpleFoam"
    ddt: str = "backward"
    div_U: str = "Gauss linearUpwind grad(U)"
    grad: str = "Gauss linear"
    laplacian: str = "Gauss linear corrected"
    n_outer_correctors: int = 1
    n_correctors: int = 2
    n_nonorth_correctors: int = 1
    # steady (simpleFoam) controls
    steady_iterations: int = 4000
    steady_residual_target: float = 1e-5
    relax_U: float = 0.7
    relax_p: float = 0.3


class TimeConfig(_Strict):
    delta_t: float = Field(0.005, gt=0, description="time step, in D/U")
    end_time: float = Field(200.0, gt=0, description="in D/U")
    adjust_time_step: bool = False
    max_co: float = 0.5
    write_interval: float = Field(50.0, gt=0, description="field output interval, in D/U")


class ForceConfig(_Strict):
    """Reference quantities for force coefficients.

    ``None`` means "derive consistently from the case" (the correct
    behaviour).  Explicit values allow modelling a user error.
    """

    mag_u_inf: float | None = None
    l_ref: float | None = None
    a_ref: float | None = None
    rho_inf: float | None = None


class AveragingConfig(_Strict):
    """Averaging window declared by the case author (in D/U)."""

    start_time: float = Field(100.0, ge=0)


class PerturbationConfig(_Strict):
    """Asymmetric initial velocity patch that triggers shedding early.

    Applied identically to every unsteady case; excluded from statistics by
    the transient-detection logic.  Box is in units of D relative to the
    cylinder centre; velocity is a fraction of the inlet velocity.
    """

    enabled: bool = True
    box_min: tuple[float, float] = (0.5, 0.0)
    box_max: tuple[float, float] = (3.0, 1.0)
    v_fraction: float = 0.3


class CaseConfig(_Strict):
    name: str
    description: str = ""
    mesh: MeshConfig = MeshConfig()
    domain: DomainConfig = DomainConfig()
    physical: PhysicalConfig
    boundaries: BoundaryConfig = BoundaryConfig()
    numerics: NumericsConfig = NumericsConfig()
    time: TimeConfig = TimeConfig()
    forces: ForceConfig = ForceConfig()
    averaging: AveragingConfig = AveragingConfig()
    perturbation: PerturbationConfig = PerturbationConfig()

    # ---- derived helpers -------------------------------------------------
    @property
    def convective_time(self) -> float:
        return self.physical.diameter / self.physical.inlet_velocity

    def configured_reynolds(self) -> float:
        p = self.physical
        return p.inlet_velocity * p.diameter / p.kinematic_viscosity

    def resolved_force_reference(self) -> dict[str, float]:
        p, f = self.physical, self.forces
        return {
            "magUInf": f.mag_u_inf if f.mag_u_inf is not None else p.inlet_velocity,
            "lRef": f.l_ref if f.l_ref is not None else p.diameter,
            "Aref": f.a_ref if f.a_ref is not None else p.diameter * self.mesh.span * p.diameter,
            "rhoInf": f.rho_inf if f.rho_inf is not None else p.density,
        }

    def content_hash(self) -> str:
        """Hash of everything that affects the numerical result (not name/description)."""
        d = self.model_dump(mode="json")
        d.pop("name", None)
        d.pop("description", None)
        blob = json.dumps(d, sort_keys=True).encode()
        return hashlib.sha256(blob).hexdigest()[:16]

    def with_changes(self, changes: dict[str, Any], name: str | None = None) -> "CaseConfig":
        """Return a copy with dotted-path changes applied, e.g. {"mesh.refinement": 1.5}."""
        d = self.model_dump(mode="json")
        for path, value in changes.items():
            node = d
            keys = path.split(".")
            for k in keys[:-1]:
                if k not in node:
                    raise KeyError(f"unknown config path {path!r}")
                node = node[k]
            if keys[-1] not in node:
                raise KeyError(f"unknown config path {path!r}")
            node[keys[-1]] = copy.deepcopy(value)
        if name is not None:
            d["name"] = name
        return CaseConfig.model_validate(d)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "CaseConfig":
        return cls.model_validate(yaml.safe_load(Path(path).read_text()))


def diff_configs(parent: CaseConfig, child: CaseConfig) -> dict[str, dict[str, Any]]:
    """Flat dotted-path diff of two configs: {path: {"from": a, "to": b}}."""

    def flatten(d: Any, prefix: str = "") -> dict[str, Any]:
        out: dict[str, Any] = {}
        if isinstance(d, dict):
            for k, v in d.items():
                out.update(flatten(v, f"{prefix}{k}."))
        else:
            out[prefix[:-1]] = d
        return out

    a = flatten(parent.model_dump(mode="json"))
    b = flatten(child.model_dump(mode="json"))
    skip = {"name", "description"}
    return {
        k: {"from": a.get(k), "to": b.get(k)}
        for k in sorted(set(a) | set(b))
        if k not in skip and a.get(k) != b.get(k)
    }
