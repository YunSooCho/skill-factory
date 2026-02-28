"""
 Email List Verify - Yoom Apps
 Email verification and validation API integration
"""

__version__ = "1.0.0"
__author__ = "Yoom Apps"

from .client import EmailListVerifyClient
from .models import (
    VerificationResult,
    DeliverabilityResult,
    BusinessEmailResult,
)
from .exceptions import EmailListVerifyError, RateLimitError, AuthenticationError

__all__ = [
    "EmailListVerifyClient",
    "VerificationResult",
    "DeliverabilityResult",
    "BusinessEmailResult",
    "EmailListVerifyError",
    "RateLimitError",
    "AuthenticationError",
]