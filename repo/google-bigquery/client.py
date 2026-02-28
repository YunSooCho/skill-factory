"""
Google BigQuery API Client

This module provides a Python client for interacting with Google BigQuery.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class BigQueryClient:
    """
    Client for Google BigQuery API.

    BigQuery provides:
    - Serverless data warehouse
    - SQL queries at petabyte scale
    - Machine learning integration
    - Real-time analytics
    """

    def __init__(
        self,
        project_id: str,
        credentials: Dict[str, Any],
        base_url: str = "https://bigquery.googleapis.com/bigquery/v2",
        timeout: int = 30
    ):
        """Initialize the BigQuery client."""
        self.project_id = project_id
        self.credentials = credentials
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.access_token = None
        self.session = requests.Session()

    def _get_access_token(self) -> str:
        """Get OAuth access token."""
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.credentials['refresh_token'],
                'client_id': self.credentials['client_id'],
                'client_secret': self.credentials['client_secret']
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data['access_token']
        return self.access_token

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        """Make authenticated request to API."""
        if not self.access_token:
            self._get_access_token()

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        response = self.session.request(method, url, params=params, json=data, headers=headers, timeout=self.timeout)

        if response.status_code == 401:
            self._get_access_token()
            headers['Authorization'] = f'Bearer {self.access_token}'
            response = self.session.request(method, url, params=params, json=data, headers=headers, timeout=self.timeout)

        response.raise_for_status()
        return response.json()

    def list_projects(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """List projects."""
        result = self._request('GET', '/projects', params={'maxResults': max_results})
        return result.get('projects', [])

    def list_datasets(self, max_results: int = 50, page_token: Optional[str] = None) -> Dict[str, Any]:
        """List datasets in project."""
        params = {'projectId': self.project_id, 'maxResults': max_results}
        if page_token:
            params['pageToken'] = page_token
        return self._request('GET', f'/projects/{self.project_id}/datasets', params=params)

    def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get dataset details."""
        return self._request('GET', f'/projects/{self.project_id}/datasets/{dataset_id}')

    def create_dataset(
        self,
        dataset_id: str,
        description: Optional[str] = None,
        location: str = "US"
    ) -> Dict[str, Any]:
        """Create a new dataset."""
        data = {
            'datasetReference': {
                'projectId': self.project_id,
                'datasetId': dataset_id
            },
            'location': location
        }
        if description:
            data['description'] = description
        return self._request('POST', f'/projects/{self.project_id}/datasets', data=data)

    def update_dataset(
        self,
        dataset_id: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update dataset."""
        data = {}
        if description:
            data['description'] = description
        return self._request('PATCH', f'/projects/{self.project_id}/datasets/{dataset_id}', data=data)

    def delete_dataset(self, dataset_id: str, delete_contents: bool = False) -> None:
        """Delete dataset."""
        params = {'deleteContents': str(delete_contents).lower()}
        self._request('DELETE', f'/projects/{self.project_id}/datasets/{dataset_id}', params=params)

    def list_tables(
        self,
        dataset_id: str,
        max_results: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List tables in dataset."""
        params = {'maxResults': max_results}
        if page_token:
            params['pageToken'] = page_token
        return self._request('GET', f'/projects/{self.project_id}/datasets/{dataset_id}/tables', params=params)

    def get_table(
        self,
        dataset_id: str,
        table_id: str,
        selected_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get table details."""
        params = {}
        if selected_fields:
            params['selectedFields'] = ','.join(selected_fields)
        return self._request('GET', f'/projects/{self.project_id}/datasets/{dataset_id}/tables/{table_id}', params=params)

    def create_table(
        self,
        dataset_id: str,
        table_id: str,
        schema: List[Dict[str, Any]],
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new table."""
        data = {
            'tableReference': {
                'projectId': self.project_id,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {
                'fields': schema
            }
        }
        if description:
            data['description'] = description
        return self._request('POST', f'/projects/{self.project_id}/datasets/{dataset_id}/tables', data=data)

    def delete_table(self, dataset_id: str, table_id: str) -> None:
        """Delete table."""
        self._request('DELETE', f'/projects/{self.project_id}/datasets/{dataset_id}/tables/{table_id}')

    def insert_rows(
        self,
        dataset_id: str,
        table_id: str,
        rows: List[Dict[str, Any]],
        skip_invalid_rows: bool = False,
        ignore_unknown_values: bool = False
    ) -> Dict[str, Any]:
        """Insert rows into table."""
        data = {
            'rows': [{'json': row} for row in rows],
            'skipInvalidRows': skip_invalid_rows,
            'ignoreUnknownValues': ignore_unknown_values
        }
        return self._request('POST', f'/projects/{self.project_id}/datasets/{dataset_id}/tables/{table_id}/insertAll', data=data)

    def query(
        self,
        sql: str,
        use_legacy_sql: bool = False,
        default_dataset: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Run a SQL query."""
        data = {
            'query': sql,
            'useLegacySql': use_legacy_sql,
            'dryRun': dry_run
        }
        if default_dataset:
            data['defaultDataset'] = {
                'projectId': self.project_id,
                'datasetId': default_dataset
            }
        if timeout_ms:
            data['timeoutMs'] = timeout_ms
        return self._request('POST', f'/projects/{self.project_id}/queries', data=data)

    def query_with_params(
        self,
        sql: str,
        parameters: List[Dict[str, Any]],
        use_query_cache: bool = True
    ) -> Dict[str, Any]:
        """Run a parameterized query."""
        data = {
            'query': sql,
            'parameterMode': 'NAMED',
            'queryParameters': parameters,
            'useQueryCache': use_query_cache
        }
        return self._request('POST', f'/projects/{self.project_id}/queries', data=data)

    def get_query_results(
        self,
        job_id: str,
        page_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """Get query results."""
        params = {'maxResults': max_results}
        if page_token:
            params['pageToken'] = page_token
        return self._request('GET', f'/projects/{self.project_id}/queries/{job_id}', params=params)

    def list_jobs(
        self,
        state_filter: Optional[str] = None,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """List jobs."""
        params = {'maxResults': max_results}
        if state_filter:
            params['stateFilter'] = state_filter
        return self._request('GET', f'/projects/{self.project_id}/jobs', params=params)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get job details."""
        return self._request('GET', f'/projects/{self.project_id}/jobs/{job_id}')

    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job."""
        return self._request('POST', f'/projects/{self.project_id}/jobs/{job_id}/cancel')

    def load_from_uri(
        self,
        dataset_id: str,
        table_id: str,
        source_uris: List[str],
        source_format: str = "CSV",
        write_disposition: str = "WRITE_TRUNCATE",
        skip_leading_rows: int = 0,
        field_delimiter: str = ",",
        autodetect: bool = True
    ) -> Dict[str, Any]:
        """Load data from GCS URI."""
        data = {
            'configuration': {
                'load': {
                    'sourceUris': source_uris,
                    'destinationTable': {
                        'projectId': self.project_id,
                        'datasetId': dataset_id,
                        'tableId': table_id
                    },
                    'sourceFormat': source_format,
                    'writeDisposition': write_disposition,
                    'skipLeadingRows': skip_leading_rows,
                    'fieldDelimiter': field_delimiter,
                    'autodetect': autodetect
                }
            }
        }
        return self._request('POST', f'/projects/{self.project_id}/jobs', data=data)

    def extract_to_gcs(
        self,
        dataset_id: str,
        table_id: str,
        destination_uris: List[str],
        destination_format: str = "CSV"
    ) -> Dict[str, Any]:
        """Extract table data to GCS."""
        data = {
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.project_id,
                        'datasetId': dataset_id,
                        'tableId': table_id
                    },
                    'destinationUris': destination_uris,
                    'destinationFormat': destination_format
                }
            }
        }
        return self._request('POST', f'/projects/{self.project_id}/jobs', data=data)

    def copy_table(
        self,
        source_dataset: str,
        source_table: str,
        destination_dataset: str,
        destination_table: str,
        write_disposition: str = "WRITE_TRUNCATE"
    ) -> Dict[str, Any]:
        """Copy table within BigQuery."""
        data = {
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': self.project_id,
                        'datasetId': source_dataset,
                        'tableId': source_table
                    },
                    'destinationTable': {
                        'projectId': self.project_id,
                        'datasetId': destination_dataset,
                        'tableId': destination_table
                    },
                    'writeDisposition': write_disposition
                }
            }
        }
        return self._request('POST', f'/projects/{self.project_id}/jobs', data=data)