"""
CloudContact AI API Integration for Yoom Apps

This module provides API actions for CloudContact AI operations.
"""

from .actions import CloudContactAIActions
from .exceptions import (
    CloudContactAIError,
    CloudContactAIAuthenticationError,
    CloudContactAIRateLimitError,
    CloudContactAINotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "CloudContactAIActions",
    "CloudContactAIError",
    "CloudContactAIAuthenticationError",
    "CloudContactAIRateLimitError",
    "CloudContactAINotFoundError",
]