"""
Google BigQuery Integration

Google BigQuery is a fully-managed, serverless data warehouse for
massive-scale analytics with SQL queries and machine learning.
"""

from .client import BigQueryClient

__all__ = ['BigQueryClient']
__version__ = '1.0.0'