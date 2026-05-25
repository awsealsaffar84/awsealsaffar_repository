"""MediaPipe Face Mesh wrapper for real-time facial landmark detection."""

from typing import Optional, List, Tuple

import cv2
import mediapipe as mp
import numpy as np


class FaceDetector:
    """Wraps MediaPipe Face Mesh to detect and return facial landmarks.

    Attributes:
        model_complexity: Complexity of the face mesh model (0 or 1).
        min_detection_confidence: Minimum confidence for face detection.
        min_tracking_confidence: Minimum confidence for landmark tracking.
        max_num_faces: Maximum number of faces to detect.
    """

    LEFT_EYE_INDICES: List[int] = [
        33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246,
    ]
    RIGHT_EYE_INDICES: List[int] = [
        362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398,
    ]

    def __init__(
        self,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        max_num_faces: int = 1,
    ) -> None:
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.max_num_faces = max_num_faces
        self._face_mesh = None
        self._use_tasks_api = not hasattr(mp, "solutions")
        self.initialize()

    def initialize(self) -> None:
        """Initialize MediaPipe Face Mesh (supports both old and new API)."""
        if self._use_tasks_api:
            self._init_tasks_api()
        else:
            self._face_mesh = mp.solutions.face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=self.max_num_faces,
                refine_landmarks=True,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )

    def _init_tasks_api(self) -> None:
        import os
        import urllib.request
        import tempfile
        from mediapipe.tasks.python import BaseOptions
        from mediapipe.tasks.python.vision import (
            FaceLandmarker, FaceLandmarkerOptions, RunningMode,
        )

        model_path = os.path.join(tempfile.gettempdir(), "face_landmarker_v2.task")
        if not os.path.exists(model_path):
            print("[INFO] Downloading MediaPipe face landmarker model...")
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            urllib.request.urlretrieve(url, model_path)
            print("[INFO] Model downloaded.")

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.IMAGE,
            num_faces=self.max_num_faces,
            min_face_detection_confidence=self.min_detection_confidence,
            min_face_presence_confidence=self.min_tracking_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self._face_mesh = FaceLandmarker.create_from_options(options)

    def detect(self, frame: np.ndarray) -> Optional[List[np.ndarray]]:
        """Detect facial landmarks in the given frame."""
        if self._use_tasks_api:
            return self._detect_tasks_api(frame)
        return self._detect_solutions_api(frame)

    def _detect_solutions_api(self, frame: np.ndarray) -> Optional[List[np.ndarray]]:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            return None
        faces: List[np.ndarray] = []
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array(
                [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark],
                dtype=np.float64,
            )
            faces.append(landmarks)
        return faces

    def _detect_tasks_api(self, frame: np.ndarray) -> Optional[List[np.ndarray]]:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results = self._face_mesh.detect(mp_image)
        if not results.face_landmarks:
            return None
        faces: List[np.ndarray] = []
        for face_landmarks in results.face_landmarks:
            landmarks = np.array(
                [(lm.x, lm.y, lm.z) for lm in face_landmarks],
                dtype=np.float64,
            )
            faces.append(landmarks)
        return faces

    def get_eye_landmarks(
        self, landmarks: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Extract left and right eye landmark subsets.

        Args:
            landmarks: Full face landmark array of shape (478, 3).

        Returns:
            Tuple of (left_eye_landmarks, right_eye_landmarks).
        """
        left_eye = landmarks[self.LEFT_EYE_INDICES]
        right_eye = landmarks[self.RIGHT_EYE_INDICES]
        return left_eye, right_eye

    def get_nose_tip(self, landmarks: np.ndarray) -> np.ndarray:
        """Extract the nose tip landmark coordinates.

        Args:
            landmarks: Full face landmark array of shape (478, 3).

        Returns:
            Nose tip coordinates as a 1-D array of shape (3,).
        """
        return landmarks[1]

    def get_ear(self, landmarks: np.ndarray, eye: str = "left") -> float:
        """Compute Eye Aspect Ratio (EAR) for blink detection.

        Args:
            landmarks: Full face landmark array of shape (478, 3).
            eye: Which eye to compute EAR for ("left" or "right").

        Returns:
            Eye Aspect Ratio as a float.
        """
        if eye == "left":
            p1, p2, p3, p4, p5, p6 = 33, 160, 158, 133, 153, 144
        else:
            p1, p2, p3, p4, p5, p6 = 362, 385, 387, 263, 380, 374

        vertical_a = np.linalg.norm(landmarks[p2] - landmarks[p6])
        vertical_b = np.linalg.norm(landmarks[p3] - landmarks[p5])
        horizontal = np.linalg.norm(landmarks[p1] - landmarks[p4])

        ear: float = (vertical_a + vertical_b) / (2.0 * horizontal)
        return ear

    def get_average_ear(self, landmarks: np.ndarray) -> float:
        """Compute the average EAR across both eyes.

        Args:
            landmarks: Full face landmark array of shape (478, 3).

        Returns:
            Average Eye Aspect Ratio as a float.
        """
        left_ear = self.get_ear(landmarks, eye="left")
        right_ear = self.get_ear(landmarks, eye="right")
        return (left_ear + right_ear) / 2.0

    def release(self) -> None:
        """Release MediaPipe resources."""
        if self._face_mesh is not None:
            try:
                self._face_mesh.close()
            except Exception:
                pass
            self._face_mesh = None


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect(frame)
        if faces is not None:
            for face_landmarks in faces:
                nose = detector.get_nose_tip(face_landmarks)
                print(
                    f"Landmarks: {face_landmarks.shape[0]}, "
                    f"Nose tip: ({nose[0]:.3f}, {nose[1]:.3f}, {nose[2]:.3f})"
                )
                cv2.putText(
                    frame,
                    f"Landmarks: {face_landmarks.shape[0]}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2,
                )

        cv2.imshow("Face Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    detector.release()
    cv2.destroyAllWindows()
