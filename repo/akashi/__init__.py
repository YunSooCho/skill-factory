"""
Akashi - Japanese Attendance & HR Management
"""

from .client import AkashiClient, AkashiError, AkashiRateLimitError, AkashiAuthenticationError

__all__ = [
    'AkashiClient',
    'AkashiError',
    'AkashiRateLimitError',
    'AkashiAuthenticationError'
]