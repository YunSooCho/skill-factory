"""
Custom exceptions for mailmodo API integration.
"""


class MailmodoError(Exception):
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


class MailmodoAuthenticationError(MailmodoError):
    """Authentication or authorization error."""
    pass


class MailmodoRateLimitError(MailmodoError):
    """Rate limit exceeded error."""
    pass


class MailmodoNotFoundError(MailmodoError):
    """Resource not found error."""
    pass


class MailmodoValidationError(MailmodoError):
    """Validation error for request parameters."""
    pass
