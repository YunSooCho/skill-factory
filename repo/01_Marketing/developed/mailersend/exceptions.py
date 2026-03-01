"""
Custom exceptions for mailersend API integration.
"""


class MailersendError(Exception):
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


class MailersendAuthenticationError(MailersendError):
    """Authentication or authorization error."""
    pass


class MailersendRateLimitError(MailersendError):
    """Rate limit exceeded error."""
    pass


class MailersendNotFoundError(MailersendError):
    """Resource not found error."""
    pass


class MailersendValidationError(MailersendError):
    """Validation error for request parameters."""
    pass
