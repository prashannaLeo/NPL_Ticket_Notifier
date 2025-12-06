# Voice Call Alerts - NPL Ticket Notifier

## Overview

The NPL Ticket Notifier now includes **voice call alerts** to notify you immediately when tickets become available. This ensures you never miss a ticket opportunity!

## How It Works

When tickets are available, the system:

1. **Generates a voice message** with ticket details using Google Text-to-Speech (gTTS)
2. **Sends the voice alert** via Telegram as an audio message
3. **Follows up with a detailed message** containing full ticket information and purchase link

## Features

### 1. Voice Alert Calls
- Converts ticket information into a natural-sounding voice message
- Sends via Telegram voice message (plays audio in Telegram app)
- Includes: ticket title, status, and price

**Example voice message:**
```
"URGENT ALERT! NPL 2025 7th Dec (Karnali Yaks Vs Janakpur Bolts) is now Available. 
Price is Rs. 500 - Rs. 1000. Check your Telegram for details."
```

### 2. Urgent Phone Call Trigger
- Sends an urgent notification message with sound
- Gets your attention immediately in Telegram
- Can be triggered separately if needed

### 3. Custom Voice Messages
- Send any custom text as a voice message
- Useful for custom alerts or testing

## Installation

Voice alerts require the `gtts` library. Install it:

```bash
pip install gtts
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Usage

### Automatic (Integrated in main.py)

Voice alerts are automatically sent when tickets are detected:

```bash
python main.py
```

The notifier will:
1. Check for available tickets
2. Send voice alert (if gtts is available)
3. Send detailed text message
4. Mark ticket as notified to avoid duplicates

### Manual Testing

Test the voice alert system:

```bash
python test_voice_alerts.py
```

### Programmatic Usage

```python
from voice_notifier import VoiceNotifier
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Initialize
voice_notifier = VoiceNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

# Send voice alert for a ticket
ticket = {
    'title': 'NPL Season Ticket 2025',
    'status': 'Available',
    'price': 'Rs. 15000'
}
voice_notifier.send_alert_call(ticket)

# Send custom voice message
voice_notifier.send_voice_message("Your custom alert message here")

# Send urgent phone trigger
voice_notifier.send_phone_call_trigger()
```

## Configuration

Voice alerts work with your existing Telegram configuration in `config.py`:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Your Telegram bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"     # Your Telegram chat ID
```

No additional configuration needed!

## Requirements

- **Internet Connection**: Required for gTTS to generate voice audio
- **Telegram Bot**: Must have a valid Telegram bot token and chat ID
- **Python 3.7+**: Required for all functionality
- **gtts library**: `pip install gtts`

## Troubleshooting

### Voice Alert Not Working?

1. **Check gtts installation:**
   ```bash
   pip list | grep gtts
   ```

2. **Check internet connection**: gTTS requires internet to generate voice audio

3. **Check Telegram configuration**: Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `config.py`

4. **Check logs**: Look at `ticket_notifier.log` for error messages

### Fallback Behavior

If voice alerts fail:
- System automatically falls back to text message notifications
- No tickets will be missed - you'll still get the detailed text message
- Check logs to diagnose the issue

## Audio Quality

The generated voice messages use:
- **Language**: English
- **Speed**: Normal (not slow)
- **Provider**: Google Text-to-Speech
- **Format**: MP3 audio (playable in Telegram)

## Notification Flow

```
┌─────────────────────────────────────────┐
│   Check for Available Tickets (API)     │
└──────────────┬──────────────────────────┘
               │
               ├─ No tickets found → Loop continues
               │
               └─ Tickets found ↓
                  ┌──────────────────────────────┐
                  │ Send Voice Alert (if gtts OK) │ 🔊
                  └──────────────┬───────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │ Send Detailed Text Message  │ 📱
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │ Mark as Notified (no dups)  │ ✓
                  └──────────────────────────────┘
```

## Performance Impact

- Voice generation: ~2-3 seconds per alert (cached by gTTS)
- Voice upload to Telegram: ~1-2 seconds
- **Total**: ~3-5 seconds per voice alert
- System remains responsive while sending alerts

## Multiple Tickets

If multiple tickets are available:
- Each ticket gets its own voice alert
- Alerts are sent sequentially with 1-second delays
- Prevents rate-limiting by Telegram API

## Examples

### Example 1: Automatic Voice Alert

```bash
$ python main.py

INFO - Starting NPL Ticket Notifier...
INFO - Monitoring: https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
INFO - Checking for available tickets...
INFO - Found 2 available ticket(s)
INFO - Sending notification for: NPL 2025 7th Dec...
INFO - Sending voice alert for: NPL 2025 7th Dec...
INFO - Voice message sent successfully
INFO - Message sent successfully
```

In Telegram, you'll receive:
1. 🔊 Voice message: "URGENT ALERT! NPL 2025 7th Dec is now Available..."
2. 📱 Detailed message with price, venue, and ticket link

## Disabling Voice Alerts

If you want text notifications only:

1. **Option 1**: Remove `voice_notifier` from main.py
2. **Option 2**: Uninstall gtts (system will gracefully fall back to text)
3. **Option 3**: Modify `check_and_notify()` in main.py to skip voice alerts

## Future Enhancements

Potential improvements:
- [ ] Custom voice message templates
- [ ] Different alert sounds for different ticket types
- [ ] Voice message in local language (Nepali)
- [ ] Integration with actual phone calls (Twilio, etc.)
- [ ] Adjustable voice speed/tone

## Support

For issues with voice alerts:
1. Check `ticket_notifier.log` for detailed error messages
2. Verify gtts is installed: `pip install gtts`
3. Test internet connection
4. Verify Telegram credentials in `config.py`
