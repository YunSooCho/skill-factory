"""
BotStar API Integration
API Reference: https://docs.botstar.com/api/
"""

from .client import BotStarClient
from .exceptions import BotStarAPIError, BotStarAuthError

__all__ = ['BotStarClient', 'BotStarAPIError', 'BotStarAuthError']