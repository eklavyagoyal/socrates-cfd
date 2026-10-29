"""Lattice Boltzmann flow: D3Q19 TRT on SDF grids, torch reference and a fused Metal kernel."""

from physis.solvers.lbm.periodic import PeriodicFlow, PeriodicFlowSpec

__all__ = ["PeriodicFlow", "PeriodicFlowSpec"]
