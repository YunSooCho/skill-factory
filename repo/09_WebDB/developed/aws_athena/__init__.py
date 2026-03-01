"""
AWS Athena Integration

AWS Athena is an interactive query service that makes it easy to analyze
data directly in Amazon S3 using standard SQL.
"""

from .client import AthenaClient

__all__ = ['AthenaClient']
__version__ = '1.0.0'