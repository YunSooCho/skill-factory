"""
Custom exceptions for leady API integration.
"""


class LeadyError(Exception):
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


class LeadyAuthenticationError(LeadyError):
    """Authentication or authorization error."""
    pass


class LeadyRateLimitError(LeadyError):
    """Rate limit exceeded error."""
    pass


class LeadyNotFoundError(LeadyError):
    """Resource not found error."""
    pass


class LeadyValidationError(LeadyError):
    """Validation error for request parameters."""
    pass
