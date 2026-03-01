"""
Liny Contact Management API Integration for Yoom Apps
"""

from .actions import LinyActions
from .exceptions import (
    LinyError,
    LinyAuthenticationError,
    LinyRateLimitError,
    LinyNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "LinyActions",
    "LinyError",
    "LinyAuthenticationError",
    "LinyRateLimitError",
    "LinyNotFoundError",
]
