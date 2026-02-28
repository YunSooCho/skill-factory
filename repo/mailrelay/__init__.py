"""
MailRelay Email API Integration for Yoom Apps
"""

from .actions import MailrelayActions
from .exceptions import (
    MailrelayError,
    MailrelayAuthenticationError,
    MailrelayRateLimitError,
    MailrelayNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailrelayActions",
    "MailrelayError",
    "MailrelayAuthenticationError",
    "MailrelayRateLimitError",
    "MailrelayNotFoundError",
]
