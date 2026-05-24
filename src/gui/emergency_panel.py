"""Image-based emergency panel for expressing needs, pain, and alerts."""

import os
import time
from typing import Optional, List, Dict, Callable, Tuple

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout,
    QApplication, QSizePolicy, QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPainter


DEFAULT_EMERGENCY_ITEMS: List[Dict[str, str]] = [
    {"label": "ماء\nWater", "action": "water", "emoji": "💧"},
    {"label": "طعام\nFood", "action": "food", "emoji": "🍽️"},
    {"label": "ألم\nPain", "action": "pain", "emoji": "🩹"},
    {"label": "مساعدة\nHelp", "action": "help", "emoji": "🆘"},
    {"label": "حمّام\nBathroom", "action": "bathroom", "emoji": "🚻"},
    {"label": "دواء\nMedicine", "action": "medicine", "emoji": "💊"},
    {"label": "حر / برد\nHot/Cold", "action": "temperature", "emoji": "🌡️"},
    {"label": "نوم\nSleep", "action": "sleep", "emoji": "😴"},
    {"label": "طبيب\nDoctor", "action": "doctor", "emoji": "👨‍⚕️"},
    {"label": "طوارئ\nEmergency", "action": "emergency", "emoji": "🚨"},
    {"label": "شكراً\nThank You", "action": "thanks", "emoji": "🙏"},
    {"label": "نعم / لا\nYes / No", "action": "yesno", "emoji": "✅"},
]


class EmergencyButton:
    """Represents a single emergency panel button."""

    def __init__(self, label: str, icon_path: str, action: str, emoji: str = "") -> None:
        self.label = label
        self.icon_path = icon_path
        self.action = action
        self.emoji = emoji


