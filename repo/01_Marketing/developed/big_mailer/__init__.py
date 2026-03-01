"""
 Big Mailer - Yoom Apps
 Contact management API integration
"""

__version__ = "1.0.0"
__author__ = "Yoom Apps"

from .client import BigMailerClient
from .models import Contact, ContactField, ContactListResponse, FieldListResponse
from .exceptions import BigMailerError, RateLimitError, AuthenticationError

__all__ = [
    "BigMailerClient",
    "Contact",
    "ContactField",
    "ContactListResponse",
    "FieldListResponse",
    "BigMailerError",
    "RateLimitError",
    "AuthenticationError",
]