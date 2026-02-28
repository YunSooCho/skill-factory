"""
Custom exceptions for CloudContact AI API integration.
"""


class CloudContactAIError(Exception):
    """Base exception for CloudContact AI API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class CloudContactAIAuthenticationError(CloudContactAIError):
    """Authentication or authorization error."""

    pass


class CloudContactAIRateLimitError(CloudContactAIError):
    """Rate limit exceeded error."""

    pass


class CloudContactAINotFoundError(CloudContactAIError):
    """Resource not found error."""

    pass


class CloudContactAIValidationError(CloudContactAIError):
    """Validation error for request parameters."""

    pass