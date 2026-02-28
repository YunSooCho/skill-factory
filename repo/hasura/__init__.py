"""
Hasura GraphQL Integration

Hasura is a GraphQL server that provides instant real-time GraphQL APIs
over existing databases with powerful authorization engine.
"""

from .client import HasuraClient

__all__ = ['HasuraClient']
__version__ = '1.0.0'