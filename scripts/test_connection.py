#!/usr/bin/env python3
"""
Connection test script.
Tests all external service connections before running the main application.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.services.sheets import SheetsService
from src.services.gemini import GeminiService
from src.services.telegram import TelegramService
from src.utils.logger import logger


def test_google_sheets():
    """Test Google Sheets connection."""
    print("\n📊 Testing Google Sheets connection...")
    try:
        sheets = SheetsService()
        target_rating = sheets.get_target_rating()
        history_count = len(sheets.get_history_ids())

        print(f"  ✅ Connected to spreadsheet: {config.SHEET_NAME}")
        print(f"  ✅ Target Rating: {target_rating}")
        print(f"  ✅ History entries: {history_count}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False


def test_gemini():
    """Test Gemini API connection."""
    print("\n🤖 Testing Gemini API connection...")
    try:
        gemini = GeminiService()
        if gemini.test_connection():
            print(f"  ✅ Connected to Gemini API")
            print(f"  ✅ Model: {config.GEMINI_MODEL}")
            return True
        else:
            print("  ❌ Connection test failed")
            return False
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False


def test_telegram():
    """Test Telegram bot connection."""
    print("\n📱 Testing Telegram bot connection...")
    try:
        telegram = TelegramService()
        if telegram.test_connection():
            print(f"  ✅ Telegram bot is active")
            print(f"  ✅ Chat ID: {config.telegram_chat_id}")
            return True
        else:
            print("  ❌ Connection test failed")
            return False
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False


def main():
    """Run all connection tests."""
    print("=" * 60)
    print("🔍 Service Connection Test")
    print("=" * 60)

    # Validate config first
    if not config.validate():
        print("\n❌ Configuration validation failed")
        print("Please check your environment variables:")
        print("  • TELEGRAM_BOT_TOKEN")
        print("  • TELEGRAM_CHAT_ID")
        print("  • GEMINI_API_KEY")
        print("  • GOOGLE_SHEETS_JSON")
        return 1

    # Run tests
    results = {
        "Google Sheets": test_google_sheets(),
        "Gemini API": test_gemini(),
        "Telegram Bot": test_telegram(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)

    all_passed = all(results.values())
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {service}: {status}")

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\n💡 Run the main script: python main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
