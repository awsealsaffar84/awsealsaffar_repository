"""Main entry point for the Head-Tracking-Based Mouse Control System."""

import argparse
import json
import sys
import os
import time
from typing import Dict, Any, Optional, TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from src.tracking.face_detector import FaceDetector
    from src.tracking.head_pose_estimator import HeadPoseEstimator
    from src.tracking.smoothing import SmoothingPipeline
    from src.tracking.calibration import CalibrationRoutine
    from src.control.mouse_controller import MouseController
    from src.control.click_engine import ClickEngine
    from src.control.gesture_mapper import GestureMapper


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Head-Tracking-Based Mouse Control System for disabled users."
    )
    parser.add_argument(
        "--config", type=str, default="config/default_config.json",
        help="Path to the configuration JSON file.",
    )
    parser.add_argument(
        "--calibrate", action="store_true",
        help="Run calibration routine before starting.",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug mode with verbose logging.",
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run without GUI (tracking + mouse control only).",
    )
    parser.add_argument(
        "--simulated", action="store_true",
        help="Run in simulated mode (no camera, no real mouse).",
    )
    return parser.parse_args()


class HeadTrackingSystem:
    """Main application class integrating all system modules."""

    def __init__(self, config: Dict[str, Any], headless: bool = False, simulated: bool = False, debug: bool = False) -> None:
        self.config = config
        self.headless = headless
        self.simulated = simulated
        self.debug = debug
        self.running = False

        self._face_detector: Optional["FaceDetector"] = None
        self._pose_estimator: Optional["HeadPoseEstimator"] = None
        self._smoothing_pipeline: Optional["SmoothingPipeline"] = None
        self._calibration: Optional["CalibrationRoutine"] = None
        self._mouse_controller: Optional["MouseController"] = None
        self._click_engine: Optional["ClickEngine"] = None
        self._gesture_mapper: Optional["GestureMapper"] = None
        self._camera: Optional[cv2.VideoCapture] = None

        self._frame_count = 0
        self._fps = 0.0
        self._last_fps_time = time.time()

    def initialize(self) -> None:
        """Initialize all system modules."""
        from src.tracking.face_detector import FaceDetector
        from src.tracking.head_pose_estimator import HeadPoseEstimator
        from src.tracking.smoothing import SmoothingPipeline
        from src.tracking.calibration import CalibrationRoutine
        from src.control.mouse_controller import MouseController
        from src.control.click_engine import ClickEngine, ClickMode
        from src.control.gesture_mapper import GestureMapper

        cam_cfg = self.config.get("camera", {})
        track_cfg = self.config.get("tracking", {})
        smooth_cfg = self.config.get("smoothing", {})
        cal_cfg = self.config.get("calibration", {})
        mouse_cfg = self.config.get("mouse_control", {})
        click_cfg = self.config.get("click_engine", {})
        gest_cfg = self.config.get("gestures", {})

        # Face detection
        self._face_detector = FaceDetector(
            model_complexity=track_cfg.get("model_complexity", 1),
            min_detection_confidence=track_cfg.get("min_detection_confidence", 0.5),
            min_tracking_confidence=track_cfg.get("min_tracking_confidence", 0.5),
            max_num_faces=track_cfg.get("max_faces", 1),
        )

        # Pose estimation
        self._pose_estimator = HeadPoseEstimator(
            frame_width=cam_cfg.get("width", 640),
            frame_height=cam_cfg.get("height", 480),
        )

        # Smoothing
        self._smoothing_pipeline = SmoothingPipeline(
            process_noise=smooth_cfg.get("kalman_process_noise", 1e-4),
            measurement_noise=smooth_cfg.get("kalman_measurement_noise", 1e-2),
            ema_alpha=smooth_cfg.get("ema_alpha", 0.3),
            deadzone_radius=smooth_cfg.get("deadzone_radius", 3.0),
        )

        # Calibration
        self._calibration = CalibrationRoutine(
            num_points=cal_cfg.get("num_points", 9),
            hold_time_ms=cal_cfg.get("hold_time_ms", 2000),
            screen_width=mouse_cfg.get("screen_width", 1920),
            screen_height=mouse_cfg.get("screen_height", 1080),
            margin=cal_cfg.get("screen_margin", 100),
        )

        # Mouse controller
        self._mouse_controller = MouseController(
            sensitivity_x=mouse_cfg.get("sensitivity_x", 1.5),
            sensitivity_y=mouse_cfg.get("sensitivity_y", 1.5),
            acceleration=mouse_cfg.get("acceleration", 1.2),
            simulated=self.simulated,
        )
        self._mouse_controller.enable()

        # Click engine
        self._click_engine = ClickEngine(
            mode=ClickMode.BOTH,
            dwell_time_ms=click_cfg.get("dwell_time_ms", 1000),
            dwell_radius=click_cfg.get("dwell_radius", 30.0),
            ear_threshold=click_cfg.get("blink_threshold_ear", 0.21),
            consecutive_frames=click_cfg.get("blink_consecutive_frames", 3),
        )
        self._click_engine.on_click = self._on_click

        # Gesture mapper
        self._gesture_mapper = GestureMapper(
            nod_threshold=gest_cfg.get("nod_threshold", 15.0),
            shake_threshold=gest_cfg.get("shake_threshold", 20.0),
            tilt_threshold=gest_cfg.get("tilt_threshold", 15.0),
            cooldown_ms=gest_cfg.get("cooldown_ms", 1000),
        )

        # Camera
        if not self.simulated:
            self._camera = cv2.VideoCapture(cam_cfg.get("index", 0))
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_cfg.get("width", 640))
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_cfg.get("height", 480))
            self._camera.set(cv2.CAP_PROP_FPS, cam_cfg.get("fps", 30))

        if self.debug:
            print("[INIT] All modules initialized successfully.")

    def _on_click(self) -> None:
        if self._mouse_controller is None:
            return
        self._mouse_controller.click("left")
        if self.debug:
            print(f"[CLICK] at {self._mouse_controller.get_position()}")

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process a single frame through the full pipeline."""
        result = {
            "face_detected": False,
            "yaw": 0.0, "pitch": 0.0, "roll": 0.0,
            "cursor_x": 0, "cursor_y": 0,
            "ear": 0.0, "click": False,
        }

        assert self._face_detector is not None, "Call initialize() before process_frame()"
        assert self._pose_estimator is not None
        assert self._smoothing_pipeline is not None
        assert self._calibration is not None
        assert self._mouse_controller is not None
        assert self._click_engine is not None
        assert self._gesture_mapper is not None

        faces = self._face_detector.detect(frame)
        if faces is None or len(faces) == 0:
            return result

        landmarks = faces[0]
        result["face_detected"] = True

        # Head pose
        yaw, pitch, roll = self._pose_estimator.estimate(landmarks)
        result["yaw"] = yaw
        result["pitch"] = pitch
        result["roll"] = roll

        # Map to screen coordinates
        if self._calibration._mapping_coefficients is not None:
            sx, sy = self._calibration.map_to_screen(yaw, pitch)
        else:
            # Fallback: direct mapping from yaw/pitch to relative movement
            dx = yaw * self.config.get("mouse_control", {}).get("sensitivity_x", 1.5)
            dy = pitch * self.config.get("mouse_control", {}).get("sensitivity_y", 1.5)
            self._mouse_controller.move_relative(dx, dy)
            sx, sy = self._mouse_controller.get_position()

        # Smoothing
        sx_smooth, sy_smooth = self._smoothing_pipeline.smooth(float(sx), float(sy))
        result["cursor_x"] = int(sx_smooth)
        result["cursor_y"] = int(sy_smooth)

        # Move mouse
        self._mouse_controller.move_to(int(sx_smooth), int(sy_smooth))

        # EAR for blink detection
        ear = self._face_detector.get_average_ear(landmarks)
        result["ear"] = ear

        # Click detection
        timestamp_ms = time.time() * 1000
        clicked = self._click_engine.update(
            (sx_smooth, sy_smooth), timestamp_ms, ear=ear
        )
        result["click"] = clicked

        # Gesture detection
        gesture = self._gesture_mapper.update(yaw, pitch, roll, timestamp_ms)
        result["gesture"] = gesture.value

        # FPS calculation
        self._frame_count += 1
        now = time.time()
        elapsed = now - self._last_fps_time
        if elapsed >= 1.0:
            self._fps = self._frame_count / elapsed
            self._frame_count = 0
            self._last_fps_time = now

        return result

    def run_headless(self) -> None:
        """Run the system in headless mode (no GUI, just tracking + control)."""
        self.running = True
        print("[RUN] Starting headless mode. Press Ctrl+C to stop.")

        while self.running:
            if self._camera is None:
                break
            ret, frame = self._camera.read()
            if not ret:
                continue

            result = self.process_frame(frame)

            if self.debug and result["face_detected"]:
                print(
                    f"[FRAME] Yaw:{result['yaw']:.1f} Pitch:{result['pitch']:.1f} "
                    f"Cursor:({result['cursor_x']},{result['cursor_y']}) "
                    f"EAR:{result['ear']:.3f} FPS:{self._fps:.0f}"
                )

    def run_gui(self) -> None:
        """Run the system with full GUI overlay."""
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        from src.gui.main_overlay import MainOverlay
        from src.gui.virtual_keyboard import VirtualKeyboard
        from src.gui.emergency_panel import EmergencyPanel
        from src.gui.settings_window import SettingsWindow

        app = QApplication(sys.argv)

        # Create GUI components
        overlay = MainOverlay(
            opacity=self.config.get("ui", {}).get("overlay_opacity", 0.85),
            theme=self.config.get("ui", {}).get("theme", "dark"),
        )
        keyboard = VirtualKeyboard(
            key_size=self.config.get("keyboard", {}).get("key_size", 60),
            language=self.config.get("keyboard", {}).get("languages", ["en"])[0],
            dwell_highlight_ms=self.config.get("keyboard", {}).get("dwell_highlight_ms", 800),
        )
        emergency = EmergencyPanel(
            button_size=self.config.get("emergency_panel", {}).get("button_size", 120),
            alert_sound_enabled=self.config.get("emergency_panel", {}).get("alert_sound_enabled", True),
        )
        settings = SettingsWindow(config=self.config, config_path="config/default_config.json")

        # Register overlay callbacks
        overlay.register_callback("toggle_tracking", lambda: self._toggle_tracking(overlay))
        overlay.register_callback("keyboard", keyboard.toggle)
        overlay.register_callback("emergency", lambda: emergency.show() if not emergency.is_visible() else emergency.hide())
        overlay.register_callback("settings", lambda: settings.show() if not settings.is_visible() else settings.hide())
        overlay.register_callback("exit", lambda: self._shutdown(app))

        settings.on_save = lambda cfg: self._apply_config(cfg)

        overlay.show()
        overlay.set_tracking_status(True)

        # Frame processing timer
        def process_tick():
            if self._camera is None:
                return
            ret, frame = self._camera.read()
            if not ret:
                return
            result = self.process_frame(frame)
            overlay.update_fps(self._fps)
            if result["face_detected"]:
                keyboard.update_cursor_position(result["cursor_x"], result["cursor_y"])

        timer = QTimer()
        timer.timeout.connect(process_tick)
        timer.start(33)  # ~30fps

        self.running = True
        app.exec_()

    def _toggle_tracking(self, overlay) -> None:
        if self._mouse_controller is None:
            return
        if self._mouse_controller.is_enabled():
            self._mouse_controller.disable()
            overlay.set_tracking_status(False)
        else:
            self._mouse_controller.enable()
            overlay.set_tracking_status(True)

    def _apply_config(self, new_config: Dict[str, Any]) -> None:
        self.config = new_config
        if self.debug:
            print("[CONFIG] Settings updated.")

    def _shutdown(self, app) -> None:
        self.running = False
        if self._camera:
            self._camera.release()
        if self._face_detector:
            self._face_detector.release()
        app.quit()

    def shutdown(self) -> None:
        """Clean up all resources."""
        self.running = False
        if self._camera:
            self._camera.release()
        if self._face_detector:
            self._face_detector.release()


def main() -> None:
    """Application entry point."""
    args = parse_args()

    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)

    if args.debug:
        print(f"[DEBUG] Configuration loaded from: {args.config}")
        print(f"[DEBUG] Headless: {args.headless}, Simulated: {args.simulated}")

    system = HeadTrackingSystem(
        config=config,
        headless=args.headless,
        simulated=args.simulated,
        debug=args.debug,
    )

    system.initialize()

    if args.calibrate:
        print("[CALIBRATE] Calibration routine not yet interactive. Using defaults.")

    try:
        if args.headless:
            system.run_headless()
        else:
            system.run_gui()
    except KeyboardInterrupt:
        print("\n[EXIT] Shutting down...")
    finally:
        system.shutdown()


if __name__ == "__main__":
    main()
