"""
brightcove API Client

This module re-exports the BrightcoveAPIClient from brightcove_client
"""

from .brightcove_client import BrightcoveAPIClient

# Re-export for convenience
__all__ = ['BrightcoveAPIClient']
