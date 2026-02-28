"""
 Pinterest Integration - Yoom Apps
 Pinterest API v5 integration for pin and board management
"""

__version__ = "1.0.0"
__author__ = "Yoom Apps"

from .client import PinterestClient
from .models import Pin, Board, PinListResponse, BoardListResponse
from .exceptions import PinterestAPIError, RateLimitError, AuthenticationError

__all__ = [
    "PinterestClient",
    "Pin",
    "Board",
    "PinListResponse",
    "BoardListResponse",
    "PinterestAPIError",
    "RateLimitError",
    "AuthenticationError",
]