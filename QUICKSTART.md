#!/usr/bin/env python3
"""
Quick Start Guide - How to Run NPL Ticket Notifier
"""

print("""
╔════════════════════════════════════════════════════════════╗
║     NPL TICKET NOTIFIER - QUICK START                      ║
╚════════════════════════════════════════════════════════════╝

📖 HOW TO RUN THE NOTIFIER:

1. ACTIVATE VIRTUAL ENVIRONMENT (if not already active):

   Windows PowerShell:
   $ .\\venv\\Scripts\\Activate.ps1
   
   Windows CMD:
   > venv\\Scripts\\activate
   
   Linux/Mac:
   $ source venv/bin/activate

   Expected: You should see (venv) at the start of your prompt


2. RUN THE NOTIFIER:

   ✓ CORRECT WAY (recommended):
   (venv) $ & "venv\\bin\\python.exe" main.py
   
   ✓ ALSO WORKS (if venv is activated):
   (venv) $ python main.py
   
   ✗ DON'T USE:
   (venv) $ py main.py          # May use wrong Python
   (venv) $ python3 main.py     # May use system Python


3. YOU SHOULD SEE:

   2025-12-06 21:13:58,429 - __main__ - INFO - Starting NPL Ticket Notifier...
   2025-12-06 21:13:58,429 - __main__ - INFO - Monitoring event: ET25AMY4AUYM
   2025-12-06 21:13:58,429 - __main__ - INFO - Check interval: 30 seconds
   ✓ Ready! Checking every 30 seconds


4. WHEN TICKETS ARE FOUND:

   ✓ Voice alert sent to Telegram
   ✓ Text message with details
   ✓ Logs show all activity


5. TO STOP THE NOTIFIER:

   Press Ctrl+C in the terminal


═════════════════════════════════════════════════════════════

📋 COMMON COMMANDS:

Local Monitoring:
  & "venv\\bin\\python.exe" main.py          # Run continuously

Testing:
  & "venv\\bin\\python.exe" test_scraper.py  # Test API
  & "venv\\bin\\python.exe" test_integration.py  # Full test
  & "venv\\bin\\python.exe" test_voice_alerts.py # Voice test

Configuration:
  Edit .env file with your Telegram credentials

═════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING:

Issue: "ModuleNotFoundError: No module named 'dotenv'"
→ Install requirements: & "venv\\bin\\python.exe" -m pip install -r requirements.txt

Issue: "Python interpreter not found"
→ Use full path: & "venv\\bin\\python.exe" main.py

Issue: No notifications sent
→ Check Telegram bot token and chat ID in .env file
→ Check internet connection

═════════════════════════════════════════════════════════════

✅ YOU'RE ALL SET!

Run this to start monitoring:
  & "venv\\bin\\python.exe" main.py

For GitHub Actions deployment, see: DEPLOYMENT.md
""")
