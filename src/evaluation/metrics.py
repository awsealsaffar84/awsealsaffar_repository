"""Evaluation metrics: RMSE, accuracy, latency, and fatigue scoring."""

from typing import List, Tuple, Dict

import numpy as np


class Metrics:
    """Computes evaluation metrics for the head-tracking system.

    Provides static methods for calculating RMSE, accuracy,
    latency statistics, throughput, and fatigue indicators.
    """

    @staticmethod
    def rmse(
        targets: List[Tuple[float, float]],
        predictions: List[Tuple[float, float]],
    ) -> float:
        """Compute Root Mean Square Error between target and predicted positions.

        Args:
            targets: List of (x, y) target positions.
            predictions: List of (x, y) predicted positions.

        Returns:
            RMSE value in pixels.
        """
        if not targets or not predictions:
            return 0.0
        targets_arr = np.array(targets, dtype=np.float64)
        preds_arr = np.array(predictions, dtype=np.float64)
        squared_dists = np.sum((targets_arr - preds_arr) ** 2, axis=1)
        return float(np.sqrt(np.mean(squared_dists)))

    @staticmethod
    def accuracy(
        targets: List[Tuple[float, float]],
        predictions: List[Tuple[float, float]],
        tolerance: float = 50.0,
    ) -> float:
        """Compute the fraction of predictions within a tolerance radius.

        Args:
            targets: List of (x, y) target positions.
            predictions: List of (x, y) predicted positions.
            tolerance: Acceptable distance threshold in pixels.

        Returns:
            Accuracy as a fraction in [0.0, 1.0].
        """
        if not targets or not predictions:
            return 0.0
        targets_arr = np.array(targets, dtype=np.float64)
        preds_arr = np.array(predictions, dtype=np.float64)
        distances = np.sqrt(np.sum((targets_arr - preds_arr) ** 2, axis=1))
        hits = np.sum(distances <= tolerance)
        return float(hits / len(distances))

    @staticmethod
    def mean_latency(latencies_ms: List[float]) -> float:
        """Compute mean latency from a list of latency measurements.

        Args:
            latencies_ms: List of latency values in milliseconds.

        Returns:
            Mean latency in milliseconds.
        """
        if not latencies_ms:
            return 0.0
        return float(np.mean(latencies_ms))

    @staticmethod
    def throughput(
        targets: List[Tuple[float, float]],
        predictions: List[Tuple[float, float]],
        task_times_ms: List[float],
    ) -> float:
        """Compute Fitts' Law throughput (bits per second).

        Uses the effective index of difficulty (IDe) based on actual
        endpoint amplitude and scatter (effective width).

        IDe = log2(Ae / We + 1)
        TP  = IDe / MT

        Args:
            targets: List of (x, y) target positions.
            predictions: List of (x, y) actual selection positions.
            task_times_ms: List of task completion times in milliseconds.

        Returns:
            Throughput in bits per second.
        """
        if not targets or not predictions or not task_times_ms:
            return 0.0

        targets_arr = np.array(targets, dtype=np.float64)
        preds_arr = np.array(predictions, dtype=np.float64)

        # Actual amplitude: mean distance from target to selection endpoint
        amplitudes = np.sqrt(np.sum((targets_arr - preds_arr) ** 2, axis=1))
        ae = float(np.mean(amplitudes))

        # Effective width: 4.133 * SD of endpoint scatter
        # Scatter is measured as distance of each endpoint from the centroid
        centroid = np.mean(preds_arr, axis=0)
        scatter = np.sqrt(np.sum((preds_arr - centroid) ** 2, axis=1))
        sd = float(np.std(scatter))

        if sd < 1e-9:
            sd = 1e-3
        we = 4.133 * sd

        # Effective index of difficulty
        ide = float(np.log2(ae / we + 1.0))

        # Mean task time in seconds
        mt = float(np.mean(task_times_ms)) / 1000.0
        if mt < 1e-9:
            return 0.0

        return float(ide / mt)

    @staticmethod
    def fatigue_score(
        session_duration_min: float,
        error_rates: List[float],
        latencies_ms: List[float],
    ) -> float:
        """Estimate a fatigue score based on session metrics.

        Splits the session data into first and second halves, compares
        mean error rate and mean latency between halves, and scales by
        session duration normalized to a 15-minute reference session.

        fatigue = (error_rate_increase_pct + latency_increase_pct) * duration_weight
        duration_weight = session_duration_min / 15.0

        Higher values indicate more fatigue.

        Args:
            session_duration_min: Total session duration in minutes.
            error_rates: Error rate samples over the session.
            latencies_ms: Latency samples over the session.

        Returns:
            Fatigue score (arbitrary units, higher = more fatigued).
        """
        if len(error_rates) < 2 or len(latencies_ms) < 2:
            return 0.0

        err = np.array(error_rates, dtype=np.float64)
        lat = np.array(latencies_ms, dtype=np.float64)

        # Split into first and second halves
        err_mid = len(err) // 2
        lat_mid = len(lat) // 2

        err_first = float(np.mean(err[:err_mid]))
        err_second = float(np.mean(err[err_mid:]))

        lat_first = float(np.mean(lat[:lat_mid]))
        lat_second = float(np.mean(lat[lat_mid:]))

        # Percentage increase (clamped to >= 0)
        if err_first > 1e-9:
            error_rate_increase_pct = max(
                0.0, (err_second - err_first) / err_first * 100.0
            )
        else:
            error_rate_increase_pct = 0.0 if err_second < 1e-9 else 100.0

        if lat_first > 1e-9:
            latency_increase_pct = max(
                0.0, (lat_second - lat_first) / lat_first * 100.0
            )
        else:
            latency_increase_pct = 0.0 if lat_second < 1e-9 else 100.0

        # Duration weight normalized to a 15-minute reference session
        duration_weight = session_duration_min / 15.0

        fatigue = (error_rate_increase_pct + latency_increase_pct) * duration_weight
        return max(0.0, float(fatigue))

    @staticmethod
    def summary(results: Dict[str, List[float]]) -> Dict[str, float]:
        """Compute a summary of all metrics from raw results.

        For each key, computes mean, std, min, max, and median.

        Args:
            results: Dictionary mapping metric names to lists of values.

        Returns:
            Dictionary mapping metric names to aggregate values,
            e.g. {"rmse_mean": X, "rmse_std": Y, "rmse_min": Z, ...}.
        """
        summary_dict: Dict[str, float] = {}
        for key, values in results.items():
            if values:
                arr = np.array(values, dtype=np.float64)
                summary_dict[f"{key}_mean"] = float(np.mean(arr))
                summary_dict[f"{key}_std"] = float(np.std(arr))
                summary_dict[f"{key}_min"] = float(np.min(arr))
                summary_dict[f"{key}_max"] = float(np.max(arr))
                summary_dict[f"{key}_median"] = float(np.median(arr))
            else:
                summary_dict[f"{key}_mean"] = 0.0
                summary_dict[f"{key}_std"] = 0.0
                summary_dict[f"{key}_min"] = 0.0
                summary_dict[f"{key}_max"] = 0.0
                summary_dict[f"{key}_median"] = 0.0
        return summary_dict

    @staticmethod
    def jitter(positions: List[Tuple[float, float]]) -> float:
        """Compute mean successive displacement (cursor jitter).

        Measures cursor stability when the user is stationary by
        computing the average Euclidean distance between consecutive
        position samples.

        Args:
            positions: List of (x, y) cursor positions over time.

        Returns:
            Mean successive displacement in pixels.
        """
        if len(positions) < 2:
            return 0.0
        pos = np.array(positions, dtype=np.float64)
        diffs = np.diff(pos, axis=0)
        displacements = np.sqrt(np.sum(diffs ** 2, axis=1))
        return float(np.mean(displacements))

    @staticmethod
    def task_completion_time(
        start_times_ms: List[float],
        end_times_ms: List[float],
    ) -> Dict[str, float]:
        """Compute per-task completion time statistics.

        Args:
            start_times_ms: List of task start times in milliseconds.
            end_times_ms: List of task end times in milliseconds.

        Returns:
            Dictionary with keys: mean, std, min, max, median
            (all in milliseconds).
        """
        starts = np.array(start_times_ms, dtype=np.float64)
        ends = np.array(end_times_ms, dtype=np.float64)
        durations = ends - starts
        return {
            "mean": float(np.mean(durations)),
            "std": float(np.std(durations)),
            "min": float(np.min(durations)),
            "max": float(np.max(durations)),
            "median": float(np.median(durations)),
        }


