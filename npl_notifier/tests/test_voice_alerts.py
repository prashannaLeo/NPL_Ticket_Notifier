"""
Demo script to test voice alert functionality
"""

import logging
from npl_notifier.core.voice_notifier import VoiceNotifier
from npl_notifier.core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_voice_alerts():
    """Test voice alert system"""
    
    # Initialize voice notifier
    voice_notifier = VoiceNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Sample ticket info
    sample_ticket = {
        'title': 'NPL 2025 7th Dec (Karnali Yaks Vs Janakpur Bolts)',
        'date': 'Sun, 07 Dec',
        'location': 'TU Cricket Ground, Kritipur',
        'status': 'Available',
        'price': 'Rs. 500 - Rs. 1000'
    }
    
    logger.info("Testing voice alert system...")
    logger.info("\n=== Test 1: Voice Alert Call ===")
    result1 = voice_notifier.send_alert_call(sample_ticket)
    if result1:
        logger.info("✓ Voice alert sent successfully!")
    else:
        logger.warning("✗ Voice alert failed (gtts may need internet connection)")
    
    logger.info("\n=== Test 2: Urgent Phone Call Trigger ===")
    result2 = voice_notifier.send_phone_call_trigger()
    if result2:
        logger.info("✓ Phone call trigger sent successfully!")
    else:
        logger.warning("✗ Phone call trigger failed")
    
    logger.info("\n=== Available Voice Alert Features ===")
    logger.info("1. send_alert_call(ticket_info) - Converts ticket details to voice message")
    logger.info("2. send_phone_call_trigger() - Sends urgent notification with sound")
    logger.info("3. send_voice_message(text) - Sends custom voice message")

if __name__ == "__main__":
    test_voice_alerts()
