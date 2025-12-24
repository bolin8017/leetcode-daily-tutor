#!/usr/bin/env python3
"""
Google Sheets setup script.
Initializes the required worksheets in your Google Sheets spreadsheet.
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.sheets import SheetsService
from src.utils.logger import logger


def main():
    """Setup Google Sheets with required worksheets."""
    print("=" * 60)
    print("📊 Google Sheets Setup Utility")
    print("=" * 60)
    print()

    try:
        # Initialize sheets service
        logger.info("Connecting to Google Sheets...")
        sheets = SheetsService()

        # Initialize worksheets
        logger.info("Initializing worksheets...")
        if sheets.initialize_sheets():
            print()
            print("=" * 60)
            print("✅ Google Sheets setup complete!")
            print("=" * 60)
            print()
            print("📋 Worksheets created:")
            print("  • Settings - Contains your target rating configuration")
            print("  • History - Tracks sent problems")
            print()
            print("💡 Next steps:")
            print("  1. Open your spreadsheet in Google Sheets")
            print("  2. Adjust the Target_Rating in cell B1 if needed")
            print("  3. Run the test script: python scripts/test_connection.py")
            return 0
        else:
            logger.error("Failed to initialize worksheets")
            return 1

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print()
        print("❌ Setup failed. Please check:")
        print("  • GOOGLE_SHEETS_JSON environment variable is set")
        print("  • Service account has access to the spreadsheet")
        print("  • Spreadsheet name matches config (LeetCode_Daily_Tutor)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
