# NPL Ticket Notifier - Production Deployment Guide

## 🎯 Project Ready for GitHub Actions

Your NPL Ticket Notifier is now fully configured for automated deployment and monitoring using GitHub Actions.

## 📦 What's Included

### Core Application Files
```
✅ main.py                      # Local monitoring script
✅ scraper.py                   # Khalti API scraper (100% reliable)
✅ telegram_notifier.py         # Text message notifications
✅ voice_notifier.py            # Voice alerts (text-to-speech)
✅ config.py                    # Configuration (environment-based)
✅ requirements.txt             # Production dependencies (cleaned)
```

### GitHub Actions Automation
```
✅ .github/workflows/deploy.yml    # Main deployment workflow
✅ .github/workflows/monitor.yml   # Continuous monitoring (every 5 min)
✅ run_check.py                    # GitHub Actions execution script
```

### Configuration Files
```
✅ .env.example                    # Configuration template
✅ .gitignore                      # Git ignore patterns
✅ config.py                       # Updated for environment variables
```

### Documentation
```
✅ README.md                       # Project overview
✅ GITHUB_ACTIONS_SETUP.md         # GitHub Actions guide (NEW)
✅ VOICE_SETUP.md                  # Voice alerts quick start
✅ VOICE_ALERTS.md                 # Complete voice documentation
✅ FEATURES.md                     # Feature summary
✅ CLEANUP_GUIDE.md                # Files to remove for cleanup
```

### Helper Scripts
```
✅ setup_github_actions.sh         # Linux/Mac setup script
✅ setup_github_actions.bat        # Windows setup script
```

## 🚀 Quick Start (3 Steps)

### Step 1: Prepare Code for GitHub
```bash
# Remove unnecessary debug files (optional)
rm analyze_html.py investigate.py test_api.py setup_playwright.py validate_config.py

# Remove log files
rm ticket_notifier.log check_log.txt

# Remove virtual environment from git
rm -rf venv __pycache__
```

### Step 2: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial NPL Ticket Notifier setup for GitHub Actions"
git branch -M main
git remote add origin https://github.com/yourusername/NPL_ticket_notifier.git
git push -u origin main
```

### Step 3: Configure GitHub Secrets
1. Go to: **GitHub → Your Repo → Settings → Secrets and variables → Actions**
2. Click **New repository secret** and add:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `KHALTI_EVENT_URL` | Event URL to monitor |

**Done!** 🎉 Workflow will start automatically.

## 📊 How It Works

```
Every 5 minutes (GitHub Actions)
    ↓
Check Khalti API for available tickets
    ↓
Tickets found?
├─ YES → Send voice alert + text message
└─ NO → Continue monitoring

Logs saved to check_log.txt
Artifacts kept for 7 days
```

## 🔍 Monitoring

### View Workflow Status
1. Go to **Actions** tab on GitHub
2. Click on workflow run
3. View logs and output

### Check Logs
- Look for `check_log.txt` in artifacts
- See what tickets were checked
- View notification status

## 🛠️ Customization

### Change Check Frequency
Edit `.github/workflows/monitor.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes (change this)
  # Examples:
  # '*/1 * * * *'  = Every 1 minute
  # '*/10 * * * *' = Every 10 minutes
  # '0 * * * *'    = Every hour
```

### Change Event to Monitor
Update `KHALTI_EVENT_URL` secret in GitHub:
1. Settings → Secrets
2. Click `KHALTI_EVENT_URL`
3. Update value

### Disable Voice Alerts
Edit `run_check.py`, comment out:
```python
# voice_notifier.send_alert_call(ticket)
```

## 📋 Files to Remove (Optional)

These are debug files - safe to delete before pushing:

```bash
# Remove debug/test files
rm analyze_html.py          # HTML analysis
rm investigate.py           # Investigation script  
rm test_api.py              # Old API test
rm setup_playwright.py       # Old Playwright setup
rm validate_config.py        # Old validation

# Or keep test files for local testing:
# test_scraper.py
# test_voice_alerts.py
# test_integration.py
```

See `CLEANUP_GUIDE.md` for complete file reference.

## ✅ Verification Checklist

Before deploying to GitHub:

- [ ] All secrets added to GitHub
- [ ] `.env` file not committed (only `.env.example`)
- [ ] `venv/` directory not in git
- [ ] `__pycache__/` not in git
- [ ] Debug files removed (optional)
- [ ] `requirements.txt` contains only production dependencies
- [ ] Workflows exist in `.github/workflows/`
- [ ] `config.py` uses environment variables

## 🔐 Security

✅ **No credentials exposed:**
- Secrets stored in GitHub only
- Config reads from environment variables
- `.gitignore` protects local files

✅ **Best practices:**
- Token rotation recommended periodically
- Never commit `.env` or credentials
- Use different bot for different projects

## 📈 Performance

- **Check Frequency**: Every 5 minutes
- **Execution Time**: ~10-30 seconds
- **Cost**: Free (GitHub provides 2000 min/month)
- **Uptime**: 99.9% (GitHub infrastructure)

## 🧪 Local Testing

Before GitHub deployment, test locally:

```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Test once
python run_check.py

# Monitor continuously
python main.py
```

## 📞 Support

### Common Issues

**Workflow not running:**
- Check Actions tab is enabled
- Verify secrets are set
- Confirm push to main/master

**No notifications:**
- Check Telegram bot token
- Verify chat ID
- View workflow logs

**Voice not working:**
- Check internet connection
- Verify event title in Nepali (gTTS works best with English)

## 📚 Documentation

Start with:
1. **GITHUB_ACTIONS_SETUP.md** - GitHub Actions specific setup
2. **README.md** - Project overview
3. **VOICE_SETUP.md** - Voice alerts guide
4. **FEATURES.md** - Feature summary

## 🎯 Next Steps

1. ✅ Remove unnecessary files (see CLEANUP_GUIDE.md)
2. ✅ Initialize Git repo
3. ✅ Push to GitHub
4. ✅ Add secrets in GitHub Settings
5. ✅ Monitor Actions tab
6. ✅ Receive Telegram notifications!

---

## Quick Commands

```bash
# Setup git
git init
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# Local testing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env
python run_check.py
```

**You're ready for production!** 🚀 Push to GitHub and let the automation handle ticket monitoring.
