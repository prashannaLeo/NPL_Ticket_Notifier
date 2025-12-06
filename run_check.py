#!/usr/bin/env python3
"""
GitHub Actions runner script for NPL Ticket Notifier
Minimal, focused script for automated ticket checking
"""

import os
import sys
import logging
from datetime import datetime
from scraper import KhaltiScraper
from telegram_notifier import TelegramNotifier
from voice_notifier import VoiceNotifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('check_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Check for tickets and notify"""
    logger.info("="*60)
    logger.info("NPL Ticket Checker (GitHub Actions)")
    logger.info("="*60)
    
    # Load credentials from environment
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    event_id = os.getenv('KHALTI_EVENT_ID')
    
    # Validate credentials
    if not all([bot_token, chat_id, event_id]):
        logger.error("Missing required environment variables:")
        logger.error(f"  TELEGRAM_BOT_TOKEN: {'✓' if bot_token else '✗'}")
        logger.error(f"  TELEGRAM_CHAT_ID: {'✓' if chat_id else '✗'}")
        logger.error(f"  KHALTI_EVENT_ID: {'✓' if event_id else '✗'}")
        return 1
        logger.error(f"  TELEGRAM_CHAT_ID: {'✓' if chat_id else '✗'}")
        logger.error(f"  KHALTI_EVENT_URL: {'✓' if khalti_url else '✗'}")
        return 1
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        scraper = KhaltiScraper(event_id)
        text_notifier = TelegramNotifier(bot_token, chat_id)
        voice_notifier = VoiceNotifier(bot_token, chat_id)
        
        # Check for tickets
        logger.info("Checking for available tickets...")
        available_tickets = scraper.get_available_tickets()
        
        if not available_tickets:
            logger.info("✓ No available tickets at this time")
            return 0
        
        # Send notifications
        logger.info(f"✓ Found {len(available_tickets)} available ticket(s)")
        
        for i, ticket in enumerate(available_tickets, 1):
            logger.info(f"\n[{i}] {ticket.get('title')}")
            logger.info(f"    Status: {ticket.get('status')}")
            logger.info(f"    Price: {ticket.get('price')}")
            
            # Send voice alert
            logger.info("    Sending voice alert...")
            voice_notifier.send_alert_call(ticket)
            
            # Wait a bit
            import time
            time.sleep(1)
            
            # Send text notification
            logger.info("    Sending text notification...")
            text_notifier.send_ticket_notification(ticket)
            
            time.sleep(1)
        
        logger.info("\n✓ All notifications sent successfully")
        return 0
        
    except Exception as e:
        logger.error(f"✗ Error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
