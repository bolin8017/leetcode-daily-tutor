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

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Send a message to the configured Telegram chat.
        If message is too long (>4000 chars), split into multiple messages.

        Args:
            text: Message text to send
            parse_mode: Parse mode for formatting (Markdown or HTML)

        Returns:
            True if message was sent successfully, False otherwise
        """
        MAX_MESSAGE_LENGTH = 4000  # Telegram limit is 4096, use 4000 for safety

        try:
            logger.info("Sending message to Telegram...")

            # If message is short enough, send directly
            if len(text) <= MAX_MESSAGE_LENGTH:
                return self._send_single_message(text, parse_mode)

            # Split long message into chunks
            logger.info(f"Message too long ({len(text)} chars), splitting...")
            chunks = self._split_message(text, MAX_MESSAGE_LENGTH)

            for i, chunk in enumerate(chunks, 1):
                logger.info(f"Sending chunk {i}/{len(chunks)}...")
                if not self._send_single_message(chunk, parse_mode):
                    logger.error(f"Failed to send chunk {i}")
                    return False

            logger.info("All message chunks sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def _send_single_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Send a single message to Telegram.

        Args:
            text: Message text to send
            parse_mode: Parse mode for formatting (Markdown or HTML)

        Returns:
            True if message was sent successfully
        """
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to send message: {e}")

            # If Markdown parsing failed, try sending without parse_mode
            if parse_mode and "Bad Request" in str(e):
                logger.warning("Markdown parsing failed, retrying without formatting...")
                try:
                    payload_plain = {
                        "chat_id": self.chat_id,
                        "text": text,
                        "disable_web_page_preview": True
                    }
                    response = requests.post(url, json=payload_plain, timeout=30)
                    response.raise_for_status()
                    logger.info("Message sent successfully without formatting")
                    return True
                except requests.RequestException as e2:
                    logger.error(f"Failed to send plain text message: {e2}")

            return False

    def _split_message(self, text: str, max_length: int) -> list:
        """
        Split a long message into chunks at natural breakpoints.

        Args:
            text: The text to split
            max_length: Maximum length per chunk

        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by lines first
        lines = text.split('\n')

        for line in lines:
            # If adding this line would exceed limit
            if len(current_chunk) + len(line) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                # If single line is too long, split it
                if len(line) > max_length:
                    # Split at word boundaries
                    words = line.split(' ')
                    for word in words:
                        if len(current_chunk) + len(word) + 1 > max_length:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = word
                        else:
                            current_chunk += (' ' if current_chunk else '') + word
                else:
                    current_chunk = line
            else:
                current_chunk += ('\n' if current_chunk else '') + line

        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def format_daily_message(
        self,
        problem_info: Dict[str, str],
        solution: str
    ) -> str:
        """
        Format a daily problem message using HTML formatting.

        Args:
            problem_info: Problem information dictionary
            solution: AI-generated solution text

        Returns:
            Formatted message text in HTML
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Format solution with better HTML structure
        solution_formatted = self._format_solution_html(solution)

        message = f"""📅 <b>LeetCode Daily Challenge - {today}</b>

🏆 <b>題目</b>: {problem_info.get('title', 'Unknown')}
⭐ <b>Rating</b>: {problem_info.get('rating', 'N/A')}
🔗 <a href="{problem_info.get('url', '')}">題目連結</a>

━━━━━━━━━━━━━━━━

{solution_formatted}

━━━━━━━━━━━━━━━━
💬 祝你練習順利！加油！🚀
"""
        return message

    def _format_solution_html(self, text: str) -> str:
        """
        Format solution text with proper HTML tags for better readability.

        - Wraps code blocks in <pre><code> tags
        - Converts **text** to <b>text</b>
        - Converts section headers to bold
        - Preserves structure while making it Telegram-friendly

        Args:
            text: Solution text to format

        Returns:
            HTML-formatted text
        """
        import re

        # First, protect code blocks by replacing them with placeholders
        code_blocks = []
        def save_code_block(match):
            code = match.group(1)
            # Escape HTML in code
            code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            code_blocks.append(code_escaped)
            return f"<<<CODE_BLOCK_{len(code_blocks)-1}>>>"

        # Match code blocks (```...```)
        text = re.sub(r'```(?:cpp|c\+\+)?\n?(.*?)```', save_code_block, text, flags=re.DOTALL)

        # Escape remaining HTML characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Convert **text** to <b>text</b>
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)

        # Convert markdown headers ### to bold
        text = re.sub(r'^###\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
        text = re.sub(r'^#\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

        # Restore code blocks with proper formatting
        for i, code in enumerate(code_blocks):
            text = text.replace(f"<<<CODE_BLOCK_{i}>>>", f"\n<pre><code class=\"language-cpp\">{code}</code></pre>\n")

        return text

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
