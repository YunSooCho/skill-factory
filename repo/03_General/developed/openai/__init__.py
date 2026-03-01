"""
OpenAI API Client Module

Provides async client for OpenAI API with rate limiting and error handling.
"""

from .openai_client import OpenAIClient

__all__ = ['OpenAIClient']
__version__ = '1.0.0'