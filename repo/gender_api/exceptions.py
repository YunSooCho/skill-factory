"""Custom exceptions for Gender API."""
class GenderAPIError(Exception):
    """Base exception for Gender API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class GenderAPIAuthenticationError(GenderAPIError):
    """Authentication error."""


class GenderAPIRateLimitError(GenderAPIError):
    """Rate limit exceeded error."""


class GenderAPINotFoundError(GenderAPIError):
    """Resource not found error."""


class GenderAPIValidationError(GenderAPIError):
    """Validation error."""