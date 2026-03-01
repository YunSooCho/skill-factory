"""
MailerSend Email API Integration for Yoom Apps
"""

from .actions import MailersendActions
from .exceptions import (
    MailersendError,
    MailersendAuthenticationError,
    MailersendRateLimitError,
    MailersendNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailersendActions",
    "MailersendError",
    "MailersendAuthenticationError",
    "MailersendRateLimitError",
    "MailersendNotFoundError",
]
