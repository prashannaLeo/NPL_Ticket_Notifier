# Interactive Bot Commands - NPL Ticket Notifier

## Overview

The bot now supports interactive commands that allow users to check ticket availability on demand, without waiting for automatic notifications.

## Available Commands

### `/tickets`
**Show all currently available tickets**

- Displays formatted list of available NPL tickets
- Shows: Title, Date, Location, Price, Status
- Direct link to book tickets
- Updates in real-time

Example response:
```
🎫 AVAILABLE TICKETS

1. NPL 2025 7th Dec (Karnali Yaks Vs Janakpur Bolts)
📅 Date: Sun, 07 Dec
📍 Location: TU Cricket Ground, Kritipur
💰 Price: Rs. 500 - Rs. 1000
✅ Status: Available
🔗 Book: https://events.khalti.com/events/ET25AMY4AUYM
```

### `/start`
**Welcome message with command overview**

- Introduces the bot
- Lists available commands
- Explains auto-notification feature
- Quick start guide

### `/help`
**Detailed help information**

- Complete command reference
- How the bot works (step-by-step)
- Check frequency information
- Pro tips for getting tickets faster

---

## How to Use

### Option 1: Local Testing (Terminal)
Test commands without webhook setup:

```bash
& "venv\bin\python.exe" test_bot_interactive.py
```

Then type commands:
```
Enter command: /tickets
```

### Option 2: Telegram Bot (Production)

#### Setup Steps:

1. **Get your Bot Token** (already have it)
   - Token format: `123456789:ABCDEFGHIjklmnopqrst...`

2. **Set webhook URL** (requires public URL)
   - Use Ngrok for local testing: `ngrok http 5000`
   - Use production server for deployment

3. **Send Telegram message**
   ```
   Message: /tickets
   Bot responds with available tickets
   ```

---

## Technical Implementation

### Files Added

1. **`telegram_bot.py`**
   - `InteractiveBot` class
   - `handle_command()` - Processes /tickets, /start, /help
   - `get_available_tickets_message()` - Formats ticket list
   - `send_message()` - Sends formatted Telegram messages

2. **`telegram_webhook.py`**
   - Flask web server for receiving Telegram updates
   - Webhook endpoint: `POST /telegram`
   - Health check: `GET /health`
   - Message routing to commands

3. **`test_bot_interactive.py`**
   - Interactive command tester (local)
   - No server/webhook needed
   - Useful for testing before deployment

### Updated Files

- **`requirements.txt`** - Added `flask>=2.3.0`

---

## Deployment Options

### Option A: Polling (Recommended for Simple Setup)
Bot continuously polls for updates (no webhook needed):

```bash
python run_polling_bot.py
```

Simpler but slightly slower (100-200ms delay).

### Option B: Webhook (Production)
Bot receives updates via webhook (faster, 0-50ms delay):

```bash
# Install Flask (if not already installed)
pip install flask

# Run webhook server
python telegram_webhook.py

# Set Telegram webhook:
curl https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://your-domain.com/telegram
```

---

## Integration with Existing Features

✅ **Existing Features Unchanged:**
- Automatic ticket monitoring (still runs every 1 minute)
- Voice alerts (still sent when new tickets appear)
- Text notifications (still sent)
- Ticket history tracking (still prevents duplicates)
- GitHub Actions automation (still running)

✅ **New Features:**
- On-demand `/tickets` command
- Interactive `/start` and `/help`
- Real-time ticket availability checks

---

## Example Usage

### User Journey:

1. **Receive notification**
   ```
   🔊 [Voice Alert]: New NPL tickets available!
   
   🎫 NPL Ticket Alert!
   Event: NPL 2025 7th Dec...
   ```

2. **Check manually anytime**
   ```
   User: /tickets
   Bot: 🎫 AVAILABLE TICKETS
        1. NPL 2025 7th Dec...
        Price: Rs. 500-1000
   ```

3. **Get help**
   ```
   User: /help
   Bot: 📖 Help - NPL Ticket Notifier Bot...
   ```

---

## Troubleshooting

### Bot doesn't respond to commands

1. **Check if bot token is valid**
   ```bash
   # Test bot token
   curl https://api.telegram.org/botYOUR_TOKEN/getMe
   ```

2. **Verify bot can send messages**
   ```bash
   python test_bot_interactive.py
   # Use /test command
   ```

3. **For webhook:** Ensure firewall allows incoming connections

### /tickets shows no available tickets
- All tickets might be sold out
- Try again in a few minutes
- Set up automatic notifications so you don't miss them

### Commands not recognized
- Ensure message starts with `/` (slash)
- Try: `/help` or `/tickets`
- Case-insensitive (works with both `/Tickets` and `/tickets`)

---

## Command Reference

| Command | Function | Response Time |
|---------|----------|---|
| `/tickets` | Show available tickets | 1-2 seconds |
| `/start` | Welcome message | Instant |
| `/help` | Help information | Instant |
| Any text | Info message | Instant |

---

## Monitoring

### View webhook logs:
```bash
Get-Content telegram_webhook.log -Tail 20
```

### Check Flask server health:
```bash
curl http://localhost:5000/health
```

### Monitor incoming messages:
```bash
Get-Content telegram_webhook.log -Tail 50 -Wait
```

---

## Future Enhancements

Possible additions (without changing current features):
- ✨ `/notify` - Configure notification preferences
- ✨ `/status` - Show bot status and last check time
- ✨ `/history` - Show notification history
- ✨ Inline button "Check Tickets Now" in auto-notifications

---

## Summary

✅ **Simple to use** - Just send `/tickets`
✅ **Always available** - Works 24/7
✅ **Real-time** - Checks live Khalti API
✅ **No breaking changes** - Existing features untouched
✅ **Easy integration** - Use webhook or polling
