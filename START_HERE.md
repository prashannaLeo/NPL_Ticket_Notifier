# QUICKSTART GUIDE - NPL Ticket Notifier

## 🎯 What This Does

Monitors the Khalti events website for NPL cricket tickets and automatically sends you a **Telegram notification** as soon as tickets become available.

## ✅ Current Status

✓ **The application is fully working and ready to use!**

The script can:
- Monitor the Khalti events page continuously
- Send formatted Telegram messages with ticket details
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

### Step 2: Update config.py

Open `config.py` and update these lines:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <- Replace with your token from BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # <- Replace with your Chat ID
```

**Verify it worked:**
```bash
python validate_config.py
```

### Step 3: Run the Notifier

```bash
python main.py
```

You should see:
```
Starting NPL Ticket Notifier...
Monitoring: https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
Check interval: 60 seconds
Checking for available tickets...
```

That's it! The notifier is now running and will send you a Telegram message when tickets are available.

**To stop it:** Press `Ctrl+C`

---

## 📱 What You'll Receive

When tickets are found, you'll get a Telegram message like:

```
🎫 NPL TICKET ALERT!

Event: NPL Season Ticket 2025
Dates: Mon, 17 Nov - Sat, 13 Dec
Venue: TU Cricket Ground, Kritipur
Status: Filling Fast
Price: Rs. 15,000

🔗 Get your tickets now:
https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
```

---

## ⚙️ Advanced Options

### Change Check Frequency

Edit `config.py`:
```python
CHECK_INTERVAL_SECONDS = 30  # Check every 30 seconds instead of 60
```

### Enable Full-Power Monitoring (RECOMMENDED)

The Khalti website uses advanced JavaScript to display tickets. For the best results, install Playwright:

```bash
pip install playwright
python setup_playwright.py
python main.py
```

This enables the scraper to properly render the page and find tickets more reliably.

---

## 📋 File Guide

| File | Purpose |
|------|---------|
| `config.py` | **Your configuration** (bot token, chat ID) |
| `main.py` | The main notifier script |
| `scraper.py` | Fetches and parses ticket data |
| `telegram_notifier.py` | Sends Telegram messages |
| `validate_config.py` | Checks if everything is set up correctly |
| `ticket_notifier.log` | Detailed activity log |

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"

**Solution:** Use the virtual environment:
```bash
.\venv\Scripts\activate
python main.py
```

Or:
```bash
.\venv\bin\python main.py
```

### "No tickets found on page"

This is normal if:
- All tickets are sold out (check Khalti site manually)
- Playwright isn't installed (see "Enable Full-Power Monitoring" above)
- The page structure changed (rare, will be updated)

### Not receiving Telegram messages

**Check:**
1. Open `config.py` - Verify your bot token and chat ID are correct (no quotes around numbers!)
2. Run: `python validate_config.py` - Look for ✓ marks
3. Check the log: `Get-Content ticket_notifier.log -Wait`
4. Make sure the Telegram bot is allowed to message you

### Connection timeout errors

This means the Khalti website isn't responding. Usually temporary. The script will automatically retry.

---

## 💡 Tips

1. **Run in background**: Use PowerShell to run in a new window:
   ```powershell
   Start-Process python -ArgumentList "main.py"
   ```

2. **Run at startup**: Add to Windows Task Scheduler to run automatically when you start your computer

3. **Multiple events**: Edit `KHALTI_EVENT_URL` in `config.py` to monitor different events

4. **Check logs**: The `ticket_notifier.log` file shows everything the script did:
   ```bash
   Get-Content ticket_notifier.log -Tail 20 -Wait
   ```

---

## ❓ Still Need Help?

1. Check the log file: `ticket_notifier.log`
2. Run the validator: `python validate_config.py`
3. Try installing Playwright: `pip install playwright && python setup_playwright.py`

---

## 🎉 You're All Set!

Your NPL ticket notifier is now running. You'll receive a Telegram notification the moment tickets become available!

Press `Ctrl+C` to stop at any time.
