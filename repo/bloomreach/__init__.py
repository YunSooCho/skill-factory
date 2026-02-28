"""
Bloomreach - Personalization & Content Delivery

API Client for Bloomreach personalization and content delivery platform.
"""

from .client import (
    BloomreachClient,
    Recommendation,
    UserEvent,
    UserProfile,
    SearchResult,
    ContentItem
)

__all__ = [
    "BloomreachClient",
    "Recommendation",
    "UserEvent",
    "UserProfile",
    "SearchResult",
    "ContentItem"
]