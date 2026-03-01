"""
Custom exceptions for location_io API integration.
"""


class LocationIoError(Exception):
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


class LocationIoAuthenticationError(LocationIoError):
    """Authentication or authorization error."""
    pass


class LocationIoRateLimitError(LocationIoError):
    """Rate limit exceeded error."""
    pass


class LocationIoNotFoundError(LocationIoError):
    """Resource not found error."""
    pass


class LocationIoValidationError(LocationIoError):
    """Validation error for request parameters."""
    pass
