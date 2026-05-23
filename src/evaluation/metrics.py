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
        raise NotImplementedError

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
        raise NotImplementedError

    @staticmethod
    def mean_latency(latencies_ms: List[float]) -> float:
        """Compute mean latency from a list of latency measurements.

        Args:
            latencies_ms: List of latency values in milliseconds.

        Returns:
            Mean latency in milliseconds.
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    @staticmethod
    def summary(results: Dict[str, List[float]]) -> Dict[str, float]:
        """Compute a summary of all metrics from raw results.

        Args:
            results: Dictionary mapping metric names to lists of values.

        Returns:
            Dictionary mapping metric names to aggregate values.
        """
        raise NotImplementedError


if __name__ == "__main__":
    print("Metrics module -- run standalone test")
    print("RMSE, accuracy, latency, throughput, fatigue metrics available.")
