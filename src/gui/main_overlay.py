"""Always-on-top control bar overlay for the head-tracking system."""

import sys
from typing import Optional, Dict, Callable

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QApplication, QSizePolicy,
)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QMouseEvent


class MainOverlay(QWidget):
    """Transparent always-on-top toolbar providing quick system controls."""

    button_clicked = pyqtSignal(str)

    BUTTONS = [
        ("toggle_tracking", "⏯ Tracking"),
        ("keyboard", "⌨ Keyboard"),
        ("emergency", "🚨 Emergency"),
        ("settings", "⚙ Settings"),
        ("calibrate", "🎯 Calibrate"),
        ("exit", "✕ Exit"),
    ]

    def __init__(
        self,
        opacity: float = 0.85,
        position: str = "top",
        theme: str = "dark",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.opacity = opacity
        self.position = position
        self.theme = theme
        self._visible: bool = False
        self._callbacks: Dict[str, Optional[Callable[[], None]]] = {}
        self._tracking_active: bool = False
        self._drag_position: Optional[QPoint] = None

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setWindowOpacity(self.opacity)
        self._apply_theme()

        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 4, 8, 4)

        # Status indicator
        self._status_label = QLabel("● OFF")
        self._status_label.setFont(QFont("Arial", 11, QFont.Bold))
        self._status_label.setStyleSheet("color: #E74C3C; padding: 4px;")
        self._status_label.setFixedWidth(80)
        layout.addWidget(self._status_label)

        # FPS counter
        self._fps_label = QLabel("FPS: --")
        self._fps_label.setFont(QFont("Consolas", 10))
        self._fps_label.setStyleSheet("color: #95A5A6; padding: 4px;")
        self._fps_label.setFixedWidth(75)
        layout.addWidget(self._fps_label)

        # Separator
        layout.addSpacing(10)

        # Control buttons
        self._btn_widgets: Dict[str, QPushButton] = {}
        for btn_id, btn_label in self.BUTTONS:
            btn = QPushButton(btn_label)
            btn.setFont(QFont("Arial", 10))
            btn.setFixedHeight(32)
            btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, bid=btn_id: self._on_button(bid))
            layout.addWidget(btn)
            self._btn_widgets[btn_id] = btn

        self._apply_button_styles()

        # Size the overlay
        self.setFixedHeight(44)
        self.setMinimumWidth(700)
        self.adjustSize()

    def _apply_theme(self) -> None:
        if self.theme == "dark":
            self.setStyleSheet(
                "QWidget { background-color: #1A1A2E; border-bottom: 2px solid #333; }"
            )
        else:
            self.setStyleSheet(
                "QWidget { background-color: #F8F9FA; border-bottom: 2px solid #DDD; }"
            )

    def _apply_button_styles(self) -> None:
        if self.theme == "dark":
            style = (
                "QPushButton { background-color: #2C3E50; color: #ECF0F1; "
                "border: 1px solid #34495E; border-radius: 6px; padding: 4px 10px; }"
                "QPushButton:hover { background-color: #34495E; }"
                "QPushButton:pressed { background-color: #1ABC9C; }"
            )
            exit_style = (
                "QPushButton { background-color: #C0392B; color: white; "
                "border: 1px solid #E74C3C; border-radius: 6px; padding: 4px 10px; }"
                "QPushButton:hover { background-color: #E74C3C; }"
            )
        else:
            style = (
                "QPushButton { background-color: #ECF0F1; color: #2C3E50; "
                "border: 1px solid #BDC3C7; border-radius: 6px; padding: 4px 10px; }"
                "QPushButton:hover { background-color: #BDC3C7; }"
            )
            exit_style = (
                "QPushButton { background-color: #E74C3C; color: white; "
                "border: none; border-radius: 6px; padding: 4px 10px; }"
                "QPushButton:hover { background-color: #C0392B; }"
            )

        for btn_id, btn in self._btn_widgets.items():
            if btn_id == "exit":
                btn.setStyleSheet(exit_style)
            else:
                btn.setStyleSheet(style)

    def _on_button(self, button_id: str) -> None:
        self.button_clicked.emit(button_id)
        callback = self._callbacks.get(button_id)
        if callback:
            callback()

    def show(self) -> None:
        self._visible = True
        super().show()
        self._position_on_screen()

    def _position_on_screen(self) -> None:
        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            x = (geom.width() - self.width()) // 2
            if self.position == "top":
                y = 0
            else:
                y = geom.height() - self.height()
            self.move(x, y)

    def hide(self) -> None:
        self._visible = False
        super().hide()

    def set_opacity(self, opacity: float) -> None:
        self.opacity = max(0.0, min(1.0, opacity))
        self.setWindowOpacity(self.opacity)

    def set_tracking_status(self, active: bool) -> None:
        self._tracking_active = active
        if active:
            self._status_label.setText("● ON")
            self._status_label.setStyleSheet("color: #2ECC71; padding: 4px; font-weight: bold;")
        else:
            self._status_label.setText("● OFF")
            self._status_label.setStyleSheet("color: #E74C3C; padding: 4px; font-weight: bold;")

    def register_callback(self, button_name: str, callback: Callable[[], None]) -> None:
        self._callbacks[button_name] = callback

    def update_fps(self, fps: float) -> None:
        self._fps_label.setText(f"FPS: {fps:.0f}")
        if fps >= 25:
            self._fps_label.setStyleSheet("color: #2ECC71; padding: 4px;")
        elif fps >= 15:
            self._fps_label.setStyleSheet("color: #F39C12; padding: 4px;")
        else:
            self._fps_label.setStyleSheet("color: #E74C3C; padding: 4px;")

    def set_theme(self, theme: str) -> None:
        self.theme = theme
        self._apply_theme()
        self._apply_button_styles()

    def is_visible(self) -> bool:
        return self._visible

    # Drag support
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton and self._drag_position is not None:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_position = None


if __name__ == "__main__":
    import os
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication(sys.argv)
    overlay = MainOverlay(opacity=0.9, position="top", theme="dark")

    clicks = []
    overlay.register_callback("toggle_tracking", lambda: clicks.append("tracking"))
    overlay.register_callback("keyboard", lambda: clicks.append("keyboard"))
    overlay.register_callback("exit", lambda: clicks.append("exit"))

    overlay.show()
    print(f"Visible: {overlay.is_visible()}")
    overlay.set_tracking_status(True)
    overlay.update_fps(30.0)
    overlay.set_opacity(0.7)

    # Simulate button presses
    overlay._on_button("toggle_tracking")
    overlay._on_button("keyboard")
    overlay._on_button("exit")
    print(f"Callbacks fired: {clicks}")

    overlay.set_theme("light")
    overlay.set_tracking_status(False)
    overlay.update_fps(12.0)

    overlay.hide()
    print(f"After hide: {overlay.is_visible()}")
    print("MainOverlay test completed.")
