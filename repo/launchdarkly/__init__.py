"""
LaunchDarkly API Client

A Python client for interacting with LaunchDarkly's REST API.
"""

from .client import LaunchDarklyClient
from .models import Flag, Segment, User, Environment, Project
from .exceptions import (
    LaunchDarklyError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError,
    ConflictError,
)

__version__ = "1.0.0"
__all__ = [
    "LaunchDarklyClient",
    "Flag",
    "Segment",
    "User",
    "Environment",
    "Project",
    "LaunchDarklyError",
    "AuthenticationError",
    "RateLimitError",
    "ResourceNotFoundError",
    "ValidationError",
    "ConflictError",
]