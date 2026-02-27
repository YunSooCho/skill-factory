"""Brightcove API"""

class BrightcoveAPIError(Exception):
    """Base exception for Brightcove API errors"""
    pass

class BrightcoveAuthError(BrightcoveAPIError):
    """Authentication error"""
    pass

class BrightcoveRateLimitError(BrightcoveAPIError):
    """Rate limit exceeded"""
    pass