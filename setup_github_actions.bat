@echo off
REM GitHub Actions Setup Script for Windows

echo ===============================================
echo NPL Ticket Notifier - GitHub Actions Setup
echo ===============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Please install Git first.
    exit /b 1
)

echo OK: Git found
echo.

REM Check if .github/workflows exists
if exist ".github\workflows" (
    echo OK: GitHub Actions workflows directory exists
    echo.
    echo Workflows found:
    dir .github\workflows
) else (
    echo ERROR: .github\workflows directory not found
    exit /b 1
)

echo.
echo ===============================================
echo Next Steps for GitHub Actions:
echo ===============================================
echo.
echo 1. Push this code to GitHub:
echo    git add .
echo    git commit -m "Configure GitHub Actions"
echo    git push origin main
echo.
echo 2. Go to GitHub ^> Settings ^> Secrets and variables ^> Actions
echo.
echo 3. Add these secrets:
echo    - TELEGRAM_BOT_TOKEN
echo    - TELEGRAM_CHAT_ID
echo    - KHALTI_EVENT_URL
echo.
echo 4. Monitor workflow runs in Actions tab
echo.
echo ===============================================
echo Configuration Template:
echo ===============================================
if exist ".env.example" (
    type .env.example
) else (
    echo Create .env.example file
)
echo.
echo OK: Setup complete!
