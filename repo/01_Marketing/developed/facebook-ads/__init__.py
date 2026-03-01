"""
Facebook Ads (Meta Marketing API) Integration for Yoom Apps

This module provides API actions and triggers for Facebook Ads operations.
"""

from .actions import FacebookAdsActions
from .triggers import FacebookAdsTriggers
from .exceptions import (
    FacebookAdsError,
    FacebookAdsAuthenticationError,
    FacebookAdsRateLimitError,
    FacebookAdsNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "FacebookAdsActions",
    "FacebookAdsTriggers",
    "FacebookAdsError",
    "FacebookAdsAuthenticationError",
    "FacebookAdsRateLimitError",
    "FacebookAdsNotFoundError",
]