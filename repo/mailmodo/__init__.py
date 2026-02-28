"""
Mailmodo Email API Integration for Yoom Apps
"""

from .actions import MailmodoActions
from .exceptions import (
    MailmodoError,
    MailmodoAuthenticationError,
    MailmodoRateLimitError,
    MailmodoNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailmodoActions",
    "MailmodoError",
    "MailmodoAuthenticationError",
    "MailmodoRateLimitError",
    "MailmodoNotFoundError",
]
