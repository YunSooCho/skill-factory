"""
Custom exceptions for lob API integration.
"""


class LobError(Exception):
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


class LobAuthenticationError(LobError):
    """Authentication or authorization error."""
    pass


class LobRateLimitError(LobError):
    """Rate limit exceeded error."""
    pass


class LobNotFoundError(LobError):
    """Resource not found error."""
    pass


class LobValidationError(LobError):
    """Validation error for request parameters."""
    pass
