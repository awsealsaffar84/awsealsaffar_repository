"""Windows bridge for opening folders, files, and applications.

Provides a comprehensive interface for launching applications, opening files,
managing windows, printing documents, and controlling the OS — enabling a
disabled user to operate the computer like a normal user via head-tracking.
"""

import os
import sys
import subprocess
import platform
import shutil
import webbrowser
from typing import Optional, List, Dict, Tuple


COMMON_APPS: Dict[str, Dict[str, str]] = {
    "notepad": {
        "label_ar": "المفكرة",
        "label_en": "Notepad",
        "command": "notepad.exe",
        "category": "office",
    },
    "calculator": {
        "label_ar": "الآلة الحاسبة",
        "label_en": "Calculator",
        "command": "calc.exe",
        "category": "utility",
    },
    "paint": {
        "label_ar": "الرسام",
        "label_en": "Paint",
        "command": "mspaint.exe",
        "category": "creative",
    },
    "wordpad": {
        "label_ar": "كاتب النصوص",
        "label_en": "WordPad",
        "command": "wordpad.exe",
        "category": "office",
    },
    "explorer": {
        "label_ar": "مستكشف الملفات",
        "label_en": "File Explorer",
        "command": "explorer.exe",
        "category": "system",
    },
    "cmd": {
        "label_ar": "موجه الأوامر",
        "label_en": "Command Prompt",
        "command": "cmd.exe",
        "category": "system",
    },
    "snipping": {
        "label_ar": "أداة القص",
        "label_en": "Snipping Tool",
        "command": "snippingtool.exe",
        "category": "utility",
    },
    "magnifier": {
        "label_ar": "المكبّر",
        "label_en": "Magnifier",
        "command": "magnify.exe",
        "category": "accessibility",
    },
    "onscreen_keyboard": {
        "label_ar": "لوحة المفاتيح على الشاشة",
        "label_en": "On-Screen Keyboard",
        "command": "osk.exe",
        "category": "accessibility",
    },
    "narrator": {
        "label_ar": "الراوي",
        "label_en": "Narrator",
        "command": "narrator.exe",
        "category": "accessibility",
    },
    "control_panel": {
        "label_ar": "لوحة التحكم",
        "label_en": "Control Panel",
        "command": "control.exe",
        "category": "system",
    },
    "settings": {
        "label_ar": "الإعدادات",
        "label_en": "Settings",
        "command": "ms-settings:",
        "category": "system",
        "url": True,
    },
    "winword": {
        "label_ar": "Microsoft Word",
        "label_en": "Microsoft Word",
        "command": "winword.exe",
        "category": "office",
    },
    "excel": {
        "label_ar": "Microsoft Excel",
        "label_en": "Microsoft Excel",
        "command": "excel.exe",
        "category": "office",
    },
    "powerpoint": {
        "label_ar": "Microsoft PowerPoint",
        "label_en": "Microsoft PowerPoint",
        "command": "powerpnt.exe",
        "category": "office",
    },
    "outlook": {
        "label_ar": "Microsoft Outlook",
        "label_en": "Microsoft Outlook",
        "command": "outlook.exe",
        "category": "office",
    },
    "chrome": {
        "label_ar": "Google Chrome",
        "label_en": "Google Chrome",
        "command": "chrome.exe",
        "category": "browser",
    },
    "firefox": {
        "label_ar": "Mozilla Firefox",
        "label_en": "Mozilla Firefox",
        "command": "firefox.exe",
        "category": "browser",
    },
    "edge": {
        "label_ar": "Microsoft Edge",
        "label_en": "Microsoft Edge",
        "command": "msedge.exe",
        "category": "browser",
    },
}

QUICK_URLS: Dict[str, str] = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram_web": "https://web.telegram.org",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "wikipedia_ar": "https://ar.wikipedia.org",
    "translate": "https://translate.google.com",
    "maps": "https://www.google.com/maps",
    "weather": "https://www.weather.com",
    "news_ar": "https://www.aljazeera.net",
}


