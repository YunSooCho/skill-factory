"""
Airtable OAuth Integration

Airtable OAuth provides secure OAuth 2.0 authentication for accessing
Airtable bases without sharing API keys directly.
"""

from .client import AirtableOAuthClient

__all__ = ['AirtableOAuthClient']
__version__ = '1.0.0'