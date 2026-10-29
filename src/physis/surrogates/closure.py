"""Learned pore-scale closure: structure descriptors (or a voxel field) -> permeability.

This is the first half of the bridge in ADR-0008/ADR-0009: trained on verified LBM RVE runs,
it later supplies Darcy coefficients to the wall model and to OpenFOAM porous zones. Two
models and one baseline, all predicting ``log10(K)`` (K in box-length units):

- Kozeny–Carman with its constant fitted on the training split only (the baseline);
- an ensemble of small MLPs on descriptors (porosity, log specific surface, family) whose
  spread is the uncertainty estimate;
- optionally a small 3D CNN on the block-averaged solid fraction field.

Evaluation reports a random split and an extrapolation split (a porosity band held out
entirely), because the model is only trustworthy inside the range it was trained on.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from torch import nn

FAMILIES = ("spheres", "voids", "gyroid")


def features(rows: list[dict[str, Any]]) -> np.ndarray:
    x = []
    for r in rows:
        onehot = [1.0 if r["family"] == f else 0.0 for f in FAMILIES]
        x.append([r["porosity"], math.log10(r["specific_surface"]), *onehot])
    return np.asarray(x, dtype=np.float64)


def target(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.log10(np.asarray([r["permeability"] for r in rows], dtype=np.float64))


def metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    ss_res = float(((y - p) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum()) or float("nan")
    return {"r2": 1.0 - ss_res / ss_tot, "mae_log10": float(np.abs(y - p).mean()),
            "max_abs_log10": float(np.abs(y - p).max()), "n": int(len(y))}


@dataclass
class KozenyCarman:
    log10_c: float = math.log10(5.0)

    def fit(self, rows: list[dict[str, Any]]) -> KozenyCarman:
        base = np.log10([r["porosity"] ** 3 / r["specific_surface"] ** 2 for r in rows])
        self.log10_c = float(np.mean(base - target(rows)))
        return self

    def predict(self, rows: list[dict[str, Any]]) -> np.ndarray:
        return np.log10([r["porosity"] ** 3 / r["specific_surface"] ** 2 for r in rows]) - self.log10_c


class _MLP(nn.Module):
    def __init__(self, d_in: int, width: int = 64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, width), nn.SiLU(), nn.Linear(width, width), nn.SiLU(),
                                 nn.Linear(width, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


class MLPEnsemble:
    def __init__(self, members: int = 5, epochs: int = 3000, lr: float = 3e-3, seed: int = 0, device: str = "cpu"):
        self.members, self.epochs, self.lr, self.seed, self.device = members, epochs, lr, seed, device
        self.models: list[_MLP] = []

    def fit(self, x: np.ndarray, y: np.ndarray, x_val: np.ndarray | None = None, y_val: np.ndarray | None = None):
        self.mu, self.sd = x.mean(0), x.std(0) + 1e-9
        self.ymu, self.ysd = y.mean(), y.std() + 1e-9
        xt = torch.tensor((x - self.mu) / self.sd, dtype=torch.float32, device=self.device)
        yt = torch.tensor((y - self.ymu) / self.ysd, dtype=torch.float32, device=self.device)
        self.models = []
        for m in range(self.members):
            torch.manual_seed(self.seed + m)
            model = _MLP(x.shape[1]).to(self.device)
            opt = torch.optim.Adam(model.parameters(), lr=self.lr, weight_decay=1e-5)
            idx = torch.randint(0, len(xt), (len(xt),), device=self.device)  # bootstrap per member
            for _ in range(self.epochs):
                opt.zero_grad()
                loss = ((model(xt[idx]) - yt[idx]) ** 2).mean()
                loss.backward()
                opt.step()
            self.models.append(model.eval())
        return self

    @torch.no_grad()
    def predict(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        xt = torch.tensor((x - self.mu) / self.sd, dtype=torch.float32, device=self.device)
        preds = torch.stack([m(xt) for m in self.models]).cpu().numpy() * self.ysd + self.ymu
        return preds.mean(0), preds.std(0)


class _CNN(nn.Module):
    def __init__(self):
        super().__init__()

        def block(i, o):
            return nn.Sequential(nn.Conv3d(i, o, 3, padding=1, padding_mode="circular"), nn.BatchNorm3d(o), nn.SiLU())

        self.body = nn.Sequential(block(1, 16), nn.MaxPool3d(2), block(16, 32), nn.MaxPool3d(2), block(32, 64),
                                  nn.MaxPool3d(2), block(64, 64), nn.AdaptiveAvgPool3d(1))
        self.head = nn.Linear(64, 1)

    def forward(self, v):
        return self.head(self.body(v).flatten(1)).squeeze(-1)


def train_cnn(volumes: np.ndarray, y: np.ndarray, *, epochs: int = 150, device: str = "cpu",
              seed: int = 0) -> tuple[_CNN, float, float]:
    """Train on (N, D, D, D) solid-fraction volumes; returns model and target scaling."""
    torch.manual_seed(seed)
    ymu, ysd = float(y.mean()), float(y.std() + 1e-9)
    v = torch.tensor(volumes[:, None], dtype=torch.float32, device=device)
    t = torch.tensor((y - ymu) / ysd, dtype=torch.float32, device=device)
    model = _CNN().to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(v), device=device)
        for i in range(0, len(v), 32):
            b = perm[i:i + 32]
            # periodic RVEs: random flips/permutations along y,z keep the x-permeability
            vb = v[b]
            if torch.rand(()) < 0.5:
                vb = vb.flip(3)
            if torch.rand(()) < 0.5:
                vb = vb.flip(4)
            opt.zero_grad()
            loss = ((model(vb) - t[b]) ** 2).mean()
            loss.backward()
            opt.step()
        sched.step()
    return model.eval(), ymu, ysd


@torch.no_grad()
def predict_cnn(model: _CNN, volumes: np.ndarray, ymu: float, ysd: float, device: str = "cpu") -> np.ndarray:
    v = torch.tensor(volumes[:, None], dtype=torch.float32, device=device)
    out = torch.cat([model(v[i:i + 64]) for i in range(0, len(v), 64)])
    return out.cpu().numpy() * ysd + ymu
