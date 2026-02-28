"""
Kickbox Email Verification API Integration for Yoom Apps
"""

from .actions import KickboxActions
from .exceptions import (
    KickboxError,
    KickboxAuthenticationError,
    KickboxRateLimitError,
    KickboxNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "KickboxActions",
    "KickboxError",
    "KickboxAuthenticationError",
    "KickboxRateLimitError",
    "KickboxNotFoundError",
]
