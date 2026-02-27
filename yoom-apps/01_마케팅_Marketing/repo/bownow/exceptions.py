"""BoNow API"""

class BoNowAPIError(Exception):
    """Base exception for BoNow API errors"""
    pass

class BoNowAuthError(BoNowAPIError):
    """Authentication error"""
    pass

class BoNowRateLimitError(BoNowAPIError):
    """Rate limit exceeded"""
    pass