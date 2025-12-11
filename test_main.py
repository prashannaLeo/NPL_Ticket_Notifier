#!/usr/bin/env python3
"""
Quick test of main.py functionality without infinite loop
"""

import sys
import logging
from datetime import datetime
from npl_notifier.core.scraper import KhaltiScraper
from npl_notifier.core.telegram_notifier import TelegramNotifier
from npl_notifier.core.voice_notifier import VoiceNotifier
from npl_notifier.core.config import (
    KHALTI_EVENT_ID,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_main_components():
    """Test main.py components"""
    logger.info("=" * 60)
    logger.info("TESTING NPL TICKET NOTIFIER - MAIN COMPONENTS")
    logger.info("=" * 60)
    
    try:
        # Test 1: Configuration
        logger.info("\n✓ Test 1: Configuration")
        logger.info(f"  Event ID: {KHALTI_EVENT_ID}")
        logger.info(f"  Bot Token: {TELEGRAM_BOT_TOKEN[:20] if TELEGRAM_BOT_TOKEN else 'NOT SET'}...")
        logger.info(f"  Chat ID: {TELEGRAM_CHAT_ID}")
        
        # Test 2: Scraper
        logger.info("\n✓ Test 2: KhaltiScraper")
        scraper = KhaltiScraper(KHALTI_EVENT_ID)
        logger.info(f"  Scraper initialized successfully")
        
        # Test 3: Get available tickets
        logger.info("\n✓ Test 3: API Query - Get Available Tickets")
        available_tickets = scraper.get_available_tickets()
        
        if available_tickets:
            logger.info(f"  ✓ Found {len(available_tickets)} available ticket(s)")
            for i, ticket in enumerate(available_tickets, 1):
                logger.info(f"    [{i}] {ticket.get('title', 'N/A')}")
                logger.info(f"        Status: {ticket.get('status', 'N/A')}")
                logger.info(f"        Price: {ticket.get('price', 'N/A')}")
        else:
            logger.info(f"  ✓ No available tickets at this time (normal)")
        
        # Test 4: Telegram Notifier
        logger.info("\n✓ Test 4: TelegramNotifier")
        notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        logger.info(f"  Notifier initialized successfully")
        
        # Test 5: Voice Notifier
        logger.info("\n✓ Test 5: VoiceNotifier")
        voice_notifier = VoiceNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        logger.info(f"  Voice notifier initialized successfully")
        
        # Test 6: Test message formatting
        logger.info("\n✓ Test 6: Message Formatting")
        if available_tickets:
            ticket = available_tickets[0]
            formatted_msg = notifier._format_ticket_message(ticket)
            logger.info(f"  Message formatted successfully ({len(formatted_msg)} chars)")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ ALL TESTS PASSED - SYSTEM READY")
        logger.info("=" * 60)
        logger.info("\nNext: Run 'python main.py' for continuous monitoring")
        logger.info("      Run 'python run_check.py' for one-time check")
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Test failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(test_main_components())
