#!/usr/bin/env python3
"""
Pre-deployment checklist for GitHub Actions
Run this to verify everything is ready
"""

import os
import sys

def check_file(filepath, category="File"):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {filepath}")
    return exists

def check_directory(dirpath, category="Directory"):
    """Check if directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"  {status} {dirpath}/")
    return exists

def main():
    print("="*60)
    print("NPL TICKET NOTIFIER - GITHUB ACTIONS CHECKLIST")
    print("="*60)
    print()
    
    all_good = True
    
    # Check core files
    print("📦 CORE APPLICATION FILES:")
    core_files = [
        'main.py',
        'scraper.py',
        'telegram_notifier.py',
        'voice_notifier.py',
        'config.py',
        'requirements.txt',
        'run_check.py'
    ]
    for f in core_files:
        if not check_file(f):
            all_good = False
    print()
    
    # Check GitHub Actions files
    print("🤖 GITHUB ACTIONS FILES:")
    if not check_directory('.github'):
        all_good = False
    if not check_directory('.github/workflows'):
        all_good = False
    if not check_file('.github/workflows/deploy.yml'):
        all_good = False
    if not check_file('.github/workflows/monitor.yml'):
        all_good = False
    print()
    
    # Check configuration files
    print("⚙️ CONFIGURATION FILES:")
    if not check_file('.gitignore'):
        all_good = False
    if not check_file('.env.example'):
        all_good = False
    print()
    
    # Check documentation
    print("📚 DOCUMENTATION FILES:")
    docs = [
        'DEPLOYMENT.md',
        'GITHUB_ACTIONS_SETUP.md',
        'README.md'
    ]
    for doc in docs:
        if not check_file(doc):
            all_good = False
    print()
    
    # Check for files to remove
    print("🗑️ FILES TO REMOVE (OPTIONAL):")
    remove_files = [
        'analyze_html.py',
        'investigate.py',
        'test_api.py',
        'setup_playwright.py',
        'validate_config.py'
    ]
    for f in remove_files:
        if os.path.exists(f):
            print(f"  ⚠️ {f} (should be removed)")
    print()
    
    # Check for files to remove from git
    print("🚫 CHECK GIT IGNORED:")
    print("  Ensure these are in .gitignore:")
    print("  • venv/")
    print("  • __pycache__/")
    print("  • *.log")
    print("  • .env (not .env.example)")
    print()
    
    # Config validation
    print("🔐 CONFIGURATION CHECK:")
    try:
        from npl_notifier.core.config import KHALTI_EVENT_URL
        print(f"  ✓ KHALTI_EVENT_URL configured")
    except:
        print(f"  ✗ KHALTI_EVENT_URL not configured")
        all_good = False
    
    # Check requirements
    print()
    print("📋 DEPENDENCIES:")
    print("  Required packages (in requirements.txt):")
    required = ['requests', 'python-dotenv', 'urllib3', 'gtts']
    with open('requirements.txt', 'r') as f:
        content = f.read()
        for pkg in required:
            found = pkg in content
            status = "✓" if found else "✗"
            print(f"    {status} {pkg}")
            if not found:
                all_good = False
    print()
    
    # Summary
    print("="*60)
    if all_good:
        print("✅ ALL CHECKS PASSED - READY FOR GITHUB ACTIONS")
        print()
        print("Next steps:")
        print("1. Optionally remove debug files (see CLEANUP_GUIDE.md)")
        print("2. Initialize git:")
        print("   git init")
        print("   git add .")
        print('   git commit -m "Setup GitHub Actions"')
        print("3. Add GitHub secrets in Settings > Secrets and variables")
        print("4. Push to GitHub:")
        print("   git push -u origin main")
        print()
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("Please review errors above and fix them")
        return 1

if __name__ == "__main__":
    sys.exit(main())
