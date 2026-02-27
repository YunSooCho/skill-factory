"""Beehiiv API"""


class BeehiivAPIError(Exception):
    """Base exception for Beehiiv API errors"""
    pass


class BeehiivAuthError(BeehiivAPIError):
    """Authentication error"""
    pass


class BeehiivRateLimitError(BeehiivAPIError):
    """Rate limit exceeded"""
    pass