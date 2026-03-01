"""
Google Ads OAuth API Integration for Yoom Apps
"""

from .actions import GoogleAdsOauthActions
from .exceptions import (
    GoogleAdsOauthError,
    GoogleAdsOauthAuthenticationError,
    GoogleAdsOauthRateLimitError,
    GoogleAdsOauthNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "GoogleAdsOauthActions",
    "GoogleAdsOauthError",
    "GoogleAdsOauthAuthenticationError",
    "GoogleAdsOauthRateLimitError",
    "GoogleAdsOauthNotFoundError",
]
