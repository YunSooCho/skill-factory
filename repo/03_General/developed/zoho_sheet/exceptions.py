"""
 Zoho Sheet API Exceptions
"""


class ZohoSheetError(Exception):
    """Base exception for Zoho Sheet API errors"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (HTTP {self.status_code})"
        return self.message


class RateLimitError(ZohoSheetError):
    """Raised when rate limit is exceeded"""

    def __init__(
        self, message: str = "Rate limit exceeded", retry_after: int = None, response: dict = None
    ):
        self.retry_after = retry_after
        super().__init__(message, status_code=429, response=response)

    def __str__(self):
        if self.retry_after:
            return f"{self.message} - Retry after {self.retry_after} seconds"
        return self.message


class AuthenticationError(ZohoSheetError):
    """Raised for authentication/authorization errors"""

    def __init__(self, message: str = "Authentication failed", response: dict = None):
        super().__init__(message, status_code=401, response=response)


class ResourceNotFoundError(ZohoSheetError):
    """Raised when a resource is not found"""

    def __init__(self, message: str = "Resource not found", response: dict = None):
        super().__init__(message, status_code=404, response=response)


class ValidationError(ZohoSheetError):
    """Raised for validation errors"""

    def __init__(self, message: str = "Validation failed", response: dict = None):
        super().__init__(message, status_code=400, response=response)