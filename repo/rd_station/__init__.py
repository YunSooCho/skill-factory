"""
 RD Station - Yoom Apps
 Marketing automation and lead management API integration
"""

__version__ = "1.0.0"
__author__ = "Yoom Apps"

from .client import RDStationClient
from .models import (
    Contact,
    ConversionEvent,
    ContactListResponse,
)
from .exceptions import RDStationError, RateLimitError, AuthenticationError

__all__ = [
    "RDStationClient",
    "Contact",
    "ConversionEvent",
    "ContactListResponse",
    "RDStationError",
    "RateLimitError",
    "AuthenticationError",
]