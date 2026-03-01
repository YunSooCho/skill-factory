"""
brevo API Client

This module re-exports the BrevoAPIClient from brevo_client
"""

from .brevo_client import BrevoAPIClient

# Re-export for convenience
__all__ = ['BrevoAPIClient']
