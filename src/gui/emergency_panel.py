"""Image-based emergency panel for expressing needs, pain, and alerts."""

from typing import Optional, List, Dict, Callable


class EmergencyButton:
    """Represents a single emergency panel button.

    Attributes:
        label: Button label text.
        icon_path: Path to the button icon image.
        action: Action identifier triggered by this button.
    """

    def __init__(
        self,
        label: str,
        icon_path: str,
        action: str,
    ) -> None:
        """Initialize an emergency button.

        Args:
            label: Display label for the button.
            icon_path: Path to the icon image file.
            action: Action identifier string.
        """
        self.label = label
        self.icon_path = icon_path
        self.action = action
        raise NotImplementedError


class EmergencyPanel:
    """Displays large image-based buttons for urgent communication.

    Provides quick access to common needs (water, pain, help, etc.)
    and can trigger audio alerts or send notifications.

    Attributes:
        button_size: Size of each button in pixels.
        alert_sound_enabled: Whether to play an audio alert on press.
        contacts: List of emergency contact identifiers.
    """

    def __init__(
        self,
        button_size: int = 120,
        alert_sound_enabled: bool = True,
        contacts: Optional[List[str]] = None,
    ) -> None:
        """Initialize the emergency panel.

        Args:
            button_size: Size of each button in pixels.
            alert_sound_enabled: Enable audio alert on button press.
            contacts: List of emergency contacts.
        """
        self.button_size = button_size
        self.alert_sound_enabled = alert_sound_enabled
        self.contacts = contacts or []
        self._buttons: List[EmergencyButton] = []
        self._visible: bool = False
        self.on_alert: Optional[Callable[[str], None]] = None
        raise NotImplementedError

    def add_button(
        self, label: str, icon_path: str, action: str
    ) -> None:
        """Add a button to the emergency panel.

        Args:
            label: Button display label.
            icon_path: Path to the button icon.
            action: Action identifier.
        """
        raise NotImplementedError

    def show(self) -> None:
        """Display the emergency panel."""
        raise NotImplementedError

    def hide(self) -> None:
        """Hide the emergency panel."""
        raise NotImplementedError

    def trigger_alert(self, action: str) -> None:
        """Trigger an emergency alert for the given action.

        Args:
            action: The action identifier to trigger.
        """
        raise NotImplementedError

    def play_sound(self, sound_path: str) -> None:
        """Play an alert sound.

        Args:
            sound_path: Path to the audio file.
        """
        raise NotImplementedError

    def send_notification(self, message: str) -> None:
        """Send a notification to emergency contacts.

        Args:
            message: Notification message text.
        """
        raise NotImplementedError

    def get_buttons(self) -> List[Dict[str, str]]:
        """Return the list of configured buttons.

        Returns:
            List of button dictionaries with label, icon_path, action.
        """
        raise NotImplementedError

    def is_visible(self) -> bool:
        """Check whether the panel is currently displayed.

        Returns:
            True if visible, False otherwise.
        """
        raise NotImplementedError


if __name__ == "__main__":
    print("EmergencyPanel module -- run standalone test")
    panel = EmergencyPanel()
    print("EmergencyPanel initialized successfully.")
