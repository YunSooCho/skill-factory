"""
Custom exceptions for mailbluster API integration.
"""


class MailblusterError(Exception):
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


class MailblusterAuthenticationError(MailblusterError):
    """Authentication or authorization error."""
    pass


class MailblusterRateLimitError(MailblusterError):
    """Rate limit exceeded error."""
    pass


class MailblusterNotFoundError(MailblusterError):
    """Resource not found error."""
    pass


class MailblusterValidationError(MailblusterError):
    """Validation error for request parameters."""
    pass
