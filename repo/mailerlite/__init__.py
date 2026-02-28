"""
MailerLite Email API Integration for Yoom Apps
"""

from .actions import MailerliteActions
from .exceptions import (
    MailerliteError,
    MailerliteAuthenticationError,
    MailerliteRateLimitError,
    MailerliteNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailerliteActions",
    "MailerliteError",
    "MailerliteAuthenticationError",
    "MailerliteRateLimitError",
    "MailerliteNotFoundError",
]
