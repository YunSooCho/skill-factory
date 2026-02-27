"""
BigQuery API Client
"""

from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from typing import Optional, Dict, Any, List
import json


class BigQueryAPIError(Exception):
    """Base exception for BigQuery API errors"""
    pass


class BigQueryAuthError(BigQueryAPIError):
    """Authentication error"""
    pass


class BigQueryClient:
    """BigQuery API Client for data operations"""

    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
        credentials: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize BigQuery client

        Args:
            project_id: Google Cloud project ID
            credentials_path: Path to service account JSON file
            credentials: Service account credentials as dict
        """
        if credentials_path:
            self.client = bigquery.Client.from_service_account_json(credentials_path)
        elif credentials:
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_info(credentials)
            self.client = bigquery.Client(credentials=creds, project=project_id)
        else:
            self.client = bigquery.Client(project=project_id)

    # ===== Query Operations =====

    def execute_query(
        self,
        query: str,
        query_parameters: Optional[List[bigquery.ScalarQueryParameter]] = None,
        use_legacy_sql: bool = False,
        use_query_cache: bool = True,
        timeout: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query

        Args:
            query: SQL query string
            query_parameters: List of query parameters
            use_legacy_sql: Whether to use legacy SQL
            use_query_cache: Whether to use query cache
            timeout: Query timeout in seconds

        Returns:
            List of result rows as dictionaries
        """
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = use_legacy_sql
        job_config.use_query_cache = use_query_cache

        if query_parameters:
            job_config.query_parameters = query_parameters

        try:
            query_job = self.client.query(
                query,
                job_config=job_config,
                timeout=timeout,
            )
            results = query_job.result()

            return [dict(row) for row in results]
        except GoogleCloudError as e:
            self._handle_error(e)
        except Exception as e:
            raise BigQueryAPIError(f"Query failed: {str(e)}")

    def query_with_job(
        self,
        query: str,
        destination_table: Optional[str] = None,
        write_disposition: Optional[str] = None,
        query_parameters: Optional[List[bigquery.ScalarQueryParameter]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a query and get job information

        Args:
            query: SQL query string
            destination_table: Destination table in format "project.dataset.table"
            write_disposition: Write disposition (WRITE_APPEND, WRITE_TRUNCATE, WRITE_EMPTY)
            query_parameters: List of query parameters

        Returns:
            Job information dictionary
        """
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = False

        if destination_table:
            job_config.destination = self.client.table(destination_table)
        if write_disposition:
            job_config.write_disposition = write_disposition
        if query_parameters:
            job_config.query_parameters = query_parameters

        try:
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()  # Wait for completion

            return {
                "job_id": query_job.job_id,
                "state": query_job.state,
                "total_bytes_billed": query_job.total_bytes_billed,
                "total_bytes_processed": query_job.total_bytes_processed,
            }
        except GoogleCloudError as e:
            self._handle_error(e)
        except Exception as e:
            raise BigQueryAPIError(f"Query failed: {str(e)}")

    # ===== Row Operations =====

    def create_row(
        self,
        dataset_id: str,
        table_id: str,
        row_data: Dict[str, Any],
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Insert a row into a table

        Args:
            dataset_id: Dataset ID
            table_id: Table ID
            row_data: Row data as dictionary
            project_id: Project ID (defaults to client project)

        Returns:
            Inserted row data
        """
        table_ref = self.client.dataset(dataset_id, project=project_id).table(table_id)
        table = self.client.get_table(table_ref)

        try:
            errors = self.client.insert_rows_json(table, [row_data])
            if errors:
                raise BigQueryAPIError(f"Insert failed: {errors}")
            return row_data
        except GoogleCloudError as e:
            self._handle_error(e)
        except Exception as e:
            raise BigQueryAPIError(f"Insert failed: {str(e)}")

    def create_rows(
        self,
        dataset_id: str,
        table_id: str,
        rows_data: List[Dict[str, Any]],
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Insert multiple rows into a table

        Args:
            dataset_id: Dataset ID
            table_id: Table ID
            rows_data: List of row data dictionaries
            project_id: Project ID

        Returns:
            Insert result information
        """
        table_ref = self.client.dataset(dataset_id, project=project_id).table(table_id)
        table = self.client.get_table(table_ref)

        try:
            errors = self.client.insert_rows_json(table, rows_data)
            if errors:
                raise BigQueryAPIError(f"Insert failed: {errors}")
            return {"rows_inserted": len(rows_data)}
        except GoogleCloudError as e:
            self._handle_error(e)
        except Exception as e:
            raise BigQueryAPIError(f"Insert failed: {str(e)}")

    def search_rows(
        self,
        dataset_id: str,
        table_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        project_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search rows in a table

        Args:
            dataset_id: Dataset ID
            table_id: Table ID
            filters: Filter conditions as key-value pairs
            limit: Maximum number of rows
            project_id: Project ID

        Returns:
            List of rows
        """
        table_ref = self.client.dataset(dataset_id, project=project_id).table(table_id)
        query = f"SELECT * FROM `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`"

        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, str):
                    conditions.append(f"{key} = '{value}'")
                elif value is None:
                    conditions.append(f"{key} IS NULL")
                else:
                    conditions.append(f"{key} = {value}")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        if limit:
            query += f" LIMIT {limit}"

        try:
            query_job = self.client.query(query)
            results = query_job.result()
            return [dict(row) for row in results]
        except GoogleCloudError as e:
            self._handle_error(e)
        except Exception as e:
            raise BigQueryAPIError(f"Search failed: {str(e)}")

    # ===== Table Operations =====

    def get_table(
        self,
        dataset_id: str,
        table_id: str,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get table information

        Args:
            dataset_id: Dataset ID
            table_id: Table ID
            project_id: Project ID

        Returns:
            Table information
        """
        table_ref = self.client.dataset(dataset_id, project=project_id).table(table_id)
        table = self.client.get_table(table_ref)

        return {
            "table_id": table.table_id,
            "dataset_id": table.dataset_id,
            "project": table.project,
            "full_table_id": table.full_table_id,
            "schema": [{"name": field.name, "type": field.field_type} for field in table.schema],
            "num_rows": table.num_rows,
            "num_bytes": table.num_bytes,
            "created": table.created.isoformat() if table.created else None,
            "modified": table.modified.isoformat() if table.modified else None,
        }

    def _handle_error(self, error: GoogleCloudError):
        """Handle API errors"""
        error_code = getattr(error, 'code', None)
        error_message = str(error)

        if error_code == 401 or 'Authentication' in error_message:
            raise BigQueryAuthError(f"Authentication error: {error_message}")
        elif error_code == 403 or 'Permission' in error_message:
            raise BigQueryAPIError(f"Permission denied: {error_message}")
        elif error_code == 404 or 'Not found' in error_message:
            raise BigQueryAPIError(f"Resource not found: {error_message}")
        elif error_code == 429 or 'Quota' in error_message:
            raise BigQueryAPIError(f"Quota exceeded: {error_message}")
        else:
            raise BigQueryAPIError(f"BigQuery error: {error_message}")