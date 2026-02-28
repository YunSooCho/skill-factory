"""
adroll API Client

This module re-exports the AdrollAPIClient from adroll_client
"""

from .adroll_client import AdrollAPIClient

# Re-export for convenience
__all__ = ['AdrollAPIClient']
