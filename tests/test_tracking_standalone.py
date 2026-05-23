"""Standalone integration test for the tracking module.

Runs face detection, head pose estimation, and smoothing pipeline
together using a webcam or synthetic data when no camera is available.
"""

import sys
import time
import math
import random
from typing import Tuple

import numpy as np

sys.path.insert(0, ".")

from src.tracking.face_detector import FaceDetector
from src.tracking.head_pose_estimator import HeadPoseEstimator
from src.tracking.smoothing import SmoothingPipeline
from src.tracking.calibration import CalibrationRoutine


def test_smoothing_pipeline() -> bool:
    print("\n=== Test 1: Smoothing Pipeline ===")
    pipeline = SmoothingPipeline(
        process_noise=1e-4,
        measurement_noise=1e-2,
        ema_alpha=0.3,
        deadzone_radius=3.0,
    )

    raw_points = []
    smoothed_points = []
    for i in range(50):
        raw_x = i * 10.0
        raw_y = 100.0 + 50.0 * math.sin(i * 0.3) + random.gauss(0, 10)
        sx, sy = pipeline.smooth(raw_x, raw_y)
        raw_points.append((raw_x, raw_y))
        smoothed_points.append((sx, sy))

    raw_var = np.var([p[1] for p in raw_points])
    smooth_var = np.var([p[1] for p in smoothed_points])
    reduction = (1 - smooth_var / raw_var) * 100 if raw_var > 0 else 0

    print(f"  Raw Y variance:      {raw_var:.1f}")
    print(f"  Smoothed Y variance: {smooth_var:.1f}")
    print(f"  Variance reduction:  {reduction:.1f}%")

    pipeline.reset()
    rx, ry = pipeline.smooth(100.0, 200.0)
    print(f"  After reset, first point: ({rx:.1f}, {ry:.1f})")

    passed = smooth_var < raw_var
    print(f"  Result: {'PASS' if passed else 'FAIL'}")
    return passed


def test_head_pose_estimator() -> bool:
    print("\n=== Test 2: Head Pose Estimator ===")
    estimator = HeadPoseEstimator(640, 480)

    landmarks = np.zeros((478, 3), dtype=np.float64)
    landmarks[1] = [0.50, 0.50, 0.0]
    landmarks[33] = [0.35, 0.35, -0.02]
    landmarks[263] = [0.65, 0.35, -0.02]
    landmarks[61] = [0.40, 0.65, -0.02]
    landmarks[291] = [0.60, 0.65, -0.02]
    landmarks[199] = [0.50, 0.75, -0.01]

    yaw, pitch, roll = estimator.estimate(landmarks)
    print(f"  Centered face -> Yaw: {yaw:.1f}, Pitch: {pitch:.1f}, Roll: {roll:.1f}")

    landmarks_left = landmarks.copy()
    landmarks_left[1] = [0.40, 0.50, 0.0]
    landmarks_left[33] = [0.25, 0.35, -0.02]
    landmarks_left[263] = [0.55, 0.35, -0.02]
    yaw2, pitch2, roll2 = estimator.estimate(landmarks_left)
    print(f"  Left-turned face -> Yaw: {yaw2:.1f}, Pitch: {pitch2:.1f}, Roll: {roll2:.1f}")

    rvec = estimator.get_rotation_vector(landmarks)
    tvec = estimator.get_translation_vector(landmarks)
    print(f"  Rotation vector available: {rvec is not None}")
    print(f"  Translation vector available: {tvec is not None}")

    passed = rvec is not None and tvec is not None
    print(f"  Result: {'PASS' if passed else 'FAIL'}")
    return passed


