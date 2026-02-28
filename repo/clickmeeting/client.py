"""
clickmeeting API Client

This module re-exports the ClickmeetingAPIClient from clickmeeting_client
"""

from .clickmeeting_client import ClickmeetingAPIClient

# Re-export for convenience
__all__ = ['ClickmeetingAPIClient']
