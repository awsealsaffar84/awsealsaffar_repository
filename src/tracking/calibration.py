"""Nine-point calibration routine for mapping head pose to screen coordinates."""

import json
import math
from typing import List, Tuple, Optional, Dict

import numpy as np


class CalibrationPoint:
    """Represents a single calibration target point.

    Attributes:
        screen_x: Target X coordinate on screen.
        screen_y: Target Y coordinate on screen.
        head_yaw: Recorded head yaw at this point.
        head_pitch: Recorded head pitch at this point.
    """

    def __init__(self, screen_x: int, screen_y: int) -> None:
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.head_yaw: Optional[float] = None
        self.head_pitch: Optional[float] = None

    def record(self, yaw: float, pitch: float) -> None:
        self.head_yaw = yaw
        self.head_pitch = pitch


class CalibrationRoutine:
    """Manages the multi-point calibration procedure.

    Generates calibration target positions, collects head-pose samples
    at each target, and computes the mapping coefficients.

    Attributes:
        num_points: Number of calibration points (e.g., 9).
        hold_time_ms: Time the user must hold gaze at each point (ms).
        screen_width: Screen width in pixels.
        screen_height: Screen height in pixels.
        margin: Margin from screen edges in pixels.
    """

    def __init__(
        self,
        num_points: int = 9,
        hold_time_ms: int = 2000,
        screen_width: int = 1920,
        screen_height: int = 1080,
        margin: int = 100,
    ) -> None:
        self.num_points = num_points
        self.hold_time_ms = hold_time_ms
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin
        self._points: List[CalibrationPoint] = []
        self._mapping_coefficients: Optional[np.ndarray] = None
        self.generate_points()

    def generate_points(self) -> List[Tuple[int, int]]:
        self._points = []

        if self.num_points == 9:
            xs = [self.margin, self.screen_width // 2, self.screen_width - self.margin]
            ys = [self.margin, self.screen_height // 2, self.screen_height - self.margin]
            for y in ys:
                for x in xs:
                    self._points.append(CalibrationPoint(x, y))

        elif self.num_points == 4:
            corners = [
                (self.margin, self.margin),
                (self.screen_width - self.margin, self.margin),
                (self.margin, self.screen_height - self.margin),
                (self.screen_width - self.margin, self.screen_height - self.margin),
            ]
            for x, y in corners:
                self._points.append(CalibrationPoint(x, y))

        elif self.num_points == 5:
            positions = [
                (self.margin, self.margin),
                (self.screen_width - self.margin, self.margin),
                (self.margin, self.screen_height - self.margin),
                (self.screen_width - self.margin, self.screen_height - self.margin),
                (self.screen_width // 2, self.screen_height // 2),
            ]
            for x, y in positions:
                self._points.append(CalibrationPoint(x, y))

        else:
            cols = max(1, int(math.ceil(math.sqrt(self.num_points))))
            rows = max(1, int(math.ceil(self.num_points / cols)))
            x_step = (self.screen_width - 2 * self.margin) / max(1, cols - 1) if cols > 1 else 0
            y_step = (self.screen_height - 2 * self.margin) / max(1, rows - 1) if rows > 1 else 0
            count = 0
            for r in range(rows):
                for c in range(cols):
                    if count >= self.num_points:
                        break
                    x = self.margin + int(c * x_step) if cols > 1 else self.screen_width // 2
                    y = self.margin + int(r * y_step) if rows > 1 else self.screen_height // 2
                    self._points.append(CalibrationPoint(x, y))
                    count += 1

        return [(p.screen_x, p.screen_y) for p in self._points]

    def record_point(self, index: int, yaw: float, pitch: float) -> None:
        if index < 0 or index >= len(self._points):
            raise IndexError(f"Point index {index} out of range [0, {len(self._points) - 1}]")
        self._points[index].record(yaw, pitch)

    def compute_mapping(self) -> np.ndarray:
        recorded = [p for p in self._points if p.head_yaw is not None and p.head_pitch is not None]

        A = np.array([[p.head_yaw, p.head_pitch, 1.0] for p in recorded])
        B_x = np.array([[p.screen_x] for p in recorded])
        B_y = np.array([[p.screen_y] for p in recorded])

        coeffs_x = np.linalg.lstsq(A, B_x, rcond=None)[0]
        coeffs_y = np.linalg.lstsq(A, B_y, rcond=None)[0]

        self._mapping_coefficients = np.vstack([coeffs_x.T, coeffs_y.T])
        return self._mapping_coefficients

    def map_to_screen(self, yaw: float, pitch: float) -> Tuple[int, int]:
        if self._mapping_coefficients is None:
            raise ValueError("Calibration not computed")

        input_vec = np.array([yaw, pitch, 1.0])
        screen_pos = self._mapping_coefficients @ input_vec

        x = max(0, min(self.screen_width - 1, screen_pos[0]))
        y = max(0, min(self.screen_height - 1, screen_pos[1]))
        return (int(x), int(y))

    def save_calibration(self, filepath: str) -> None:
        data: Dict = {
            "coefficients": self._mapping_coefficients.tolist() if self._mapping_coefficients is not None else None,
            "points": [
                {
                    "screen_x": p.screen_x,
                    "screen_y": p.screen_y,
                    "head_yaw": p.head_yaw,
                    "head_pitch": p.head_pitch,
                }
                for p in self._points
            ],
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_calibration(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            data = json.load(f)

        if data["coefficients"] is not None:
            self._mapping_coefficients = np.array(data["coefficients"])
        else:
            self._mapping_coefficients = None

        self._points = []
        for pd in data["points"]:
            point = CalibrationPoint(pd["screen_x"], pd["screen_y"])
            if pd["head_yaw"] is not None and pd["head_pitch"] is not None:
                point.record(pd["head_yaw"], pd["head_pitch"])
            self._points.append(point)

        self.screen_width = data["screen_width"]
        self.screen_height = data["screen_height"]

    def is_complete(self) -> bool:
        return all(p.head_yaw is not None and p.head_pitch is not None for p in self._points)


if __name__ == "__main__":
    import tempfile
    import os
    import random

    routine = CalibrationRoutine(num_points=9, screen_width=1920, screen_height=1080, margin=100)
    points = [(p.screen_x, p.screen_y) for p in routine._points]
    print("Generated calibration points:")
    for i, (x, y) in enumerate(points):
        print(f"  Point {i}: ({x}, {y})")

    random.seed(42)
    for i, (sx, sy) in enumerate(points):
        yaw = (sx - 960) / 50.0 + random.gauss(0, 0.1)
        pitch = (sy - 540) / 50.0 + random.gauss(0, 0.1)
        routine.record_point(i, yaw, pitch)

    print(f"\nAll points recorded: {routine.is_complete()}")

    coefficients = routine.compute_mapping()
    print(f"\nMapping coefficients:\n{coefficients}")

    test_cases = [(0.0, 0.0), (-17.2, -8.8), (17.2, 8.8)]
    print("\nMapping test:")
    for yaw, pitch in test_cases:
        sx, sy = routine.map_to_screen(yaw, pitch)
        print(f"  yaw={yaw:6.1f}, pitch={pitch:6.1f} -> screen=({sx}, {sy})")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name
    routine.save_calibration(tmp_path)
    print(f"\nCalibration saved to {tmp_path}")

    routine2 = CalibrationRoutine(num_points=9, screen_width=1920, screen_height=1080, margin=100)
    routine2.load_calibration(tmp_path)
    print("Calibration loaded back.")

    for yaw, pitch in test_cases:
        sx, sy = routine2.map_to_screen(yaw, pitch)
        print(f"  yaw={yaw:6.1f}, pitch={pitch:6.1f} -> screen=({sx}, {sy})")

    os.unlink(tmp_path)
    print("\nCalibration module test completed.")
