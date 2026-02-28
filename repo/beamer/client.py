"""
beamer API Client

This module re-exports the BeamerAPIClient from beamer_client
"""

from .beamer_client import BeamerAPIClient

# Re-export for convenience
__all__ = ['BeamerAPIClient']
