"""
YouTube Data API Client for Yoom Apps Integration.
"""

from .actions import YoutubeDataActions
from .exceptions import (
    YoutubeDataError,
    YoutubeDataAuthenticationError,
    YoutubeDataRateLimitError,
    YoutubeDataNotFoundError,
    YoutubeDataValidationError,
)

__all__ = [
    "YoutubeDataActions",
    "YoutubeDataError",
    "YoutubeDataAuthenticationError",
    "YoutubeDataRateLimitError",
    "YoutubeDataNotFoundError",
    "YoutubeDataValidationError",
]

__version__ = "1.0.0"