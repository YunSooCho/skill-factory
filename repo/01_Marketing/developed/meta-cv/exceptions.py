"""Custom exceptions for Meta CV."""
class MetaCVError(Exception):
    """Base exception for Meta CV errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class MetaCVAuthenticationError(MetaCVError):
    """Authentication error."""


class MetaCVRateLimitError(MetaCVError):
    """Rate limit exceeded error."""


class MetaCVNotFoundError(MetaCVError):
    """Resource not found error."""


class MetaCVValidationError(MetaCVError):
    """Validation error."""