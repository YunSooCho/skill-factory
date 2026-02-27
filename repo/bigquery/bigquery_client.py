"""
BigQuery API Client

Supports:
- Search Records
- Execute Query
- Create Record
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class QueryResult:
    """BigQuery query result representation"""
    rows: List[Dict[str, Any]]
    columns: List[str]
    total_rows: int
    job_id: Optional[str] = None


class BigQueryClient:
    """
    BigQuery API client for data warehouse operations.

    Authentication: OAuth 2.0 (Access Token)
    Base URL: https://bigquery.googleapis.com/bigquery/v2
    """

    BASE_URL = "https://bigquery.googleapis.com/bigquery/v2"

    def __init__(self, access_token: str, project_id: str):
        """
        Initialize BigQuery client.

        Args:
            access_token: OAuth 2.0 access token
            project_id: Google Cloud project ID
        """
        self.access_token = access_token
        self.project_id = project_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid access token")
            elif response.status_code == 403:
                raise Exception(
Permission denied")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Query Operations ====================

    def execute_query(
        self,
        query: str,
        use_legacy_sql: bool = False,
        timeout_ms: int = 30000,
        dry_run: bool = False
    ) -> QueryResult:
        """
        Execute a SQL query.

        Args:
            query: SQL query string
            use_legacy_sql: Use legacy SQL instead of standard SQL
            timeout_ms: Query timeout in milliseconds
            dry_run: Validate query without executing

        Returns:
            QueryResult with rows and metadata
        """
        if not query:
            raise ValueError("Query string is required")

        payload = {
            "query": query,
            "useLegacySql": use_legacy_sql,
            "timeoutMs": timeout_ms,
            "dryRun": dry_run
        }

        result = self._request(
            "POST",
            f"/projects/{self.project_id}/queries",
            json=payload
        )

        # Parse results
        rows = []
        columns = []

        if "rows" in result and "schema" in result:
            # Extract column names
            columns = [field.get("name", "") for field in result.get("schema", {}).get("fields", [])]

            # Convert rows to dictionaries
            for row_data in result.get("rows", []):
                row = {}
                for i, cell in enumerate(row_data.get("f", [])):
                    if i < len(columns):
                        # Get value from cell (may have v object)
                        value = cell.get("v")
                        row[columns[i]] = value
                rows.append(row)

        return QueryResult(
            rows=rows,
            columns=columns,
            total_rows=len(rows),
            job_id=result.get("jobReference", {}).get("jobId")
        )

    def search_records(
        self,
        table: str,
        dataset: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        selected_fields: Optional[List[str]] = None
    ) -> QueryResult:
        """
        Search for records in a table.

        Args:
            table: Table name
            dataset: Dataset ID
            filters: Dictionary of field:value pairs for filtering
            limit: Maximum number of records to return
            selected_fields: List of fields to select

        Returns:
            QueryResult with matching records
        """
        if not table:
            raise ValueError("Table name is required")
        if not dataset:
            raise ValueError("Dataset ID is required")

        # Build SQL query
        if selected_fields:
            fields_str = ", ".join(selected_fields)
        else:
            fields_str = "*"

        query = f"SELECT {fields_str} FROM `{self.project_id}.{dataset}.{table}`"

        # Add filters
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, str):
                    conditions.append(f"{key} = '{value}'")
                elif isinstance(value, (int, float, bool)):
                    conditions.append(f"{key} = {value}")
                elif value is None:
                    conditions.append(f"{key} IS NULL")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        # Add limit
        query += f" LIMIT {limit}"

        return self.execute_query(query)

    # ==================== Record Operations ====================

    def create_record(
        self,
        table: str,
        dataset: str,
        record: Dict[str, Any],
        insert_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Insert a new record into a table.

        Args:
            table: Table name
            dataset: Dataset ID
            record: Dictionary of field:value pairs
            insert_id: Optional insertion ID for deduplication

        Returns:
            Insert response with job info
        """
        if not table:
            raise ValueError("Table name is required")
        if not dataset:
            raise ValueError("Dataset ID is required")
        if not record:
            raise ValueError("Record data is required")

        payload = {
            "rows": [
                {
                    "json": record
                }
            ]
        }

        if insert_id:
            payload["rows"][0]["insertId"] = insert_id

        result = self._request(
            "POST",
            f"/projects/{self.project_id}/datasets/{dataset}/tables/{table}/insertAll",
            json=payload
        )

        return {
            "status": "success" if result.get("kind") == "bigquery#tableDataInsertAllResponse" else "error",
            "insert_errors": result.get("insertErrors", []),
            "job_status": result.get("status")
        }

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    access_token = "your_oauth_access_token"
    project_id = "your_project_id"

    client = BigQueryClient(access_token=access_token, project_id=project_id)

    try:
        # Execute custom query
        query_result = client.execute_query(
            "SELECT COUNT(*) as total FROM `your_project.your_dataset.your_table`"
        )
        print(f"Query result: {query_result.rows}")
        print(f"Job ID: {query_result.job_id}")

        # Search records
        search_result = client.search_records(
            table="your_table",
            dataset="your_dataset",
            filters={"status": "active"},
            limit=50
        )
        print(f"Found {len(search_result.rows)} records")

        # Create record
        insert_result = client.create_record(
            table="your_table",
            dataset="your_dataset",
            record={
                "name": "John Doe",
                "email": "john@example.com",
                "status": "active"
            },
            insert_id="unique_id_123"
        )
        print(f"Insert status: {insert_result['status']}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()