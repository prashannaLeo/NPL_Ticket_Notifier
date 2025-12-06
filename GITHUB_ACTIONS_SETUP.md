# NPL Ticket Notifier - GitHub Actions Deployment

Automated ticket monitoring with voice and text notifications using GitHub Actions.

## 📋 Overview

This project monitors Khalti events API and sends:
- 🔊 **Voice alerts** with ticket details (using text-to-speech)
- 📱 **Text messages** with full ticket information
- 🔗 Direct link to purchase tickets

Runs automatically every 5 minutes on GitHub Actions. **No server needed!**

## 🚀 Quick Setup (GitHub Actions)

### Step 1: Fork/Clone the Repository
```bash
git clone https://github.com/yourusername/NPL_ticket_notifier.git
cd NPL_ticket_notifier
```

### Step 2: Set Up Secrets
Go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Value |
|------------|-------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `KHALTI_EVENT_URL` | Event URL to monitor |

**How to get these:**
1. **Bot Token & Chat ID**: Message [@BotFather](https://t.me/botfather) on Telegram
2. **Event URL**: Copy from Khalti website (default: `https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true`)

### Step 3: Push to Trigger
```bash
git add .
git commit -m "Configure GitHub Actions"
git push origin main
```

That's it! ✅ The notifier will now run every 5 minutes.

## 📊 Monitoring

### View Workflow Runs
1. Go to your repository on GitHub
2. Click **Actions** tab
3. View all runs with status

### Check Logs
Click any run to see:
- ✓ Tickets found
- ✓ Notifications sent
- ✗ Errors or issues

## 🔧 Configuration

### Environment Variables

Edit `.env.example` → `.env` (for local testing only):

```env
KHALTI_EVENT_URL=https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_SECONDS=60
```

For GitHub Actions, use **Secrets** instead.

## 📁 Project Structure

```
.
├── .github/workflows/          # GitHub Actions workflows
│   ├── deploy.yml              # Main deployment workflow
│   └── monitor.yml             # Continuous monitoring (every 5 mins)
├── scraper.py                  # Khalti API scraper
├── telegram_notifier.py        # Text message notifications
├── voice_notifier.py           # Voice alert system
├── config.py                   # Configuration loader
├── run_check.py                # GitHub Actions runner
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
└── README.md                   # This file
```

## 🧪 Local Testing

### Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Local `.env`
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Run Ticket Check
```bash
python run_check.py
```

### Run Monitoring (Continuous)
```bash
python main.py
```

## 📚 Documentation

- **VOICE_SETUP.md** - Quick voice alerts guide
- **VOICE_ALERTS.md** - Complete voice feature documentation
- **FEATURES.md** - Feature summary
- **START_HERE.md** - Initial setup guide

## 🔐 Security

✅ **No credentials in code:**
- Secrets stored in GitHub only
- Environment variables used at runtime
- `.env` file ignored in git
- `.gitignore` prevents accidental commits

✅ **Best practices:**
- Never commit `.env` or credentials
- Use different secrets for different projects
- Rotate tokens periodically

## 🐛 Troubleshooting

### Workflow doesn't run
1. Check **Actions** tab - is it enabled?
2. Verify secrets are set in **Settings → Secrets**
3. Check push is to `main` or `master` branch

### No notifications sent
1. Verify Telegram bot token is valid
2. Check chat ID is correct
3. View workflow logs for error messages
4. Ensure internet is available

### Voice alerts not working
1. Check gtts library in logs
2. Verify internet connection
3. Voice works best with English event titles

## 📈 Performance

- **Check frequency**: Every 5 minutes
- **Execution time**: ~10-30 seconds per check
- **Cost**: Free (GitHub Actions provides 2000 minutes/month)
- **Reliability**: GitHub's infrastructure

## 🔄 Workflows

### Deploy Workflow (`deploy.yml`)
- Triggers on push to main/master
- Runs manual ticket checks
- Good for testing changes

### Monitor Workflow (`monitor.yml`)
- Runs every 5 minutes (scheduled)
- Sends notifications automatically
- Main production workflow

## 💡 Tips

1. **Adjust check frequency**: Edit cron in `monitor.yml`
2. **Change event**: Update `KHALTI_EVENT_URL` secret
3. **Disable notifications**: Comment out notifier calls in `run_check.py`
4. **View artifacts**: Check logs uploaded after each run

## 🤝 Contributing

Improvements welcome! Please:
1. Test locally first
2. Update documentation
3. Create pull request

## 📝 License

MIT License - feel free to use for any purpose

## ⚡ Quick Commands

```bash
# Local setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test configuration
python -c "from config import validate_config; validate_config(); print('✓ Config valid')"

# Run check once
python run_check.py

# Monitor continuously
python main.py

# Test voice alerts
python test_voice_alerts.py
```

## 🆘 Support

Having issues?
1. Check the **Actions** logs on GitHub
2. Review this README
3. Check error messages in `check_log.txt`
4. Verify all secrets are set correctly

---

**Happy monitoring!** 🎉 Your tickets will be found automatically with GitHub Actions!
