"""
anymail-finder API Client

This module re-exports the AnymailFinderAPIClient from anymail_finder_client
"""

from .anymail_finder_client import AnymailFinderAPIClient

# Re-export for convenience
__all__ = ['AnymailFinderAPIClient']
