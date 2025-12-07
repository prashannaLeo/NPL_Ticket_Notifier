"""
Telegram notifier for sending messages
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a text message via Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Message sent successfully")
            return True
        except requests.RequestException as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def send_ticket_notification(self, ticket_info: dict) -> bool:
        """Send a formatted notification about available tickets"""
        try:
            message = self._format_ticket_message(ticket_info)
            return self.send_message(message)
        except Exception as e:
            logger.error(f"Error sending ticket notification: {e}")
            return False

    def _format_ticket_message(self, ticket_info: dict) -> str:
        """Format ticket information into a Telegram message"""
        title = ticket_info.get('title', 'N/A')
        # Support both old and new field names (dates/date, venue/location)
        dates = ticket_info.get('dates') or ticket_info.get('date', 'N/A')
        venue = ticket_info.get('venue') or ticket_info.get('location', 'N/A')
        status = ticket_info.get('status', 'Available')
        price = ticket_info.get('price', 'N/A')

        message = f"""
<b>🎫 NPL TICKET ALERT!</b>

<b>Event:</b> {title}
<b>Dates:</b> {dates}
<b>Venue:</b> {venue}
<b>Status:</b> <u>{status}</u>
<b>Price:</b> {price}

<b>🔗 Get your tickets now:</b>
https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
"""
        return message.strip()
