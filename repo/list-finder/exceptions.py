"""
Custom exceptions for list-finder API integration.
"""


class ListFinderError(Exception):
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


class ListFinderAuthenticationError(ListFinderError):
    """Authentication or authorization error."""
    pass


class ListFinderRateLimitError(ListFinderError):
    """Rate limit exceeded error."""
    pass


class ListFinderNotFoundError(ListFinderError):
    """Resource not found error."""
    pass


class ListFinderValidationError(ListFinderError):
    """Validation error for request parameters."""
    pass
