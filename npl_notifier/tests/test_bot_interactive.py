#!/usr/bin/env python3
"""
Simple interactive bot tester - Check available tickets on demand
This allows testing the /tickets command without a full webhook server
"""

import logging
from npl_notifier.bot.telegram_bot import InteractiveBot
from npl_notifier.core.config import TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID, TELEGRAM_CHAT_ID

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Interactive bot tester"""
    bot = InteractiveBot(TELEGRAM_BOT_TOKEN, KHALTI_EVENT_ID)
    
    print("\n" + "="*60)
    print("NPL TICKET NOTIFIER - INTERACTIVE BOT TESTER")
    print("="*60)
    print("\nAvailable commands:")
    print("  /tickets - Show all available tickets")
    print("  /start   - Show welcome message")
    print("  /help    - Show help message")
    print("  /test    - Send test message to your chat")
    print("  /quit    - Exit\n")
    
    while True:
        try:
            command = input("Enter command: ").strip()
            
            if not command:
                continue
            
            if command.lower() == '/quit':
                print("Goodbye!")
                break
            
            elif command.lower() == '/test':
                # Send test message to configured chat
                test_msg = "✅ Bot is working! Your Telegram bot is properly configured."
                bot.send_message(TELEGRAM_CHAT_ID, test_msg)
                print("✓ Test message sent!")
            
            elif command.lower().startswith('/'):
                # Handle command
                print("\n" + "-"*60)
                message = bot.get_available_tickets_message() if command.lower() == '/tickets' else None
                
                if command.lower() == '/tickets':
                    print(message)
                elif command.lower() == '/start':
                    start_msg = (
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
                    print(start_msg)
                elif command.lower() == '/help':
                    help_msg = (
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
                    print(help_msg)
                else:
                    print("Unknown command. Type /help for available commands.")
                print("-"*60 + "\n")
            
            else:
                print("Please enter a command starting with / (e.g., /tickets)\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