class WindowsBridge:
    """Provides methods to open files, folders, and applications on Windows.

    Acts as a simplified interface to common OS operations that
    disabled users need to perform via head-tracking control. Designed
    to enable a disabled user to operate the computer as a normal user
    would — browsing the web, using Office, printing, listening to music,
    and communicating with others.

    Attributes:
        default_apps: List of pre-configured application paths.
        platform: The current platform name (windows, linux, darwin).
    """

    def __init__(
        self,
        default_apps: Optional[List[str]] = None,
    ) -> None:
        """Initialize the Windows bridge.

        Args:
            default_apps: List of default application executable paths.
        """
        self.default_apps = default_apps or []
        self.platform = platform.system().lower()
        self._psutil = self._try_import_psutil()
        self._pyautogui = self._try_import_pyautogui()
        self._keyboard = self._try_import_keyboard()

    def _try_import_psutil(self):
        try:
            import psutil
            return psutil
        except ImportError:
            return None

    def _try_import_pyautogui(self):
        try:
            import pyautogui
            pyautogui.FAILSAFE = False
            return pyautogui
        except Exception:
            return None

    def _try_import_keyboard(self):
        try:
            import keyboard
            return keyboard
        except Exception:
            return None

    def open_file(self, filepath: str) -> bool:
        """Open a file with the default system application.

        Args:
            filepath: Path to the file to open.

        Returns:
            True if the file was opened successfully.
        """
        if not os.path.exists(filepath):
            print(f"[WindowsBridge] File not found: {filepath}")
            return False
        try:
            if self.platform == "windows":
                os.startfile(filepath)
            elif self.platform == "darwin":
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])
            return True
        except Exception as e:
            print(f"[WindowsBridge] open_file error: {e}")
            return False

    def open_folder(self, folderpath: str) -> bool:
        """Open a folder in the file explorer.

        Args:
            folderpath: Path to the folder to open.

        Returns:
            True if the folder was opened successfully.
        """
        if not os.path.isdir(folderpath):
            print(f"[WindowsBridge] Folder not found: {folderpath}")
            return False
        try:
            if self.platform == "windows":
                subprocess.Popen(["explorer", folderpath])
            elif self.platform == "darwin":
                subprocess.Popen(["open", folderpath])
            else:
                subprocess.Popen(["xdg-open", folderpath])
            return True
        except Exception as e:
            print(f"[WindowsBridge] open_folder error: {e}")
            return False

    def open_url(self, url: str, browser: Optional[str] = None) -> bool:
        """Open a URL in the default or specified browser.

        Args:
            url: The URL to open.
            browser: Optional browser name (chrome, firefox, edge).

        Returns:
            True if opened successfully.
        """
        try:
            if browser:
                browser_lower = browser.lower()
                if browser_lower in COMMON_APPS:
                    cmd = COMMON_APPS[browser_lower]["command"]
                    subprocess.Popen([cmd, url], shell=True)
                    return True
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"[WindowsBridge] open_url error: {e}")
            return False

    def launch_application(self, app_path: str) -> bool:
        """Launch an application by its executable path or known short name.

        Args:
            app_path: Path to the executable, or a key from COMMON_APPS.

        Returns:
            True if the application was launched successfully.
        """
        try:
            key = app_path.lower().strip()
            if key in COMMON_APPS:
                spec = COMMON_APPS[key]
                cmd = spec["command"]
                if spec.get("url"):
                    if self.platform == "windows":
                        os.startfile(cmd)
                    else:
                        subprocess.Popen(["xdg-open", cmd])
                else:
                    if self.platform == "windows":
                        subprocess.Popen(cmd, shell=True)
                    else:
                        subprocess.Popen([cmd])
                print(f"[WindowsBridge] Launched: {spec['label_en']}")
                return True

            if os.path.exists(app_path):
                if self.platform == "windows":
                    os.startfile(app_path)
                else:
                    subprocess.Popen([app_path])
                return True

            subprocess.Popen(app_path, shell=True)
            return True
        except Exception as e:
            print(f"[WindowsBridge] launch_application error: {e}")
            return False

    def open_quick_site(self, site_key: str) -> bool:
        """Open a quick-access website (youtube, gmail, whatsapp, etc.).

        Args:
            site_key: Key from QUICK_URLS.

        Returns:
            True if opened successfully.
        """
        url = QUICK_URLS.get(site_key.lower())
        if not url:
            print(f"[WindowsBridge] Unknown site: {site_key}")
            return False
        return self.open_url(url)

    def print_file(self, filepath: str, printer: Optional[str] = None) -> bool:
        """Print a file using the default or specified printer.

        Args:
            filepath: Path to the file to print.
            printer: Optional printer name.

        Returns:
            True if the print job was sent successfully.
        """
        if not os.path.exists(filepath):
            print(f"[WindowsBridge] File not found: {filepath}")
            return False
        try:
            if self.platform == "windows":
                if printer:
                    os.startfile(filepath, f"printto \"{printer}\"")
                else:
                    os.startfile(filepath, "print")
                return True
            elif self.platform == "linux":
                cmd = ["lp"]
                if printer:
                    cmd.extend(["-d", printer])
                cmd.append(filepath)
                subprocess.Popen(cmd)
                return True
            else:
                subprocess.Popen(["lpr", filepath])
                return True
        except Exception as e:
            print(f"[WindowsBridge] print_file error: {e}")
            return False

    def get_user_folders(self) -> Dict[str, str]:
        """Return paths to common user folders.

        Returns:
            Dictionary of folder names to paths (Documents, Downloads, etc.).
        """
        home = os.path.expanduser("~")
        folders = {
            "home": home,
            "documents": os.path.join(home, "Documents"),
            "downloads": os.path.join(home, "Downloads"),
            "desktop": os.path.join(home, "Desktop"),
            "pictures": os.path.join(home, "Pictures"),
            "music": os.path.join(home, "Music"),
            "videos": os.path.join(home, "Videos"),
        }
        return {k: v for k, v in folders.items() if os.path.exists(v)}

    def list_running_apps(self) -> List[str]:
        """List currently running application names.

        Returns:
            List of running application names. Requires psutil.
        """
        if not self._psutil:
            print("[WindowsBridge] psutil not installed; cannot list running apps.")
            return []
        try:
            seen = set()
            apps: List[str] = []
            for proc in self._psutil.process_iter(["name"]):
                name = proc.info.get("name", "")
                if name and name not in seen:
                    seen.add(name)
                    apps.append(name)
            return sorted(apps)
        except Exception as e:
            print(f"[WindowsBridge] list_running_apps error: {e}")
            return []

    def switch_to_app(self, app_name: str) -> bool:
        """Switch focus to a running application by name.

        Args:
            app_name: Name of the application to switch to.

        Returns:
            True if focus was switched successfully.
        """
        if not self._pyautogui:
            print("[WindowsBridge] pyautogui not installed.")
            return False
        try:
            try:
                windows = self._pyautogui.getWindowsWithTitle(app_name)
                if windows:
                    windows[0].activate()
                    return True
            except Exception:
                pass

            if self._keyboard:
                self._keyboard.press_and_release("alt+tab")
                return True
            return False
        except Exception as e:
            print(f"[WindowsBridge] switch_to_app error: {e}")
            return False

    def close_app(self, app_name: str) -> bool:
        """Close a running application by name.

        Args:
            app_name: Name of the application/process to close.

        Returns:
            True if the application was closed successfully.
        """
        if not self._psutil:
            print("[WindowsBridge] psutil not installed.")
            return False
        try:
            closed = False
            for proc in self._psutil.process_iter(["name", "pid"]):
                name = proc.info.get("name", "") or ""
                if app_name.lower() in name.lower():
                    proc.terminate()
                    closed = True
            return closed
        except Exception as e:
            print(f"[WindowsBridge] close_app error: {e}")
            return False

    def send_hotkey(self, *keys: str) -> bool:
        """Send a keyboard shortcut (e.g. ctrl+c, alt+f4).

        Args:
            keys: Sequence of key names to press together.

        Returns:
            True if sent successfully.
        """
        if not self._pyautogui:
            return False
        try:
            self._pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"[WindowsBridge] send_hotkey error: {e}")
            return False

    def type_text(self, text: str, interval: float = 0.02) -> bool:
        """Type a string into the focused window.

        Args:
            text: Text to type.
            interval: Delay between characters in seconds.

        Returns:
            True if typed successfully.
        """
        if not self._pyautogui:
            return False
        try:
            self._pyautogui.typewrite(text, interval=interval)
            return True
        except Exception as e:
            print(f"[WindowsBridge] type_text error: {e}")
            return False

    def shutdown_pc(self, delay_seconds: int = 60) -> bool:
        """Schedule a system shutdown.

        Args:
            delay_seconds: Delay before shutdown.

        Returns:
            True if scheduled successfully.
        """
        try:
            if self.platform == "windows":
                subprocess.Popen(["shutdown", "/s", "/t", str(delay_seconds)])
            else:
                subprocess.Popen(["shutdown", "-h", f"+{delay_seconds // 60}"])
            return True
        except Exception as e:
            print(f"[WindowsBridge] shutdown_pc error: {e}")
            return False

    def cancel_shutdown(self) -> bool:
        """Cancel a pending shutdown."""
        try:
            if self.platform == "windows":
                subprocess.Popen(["shutdown", "/a"])
            else:
                subprocess.Popen(["shutdown", "-c"])
            return True
        except Exception:
            return False

    def get_apps_by_category(self, category: str) -> List[Dict[str, str]]:
        """Return apps filtered by category.

        Args:
            category: One of office, browser, system, utility, creative,
                      accessibility, or 'all'.

        Returns:
            List of app spec dicts.
        """
        if category == "all":
            return [
                {"key": k, **v} for k, v in COMMON_APPS.items()
            ]
        return [
            {"key": k, **v}
            for k, v in COMMON_APPS.items()
            if v.get("category") == category
        ]

    def is_app_installed(self, app_key: str) -> bool:
        """Check whether a known application is installed and reachable.

        Args:
            app_key: Key from COMMON_APPS.

        Returns:
            True if the executable is found in PATH or known install dirs.
        """
        spec = COMMON_APPS.get(app_key.lower())
        if not spec:
            return False
        cmd = spec["command"]
        if spec.get("url"):
            return True
        if shutil.which(cmd):
            return True
        common_paths = [
            os.path.expandvars(r"%ProgramFiles%"),
            os.path.expandvars(r"%ProgramFiles(x86)%"),
            os.path.expandvars(r"%LocalAppData%"),
        ]
        for base in common_paths:
            for root, _, files in os.walk(base):
                if cmd in files:
                    return True
                if root.count(os.sep) - base.count(os.sep) > 3:
                    break
        return False


if __name__ == "__main__":
    print("WindowsBridge module -- standalone test")
    print("=" * 50)

    bridge = WindowsBridge()
    print(f"Platform: {bridge.platform}")
    print(f"psutil available: {bridge._psutil is not None}")
    print(f"pyautogui available: {bridge._pyautogui is not None}")

    print("\n--- User Folders ---")
    folders = bridge.get_user_folders()
    for name, path in folders.items():
        print(f"  {name}: {path}")

    print("\n--- Apps by Category ---")
    for cat in ["office", "browser", "accessibility", "system"]:
        apps = bridge.get_apps_by_category(cat)
        names = [a["label_en"] for a in apps]
        print(f"  {cat}: {names}")

    print(f"\n--- Quick URLs ({len(QUICK_URLS)}) ---")
    for k, url in list(QUICK_URLS.items())[:5]:
        print(f"  {k}: {url}")
    print(f"  ... and {len(QUICK_URLS) - 5} more")

    print("\n--- Running Apps (first 10) ---")
    apps = bridge.list_running_apps()
    for app in apps[:10]:
        print(f"  {app}")
    print(f"  Total: {len(apps)}")

    print("\nWindowsBridge test completed.")
