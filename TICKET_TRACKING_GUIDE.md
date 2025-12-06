# Ticket Tracking & Duplicate Prevention Guide

## Overview

The NPL Ticket Notifier now tracks which tickets you've already been notified about. **You will only receive alerts for NEW tickets** - same tickets won't trigger repeated notifications.

## How It Works

### Ticket Identification
Each ticket is uniquely identified by combining:
- **Title** (e.g., "NPL Season Ticket 2025")
- **Dates** (e.g., "Mon, 17 Nov - Sat, 13 Dec")
- **Price** (e.g., "Rs. 15,000")

### History File
The notifier saves the list of notified tickets in `notified_tickets.json`:

```json
[
  "NPL Season Ticket 2025_Mon, 17 Nov - Sat, 13 Dec_Rs. 15,000",
  "NPL 2025 6th Dec event_Fri, 6 Dec_Rs. 500-1000"
]
```

This file is:
- ✅ **Automatically created** when a new ticket is notified
- ✅ **Automatically updated** as new tickets are found
- ✅ **Persisted** across program restarts
- ✅ **Ignored by Git** (won't be committed to GitHub)

## Behavior

### First Run
When you first start the notifier and tickets are available:
- ✅ You receive notifications for ALL available tickets
- ✅ Each ticket is added to `notified_tickets.json`

### Subsequent Runs
When you run the notifier again and the same tickets are still available:
- ✅ **NO notifications sent** (same tickets)
- ✅ Log message: `"Already notified about: [Ticket Name]"`
- ✅ No new entries added to history

### When NEW Tickets Appear
If a previously sold-out ticket becomes available again:
- ✅ You receive an alert for the NEW ticket
- ✅ Voice notification + Text message sent
- ✅ Ticket is added to history to prevent future duplicates

## Examples

### Scenario 1: Continuous Monitoring
```
Hour 1: 3 available tickets → Notifications sent ✅
Hour 2: Same 3 tickets available → No notifications (already know about them)
Hour 3: 4 tickets available (1 new) → Notification for new ticket only ✅
```

### Scenario 2: GitHub Actions (Every 5 minutes)
```
5:00 PM: Ticket discovered → Alert sent ✅
5:05 PM: Same ticket available → No alert
5:10 PM: Same ticket available → No alert
5:15 PM: New ticket appears → Alert sent ✅
```

## Managing Ticket History

### View History
```bash
Get-Content notified_tickets.json
```

### Clear History (Reset Tracking)
If you want to get notifications for already-notified tickets again:

```bash
Remove-Item notified_tickets.json
```

**Next run will send alerts for all available tickets again.**

### Manual History Edit
```bash
# Remove specific ticket from history
$history = Get-Content notified_tickets.json | ConvertFrom-Json
$history = $history | Where-Object { $_ -ne "TICKET_HASH_TO_REMOVE" }
$history | ConvertTo-Json | Set-Content notified_tickets.json
```

## Log Messages

### New Ticket Found
```
2025-12-06 15:30:45,123 - __main__ - INFO - NEW TICKET FOUND: NPL Season Ticket 2025
2025-12-06 15:30:45,234 - __main__ - INFO - Sending notification for: NPL Season Ticket 2025
```

### Same Ticket (No Alert)
```
2025-12-06 15:31:45,456 - __main__ - DEBUG - Already notified about: NPL Season Ticket 2025
2025-12-06 15:31:45,567 - __main__ - INFO - Available tickets are same as before - no new notifications
```

## GitHub Actions Integration

Both workflows use ticket tracking:

- **`monitor.yml`** (every 1 minute): Checks for new tickets
- **`deploy.yml`** (push trigger): One-time check with history tracking

The `notified_tickets.json` file is downloaded as an artifact after each run, allowing history to persist across workflows.

## Troubleshooting

### History File Not Saving
Check the logs for permission errors:
```bash
Get-Content ticket_notifier.log | Select-String "Could not save"
```

**Solution**: Ensure the script has write permissions in the project directory.

### Getting Notifications Again for Old Tickets
Delete the history file:
```bash
Remove-Item notified_tickets.json -Force
```

### History File Growing Too Large
Remove duplicates:
```bash
$history = Get-Content notified_tickets.json | ConvertFrom-Json
$history = $history | Sort-Object -Unique
$history | ConvertTo-Json | Set-Content notified_tickets.json
```

## Files Modified

- ✅ `main.py` - Added `_load_ticket_history()`, `_save_ticket_history()`
- ✅ `run_check.py` - Added ticket tracking for GitHub Actions
- ✅ `.gitignore` - Added `notified_tickets.json` to prevent accidental commits
- ✅ `.github/workflows/monitor.yml` - Uses persistent history tracking
- ✅ `.github/workflows/deploy.yml` - Uses persistent history tracking

## Summary

You now get smarter alerts:
- ✅ Only notified about NEW tickets
- ✅ No more duplicate alerts for same tickets
- ✅ History persists across restarts
- ✅ Works locally and in GitHub Actions
- ✅ Easy to reset if needed

Happy monitoring! 🎫
