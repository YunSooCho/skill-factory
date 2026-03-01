"""
GetResponse Email Marketing API Integration for Yoom Apps
"""

from .actions import GetresponseApiActions
from .exceptions import (
    GetresponseApiError,
    GetresponseApiAuthenticationError,
    GetresponseApiRateLimitError,
    GetresponseApiNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "GetresponseApiActions",
    "GetresponseApiError",
    "GetresponseApiAuthenticationError",
    "GetresponseApiRateLimitError",
    "GetresponseApiNotFoundError",
]
