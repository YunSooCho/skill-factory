"""
Baserow Database Integration

Baserow is an open-source no-code database and Airtable alternative
with self-hosting options and API access.
"""

from .client import BaserowClient

__all__ = ['BaserowClient']
__version__ = '1.0.0'