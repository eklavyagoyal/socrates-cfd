# ADR-0005: Content-addressed run store with provenance

**Status:** accepted (2026-10-27)

## Decision
Every stored run is keyed by sha256(kind, canonical spec, source fingerprint of the
solver's subpackage + core). Records carry git commit and dirty flag, environment,
backend, status (completed/failed with traceback) and result meta; arrays are compressed
npz (fields float32, series float64). The store lives outside git (`var/store` or
`$PHYSIS_STORE`). Failed runs are recorded, never dropped or hidden.

## Consequences
Identical requests are free; any solver change invalidates only that solver's runs;
results from uncommitted code remain traceable (Socrates had 15 roots it could not trace).
