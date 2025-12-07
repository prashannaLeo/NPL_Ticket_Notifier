#!/usr/bin/env python3
"""
Polling-based Telegram bot for NPL Ticket Notifier
Works in group chats (no webhook/public URL needed)
Usage: python -m npl_notifier.bot.telegram_polling_bot
"""

import logging
import requests
import time
import json
import os
from npl_notifier.core.scraper import KhaltiScraper
from npl_notifier.core.config import KHALTI_EVENT_ID, TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)


class PollingBot:
    """Telegram bot using long polling (works in groups)"""
    
    def __init__(self, bot_token: str, event_id: str):
        self.bot_token = bot_token
        self.event_id = event_id
        self.scraper = KhaltiScraper(event_id)
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_update_id = 0
        self.poll_timeout = 30  # Long polling timeout
        
    def get_updates(self):
        """Get new messages from Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                "offset": self.last_update_id + 1,
                "timeout": self.poll_timeout,
                "allowed_updates": ["message"]
            }
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            return response.json().get("result", [])
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = "HTML"):
        """Send a message"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": False
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def get_available_tickets_message(self) -> str:
        """Fetch tickets and format as message"""
        try:
            available_tickets = self.scraper.get_available_tickets()
            
            if not available_tickets:
                return "❌ No available tickets at the moment.\n\nAll tickets are currently sold out."
            
            message = "🎫 <b>AVAILABLE TICKETS</b>\n\n"
            
            for i, ticket in enumerate(available_tickets[:5], 1):  # Limit to 5 to avoid message too long
                title = ticket.get('title', 'N/A')
                date = ticket.get('dates') or ticket.get('date', 'N/A')
                location = ticket.get('venue') or ticket.get('location', 'N/A')
                price = ticket.get('price', 'N/A')
                
                message += f"<b>{i}. {title}</b>\n"
                message += f"📅 Date: {date}\n"
                message += f"📍 Location: {location}\n"
                message += f"💰 Price: {price}\n"
                message += f"🔗 <a href=\"https://events.khalti.com/events/{self.event_id}\">Get tickets</a>\n\n"
            
            return message
        
        except Exception as e:
            logger.error(f"Error fetching tickets: {e}")
            return f"❌ Error fetching tickets: {str(e)}"
    
    def handle_message(self, update: dict):
        """Handle incoming message"""
        try:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "").strip()
            
            if not chat_id or not text:
                return
            
            # Log the message
            user = message.get("from", {})
            username = user.get("username", "Unknown")
            logger.info(f"Message from @{username}: {text}")
            
            # Handle commands
            if text == "/tickets" or text == "/tickets@npl_bot":
                logger.info(f"Sending tickets list to {chat_id}")
                self.send_message(chat_id, self.get_available_tickets_message())
            
            elif text == "/start" or text == "/start@npl_bot":
                welcome = (
                    "👋 <b>Welcome to NPL Ticket Notifier Bot</b>\n\n"
                    "🎫 <b>Available Commands:</b>\n"
                    "• <b>/tickets</b> - Show available NPL tickets\n"
                    "• <b>/help</b> - Get help and information\n"
                    "• <b>/status</b> - Check bot status\n\n"
                    "📢 <b>How it works:</b>\n"
                    "This bot monitors Khalti API for NPL ticket availability.\n"
                    "Use /tickets to check current availability.\n\n"
                    "🔔 You also receive automatic notifications when new tickets appear."
                )
                self.send_message(chat_id, welcome)
            
            elif text == "/help" or text == "/help@npl_bot":
                help_text = (
                    "❓ <b>How to Use NPL Ticket Notifier</b>\n\n"
                    "<b>Commands:</b>\n"
                    "• <b>/tickets</b> - View all available tickets\n"
                    "• <b>/start</b> - Welcome message\n"
                    "• <b>/status</b> - Bot status\n"
                    "• <b>/help</b> - This message\n\n"
                    "<b>Features:</b>\n"
                    "✅ Real-time ticket monitoring\n"
                    "✅ Automatic voice alerts\n"
                    "✅ Text notifications with details\n"
                    "✅ Direct Khalti API integration\n\n"
                    "<b>💡 Pro Tips:</b>\n"
                    "• Check /tickets regularly for updates\n"
                    "• Bell notifications ON for immediate alerts\n"
                    "• Share bot with cricket fans in group"
                )
                self.send_message(chat_id, help_text)
            
            elif text == "/status" or text == "/status@npl_bot":
                status = (
                    "✅ <b>Bot Status: ONLINE</b>\n\n"
                    "📊 <b>Info:</b>\n"
                    f"• Monitoring: NPL 2025\n"
                    f"• Event ID: {self.event_id}\n"
                    "• Polling: Active (checks every 30 sec)\n"
                    "• API: Khalti (Direct)\n"
                    "• Status: ✅ Running\n\n"
                    "Use /tickets to check availability"
                )
                self.send_message(chat_id, status)
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def run(self):
        """Start polling for messages"""
        logger.info("=" * 60)
        logger.info("NPL TICKET NOTIFIER BOT (POLLING MODE)")
        logger.info("=" * 60)
        logger.info(f"Bot token: {self.bot_token[:10]}...")
        logger.info(f"Event ID: {self.event_id}")
        logger.info("Status: Running (waiting for commands)")
        logger.info("\nSupported commands:")
        logger.info("  /tickets - Show available tickets")
        logger.info("  /start   - Welcome message")
        logger.info("  /help    - Help information")
        logger.info("  /status  - Bot status")
        logger.info("\nPress Ctrl+C to stop")
        logger.info("=" * 60)
        
        try:
            while True:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update.get("update_id", 0)
                    self.handle_message(update)
                
                # Prevent CPU spinning
                if not updates:
                    time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise


def main():
    """Entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('telegram_bot.log'),
            logging.StreamHandler()
        ]
    )
    
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ TELEGRAM_BOT_TOKEN not configured in environment variables")
        raise ValueError("Set TELEGRAM_BOT_TOKEN in .env file")
    
    bot = PollingBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)
    bot.run()


if __name__ == "__main__":
    main()
