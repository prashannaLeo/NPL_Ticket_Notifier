"""
Interactive Telegram bot for NPL Ticket Notifier
Handles user commands like /tickets, /start, etc.
"""

import logging
import requests
from scraper import KhaltiScraper
from config import KHALTI_EVENT_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class InteractiveBot:
    def __init__(self, bot_token, event_id):
        self.bot_token = bot_token
        self.event_id = event_id
        self.scraper = KhaltiScraper(event_id)
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def get_available_tickets_message(self):
        """Fetch tickets and format as readable message"""
        try:
            available_tickets = self.scraper.get_available_tickets()
            
            if not available_tickets:
                return "❌ No available tickets at the moment.\n\nAll tickets are currently sold out."
            
            message = "🎫 **AVAILABLE TICKETS**\n\n"
            
            for i, ticket in enumerate(available_tickets, 1):
                title = ticket.get('title', 'N/A')
                date = ticket.get('dates') or ticket.get('date', 'N/A')
                location = ticket.get('venue') or ticket.get('location', 'N/A')
                price = ticket.get('price', 'N/A')
                status = ticket.get('status', 'Available')
                
                message += f"**{i}. {title}**\n"
                message += f"📅 Date: {date}\n"
                message += f"📍 Location: {location}\n"
                message += f"💰 Price: {price}\n"
                message += f"✅ Status: {status}\n"
                message += f"🔗 Book: https://events.khalti.com/events/{self.event_id}\n\n"
            
            return message
        
        except Exception as e:
            logger.error(f"Error fetching tickets: {e}")
            return f"❌ Error fetching tickets: {str(e)}"

    def send_message(self, chat_id, text, parse_mode="Markdown"):
        """Send a message to Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✓ Message sent to {chat_id}")
                return True
            else:
                logger.error(f"✗ Failed to send message: {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def handle_command(self, chat_id, command):
        """Handle incoming bot commands"""
        command = command.lower().strip()
        
        if command == "/tickets" or command == "/tickets@nplticketbot":
            logger.info(f"Received /tickets command from {chat_id}")
            message = self.get_available_tickets_message()
            return self.send_message(chat_id, message)
        
        elif command == "/start":
            welcome_message = (
                "👋 Welcome to **NPL Ticket Notifier Bot**!\n\n"
                "📌 **Available Commands:**\n"
                "• `/tickets` - Show all available NPL tickets\n"
                "• `/help` - Show this help message\n\n"
                "🔔 **Auto Notifications:**\n"
                "I'll automatically send you voice alerts and messages when new tickets become available.\n\n"
                "⏱️ **Check Frequency:**\n"
                "Every 1 minute for latest updates\n\n"
                "🎫 Need tickets? Use `/tickets` to check availability!"
            )
            return self.send_message(chat_id, welcome_message)
        
        elif command == "/help":
            help_message = (
                "📖 **Help - NPL Ticket Notifier Bot**\n\n"
                "**Commands:**\n"
                "• `/tickets` - Display all currently available tickets\n"
                "• `/start` - Show welcome message\n"
                "• `/help` - Show this message\n\n"
                "**How It Works:**\n"
                "1️⃣ Bot checks for available tickets every 1 minute\n"
                "2️⃣ When new tickets appear, you get:\n"
                "   • 🔊 Voice alert notification\n"
                "   • 📱 Text message with details\n"
                "3️⃣ Use `/tickets` anytime to check current availability\n\n"
                "💡 **Pro Tip:**\n"
                "Save this chat to get instant notifications when tickets drop!"
            )
            return self.send_message(chat_id, help_message)
        
        else:
            response = (
                "❓ Unknown command.\n\n"
                "Available commands:\n"
                "• `/tickets` - Show available tickets\n"
                "• `/start` - Welcome message\n"
                "• `/help` - Help information"
            )
            return self.send_message(chat_id, response)


def main():
    """Example usage"""
    bot = InteractiveBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)
    
    # Example: Get available tickets message
    print(bot.get_available_tickets_message())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()
