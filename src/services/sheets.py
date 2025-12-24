"""
Google Sheets service module.
Handles all interactions with Google Sheets for configuration and history tracking.
"""

import json
from typing import Set, Optional

import gspread
from google.oauth2.service_account import Credentials

from src.config import config
from src.utils.logger import logger


class SheetsService:
    """Service for interacting with Google Sheets."""

    # Google API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self):
        """Initialize Google Sheets service."""
        self.client = None
        self.spreadsheet = None
        self._connect()

    def _connect(self):
        """Establish connection to Google Sheets."""
        try:
            logger.info("Connecting to Google Sheets...")

            # Parse service account credentials
            creds_dict = json.loads(config.google_sheets_json)

            # Create credentials
            credentials = Credentials.from_service_account_info(
                creds_dict,
                scopes=self.SCOPES
            )

            # Authorize client
            self.client = gspread.authorize(credentials)

            # Open spreadsheet
            self.spreadsheet = self.client.open(config.SHEET_NAME)

            logger.info(f"Successfully connected to spreadsheet: {config.SHEET_NAME}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid Google Sheets JSON credentials: {e}")
            raise

        except gspread.exceptions.SpreadsheetNotFound:
            logger.error(
                f"Spreadsheet '{config.SHEET_NAME}' not found. "
                "Please ensure it exists and the service account has access."
            )
            raise

        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            raise

    def get_target_rating(self) -> int:
        """
        Retrieve target rating from Settings worksheet.

        Returns:
            Target rating value

        Raises:
            ValueError: If the rating value is invalid
        """
        try:
            worksheet = self.spreadsheet.worksheet(config.SETTINGS_WORKSHEET)
            rating_value = worksheet.acell('B1').value

            if not rating_value:
                raise ValueError("Target rating (B1) is empty")

            rating = int(rating_value)
            logger.info(f"Target rating: {rating}")

            return rating

        except gspread.exceptions.WorksheetNotFound:
            logger.error(
                f"Worksheet '{config.SETTINGS_WORKSHEET}' not found. "
                "Please create it in your spreadsheet."
            )
            raise

        except ValueError as e:
            logger.error(f"Invalid target rating value: {e}")
            raise

    def get_history_ids(self) -> Set[str]:
        """
        Retrieve set of problem IDs from History worksheet.

        Returns:
            Set of problem IDs that have been sent before
        """
        try:
            worksheet = self.spreadsheet.worksheet(config.HISTORY_WORKSHEET)

            # Read all values from column A
            values = worksheet.col_values(1)

            # Skip header row and create set
            history_ids = set(values[1:]) if len(values) > 1 else set()

            logger.info(f"Loaded {len(history_ids)} problem IDs from history")

            return history_ids

        except gspread.exceptions.WorksheetNotFound:
            logger.warning(
                f"Worksheet '{config.HISTORY_WORKSHEET}' not found. "
                "Creating new history..."
            )
            return set()

        except Exception as e:
            logger.error(f"Failed to read history: {e}")
            return set()

    def add_to_history(self, problem_id: str) -> bool:
        """
        Add a problem ID to the history worksheet.

        Args:
            problem_id: Problem ID to add

        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self.spreadsheet.worksheet(config.HISTORY_WORKSHEET)
            worksheet.append_row([problem_id])

            logger.info(f"Added problem ID {problem_id} to history")
            return True

        except Exception as e:
            logger.error(f"Failed to add problem to history: {e}")
            return False

    def initialize_sheets(self):
        """
        Initialize spreadsheet with required worksheets if they don't exist.
        This is a helper method for setup.
        """
        try:
            # Check/create Settings worksheet
            try:
                settings = self.spreadsheet.worksheet(config.SETTINGS_WORKSHEET)
                logger.info("Settings worksheet already exists")
            except gspread.exceptions.WorksheetNotFound:
                logger.info("Creating Settings worksheet...")
                settings = self.spreadsheet.add_worksheet(
                    title=config.SETTINGS_WORKSHEET,
                    rows=10,
                    cols=5
                )
                settings.update('A1:B1', [['Target_Rating', '1500']])
                logger.info("Settings worksheet created with default rating 1500")

            # Check/create History worksheet
            try:
                history = self.spreadsheet.worksheet(config.HISTORY_WORKSHEET)
                logger.info("History worksheet already exists")
            except gspread.exceptions.WorksheetNotFound:
                logger.info("Creating History worksheet...")
                history = self.spreadsheet.add_worksheet(
                    title=config.HISTORY_WORKSHEET,
                    rows=1000,
                    cols=1
                )
                history.update('A1', [['Problem_ID']])
                logger.info("History worksheet created")

            logger.info("Spreadsheet initialization complete")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize spreadsheet: {e}")
            return False
