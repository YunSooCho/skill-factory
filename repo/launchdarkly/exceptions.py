"""LaunchDarkly API Exceptions"""


class LaunchDarklyError(Exception):
    """Base exception for LaunchDarkly API errors"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(LaunchDarklyError):
    """Authentication or authorization failed"""

    pass


class RateLimitError(LaunchDarklyError):
    """Rate limit exceeded"""

    def __init__(self, message: str, retry_after: int = None, response: dict = None):
        self.retry_after = retry_after
        super().__init__(message, response=response)


class ResourceNotFoundError(LaunchDarklyError):
    """Resource not found"""

    pass


class ValidationError(LaunchDarklyError):
    """Validation error"""

    pass


class ConflictError(LaunchDarklyError):
    """Resource conflict"""

    pass