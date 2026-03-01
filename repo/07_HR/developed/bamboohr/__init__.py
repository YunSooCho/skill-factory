"""
BambooHR - HR Management Platform
"""

from .client import BambooHRClient, BambooHRError, BambooHRRateLimitError, BambooHRAuthenticationError

__all__ = [
    'BambooHRClient',
    'BambooHRError',
    'BambooHRRateLimitError',
    'BambooHRAuthenticationError'
]