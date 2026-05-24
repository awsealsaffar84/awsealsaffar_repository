"""Run benchmark experiment scenarios for system evaluation."""

import csv
import os
import math
import random
import time
from typing import List, Dict, Any, Optional

import numpy as np

from src.evaluation.metrics import Metrics


class ExperimentConfig:
    """Configuration for a single experiment run.

    Attributes:
        name: Experiment name.
        target_sizes: List of target sizes to test (pixels).
        target_distances: List of target distances to test (pixels).
        num_trials: Number of trials per condition.
        csv_log_path: Path to save CSV results.
    """

    def __init__(
        self,
        name: str = "default_experiment",
        target_sizes: Optional[List[int]] = None,
        target_distances: Optional[List[int]] = None,
        num_trials: int = 20,
        csv_log_path: str = "data/results/experiment_log.csv",
    ) -> None:
        """Initialize experiment configuration.

        Args:
            name: Name of the experiment.
            target_sizes: Target sizes in pixels.
            target_distances: Target distances in pixels.
            num_trials: Number of trials per condition.
            csv_log_path: CSV log output path.
        """
        self.name = name
        self.target_sizes = target_sizes or [30, 50, 80, 120]
        self.target_distances = target_distances or [100, 200, 400, 600]
        self.num_trials = num_trials
        self.csv_log_path = csv_log_path


