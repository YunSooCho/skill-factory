"""
YouTube Data API Exceptions.
"""

class YoutubeDataError(Exception):
    """Base exception for YouTube Data API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.__class__.__name__} (status={self.status_code}): {self.message}"
        return f"{self.__class__.__name__}: {self.message}"


class YoutubeDataAuthenticationError(YoutubeDataError):
    """Raised when authentication fails."""
    pass


class YoutubeDataRateLimitError(YoutubeDataError):
    """Raised when rate limit is exceeded."""
    pass


class YoutubeDataNotFoundError(YoutubeDataError):
    """Raised when a requested resource is not found."""
    pass


class YoutubeDataValidationError(YoutubeDataError):
    """Raised when validation fails."""
    pass


class YoutubeDataConnectionError(YoutubeDataError):
    """Raised when connection fails."""
    pass