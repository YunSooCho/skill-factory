"""Bouncer API"""

class BouncerAPIError(Exception):
    """Base exception for Bouncer API errors"""
    pass

class BouncerAuthError(BouncerAPIError):
    """Authentication error"""
    pass

class BouncerRateLimitError(BouncerAPIError):
    """Rate limit exceeded"""
    pass