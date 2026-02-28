"""
Custom exceptions for liny API integration.
"""


class LinyError(Exception):
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


class LinyAuthenticationError(LinyError):
    """Authentication or authorization error."""
    pass


class LinyRateLimitError(LinyError):
    """Rate limit exceeded error."""
    pass


class LinyNotFoundError(LinyError):
    """Resource not found error."""
    pass


class LinyValidationError(LinyError):
    """Validation error for request parameters."""
    pass
