"""
Abstract API Client for Yoom Integration

This package provides integration with Abstract API services:
- Exchange Rates API
- Phone Validation API
- Date & Time API
- IP Geolocation API
- Email Validation API
- Holidays API
"""

from .client import AbstractClient

__version__ = "1.0.0"
__all__ = ["AbstractClient"]