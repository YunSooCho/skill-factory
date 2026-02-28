"""
Fauna API Client

This module provides a Python client for interacting with Fauna.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class FaunaClient:
    """
    Client for Fauna Database API.

    Fauna provides:
    - Distributed ACID transactions
    - Native GraphQL API
    - Serverless auto-scaling
    - Strong consistency
    - Built-in search
    """

    def __init__(
        self,
        secret: str,
        endpoint: str = "https://db.fauna.com",
        domain: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the Fauna client."""
        self.secret = secret
        self.endpoint = endpoint.split('://', 1)[1].split('/')[0]
        if domain:
            self.endpoint = f"{domain}.{self.endpoint}"
        self.base_url = f"https://{self.endpoint}"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {secret}',
            'Content-Type': 'application/json'
        })

    def _query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Fauna Query."""
        response = self.session.post(
            f"{self.base_url}",
            json=query,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def _paginated_query(
        self,
        query: Dict[str, Any],
        fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute query with pagination."""
        results = []
        current_query = query

        while True:
            response = self._query(current_query)
            data = response.get('data', [])
            results.extend(data)

            if not fetch_all or not response.get('after'):
                break

            after_token = response['after']
            original_expr = query.get('query', {})
            current_query = {
                'query': {
                    'map': {
                        'lambda': 'x',
                        'expr': 'x'
                    },
                    'collection': original_expr
                },
                'after': after_token
            }

        return results

    def ping(self) -> Dict[str, Any]:
        """Ping the Fauna server."""
        return self._query({'query': {'ping': None}})

    def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a document in a collection."""
        query = {
            'query': {
                'create': {
                    'collection': collection,
                    'data': data
                }
            }
        }
        return self._query(query)

    def create_by_id(self, collection: str, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a document with specific ID."""
        query = {
            'query': {
                'create': {
                    'id': id,
                    'collection': collection,
                    'data': data
                }
            }
        }
        return self._query(query)

    def get(self, ref: str) -> Optional[Dict[str, Any]]:
        """Get a document by reference."""
        try:
            query = {'query': {'get': {'ref': ref}}}
            return self._query(query)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_by_id(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a document by collection name and ID."""
        try:
            query = {
                'query': {
                    'get': {
                        'id': id,
                        'collection': collection
                    }
                }
            }
            return self._query(query)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def update(self, ref: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a document."""
        query = {
            'query': {
                'update': {
                    'ref': ref,
                    'data': data
                }
            }
        }
        return self._query(query)

    def replace(self, ref: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Replace a document entirely."""
        query = {
            'query': {
                'replace': {
                    'ref': ref,
                    'data': data
                }
            }
        }
        return self._query(query)

    def delete(self, ref: str) -> Dict[str, Any]:
        """Delete a document."""
        query = {'query': {'delete': {'ref': ref}}}
        return self._query(query)

    def paginate(
        self,
        collection: str,
        size: int = 100,
        cursor: Optional[str] = None,
        fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """Paginate through a collection."""
        query = {
            'query': {
                'paginate': {
                    'collection': collection,
                    'size': size
                }
            }
        }
        if cursor:
            query['cursor'] = cursor
        return self._paginated_query(query, fetch_all=fetch_all)

    def map(self, collection: str, lambda_expr: str) -> List[Dict[str, Any]]:
        """Map a function over collection documents."""
        query = {
            'query': {
                'map': {
                    'lambda': lambda_expr,
                    'expr': '?'  # TODO: Proper lambda expression
                },
                'collection': collection
            }
        }
        return self._query(query)

    def filter(self, collection: str, condition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter documents in a collection."""
        query = {
            'query': {
                'map': {
                    'lambda': 'x',
                    'expr': 'x'
                },
                'collection': collection
            }
        }
        results = self._query(query)
        return [r for r in results.get('data', [])]

    def index_create(
        self,
        name: str,
        source: str,
        terms: Optional[List[str]] = None,
        values: Optional[List[str]] = None,
        unique: bool = False,
        serialized: bool = True
    ) -> Dict[str, Any]:
        """Create an index."""
        index_def = {
            'name': name,
            'source': {'collection': source},
            'unique': unique,
            'serialized': serialized
        }
        if terms:
            index_def['terms'] = [{'field': term} for term in terms]
        if values:
            index_def['values'] = [{'field': value} for value in values]

        query = {'query': {'create_index': index_def}}
        return self._query(query)

    def index_get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get index details."""
        try:
            return self._query({'query': {'get': {'index': name}}})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def delete_index(self, name: str) -> Dict[str, Any]:
        """Delete an index."""
        query = {'query': {'delete': {'index': name}}}
        return self._query(query)

    def search_index(
        self,
        index_name: str,
        terms: List[Any],
        size: int = 10,
        after: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search using an index."""
        query = {
            'query': {
                'match': {
                    'index': index_name,
                    'terms': terms
                }
            },
            'size': size
        }
        if after:
            query['after'] = after
        result = self._query(query)
        return result.get('data', [])

    def create_collection(self, name: str) -> Dict[str, Any]:
        """Create a collection."""
        query = {
            'query': {
                'create_collection': {
                    'name': name
                }
            }
        }
        return self._query(query)

    def get_collection(self, name: str) -> Optional[Dict[str, Any]]:
        """Get collection details."""
        try:
            return self._query({'query': {'get': {'collection': name}}})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def delete_collection(self, name: str) -> Dict[str, Any]:
        """Delete a collection."""
        query = {'query': {'delete': {'collection': name}}}
        return self._query(query)

    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections."""
        query = {
            'query': {
                'map': {
                    'lambda': 'x',
                    'expr': 'x'
                },
                'paginate': {'collections': None}
            }
        }
        result = self._query(query)
        return result.get('data', [])

    def create_database(self, name: str) -> Dict[str, Any]:
        """Create a database."""
        query = {
            'query': {
                'create_database': {
                    'name': name
                }
            }
        }
        return self._query(query)

    def get_database(self, name: str) -> Optional[Dict[str, Any]]:
        """Get database details."""
        try:
            return self._query({'query': {'get': {'database': name}}})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def delete_database(self, name: str) -> Dict[str, Any]:
        """Delete a database."""
        query = {'query': {'delete': {'database': name}}}
        return self._query(query)

    def create_key(
        self,
        database: Optional[str] = None,
        role: str = "server",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an API key."""
        key_def = {'role': role}
        if database:
            key_def['database'] = database
        if data:
            key_def['data'] = data

        query = {'query': {'create_key': key_def}}
        return self._query(query)

    def delete_key(self, key_ref: str) -> Dict[str, Any]:
        """Delete an API key."""
        query = {'query': {'delete': {'ref': key_ref}}}
        return self._query(query)

    def let(self, bindings: Dict[str, Any], in_expr: Any) -> Dict[str, Any]:
        """Create let expression."""
        query = {
            'query': {
                'let': {
                    'bindings': [
                        {'var': k, 'expression': v}
                        for k, v in bindings.items()
                    ],
                    'in': in_expr
                }
            }
        }
        return self._query(query)

    def if_else(self, test_expr: Any, then_expr: Any, else_expr: Any) -> Dict[str, Any]:
        """Create if-else expression."""
        query = {
            'query': {
                'if': test_expr,
                'then': then_expr,
                'else': else_expr
            }
        }
        return self._query(query)

    def exists(self, ref: str) -> bool:
        """Check if a document exists."""
        try:
            self.get(ref)
            return True
        except requests.exceptions.HTTPError:
            return False

    def count(self, collection: str) -> int:
        """Count documents in a collection."""
        # Create a count index first
        query = {
            'query': {
                'count': {
                    'collection': collection
                }
            }
        }
        result = self._query(query)
        return result.get('resource', 0)

    def create_function(
        self,
        name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a UDF (User Defined Function)."""
        query = {
            'query': {
                'create_function': {
                    'name': name,
                    **data
                }
            }
        }
        return self._query(query)

    def call_function(self, name: str, arguments: List[Any]) -> Dict[str, Any]:
        """Call a UDF."""
        query = {
            'query': {
                'call': {
                    'name': name,
                    'arguments': arguments
                }
            }
        }
        return self._query(query)