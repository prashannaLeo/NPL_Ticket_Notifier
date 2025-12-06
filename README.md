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

4. **(Recommended) Install Playwright for JavaScript rendering**:
   ```bash
   pip install playwright
   python setup_playwright.py
   ```
   This enables the scraper to work with the Khalti site's client-side rendered content.

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
├── main.py                 # Main script with monitoring loop
├── scraper.py             # Web scraper for Khalti events
├── telegram_notifier.py   # Telegram notification handler
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── setup_playwright.py    # Playwright setup script
├── ticket_notifier.log    # Log file (generated)
├── SETUP.md              # Detailed setup guide
└── README.md             # This file
```

## How It Works

1. **Scraper Module**: Uses BeautifulSoup to parse HTML, with optional Playwright for JavaScript rendering
2. **Parser**: Extracts ticket information (title, dates, venue, status, price)
3. **Notifier**: Sends formatted messages via Telegram Bot API
4. **Main Loop**: Continuously monitors with configurable intervals
5. **Deduplication**: Tracks already-notified tickets to avoid spam

## Note on Khalti Website

The Khalti events website uses **client-side rendering** (React/Next.js framework). For optimal results:

- **With Playwright** (recommended): The scraper can render JavaScript and extract ticket data reliably
- **Without Playwright**: The scraper attempts static HTML parsing but may not find tickets

**Recommendation**: Install Playwright for best results:
```bash
pip install playwright
python setup_playwright.py
```

## Log File

The script creates a `ticket_notifier.log` file with detailed information about:
- When checks are performed
- Tickets found
- Notifications sent
- Any errors encountered

View live logs:
```bash
Get-Content -Path ticket_notifier.log -Wait
```

## Troubleshooting

### No notifications received
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `config.py`
- Check `ticket_notifier.log` for error messages
- Ensure the bot can send messages (check Telegram privacy settings)

### "No tickets found on page"
- This is normal if:
  - Playwright isn't installed (install it with: `pip install playwright && python setup_playwright.py`)
  - All tickets are currently sold out
  - The Khalti website structure has changed

### Connection issues
- Check your internet connection
- Verify the Khalti URL is accessible
- Adjust `TIMEOUT_SECONDS` in config if the site is slow

### Playwright installation fails
- Ensure you have a compatible browser available
- Try: `python -m playwright install chromium`
- Check [Playwright documentation](https://playwright.dev/python/) for your OS

## License

MIT License

## Support

For issues or questions, check the log file first for detailed error messages.
