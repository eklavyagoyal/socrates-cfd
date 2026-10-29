"""GPU benchmark for lattice-Boltzmann-type workloads on Apple Silicon (Metal via PyTorch).

Measures what a machine really delivers for bandwidth-bound simulation kernels, so
hardware decisions rest on measurements instead of datasheet extrapolation:

1. copy bandwidth: a custom Metal copy kernel (the practical ceiling, "STREAM copy")
2. D3Q19 stream + collide proxy: one fused Metal kernel per time step (pull streaming on a
   periodic grid, BGK-like relaxation; 19 floats read + 19 written per cell = 152 B)
   at several grid sizes, reported as MLUPS (million lattice updates per second)
3. the same step written in plain PyTorch (torch.roll), to show the software headroom

Every kernel is checked against a plain-PyTorch reference before it is timed; a fast but
wrong kernel aborts the run. Results print as a table and are saved as JSON next to the
script (no hostname or user data, only chip, memory, OS and torch versions).

Run (needs only Python 3 and ~1 GB disk for torch):

    python3 -m venv ~/physis-bench
    ~/physis-bench/bin/pip install torch
    ~/physis-bench/bin/python bench_lbm_gpu.py

Close heavy apps first; on a laptop, plug in power. Takes about 1-3 minutes.
"""

from __future__ import annotations

import json
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

import torch

SHADERS = r"""
#include <metal_stdlib>
using namespace metal;

kernel void copy_f4(device const float4* a [[buffer(0)]],
                    device float4* b [[buffer(1)]],
                    uint i [[thread_position_in_grid]]) {
    b[i] = a[i];
}

// D3Q19 velocity set (same order as ref_step below)
constant int CX[19] = {0, 1,-1, 0, 0, 0, 0, 1,-1, 1,-1, 1,-1, 1,-1, 0, 0, 0, 0};
constant int CY[19] = {0, 0, 0, 1,-1, 0, 0, 1,-1,-1, 1, 0, 0, 0, 0, 1,-1, 1,-1};
constant int CZ[19] = {0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 1,-1,-1, 1, 1,-1,-1, 1};

// Layout: f[q][z][y][x], x fastest. Pull streaming on a periodic N^3 grid, then
// relaxation towards rho/19 (conserves mass exactly).
kernel void d3q19_step(device const float* fin [[buffer(0)]],
                       device float* fout [[buffer(1)]],
                       constant uint& N [[buffer(2)]],
                       uint idx [[thread_position_in_grid]]) {
    uint n3 = N * N * N;
    if (idx >= n3) return;
    int n = int(N);
    int x = int(idx % N), y = int((idx / N) % N), z = int(idx / (N * N));
    float f[19];
    float rho = 0.0f;
    for (int q = 0; q < 19; ++q) {
        int xs = (x - CX[q] + n) % n;
        int ys = (y - CY[q] + n) % n;
        int zs = (z - CZ[q] + n) % n;
        f[q] = fin[q * n3 + uint((zs * n + ys) * n + xs)];
        rho += f[q];
    }
    float feq = rho / 19.0f;
    for (int q = 0; q < 19; ++q) {
        fout[q * n3 + idx] = 0.9f * f[q] + 0.1f * feq;
    }
}
"""

C = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
     (1, 1, 0), (-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 0, 1), (-1, 0, -1), (1, 0, -1),
     (-1, 0, 1), (0, 1, 1), (0, -1, -1), (0, 1, -1), (0, -1, 1)]
BYTES_PER_CELL = 19 * 4 * 2  # read + write, float32


