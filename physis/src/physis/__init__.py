"""physis: self-built engineering physics platform.

Layers (see docs/architecture.md):
    geometry      SDF geometry (torch evaluator, Volyra parity) and voxelization
    solvers       lbm (flow), thermal (heat), fem (structure) on SDF-derived Cartesian grids
    verification  convergence/GCI, evidence extraction, validation gates
    data          design spaces, batch simulation, verified datasets
    surrogates    physics-AI models trained on verified data
    optimize      design optimization (direct, surrogate-assisted, gradient)
    platform      CLI, REST API, MCP server
"""

__version__ = "0.1.0"
