# ADR-0004: Volyra as geometry reference, torch evaluator in physis

**Status:** accepted (2026-10-27)

## Context
Volyra (`01_Projects/volyra`, C++20 SDF kernel with C ABI/WASM, MCP, web app) is the
geometry kernel. Solvers and data generation need SDF evaluation on GPU tensors, in
batches and with gradients, which a CPU C ABI cannot provide. Volyra's ownership in the
E-Lab project is not decided yet.

## Decision
physis has its own torch SDF evaluator, kept equal to Volyra by a parity test that builds
Volyra's C library out-of-tree (`build/volyra`) and compares fields on random points.
physis reads Volyra models (its primitive-list JSON); it never modifies the Volyra repo.

## Consequences
Two implementations of the same formulas, pinned by a differential test (the same pattern
Volyra uses for its TS mirror). Volyra stays the reference for geometry semantics.
