"""Bitly API"""

class BitlyAPIError(Exception):
    """Base exception for Bitly API errors"""
    pass

class BitlyAuthError(BitlyAPIError):
    """Authentication error"""
    pass

class BitlyRateLimitError(BitlyAPIError):
    """Rate limit exceeded"""
    pass