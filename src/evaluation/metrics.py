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
        targets_arr = np.array(targets, dtype=float)
        preds_arr = np.array(predictions, dtype=float)
        squared_diffs = np.sum((targets_arr - preds_arr) ** 2, axis=1)
        return float(np.sqrt(np.mean(squared_diffs)))

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
        targets_arr = np.array(targets, dtype=float)
        preds_arr = np.array(predictions, dtype=float)
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

        Args:
            targets: List of (x, y) target positions.
            predictions: List of (x, y) actual selection positions.
            task_times_ms: List of task completion times in milliseconds.

        Returns:
            Throughput in bits per second.
        """
        if not targets or not predictions or not task_times_ms:
            return 0.0
        targets_arr = np.array(targets, dtype=float)
        preds_arr = np.array(predictions, dtype=float)
        distances = np.sqrt(np.sum((targets_arr - preds_arr) ** 2, axis=1))
        # Effective width (We) approximated as 4.133 * std of endpoint spread
        we = 4.133 * float(np.std(distances)) if len(distances) > 1 else 1.0
        if we < 1.0:
            we = 1.0
        # Mean distance
        mean_d = float(np.mean(distances)) if float(np.mean(distances)) > 0 else 1.0
        # Effective ID
        id_e = np.log2(mean_d / we + 1.0)
        # Mean task time in seconds
        mean_time_s = float(np.mean(task_times_ms)) / 1000.0
        if mean_time_s <= 0:
            return 0.0
        return float(id_e / mean_time_s)

    @staticmethod
    def fatigue_score(
        session_duration_min: float,
        error_rates: List[float],
        latencies_ms: List[float],
    ) -> float:
        """Estimate a fatigue score based on session metrics.

        Higher values indicate more fatigue. Considers increasing
        error rates and latencies over the session duration.

        Args:
            session_duration_min: Total session duration in minutes.
            error_rates: Error rate samples over the session.
            latencies_ms: Latency samples over the session.

        Returns:
            Fatigue score (arbitrary units, higher = more fatigued).
        """
        if not error_rates or not latencies_ms:
            return 0.0
        # Compute trend (slope) of error rates and latencies
        n = len(error_rates)
        x = np.arange(n, dtype=float)
        if n > 1:
            error_slope = float(np.polyfit(x, error_rates, 1)[0])
            latency_slope = float(np.polyfit(x, latencies_ms, 1)[0])
        else:
            error_slope = 0.0
            latency_slope = 0.0
        # Normalize latency slope to similar scale as error slope
        latency_slope_norm = latency_slope / 1000.0
        # Combine with duration weight
        duration_weight = min(session_duration_min / 30.0, 1.0)
        score = (error_slope * 50.0 + latency_slope_norm * 50.0) * (1.0 + duration_weight)
        return max(0.0, float(score))

    @staticmethod
    def summary(results: Dict[str, List[float]]) -> Dict[str, float]:
        """Compute a summary of all metrics from raw results.

        Args:
            results: Dictionary mapping metric names to lists of values.

        Returns:
            Dictionary mapping metric names to aggregate values.
        """
        summary_dict: Dict[str, float] = {}
        for key, values in results.items():
            if values:
                summary_dict[f"{key}_mean"] = float(np.mean(values))
                summary_dict[f"{key}_std"] = float(np.std(values))
                summary_dict[f"{key}_min"] = float(np.min(values))
                summary_dict[f"{key}_max"] = float(np.max(values))
            else:
                summary_dict[f"{key}_mean"] = 0.0
                summary_dict[f"{key}_std"] = 0.0
                summary_dict[f"{key}_min"] = 0.0
                summary_dict[f"{key}_max"] = 0.0
        return summary_dict


if __name__ == "__main__":
    print("Metrics module -- run standalone test")
    print("RMSE, accuracy, latency, throughput, fatigue metrics available.")
