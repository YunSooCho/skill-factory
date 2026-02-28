"""
Custom exceptions for Pinterest API integration.
"""


class PinterestAPIError(Exception):
    """Base exception for Pinterest API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class PinterestAuthenticationError(PinterestAPIError):
    """Authentication or authorization error."""

    pass


class PinterestRateLimitError(PinterestAPIError):
    """Rate limit exceeded error."""

    pass


class PinterestNotFoundError(PinterestAPIError):
    """Resource not found error."""

    pass


class PinterestValidationError(PinterestAPIError):
    """Validation error for request parameters."""

    pass