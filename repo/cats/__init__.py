"""
CATS - Applicant Tracking System (ATS)
"""

from .client import CATSClient, CATSError, CATSRateLimitError, CATSAuthenticationError

__all__ = [
    'CATSClient',
    'CATSError',
    'CATSRateLimitError',
    'CATSAuthenticationError'
]