def test_calibration() -> bool:
    print("\n=== Test 3: Calibration Routine ===")
    cal = CalibrationRoutine(
        num_points=9,
        screen_width=1920,
        screen_height=1080,
        margin=100,
    )

    points = [(p.screen_x, p.screen_y) for p in cal._points]
    print(f"  Generated {len(points)} calibration points")
    assert len(points) == 9, f"Expected 9, got {len(points)}"

    for i, p in enumerate(cal._points):
        yaw = (p.screen_x - 960) / 50.0 + random.gauss(0, 0.05)
        pitch = (p.screen_y - 540) / 50.0 + random.gauss(0, 0.05)
        cal.record_point(i, yaw, pitch)

    assert cal.is_complete(), "Calibration should be complete"
    print("  All points recorded: True")

    coeffs = cal.compute_mapping()
    print(f"  Mapping coefficients shape: {coeffs.shape}")

    test_cases = [
        (0.0, 0.0, 960, 540),
        (-17.2, -8.8, 100, 100),
        (17.2, 8.8, 1820, 980),
    ]

    max_error = 0
    for yaw, pitch, expected_x, expected_y in test_cases:
        sx, sy = cal.map_to_screen(yaw, pitch)
        error = math.sqrt((sx - expected_x) ** 2 + (sy - expected_y) ** 2)
        max_error = max(max_error, error)
        print(f"  map({yaw:.1f}, {pitch:.1f}) -> ({sx}, {sy}) [expected ~({expected_x}, {expected_y}), error: {error:.1f}px]")

    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp_path = f.name
    cal.save_calibration(tmp_path)
    cal2 = CalibrationRoutine(num_points=9, screen_width=1920, screen_height=1080)
    cal2.load_calibration(tmp_path)
    sx2, sy2 = cal2.map_to_screen(0.0, 0.0)
    os.unlink(tmp_path)
    print(f"  Save/load round-trip: map(0,0) -> ({sx2}, {sy2})")

    passed = max_error < 50
    print(f"  Max mapping error: {max_error:.1f}px")
    print(f"  Result: {'PASS' if passed else 'FAIL'}")
    return passed


def test_face_detector_init() -> bool:
    print("\n=== Test 4: FaceDetector Initialization ===")
    try:
        detector = FaceDetector(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_faces=1,
        )
        print(f"  FaceDetector created: True")
        print(f"  Face mesh initialized: {detector._face_mesh is not None}")
        detector.release()
        print(f"  Released successfully: True")
        print(f"  Result: PASS")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        print(f"  Result: FAIL")
        return False


def test_ear_calculation() -> bool:
    print("\n=== Test 5: Eye Aspect Ratio (EAR) ===")
    try:
        detector = FaceDetector()
        landmarks = np.zeros((478, 3), dtype=np.float64)

        landmarks[33] = [0.30, 0.40, 0.0]
        landmarks[160] = [0.33, 0.38, 0.0]
        landmarks[158] = [0.36, 0.38, 0.0]
        landmarks[133] = [0.39, 0.40, 0.0]
        landmarks[153] = [0.36, 0.42, 0.0]
        landmarks[144] = [0.33, 0.42, 0.0]

        ear_open = detector.get_ear(landmarks, "left")
        print(f"  EAR (eyes open):  {ear_open:.3f}")

        landmarks[160] = [0.33, 0.40, 0.0]
        landmarks[158] = [0.36, 0.40, 0.0]
        landmarks[153] = [0.36, 0.40, 0.0]
        landmarks[144] = [0.33, 0.40, 0.0]

        ear_closed = detector.get_ear(landmarks, "left")
        print(f"  EAR (eyes closed): {ear_closed:.3f}")

        detector.release()

        passed = ear_open > ear_closed and ear_closed < 0.1
        print(f"  Open > Closed: {ear_open > ear_closed}")
        print(f"  Result: {'PASS' if passed else 'FAIL'}")
        return passed
    except Exception as e:
        print(f"  Error: {e}")
        print(f"  Result: FAIL")
        return False


def main() -> None:
    print("=" * 60)
    print("  HEAD TRACKING MODULE - STANDALONE TESTS")
    print("=" * 60)

    results = []
    results.append(("Smoothing Pipeline", test_smoothing_pipeline()))
    results.append(("Head Pose Estimator", test_head_pose_estimator()))
    results.append(("Calibration Routine", test_calibration()))
    results.append(("FaceDetector Init", test_face_detector_init()))
    results.append(("EAR Calculation", test_ear_calculation()))

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print(f"\n  Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 60)

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
