"""
Airtable Pocket Integration

Pocket is Airtable's mobile app companion for quick data capture
and offline access to your bases.
"""

from .client import PocketClient

__all__ = ['PocketClient']
__version__ = '1.0.0'