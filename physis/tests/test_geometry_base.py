"""Base SDF nodes and the voxelization bridge."""

from __future__ import annotations

import math

import pytest
import torch

from physis.core.grid import Grid
from physis.geometry import Ball, Box, from_spec, link_fractions, sample, solid_mask


def test_ball_and_box_distances(cpu64):
    b = Ball((0.0, 0.0), 1.0)
    p = cpu64.tensor([[2.0, 0.0], [0.0, 0.5], [3.0, 4.0]])
    assert b(p).tolist() == pytest.approx([1.0, -0.5, 4.0])
    box = Box((0.0, 0.0, 0.0), (1.0, 2.0, 3.0))
    q = cpu64.tensor([[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [2.0, 3.0, 0.0]])
    assert box(q).tolist() == pytest.approx([1.0, -1.0, math.sqrt(2.0)])


def test_booleans_and_spec_roundtrip(cpu64):
    g = (Box((0.0, 0.0), (2.0, 1.0)) - Ball((0.0, 0.0), 0.5)) | Ball((3.0, 0.0), 0.25)
    g = g.translate((1.0, 0.0))
    g2 = from_spec(g.to_spec())
    p = torch.rand(200, 2, dtype=torch.float64) * 8 - 4
    assert torch.allclose(g(p), g2(p))
    assert g(cpu64.tensor([[1.0, 0.0]])).item() == pytest.approx(0.5)  # hole centre
    assert g(cpu64.tensor([[4.0, 0.0]])).item() == pytest.approx(-0.25)


def test_dimension_mismatch_raises(cpu64):
    with pytest.raises(ValueError):
        Ball((0.0, 0.0), 1.0)(cpu64.tensor([[0.0, 0.0, 0.0]]))
    with pytest.raises(ValueError):
        Ball((0.0, 0.0), 1.0) | Ball((0.0, 0.0, 0.0), 1.0)


def test_sample_and_mask(cpu64):
    grid = Grid((10, 10), 0.2, (-1.0, -1.0))
    d = sample(Ball((0.0, 0.0), 0.5), grid, cpu64)
    assert d.shape == (10, 10)
    m = solid_mask(Ball((0.0, 0.0), 0.5), grid, cpu64)
    centers = grid.centers(cpu64)
    expected = torch.linalg.vector_norm(centers, dim=-1) < 0.5
    assert torch.equal(m, expected)


def test_link_fractions_match_analytic_circle(cpu64):
    """Along a +x link from fluid node (x0, y0) the wall of a circle of radius R is at
    x_w = -sqrt(R^2 - y0^2) (left side); q = (x_w - x0) / h."""
    R, h = 0.37, 0.05
    grid = Grid((40, 40), h, (-1.0, -1.0))
    c = torch.tensor([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1]])
    circle = Ball((0.0, 0.0), R)
    q = link_fractions(circle, grid, c, cpu64)
    solid = solid_mask(circle, grid, cpu64)
    centers = grid.centers(cpu64)
    i_plus_x = 0
    ix, iy = torch.nonzero(~torch.isnan(q[i_plus_x]), as_tuple=True)
    assert ix.numel() > 0
    for a, b in zip(ix.tolist(), iy.tolist()):
        assert not solid[a, b] and solid[a + 1, b]
        x0, y0 = centers[a, b].tolist()
        xw = -math.sqrt(R * R - y0 * y0)
        assert q[i_plus_x, a, b].item() == pytest.approx((xw - x0) / h, abs=1e-10)
    # every q in (0, 1], and only on fluid nodes
    valid = q[~torch.isnan(q)]
    assert torch.all((valid > 0) & (valid <= 1))
    assert not torch.any(~torch.isnan(q[:, solid]))
