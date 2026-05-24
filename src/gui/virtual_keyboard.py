"""On-screen virtual keyboard with Arabic and English layouts."""

import time
from typing import Optional, Callable, List, Tuple, Dict

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QApplication, QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor


ENGLISH_LAYOUT: List[List[str]] = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
]

ARABIC_LAYOUT: List[List[str]] = [
    ["١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩", "٠"],
    ["ض", "ص", "ث", "ق", "ف", "غ", "ع", "ه", "خ", "ح"],
    ["ش", "س", "ي", "ب", "ل", "ا", "ت", "ن", "م", "ك"],
    ["ئ", "ء", "ؤ", "ر", "لا", "ى", "ة", "و", "ز", "د"],
]

SPECIAL_KEYS: List[str] = ["SPACE", "BACKSPACE", "ENTER", "LANG", "CLEAR"]


class KeyButton(QPushButton):
    """A single keyboard key with dwell-highlight support."""

    def __init__(self, label: str, key_size: int = 60, parent: Optional[QWidget] = None) -> None:
        super().__init__(label, parent)
        self.key_label = label
        self._highlighted = False
        self._dwell_start: Optional[float] = None
        self.setFixedSize(key_size, key_size)
        self.setFont(QFont("Arial", 16, QFont.Bold))
        self._apply_style(False)

    def _apply_style(self, highlighted: bool) -> None:
        if highlighted:
            self.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; "
                "border: 2px solid #388E3C; border-radius: 8px; font-size: 16px; }"
            )
        else:
            self.setStyleSheet(
                "QPushButton { background-color: #2C2C2C; color: #E0E0E0; "
                "border: 1px solid #555; border-radius: 8px; font-size: 16px; }"
                "QPushButton:hover { background-color: #3C3C3C; }"
            )

    def set_highlighted(self, state: bool) -> None:
        if state != self._highlighted:
            self._highlighted = state
            self._apply_style(state)

    def start_dwell(self) -> None:
        if self._dwell_start is None:
            self._dwell_start = time.time()

    def reset_dwell(self) -> None:
        self._dwell_start = None
        self.set_highlighted(False)

    def get_dwell_elapsed_ms(self) -> float:
        if self._dwell_start is None:
            return 0.0
        return (time.time() - self._dwell_start) * 1000.0


