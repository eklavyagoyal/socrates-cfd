# socrates-cfd — autonomous CFD verification (research prototype)

**Question this repository answers empirically:** can an adaptive system that
*requests additional simulations* detect meaningful CFD failures that ordinary
solver diagnostics and static (single-run) verification do not? And does an LLM
critic add anything over a deterministic planner?

The loop is:

> problem → OpenFOAM simulation → deterministic evidence → checks → critic →
> validated experiment → new simulation → new evidence → verdict

The LLM is **never a source of numerical truth**:
- it sees only recorded evidence;
- it can only pick one of four validated experiment primitives;
- ACCEPT/REJECT come from deterministic checks;
- every number in its text is audited against the evidence.

**Benchmark:** 2D laminar flow past a circular cylinder at Re = 100 (periodic
vortex shedding), asking for mean drag coefficient and Strouhal number to ±3 %.

**Results and verdict on the idea:** see [`reports/final_report.md`](reports/final_report.md).

## Repository map

| Path | Contents |
|---|---|
| `docs/research.md` | Phase 0 research: benchmark choice, verified reference data, V&V methods, OpenFOAM v2412 diagnostics (source-checked), related LLM/CFD systems |
| `docs/design.md` | Technical design (all 20 requested items), decision log, **pre-registered evaluation protocol**, risks, falsification test |
| `docs/methodology.md` | How evidence is extracted and judged; development log of corrections |
| `configs/problem_cylinder_re100.yaml` | The engineering question as a machine-readable spec |
| `configs/verification.yaml` | Every threshold with its provenance |
| `cases/baseline/baseline.yaml` | The credible baseline case |
| `cases/adversarial/`, `cases/variants/`, `cases/attacks/` | Flawed, borderline/credible, and attack cases, as diffs against the baseline; `DISCARDED.md` lists rejected candidates |
| `benchmark/manifest.yaml`, `benchmark/labels.json` | Pre-registered expectations and measured ground-truth labels |
| `src/socrates/case_generation/` | Parametric blockMesh/case writer with systematic refinement |
| `src/socrates/openfoam/` | Runner and parsers (the only OpenFOAM-specific code besides the writer) |
| `src/socrates/evidence/` | Evidence extraction (MSER transient removal, cycle statistics, two independent St estimates) |
| `src/socrates/checks/` | Deterministic checks, sensitivity (Richardson/GCI) analysis, verdict aggregation |
| `src/socrates/experiments/` | REFINE_MESH, REDUCE_TIME_STEP, EXPAND_DOMAIN, RUN_LONGER |
| `src/socrates/critic/` | LLM critic (tool-less, schema-constrained), rule-based planner, numeric audit |
| `src/socrates/orchestration/` | Content-addressed run store with provenance, adaptive loop, benchmark systems, truth/labels |
| `src/socrates/reporting/` | Per-case reports with evidence graphs |
| `results/runs/<run_id>/` | Every simulation: `run.json` (provenance), `evidence.json`, `series.npz`, `case/` (dictionaries; meshes/fields regenerable) |
| `results/benchmark/` | Per-system, per-case results and metrics |
| `reports/` | `baseline_validation.md`, `benchmark_results.md`, `final_report.md`, per-case reports, figures |

## Reproduce

### Option A — container (recommended)

```bash
docker build -t socrates-cfd -f docker/Dockerfile .
docker run --rm -v "$PWD/results:/work/results" socrates-cfd pytest -q
docker run --rm -v "$PWD/results:/work/results" socrates-cfd \
    python3 scripts/run_root_cases.py cases/adversarial/A1_coarse_mesh.yaml
```

Behind a TLS-intercepting proxy, add
`--secret id=extra_ca,src=<proxy-ca.crt> --build-arg https_proxy=...` to the build.
The CA is used at build time only and is not kept in the image.

### Option B — host (Ubuntu 24.04)

```bash
curl -fsSL https://dl.openfoam.com/add-debian-repo.sh -o add-repo.sh && sudo bash add-repo.sh
sudo apt-get install openfoam2412=2412.260127-1
pip install -r requirements.lock && pip install -e .
pytest -q                                              # software tests (not physics!)
socrates run-case cases/baseline/baseline.yaml         # one simulation + evidence
socrates verify <run_id>                               # static verification
python scripts/baseline_study.py                       # mesh/time/domain chains for the baseline
python scripts/make_baseline_report.py
python scripts/run_root_cases.py cases/adversarial/*.yaml
python scripts/run_benchmark.py --systems A,B,L-judge,C-rule,C-llm,Bexh
python scripts/analyze_benchmark.py
```

### Notes

- `C-llm` and `L-judge` need the `claude` CLI with credentials. All deterministic systems run without it.
- Runs are content-addressed: re-running a script reuses completed simulations.
  - `SOCRATES_CPU_SLOTS` limits concurrent OpenFOAM processes machine-wide.
  - Pinned versions: OpenFOAM v2412 (`openfoam2412=2412.260127-1`); Python packages in `requirements.lock`.

## Status and scope

This is a single-benchmark research prototype. It is deliberately **not** a
platform: no UI, no multi-solver support, no cloud infrastructure. See
`reports/final_report.md` for what works, what fails, and what should and should
not be built next.
