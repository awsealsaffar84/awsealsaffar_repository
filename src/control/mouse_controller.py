"""Mouse control bridge using pyautogui for cross-platform cursor movement."""

import math
from typing import Tuple, Optional


class MouseController:
    """Controls the system mouse cursor based on head-tracking input."""

    def __init__(
        self,
        sensitivity_x: float = 1.5,
        sensitivity_y: float = 1.5,
        acceleration: float = 1.2,
        screen_width: int = 1920,
        screen_height: int = 1080,
        simulated: bool = False,
    ) -> None:
        self.sensitivity_x = sensitivity_x
        self.sensitivity_y = sensitivity_y
        self.acceleration = acceleration
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.simulated = simulated
        self._enabled = False
        self._pos_x: float = screen_width / 2.0
        self._pos_y: float = screen_height / 2.0
        self._pyautogui = None

        if not simulated:
            try:
                import pyautogui
                pyautogui.FAILSAFE = False
                pyautogui.PAUSE = 0
                self._pyautogui = pyautogui
                size = pyautogui.size()
                self.screen_width = size.width
                self.screen_height = size.height
            except Exception:
                self.simulated = True

    def _apply_acceleration(self, dx: float, dy: float) -> Tuple[float, float]:
        """Apply non-linear acceleration curve to movement deltas."""
        magnitude = math.sqrt(dx * dx + dy * dy)
        if magnitude < 1e-6:
            return (0.0, 0.0)
        # Sigmoid-like acceleration: small movements stay small, large ones amplified
        scale = math.pow(magnitude, self.acceleration - 1.0)
        return (dx * scale, dy * scale)

    def move_to(self, x: int, y: int) -> None:
        """Move the cursor to an absolute screen position."""
        if not self._enabled:
            return
        self._pos_x = max(0, min(x, self.screen_width - 1))
        self._pos_y = max(0, min(y, self.screen_height - 1))
        if self._pyautogui and not self.simulated:
            self._pyautogui.moveTo(int(self._pos_x), int(self._pos_y), _pause=False)

    def move_relative(self, dx: float, dy: float) -> None:
        """Move the cursor relative to its current position with sensitivity and acceleration."""
        if not self._enabled:
            return
        # Apply sensitivity
        dx *= self.sensitivity_x
        dy *= self.sensitivity_y
        # Apply acceleration
        dx, dy = self._apply_acceleration(dx, dy)
        # Update position with clamping
        self._pos_x = max(0.0, min(self._pos_x + dx, self.screen_width - 1.0))
        self._pos_y = max(0.0, min(self._pos_y + dy, self.screen_height - 1.0))
        if self._pyautogui and not self.simulated:
            self._pyautogui.moveTo(int(self._pos_x), int(self._pos_y), _pause=False)

    def click(self, button: str = "left") -> None:
        """Perform a mouse click."""
        if not self._enabled:
            return
        if self._pyautogui and not self.simulated:
            self._pyautogui.click(button=button, _pause=False)

    def double_click(self) -> None:
        """Perform a left double-click."""
        if not self._enabled:
            return
        if self._pyautogui and not self.simulated:
            self._pyautogui.doubleClick(_pause=False)

    def scroll(self, amount: int) -> None:
        """Scroll the mouse wheel."""
        if not self._enabled:
            return
        if self._pyautogui and not self.simulated:
            self._pyautogui.scroll(amount, _pause=False)

    def get_position(self) -> Tuple[int, int]:
        """Get the current cursor position."""
        return (int(self._pos_x), int(self._pos_y))

    def enable(self) -> None:
        """Enable mouse control."""
        self._enabled = True

    def disable(self) -> None:
        """Disable mouse control."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check whether mouse control is active."""
        return self._enabled


if __name__ == "__main__":
    print("MouseController module -- standalone test")
    ctrl = MouseController(simulated=True)
    ctrl.enable()
    print(f"Initial position: {ctrl.get_position()}")
    ctrl.move_relative(100, 50)
    print(f"After move_relative(100, 50): {ctrl.get_position()}")
    ctrl.move_to(500, 300)
    print(f"After move_to(500, 300): {ctrl.get_position()}")
    ctrl.move_relative(-1000, -1000)
    print(f"After clamping to (0,0): {ctrl.get_position()}")
    ctrl.disable()
    ctrl.move_relative(100, 100)
    print(f"After disabled move (should not change): {ctrl.get_position()}")
    print("MouseController test completed.")
