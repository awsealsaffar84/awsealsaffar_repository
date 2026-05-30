"""Telegram application launcher with desktop and web fallback.

Intelligently launches Telegram: tries the desktop application first
(if installed) and falls back to the web version (web.telegram.org)
otherwise. Auto-detects Telegram installations across common Windows paths.
"""

import os
import sys
import subprocess
import platform
import webbrowser
from typing import Optional, List


TELEGRAM_WEB_URL: str = "https://web.telegram.org"
TELEGRAM_DEEP_LINK: str = "tg://"


COMMON_TELEGRAM_PATHS: List[str] = [
    r"%LocalAppData%\Programs\Telegram Desktop\Telegram.exe",
    r"%LocalAppData%\Telegram Desktop\Telegram.exe",
    r"%ProgramFiles%\Telegram Desktop\Telegram.exe",
    r"%ProgramFiles(x86)%\Telegram Desktop\Telegram.exe",
    r"%AppData%\Telegram Desktop\Telegram.exe",
]


class TelegramLauncher:
    """Launches and manages the Telegram desktop application.

    Provides a simplified interface to open Telegram and optionally
    navigate to a specific chat for quick communication. If the desktop
    app is unavailable, automatically falls back to the web version.

    Attributes:
        app_path: Path to the Telegram desktop executable (auto-detected).
        auto_start: Whether to launch Telegram on system startup.
        prefer_web: Force using web version even if desktop is installed.
    """

    def __init__(
        self,
        app_path: Optional[str] = None,
        auto_start: bool = False,
        prefer_web: bool = False,
    ) -> None:
        """Initialize the Telegram launcher.

        Args:
            app_path: Path to the Telegram executable. Auto-detected if None.
            auto_start: Whether to auto-launch on startup.
            prefer_web: Use web version even when desktop is available.
        """
        self.auto_start = auto_start
        self.prefer_web = prefer_web
        self.platform = platform.system().lower()
        self._is_running: bool = False
        self.app_path: Optional[str] = app_path or self.detect_installation()
        self._psutil = self._try_import_psutil()

    def _try_import_psutil(self):
        try:
            import psutil
            return psutil
        except ImportError:
            return None

    def detect_installation(self) -> Optional[str]:
        """Detect the Telegram installation path on the system.

        Returns:
            Path to the Telegram executable, or None if not found.
        """
        if self.platform != "windows":
            import shutil
            for cmd in ("telegram-desktop", "telegram"):
                found = shutil.which(cmd)
                if found:
                    return found
            return None

        for path_template in COMMON_TELEGRAM_PATHS:
            expanded = os.path.expandvars(path_template)
            if os.path.exists(expanded):
                return expanded
        return None

    def launch(self, chat_username: Optional[str] = None) -> bool:
        """Launch Telegram, optionally opening a specific chat.

        Tries the desktop app first; falls back to web if unavailable.

        Args:
            chat_username: Optional Telegram username (without @) to open.

        Returns:
            True if launched successfully, False otherwise.
        """
        if self.prefer_web or not self.app_path:
            return self.launch_web(chat_username)

        try:
            if chat_username:
                subprocess.Popen([self.app_path, "-startintray", f"tg://resolve?domain={chat_username}"])
            else:
                subprocess.Popen([self.app_path, "-startintray"])
            self._is_running = True
            print(f"[TelegramLauncher] Desktop app launched: {self.app_path}")
            return True
        except Exception as e:
            print(f"[TelegramLauncher] Desktop launch failed: {e}")
            return self.launch_web(chat_username)

    def launch_web(self, chat_username: Optional[str] = None) -> bool:
        """Open Telegram in the default web browser.

        Args:
            chat_username: Optional Telegram username (without @) to open.

        Returns:
            True if opened successfully.
        """
        try:
            url = TELEGRAM_WEB_URL
            if chat_username:
                url = f"{TELEGRAM_WEB_URL}/k/#@{chat_username}"
            webbrowser.open(url)
            print(f"[TelegramLauncher] Web version opened: {url}")
            return True
        except Exception as e:
            print(f"[TelegramLauncher] Web launch failed: {e}")
            return False

    def is_installed(self) -> bool:
        """Check whether Telegram desktop is installed.

        Returns:
            True if the desktop application is installed.
        """
        return self.app_path is not None and os.path.exists(self.app_path)

    def is_running(self) -> bool:
        """Check whether Telegram is currently running.

        Returns:
            True if Telegram process is running.
        """
        if not self._psutil:
            return self._is_running

        try:
            for proc in self._psutil.process_iter(["name"]):
                name = (proc.info.get("name") or "").lower()
                if "telegram" in name:
                    self._is_running = True
                    return True
            self._is_running = False
            return False
        except Exception:
            return self._is_running

    def close(self) -> bool:
        """Close the Telegram desktop application.

        Returns:
            True if closed successfully.
        """
        if not self._psutil:
            print("[TelegramLauncher] psutil not installed; cannot close.")
            return False

        try:
            closed = False
            for proc in self._psutil.process_iter(["name"]):
                name = (proc.info.get("name") or "").lower()
                if "telegram" in name:
                    proc.terminate()
                    closed = True
            self._is_running = False
            return closed
        except Exception as e:
            print(f"[TelegramLauncher] close error: {e}")
            return False

    def open_chat(self, username: str) -> bool:
        """Open a specific Telegram chat by username.

        Args:
            username: Telegram username without the @ prefix.

        Returns:
            True if the chat was opened.
        """
        username = username.lstrip("@")
        return self.launch(chat_username=username)

    def send_quick_message(self, username: str, message: str) -> bool:
        """Open a chat with a pre-filled message (web only).

        Args:
            username: Recipient's Telegram username.
            message: Pre-filled message text.

        Returns:
            True if the URL was opened successfully.
        """
        username = username.lstrip("@")
        from urllib.parse import quote
        url = f"https://t.me/{username}?text={quote(message)}"
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"[TelegramLauncher] send_quick_message error: {e}")
            return False

    def get_status(self) -> dict:
        """Return a status summary for the launcher.

        Returns:
            Dictionary with installation, running, and path info.
        """
        return {
            "installed": self.is_installed(),
            "running": self.is_running(),
            "app_path": self.app_path,
            "platform": self.platform,
            "prefer_web": self.prefer_web,
            "fallback_url": TELEGRAM_WEB_URL,
        }


if __name__ == "__main__":
    print("TelegramLauncher module -- standalone test")
    print("=" * 50)

    launcher = TelegramLauncher()

    print(f"Platform: {launcher.platform}")
    print(f"Desktop installed: {launcher.is_installed()}")
    print(f"Desktop path: {launcher.app_path}")
    print(f"Currently running: {launcher.is_running()}")
    print(f"psutil available: {launcher._psutil is not None}")

    print("\n--- Full Status ---")
    status = launcher.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n--- Search Paths Checked ---")
    for path_template in COMMON_TELEGRAM_PATHS:
        expanded = os.path.expandvars(path_template)
        exists = os.path.exists(expanded)
        marker = "OK" if exists else "--"
        print(f"  [{marker}] {expanded}")

    print("\nTelegramLauncher test completed.")
    print("Note: launch() and launch_web() not invoked in test to avoid")
    print("      opening windows. Call manually to test actual launching.")
