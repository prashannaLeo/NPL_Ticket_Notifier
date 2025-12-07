"""
NPL Ticket Notifier - Professional package for monitoring NPL cricket tickets
"""

__version__ = "1.0.0"
__author__ = "NPL Ticket Notifier Team"
__description__ = "Real-time Khalti events API monitoring with Telegram notifications"

from npl_notifier.core.scraper import KhaltiScraper
from npl_notifier.core.config import (
    KHALTI_EVENT_ID,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    CHECK_INTERVAL_SECONDS,
)

__all__ = [
    "KhaltiScraper",
    "KHALTI_EVENT_ID",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "CHECK_INTERVAL_SECONDS",
]
