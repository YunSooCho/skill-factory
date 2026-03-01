"""
Hugging Face API Client Module

Provides async client for Hugging Face API with rate limiting and error handling.
"""

from .huggingface_client import HuggingFaceClient

__all__ = ['HuggingFaceClient']
__version__ = '1.0.0'