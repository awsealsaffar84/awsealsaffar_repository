"""Apps module: Windows bridge and application launchers."""

from src.apps.windows_bridge import WindowsBridge, COMMON_APPS, QUICK_URLS
from src.apps.telegram_launcher import TelegramLauncher, TELEGRAM_WEB_URL

__all__ = [
    "WindowsBridge",
    "COMMON_APPS",
    "QUICK_URLS",
    "TelegramLauncher",
    "TELEGRAM_WEB_URL",
]
