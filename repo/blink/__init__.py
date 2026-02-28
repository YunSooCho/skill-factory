"""
Blink - URL Shortening Service

API Client for Blink URL shortening service.
"""

from .client import BlinkClient, BlinkLink, LinkAnalytics

__all__ = ["BlinkClient", "BlinkLink", "LinkAnalytics"]