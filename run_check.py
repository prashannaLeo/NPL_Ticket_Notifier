#!/usr/bin/env python3
"""
GitHub Actions runner script for NPL Ticket Notifier
Minimal, focused script for automated ticket checking
Uses Telegram message search to detect duplicate notifications
"""

import os
import sys
import logging
import json
import time
from datetime import datetime, timedelta
from npl_notifier.core.scraper import KhaltiScraper
from npl_notifier.core.telegram_notifier import TelegramNotifier
from npl_notifier.core.voice_notifier import VoiceNotifier
from npl_notifier.core.enhanced_notifier import notify_ticket_alert

# Fix Unicode encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup logging with Unicode support
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('check_log.txt', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_ticket_hash(ticket_info: dict) -> str:
    """Create a unique hash for a ticket"""
    date_field = ticket_info.get('dates') or ticket_info.get('date', '')
    return f"{ticket_info['title']}_{date_field}_{ticket_info.get('price', '')}"

def load_ticket_history() -> set:
    """Load previously notified tickets from persistent storage"""
    # GitHub Actions: Read from artifact or git
    history_file = 'notified_tickets.json'
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                data = json.load(f)
                logger.info(f"✓ Loaded {len(data)} previously notified tickets from {history_file}")
                return set(data)
        except Exception as e:
            logger.warning(f"Could not load ticket history: {e}")
    else:
        logger.info("No ticket history found - first run or fresh environment")
    
    return set()

def save_ticket_history(notified: set):
    """Save notified tickets to persistent storage"""
    try:
        with open('notified_tickets.json', 'w') as f:
            json.dump(list(notified), f, indent=2)
        logger.info(f"✓ Saved {len(notified)} tickets to history")
        
        # Also append to git for version control
        _save_to_git(notified)
    except Exception as e:
        logger.error(f"Could not save ticket history: {e}")

def _save_to_git(notified: set):
    """Optionally commit and push history to git"""
    try:
        import subprocess
        if os.path.exists('.git'):
            subprocess.run(['git', 'config', 'user.email', 'github-actions@bot.local'], 
                          check=False, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'GitHub Actions'], 
                          check=False, capture_output=True)
            subprocess.run(['git', 'add', 'notified_tickets.json'], 
                          check=False, capture_output=True)
            result = subprocess.run(['git', 'commit', '-m', 'Update ticket history'], 
                                   check=False, capture_output=True)
            if result.returncode == 0:
                logger.info("✓ Committed ticket history to git")
    except Exception as e:
        logger.debug(f"Could not save to git: {e}")

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
        # Load ticket history
        logger.info("Loading ticket history...")
        notified_tickets = load_ticket_history()
        
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
        
        # Check for NEW tickets only
        logger.info(f"✓ Found {len(available_tickets)} available ticket(s)")
        new_tickets_found = False
        
        for i, ticket in enumerate(available_tickets, 1):
            ticket_hash = get_ticket_hash(ticket)
            
            logger.info(f"\n[{i}] {ticket.get('title')}")
            logger.info(f"    Status: {ticket.get('status')}")
            logger.info(f"    Price: {ticket.get('price')}")
            
            # Only notify about NEW tickets
            if ticket_hash not in notified_tickets:
                logger.info("    ⭐ NEW TICKET - Sending MAXIMUM ESCALATION alerts...")
                new_tickets_found = True
                
                # Use enhanced critical alert system with full escalation
                notify_ticket_alert(bot_token, chat_id, ticket)
                
                # Track this ticket
                notified_tickets.add(ticket_hash)
                save_ticket_history(notified_tickets)
                time.sleep(3)
            else:
                logger.info("    ℹ️  Already notified about this ticket - skipping")
        
        if new_tickets_found:
            logger.info("\n✓ New ticket notifications sent successfully")
        else:
            logger.info("\n✓ No new tickets found (same as before)")
        return 0
        
    except Exception as e:
        logger.error(f"✗ Error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
