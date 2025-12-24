"""
Configuration management module.
Handles environment variables and application settings.
"""

import os
import sys
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # LeetCode settings
    LEETCODE_RATING_URL: str = "https://zerotrac.github.io/leetcode_problem_rating/data.json"
    LEETCODE_PROBLEM_URL: str = "https://leetcode.com/problems/{slug}/"
    RATING_TOLERANCE: int = 50

    # Google Sheets settings
    SHEET_NAME: str = "LeetCode_Daily_Tutor"
    SETTINGS_WORKSHEET: str = "Settings"
    HISTORY_WORKSHEET: str = "History"

    # API Keys and Tokens (loaded from environment)
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    gemini_api_key: Optional[str] = None
    google_sheets_json: Optional[str] = None

    # Gemini settings
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 7500  # Safe limit (max is 8000)

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def __post_init__(self):
        """Load environment variables after initialization."""
        self.load_env_vars()

    def load_env_vars(self):
        """Load required environment variables."""
        self.telegram_bot_token = self._get_env_var("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = self._get_env_var("TELEGRAM_CHAT_ID")
        self.gemini_api_key = self._get_env_var("GEMINI_API_KEY")
        self.google_sheets_json = self._get_env_var("GOOGLE_SHEETS_JSON")

    @staticmethod
    def _get_env_var(var_name: str) -> str:
        """
        Safely retrieve environment variable.

        Args:
            var_name: Name of the environment variable

        Returns:
            Value of the environment variable

        Raises:
            SystemExit: If the environment variable is not set
        """
        value = os.getenv(var_name)
        if not value:
            print(f"❌ Error: Environment variable '{var_name}' is not set")
            print(f"💡 Please set {var_name} in your environment or GitHub Secrets")
            sys.exit(1)
        return value

    def validate(self) -> bool:
        """
        Validate that all required configuration is present.

        Returns:
            True if configuration is valid
        """
        required_fields = [
            "telegram_bot_token",
            "telegram_chat_id",
            "gemini_api_key",
            "google_sheets_json",
        ]

        for field in required_fields:
            if not getattr(self, field):
                print(f"❌ Validation failed: {field} is not configured")
                return False

        return True


# Global configuration instance
config = Config()
