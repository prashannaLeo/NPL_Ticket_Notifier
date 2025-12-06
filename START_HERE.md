# QUICKSTART GUIDE - NPL Ticket Notifier

## 🎯 What This Does

Monitors the Khalti events API for NPL cricket tickets and automatically sends you a **Telegram notification** as soon as tickets become available.

## ✅ Current Status

✓ **The application is fully working and ready to use!**

The script can:
- Monitor the Khalti API continuously for ticket availability
- Send formatted Telegram messages with ticket details
- Send voice alerts via Telegram when tickets appear
- Log all activities for troubleshooting
- Avoid duplicate notifications

## 🚀 Get Started in 3 Steps

### Step 1: Configure Telegram (5 minutes)

**Get your Bot Token:**
1. Open Telegram app
2. Search for `@BotFather`
3. Click "Start"
4. Send message: `/newbot`
5. Follow the prompts to create a bot
6. Copy the token you receive (looks like: `123456:ABC-DEF...`)

**Get your Chat ID:**
1. Search for `@userinfobot` in Telegram
2. Click "Start"
3. Copy the Chat ID number it shows (like: `123456789`)

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root with your credentials:

```env
KHALTI_EVENT_ID=ET25AMY4AUYM
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
CHECK_INTERVAL_SECONDS=60
TIMEOUT_SECONDS=10
```

**Or copy from template:**
```bash
Copy-Item .env.example .env
# Then edit .env and add your credentials
```

### Step 3: Run the Notifier

```bash
python main.py
```

You should see:
```
Starting NPL Ticket Notifier...
Monitoring event: ET25AMY4AUYM
API endpoint: https://khalti.com/api/e5/events/ET25AMY4AUYM/children/
Check interval: 60 seconds
Checking for available tickets...
```

That's it! The notifier is now running and will send you a Telegram message when tickets are available.

**To stop it:** Press `Ctrl+C`

---

## 📱 What You'll Receive

When tickets are found, you'll get a Telegram **voice alert** and a message like:

```
🎫 NPL TICKET ALERT!

Event: NPL Season Ticket 2025
Dates: Mon, 17 Nov - Sat, 13 Dec
Venue: TU Cricket Ground, Kritipur
Status: Available
Price: Rs. 15,000

🔗 Get your tickets now:
https://events.khalti.com/events/ET25AMY4AUYM
```

Plus an automatic voice message will play saying the ticket alert!

---

## ⚙️ Configuration Options

Edit the `.env` file to customize:

```env
KHALTI_EVENT_ID=ET25AMY4AUYM          # Event to monitor
TELEGRAM_BOT_TOKEN=your_token         # Your Telegram bot token
TELEGRAM_CHAT_ID=your_chat_id         # Your Telegram chat ID
CHECK_INTERVAL_SECONDS=60             # How often to check (in seconds)
TIMEOUT_SECONDS=10                    # API timeout (in seconds)
```

**To monitor a different event:**
1. Go to https://events.khalti.com
2. Find the event URL (e.g., `...ET25AMY4AUYM...`)
3. Copy the event ID and update `KHALTI_EVENT_ID` in `.env`

---

## 📋 File Guide

| File | Purpose |
|------|---------|
| `.env` | **Your configuration** (credentials and settings) |
| `.env.example` | Template for `.env` |
| `main.py` | The main notifier script |
| `scraper.py` | Fetches ticket data from Khalti API |
| `telegram_notifier.py` | Sends formatted text messages |
| `voice_notifier.py` | Sends voice alerts |
| `config.py` | Loads settings from `.env` |
| `ticket_notifier.log` | Detailed activity log |

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install python-dotenv requests gtts urllib3
```

### ".env file not found" or "Missing credentials"

**Solution:** Create `.env` file with your credentials:
```bash
Copy-Item .env.example .env
```

Then edit `.env` and add your Telegram bot token and chat ID.

### "No tickets found on page" / "Available: 0"

This is normal if all tickets are sold out. Check manually on Khalti to verify.

### Not receiving Telegram messages

**Check:**
1. Verify `.env` has correct bot token and chat ID
2. Make sure you've messaged the bot first (click Start)
3. Check the log: `Get-Content ticket_notifier.log -Tail 50`

### Connection timeout errors

The Khalti API isn't responding. This is usually temporary. The script will automatically retry every `CHECK_INTERVAL_SECONDS`.

---

## 💡 Tips

1. **Run in background**: Use PowerShell to run in a new window:
   ```powershell
   Start-Process python -ArgumentList "main.py"
   ```

2. **Run at startup**: Add to Windows Task Scheduler to run automatically

3. **Check logs**: See what the script is doing:
   ```bash
   Get-Content ticket_notifier.log -Tail 20 -Wait
   ```

4. **Test voice alerts**: Run:
   ```bash
   python test_voice_alerts.py
   ```

5. **Test entire system**: Run:
   ```bash
   python test_integration.py
   ```

---

## ❓ Still Need Help?

1. **Check the log file:** `ticket_notifier.log` shows everything
2. **Test your setup:** `python test_scraper.py`
3. **See documentation:** `README.md` or `VOICE_ALERTS.md`

---

## 🎉 You're All Set!

Your NPL ticket notifier is now running. You'll receive a voice alert and Telegram notification the moment tickets become available!

Press `Ctrl+C` to stop at any time.
