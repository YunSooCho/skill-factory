"""Custom exceptions for Cuénote SMS."""
class CuenoteSMSError(Exception):
    """Base exception for Cuénote SMS errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class CuenoteSMSAuthenticationError(CuenoteSMSError):
    """Authentication error."""


class CuenoteSMSRateLimitError(CuenoteSMSError):
    """Rate limit exceeded error."""


class CuenoteSMSNotFoundError(CuenoteSMSError):
    """Resource not found error."""


class CuenoteSMSValidationError(CuenoteSMSError):
    """Validation error."""