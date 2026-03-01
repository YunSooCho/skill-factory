"""
aweber API Client

This module re-exports the AweberAPIClient from aweber_client
"""

from .aweber_client import AweberAPIClient

# Re-export for convenience
__all__ = ['AweberAPIClient']
