"""
LeetCode service module.
Handles fetching and processing LeetCode problem data.
"""

from typing import List, Dict, Optional
import requests

from src.config import config
from src.utils.logger import logger


class LeetCodeService:
    """Service for interacting with LeetCode problem data."""

    def __init__(self):
        """Initialize LeetCode service."""
        self.rating_url = config.LEETCODE_RATING_URL
        self.problem_url_template = config.LEETCODE_PROBLEM_URL

    def fetch_problem_ratings(self) -> List[Dict]:
        """
        Fetch all LeetCode problem ratings from the data source.

        Returns:
            List of problem dictionaries with rating information

        Raises:
            requests.RequestException: If the HTTP request fails
        """
        try:
            logger.info("Fetching LeetCode problem ratings...")
            response = requests.get(self.rating_url, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Successfully fetched {len(data)} problems")

            return data

        except requests.RequestException as e:
            logger.error(f"Failed to fetch LeetCode ratings: {e}")
            raise

    def filter_by_rating(
        self,
        problems: List[Dict],
        target_rating: int,
        tolerance: Optional[int] = None
    ) -> List[Dict]:
        """
        Filter problems by target rating within tolerance range.

        Args:
            problems: List of problem dictionaries
            target_rating: Target difficulty rating
            tolerance: Rating tolerance (defaults to config.RATING_TOLERANCE)

        Returns:
            Filtered list of problems
        """
        if tolerance is None:
            tolerance = config.RATING_TOLERANCE

        filtered = []
        for problem in problems:
            # Validate required fields
            if 'Rating' not in problem or 'ID' not in problem:
                continue

            rating = problem['Rating']

            # Check if rating is within tolerance
            if abs(rating - target_rating) <= tolerance:
                filtered.append(problem)

        logger.info(
            f"Filtered {len(filtered)} problems with rating "
            f"{target_rating} ± {tolerance}"
        )

        return filtered

    def exclude_solved(
        self,
        problems: List[Dict],
        solved_ids: set
    ) -> List[Dict]:
        """
        Exclude problems that have already been solved/sent.

        Args:
            problems: List of problem dictionaries
            solved_ids: Set of problem IDs to exclude

        Returns:
            Filtered list of unsolved problems
        """
        unsolved = [
            p for p in problems
            if str(p.get('ID', '')) not in solved_ids
        ]

        logger.info(
            f"Filtered out {len(problems) - len(unsolved)} already solved problems. "
            f"{len(unsolved)} remaining"
        )

        return unsolved

    def get_problem_url(self, slug: str) -> str:
        """
        Get the full LeetCode URL for a problem.

        Args:
            slug: Problem title slug

        Returns:
            Full problem URL
        """
        return self.problem_url_template.format(slug=slug)

    def format_problem_info(self, problem: Dict) -> Dict[str, str]:
        """
        Format problem information for display.

        Args:
            problem: Problem dictionary

        Returns:
            Formatted problem information
        """
        return {
            'id': str(problem.get('ID', 'Unknown')),
            'title': problem.get('Title', 'Unknown'),
            'slug': problem.get('TitleSlug', ''),
            'rating': str(problem.get('Rating', 0)),
            'url': self.get_problem_url(problem.get('TitleSlug', ''))
        }
