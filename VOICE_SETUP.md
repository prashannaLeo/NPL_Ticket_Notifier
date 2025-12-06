# 🔊 Voice Alerts - Quick Setup (5 minutes)

## What You Get

When tickets are available:
1. **🔊 Voice Alert**: Automatic voice message with ticket details
2. **📱 Text Message**: Detailed message with price and link
3. **⏰ Every Check**: New alerts if new tickets appear

## Setup Steps

### Step 1: Install Voice Library (1 minute)
```bash
pip install gtts
```

### Step 2: Configure Telegram (Already Done!)
Your Telegram bot is already configured in `config.py`:
```python
TELEGRAM_BOT_TOKEN = "AAGCivJZviOUFoD83yU6wHyuz13uF_ZrBdc"
TELEGRAM_CHAT_ID = "8308605097"
```

### Step 3: Start Monitoring (Now!)
```bash
python main.py
```

That's it! 🎉

## What Happens

```
When you run: python main.py

Every 60 seconds:
├─ Check Khalti API for tickets
├─ If new tickets found:
│  ├─ Generate voice message (gTTS)
│  ├─ Send voice audio to Telegram 🔊
│  └─ Send detailed text message 📱
└─ Check again in 60 seconds
```

## Example Alert You'll Receive

**Voice Message (audio):**
> "URGENT ALERT! NPL 2025 7th Dec Karnali Yaks Versus Janakpur Bolts is now Available. Price is Rs. 500 to 1000. Check your Telegram for details."

**Text Message (detailed):**
```
🎫 NPL TICKET ALERT!

Event: NPL 2025 7th Dec
Dates: Sun, 07 Dec
Venue: TU Cricket Ground, Kritipur
Status: Available
Price: Rs. 500 - Rs. 1000

🔗 Get your tickets now:
https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
```

## Testing

### Test Voice Alerts:
```bash
python test_voice_alerts.py
```

### Test Full System:
```bash
python test_integration.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Voice not working | Install gtts: `pip install gtts` |
| No audio in Telegram | Check internet connection |
| Not receiving messages | Verify bot token in `config.py` |
| Text works but not voice | gtts generates voice automatically |

## Features

✅ Automatic voice generation with gTTS
✅ Sends voice as Telegram audio message
✅ Fallback to text if voice fails
✅ Zero configuration needed (already set up!)
✅ Works 24/7 when you run `python main.py`

## Running in Background

To keep monitoring even when terminal closes:

### Windows - Create batch file `run_notifier.bat`:
```batch
@echo off
cd /d "c:\dev\python\NPL_ticket_notifier"
venv\bin\python.exe main.py
pause
```

Then double-click `run_notifier.bat`

### Linux/Mac - Use screen or tmux:
```bash
screen -S notifier
python main.py
# Press Ctrl+A then D to detach
```

## Disabling Voice Alerts

If you only want text messages, edit `main.py` and comment out:
```python
# self.voice_notifier.send_alert_call(ticket)
```

## More Info

See `VOICE_ALERTS.md` for complete documentation.

---

**You're all set!** Run `python main.py` and you'll get voice alerts as soon as tickets are available! 🎉
