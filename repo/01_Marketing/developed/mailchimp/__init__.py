"""
Mailchimp Email Marketing API Integration for Yoom Apps
"""

from .actions import MailchimpActions
from .exceptions import (
    MailchimpError,
    MailchimpAuthenticationError,
    MailchimpRateLimitError,
    MailchimpNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailchimpActions",
    "MailchimpError",
    "MailchimpAuthenticationError",
    "MailchimpRateLimitError",
    "MailchimpNotFoundError",
]
