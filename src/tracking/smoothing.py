"""Kalman filter and exponential moving average (EMA) smoothing filters."""

import math
from typing import Tuple, Optional

import numpy as np


class KalmanFilter2D:
    """Two-dimensional Kalman filter for smoothing cursor position.

    Uses a constant-velocity model to predict and correct the
    (x, y) cursor position based on noisy head-pose measurements.

    Attributes:
        process_noise: Process noise covariance scalar.
        measurement_noise: Measurement noise covariance scalar.
    """

    def __init__(
        self,
        process_noise: float = 1e-4,
        measurement_noise: float = 1e-2,
    ) -> None:
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

        self._state: np.ndarray = np.zeros((4, 1))
        self._covariance: np.ndarray = np.eye(4) * 1000.0

        self._F: np.ndarray = np.array([
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

        self._H: np.ndarray = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ])

        self._Q: np.ndarray = np.eye(4) * process_noise
        self._R: np.ndarray = np.eye(2) * measurement_noise

        self._initialized: bool = False

    def predict(self) -> Tuple[float, float]:
        if not self._initialized:
            return (0.0, 0.0)

        self._state = self._F @ self._state
        self._covariance = self._F @ self._covariance @ self._F.T + self._Q

        return (float(self._state[0, 0]), float(self._state[1, 0]))

    def update(self, measurement: Tuple[float, float]) -> Tuple[float, float]:
        if not self._initialized:
            self._state[0, 0] = measurement[0]
            self._state[1, 0] = measurement[1]
            self._initialized = True
            return measurement

        self.predict()

        z = np.array([[measurement[0]], [measurement[1]]])
        y = z - self._H @ self._state
        S = self._H @ self._covariance @ self._H.T + self._R
        K = self._covariance @ self._H.T @ np.linalg.inv(S)

        self._state = self._state + K @ y
        self._covariance = (np.eye(4) - K @ self._H) @ self._covariance

        return (float(self._state[0, 0]), float(self._state[1, 0]))

    def reset(self) -> None:
        self._state = np.zeros((4, 1))
        self._covariance = np.eye(4) * 1000.0
        self._initialized = False


class EMAFilter:
    """Exponential Moving Average filter for single-axis smoothing.

    Attributes:
        alpha: Smoothing factor in (0, 1]. Lower values = more smoothing.
    """

    def __init__(self, alpha: float = 0.3) -> None:
        self.alpha = alpha
        self._value: Optional[float] = None

    def update(self, new_value: float) -> float:
        if self._value is None:
            self._value = new_value
            return new_value

        self._value = self.alpha * new_value + (1.0 - self.alpha) * self._value
        return self._value

    def reset(self) -> None:
        self._value = None


class DeadzoneFilter:
    """Applies a deadzone to suppress small jittery movements.

    Movements smaller than the deadzone radius are ignored.

    Attributes:
        radius: Minimum movement threshold in pixels.
    """

    def __init__(self, radius: float = 3.0) -> None:
        self.radius = radius
        self._last_position: Optional[Tuple[float, float]] = None

    def apply(self, position: Tuple[float, float]) -> Tuple[float, float]:
        if self._last_position is None:
            self._last_position = position
            return position

        dx = position[0] - self._last_position[0]
        dy = position[1] - self._last_position[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.radius:
            return self._last_position

        self._last_position = position
        return position

    def reset(self) -> None:
        self._last_position = None


class SmoothingPipeline:
    """Combines Kalman filter, EMA, and deadzone into a single pipeline."""

    def __init__(
        self,
        process_noise: float = 1e-4,
        measurement_noise: float = 1e-2,
        ema_alpha: float = 0.3,
        deadzone_radius: float = 3.0,
    ) -> None:
        self._kalman = KalmanFilter2D(process_noise, measurement_noise)
        self._ema_x = EMAFilter(ema_alpha)
        self._ema_y = EMAFilter(ema_alpha)
        self._deadzone = DeadzoneFilter(deadzone_radius)

    def smooth(self, x: float, y: float) -> Tuple[float, float]:
        kx, ky = self._kalman.update((x, y))
        ex = self._ema_x.update(kx)
        ey = self._ema_y.update(ky)
        return self._deadzone.apply((ex, ey))

    def reset(self) -> None:
        self._kalman.reset()
        self._ema_x.reset()
        self._ema_y.reset()
        self._deadzone.reset()


if __name__ == "__main__":
    np.random.seed(42)

    pipeline = SmoothingPipeline()

    raw_points: list[Tuple[float, float]] = []
    smoothed_points: list[Tuple[float, float]] = []

    for i in range(50):
        raw_x = float(i * 10)
        raw_y = 100.0 + 50.0 * math.sin(i * 0.3) + np.random.normal(0, 5)
        raw_points.append((raw_x, raw_y))
        sx, sy = pipeline.smooth(raw_x, raw_y)
        smoothed_points.append((sx, sy))

    for i in range(10):
        rx, ry = raw_points[i]
        sx, sy = smoothed_points[i]
        print(f"Raw: ({rx:8.2f}, {ry:8.2f})  Smoothed: ({sx:8.2f}, {sy:8.2f})")

    print("Smoothing pipeline test completed.")
