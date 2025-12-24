"""
Telegram Bot service module.
Handles sending formatted messages to Telegram.
"""

from datetime import datetime
from typing import Dict
import requests

from src.config import config
from src.utils.logger import logger


class TelegramService:
    """Service for sending messages via Telegram Bot API."""

    def __init__(self):
        """Initialize Telegram service."""
        self.bot_token = config.telegram_bot_token
        self.chat_id = config.telegram_chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        logger.info("Telegram service initialized")

    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """
        Send a message to the configured Telegram chat.

        Args:
            text: Message text to send
            parse_mode: Parse mode for formatting (Markdown or HTML)

        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            logger.info("Sending message to Telegram...")

            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            logger.info("Message sent successfully")
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def format_daily_message(
        self,
        problem_info: Dict[str, str],
        solution: str
    ) -> str:
        """
        Format a daily problem message.

        Args:
            problem_info: Problem information dictionary
            solution: AI-generated solution text

        Returns:
            Formatted message text
        """
        today = datetime.now().strftime("%Y-%m-%d")

        message = f"""📅 **LeetCode Daily Challenge - {today}**

🏆 **題目**: {problem_info.get('title', 'Unknown')}
⭐ **Rating**: {problem_info.get('rating', 'N/A')}
🔗 [題目連結]({problem_info.get('url', '')})

---

{solution}

---
💬 祝你練習順利！加油！🚀
"""
        return message

    def test_connection(self) -> bool:
        """
        Test Telegram bot connection by calling getMe API.

        Returns:
            True if connection is successful
        """
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                logger.info(
                    f"Telegram bot connected: @{bot_info.get('username', 'unknown')}"
                )
                return True

            return False

        except Exception as e:
            logger.error(f"Telegram connection test failed: {e}")
            return False
