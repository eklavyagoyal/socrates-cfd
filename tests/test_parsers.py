"""Parsers tested against real OpenFOAM v2412 output (tests/fixtures)."""

from pathlib import Path

import numpy as np

from socrates.openfoam.parsers import parse_checkmesh, parse_dat, parse_solver_log

FX = Path(__file__).parent / "fixtures"


def test_checkmesh_real_log():
    cm = parse_checkmesh((FX / "checkMesh.log").read_text())
    assert cm["cells"] == 7616
    assert cm["mesh_ok"] is True
    assert cm["failed_checks"] == 0
    assert 0 < cm["max_non_orthogonality"] < 70
    assert 0 < cm["max_skewness"] < 4
    assert cm["bounding_box"][1][2] > cm["bounding_box"][0][2]  # one-cell span
    assert cm["geometric_directions"] == 2
    assert cm["completed"]


def test_checkmesh_failure_is_detected_from_text():
    # checkMesh exits 0 even on failure; the verdict must come from the log text
    txt = (FX / "checkMesh.log").read_text().replace("Mesh OK.", "Failed 1 mesh checks.")
    txt = txt.replace("Max skewness", "***Max skewness")
    cm = parse_checkmesh(txt)
    assert cm["mesh_ok"] is False
    assert cm["failed_checks"] == 1
    assert cm["error_lines"]


def test_solver_log_head_and_tail():
    log = parse_solver_log((FX / "pimpleFoam_head.log").read_text())
    assert log.application == "pimpleFoam"
    assert "2412" in log.build
    assert log.completed  # fixture keeps the final 'End'
    assert log.n_steps == len(log.courant_max) == len(log.cont_sum_local) == len(log.p_last_final)
    assert np.all(np.isfinite(log.courant_max))
    # last pressure solve of every step uses relTol 0 -> must reach 1e-7
    assert np.nanmax(log.p_last_final[1:]) <= 1.0001e-7
    assert log.fatal_errors == []


def test_solver_log_divergence_is_not_completed():
    log = parse_solver_log((FX / "pimpleFoam_diverged_tail.log").read_text())
    assert not log.completed
    assert np.nanmax(log.courant_max) > 1e50


def test_force_coefficients_parsed_by_header_name():
    cols, data = parse_dat(FX / "coefficient_head.dat")
    # v2412 column order is alphabetical: Cd, Cd(f), Cd(r), Cl, ... (not the v2112 order)
    assert cols[:5] == ["Time", "Cd", "Cd(f)", "Cd(r)", "Cl"]
    assert np.allclose(data["Cd(f)"] + data["Cd(r)"], data["Cd"], rtol=1e-6, atol=1e-9)
    assert np.all(np.diff(data["Time"]) > 0)


def test_solverinfo_mixed_types():
    cols, data = parse_dat(FX / "solverInfo_head.dat")
    assert "p_final" in cols and data["p_final"].dtype == float
    assert data["U_solver"].dtype == object


def test_dat_duplicate_times_keep_last(tmp_path):
    f = tmp_path / "x.dat"
    f.write_text("# Time a\n0.1 1\n0.2 2\n0.2 3\n0.3 4\n")
    _, d = parse_dat(f)
    assert list(d["Time"]) == [0.1, 0.2, 0.3]
    assert list(d["a"]) == [1, 3, 4]
