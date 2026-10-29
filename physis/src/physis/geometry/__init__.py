"""Geometry: SDF nodes (torch), voxelization bridge to solver grids."""

from physis.geometry.sdf import SDF, Ball, Box, Difference, Intersection, Translate, Union, from_spec
from physis.geometry.porous import Gyroid, PeriodicSpheres, spheres_for_porosity
from physis.geometry.voxelize import link_fractions, sample, solid_mask

__all__ = [
    "SDF",
    "Ball",
    "Box",
    "Difference",
    "Gyroid",
    "Intersection",
    "PeriodicSpheres",
    "Translate",
    "Union",
    "from_spec",
    "link_fractions",
    "sample",
    "solid_mask",
    "spheres_for_porosity",
]
