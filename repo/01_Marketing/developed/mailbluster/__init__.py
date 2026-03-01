"""
MailBluster Email API Integration for Yoom Apps
"""

from .actions import MailblusterActions
from .exceptions import (
    MailblusterError,
    MailblusterAuthenticationError,
    MailblusterRateLimitError,
    MailblusterNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailblusterActions",
    "MailblusterError",
    "MailblusterAuthenticationError",
    "MailblusterRateLimitError",
    "MailblusterNotFoundError",
]