class ExperimentRunner:
    """Runs benchmark experiments and records results.

    Manages the lifecycle of Fitts' Law and pointing experiments,
    presenting targets and collecting timing/accuracy data.

    Attributes:
        config: Experiment configuration.
        results: Collected experiment results.
    """

    def __init__(self, config: Optional[ExperimentConfig] = None) -> None:
        """Initialize the experiment runner.

        Args:
            config: Experiment configuration. Uses defaults if None.
        """
        self.config = config if config is not None else ExperimentConfig()
        self.results: List[Dict[str, Any]] = []

    def setup(self) -> None:
        """Prepare the experiment environment and display."""
        output_dir = os.path.dirname(self.config.csv_log_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    def run_fitts_law_test(self) -> Dict[str, Any]:
        """Run a Fitts' Law pointing experiment.

        Presents circular targets at varying sizes and distances
        and records movement time and accuracy.

        Returns:
            Dictionary of aggregated experiment results.
        """
        base_time = 200.0  # base movement time in ms
        all_movement_times: List[float] = []
        all_error_distances: List[float] = []
        conditions_tested = 0

        for target_size in self.config.target_sizes:
            for target_distance in self.config.target_distances:
                W = float(target_size)
                D = float(target_distance)
                ID = math.log2(D / W + 1.0)
                conditions_tested += 1

                for trial in range(self.config.num_trials):
                    # Simulate movement time: base_time * (1 + ID * 0.3) + noise
                    noise = random.gauss(0, 15.0)
                    movement_time = base_time * (1.0 + ID * 0.3) + noise
                    movement_time = max(50.0, movement_time)

                    # Target position: place target at distance D from origin
                    # along a random angle
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = D * math.cos(angle)
                    target_y = D * math.sin(angle)

                    # Endpoint position: target + random offset
                    offset_x = random.gauss(0, W * 0.15)
                    offset_y = random.gauss(0, W * 0.15)
                    endpoint_x = target_x + offset_x
                    endpoint_y = target_y + offset_y

                    error_distance = math.sqrt(offset_x ** 2 + offset_y ** 2)

                    trial_result = {
                        "test_type": "fitts_law",
                        "trial_num": trial + 1,
                        "target_size": target_size,
                        "target_distance": target_distance,
                        "index_of_difficulty": round(ID, 4),
                        "movement_time_ms": round(movement_time, 2),
                        "target_x": round(target_x, 2),
                        "target_y": round(target_y, 2),
                        "endpoint_x": round(endpoint_x, 2),
                        "endpoint_y": round(endpoint_y, 2),
                        "error_distance": round(error_distance, 2),
                    }
                    self.results.append(trial_result)
                    all_movement_times.append(movement_time)
                    all_error_distances.append(error_distance)

        mean_mt = float(np.mean(all_movement_times)) if all_movement_times else 0.0
        mean_accuracy = float(np.mean(all_error_distances)) if all_error_distances else 0.0
        # Throughput: mean ID / mean MT (in seconds)
        all_ids = [r["index_of_difficulty"] for r in self.results if r["test_type"] == "fitts_law"]
        mean_id = float(np.mean(all_ids)) if all_ids else 0.0
        mean_throughput = mean_id / (mean_mt / 1000.0) if mean_mt > 0 else 0.0

        summary = {
            "test_type": "fitts_law",
            "mean_mt": round(mean_mt, 2),
            "mean_accuracy": round(mean_accuracy, 2),
            "mean_throughput": round(mean_throughput, 4),
            "conditions_tested": conditions_tested,
            "total_trials": len(all_movement_times),
        }
        return summary

    def run_click_accuracy_test(self) -> Dict[str, Any]:
        """Run a click accuracy test.

        Measures the positional error of dwell and blink clicks.

        Returns:
            Dictionary of click accuracy results.
        """
        num_targets = 50
        screen_width = 1920
        screen_height = 1080
        click_radius = 30.0  # pixels, hit threshold

        click_results: List[Dict[str, Any]] = []
        error_distances: List[float] = []
        hits = 0

        for i in range(num_targets):
            # Random target position
            target_x = random.uniform(50, screen_width - 50)
            target_y = random.uniform(50, screen_height - 50)

            # Simulate click position with some offset
            click_offset_x = random.gauss(0, 12.0)
            click_offset_y = random.gauss(0, 12.0)
            click_x = target_x + click_offset_x
            click_y = target_y + click_offset_y

            error_dist = math.sqrt(click_offset_x ** 2 + click_offset_y ** 2)
            is_hit = error_dist <= click_radius

            if is_hit:
                hits += 1

            trial_result = {
                "test_type": "click_accuracy",
                "trial_num": i + 1,
                "target_x": round(target_x, 2),
                "target_y": round(target_y, 2),
                "click_x": round(click_x, 2),
                "click_y": round(click_y, 2),
                "error_distance": round(error_dist, 2),
                "hit": is_hit,
            }
            self.results.append(trial_result)
            click_results.append(trial_result)
            error_distances.append(error_dist)

        mean_error = float(np.mean(error_distances)) if error_distances else 0.0
        hit_rate = hits / num_targets if num_targets > 0 else 0.0

        summary = {
            "test_type": "click_accuracy",
            "mean_error": round(mean_error, 2),
            "hit_rate": round(hit_rate, 4),
            "total_targets": num_targets,
            "total_hits": hits,
            "results": click_results,
        }
        return summary

    def run_fatigue_test(self, duration_min: float = 15.0) -> Dict[str, Any]:
        """Run a fatigue monitoring test over a fixed duration.

        Args:
            duration_min: Duration of the fatigue test in minutes.

        Returns:
            Dictionary of fatigue test results.
        """
        block_duration_min = 1.0
        num_blocks = max(1, int(duration_min / block_duration_min))

        time_blocks: List[float] = []
        error_rates: List[float] = []
        latencies: List[float] = []

        for block_idx in range(num_blocks):
            t = (block_idx + 1) * block_duration_min
            progress = block_idx / max(1, num_blocks - 1)

            # Error rate starts at ~5% and increases to ~15%
            base_error = 0.05 + 0.10 * progress
            error_rate = base_error + random.gauss(0, 0.01)
            error_rate = max(0.0, min(1.0, error_rate))

            # Latency starts at ~300ms and increases to ~500ms
            base_latency = 300.0 + 200.0 * progress
            latency = base_latency + random.gauss(0, 10.0)
            latency = max(100.0, latency)

            time_blocks.append(round(t, 2))
            error_rates.append(round(error_rate, 4))
            latencies.append(round(latency, 2))

            # Record each block as a result entry
            block_result = {
                "test_type": "fatigue",
                "block_num": block_idx + 1,
                "time_min": round(t, 2),
                "error_rate": round(error_rate, 4),
                "latency_ms": round(latency, 2),
            }
            self.results.append(block_result)

        # Compute fatigue score using Metrics
        fatigue = Metrics.fatigue_score(duration_min, error_rates, latencies)

        summary = {
            "test_type": "fatigue",
            "duration_min": duration_min,
            "num_blocks": num_blocks,
            "time_blocks": time_blocks,
            "error_rates": error_rates,
            "latencies": latencies,
            "fatigue_score": round(fatigue, 4),
        }
        return summary

    def save_results(self, path: Optional[str] = None) -> None:
        """Save experiment results to a CSV file.

        Args:
            path: Output file path. Defaults to config csv_log_path.
        """
        output_path = path if path is not None else self.config.csv_log_path
        if not self.results:
            return

        # Collect all field names across all result dicts
        fieldnames: List[str] = []
        seen: set = set()
        for row in self.results:
            for key in row.keys():
                if key not in seen:
                    fieldnames.append(key)
                    seen.add(key)

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)

    def load_results(self, path: str) -> List[Dict[str, Any]]:
        """Load experiment results from a CSV file.

        Args:
            path: Path to the CSV file.

        Returns:
            List of result dictionaries.
        """
        loaded: List[Dict[str, Any]] = []
        with open(path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                loaded.append(dict(row))
        return loaded

    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of collected results.

        Returns:
            Summary statistics dictionary.
        """
        if not self.results:
            return {
                "rmse": 0.0,
                "accuracy": 0.0,
                "throughput": 0.0,
                "mean_latency": 0.0,
            }

        # Gather targets and predictions from fitts_law and click_accuracy results
        targets: List[tuple] = []
        predictions: List[tuple] = []
        task_times: List[float] = []
        latencies: List[float] = []

        for r in self.results:
            test_type = r.get("test_type", "")
            if test_type == "fitts_law":
                targets.append((float(r["target_x"]), float(r["target_y"])))
                predictions.append((float(r["endpoint_x"]), float(r["endpoint_y"])))
                task_times.append(float(r["movement_time_ms"]))
            elif test_type == "click_accuracy":
                targets.append((float(r["target_x"]), float(r["target_y"])))
                predictions.append((float(r["click_x"]), float(r["click_y"])))
            elif test_type == "fatigue":
                latencies.append(float(r["latency_ms"]))

        rmse_val = Metrics.rmse(targets, predictions) if targets else 0.0
        accuracy_val = Metrics.accuracy(targets, predictions) if targets else 0.0
        throughput_val = Metrics.throughput(targets, predictions, task_times) if task_times else 0.0
        mean_latency_val = Metrics.mean_latency(latencies) if latencies else 0.0

        return {
            "rmse": round(rmse_val, 4),
            "accuracy": round(accuracy_val, 4),
            "throughput": round(throughput_val, 4),
            "mean_latency": round(mean_latency_val, 4),
        }


if __name__ == "__main__":
    print("Experiments module -- run standalone test")
    config = ExperimentConfig(num_trials=5)
    runner = ExperimentRunner(config)
    runner.setup()

    print("\nRunning Fitts' Law test...")
    fitts_summary = runner.run_fitts_law_test()
    print(f"  Fitts' Law summary: {fitts_summary}")

    print("\nRunning Click Accuracy test...")
    click_summary = runner.run_click_accuracy_test()
    # Don't print the full results list, just the key stats
    print(f"  Click Accuracy: mean_error={click_summary['mean_error']}, "
          f"hit_rate={click_summary['hit_rate']}, "
          f"total_targets={click_summary['total_targets']}")

    print("\nRunning Fatigue test...")
    fatigue_summary = runner.run_fatigue_test()
    print(f"  Fatigue score: {fatigue_summary['fatigue_score']}, "
          f"blocks: {fatigue_summary['num_blocks']}")

    print(f"\nTotal results collected: {len(runner.results)}")

    # Save results
    runner.save_results()
    print(f"Results saved to: {runner.config.csv_log_path}")

    # Get overall summary
    summary = runner.get_summary()
    print(f"\nOverall summary: {summary}")

    print("\nExperiments module test completed.")
