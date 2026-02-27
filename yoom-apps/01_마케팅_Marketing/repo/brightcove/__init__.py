"""
Brightcove API Integration
API Reference: https://apis.support.brightcove.com/
"""

from .client import BrightcoveClient
from .exceptions import BrightcoveAPIError, BrightcoveAuthError

__all__ = ['BrightcoveClient', 'BrightcoveAPIError', 'BrightcoveAuthError']