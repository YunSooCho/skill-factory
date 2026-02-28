"""
 Elastic Email - Yoom Apps
 Email marketing and contact management API integration
"""

__version__ = "1.0.0"
__author__ = "Yoom Apps"

from .client import ElasticEmailClient
from .models import Contact, EmailList, ContactListResponse, EmailListListResponse
from .exceptions import ElasticEmailError, RateLimitError, AuthenticationError

__all__ = [
    "ElasticEmailClient",
    "Contact",
    "EmailList",
    "ContactListResponse",
    "EmailListListResponse",
    "ElasticEmailError",
    "RateLimitError",
    "AuthenticationError",
]