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
🚨 <b>URGENT: TICKETS NOW AVAILABLE!</b> 🚨

<b>Event:</b> {title}
<b>Dates:</b> {dates}
<b>Venue:</b> {venue}
<b>Status:</b> <u>{status}</u>
<b>Price:</b> {price}

⚡ <b>QUICK ACTION REQUIRED:</b>
1. Click the link below immediately
2. Complete purchase in next 2-3 minutes (before sold out)
3. Use saved payment method for fastest checkout

<b>🔗 BUY NOW (Click here):</b>
https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true

⏱️ <b>TIP:</b> Most tickets sell out within 5-10 minutes
💡 Have payment method saved for instant checkout
🔔 Multiple reminders will be sent if still available"""
        return message.strip()
    
    def send_urgent_alert(self, ticket_info: dict) -> bool:
        """Send multiple urgent alerts with emphasis on limited availability"""
        try:
            # First alert with all details
            self.send_ticket_notification(ticket_info)
            
            # Quick follow-up with purchase reminder (after 2 seconds)
            import time
            time.sleep(2)
            
            quick_reminder = f"""
⚡ <b>REMINDER: TICKETS STILL AVAILABLE!</b>

Limited quantity remaining!

<b>🎫 {ticket_info.get('title')}</b>
<b>Price:</b> {ticket_info.get('price')}

🔗 <a href="https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true"><b>PURCHASE NOW</b></a>

⚠️ These tickets may sell out any moment!"""
            
            self.send_message(quick_reminder)
            logger.info("Urgent alert sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending urgent alert: {e}")
            return False
