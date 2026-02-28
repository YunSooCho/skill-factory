"""
Fauna Database Integration

Fauna is a distributed database with native GraphQL support,
serverless scaling, and strong consistency guarantees.
"""

from .client import FaunaClient

__all__ = ['FaunaClient']
__version__ = '1.0.0'