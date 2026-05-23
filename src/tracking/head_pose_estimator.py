"""SolvePnP-based head pose estimation for yaw, pitch, and roll angles."""

from math import atan2, degrees, sqrt
from typing import Optional, Tuple

import cv2
import numpy as np


class HeadPoseEstimator:
    """Estimates head orientation (yaw, pitch, roll) from facial landmarks.

    Uses OpenCV's solvePnP with a generic 3-D face model to compute
    rotation and translation vectors, then converts to Euler angles.

    Attributes:
        camera_matrix: Intrinsic camera matrix (3x3).
        dist_coeffs: Distortion coefficients.
    """

    LANDMARK_INDICES: Tuple[int, ...] = (1, 33, 263, 61, 291, 199)

    def __init__(
        self,
        frame_width: int = 640,
        frame_height: int = 480,
    ) -> None:
        self.frame_width: int = frame_width
        self.frame_height: int = frame_height
        self.camera_matrix: np.ndarray = self._build_camera_matrix()
        self.dist_coeffs: np.ndarray = np.zeros((4, 1), dtype=np.float64)
        self._model_points: np.ndarray = self._build_3d_model_points()
        self._prev_rvec: Optional[np.ndarray] = None
        self._prev_tvec: Optional[np.ndarray] = None

    def _build_camera_matrix(self) -> np.ndarray:
        focal_length: float = float(self.frame_width)
        center_x: float = self.frame_width / 2.0
        center_y: float = self.frame_height / 2.0
        return np.array(
            [
                [focal_length, 0.0, center_x],
                [0.0, focal_length, center_y],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )

    def _build_3d_model_points(self) -> np.ndarray:
        return np.array(
            [
                [0.0, 0.0, 0.0],          # Nose tip
                [-225.0, 170.0, -135.0],   # Left eye left corner
                [225.0, 170.0, -135.0],    # Right eye right corner
                [-150.0, -150.0, -125.0],  # Left mouth corner
                [150.0, -150.0, -125.0],   # Right mouth corner
                [0.0, -330.0, -65.0],      # Chin
            ],
            dtype=np.float64,
        )

    def _solve_pnp(
        self, landmarks: np.ndarray
    ) -> Tuple[bool, Optional[np.ndarray], Optional[np.ndarray]]:
        image_points: np.ndarray = np.array(
            [
                [
                    landmarks[idx, 0] * self.frame_width,
                    landmarks[idx, 1] * self.frame_height,
                ]
                for idx in self.LANDMARK_INDICES
            ],
            dtype=np.float64,
        )

        kwargs = {
            "objectPoints": self._model_points,
            "imagePoints": image_points,
            "cameraMatrix": self.camera_matrix,
            "distCoeffs": self.dist_coeffs,
            "flags": cv2.SOLVEPNP_ITERATIVE,
        }

        if self._prev_rvec is not None:
            kwargs["useExtrinsicGuess"] = True
            kwargs["rvec"] = self._prev_rvec.copy()
            kwargs["tvec"] = self._prev_tvec.copy()

        success, rvec, tvec = cv2.solvePnP(**kwargs)

        if success:
            self._prev_rvec = rvec
            self._prev_tvec = tvec
            return True, rvec, tvec

        return False, None, None

    def estimate(
        self, landmarks: np.ndarray
    ) -> Tuple[float, float, float]:
        success, rvec, tvec = self._solve_pnp(landmarks)

        if not success:
            return (0.0, 0.0, 0.0)

        rotation_matrix, _ = cv2.Rodrigues(rvec)
        R: np.ndarray = rotation_matrix

        pitch: float = degrees(atan2(-R[2, 0], sqrt(R[2, 1] ** 2 + R[2, 2] ** 2)))
        yaw: float = degrees(atan2(R[2, 1], R[2, 2]))
        roll: float = degrees(atan2(R[1, 0], R[0, 0]))

        return (yaw, pitch, roll)

    def get_rotation_vector(
        self, landmarks: np.ndarray
    ) -> Optional[np.ndarray]:
        if self._prev_rvec is not None:
            return self._prev_rvec

        success, rvec, _ = self._solve_pnp(landmarks)
        if success:
            return rvec
        return None

    def get_translation_vector(
        self, landmarks: np.ndarray
    ) -> Optional[np.ndarray]:
        return self._prev_tvec


if __name__ == "__main__":
    print("HeadPoseEstimator module -- standalone test")

    estimator = HeadPoseEstimator(640, 480)

    fake_landmarks: np.ndarray = np.full((478, 3), 0.5, dtype=np.float64)
    fake_landmarks[1] = [0.50, 0.45, 0.0]    # Nose tip
    fake_landmarks[33] = [0.35, 0.35, 0.0]   # Left eye left corner
    fake_landmarks[263] = [0.65, 0.35, 0.0]  # Right eye right corner
    fake_landmarks[61] = [0.38, 0.60, 0.0]   # Left mouth corner
    fake_landmarks[291] = [0.62, 0.60, 0.0]  # Right mouth corner
    fake_landmarks[199] = [0.50, 0.75, 0.0]  # Chin

    yaw, pitch, roll = estimator.estimate(fake_landmarks)
    print(f"Yaw: {yaw:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}")

    print("Test completed.")