def sh(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return ""


def machine_info() -> dict:
    info = {
        "chip": sh(["sysctl", "-n", "machdep.cpu.brand_string"]).strip(),
        "memory_gb": round(int(sh(["sysctl", "-n", "hw.memsize"]).strip() or 0) / 2**30),
        "cpu_perf_cores": sh(["sysctl", "-n", "hw.perflevel0.physicalcpu"]).strip(),
        "cpu_eff_cores": sh(["sysctl", "-n", "hw.perflevel1.physicalcpu"]).strip(),
        "macos": platform.mac_ver()[0],
        "python": platform.python_version(),
        "torch": torch.__version__,
    }
    model, gpu_cores = "", ""
    for line in sh(["system_profiler", "SPHardwareDataType", "SPDisplaysDataType"]).splitlines():
        s = line.strip()
        if s.startswith("Model Name:") and not model:
            model = s.split(":", 1)[1].strip()
        if s.startswith("Total Number of Cores:"):
            gpu_cores = s.split(":", 1)[1].strip()  # last match is the GPU section
    info["model"], info["gpu_cores"] = model, gpu_cores
    return info


def sync() -> None:
    torch.mps.synchronize()


def timed(fn, min_seconds: float = 0.6, repeats: int = 5) -> tuple[float, float, int]:
    """Median and spread (max-min)/median of per-call time; calls per sample chosen to
    last >= min_seconds."""
    fn(); sync()
    t0 = time.perf_counter(); fn(); sync()
    one = max(time.perf_counter() - t0, 1e-6)
    calls = max(1, int(min_seconds / one))
    samples = []
    for _ in range(repeats):
        t = time.perf_counter()
        for _ in range(calls):
            fn()
        sync()
        samples.append((time.perf_counter() - t) / calls)
    med = statistics.median(samples)
    return med, (max(samples) - min(samples)) / med, calls


def ref_step(f: torch.Tensor) -> torch.Tensor:
    """Plain-PyTorch reference: f has shape (19, N, N, N) indexed [q, z, y, x]."""
    g = torch.stack([torch.roll(f[q], shifts=(cz, cy, cx), dims=(0, 1, 2))
                     for q, (cx, cy, cz) in enumerate(C)])
    return 0.9 * g + 0.1 * g.sum(0, keepdim=True) / 19.0


def main() -> int:
    if not torch.backends.mps.is_available():
        print("MPS (Apple GPU) not available: this script needs an Apple Silicon Mac.")
        return 1
    if not hasattr(torch.mps, "compile_shader"):
        print(f"torch {torch.__version__} lacks torch.mps.compile_shader; install a newer torch.")
        return 1
    info = machine_info()
    print(f"{info['model']} | {info['chip']} | GPU cores {info['gpu_cores']} | "
          f"{info['memory_gb']} GB | macOS {info['macos']} | torch {info['torch']}")
    lib = torch.mps.compile_shader(SHADERS)
    mem_budget = info["memory_gb"] * 2**30 * 0.25  # use at most a quarter of RAM
    results: dict = {"machine": info, "copy": [], "d3q19_metal": [], "d3q19_torch": []}

    # 1. correctness of the fused kernel against the reference
    n = 24
    f = torch.rand(19, n, n, n, device="mps")
    out = torch.empty_like(f)
    lib.d3q19_step(f, out, n, threads=n**3)
    sync()
    ref = ref_step(f)
    err = ((out - ref).abs().max() / ref.abs().max()).item()
    m_in, m_out = f.cpu().double().sum().item(), out.cpu().double().sum().item()  # MPS has no float64
    mass = abs(m_out - m_in) / m_in
    results["correctness"] = {"max_rel_error_vs_reference": err, "mass_drift": mass}
    print(f"correctness: max rel. error vs reference {err:.1e}, mass drift {mass:.1e}")
    if not (err < 1e-5 and mass < 1e-5):
        print("Kernel output does not match the reference; aborting (numbers would be meaningless).")
        return 2

    # 2. copy bandwidth
    for gib in (0.25, 1.0, 2.0):
        if 2 * gib * 2**30 > mem_budget:
            continue
        n4 = int(gib * 2**30) // 16
        a = torch.rand(n4 * 4, device="mps")
        b = torch.empty_like(a)
        med, spread, _ = timed(lambda: lib.copy_f4(a, b, threads=n4))
        gbs = 2 * a.numel() * 4 / med / 1e9
        assert torch.equal(a[:1000], b[:1000])
        results["copy"].append({"size_gib": gib, "gb_s": round(gbs, 1), "spread": round(spread, 3)})
        print(f"copy  {gib:>5.2f} GiB per buffer: {gbs:7.1f} GB/s  (spread {spread:.1%})")
        del a, b
    copy_peak = max(r["gb_s"] for r in results["copy"])

    # 3. fused D3Q19 step at several sizes
    for n in (128, 192, 256, 320, 384):
        need = 2 * 19 * 4 * n**3
        if need > mem_budget:
            continue
        fa = torch.rand(19 * n**3, device="mps")
        fb = torch.empty_like(fa)
        state = [fa, fb]

        def step():
            lib.d3q19_step(state[0], state[1], n, threads=n**3)
            state[0], state[1] = state[1], state[0]

        med, spread, calls = timed(step)
        mlups = n**3 / med / 1e6
        gbs = mlups * 1e6 * BYTES_PER_CELL / 1e9
        results["d3q19_metal"].append({"n": n, "mlups": round(mlups), "effective_gb_s": round(gbs, 1),
                                       "fraction_of_copy": round(gbs / copy_peak, 3),
                                       "spread": round(spread, 3), "memory_gib": round(need / 2**30, 2)})
        print(f"D3Q19 Metal {n:>3}^3 ({need / 2**30:4.1f} GiB): {mlups:7.0f} MLUPS, "
              f"{gbs:6.1f} GB/s = {gbs / copy_peak:.0%} of copy  (spread {spread:.1%})")
        del fa, fb, state

    # 4. plain PyTorch for comparison (software headroom)
    n = 128
    fq = torch.rand(19, n, n, n, device="mps")
    holder = [fq]

    def tstep():
        holder[0] = ref_step(holder[0])

    med, spread, _ = timed(tstep, repeats=3)
    mlups = n**3 / med / 1e6
    results["d3q19_torch"].append({"n": n, "mlups": round(mlups), "spread": round(spread, 3)})
    print(f"D3Q19 plain PyTorch {n}^3: {mlups:7.0f} MLUPS (same math, no custom kernel)")

    best = max((r["mlups"] for r in results["d3q19_metal"]), default=0)
    results["summary"] = {"copy_peak_gb_s": copy_peak, "d3q19_best_mlups": best}
    stamp = time.strftime("%Y%m%d-%H%M%S")
    chip = (info["chip"] or "unknown").replace(" ", "_")
    out_path = Path(__file__).with_name(f"bench_{chip}_{info['memory_gb']}GB_{stamp}.json")
    out_path.write_text(json.dumps(results, indent=1))
    print(f"\nsummary: copy {copy_peak:.0f} GB/s, D3Q19 best {best} MLUPS -> {out_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
