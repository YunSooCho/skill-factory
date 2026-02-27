"""Beamer API"""


class BeamerAPIError(Exception):
    """Base exception for Beamer API errors"""
    pass


class BeamerAuthError(BeamerAPIError):
    """Authentication error"""
    pass


class BeamerRateLimitError(BeamerAPIError):
    """Rate limit exceeded"""
    pass