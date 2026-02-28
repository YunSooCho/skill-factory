"""
beehiiv API Client

This module re-exports the BeehiivAPIClient from beehiiv_client
"""

from .beehiiv_client import BeehiivAPIClient

# Re-export for convenience
__all__ = ['BeehiivAPIClient']
