"""
Notion API Client Module

Provides async client for Notion API with rate limiting and error handling.
"""

from .notion_client import NotionClient

__all__ = ['NotionClient']
__version__ = '1.0.0'