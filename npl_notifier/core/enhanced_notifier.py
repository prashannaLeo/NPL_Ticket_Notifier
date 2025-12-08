"""
Enhanced notification system with retry logic and smart escalation
Ensures you get MAXIMUM alerts when tickets appear
"""

import logging
import time
from typing import Dict, Optional
from .telegram_notifier import TelegramNotifier
from .voice_notifier import VoiceNotifier

logger = logging.getLogger(__name__)


class EnhancedNotifier:
    """Advanced multi-channel notification with escalation"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.telegram = TelegramNotifier(bot_token, chat_id)
        self.voice = VoiceNotifier(bot_token, chat_id)
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    def send_critical_alert(self, ticket_info: Dict) -> bool:
        """Send CRITICAL ALERT with maximum escalation and retries"""
        try:
            logger.warning("🚨 CRITICAL TICKET ALERT - Starting maximum escalation...")
            
            # PHASE 1: Immediate voice alert (highest priority)
            logger.info("Phase 1: Sending voice alerts...")
            for attempt in range(1, self.max_retries + 1):
                if self.voice.send_alert_call(ticket_info):
                    logger.info(f"✓ Voice alert sent (attempt {attempt}/{self.max_retries})")
                    break
                else:
                    logger.warning(f"✗ Voice alert failed (attempt {attempt}/{self.max_retries})")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
            
            time.sleep(1)
            
            # PHASE 2: Push notification (immediate visibility)
            logger.info("Phase 2: Sending push notification...")
            for attempt in range(1, self.max_retries + 1):
                if self.voice.send_push_notification_alert(ticket_info):
                    logger.info(f"✓ Push notification sent (attempt {attempt}/{self.max_retries})")
                    break
                else:
                    logger.warning(f"✗ Push notification failed (attempt {attempt}/{self.max_retries})")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
            
            time.sleep(1)
            
            # PHASE 3: Detailed ticket information with action links
            logger.info("Phase 3: Sending detailed ticket information...")
            for attempt in range(1, self.max_retries + 1):
                if self.telegram.send_urgent_alert(ticket_info):
                    logger.info(f"✓ Detailed alert sent (attempt {attempt}/{self.max_retries})")
                    break
                else:
                    logger.warning(f"✗ Detailed alert failed (attempt {attempt}/{self.max_retries})")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
            
            logger.info("✅ CRITICAL ALERT ESCALATION COMPLETE")
            return True
            
        except Exception as e:
            logger.error(f"Error in critical alert escalation: {e}", exc_info=True)
            return False
    
    def send_availability_reminder(self, ticket_info: Dict, hours_available: int = 1) -> bool:
        """Send reminder notifications if tickets still available after some time"""
        try:
            title = ticket_info.get('title', 'NPL Ticket')
            
            reminder_message = f"""
⏰ <b>REMINDER: TICKETS STILL AVAILABLE!</b>

{title}
Price: {ticket_info.get('price')}

This event may be your LAST CHANCE to get tickets!

🔗 <a href="https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true"><b>BUY NOW BEFORE SOLD OUT</b></a>

⚠️ Supply is LIMITED - Don't miss this opportunity!"""
            
            return self.telegram.send_message(reminder_message)
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return False
    
    def send_quick_action_buttons(self, ticket_info: Dict) -> bool:
        """Send message with quick action buttons for faster purchasing"""
        try:
            import requests
            
            url = f"https://api.telegram.org/bot{self.telegram.bot_token}/sendMessage"
            
            message = f"""
<b>⚡ QUICK ACTION: {ticket_info.get('title')}</b>

Price: {ticket_info.get('price')}
Status: {ticket_info.get('status')}

<b>🎟️ ONE-TAP PURCHASE:</b>
<a href="https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true">🛒 Buy Now (No Registration)</a>

<b>💳 Payment Tips:</b>
✅ Use saved card for instant checkout
✅ Have OTP ready for verification
✅ Complete purchase within 3 minutes"""
            
            payload = {
                "chat_id": self.telegram.chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Quick action message sent")
            return True
            
        except Exception as e:
            logger.error(f"Error sending quick actions: {e}")
            return False


def notify_ticket_alert(bot_token: str, chat_id: str, ticket_info: Dict) -> bool:
    """Convenience function for maximum escalation"""
    notifier = EnhancedNotifier(bot_token, chat_id)
    success = notifier.send_critical_alert(ticket_info)
    
    if success:
        # Optional: Send quick action buttons
        time.sleep(2)
        notifier.send_quick_action_buttons(ticket_info)
    
    return success
