"""
Configuration file for NPL Ticket Notifier
Reads from environment variables (for security)
Falls back to defaults for local development
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Khalti Event ID to monitor
KHALTI_EVENT_ID = os.getenv(
    "KHALTI_EVENT_ID",
    "ET25AMY4AUYM"
)

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Scraping Configuration
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "10"))

# Ticket availability status
TICKET_STATUS = {
    "FILLING_FAST": "Filling Fast",
    "SOLD_OUT": "Sold Out",
    "AVAILABLE": "Available"
}

# Validate required configuration
def validate_config():
    """Ensure required configuration is present"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
    if not TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID not set in environment variables")
    return True

