"""BigQuery API"""

class BigQueryAPIError(Exception):
    """Base exception for BigQuery API errors"""
    pass

class BigQueryAuthError(BigQueryAPIError):
    """Authentication error"""
    pass