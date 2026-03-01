"""
Custom exceptions for loops API integration.
"""


class LoopsError(Exception):
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


class LoopsAuthenticationError(LoopsError):
    """Authentication or authorization error."""
    pass


class LoopsRateLimitError(LoopsError):
    """Rate limit exceeded error."""
    pass


class LoopsNotFoundError(LoopsError):
    """Resource not found error."""
    pass


class LoopsValidationError(LoopsError):
    """Validation error for request parameters."""
    pass
