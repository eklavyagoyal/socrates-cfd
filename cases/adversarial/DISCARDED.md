# Discarded adversarial candidates

Candidates that did not produce a *plausible, successfully executed* run are
recorded here (they remain in the run store for provenance) and are excluded
from the benchmark, as required by the project brief.

| id | change vs baseline | outcome | run |
|---|---|---|---|
| C1 (v0) | `time.delta_t: 0.1` (Co_max ~7.5), `numerics.n_outer_correctors: 3`, backward | Diverged at t ~ 5 D/U (Courant number 3.9e103, floating-point exception in GAMG). Obvious crash -> not a plausible-but-wrong case. | `C1_large_timestep-2c56fe2482da` |
