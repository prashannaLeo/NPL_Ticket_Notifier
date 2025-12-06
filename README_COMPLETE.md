# NPL Ticket Notifier - Complete & Production Ready

Automated NPL ticket monitoring with voice and text notifications using GitHub Actions.

## 🎯 Features

✅ **Real-time Monitoring** - Checks Khalti API every 5 minutes via GitHub Actions
✅ **Voice Alerts** - Automatic voice notifications with ticket details (gTTS)
✅ **Text Messages** - Detailed Telegram notifications with pricing and venue
✅ **Zero Cost** - Runs on GitHub's free infrastructure
✅ **No Server Needed** - 100% serverless automation
✅ **API-based** - Direct Khalti API integration (reliable, no web scraping)
✅ **Secure** - Credentials stored in GitHub Secrets only

## 🚀 Quick Start (3 Steps)

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd NPL_ticket_notifier
```

### Step 2: Configure Locally (Optional Testing)
```bash
cp .env.example .env
# Edit .env with your credentials
python main.py  # Start monitoring locally
```

### Step 3: Deploy to GitHub
```bash
git add .
git commit -m "Deploy to GitHub Actions"
git push origin main
```

Then go to **GitHub Settings → Secrets and variables → Actions** and add:
- `TELEGRAM_BOT_TOKEN` 
- `TELEGRAM_CHAT_ID`
- `KHALTI_EVENT_ID` (default: ET25AMY4AUYM)

**Done!** 🎉 Monitoring starts automatically every 5 minutes.

## 📋 Project Structure

```
NPL_ticket_notifier/
├── .github/workflows/
│   ├── deploy.yml          # Push-triggered workflow
│   └── monitor.yml         # 5-minute scheduled workflow
├── main.py                 # Local monitoring script
├── scraper.py              # Khalti API scraper
├── telegram_notifier.py    # Text notifications
├── voice_notifier.py       # Voice alerts (gTTS)
├── config.py               # Configuration loader
├── run_check.py            # GitHub Actions runner
├── requirements.txt        # Python dependencies
├── .env.example            # Configuration template
├── .gitignore              # Git ignore patterns
└── Documentation/
    ├── DEPLOYMENT.md                 # Full deployment guide
    ├── GITHUB_ACTIONS_SETUP.md       # GitHub setup guide
    ├── GITHUB_ACTIONS_SUMMARY.md     # Implementation details
    ├── VOICE_SETUP.md                # Voice feature guide
    ├── VOICE_ALERTS.md               # Complete voice docs
    └── FEATURES.md                   # Feature summary
```

## 🔧 Configuration

### Environment Variables

Create `.env` file (for local testing):
```bash
KHALTI_EVENT_ID=ET25AMY4AUYM
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_SECONDS=60
TIMEOUT_SECONDS=10
```

For GitHub Actions, add these as **Secrets** in repository settings.

## 📱 How It Works

```
Every 5 minutes (GitHub Actions)
    ↓
Check Khalti API: https://khalti.com/api/e5/events/{EVENT_ID}/children/
    ↓
Tickets available?
├─ YES → Send voice alert + text message to Telegram
└─ NO → Wait for next check
```

## 🧪 Testing Locally

### Test API Scraper
```bash
python test_scraper.py
```

### Test Voice Alerts
```bash
python test_voice_alerts.py
```

### Test Full Integration
```bash
python test_integration.py
```

### Monitor Continuously
```bash
python main.py
```

## 🤖 GitHub Actions Workflows

### Deploy Workflow (deploy.yml)
- Triggers: Push to main/master or manual trigger
- Action: Run ticket check once
- Use: Testing and on-demand checks

### Monitor Workflow (monitor.yml)
- Triggers: Every 5 minutes (scheduled)
- Action: Run ticket check
- Use: Main production monitoring

### Customize Schedule

Edit `.github/workflows/monitor.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # Other options:
  # '*/1 * * * *'   = Every 1 minute
  # '*/10 * * * *'  = Every 10 minutes
  # '0 * * * *'     = Every hour
```

## 🔐 Security

✅ **No credentials in code**
- All secrets in GitHub Secrets (encrypted)
- Environment variables loaded at runtime
- `.env` file ignored by `.gitignore`

✅ **Best practices**
- Never commit `.env` or credentials
- Use different bots for different projects
- Rotate tokens periodically

## 📊 Performance

- **Execution time**: 10-30 seconds per check
- **Check frequency**: Every 5 minutes (288 times/day)
- **Cost**: FREE (GitHub provides 2000 min/month)
- **Uptime**: 99.9% (GitHub infrastructure)

## 📞 Support

### Common Issues

**Workflow doesn't run:**
- Check Actions tab is enabled
- Verify secrets are set
- Check push is to main/master

**No notifications:**
- Verify Telegram bot token
- Check chat ID is correct
- View workflow logs for errors

**Voice not working:**
- Check internet connection
- Verify gtts library installed
- Check event title format

## 💾 Installation

### Local Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

### GitHub Actions
```bash
git init
git add .
git commit -m "Initial setup"
git push -u origin main
# Add secrets in GitHub Settings
```

## 📚 Documentation

- **START HERE**: DEPLOYMENT.md
- **GitHub Setup**: GITHUB_ACTIONS_SETUP.md
- **Implementation**: GITHUB_ACTIONS_SUMMARY.md
- **Voice Alerts**: VOICE_SETUP.md
- **Features**: FEATURES.md

## 🔄 Notifications

When tickets are found, you receive:

1. **Voice Message** (audio)
   ```
   "URGENT ALERT! NPL 2025 7th Dec is now Available. 
    Price is Rs. 500 to Rs. 1000. Check your Telegram for details."
   ```

2. **Text Message** (detailed)
   ```
   🎫 NPL TICKET ALERT!
   
   Event: NPL 2025 7th Dec
   Dates: Sun, 07 Dec
   Venue: TU Cricket Ground, Kritipur
   Status: Available
   Price: Rs. 500 - Rs. 1000
   
   🔗 Get your tickets: https://events.khalti.com/...
   ```

## 🎯 API Details

**Khalti API Endpoint:**
```
https://khalti.com/api/e5/events/{EVENT_ID}/children/
```

**Response Format:**
```json
{
  "idx": "ET25AMY4AUYM",
  "title": "Siddhartha Bank Nepal Premier League 2025",
  "children": [
    {
      "title": "Event Name",
      "status": "Available",
      "is_sold_out": false,
      "price": {"min_price": 50000, "max_price": 150000},
      "date": "Mon, 17 Nov - Sat, 13 Dec",
      "location": "TU Cricket Ground, Kritipur"
    }
  ]
}
```

## 🚀 Deployment Checklist

- [ ] Clone/fork repository
- [ ] Test locally with `.env` file
- [ ] Verify `python test_scraper.py` works
- [ ] Initialize git and commit
- [ ] Push to GitHub
- [ ] Add GitHub Secrets (3 required)
- [ ] Verify Actions tab shows workflows running
- [ ] Monitor Actions tab for ticket alerts

## 🎉 You're Done!

Your NPL Ticket Notifier is now:
- ✅ Monitoring 24/7 via GitHub Actions
- ✅ Sending voice alerts immediately
- ✅ Sending detailed text messages
- ✅ Running at zero cost
- ✅ Completely automated

**Happy ticket hunting!** 🎫

---

Need help? Check the documentation files or view workflow logs in GitHub Actions tab.
