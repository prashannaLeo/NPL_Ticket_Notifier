# NPL Ticket Notifier - Setup Guide

## Step-by-Step Setup Instructions

### 1. Get Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Start a conversation and use `/newbot` command
3. Follow the prompts to create a new bot
4. Copy the bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
5. Save this token - you'll need it in config.py

### 2. Get Your Telegram Chat ID

1. Create a new Telegram group or use an existing one
2. Add your bot to the group
3. Search for **@userinfobot** on Telegram
4. Start it and it will show your Chat ID (a number like: `123456789`)
5. Save this ID - you'll need it in config.py

### 3. Configure the Application

Edit `config.py` and replace:
- `YOUR_BOT_TOKEN_HERE` with your actual bot token
- `YOUR_CHAT_ID_HERE` with your actual chat ID

Example:
```python
TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
TELEGRAM_CHAT_ID = "123456789"
```

### 4. Install Dependencies

In PowerShell:
```powershell
cd c:\dev\python\NPL_ticket_notifier
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the Notifier

```powershell
python main.py
```

You should see:
```
INFO - Starting NPL Ticket Notifier...
INFO - Monitoring: https://events.khalti.com/events/ET25AMY4AUYM?sub_event=true
INFO - Check interval: 60 seconds
```

### 6. Test the Setup

1. Wait for the first check to complete
2. You should receive a Telegram message when tickets are available
3. The log file `ticket_notifier.log` will track all activity

## Customization Options

In `config.py`:
- **CHECK_INTERVAL_SECONDS**: Change how often to check (60 = every minute)
- **TIMEOUT_SECONDS**: Increase if you get timeout errors

## Running in Background (Windows)

To run the notifier continuously:

1. **Using Windows Task Scheduler**:
   - Create a new task
   - Set trigger to "On startup" or "Daily"
   - Set action to: `python c:\dev\python\NPL_ticket_notifier\main.py`
   - Start in: `c:\dev\python\NPL_ticket_notifier`

2. **Using a batch file**:
   - Create `run_notifier.bat`:
   ```batch
   @echo off
   cd c:\dev\python\NPL_ticket_notifier
   call .\venv\Scripts\activate
   python main.py
   pause
   ```

## Monitoring the Logs

```powershell
# View real-time log updates
Get-Content -Path ticket_notifier.log -Wait -Tail 10
```

## Stopping the Notifier

Press `Ctrl+C` in the PowerShell window running the script.
