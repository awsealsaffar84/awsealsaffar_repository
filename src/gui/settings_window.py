"""Settings window for configuring system parameters."""

import json
import os
from typing import Dict, Any, Optional, Callable

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QSlider, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
    QPushButton, QGroupBox, QFormLayout, QScrollArea, QApplication,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SettingsWindow(QWidget):
    """GUI window for adjusting all configurable system parameters."""

    settings_saved = pyqtSignal(dict)

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        config_path: str = "config/default_config.json",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.config = config if config is not None else self._load_default_config(config_path)
        self.config_path = config_path
        self.on_save: Optional[Callable[[Dict[str, Any]], None]] = None
        self._visible: bool = False
        self._defaults: Dict[str, Any] = json.loads(json.dumps(self.config))
        self._init_ui()

    def _load_default_config(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _init_ui(self) -> None:
        self.setWindowTitle("Settings — إعدادات النظام")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(500, 600)
        self.setStyleSheet("background-color: #1E1E2E; color: #CDD6F4;")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)

        title = QLabel("⚙ System Settings — إعدادات النظام")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #89B4FA; padding: 8px;")
        main_layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #45475A; }"
            "QTabBar::tab { background: #313244; color: #CDD6F4; padding: 8px 16px; }"
            "QTabBar::tab:selected { background: #45475A; color: #89B4FA; }"
        )
        main_layout.addWidget(tabs)

        tabs.addTab(self._create_camera_tab(), "📷 Camera")
        tabs.addTab(self._create_tracking_tab(), "🎯 Tracking")
        tabs.addTab(self._create_smoothing_tab(), "〰 Smoothing")
        tabs.addTab(self._create_mouse_tab(), "🖱 Mouse")
        tabs.addTab(self._create_click_tab(), "👆 Click")
        tabs.addTab(self._create_ui_tab(), "🎨 UI")

        # Bottom buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet(
            "QPushButton { background-color: #A6E3A1; color: #1E1E2E; "
            "border-radius: 6px; padding: 8px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #94E2D5; }"
        )
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)

        reset_btn = QPushButton("🔄 Reset Defaults")
        reset_btn.setStyleSheet(
            "QPushButton { background-color: #F38BA8; color: #1E1E2E; "
            "border-radius: 6px; padding: 8px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #EBA0AC; }"
        )
        reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(reset_btn)

        close_btn = QPushButton("✕ Close")
        close_btn.setStyleSheet(
            "QPushButton { background-color: #45475A; color: #CDD6F4; "
            "border-radius: 6px; padding: 8px 20px; }"
            "QPushButton:hover { background-color: #585B70; }"
        )
        close_btn.clicked.connect(self.hide)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)

    def _create_camera_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        cam = self.config.get("camera", {})

        self._cam_index = QSpinBox()
        self._cam_index.setRange(0, 10)
        self._cam_index.setValue(cam.get("index", 0))
        layout.addRow("Camera Index:", self._cam_index)

        self._cam_width = QSpinBox()
        self._cam_width.setRange(320, 1920)
        self._cam_width.setValue(cam.get("width", 640))
        layout.addRow("Width:", self._cam_width)

        self._cam_height = QSpinBox()
        self._cam_height.setRange(240, 1080)
        self._cam_height.setValue(cam.get("height", 480))
        layout.addRow("Height:", self._cam_height)

        self._cam_fps = QSpinBox()
        self._cam_fps.setRange(10, 120)
        self._cam_fps.setValue(cam.get("fps", 30))
        layout.addRow("FPS:", self._cam_fps)

        return widget

    def _create_tracking_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        tracking = self.config.get("tracking", {})

        self._track_complexity = QComboBox()
        self._track_complexity.addItems(["0 (Lite)", "1 (Full)"])
        self._track_complexity.setCurrentIndex(tracking.get("model_complexity", 1))
        layout.addRow("Model Complexity:", self._track_complexity)

        self._track_detect_conf = QDoubleSpinBox()
        self._track_detect_conf.setRange(0.1, 1.0)
        self._track_detect_conf.setSingleStep(0.05)
        self._track_detect_conf.setValue(tracking.get("min_detection_confidence", 0.5))
        layout.addRow("Detection Confidence:", self._track_detect_conf)

        self._track_track_conf = QDoubleSpinBox()
        self._track_track_conf.setRange(0.1, 1.0)
        self._track_track_conf.setSingleStep(0.05)
        self._track_track_conf.setValue(tracking.get("min_tracking_confidence", 0.5))
        layout.addRow("Tracking Confidence:", self._track_track_conf)

        return widget

    def _create_smoothing_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        sm = self.config.get("smoothing", {})

        self._sm_kalman_q = QDoubleSpinBox()
        self._sm_kalman_q.setRange(0.00001, 0.1)
        self._sm_kalman_q.setDecimals(5)
        self._sm_kalman_q.setValue(sm.get("kalman_process_noise", 0.0001))
        layout.addRow("Kalman Process Noise (Q):", self._sm_kalman_q)

        self._sm_kalman_r = QDoubleSpinBox()
        self._sm_kalman_r.setRange(0.001, 1.0)
        self._sm_kalman_r.setDecimals(4)
        self._sm_kalman_r.setValue(sm.get("kalman_measurement_noise", 0.01))
        layout.addRow("Kalman Measurement Noise (R):", self._sm_kalman_r)

        self._sm_ema = QDoubleSpinBox()
        self._sm_ema.setRange(0.05, 1.0)
        self._sm_ema.setSingleStep(0.05)
        self._sm_ema.setValue(sm.get("ema_alpha", 0.3))
        layout.addRow("EMA Alpha:", self._sm_ema)

        self._sm_deadzone = QDoubleSpinBox()
        self._sm_deadzone.setRange(0.0, 20.0)
        self._sm_deadzone.setValue(sm.get("deadzone_radius", 3.0))
        layout.addRow("Deadzone Radius (px):", self._sm_deadzone)

        return widget

    def _create_mouse_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        mc = self.config.get("mouse_control", {})

        self._mouse_sens_x = QDoubleSpinBox()
        self._mouse_sens_x.setRange(0.5, 5.0)
        self._mouse_sens_x.setSingleStep(0.1)
        self._mouse_sens_x.setValue(mc.get("sensitivity_x", 1.5))
        layout.addRow("Sensitivity X:", self._mouse_sens_x)

        self._mouse_sens_y = QDoubleSpinBox()
        self._mouse_sens_y.setRange(0.5, 5.0)
        self._mouse_sens_y.setSingleStep(0.1)
        self._mouse_sens_y.setValue(mc.get("sensitivity_y", 1.5))
        layout.addRow("Sensitivity Y:", self._mouse_sens_y)

        self._mouse_accel = QDoubleSpinBox()
        self._mouse_accel.setRange(1.0, 3.0)
        self._mouse_accel.setSingleStep(0.1)
        self._mouse_accel.setValue(mc.get("acceleration", 1.2))
        layout.addRow("Acceleration:", self._mouse_accel)

        return widget

    def _create_click_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        ce = self.config.get("click_engine", {})

        self._click_dwell = QSpinBox()
        self._click_dwell.setRange(300, 3000)
        self._click_dwell.setSingleStep(100)
        self._click_dwell.setValue(ce.get("dwell_time_ms", 1000))
        self._click_dwell.setSuffix(" ms")
        layout.addRow("Dwell Time:", self._click_dwell)

        self._click_radius = QDoubleSpinBox()
        self._click_radius.setRange(10.0, 100.0)
        self._click_radius.setValue(ce.get("dwell_radius", 30.0))
        self._click_radius.setSuffix(" px")
        layout.addRow("Dwell Radius:", self._click_radius)

        self._click_ear = QDoubleSpinBox()
        self._click_ear.setRange(0.10, 0.40)
        self._click_ear.setSingleStep(0.01)
        self._click_ear.setValue(ce.get("blink_threshold_ear", 0.21))
        layout.addRow("Blink EAR Threshold:", self._click_ear)

        self._click_frames = QSpinBox()
        self._click_frames.setRange(1, 10)
        self._click_frames.setValue(ce.get("blink_consecutive_frames", 3))
        layout.addRow("Blink Consecutive Frames:", self._click_frames)

        return widget

    def _create_ui_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)
        ui = self.config.get("ui", {})

        self._ui_opacity = QDoubleSpinBox()
        self._ui_opacity.setRange(0.3, 1.0)
        self._ui_opacity.setSingleStep(0.05)
        self._ui_opacity.setValue(ui.get("overlay_opacity", 0.85))
        layout.addRow("Overlay Opacity:", self._ui_opacity)

        self._ui_theme = QComboBox()
        self._ui_theme.addItems(["dark", "light"])
        current_theme = ui.get("theme", "dark")
        self._ui_theme.setCurrentText(current_theme)
        layout.addRow("Theme:", self._ui_theme)

        self._ui_font_size = QSpinBox()
        self._ui_font_size.setRange(10, 24)
        self._ui_font_size.setValue(ui.get("font_size", 14))
        layout.addRow("Font Size:", self._ui_font_size)

        return widget

    def _collect_config(self) -> Dict[str, Any]:
        return {
            "camera": {
                "index": self._cam_index.value(),
                "width": self._cam_width.value(),
                "height": self._cam_height.value(),
                "fps": self._cam_fps.value(),
            },
            "tracking": {
                "model_complexity": self._track_complexity.currentIndex(),
                "min_detection_confidence": self._track_detect_conf.value(),
                "min_tracking_confidence": self._track_track_conf.value(),
                "max_faces": self.config.get("tracking", {}).get("max_faces", 1),
            },
            "smoothing": {
                "kalman_process_noise": self._sm_kalman_q.value(),
                "kalman_measurement_noise": self._sm_kalman_r.value(),
                "ema_alpha": self._sm_ema.value(),
                "deadzone_radius": self._sm_deadzone.value(),
            },
            "mouse_control": {
                "sensitivity_x": self._mouse_sens_x.value(),
                "sensitivity_y": self._mouse_sens_y.value(),
                "acceleration": self._mouse_accel.value(),
                "smoothing_enabled": True,
            },
            "click_engine": {
                "dwell_time_ms": self._click_dwell.value(),
                "dwell_radius": self._click_radius.value(),
                "blink_threshold_ear": self._click_ear.value(),
                "blink_consecutive_frames": self._click_frames.value(),
            },
            "gestures": self.config.get("gestures", {}),
            "keyboard": self.config.get("keyboard", {}),
            "emergency_panel": self.config.get("emergency_panel", {}),
            "evaluation": self.config.get("evaluation", {}),
            "ui": {
                "overlay_opacity": self._ui_opacity.value(),
                "theme": self._ui_theme.currentText(),
                "font_size": self._ui_font_size.value(),
            },
        }

    def _on_save(self) -> None:
        self.config = self._collect_config()
        self.save_config()
        if self.on_save:
            self.on_save(self.config)
        self.settings_saved.emit(self.config)

    def show(self) -> None:
        self._visible = True
        super().show()

    def hide(self) -> None:
        self._visible = False
        super().hide()

    def load_config(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        return self.config

    def save_config(self, path: Optional[str] = None) -> None:
        target = path or self.config_path
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_value(self, key: str) -> Any:
        parts = key.split(".")
        obj = self.config
        for part in parts:
            if isinstance(obj, dict):
                obj = obj.get(part)
            else:
                return None
        return obj

    def set_value(self, key: str, value: Any) -> None:
        parts = key.split(".")
        obj = self.config
        for part in parts[:-1]:
            if part not in obj:
                obj[part] = {}
            obj = obj[part]
        obj[parts[-1]] = value

    def reset_defaults(self) -> None:
        self.config = json.loads(json.dumps(self._defaults))
        # Reload UI values from defaults
        cam = self.config.get("camera", {})
        self._cam_index.setValue(cam.get("index", 0))
        self._cam_width.setValue(cam.get("width", 640))
        self._cam_height.setValue(cam.get("height", 480))
        self._cam_fps.setValue(cam.get("fps", 30))

    def is_visible(self) -> bool:
        return self._visible


if __name__ == "__main__":
    import sys
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication(sys.argv)
    settings = SettingsWindow(config_path="config/default_config.json")

    print(f"Config loaded: {len(settings.config)} sections")
    print(f"Camera width: {settings.get_value('camera.width')}")
    print(f"EMA alpha: {settings.get_value('smoothing.ema_alpha')}")

    settings.set_value("mouse_control.sensitivity_x", 2.0)
    print(f"After set: sensitivity_x = {settings.get_value('mouse_control.sensitivity_x')}")

    settings.show()
    print(f"Visible: {settings.is_visible()}")
    settings.hide()
    print(f"Hidden: {not settings.is_visible()}")

    print("SettingsWindow test completed.")
