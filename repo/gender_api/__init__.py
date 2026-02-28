"""Gender API Client Library."""
from .actions import GenderAPIActions
from .exceptions import (
    GenderAPIError,
    GenderAPIAuthenticationError,
    GenderAPIRateLimitError,
    GenderAPINotFoundError,
    GenderAPIValidationError,
)
from .models import GenderPrediction, AccountStats, CountryOrigin

__all__ = [
    "GenderAPIActions",
    "GenderAPIError",
    "GenderAPIAuthenticationError",
    "GenderAPIRateLimitError",
    "GenderAPINotFoundError",
    "GenderAPIValidationError",
    "GenderPrediction",
    "AccountStats",
    "CountryOrigin",
]

__version__ = "1.0.0"