"""GPU benchmark for lattice-Boltzmann-type workloads on NVIDIA GPUs (CUDA via PyTorch + Triton).

Counterpart of bench_lbm_gpu.py (Apple/Metal): same D3Q19 kernel, same correctness check,
same JSON layout, so Apple and NVIDIA numbers are directly comparable.

1. copy bandwidth: torch's device copy (the practical ceiling, "STREAM copy")
2. D3Q19 stream + collide proxy: one fused Triton kernel per time step (pull streaming on
   a periodic grid, BGK-like relaxation; 19 floats read + 19 written per cell = 152 B) at
   several grid sizes, reported as MLUPS (million lattice updates per second)
3. the same step in plain PyTorch (torch.roll), to show the software headroom

The fused kernel is checked against a plain-PyTorch reference before it is timed; a wrong
kernel aborts the run. If Triton is not available (e.g. native Windows), steps 1 and 3
still run and the JSON says the kernel was not measured.

Run on Linux or WSL2 (PyTorch's Linux wheels include CUDA and Triton):

    python3 -m venv ~/physis-bench
    ~/physis-bench/bin/pip install torch
    ~/physis-bench/bin/python bench_lbm_cuda.py

Takes about 1-3 minutes. Nothing but the GPU model, driver, VRAM and software versions is
recorded.
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

try:
    import triton
    import triton.language as tl

    HAVE_TRITON = True
    TRITON_ERROR = ""
except Exception as exc:  # not installed or unsupported platform
    HAVE_TRITON = False
    TRITON_ERROR = f"{type(exc).__name__}: {exc}"

# D3Q19 velocity set, identical order to bench_lbm_gpu.py
C = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
     (1, 1, 0), (-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 0, 1), (-1, 0, -1), (1, 0, -1),
     (-1, 0, 1), (0, 1, 1), (0, -1, -1), (0, 1, -1), (0, -1, 1)]
BYTES_PER_CELL = 19 * 4 * 2  # read + write, float32


if HAVE_TRITON:

    @triton.jit
    def _pull(fin, q: tl.constexpr, cx: tl.constexpr, cy: tl.constexpr, cz: tl.constexpr,
              x, y, z, N, n3, mask):
        xs = (x - cx + N) % N
        ys = (y - cy + N) % N
        zs = (z - cz + N) % N
        return tl.load(fin + q * n3 + (zs * N + ys) * N + xs, mask=mask, other=0.0)

    @triton.jit
    def _put(fout, q: tl.constexpr, val, idx, n3, mask):
        tl.store(fout + q * n3 + idx, val, mask=mask)

    @triton.jit
    def d3q19_step_kernel(fin, fout, N, n3, BLOCK: tl.constexpr):
        # Layout f[q][z][y][x], x fastest; 64-bit offsets (q * n3 exceeds 2^31 on big grids).
        idx = tl.program_id(0).to(tl.int64) * BLOCK + tl.arange(0, BLOCK).to(tl.int64)
        n = N.to(tl.int64)
        m = n3.to(tl.int64)
        mask = idx < m
        x = idx % n
        y = (idx // n) % n
        z = idx // (n * n)
        f0 = _pull(fin, 0, 0, 0, 0, x, y, z, n, m, mask)
        f1 = _pull(fin, 1, 1, 0, 0, x, y, z, n, m, mask)
        f2 = _pull(fin, 2, -1, 0, 0, x, y, z, n, m, mask)
        f3 = _pull(fin, 3, 0, 1, 0, x, y, z, n, m, mask)
        f4 = _pull(fin, 4, 0, -1, 0, x, y, z, n, m, mask)
        f5 = _pull(fin, 5, 0, 0, 1, x, y, z, n, m, mask)
        f6 = _pull(fin, 6, 0, 0, -1, x, y, z, n, m, mask)
        f7 = _pull(fin, 7, 1, 1, 0, x, y, z, n, m, mask)
        f8 = _pull(fin, 8, -1, -1, 0, x, y, z, n, m, mask)
        f9 = _pull(fin, 9, 1, -1, 0, x, y, z, n, m, mask)
        f10 = _pull(fin, 10, -1, 1, 0, x, y, z, n, m, mask)
        f11 = _pull(fin, 11, 1, 0, 1, x, y, z, n, m, mask)
        f12 = _pull(fin, 12, -1, 0, -1, x, y, z, n, m, mask)
        f13 = _pull(fin, 13, 1, 0, -1, x, y, z, n, m, mask)
        f14 = _pull(fin, 14, -1, 0, 1, x, y, z, n, m, mask)
        f15 = _pull(fin, 15, 0, 1, 1, x, y, z, n, m, mask)
        f16 = _pull(fin, 16, 0, -1, -1, x, y, z, n, m, mask)
        f17 = _pull(fin, 17, 0, 1, -1, x, y, z, n, m, mask)
        f18 = _pull(fin, 18, 0, -1, 1, x, y, z, n, m, mask)
        rho = (f0 + f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8 + f9 + f10 + f11 + f12 + f13
               + f14 + f15 + f16 + f17 + f18)
        feq = rho / 19.0
        _put(fout, 0, 0.9 * f0 + 0.1 * feq, idx, m, mask)
        _put(fout, 1, 0.9 * f1 + 0.1 * feq, idx, m, mask)
        _put(fout, 2, 0.9 * f2 + 0.1 * feq, idx, m, mask)
        _put(fout, 3, 0.9 * f3 + 0.1 * feq, idx, m, mask)
        _put(fout, 4, 0.9 * f4 + 0.1 * feq, idx, m, mask)
        _put(fout, 5, 0.9 * f5 + 0.1 * feq, idx, m, mask)
        _put(fout, 6, 0.9 * f6 + 0.1 * feq, idx, m, mask)
        _put(fout, 7, 0.9 * f7 + 0.1 * feq, idx, m, mask)
        _put(fout, 8, 0.9 * f8 + 0.1 * feq, idx, m, mask)
        _put(fout, 9, 0.9 * f9 + 0.1 * feq, idx, m, mask)
        _put(fout, 10, 0.9 * f10 + 0.1 * feq, idx, m, mask)
        _put(fout, 11, 0.9 * f11 + 0.1 * feq, idx, m, mask)
        _put(fout, 12, 0.9 * f12 + 0.1 * feq, idx, m, mask)
        _put(fout, 13, 0.9 * f13 + 0.1 * feq, idx, m, mask)
        _put(fout, 14, 0.9 * f14 + 0.1 * feq, idx, m, mask)
        _put(fout, 15, 0.9 * f15 + 0.1 * feq, idx, m, mask)
        _put(fout, 16, 0.9 * f16 + 0.1 * feq, idx, m, mask)
        _put(fout, 17, 0.9 * f17 + 0.1 * feq, idx, m, mask)
        _put(fout, 18, 0.9 * f18 + 0.1 * feq, idx, m, mask)


def launch(fin: torch.Tensor, fout: torch.Tensor, n: int, block: int) -> None:
    n3 = n**3
    d3q19_step_kernel[(triton.cdiv(n3, block),)](fin, fout, n, n3, BLOCK=block)


def sh(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return ""


def machine_info() -> dict:
    p = torch.cuda.get_device_properties(0)
    smi = sh(["nvidia-smi", "--query-gpu=driver_version,memory.total,clocks.max.memory,power.limit",
              "--format=csv,noheader"]).strip()
    return {
        "gpu": p.name,
        "compute_capability": f"{p.major}.{p.minor}",
        "sm_count": p.multi_processor_count,
        "vram_gb": round(p.total_memory / 2**30, 1),
        "nvidia_smi": smi,
        "os": platform.platform(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "triton": triton.__version__ if HAVE_TRITON else None,
    }


def sync() -> None:
    torch.cuda.synchronize()


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
    if not torch.cuda.is_available():
        print("CUDA not available: this script needs an NVIDIA GPU and a CUDA build of torch.")
        print(f"torch {torch.__version__}, torch.version.cuda = {torch.version.cuda}")
        return 1
    torch.backends.cuda.matmul.allow_tf32 = False
    info = machine_info()
    print(f"{info['gpu']} | CC {info['compute_capability']} | {info['sm_count']} SMs | "
          f"{info['vram_gb']} GB | driver/mem/clock/power: {info['nvidia_smi']} | "
          f"torch {info['torch']} CUDA {info['cuda']} | triton {info['triton']}")
    free, _ = torch.cuda.mem_get_info()
    mem_budget = 0.7 * free
    results: dict = {"machine": info, "copy": [], "d3q19_kernel": [], "d3q19_torch": [],
                     "kernel_backend": "triton" if HAVE_TRITON else None}

    # 1. copy bandwidth
    for gib in (0.25, 1.0, 2.0, 4.0):
        if 2 * gib * 2**30 > mem_budget:
            continue
        a = torch.rand(int(gib * 2**30) // 4, device="cuda")
        b = torch.empty_like(a)
        med, spread, _ = timed(lambda: b.copy_(a))
        gbs = 2 * a.numel() * 4 / med / 1e9
        assert torch.equal(a[:1000], b[:1000])
        results["copy"].append({"size_gib": gib, "gb_s": round(gbs, 1), "spread": round(spread, 3)})
        print(f"copy  {gib:>5.2f} GiB per buffer: {gbs:7.1f} GB/s  (spread {spread:.1%})")
        del a, b
    torch.cuda.empty_cache()
    copy_peak = max(r["gb_s"] for r in results["copy"])

    # 2. fused D3Q19 kernel: correctness, block-size choice, sizes
    if HAVE_TRITON:
        n = 24
        f = torch.rand(19, n, n, n, device="cuda")
        out = torch.empty_like(f)
        try:
            launch(f, out, n, 256)
            sync()
        except Exception as exc:
            results["kernel_error"] = f"{type(exc).__name__}: {exc}"
            print(f"Triton kernel failed to compile/run: {results['kernel_error']}")
        else:
            ref = ref_step(f)
            err = ((out - ref).abs().max() / ref.abs().max()).item()
            m_in, m_out = f.double().sum().item(), out.double().sum().item()
            mass = abs(m_out - m_in) / m_in
            results["correctness"] = {"max_rel_error_vs_reference": err, "mass_drift": mass}
            print(f"correctness: max rel. error vs reference {err:.1e}, mass drift {mass:.1e}")
            if not (err < 1e-5 and mass < 1e-5):
                print("Kernel output does not match the reference; aborting (numbers would be meaningless).")
                return 2

            n = 256
            fa = torch.rand(19 * n**3, device="cuda")
            fb = torch.empty_like(fa)
            best_block, best_t = 256, float("inf")
            for block in (128, 256, 512, 1024):
                t, _, _ = timed(lambda: launch(fa, fb, n, block), min_seconds=0.3, repeats=3)
                if t < best_t:
                    best_block, best_t = block, t
            results["block_size"] = best_block
            del fa, fb
            torch.cuda.empty_cache()
            print(f"block size: {best_block}")

            for n in (128, 192, 256, 320, 384, 448, 512):
                need = 2 * 19 * 4 * n**3
                if need > mem_budget:
                    continue
                state = [torch.rand(19 * n**3, device="cuda"), torch.empty(19 * n**3, device="cuda")]

                def step():
                    launch(state[0], state[1], n, best_block)
                    state[0], state[1] = state[1], state[0]

                med, spread, _ = timed(step)
                mlups = n**3 / med / 1e6
                gbs = mlups * 1e6 * BYTES_PER_CELL / 1e9
                results["d3q19_kernel"].append({"n": n, "mlups": round(mlups), "effective_gb_s": round(gbs, 1),
                                                "fraction_of_copy": round(gbs / copy_peak, 3),
                                                "spread": round(spread, 3), "memory_gib": round(need / 2**30, 2)})
                print(f"D3Q19 Triton {n:>3}^3 ({need / 2**30:4.1f} GiB): {mlups:7.0f} MLUPS, "
                      f"{gbs:6.1f} GB/s = {gbs / copy_peak:.0%} of copy  (spread {spread:.1%})")
                del state
                torch.cuda.empty_cache()
    else:
        print(f"Triton not available ({TRITON_ERROR}); fused kernel not measured.")
        results["kernel_error"] = TRITON_ERROR

    # 3. plain PyTorch for comparison
    n = 128
    holder = [torch.rand(19, n, n, n, device="cuda")]

    def tstep():
        holder[0] = ref_step(holder[0])

    med, spread, _ = timed(tstep, repeats=3)
    mlups = n**3 / med / 1e6
    results["d3q19_torch"].append({"n": n, "mlups": round(mlups), "spread": round(spread, 3)})
    print(f"D3Q19 plain PyTorch {n}^3: {mlups:7.0f} MLUPS (same math, no custom kernel)")

    best = max((r["mlups"] for r in results["d3q19_kernel"]), default=None)
    results["summary"] = {"copy_peak_gb_s": copy_peak, "d3q19_best_mlups": best,
                          "d3q19_estimate_from_copy_mlups": round(copy_peak * 1e9 / BYTES_PER_CELL / 1e6)}
    stamp = time.strftime("%Y%m%d-%H%M%S")
    gpu = info["gpu"].replace(" ", "_").replace("/", "_")
    out_path = Path(__file__).with_name(f"bench_{gpu}_{round(info['vram_gb'])}GB_{stamp}.json")
    out_path.write_text(json.dumps(results, indent=1))
    measured = f"D3Q19 best {best} MLUPS" if best else "D3Q19 kernel not measured"
    print(f"\nsummary: copy {copy_peak:.0f} GB/s, {measured} -> {out_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
