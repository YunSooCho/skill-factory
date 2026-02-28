"""Custom exceptions for OneSignal."""
class OneSignalError(Exception):
    """Base exception for OneSignal errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class OneSignalAuthenticationError(OneSignalError):
    """Authentication error."""


class OneSignalRateLimitError(OneSignalError):
    """Rate limit exceeded error."""


class OneSignalNotFoundError(OneSignalError):
    """Resource not found error."""


class OneSignalValidationError(OneSignalError):
    """Validation error."""