"""Generate Matplotlib and Seaborn charts from experiment results."""

import os
import math
from typing import List, Dict, Any, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False


class ResultPlotter:
    """Creates publication-quality charts from experiment data."""

    def __init__(
        self,
        output_dir: str = "data/results/figures",
        style: str = "seaborn-v0_8-whitegrid",
        dpi: int = 300,
    ) -> None:
        self.output_dir = output_dir
        self.dpi = dpi
        os.makedirs(output_dir, exist_ok=True)
        try:
            plt.style.use(style)
        except OSError:
            plt.style.use("default")
        plt.rcParams.update({
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.dpi": dpi,
            "savefig.dpi": dpi,
            "savefig.bbox": "tight",
            "font.family": "serif",
        })

    def _save_fig(self, fig, save_path: Optional[str], default_name: str) -> str:
        if save_path is None:
            save_path = os.path.join(self.output_dir, default_name)
        fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")
        plt.close(fig)
        return save_path

    def plot_fitts_law(self, results: List[Dict[str, Any]], save_path: Optional[str] = None) -> None:
        """Plot Fitts' Law regression (MT vs ID)."""
        ids = [r["id"] for r in results]
        mts = [r["movement_time_ms"] for r in results]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(ids, mts, alpha=0.5, s=20, color="#2196F3", label="Trials")

        # Linear regression
        coeffs = np.polyfit(ids, mts, 1)
        x_line = np.linspace(min(ids), max(ids), 100)
        y_line = np.polyval(coeffs, x_line)
        ax.plot(x_line, y_line, "r--", linewidth=2, label=f"Fit: MT = {coeffs[0]:.0f}·ID + {coeffs[1]:.0f}")

        # R² calculation
        y_pred = np.polyval(coeffs, ids)
        ss_res = np.sum((np.array(mts) - y_pred) ** 2)
        ss_tot = np.sum((np.array(mts) - np.mean(mts)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        ax.set_xlabel("Index of Difficulty (bits)")
        ax.set_ylabel("Movement Time (ms)")
        ax.set_title(f"Fitts' Law: Movement Time vs. Index of Difficulty (R²={r_squared:.3f})")
        ax.legend()
        ax.grid(True, alpha=0.3)

        path = self._save_fig(fig, save_path, "fitts_law.png")
        print(f"  Saved: {path}")

    def plot_accuracy_heatmap(self, targets: List[Dict[str, Any]], save_path: Optional[str] = None) -> None:
        """Plot heatmap of click accuracy across screen regions."""
        # Bin the screen into a grid
        grid_size = 6
        heatmap = np.zeros((grid_size, grid_size))
        counts = np.zeros((grid_size, grid_size))

        screen_w = max(t.get("target_x", 1920) for t in targets) + 1
        screen_h = max(t.get("target_y", 1080) for t in targets) + 1

        for t in targets:
            tx, ty = t.get("target_x", 0), t.get("target_y", 0)
            error = t.get("error_distance", 0)
            gx = min(int(tx / screen_w * grid_size), grid_size - 1)
            gy = min(int(ty / screen_h * grid_size), grid_size - 1)
            heatmap[gy, gx] += error
            counts[gy, gx] += 1

        counts[counts == 0] = 1
        heatmap = heatmap / counts

        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(heatmap, cmap="RdYlGn_r", aspect="auto", interpolation="nearest")
        plt.colorbar(im, ax=ax, label="Mean Error (px)")
        ax.set_xlabel("Screen X Region")
        ax.set_ylabel("Screen Y Region")
        ax.set_title("Click Accuracy Heatmap Across Screen Regions")

        path = self._save_fig(fig, save_path, "accuracy_heatmap.png")
        print(f"  Saved: {path}")

    def plot_latency_distribution(self, latencies_ms: List[float], save_path: Optional[str] = None) -> None:
        """Plot histogram and KDE of latency measurements."""
        fig, ax = plt.subplots(figsize=(6, 4))

        if HAS_SEABORN:
            sns.histplot(latencies_ms, kde=True, bins=30, color="#4CAF50", ax=ax, alpha=0.7)
        else:
            ax.hist(latencies_ms, bins=30, color="#4CAF50", alpha=0.7, edgecolor="black")

        mean_lat = np.mean(latencies_ms)
        median_lat = np.median(latencies_ms)
        ax.axvline(mean_lat, color="red", linestyle="--", label=f"Mean: {mean_lat:.0f} ms")
        ax.axvline(median_lat, color="blue", linestyle=":", label=f"Median: {median_lat:.0f} ms")

        ax.set_xlabel("Latency (ms)")
        ax.set_ylabel("Frequency")
        ax.set_title("Movement Latency Distribution")
        ax.legend()

        path = self._save_fig(fig, save_path, "latency_distribution.png")
        print(f"  Saved: {path}")

    def plot_fatigue_timeline(
        self,
        timestamps_min: List[float],
        error_rates: List[float],
        latencies_ms: List[float],
        save_path: Optional[str] = None,
    ) -> None:
        """Plot fatigue indicators over time with dual y-axes."""
        fig, ax1 = plt.subplots(figsize=(7, 4))

        color1 = "#E74C3C"
        ax1.plot(timestamps_min, error_rates, "o-", color=color1, linewidth=2, markersize=5, label="Error Rate")
        ax1.set_xlabel("Session Time (minutes)")
        ax1.set_ylabel("Error Rate (%)", color=color1)
        ax1.tick_params(axis="y", labelcolor=color1)

        ax2 = ax1.twinx()
        color2 = "#2196F3"
        ax2.plot(timestamps_min, latencies_ms, "s--", color=color2, linewidth=2, markersize=5, label="Latency")
        ax2.set_ylabel("Mean Latency (ms)", color=color2)
        ax2.tick_params(axis="y", labelcolor=color2)

        ax1.set_title("Fatigue Analysis: Error Rate & Latency Over Time")
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
        ax1.grid(True, alpha=0.3)

        path = self._save_fig(fig, save_path, "fatigue_timeline.png")
        print(f"  Saved: {path}")

    def plot_comparison_bar(
        self,
        methods: List[str],
        metrics: Dict[str, List[float]],
        save_path: Optional[str] = None,
    ) -> None:
        """Plot grouped bar chart comparing methods across metrics."""
        n_methods = len(methods)
        n_metrics = len(metrics)
        x = np.arange(n_methods)
        bar_width = 0.8 / n_metrics

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["#2196F3", "#4CAF50", "#FF9800", "#E74C3C", "#9C27B0"]

        for i, (metric_name, values) in enumerate(metrics.items()):
            offset = (i - n_metrics / 2 + 0.5) * bar_width
            bars = ax.bar(x + offset, values, bar_width, label=metric_name,
                         color=colors[i % len(colors)], alpha=0.85, edgecolor="white")
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                       f"{val:.1f}", ha="center", va="bottom", fontsize=8)

        ax.set_xlabel("Method")
        ax.set_ylabel("Score")
        ax.set_title("System Comparison Across Metrics")
        ax.set_xticks(x)
        ax.set_xticklabels(methods, rotation=15)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        path = self._save_fig(fig, save_path, "comparison_bar.png")
        print(f"  Saved: {path}")

    def plot_jitter_comparison(
        self,
        methods: List[str],
        jitter_values: List[float],
        save_path: Optional[str] = None,
    ) -> None:
        """Plot bar chart comparing jitter across methods/configs."""
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ["#E74C3C" if v > 50 else "#FF9800" if v > 20 else "#4CAF50" for v in jitter_values]
        bars = ax.bar(methods, jitter_values, color=colors, alpha=0.85, edgecolor="white")

        for bar, val in zip(bars, jitter_values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                   f"{val:.1f}px", ha="center", va="bottom", fontsize=9)

        ax.set_ylabel("Jitter Deviation (pixels)")
        ax.set_title("Cursor Jitter Comparison")
        ax.grid(True, alpha=0.3, axis="y")

        path = self._save_fig(fig, save_path, "jitter_comparison.png")
        print(f"  Saved: {path}")

    def save_all(self, results: Dict[str, Any]) -> None:
        """Generate and save all standard plots from a results dictionary."""
        print(f"Generating all plots to {self.output_dir}/")

        if "fitts_trials" in results:
            self.plot_fitts_law(results["fitts_trials"])

        if "click_trials" in results:
            self.plot_accuracy_heatmap(results["click_trials"])

        if "latencies_ms" in results:
            self.plot_latency_distribution(results["latencies_ms"])

        if "fatigue" in results:
            f = results["fatigue"]
            self.plot_fatigue_timeline(
                f.get("timestamps_min", []),
                f.get("error_rates", []),
                f.get("latencies_ms", []),
            )

        if "comparison" in results:
            c = results["comparison"]
            self.plot_comparison_bar(c["methods"], c["metrics"])

        if "jitter" in results:
            j = results["jitter"]
            self.plot_jitter_comparison(j["methods"], j["values"])

        print("All plots saved.")


if __name__ == "__main__":
    import random
    random.seed(42)
    np.random.seed(42)

    plotter = ResultPlotter(output_dir="data/results/figures", dpi=300)

    # Generate synthetic data
    fitts_trials = []
    for _ in range(100):
        id_val = random.uniform(1.0, 5.0)
        mt = 200 + id_val * 150 + random.gauss(0, 50)
        fitts_trials.append({
            "id": id_val,
            "movement_time_ms": mt,
            "target_x": random.randint(100, 1800),
            "target_y": random.randint(100, 1000),
            "error_distance": abs(random.gauss(0, 30)),
        })

    latencies = [abs(random.gauss(400, 120)) for _ in range(200)]
    timestamps = list(range(1, 16))
    error_rates = [5 + i * 0.7 + random.gauss(0, 1) for i in range(15)]
    fatigue_latencies = [300 + i * 15 + random.gauss(0, 20) for i in range(15)]

    print("Generating publication-quality figures (300 DPI)...")
    plotter.plot_fitts_law(fitts_trials)
    plotter.plot_accuracy_heatmap(fitts_trials)
    plotter.plot_latency_distribution(latencies)
    plotter.plot_fatigue_timeline(timestamps, error_rates, fatigue_latencies)
    plotter.plot_comparison_bar(
        ["Our System", "CameraMouseAI", "GameFace", "3M-HCI"],
        {
            "RMSE (px)": [7.6, 15.2, 12.1, 9.8],
            "Jitter (px)": [8.5, 120.0, 80.0, 10.0],
            "Latency (ms)": [350, 520, 480, 400],
        },
    )
    plotter.plot_jitter_comparison(
        ["Our System", "CameraMouseAI", "GameFace", "3M-HCI"],
        [8.5, 120.0, 80.0, 10.0],
    )

    print("\nResultPlotter test completed.")
