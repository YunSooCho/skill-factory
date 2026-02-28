"""
Custom exceptions for Facebook Ads API integration.
"""


class FacebookAdsError(Exception):
    """Base exception for Facebook Ads API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class FacebookAdsAuthenticationError(FacebookAdsError):
    """Authentication or authorization error."""

    pass


class FacebookAdsRateLimitError(FacebookAdsError):
    """Rate limit exceeded error."""

    pass


class FacebookAdsNotFoundError(FacebookAdsError):
    """Resource not found error."""

    pass


class FacebookAdsValidationError(FacebookAdsError):
    """Validation error for request parameters."""

    pass