if __name__ == "__main__":
    print("Metrics module -- run standalone test")
    print("=" * 50)

    # --- Generate synthetic test data ---
    np.random.seed(42)
    n_samples = 100

    # Targets on a grid-like pattern
    targets = [
        (float(100 + i * 10), float(200 + i * 5)) for i in range(n_samples)
    ]
    # Predictions with some Gaussian noise
    predictions = [
        (t[0] + np.random.normal(0, 15), t[1] + np.random.normal(0, 15))
        for t in targets
    ]

    # Latencies with slight upward trend (simulating fatigue)
    latencies = [
        float(30 + i * 0.2 + np.random.normal(0, 5)) for i in range(n_samples)
    ]

    # Task times in milliseconds
    task_times = [
        float(800 + np.random.normal(0, 100)) for _ in range(n_samples)
    ]

    # Error rates with upward drift
    error_rates = [
        float(0.05 + i * 0.001 + np.random.normal(0, 0.01))
        for i in range(n_samples)
    ]

    # --- 1. RMSE ---
    rmse_val = Metrics.rmse(targets, predictions)
    print(f"RMSE: {rmse_val:.2f} px")
    assert rmse_val > 0, "RMSE should be > 0"

    # --- 2. Accuracy ---
    acc_val = Metrics.accuracy(targets, predictions, tolerance=50.0)
    print(f"Accuracy (tol=50px): {acc_val:.4f}")
    assert 0.0 <= acc_val <= 1.0, "Accuracy should be in [0, 1]"

    # --- 3. Mean Latency ---
    lat_val = Metrics.mean_latency(latencies)
    print(f"Mean Latency: {lat_val:.2f} ms")
    assert lat_val > 0, "Mean latency should be > 0"

    lat_empty = Metrics.mean_latency([])
    assert lat_empty == 0.0, "Mean latency of empty list should be 0.0"

    # --- 4. Throughput ---
    tp_val = Metrics.throughput(targets, predictions, task_times)
    print(f"Throughput: {tp_val:.4f} bits/s")
    assert tp_val > 0, "Throughput should be > 0"

    tp_empty = Metrics.throughput([], [], [])
    assert tp_empty == 0.0, "Throughput of empty data should be 0.0"

    # --- 5. Fatigue Score ---
    fatigue_val = Metrics.fatigue_score(10.0, error_rates, latencies)
    print(f"Fatigue Score (10 min session): {fatigue_val:.2f}")
    assert fatigue_val >= 0.0, "Fatigue score should be >= 0"

    fatigue_empty = Metrics.fatigue_score(5.0, [0.1], [30.0])
    assert fatigue_empty == 0.0, "Fatigue with <2 samples should be 0.0"

    # --- 6. Summary ---
    results = {
        "rmse": [rmse_val, rmse_val * 1.1, rmse_val * 0.9],
        "accuracy": [acc_val, acc_val * 0.95, acc_val * 1.02],
        "latency": [lat_val, lat_val * 1.05, lat_val * 0.98],
    }
    summary_val = Metrics.summary(results)
    print(f"Summary keys: {sorted(summary_val.keys())}")
    for stat in ("mean", "std", "min", "max", "median"):
        assert f"rmse_{stat}" in summary_val, f"Summary should have rmse_{stat}"
        assert f"accuracy_{stat}" in summary_val, f"Summary should have accuracy_{stat}"
        assert f"latency_{stat}" in summary_val, f"Summary should have latency_{stat}"

    # --- 7. Jitter ---
    stationary_positions = [
        (500.0 + np.random.normal(0, 2), 400.0 + np.random.normal(0, 2))
        for _ in range(50)
    ]
    jitter_val = Metrics.jitter(stationary_positions)
    print(f"Jitter (stationary): {jitter_val:.4f} px")
    assert jitter_val > 0, "Jitter should be > 0 with noisy positions"

    jitter_single = Metrics.jitter([(100.0, 200.0)])
    assert jitter_single == 0.0, "Jitter with single point should be 0.0"

    # --- 8. Task Completion Time ---
    start_times = [float(i * 1000) for i in range(20)]
    end_times = [
        float(i * 1000 + 500 + np.random.normal(0, 50)) for i in range(20)
    ]
    tct_val = Metrics.task_completion_time(start_times, end_times)
    print(
        f"Task Completion Time: mean={tct_val['mean']:.1f} ms, "
        f"std={tct_val['std']:.1f} ms, min={tct_val['min']:.1f} ms, "
        f"max={tct_val['max']:.1f} ms, median={tct_val['median']:.1f} ms"
    )
    for key in ("mean", "std", "min", "max", "median"):
        assert key in tct_val, f"TCT should have {key}"

    print("=" * 50)
    print("All assertions passed.")
    print("Metrics module test completed.")
