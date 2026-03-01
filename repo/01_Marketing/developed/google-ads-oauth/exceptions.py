"""
Custom exceptions for google-ads-oauth API integration.
"""


class GoogleAdsOauthError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class GoogleAdsOauthAuthenticationError(GoogleAdsOauthError):
    """Authentication or authorization error."""
    pass


class GoogleAdsOauthRateLimitError(GoogleAdsOauthError):
    """Rate limit exceeded error."""
    pass


class GoogleAdsOauthNotFoundError(GoogleAdsOauthError):
    """Resource not found error."""
    pass


class GoogleAdsOauthValidationError(GoogleAdsOauthError):
    """Validation error for request parameters."""
    pass
