"""
MailerCloud Email API Integration for Yoom Apps
"""

from .actions import MailercloudActions
from .exceptions import (
    MailercloudError,
    MailercloudAuthenticationError,
    MailercloudRateLimitError,
    MailercloudNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailercloudActions",
    "MailercloudError",
    "MailercloudAuthenticationError",
    "MailercloudRateLimitError",
    "MailercloudNotFoundError",
]
