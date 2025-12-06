"""
Main notifier script - Monitors Khalti events and sends Telegram notifications
"""

import logging
import time
from datetime import datetime
from scraper import KhaltiScraper
from telegram_notifier import TelegramNotifier
from voice_notifier import VoiceNotifier
from config import (
    KHALTI_EVENT_ID,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    CHECK_INTERVAL_SECONDS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ticket_notifier.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TicketNotifier:
    def __init__(self):
        self.scraper = KhaltiScraper(KHALTI_EVENT_ID)
        self.notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.voice_notifier = VoiceNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.notified_tickets = set()  # Track which tickets we've already notified about

    def get_ticket_hash(self, ticket_info: dict) -> str:
        """Create a unique hash for a ticket to avoid duplicate notifications"""
        # Support both old and new field names
        date_field = ticket_info.get('dates') or ticket_info.get('date', '')
        return f"{ticket_info['title']}_{date_field}_{ticket_info.get('price', '')}"

    def check_and_notify(self):
        """Check for available tickets and send notifications"""
        logger.info("Checking for available tickets...")

        try:
            available_tickets = self.scraper.get_available_tickets()

            if available_tickets:
                logger.info(f"Found {len(available_tickets)} available ticket(s)")
                for ticket in available_tickets:
                    ticket_hash = self.get_ticket_hash(ticket)

                    # Only notify about new tickets
                    if ticket_hash not in self.notified_tickets:
                        logger.info(f"Sending notification for: {ticket['title']}")
                        
                        # Send voice alert first (urgent)
                        self.voice_notifier.send_alert_call(ticket)
                        time.sleep(0.5)
                        
                        # Then send detailed message
                        if self.notifier.send_ticket_notification(ticket):
                            self.notified_tickets.add(ticket_hash)
                        time.sleep(1)  # Rate limit to avoid Telegram API issues
            else:
                logger.info("No available tickets found")

        except Exception as e:
            logger.error(f"Error in check_and_notify: {e}")

    def run(self):
        """Main loop - continuously check for tickets"""
        logger.info("Starting NPL Ticket Notifier...")
        logger.info(f"Monitoring event: {KHALTI_EVENT_ID}")
        logger.info(f"API: https://khalti.com/api/e5/events/{KHALTI_EVENT_ID}/children/")
        logger.info(f"Check interval: {CHECK_INTERVAL_SECONDS} seconds")

        try:
            while True:
                self.check_and_notify()
                logger.debug(f"Next check in {CHECK_INTERVAL_SECONDS} seconds...")
                time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            logger.info("Notifier stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    # Validate configuration
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        logger.error("Please configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in config.py")
        exit(1)

    notifier = TicketNotifier()
    notifier.run()
