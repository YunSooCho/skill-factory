"""
Chatwork API Client

Chatwork is a Japanese team chat and collaboration platform.

Authentication: API Token
Documentation: https://go.chatwork.com
"""

from .client import ChatworkClient

__all__ = ["ChatworkClient"]
__version__ = "1.0.0"