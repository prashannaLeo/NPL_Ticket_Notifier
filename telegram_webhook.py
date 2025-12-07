#!/usr/bin/env python3
"""
Webhook handler for Telegram bot commands
Run this as a separate service to handle incoming messages
Usage: python telegram_webhook.py
"""

import logging
import json
import os
from flask import Flask, request
from telegram_bot import InteractiveBot
from config import TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_webhook.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = InteractiveBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)

# Webhook secret for validation
WEBHOOK_SECRET = os.getenv('TELEGRAM_WEBHOOK_SECRET', 'npl-tickets-secret')


@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    """Handle incoming Telegram messages"""
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Empty request received")
            return {'ok': False, 'error': 'Empty request'}, 400
        
        logger.info(f"Received update: {json.dumps(data, indent=2)}")
        
        # Check if this is a message update
        if 'message' not in data:
            logger.debug("Not a message update, ignoring")
            return {'ok': True}, 200
        
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()
        
        if not text:
            logger.warning("Empty message text")
            return {'ok': True}, 200
        
        logger.info(f"Message from {chat_id}: {text}")
        
        # Check if message is a command
        if text.startswith('/'):
            bot.handle_command(chat_id, text)
        else:
            # Non-command message - send help
            response = (
                "📌 I'm a ticket notification bot!\n\n"
                "Use `/tickets` to see available tickets\n"
                "Use `/help` for more information"
            )
            bot.send_message(chat_id, response)
        
        return {'ok': True}, 200
    
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
        return {'ok': False, 'error': str(e)}, 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'service': 'telegram-webhook'}, 200


@app.route('/', methods=['GET'])
def index():
    """Index endpoint"""
    return {
        'service': 'NPL Ticket Notifier Bot',
        'version': '1.0',
        'endpoints': [
            'POST /telegram - Webhook for Telegram updates',
            'GET /health - Health check'
        ]
    }, 200


if __name__ == '__main__':
    logger.info("Starting Telegram webhook server...")
    logger.info("Listening on http://localhost:5000")
    logger.info("Telegram webhook: http://localhost:5000/telegram")
    
    # For production, use a proper WSGI server like gunicorn
    # Development mode:
    app.run(host='0.0.0.0', port=5000, debug=False)
