#!/usr/bin/env python3
"""
Persistent Telegram Bot for GitHub Actions
This keeps the bot running continuously, listening for commands
Uses long polling to stay connected without webhooks
"""

import logging
import requests
import time
import sys
import os
from npl_notifier.core.scraper import KhaltiScraper
from npl_notifier.core.config import KHALTI_EVENT_ID, TELEGRAM_BOT_TOKEN

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PersistentBot:
    """Bot that runs continuously on GitHub Actions"""
    
    def __init__(self, bot_token: str, event_id: str):
        self.bot_token = bot_token
        self.event_id = event_id
        self.scraper = KhaltiScraper(event_id)
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_update_id = 0
        self.poll_timeout = 1  # 1 second timeout for fast response
        
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
                return "No available tickets at the moment.\n\nAll tickets are currently sold out."
            
            message = "<b>AVAILABLE TICKETS</b>\n\n"
            
            for i, ticket in enumerate(available_tickets[:5], 1):
                title = ticket.get('title', 'N/A')
                date = ticket.get('dates') or ticket.get('date', 'N/A')
                location = ticket.get('venue') or ticket.get('location', 'N/A')
                price = ticket.get('price', 'N/A')
                
                message += f"<b>{i}. {title}</b>\n"
                message += f"Date: {date}\n"
                message += f"Location: {location}\n"
                message += f"Price: {price}\n"
                message += f"<a href=\"https://events.khalti.com/events/{self.event_id}\">Get tickets</a>\n\n"
            
            return message
        
        except Exception as e:
            logger.error(f"Error fetching tickets: {e}")
            return f"Error fetching tickets: {str(e)}"
    
    def handle_message(self, update: dict):
        """Handle incoming message"""
        try:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "").strip()
            
            if not chat_id or not text:
                return
            
            user = message.get("from", {})
            username = user.get("username", "Unknown")
            logger.info(f"Message from @{username}: {text}")
            
            # Handle commands
            if text.startswith("/tickets"):
                logger.info(f"Sending tickets list to {chat_id}")
                self.send_message(chat_id, self.get_available_tickets_message())
            
            elif text.startswith("/start"):
                welcome = (
                    "<b>Welcome to NPL Ticket Notifier</b>\n\n"
                    "<b>Available Commands:</b>\n"
                    "/tickets - Show available NPL tickets\n"
                    "/help - Get help\n"
                    "/status - Check bot status\n\n"
                    "This bot monitors Khalti API for ticket availability."
                )
                self.send_message(chat_id, welcome)
            
            elif text.startswith("/help"):
                help_text = (
                    "<b>NPL Ticket Notifier Help</b>\n\n"
                    "Commands:\n"
                    "/tickets - View all available tickets\n"
                    "/start - Welcome message\n"
                    "/status - Bot status\n"
                    "/help - This message\n\n"
                    "Features: Real-time monitoring, Voice alerts, Text notifications"
                )
                self.send_message(chat_id, help_text)
            
            elif text.startswith("/status"):
                status = (
                    "<b>Bot Status: ONLINE</b>\n\n"
                    f"Event: NPL 2025\n"
                    f"Event ID: {self.event_id}\n"
                    "Status: Running on GitHub Actions\n\n"
                    "Use /tickets to check availability"
                )
                self.send_message(chat_id, status)
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def run(self, max_duration_seconds=240):
        """Run the bot for a limited duration (GitHub Actions constraint)
        4 minutes per job × 60 jobs/hour = near-continuous coverage"""
        logger.info("=" * 60)
        logger.info("NPL TICKET NOTIFIER BOT (GitHub Actions - Persistent)")
        logger.info("=" * 60)
        logger.info(f"Bot token: {self.bot_token[:10]}...")
        logger.info(f"Event ID: {self.event_id}")
        logger.info(f"Max duration: {max_duration_seconds} seconds")
        logger.info("Status: Listening for commands...")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        try:
            while True:
                # Check if we've exceeded max duration
                elapsed = time.time() - start_time
                if elapsed > max_duration_seconds:
                    logger.info(f"Max duration reached ({max_duration_seconds}s). Exiting gracefully.")
                    break
                
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update.get("update_id", 0)
                    self.handle_message(update)
                
                # Prevent CPU spinning
                if not updates:
                    time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise
        finally:
            logger.info("Bot shutdown complete")


def main():
    """Entry point"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("TELEGRAM_BOT_TOKEN not configured")
        raise ValueError("Set TELEGRAM_BOT_TOKEN in environment")
    
    bot = PersistentBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)
    
    # Run for 30 minutes (GitHub Actions will restart the job)
    # This creates a continuous loop across multiple runs
    bot.run(max_duration_seconds=1800)


if __name__ == "__main__":
    main()
