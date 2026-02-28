"""
clicksend API Client

This module re-exports the ClicksendAPIClient from clicksend_client
"""

from .clicksend_client import ClicksendAPIClient

# Re-export for convenience
__all__ = ['ClicksendAPIClient']
