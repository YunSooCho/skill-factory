"""BigMailer API"""

class BigMailerAPIError(Exception):
    """Base exception for BigMailer API errors"""
    pass

class BigMailerAuthError(BigMailerAPIError):
    """Authentication error"""
    pass

class BigMailerRateLimitError(BigMailerAPIError):
    """Rate limit exceeded"""
    pass