class VirtualKeyboard(QWidget):
    """Displays an on-screen keyboard controlled by head-tracking."""

    key_pressed = pyqtSignal(str)

    SUPPORTED_LANGUAGES: List[str] = ["en", "ar"]

    def __init__(
        self,
        key_size: int = 60,
        language: str = "en",
        dwell_highlight_ms: int = 800,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.key_size = key_size
        self.language = language
        self.dwell_highlight_ms = dwell_highlight_ms
        self.on_key_press: Optional[Callable[[str], None]] = None
        self._visible: bool = False
        self._text_buffer: str = ""
        self._shift_active: bool = False
        self._buttons: List[KeyButton] = []
        self._special_buttons: Dict[str, QPushButton] = {}
        self._current_hover_btn: Optional[KeyButton] = None

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: #1A1A1A;")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(8, 8, 8, 8)

        self._text_display = QLabel("")
        self._text_display.setFont(QFont("Arial", 14))
        self._text_display.setStyleSheet(
            "QLabel { background-color: #333; color: #FFF; padding: 8px; "
            "border-radius: 6px; min-height: 30px; }"
        )
        self._text_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._text_display.setWordWrap(True)
        main_layout.addWidget(self._text_display)

        self._keys_layout = QGridLayout()
        self._keys_layout.setSpacing(4)
        main_layout.addLayout(self._keys_layout)

        special_layout = QHBoxLayout()
        special_layout.setSpacing(4)

        for key_name in SPECIAL_KEYS:
            btn = QPushButton(self._get_special_label(key_name))
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(self.key_size)
            btn.setStyleSheet(
                "QPushButton { background-color: #444; color: #FFF; "
                "border: 1px solid #666; border-radius: 8px; }"
                "QPushButton:hover { background-color: #555; }"
            )
            btn.clicked.connect(lambda checked, k=key_name: self._on_special_key(k))
            special_layout.addWidget(btn)
            self._special_buttons[key_name] = btn

        main_layout.addLayout(special_layout)

        self._populate_keys()
        self._update_size()

    def _get_special_label(self, key_name: str) -> str:
        labels = {
            "SPACE": "␣ Space",
            "BACKSPACE": "⌫ Bksp",
            "ENTER": "↵ Enter",
            "LANG": "🌐 AR/EN",
            "CLEAR": "✕ Clear",
        }
        return labels.get(key_name, key_name)

    def _populate_keys(self) -> None:
        for btn in self._buttons:
            self._keys_layout.removeWidget(btn)
            btn.deleteLater()
        self._buttons.clear()

        layout = ARABIC_LAYOUT if self.language == "ar" else ENGLISH_LAYOUT

        for row_idx, row in enumerate(layout):
            for col_idx, key in enumerate(row):
                btn = KeyButton(key, self.key_size, self)
                btn.clicked.connect(lambda checked, k=key: self._on_key_clicked(k))
                self._keys_layout.addWidget(btn, row_idx, col_idx)
                self._buttons.append(btn)

        if self.language == "ar":
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)

    def _update_size(self) -> None:
        cols = 10
        rows = 4
        width = cols * (self.key_size + 4) + 20
        height = (rows + 1) * (self.key_size + 4) + 60 + 20
        self.setFixedSize(width, height)

    def _on_key_clicked(self, key: str) -> None:
        if self._shift_active:
            char = key.upper()
            self._shift_active = False
        else:
            char = key.lower() if self.language == "en" else key

        self._text_buffer += char
        self._text_display.setText(self._text_buffer)

        if self.on_key_press:
            self.on_key_press(char)
        self.key_pressed.emit(char)

    def _on_special_key(self, key_name: str) -> None:
        if key_name == "SPACE":
            self._text_buffer += " "
            if self.on_key_press:
                self.on_key_press(" ")
            self.key_pressed.emit(" ")
        elif key_name == "BACKSPACE":
            if self._text_buffer:
                self._text_buffer = self._text_buffer[:-1]
            if self.on_key_press:
                self.on_key_press("\b")
            self.key_pressed.emit("\b")
        elif key_name == "ENTER":
            self._text_buffer += "\n"
            if self.on_key_press:
                self.on_key_press("\n")
            self.key_pressed.emit("\n")
        elif key_name == "LANG":
            new_lang = "ar" if self.language == "en" else "en"
            self.set_language(new_lang)
        elif key_name == "CLEAR":
            self.clear_buffer()

        self._text_display.setText(self._text_buffer)

    def show(self) -> None:
        self._visible = True
        super().show()

    def hide(self) -> None:
        self._visible = False
        super().hide()

    def toggle(self) -> None:
        if self._visible:
            self.hide()
        else:
            self.show()

    def set_language(self, language: str) -> None:
        if language in self.SUPPORTED_LANGUAGES:
            self.language = language
            self._populate_keys()
            lang_btn = self._special_buttons.get("LANG")
            if lang_btn:
                label = "🌐 EN→AR" if language == "en" else "🌐 AR→EN"
                lang_btn.setText(label)

    def update_cursor_position(self, x: int, y: int) -> None:
        """Update cursor position for dwell-based key selection."""
        hit_btn: Optional[KeyButton] = None
        for btn in self._buttons:
            btn_global = btn.mapToGlobal(btn.rect().topLeft())
            bx, by = btn_global.x(), btn_global.y()
            bw, bh = btn.width(), btn.height()
            if bx <= x <= bx + bw and by <= y <= by + bh:
                hit_btn = btn
                break

        if hit_btn != self._current_hover_btn:
            if self._current_hover_btn:
                self._current_hover_btn.reset_dwell()
            self._current_hover_btn = hit_btn
            if hit_btn:
                hit_btn.start_dwell()
        elif hit_btn is not None:
            elapsed = hit_btn.get_dwell_elapsed_ms()
            progress = min(elapsed / self.dwell_highlight_ms, 1.0)
            hit_btn.set_highlighted(progress > 0.5)
            if elapsed >= self.dwell_highlight_ms:
                self._on_key_clicked(hit_btn.key_label)
                hit_btn.reset_dwell()
                self._current_hover_btn = None

    def get_text_buffer(self) -> str:
        return self._text_buffer

    def clear_buffer(self) -> None:
        self._text_buffer = ""
        self._text_display.setText("")

    def is_visible(self) -> bool:
        return self._visible


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    kb = VirtualKeyboard(key_size=60, language="en", dwell_highlight_ms=800)

    def on_key(char: str) -> None:
        if char == "\b":
            print("[BACKSPACE]", end="", flush=True)
        elif char == "\n":
            print("\n[ENTER]", end="", flush=True)
        elif char == " ":
            print("[SPACE]", end="", flush=True)
        else:
            print(char, end="", flush=True)

    kb.on_key_press = on_key
    kb.show()
    kb.move(100, 400)

    print("Virtual Keyboard running. Close window to exit.")
    print("Buffer contents will display as you type.")
    print("=" * 50)

    sys.exit(app.exec_())
