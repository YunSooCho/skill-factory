"""
bouncer API Client

This module re-exports the BouncerAPIClient from bouncer_client
"""

from .bouncer_client import BouncerAPIClient

# Re-export for convenience
__all__ = ['BouncerAPIClient']
