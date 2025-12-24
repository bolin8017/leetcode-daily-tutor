#!/usr/bin/env python3
"""
LeetCode Daily AI Tutor
Main entry point for the application.

This script orchestrates the daily LeetCode problem delivery:
1. Fetches LeetCode problem ratings
2. Filters problems based on target rating from Google Sheets
3. Excludes already-sent problems
4. Generates AI solution using Gemini
5. Sends formatted message to Telegram
6. Records problem in history
"""

import sys
import random
from typing import Optional, Dict

from src.config import config
from src.utils.logger import logger
from src.services.leetcode import LeetCodeService
from src.services.sheets import SheetsService
from src.services.gemini import GeminiService
from src.services.telegram import TelegramService


class LeetCodeDailyTutor:
    """Main application orchestrator."""

    def __init__(self):
        """Initialize all services."""
        logger.info("=" * 60)
        logger.info("🚀 LeetCode Daily AI Tutor Starting...")
        logger.info("=" * 60)

        # Validate configuration
        if not config.validate():
            logger.error("Configuration validation failed")
            sys.exit(1)

        # Initialize services
        try:
            self.leetcode = LeetCodeService()
            self.sheets = SheetsService()
            self.gemini = GeminiService()
            self.telegram = TelegramService()
            logger.info("All services initialized successfully")
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
            sys.exit(1)

    def select_problem(self) -> Optional[Dict]:
        """
        Select a suitable problem based on criteria.

        Returns:
            Selected problem dictionary or None if no suitable problem found
        """
        # Step 1: Fetch all problems
        try:
            all_problems = self.leetcode.fetch_problem_ratings()
        except Exception as e:
            logger.error(f"Failed to fetch problems: {e}")
            return None

        # Step 2: Get target rating from Google Sheets
        try:
            target_rating = self.sheets.get_target_rating()
        except Exception as e:
            logger.error(f"Failed to get target rating: {e}")
            return None

        # Step 3: Get history of sent problems
        history_ids = self.sheets.get_history_ids()

        # Step 4: Filter problems by rating
        candidates = self.leetcode.filter_by_rating(all_problems, target_rating)

        # Step 5: Exclude already-sent problems
        candidates = self.leetcode.exclude_solved(candidates, history_ids)

        # Step 6: Check if we have candidates
        if not candidates:
            logger.error("No suitable problems found!")
            logger.info(
                "💡 Suggestions:\n"
                "   - Adjust Target_Rating in Google Sheets\n"
                "   - Clear some entries from History worksheet\n"
                f"   - Current target: {target_rating}, "
                f"History count: {len(history_ids)}"
            )
            return None

        # Step 7: Randomly select one problem
        problem = random.choice(candidates)
        logger.info(
            f"🎲 Selected problem: {problem.get('Title')} "
            f"(ID: {problem.get('ID')}, Rating: {problem.get('Rating')})"
        )

        return problem

    def process_problem(self, problem: Dict) -> bool:
        """
        Process a selected problem: generate solution and send to Telegram.

        Args:
            problem: Problem dictionary

        Returns:
            True if processing was successful
        """
        # Format problem information
        problem_info = self.leetcode.format_problem_info(problem)

        # Generate AI solution
        try:
            solution = self.gemini.generate_solution(problem_info)
        except Exception as e:
            logger.error(f"Solution generation failed: {e}")
            # Continue with fallback message
            solution = "⚠️ AI 解法生成失敗，請參考題目連結"

        # Format Telegram message
        message = self.telegram.format_daily_message(problem_info, solution)

        # Send to Telegram
        if not self.telegram.send_message(message):
            logger.error("Failed to send message to Telegram")
            return False

        # Add to history
        if not self.sheets.add_to_history(problem_info['id']):
            logger.warning("Failed to update history (message was sent)")
            # Don't return False here - message was already sent

        return True

    def run(self) -> int:
        """
        Main execution flow.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            # Select a problem
            problem = self.select_problem()
            if not problem:
                return 1

            # Process the problem
            if not self.process_problem(problem):
                return 1

            logger.info("=" * 60)
            logger.info("✅ Daily problem sent successfully!")
            logger.info("=" * 60)
            return 0

        except KeyboardInterrupt:
            logger.info("\n⚠️  Process interrupted by user")
            return 1

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return 1


def main():
    """Application entry point."""
    app = LeetCodeDailyTutor()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