class EmergencyPanel(QWidget):
    """Displays large image-based buttons for urgent communication."""

    alert_triggered = pyqtSignal(str, str)

    def __init__(
        self,
        button_size: int = 120,
        alert_sound_enabled: bool = True,
        contacts: Optional[List[str]] = None,
        columns: int = 4,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.button_size = button_size
        self.alert_sound_enabled = alert_sound_enabled
        self.contacts = contacts or []
        self.columns = columns
        self._buttons: List[EmergencyButton] = []
        self._qt_buttons: List[QPushButton] = []
        self._visible: bool = False
        self.on_alert: Optional[Callable[[str], None]] = None
        self._last_alert_time: float = 0.0
        self._cooldown_ms: float = 2000.0

        self._init_ui()
        self._load_default_buttons()

    def _init_ui(self) -> None:
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setStyleSheet("background-color: #1A1A2E;")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("🆘 لوحة الطوارئ — Emergency Panel")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6B6B; padding: 8px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self._status_label = QLabel("")
        self._status_label.setFont(QFont("Arial", 13))
        self._status_label.setStyleSheet(
            "color: #4ECDC4; padding: 6px; background-color: #16213E; border-radius: 6px;"
        )
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setMinimumHeight(40)
        main_layout.addWidget(self._status_label)

        self._grid_layout = QGridLayout()
        self._grid_layout.setSpacing(8)
        main_layout.addLayout(self._grid_layout)

        close_btn = QPushButton("✕ إغلاق / Close")
        close_btn.setFont(QFont("Arial", 12, QFont.Bold))
        close_btn.setFixedHeight(45)
        close_btn.setStyleSheet(
            "QPushButton { background-color: #E74C3C; color: white; "
            "border-radius: 8px; border: none; }"
            "QPushButton:hover { background-color: #C0392B; }"
        )
        close_btn.clicked.connect(self.hide)
        main_layout.addWidget(close_btn)

    def _load_default_buttons(self) -> None:
        for item in DEFAULT_EMERGENCY_ITEMS:
            self.add_button(
                label=item["label"],
                icon_path="",
                action=item["action"],
                emoji=item.get("emoji", ""),
            )

    def _create_emoji_icon(self, emoji: str, size: int) -> QIcon:
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setFont(QFont("Segoe UI Emoji", size // 2))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, emoji)
        painter.end()
        return QIcon(pixmap)

    def add_button(self, label: str, icon_path: str, action: str, emoji: str = "") -> None:
        eb = EmergencyButton(label, icon_path, action, emoji)
        self._buttons.append(eb)

        btn = QPushButton()
        btn.setFixedSize(self.button_size, self.button_size)
        btn.setFont(QFont("Arial", 11, QFont.Bold))

        display_text = f"{emoji}\n{label}" if emoji else label
        btn.setText(display_text)

        if icon_path and os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(self.button_size // 2, self.button_size // 2))

        btn.setStyleSheet(
            "QPushButton { background-color: #0F3460; color: #E0E0E0; "
            "border: 2px solid #1A5276; border-radius: 12px; "
            "font-size: 11px; padding: 4px; }"
            "QPushButton:hover { background-color: #1A5276; border-color: #4ECDC4; }"
            "QPushButton:pressed { background-color: #E74C3C; }"
        )

        btn.clicked.connect(lambda checked, a=action, l=label: self._on_button_pressed(a, l))
        self._qt_buttons.append(btn)

        idx = len(self._qt_buttons) - 1
        row = idx // self.columns
        col = idx % self.columns
        self._grid_layout.addWidget(btn, row, col)

        self._update_panel_size()

    def _update_panel_size(self) -> None:
        rows = (len(self._qt_buttons) + self.columns - 1) // self.columns
        width = self.columns * (self.button_size + 8) + 32
        height = rows * (self.button_size + 8) + 180
        self.setMinimumSize(width, height)

    def _on_button_pressed(self, action: str, label: str) -> None:
        now = time.time() * 1000
        if now - self._last_alert_time < self._cooldown_ms:
            return
        self._last_alert_time = now

        self.trigger_alert(action)

        clean_label = label.replace("\n", " / ")
        self._status_label.setText(f"⚡ تم الإرسال: {clean_label}")
        self._status_label.setStyleSheet(
            "color: #FFF; padding: 6px; background-color: #E74C3C; border-radius: 6px;"
        )

        QTimer.singleShot(3000, self._reset_status)

    def _reset_status(self) -> None:
        self._status_label.setText("")
        self._status_label.setStyleSheet(
            "color: #4ECDC4; padding: 6px; background-color: #16213E; border-radius: 6px;"
        )

    def show(self) -> None:
        self._visible = True
        super().show()

    def hide(self) -> None:
        self._visible = False
        super().hide()

    def trigger_alert(self, action: str) -> None:
        if self.on_alert:
            self.on_alert(action)

        self.alert_triggered.emit(action, time.strftime("%H:%M:%S"))

        if self.alert_sound_enabled:
            self._play_alert_sound(action)

        if self.contacts and action in ("emergency", "doctor", "help"):
            self.send_notification(f"URGENT: {action} requested at {time.strftime('%H:%M:%S')}")

    def _play_alert_sound(self, action: str) -> None:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            messages = {
                "water": "المريض يريد ماء. Patient needs water.",
                "food": "المريض يريد طعام. Patient needs food.",
                "pain": "المريض يشعر بألم. Patient is in pain.",
                "help": "المريض يحتاج مساعدة. Patient needs help.",
                "bathroom": "المريض يريد الحمام. Patient needs bathroom.",
                "medicine": "المريض يريد دواء. Patient needs medicine.",
                "temperature": "المريض يشعر بحرارة أو برودة. Patient feels hot or cold.",
                "sleep": "المريض يريد النوم. Patient wants to sleep.",
                "doctor": "المريض يريد طبيب. Patient needs a doctor.",
                "emergency": "حالة طوارئ! Emergency!",
                "thanks": "شكراً. Thank you.",
                "yesno": "نعم أو لا. Yes or No.",
            }
            msg = messages.get(action, f"Alert: {action}")
            engine.say(msg)
            engine.runAndWait()
            engine.stop()
        except Exception:
            pass

    def play_sound(self, sound_path: str) -> None:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("Alert")
            engine.runAndWait()
            engine.stop()
        except Exception:
            pass

    def send_notification(self, message: str) -> None:
        for contact in self.contacts:
            print(f"[NOTIFICATION → {contact}]: {message}")

    def get_buttons(self) -> List[Dict[str, str]]:
        return [
            {"label": b.label, "icon_path": b.icon_path, "action": b.action, "emoji": b.emoji}
            for b in self._buttons
        ]

    def is_visible(self) -> bool:
        return self._visible


if __name__ == "__main__":
    import sys

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication(sys.argv)
    panel = EmergencyPanel(button_size=120, alert_sound_enabled=False)

    alerts_log: List[str] = []
    panel.on_alert = lambda action: alerts_log.append(action)

    print(f"Buttons: {len(panel.get_buttons())}")
    for b in panel.get_buttons():
        print(f"  {b['emoji']} {b['action']}: {b['label'].replace(chr(10), ' / ')}")

    panel.trigger_alert("water")
    panel.trigger_alert("pain")
    print(f"\nAlerts triggered: {alerts_log}")
    print(f"Visible: {panel.is_visible()}")
    panel.show()
    print(f"After show: {panel.is_visible()}")
    panel.hide()
    print(f"After hide: {panel.is_visible()}")
    print("\nEmergencyPanel test completed.")
