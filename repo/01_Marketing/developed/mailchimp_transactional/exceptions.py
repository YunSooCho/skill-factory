"""
Custom exceptions for mailchimp_transactional API integration.
"""


class MailchimpTransactionalError(Exception):
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


class MailchimpTransactionalAuthenticationError(MailchimpTransactionalError):
    """Authentication or authorization error."""
    pass


class MailchimpTransactionalRateLimitError(MailchimpTransactionalError):
    """Rate limit exceeded error."""
    pass


class MailchimpTransactionalNotFoundError(MailchimpTransactionalError):
    """Resource not found error."""
    pass


class MailchimpTransactionalValidationError(MailchimpTransactionalError):
    """Validation error for request parameters."""
    pass
