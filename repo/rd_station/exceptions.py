"""
Rd Station API Exceptions.
"""

class RdStationError(Exception):
    """Base exception for Rd Station API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.__class__.__name__} (status={self.status_code}): {self.message}"
        return f"{self.__class__.__name__}: {self.message}"


class RdStationAuthenticationError(RdStationError):
    """Raised when authentication fails."""
    pass


class RdStationRateLimitError(RdStationError):
    """Raised when rate limit is exceeded."""
    pass


class RdStationNotFoundError(RdStationError):
    """Raised when a requested resource is not found."""
    pass


class RdStationValidationError(RdStationError):
    """Raised when validation fails."""
    pass


class RdStudioConnectionError(RdStationError):
    """Raised when connection fails."""
    pass