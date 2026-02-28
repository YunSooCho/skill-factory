"""
Custom exceptions for getresponse-api API integration.
"""


class GetresponseApiError(Exception):
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


class GetresponseApiAuthenticationError(GetresponseApiError):
    """Authentication or authorization error."""
    pass


class GetresponseApiRateLimitError(GetresponseApiError):
    """Rate limit exceeded error."""
    pass


class GetresponseApiNotFoundError(GetresponseApiError):
    """Resource not found error."""
    pass


class GetresponseApiValidationError(GetresponseApiError):
    """Validation error for request parameters."""
    pass
