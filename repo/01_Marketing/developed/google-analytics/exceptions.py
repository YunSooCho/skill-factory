"""
Custom exceptions for google-analytics API integration.
"""


class GoogleAnalyticsError(Exception):
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


class GoogleAnalyticsAuthenticationError(GoogleAnalyticsError):
    """Authentication or authorization error."""
    pass


class GoogleAnalyticsRateLimitError(GoogleAnalyticsError):
    """Rate limit exceeded error."""
    pass


class GoogleAnalyticsNotFoundError(GoogleAnalyticsError):
    """Resource not found error."""
    pass


class GoogleAnalyticsValidationError(GoogleAnalyticsError):
    """Validation error for request parameters."""
    pass
