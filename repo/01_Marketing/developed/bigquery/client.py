"""
bigquery API Client

This module re-exports the BigqueryAPIClient from bigquery_client
"""

from .bigquery_client import BigqueryAPIClient

# Re-export for convenience
__all__ = ['BigqueryAPIClient']
