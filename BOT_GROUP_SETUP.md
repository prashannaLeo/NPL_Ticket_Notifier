# 🤖 Bot Commands - Group Chat Setup

## ✅ What Was Fixed

The bot now uses **long polling** (not webhooks) so it works perfectly in **group chats** without needing a public URL or server.

## 🚀 Quick Setup (Group Chat)

### Step 1: Make Your Bot an Admin in the Group

1. Open Telegram
2. Go to your group
3. Tap group name → Members/Settings
4. Find your bot (should be in members list)
5. **Make it an Admin** (give it permissions)
   - Allow messages
   - Allow commands
   - Allow to see messages

### Step 2: Start the Bot

**Option A: From terminal** (simplest)
```bash
python run_bot.py
```

**Option B: Using module syntax**
```bash
python -m npl_notifier.bot.telegram_polling_bot
```

Expected output:
```
============================================================
NPL TICKET NOTIFIER BOT (POLLING MODE)
============================================================
Bot token: 830860509...
Event ID: ET25AMY4AUYM
Status: Running (waiting for commands)

Supported commands:
  /tickets - Show available tickets
  /start   - Welcome message
  /help    - Help information
  /status  - Bot status

Press Ctrl+C to stop
============================================================
```

### Step 3: Use Commands in Group Chat

Send these commands in your group chat:

```
/tickets  - Show available NPL tickets
/start    - Welcome message with command list
/help     - Detailed help and features
/status   - Check bot status
```

## 🎯 How It Works

```
Your Group Chat
      ↓
   /tickets (you send command)
      ↓
   Telegram API
      ↓
   run_bot.py (polling for updates)
      ↓
   Bot fetches tickets from Khalti API
      ↓
   Sends formatted message back to group
```

## 🔧 Configuration

The bot reads from `.env` file:

```env
KHALTI_EVENT_ID=ET25AMY4AUYM
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=-1001234567890  # (not needed for group polling)
CHECK_INTERVAL_SECONDS=60
```

## ✨ Features in Group Chat

### /tickets
Shows all currently available NPL tickets with:
- Event title
- Date and time
- Venue/Location
- Price range
- Direct booking link

### /start
Shows welcome message and all available commands

### /help
Detailed help with pro tips for getting tickets faster

### /status
Shows bot status and configuration

## 🛠️ Troubleshooting

### "Bot is in the group but not responding"
✅ **Solution:**
1. Make sure bot is **Admin** in the group
2. Check bot permissions (allow messages)
3. Make sure bot token is correct in `.env`
4. Run `run_bot.py` in terminal - it should say "Running"

### "Command not recognized"
✅ **Solution:**
1. Make sure to send exact command: `/tickets`
2. Not case-sensitive
3. Bot must be Admin in group
4. Check bot is running in terminal

### "Error: No available tickets"
✅ This is **not an error** - it means tickets are currently sold out
- The bot will show: "❌ No available tickets at the moment"
- This is expected behavior
- Check back later using `/tickets`

### "Bot token error"
✅ **Solution:**
1. Check `.env` file has correct token
2. Get fresh token from @BotFather
3. Make sure no spaces in token
4. Restart `run_bot.py`

## 📊 Running Multiple Things

If you want both:
- **Bot commands** (group chat interaction)
- **Auto-notifications** (automatic alerts when tickets appear)

Run both simultaneously:

```powershell
# Terminal 1: Start the bot
python run_bot.py

# Terminal 2 (new terminal): Start auto-monitoring
python main.py
```

## 📝 Log Files

Bot creates logs:
- `telegram_bot.log` - Bot command logs
- `ticket_notifier.log` - Auto-notification logs
- `check_log.txt` - Check script logs

Check these to debug issues.

## ✅ Verification Checklist

- [ ] Bot created via @BotFather
- [ ] Bot token in `.env` file
- [ ] Bot added to your group
- [ ] Bot made an Admin in group
- [ ] Run `python run_bot.py` (terminal shows "Running")
- [ ] Send `/tickets` in group chat
- [ ] Bot responds with ticket list

## 🎉 You're All Set!

Now you can:
1. Use `/tickets` anytime to check availability
2. Run `python main.py` for automatic alerts
3. Get voice notifications when tickets appear
4. Share the group with friends who want tickets
