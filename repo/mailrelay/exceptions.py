"""
Custom exceptions for mailrelay API integration.
"""


class MailrelayError(Exception):
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


class MailrelayAuthenticationError(MailrelayError):
    """Authentication or authorization error."""
    pass


class MailrelayRateLimitError(MailrelayError):
    """Rate limit exceeded error."""
    pass


class MailrelayNotFoundError(MailrelayError):
    """Resource not found error."""
    pass


class MailrelayValidationError(MailrelayError):
    """Validation error for request parameters."""
    pass
