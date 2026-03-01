"""
Mailchimp Transactional API Integration for Yoom Apps
"""

from .actions import MailchimpTransactionalActions
from .exceptions import (
    MailchimpTransactionalError,
    MailchimpTransactionalAuthenticationError,
    MailchimpTransactionalRateLimitError,
    MailchimpTransactionalNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "MailchimpTransactionalActions",
    "MailchimpTransactionalError",
    "MailchimpTransactionalAuthenticationError",
    "MailchimpTransactionalRateLimitError",
    "MailchimpTransactionalNotFoundError",
]
