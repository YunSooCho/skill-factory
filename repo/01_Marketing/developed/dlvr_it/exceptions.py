"""Custom exceptions for DLVR.it."""
class DlvrItError(Exception):
    """Base exception for DLVR.it errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class DlvrItAuthenticationError(DlvrItError):
    """Authentication error."""


class DlvrItRateLimitError(DlvrItError):
    """Rate limit exceeded error."""


class DlvrItNotFoundError(DlvrItError):
    """Resource not found error."""


class DlvrItValidationError(DlvrItError):
    """Validation error."""