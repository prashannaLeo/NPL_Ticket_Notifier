# GitHub Actions Deployment - Complete Setup

## ✅ What's Ready for GitHub Actions

Your project is **fully configured** for GitHub Actions deployment. Both auto-notifications and bot commands will work on GitHub.

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
git init
git add .
git commit -m "NPL Ticket Notifier - GitHub Actions Ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/NPL_Ticket_Notifier.git
git push -u origin main
```

### Step 2: Configure GitHub Secrets

Go to: **GitHub Repository → Settings → Secrets and variables → Actions**

Add these 3 secrets:

| Secret Name | Value | Where to Get |
|------------|-------|--------------|
| `TELEGRAM_BOT_TOKEN` | Your bot token | @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your chat/group ID | @userinfobot on Telegram |
| `KHALTI_EVENT_ID` | Event ID to monitor | Default: `ET25AMY4AUYM` |

**Example:**
```
TELEGRAM_BOT_TOKEN = 8307855097:AAGCivJZviOUFoD8973yU6wHyuz13uF_ZrBdc
TELEGRAM_CHAT_ID = -1093378555002
KHALTI_EVENT_ID = ET25AMP4AUYM
```

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"

That's it! ✅ GitHub Actions will now run automatically.

## 📊 What Will Happen

### Workflow 1: `monitor.yml` (Automatic Checks)
- **Runs:** Every 1 minute
- **What it does:**
  - Checks Khalti API for available tickets
  - Sends Telegram notifications for new tickets
  - Saves ticket history to `notified_tickets.json`
  - Pushes updates back to GitHub
- **No manual action needed** - fully automated

### Workflow 2: `deploy.yml` (On Push)
- **Runs:** Every time you push code
- **What it does:**
  - Runs the same ticket check
  - Updates history file
  - Can be manually triggered anytime

## 🔔 How Notifications Work on GitHub

When a new ticket is found:
1. **Voice Alert** 🔊 - Telegram voice message with details
2. **Text Message** 📱 - Formatted message with link to buy
3. **History Update** 📝 - Saved to prevent duplicates
4. **Push to GitHub** 🔄 - Commits history file

## 📈 Monitoring

### Check Workflow Status
1. Go to **Actions** tab
2. See all workflow runs with status (✅ passed, ❌ failed)
3. Click any run to see detailed logs

### View Logs
Each workflow run includes:
- Ticket check results
- Tickets found/skipped
- Notifications sent
- Errors (if any)

### Download Artifacts
Each run creates log files you can download:
- `check-logs` - Ticket checking logs
- `deploy-logs` - Deployment logs

## 🛠️ Troubleshooting on GitHub

### Workflow Not Running?
1. Check **Actions** tab - should see workflows listed
2. Check **Settings → Actions → General** - ensure workflows are enabled
3. Check **Secrets** - all 3 secrets must be configured

### Notifications Not Sent?
1. Check logs in **Actions** tab
2. Verify bot token is correct
3. Verify chat ID is correct
4. Make sure bot is admin in group (for groups)

### "Secret not found" error?
1. Go to **Settings → Secrets and variables → Actions**
2. Add missing secrets
3. Re-run workflow

## 📝 Log Files Created

When GitHub Actions runs, these files are created:

| File | Created By | Content |
|------|-----------|---------|
| `check_log.txt` | `run_check.py` | Detailed check logs |
| `deploy_log.txt` | `deploy.yml` | Deployment summary |
| `ticket_notifier.log` | `main.py` | Main app logs |
| `notified_tickets.json` | Both scripts | History of notified tickets |

These are **committed back to GitHub** so history persists.

## 🔐 Security Notes

✅ **Your credentials are safe:**
- Secrets never logged to console
- Secrets not in code or files
- Only used during workflow execution
- GitHub encrypts all secrets

## ⏰ Scheduling Frequency

### Current Settings (from `monitor.yml`):
- **Every 1 minute** - Fast detection
- Adjustable via cron expression: `*/1 * * * *`

To change frequency, edit `.github/workflows/monitor.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # or
  - cron: '0 * * * *'    # Every hour
  # or
  - cron: '*/30 * * * *' # Every 30 minutes
```

## ✅ Verification Checklist

- [ ] Code pushed to GitHub
- [ ] Secrets configured (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, KHALTI_EVENT_ID)
- [ ] Actions tab shows workflows
- [ ] First workflow run completes
- [ ] Check logs show "Found tickets" or "No new tickets"
- [ ] Bot works in group chat (send `/tickets`)
- [ ] Received Telegram notification

## 🎉 You're All Set!

Your project will now:
1. ✅ Check for tickets **every 1 minute** on GitHub
2. ✅ Send automatic **voice + text notifications** when tickets appear
3. ✅ **Track history** to prevent duplicate alerts
4. ✅ Work in **group chats** without needing a server
5. ✅ **Run forever** on GitHub's free tier (no cost!)

## 📞 Support

If something doesn't work:
1. Check **Actions** tab for error logs
2. Verify secrets are correct
3. Ensure bot is admin in group (for groups)
4. Check bot token has correct permissions from @BotFather
