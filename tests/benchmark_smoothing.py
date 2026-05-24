"""Smoothing benchmarks comparing filter configurations.

Evaluates jitter reduction, latency, and tracking accuracy across
different smoothing parameter combinations.
"""

import sys
import math
import time
import random
from typing import List, Tuple, Dict

import numpy as np

sys.path.insert(0, ".")

from src.tracking.smoothing import KalmanFilter2D, EMAFilter, DeadzoneFilter, SmoothingPipeline


def generate_test_trajectory(
    num_points: int = 200, noise_std: float = 8.0
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """Generate a smooth trajectory with noisy observations."""
    clean = []
    noisy = []
    for i in range(num_points):
        t = i / 30.0
        x = 400.0 + 300.0 * math.sin(t * 0.8)
        y = 300.0 + 200.0 * math.cos(t * 1.2)
        clean.append((x, y))
        nx = x + random.gauss(0, noise_std)
        ny = y + random.gauss(0, noise_std)
        noisy.append((nx, ny))
    return clean, noisy


def compute_rmse(
    reference: List[Tuple[float, float]], actual: List[Tuple[float, float]]
) -> float:
    """Compute RMSE between two trajectories."""
    total = 0.0
    for (rx, ry), (ax, ay) in zip(reference, actual):
        total += (rx - ax) ** 2 + (ry - ay) ** 2
    return math.sqrt(total / len(reference))


def compute_jitter(points: List[Tuple[float, float]]) -> float:
    """Compute average frame-to-frame jitter (mean successive displacement)."""
    if len(points) < 2:
        return 0.0
    total = 0.0
    for i in range(1, len(points)):
        dx = points[i][0] - points[i - 1][0]
        dy = points[i][1] - points[i - 1][1]
        total += math.sqrt(dx * dx + dy * dy)
    return total / (len(points) - 1)


def compute_latency_frames(
    reference: List[Tuple[float, float]], filtered: List[Tuple[float, float]]
) -> float:
    """Estimate tracking latency in frames via cross-correlation of x-axis."""
    ref_x = np.array([p[0] for p in reference])
    filt_x = np.array([p[0] for p in filtered])
    ref_x = ref_x - np.mean(ref_x)
    filt_x = filt_x - np.mean(filt_x)
    correlation = np.correlate(ref_x, filt_x, mode="full")
    lag = np.argmax(correlation) - (len(ref_x) - 1)
    return abs(lag)


def benchmark_pipeline(
    name: str,
    pipeline_factory,
    clean: List[Tuple[float, float]],
    noisy: List[Tuple[float, float]],
) -> Dict[str, float]:
    """Run a single benchmark for a given pipeline configuration."""
    pipeline = pipeline_factory()
    filtered = []

    start = time.perf_counter()
    for x, y in noisy:
        sx, sy = pipeline.smooth(x, y)
        filtered.append((sx, sy))
    elapsed_ms = (time.perf_counter() - start) * 1000

    rmse_noisy = compute_rmse(clean, noisy)
    rmse_filtered = compute_rmse(clean, filtered)
    jitter_noisy = compute_jitter(noisy)
    jitter_filtered = compute_jitter(filtered)
    latency = compute_latency_frames(clean, filtered)

    return {
        "name": name,
        "rmse_noisy": rmse_noisy,
        "rmse_filtered": rmse_filtered,
        "rmse_reduction_pct": (1 - rmse_filtered / rmse_noisy) * 100 if rmse_noisy > 0 else 0,
        "jitter_noisy": jitter_noisy,
        "jitter_filtered": jitter_filtered,
        "jitter_reduction_pct": (1 - jitter_filtered / jitter_noisy) * 100 if jitter_noisy > 0 else 0,
        "latency_frames": latency,
        "processing_time_ms": elapsed_ms,
    }


def main() -> None:
    print("=" * 75)
    print("  SMOOTHING BENCHMARKS")
    print("=" * 75)

    random.seed(42)
    np.random.seed(42)

    clean, noisy = generate_test_trajectory(num_points=300, noise_std=10.0)
    print(f"\nTrajectory: {len(clean)} points, noise_std=10.0px")

    configs = [
        ("Kalman Only (low Q)", lambda: SmoothingPipeline(1e-5, 1e-1, 1.0, 0.0)),
        ("Kalman Only (default)", lambda: SmoothingPipeline(1e-4, 1e-2, 1.0, 0.0)),
        ("Kalman Only (high Q)", lambda: SmoothingPipeline(1e-3, 1e-2, 1.0, 0.0)),
        ("EMA Only (alpha=0.2)", lambda: SmoothingPipeline(1e-4, 1e-2, 0.2, 0.0)),
        ("EMA Only (alpha=0.5)", lambda: SmoothingPipeline(1e-4, 1e-2, 0.5, 0.0)),
        ("Deadzone Only (r=5)", lambda: SmoothingPipeline(1e-4, 1e-2, 1.0, 5.0)),
        ("Full Pipeline (default)", lambda: SmoothingPipeline(1e-4, 1e-2, 0.3, 3.0)),
        ("Full Pipeline (aggressive)", lambda: SmoothingPipeline(1e-5, 1e-1, 0.2, 5.0)),
        ("Full Pipeline (responsive)", lambda: SmoothingPipeline(1e-3, 1e-3, 0.6, 2.0)),
    ]

    results = []
    for name, factory in configs:
        result = benchmark_pipeline(name, factory, clean, noisy)
        results.append(result)

    header = f"{'Config':<30} {'RMSE':>8} {'RMSE%':>7} {'Jitter':>8} {'Jit%':>7} {'Lag':>5} {'Time':>8}"
    print(f"\n{header}")
    print("-" * 75)

    noisy_rmse = results[0]["rmse_noisy"]
    noisy_jitter = results[0]["jitter_noisy"]
    print(f"{'(Unfiltered baseline)':<30} {noisy_rmse:>8.2f} {'---':>7} {noisy_jitter:>8.2f} {'---':>7} {'---':>5} {'---':>8}")

    for r in results:
        print(
            f"{r['name']:<30} "
            f"{r['rmse_filtered']:>8.2f} "
            f"{r['rmse_reduction_pct']:>6.1f}% "
            f"{r['jitter_filtered']:>8.2f} "
            f"{r['jitter_reduction_pct']:>6.1f}% "
            f"{r['latency_frames']:>5.0f} "
            f"{r['processing_time_ms']:>7.2f}ms"
        )

    best_rmse = min(results, key=lambda r: r["rmse_filtered"])
    best_jitter = min(results, key=lambda r: r["jitter_filtered"])
    best_balanced = min(
        results,
        key=lambda r: r["rmse_filtered"] * 0.5 + r["jitter_filtered"] * 0.3 + r["latency_frames"] * 2.0,
    )

    print(f"\n{'Best RMSE:':<25} {best_rmse['name']} ({best_rmse['rmse_filtered']:.2f}px)")
    print(f"{'Best Jitter:':<25} {best_jitter['name']} ({best_jitter['jitter_filtered']:.2f}px)")
    print(f"{'Best Balanced:':<25} {best_balanced['name']}")

    print("\n" + "=" * 75)
    print("  COMPONENT ISOLATION TESTS")
    print("=" * 75)

    # Kalman filter standalone
    print("\n--- KalmanFilter2D ---")
    kf = KalmanFilter2D(process_noise=1e-4, measurement_noise=1e-2)
    kf_out = []
    for x, y in noisy:
        sx, sy = kf.update((x, y))
        kf_out.append((sx, sy))
    print(f"  RMSE: {compute_rmse(clean, kf_out):.2f}px")
    print(f"  Jitter: {compute_jitter(kf_out):.2f}px")

    # EMA standalone
    print("\n--- EMAFilter (alpha=0.3) ---")
    ema_x = EMAFilter(alpha=0.3)
    ema_y = EMAFilter(alpha=0.3)
    ema_out = []
    for x, y in noisy:
        ema_out.append((ema_x.update(x), ema_y.update(y)))
    print(f"  RMSE: {compute_rmse(clean, ema_out):.2f}px")
    print(f"  Jitter: {compute_jitter(ema_out):.2f}px")

    # Deadzone standalone
    print("\n--- DeadzoneFilter (radius=5.0) ---")
    dz = DeadzoneFilter(radius=5.0)
    dz_out = []
    for x, y in noisy:
        dz_out.append(dz.apply((x, y)))
    print(f"  RMSE: {compute_rmse(clean, dz_out):.2f}px")
    print(f"  Jitter: {compute_jitter(dz_out):.2f}px")

    print("\n" + "=" * 75)
    print("  BENCHMARK COMPLETE")
    print("=" * 75)


if __name__ == "__main__":
    main()
