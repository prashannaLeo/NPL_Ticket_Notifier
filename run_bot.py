#!/usr/bin/env python3
"""
Start the interactive bot for group chats
Usage: python run_bot.py
"""

from npl_notifier.bot.telegram_polling_bot import PollingBot
from npl_notifier.core.config import KHALTI_EVENT_ID, TELEGRAM_BOT_TOKEN
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ TELEGRAM_BOT_TOKEN not set in .env file")
        print("\n⚠️  Configure your bot token:")
        print("   1. Edit .env file")
        print("   2. Set: TELEGRAM_BOT_TOKEN=your_token_here")
        print("   3. Get token from @BotFather on Telegram")
        exit(1)
    
    bot = PollingBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)
    bot.run()
