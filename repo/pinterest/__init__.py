"""
Pinterest API Integration for Yoom Apps

This module provides API actions and triggers for Pinterest operations.
"""

from .actions import PinterestActions
from .triggers import PinterestTriggers
from .exceptions import (
    PinterestAPIError,
    PinterestAuthenticationError,
    PinterestRateLimitError,
    PinterestNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "PinterestActions",
    "PinterestTriggers",
    "PinterestAPIError",
    "PinterestAuthenticationError",
    "PinterestRateLimitError",
    "PinterestNotFoundError",
]