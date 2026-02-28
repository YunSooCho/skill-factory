"""
Hasura GraphQL API Client

This module provides a Python client for interacting with Hasura.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class HasuraClient:
    """
    Client for Hasura GraphQL API.

    Hasura provides:
    - Instant GraphQL over databases
    - Real-time subscriptions
    - Authorization & permissions
    - API federation
    - Event triggers
    """

    def __init__(
        self,
        graphql_url: str,
        admin_secret: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the Hasura client."""
        self.graphql_url = graphql_url.rstrip('/')
        self.admin_secret = admin_secret
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        if admin_secret:
            self.session.headers['X-Hasura-Admin-Secret'] = admin_secret

    def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query."""
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
        if operation_name:
            payload['operationName'] = operation_name

        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.post(
            self.graphql_url,
            json=payload,
            headers=request_headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()

        if 'errors' in result:
            raise Exception(f"GraphQL Error: {result['errors']}")

        return result.get('data', {})

    def run_sql(self, sql: str, source: str = "default") -> Dict[str, Any]:
        """Run raw SQL query."""
        query = f"""{{
            run_sql(args: {{sql: "{self._escape_sql(sql)}", source: "{source}"}}) {{
                result
                affected_rows
            }}
        }}"""
        return self.execute(query)

    def _escape_sql(self, sql: str) -> str:
        """Escape SQL string for GraphQL."""
        return sql.replace('"', '\\"').replace('\n', '\\n')

    def get_tables(self, source: str = "default") -> List[Dict[str, Any]]:
        """Get all tables."""
        query = f"""{{
            tables: get_tables(args: {{source: "{source}"}}) {{
                name
                schema
            }}
        }}"""
        result = self.execute(query)
        return result.get('tables', [])

    def get_columns(
        self,
        table: str,
        source: str = "default"
    ) -> List[Dict[str, Any]]:
        """Get table columns."""
        query = f"""{{
            columns: get_columns(args: {{table: {{name: "{table}"}}}}) {{
                name
                type
                isNullable
                isPrimaryKey
            }}
        }}"""
        result = self.execute(query)
        return result.get('columns', [])

    def track_table(
        self,
        table: str,
        schema: str = "public",
        source: str = "default"
    ) -> Dict[str, Any]:
        """Track a table in Hasura."""
        query = f"""mutation {{
            track_table(
                configuration: {{table: {{name: "{table}", schema: "{schema}"}}, source: "{source}"}}
            ) {{
                success
                message
            }}
        }}"""
        return self.execute(query)

    def untrack_table(
        self,
        table: str,
        schema: str = "public",
        source: str = "default"
    ) -> Dict[str, Any]:
        """Untrack a table from Hasura."""
        query = f"""mutation {{
            untrack_table(
                configuration: {{table: {{name: "{table}", schema: "{schema}"}}, source: "{source}"}}
            ) {{
                success
                message
            }}
        }}"""
        return self.execute(query)

    def create_relationship(
        self,
        table: str,
        column: str,
        foreign_key: str,
        name: str,
        remote_table: str,
        remote_column: str
    ) -> Dict[str, Any]:
        """Create a relationship."""
        query = f"""mutation {{
            create_object_relationship(
                table: {{name: "{table}"}},
                using: {{foreign_key_constraint_on: "{column}"}},
                name: "{name}"
            ) {{
                relationship {{
                    name
                }}
            }}
        }}"""
        return self.execute(query)

    def create_remote_schema(
        self,
        name: str,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Add a remote schema."""
        query = f"""mutation {{
            add_remote_schema(name: "{name}", definition: {{url: "{url}", headers: {json.dumps(headers or {})}}}) {{
                name
            }}
        }}"""
        return self.execute(query)

    def create_api_source(
        self,
        name: str,
        url: str
    ) -> Dict[str, Any]:
        """Create an API source."""
        query = f"""mutation {{
            create_api_source(name: "{name}", definition: {{url: "{url}"}}) {{
                name
            }}
        }}"""
        return self.execute(query)

    def create_allowlist(
        self,
        list: List[str]
    ) -> Dict[str, Any]:
        """Add query collection to allowlist."""
        query = f"""mutation {{
            add_query_collection_to_allowlist(query_collection: {{name: "allowed", definition: {{queries: [{", ".join([f'{{name: "{q}"}}' for q in list])}]}}}}) {{
                success
            }}
        }}"""
        return self.execute(query)

    def export_metadata(self) -> Dict[str, Any]:
        """Export Hasura metadata."""
        query = """{
            export_metadata {
                tables
                remote_schemas
                custom_types
            }
        }"""
        return self.execute(query)

    def replace_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Replace Hasura metadata."""
        query = f"""mutation {{
            replace_metadata(metadata: {json.dumps(metadata)}) {{
                is consistency_happening
            }}
        }}"""
        return self.execute(query)

    def get_api_versions(self) -> Dict[str, Any]:
        """Get Hasura version info."""
        query = """{
            version
        }"""
        return self.execute(query)

    def get_tracked_tables(self) -> List[Dict[str, Any]]:
        """Get all tracked tables."""
        query = """{
            tables {
                name
                schema
                type
            }
        }"""
        result = self.execute(query)
        return result.get('tables', [])

    def subscribe(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        callback: Optional[callable] = None
    ):
        """Initialize a WebSocket subscription (requires websocket client)."""
        raise NotImplementedError("WebSocket subscriptions require websockets library. Install: pip install websockets")

    def batch_execute(
        self,
        queries: List[str],
        variable_list: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """Execute multiple queries in batch."""
        results = []
        for i, query_str in enumerate(queries):
            variables = variable_list[i] if variable_list else None
            results.append(self.execute(query_str, variables))
        return results

    def get_query_collections(self) -> List[Dict[str, Any]]:
        """Get all query collections."""
        query = """{
            query_collections {
                name
                queries
            }
        }"""
        result = self.execute(query)
        return result.get('query_collections', [])

    def create_query_collection(
        self,
        name: str,
        queries: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Create a query collection."""
        query = f"""mutation {{
            create_query_collection(name: "{name}", definition: {{queries: {json.dumps(queries)}}}) {{
                name
            }}
        }}"""
        return self.execute(query)

    def drop_query_collection(self, name: str) -> Dict[str, Any]:
        """Drop a query collection."""
        query = f"""mutation {{
            drop_query_collection(name: "{name}") {{
                success
            }}
        }}"""
        return self.execute(query)