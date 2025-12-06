# NPL Ticket Notifier

A Python-based notification system that monitors the Khalti events API for NPL (Nepal Premier League) ticket availability and sends real-time Telegram notifications (voice + text) when tickets become available.

## ✨ Features

- ⚡ **Fast Monitoring**: Checks every 30 seconds locally, every 1 minute on GitHub Actions
- 🔊 **Voice Alerts**: Automatic text-to-speech notifications via Telegram
- 📱 **Text Messages**: Formatted detailed ticket information
- 🎯 **Smart Detection**: Only alerts for NEW tickets (prevents duplicates)
- 🌐 **API-Based**: Direct Khalti API integration (no HTML scraping issues)
- 🤖 **GitHub Actions**: Runs 24/7 automatically - no server needed!
- 💾 **Ticket History**: Persistent history prevents repeated notifications
- 🛡️ **Secure**: No hardcoded credentials, uses environment variables
- 📊 **Logging**: Comprehensive logs for monitoring and troubleshooting
- 🎨 **Group Support**: Send alerts to personal chat or group

## 🚀 Quick Start

**30 seconds to set up:**

1. **Get Telegram credentials:**
   - Bot Token: [@BotFather](https://t.me/botfather) → `/newbot`
   - Chat ID: [@userinfobot](https://t.me/userinfobot) (or group ID from API)

2. **Configure `.env`:**
   ```env
   KHALTI_EVENT_ID=ET25AMY4AUYM
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
   CHECK_INTERVAL_SECONDS=30
   ```

3. **Run:**
   ```bash
   python main.py
   ```

**Or deploy to GitHub Actions** for 24/7 automatic monitoring!

## Prerequisites

- Python 3.11+
- Telegram Bot (get from [@BotFather](https://t.me/botfather))
- Active internet connection

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd c:\dev\python\NPL_ticket_notifier
   ```

2. **Activate virtual environment**:
   ```bash
   .\venv\Scripts\activate
   ```
   Or on PowerShell:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This installs: `requests`, `python-dotenv`, `gtts` (for voice alerts)

## Configuration

1. **Get your Telegram Bot Token**:
   - Chat with [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot and copy the token

2. **Get your Chat ID**:
   - Chat with [@userinfobot](https://t.me/userinfobot) on Telegram
   - It will return your numeric chat ID

3. **Edit `config.py`**:
   ```python
   TELEGRAM_BOT_TOKEN = "your_bot_token_here"
   TELEGRAM_CHAT_ID = "your_chat_id_here"
   ```

4. **Optional Settings in `config.py`**:
   - `CHECK_INTERVAL_SECONDS`: How often to check for tickets (default: 60)
   - `TIMEOUT_SECONDS`: Request timeout in seconds (default: 10)

## Usage

1. **Start the notifier**:
   ```bash
   python main.py
   ```
   Or with explicit venv:
   ```bash
   .\venv\bin\python main.py
   ```

2. The script will:
   - Start monitoring the Khalti events page
   - Check for available tickets every 60 seconds (configurable)
   - Send Telegram notifications when tickets are found
   - Log all activity to `ticket_notifier.log` and console

3. **Stop the notifier**:
   - Press `Ctrl+C` to stop

## Project Structure

```
NPL_ticket_notifier/
├── main.py                    # Main script with monitoring loop
├── scraper.py                 # Khalti API scraper
├── telegram_notifier.py       # Text message notifications
├── voice_notifier.py          # Voice alert generation (gTTS)
├── config.py                  # Configuration loader
├── run_check.py               # GitHub Actions runner
├── requirements.txt           # Python dependencies
├── notified_tickets.json      # Ticket history (auto-managed)
├── ticket_notifier.log        # Activity log (generated)
├── .github/workflows/         # GitHub Actions automation
├── SETUP.md                   # Detailed setup guide
└── README.md                  # This file
```

## How It Works

1. **API Scraper**: Fetches live ticket data from Khalti API (`/api/e5/events/{EVENT_ID}/children/`)
2. **Ticket Parser**: Extracts title, dates, venue, price, and availability status
3. **History Check**: Compares against `notified_tickets.json` to detect NEW tickets only
4. **Notifications**: Sends voice alert + text message via Telegram
5. **Persistent Storage**: Saves ticket hash to prevent duplicate notifications
6. **Continuous Monitoring**: Checks every 30 seconds (local) or 1 minute (GitHub Actions)

## API-Based Approach

Unlike HTML scraping, this uses the direct Khalti API:
- ✅ **Reliable**: Direct data source, not affected by page structure changes
- ✅ **Fast**: JSON response is cleaner than HTML parsing
- ✅ **Simple**: No browser automation needed
- ✅ **Efficient**: Lower resource usage

## Log File

The script creates `ticket_notifier.log` with:
- Ticket check timestamps
- Available tickets found
- Notification status
- Error messages for troubleshooting
- Notifications sent
- Any errors encountered

View live logs:
```bash
Get-Content -Path ticket_notifier.log -Wait
```

## Troubleshooting

### No notifications received
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- Check `ticket_notifier.log` for error messages
- Ensure the bot can send messages (add bot to chat first)
- For groups: Verify you're using the negative chat ID

### No tickets found
- Check Khalti website manually to verify tickets are available
- Ensure `KHALTI_EVENT_ID` is correct
- Check API response: `https://khalti.com/api/e5/events/{EVENT_ID}/children/`

### Connection timeout errors
- Check your internet connection
- Adjust `TIMEOUT_SECONDS` in `.env` if API is slow
- GitHub Actions runs from US servers (may have latency)

### Duplicate notifications still received
- Delete `notified_tickets.json` to reset history
- Check if `notified_tickets.json` is being saved (check logs)

## License

MIT License

## Support

For issues, check:
1. `ticket_notifier.log` for detailed error messages
2. GitHub Actions logs in your repository
3. Verify credentials in `.env` or GitHub Secrets

