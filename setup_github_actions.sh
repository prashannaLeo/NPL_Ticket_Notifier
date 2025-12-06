#!/bin/bash
# GitHub Actions Setup Script
# This script helps set up the GitHub Actions environment

echo "==============================================="
echo "NPL Ticket Notifier - GitHub Actions Setup"
echo "==============================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi

echo "✅ Git found"

# Check if .github/workflows exists
if [ -d ".github/workflows" ]; then
    echo "✅ GitHub Actions workflows directory exists"
    echo ""
    echo "Workflows found:"
    ls -la .github/workflows/
else
    echo "❌ .github/workflows directory not found"
    exit 1
fi

echo ""
echo "==============================================="
echo "Next Steps for GitHub Actions:"
echo "==============================================="
echo ""
echo "1. Push this code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Configure GitHub Actions'"
echo "   git push origin main"
echo ""
echo "2. Go to GitHub → Settings → Secrets and variables → Actions"
echo ""
echo "3. Add these secrets:"
echo "   • TELEGRAM_BOT_TOKEN"
echo "   • TELEGRAM_CHAT_ID"
echo "   • KHALTI_EVENT_URL"
echo ""
echo "4. Monitor → Actions tab to see workflow runs"
echo ""
echo "==============================================="
echo "Configuration:"
echo "==============================================="
cat .env.example 2>/dev/null || echo "Create .env.example file"
echo ""
echo "✅ Setup complete!"
