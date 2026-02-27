"""
Pinterest API Client for Yoom Integration
API Version: v5
Documentation: https://developers.pinterest.com/docs/api/
"""

from .client import PinterestClient
from .models import Pin, Board

__all__ = ['PinterestClient', 'Pin', 'Board']
__version__ = '1.0.0'