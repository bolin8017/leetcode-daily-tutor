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
        try:
            logger.info("Sending message to Telegram...")

            # If message is short enough, send directly
            if len(text) <= config.TELEGRAM_MAX_MESSAGE_LENGTH:
                return self._send_single_message(text, parse_mode)

            # Split long message into chunks
            logger.info(f"Message too long ({len(text)} chars), splitting...")
            chunks = self._split_message(text, config.TELEGRAM_MAX_MESSAGE_LENGTH)

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

            response = requests.post(url, json=payload, timeout=config.TELEGRAM_REQUEST_TIMEOUT)
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
                    response = requests.post(url, json=payload_plain, timeout=config.TELEGRAM_REQUEST_TIMEOUT)
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
        Format a daily problem message using HTML.

        Args:
            problem_info: Problem information dictionary
            solution: AI-generated solution text (markdown format)

        Returns:
            Formatted message text in HTML
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Convert markdown solution to HTML-friendly format
        solution_html = self._convert_markdown_to_html(solution)

        message = f"""<b>LeetCode Daily Challenge - {today}</b>

🏆 <b>題目</b>: {problem_info.get('title', 'Unknown')}
⭐ <b>Rating</b>: {problem_info.get('rating', 'N/A')}
🔗 <a href="{problem_info.get('url', '')}">題目連結</a>

━━━━━━━━━━━━━━━━

{solution_html}

━━━━━━━━━━━━━━━━
祝你練習順利！加油！
"""
        return message

    def _convert_markdown_to_html(self, text: str) -> str:
        """
        Convert markdown solution to HTML format for Telegram.

        Strategy: Extract code blocks first, convert the rest to HTML, then restore code blocks.

        Args:
            text: Markdown formatted text

        Returns:
            HTML formatted text
        """
        import re

        # Step 1: Extract and protect code blocks
        code_blocks = []
        def extract_code_block(match):
            code = match.group(1).strip()
            # Don't escape HTML in code - keep it raw for <pre>
            code_blocks.append(code)
            return f"\n___CODE_BLOCK_{len(code_blocks)-1}___\n"

        # Extract code blocks (```cpp ... ``` or ``` ... ```)
        text = re.sub(r'```(?:cpp|c\+\+)?\s*\n(.*?)\n```', extract_code_block, text, flags=re.DOTALL | re.IGNORECASE)

        # Step 2: Convert remaining markdown to HTML
        # Escape HTML characters in non-code content
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Convert headers (##) to bold
        text = re.sub(r'^##\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

        # Convert **text** to <b>text</b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

        # Convert inline `code` to <code>code</code>
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

        # Step 3: Restore code blocks with <pre> tags
        for i, code in enumerate(code_blocks):
            # Escape HTML in code content
            code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            text = text.replace(f"___CODE_BLOCK_{i}___", f"<pre>{code_escaped}</pre>")

        return text

    def test_connection(self) -> bool:
        """
        Test Telegram bot connection by calling getMe API.

        Returns:
            True if connection is successful
        """
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=config.HTTP_QUICK_TIMEOUT)
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
