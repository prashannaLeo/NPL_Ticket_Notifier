"""
Voice call notifier using Telegram bot
Sends voice message alerts when tickets become available
"""

import requests
import logging
from typing import Optional
from io import BytesIO

logger = logging.getLogger(__name__)


class VoiceNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_voice_message(self, text: str) -> bool:
        """Send a voice message via Telegram using text-to-speech"""
        try:
            # Use Google Text-to-Speech to create audio
            from gtts import gTTS
            
            # Create voice message
            tts = gTTS(text=text, lang='en', slow=False)
            voice_buffer = BytesIO()
            tts.write_to_fp(voice_buffer)
            voice_buffer.seek(0)
            
            # Send voice message
            url = f"{self.api_url}/sendVoice"
            files = {'voice': ('ticket_alert.mp3', voice_buffer, 'audio/mpeg')}
            data = {'chat_id': self.chat_id}
            
            response = requests.post(url, files=files, data=data, timeout=10)
            response.raise_for_status()
            logger.info("Voice message sent successfully")
            return True
            
        except ImportError:
            logger.warning("gTTS not installed. Install with: pip install gtts")
            return False
        except requests.RequestException as e:
            logger.error(f"Error sending voice message: {e}")
            return False
        except Exception as e:
            logger.error(f"Error generating voice message: {e}")
            return False

    def send_alert_call(self, ticket_info: dict) -> bool:
        """Send an urgent voice alert about ticket availability"""
        try:
            title = ticket_info.get('title', 'NPL Ticket')
            status = ticket_info.get('status', 'Available')
            price = ticket_info.get('price', 'unknown price')
            
            # Create HIGHLY URGENT voice alert message with repeat emphasis
            alert_text = f"CRITICAL ALERT! CRITICAL ALERT! {title} tickets are NOW AVAILABLE. Price: {price}. Limited quantity! Go to Khalti NOW! CRITICAL ALERT!"
            
            logger.info(f"Sending URGENT voice alert for: {title}")
            result = self.send_voice_message(alert_text)
            
            # Send loud push notification too
            self.send_push_notification_alert(ticket_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Error sending alert call: {e}")
            return False

    def send_push_notification_alert(self, ticket_info: dict) -> bool:
        """Send loud push notification with maximum urgency"""
        try:
            url = f"{self.api_url}/sendMessage"
            
            title = ticket_info.get('title', 'NPL Ticket')
            
            payload = {
                "chat_id": self.chat_id,
                "text": "🚨🚨🚨 URGENT! TICKETS AVAILABLE! 🚨🚨🚨\n\n" + 
                        f"⚡ {title} IS NOW ON SALE\n" +
                        "⏱️ LIMITED TIME - BUY NOW!\n" +
                        "🔔 Check full details above",
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Push notification alert sent with maximum urgency")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Error sending push notification: {e}")
            return False

    def send_phone_call_trigger(self) -> bool:
        """Trigger a phone call notification (alternative using Telegram)"""
        try:
            # Send urgent message with sound notification
            url = f"{self.api_url}/sendMessage"
            
            payload = {
                "chat_id": self.chat_id,
                "text": "🚨 TICKET ALERT! Check above for available NPL tickets!",
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Alert notification sent")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Error sending alert notification: {e}")
            return False
