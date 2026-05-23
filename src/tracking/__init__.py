"""Tracking module: face detection, head pose estimation, smoothing, and calibration."""

from src.tracking.face_detector import FaceDetector
from src.tracking.head_pose_estimator import HeadPoseEstimator
from src.tracking.smoothing import KalmanFilter2D, EMAFilter, DeadzoneFilter, SmoothingPipeline
from src.tracking.calibration import CalibrationRoutine, CalibrationPoint

__all__ = [
    "FaceDetector",
    "HeadPoseEstimator",
    "KalmanFilter2D",
    "EMAFilter",
    "DeadzoneFilter",
    "SmoothingPipeline",
    "CalibrationRoutine",
    "CalibrationPoint",
]
