# Files to Remove (for cleanup)

These are test and debug files that are no longer needed for production:

## Debug/Investigation Files (safe to remove)
- `analyze_html.py` - HTML analysis (not used with API)
- `investigate.py` - Investigation script (debugging)
- `test_api.py` - API testing (redundant with main tests)
- `setup_playwright.py` - Old Playwright setup (not used)
- `validate_config.py` - Old validation (not used)

## Test Files (optional, can keep for local testing)
- `test_scraper.py` - Can keep for local testing
- `test_voice_alerts.py` - Can keep for local testing
- `test_integration.py` - Can keep for local testing

## Documentation (keep for reference)
All markdown files should be kept:
- `README.md`
- `VOICE_SETUP.md`
- `VOICE_ALERTS.md`
- `FEATURES.md`
- `GITHUB_ACTIONS_SETUP.md` (new)
- etc.

## Log Files (remove before commit)
- `ticket_notifier.log` - Will be regenerated
- `check_log.txt` - Will be regenerated

## Directories (remove before commit)
- `__pycache__/` - Ignored by .gitignore
- `venv/` - Not committed, covered by .gitignore

## Production Files (keep)
- `main.py` - Main local monitoring script
- `run_check.py` - GitHub Actions runner (new)
- `scraper.py` - API scraper
- `telegram_notifier.py` - Text notifications
- `voice_notifier.py` - Voice alerts
- `config.py` - Configuration loader (updated)
- `requirements.txt` - Dependencies (cleaned)
- `.github/` - GitHub Actions workflows (new)
- `.gitignore` - Git ignore patterns (new)
- `.env.example` - Configuration template (new)
