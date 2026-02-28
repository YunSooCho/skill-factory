"""
Google Analytics 4 API Integration for Yoom Apps
"""

from .actions import GoogleAnalyticsActions
from .exceptions import (
    GoogleAnalyticsError,
    GoogleAnalyticsAuthenticationError,
    GoogleAnalyticsRateLimitError,
    GoogleAnalyticsNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "GoogleAnalyticsActions",
    "GoogleAnalyticsError",
    "GoogleAnalyticsAuthenticationError",
    "GoogleAnalyticsRateLimitError",
    "GoogleAnalyticsNotFoundError",
]
