"""
Loops Email API Integration for Yoom Apps
"""

from .actions import LoopsActions
from .exceptions import (
    LoopsError,
    LoopsAuthenticationError,
    LoopsRateLimitError,
    LoopsNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "LoopsActions",
    "LoopsError",
    "LoopsAuthenticationError",
    "LoopsRateLimitError",
    "LoopsNotFoundError",
]
