"""Custom exceptions for BurstSMS."""
class BurstSMSError(Exception):
    """Base exception for BurstSMS errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class BurstSMSAuthenticationError(BurstSMSError):
    """Authentication error."""


class BurstSMSRateLimitError(BurstSMSError):
    """Rate limit exceeded error."""


class BurstSMSNotFoundError(BurstSMSError):
    """Resource not found error."""


class BurstSMSValidationError(BurstSMSError):
    """Validation error."""