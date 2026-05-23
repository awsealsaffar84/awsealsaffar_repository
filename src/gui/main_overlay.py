"""Always-on-top control bar overlay for the head-tracking system."""

from typing import Optional, Dict, Callable


class MainOverlay:
    """Transparent always-on-top toolbar providing quick system controls.

    Displays status indicators and buttons for toggling tracking,
    opening the keyboard, emergency panel, and settings.

    Attributes:
        opacity: Overlay transparency (0.0 = invisible, 1.0 = opaque).
        position: Overlay position on screen ('top', 'bottom').
        theme: Visual theme ('light' or 'dark').
    """

    def __init__(
        self,
        opacity: float = 0.85,
        position: str = "top",
        theme: str = "dark",
    ) -> None:
        """Initialize the main overlay.

        Args:
            opacity: Overlay opacity level.
            position: Screen position for the overlay bar.
            theme: UI theme.
        """
        self.opacity = opacity
        self.position = position
        self.theme = theme
        self._visible: bool = False
        self._callbacks: Dict[str, Optional[Callable[[], None]]] = {}
        raise NotImplementedError

    def show(self) -> None:
        """Display the overlay bar."""
        raise NotImplementedError

    def hide(self) -> None:
        """Hide the overlay bar."""
        raise NotImplementedError

    def set_opacity(self, opacity: float) -> None:
        """Set the overlay transparency.

        Args:
            opacity: Opacity value in [0.0, 1.0].
        """
        raise NotImplementedError

    def set_tracking_status(self, active: bool) -> None:
        """Update the tracking status indicator.

        Args:
            active: True if tracking is active.
        """
        raise NotImplementedError

    def register_callback(
        self, button_name: str, callback: Callable[[], None]
    ) -> None:
        """Register a callback for a toolbar button.

        Args:
            button_name: Name of the toolbar button.
            callback: Function to call when the button is activated.
        """
        raise NotImplementedError

    def update_fps(self, fps: float) -> None:
        """Update the FPS display on the overlay.

        Args:
            fps: Current frames per second.
        """
        raise NotImplementedError

    def set_theme(self, theme: str) -> None:
        """Change the overlay theme.

        Args:
            theme: Theme name ('light' or 'dark').
        """
        raise NotImplementedError

    def is_visible(self) -> bool:
        """Check whether the overlay is currently displayed.

        Returns:
            True if visible, False otherwise.
        """
        raise NotImplementedError


if __name__ == "__main__":
    print("MainOverlay module -- run standalone test")
    overlay = MainOverlay()
    print("MainOverlay initialized successfully.")
