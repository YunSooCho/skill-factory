"""
Zoho Creator API Client

This module provides a Python client for interacting with Zoho Creator low-code platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class ZohoCreatorClient:
    """
    Client for Zoho Creator Low-Code Platform.

    Zoho Creator provides:
    - Application and form management
    - Record management
    - Field operations
    - Report generation
    - Workflow automation
    """

    def __init__(
        self,
        auth_token: str,
        owner: str,
        app_link_name: str,
        base_url: str = "https://creator.zoho.com/api/v2",
        timeout: int = 30
    ):
        """
        Initialize the Zoho Creator client.

        Args:
            auth_token: Zoho OAuth token
            owner: Account owner ID
            app_link_name: Application link name
            base_url: Base URL for the Zoho Creator API
            timeout: Request timeout in seconds
        """
        self.auth_token = auth_token
        self.owner = owner
        self.app_link_name = app_link_name
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None, json_data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, data=data, json=json_data, timeout=self.timeout)
        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")
        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_forms(self) -> List[Dict[str, Any]]:
        """Get all forms in the application."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/All_Forms')

    def get_form(self, form_link_name: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}')

    def get_records(
        self,
        form_link_name: str,
        limit: int = 100,
        offset: int = 0,
        criteria: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get records from a form."""
        params = {'limit': limit, 'offset': offset}
        if criteria:
            params['criteria'] = criteria
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/{form_link_name}/JSON', params=params)

    def get_record(self, form_link_name: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/{form_link_name}/{record_id}')

    def create_record(self, form_link_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/JSON'
        return self._request('POST', url, data=json.dumps(data))

    def update_record(self, form_link_name: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/JSON'
        return self._request('POST', url, data=json.dumps(data))

    def delete_record(self, form_link_name: str, record_id: str) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}')

    def batch_create_records(self, form_link_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple records in batch."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/Batch_Insert'
        data = {'data': records}
        return self._request('POST', url, json_data=data)

    def batch_update_records(self, form_link_name: str, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update multiple records in batch."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/Batch_Update'
        data = {'data': updates}
        return self._request('POST', url, json_data=data)

    def batch_delete_records(self, form_link_name: str, record_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple records in batch."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/Batch_Delete'
        data = {'IDs': record_ids}
        return self._request('POST', url, json_data=data)

    def get_fields(self, form_link_name: str) -> List[Dict[str, Any]]:
        """Get all fields in a form."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/fields')

    def add_field(
        self,
        form_link_name: str,
        field_name: str,
        field_type: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a new field to a form."""
        data = {
            'field_name': field_name,
            'field_type': field_type
        }
        if options:
            data['options'] = options
        return self._request('POST', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/fields', json_data=data)

    def delete_field(self, form_link_name: str, field_link_name: str) -> Dict[str, Any]:
        """Delete a field from a form."""
        return self._request('DELETE', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/field/{field_link_name}')

    def get_reports(self) -> List[Dict[str, Any]]:
        """Get all reports in the application."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/All_Reports')

    def get_report(self, report_link_name: str) -> Dict[str, Any]:
        """Get report details."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/{report_link_name}')

    def execute_report(
        self,
        report_link_name: str,
        limit: int = 100,
        offset: int = 0,
        criteria: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a report."""
        params = {'limit': limit, 'offset': offset}
        if criteria:
            params['criteria'] = criteria
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/{report_link_name}/JSON', params=params)

    def get_pages(self) -> List[Dict[str, Any]]:
        """Get all pages in the application."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/application/pages')

    def get_settings(self) -> Dict[str, Any]:
        """Get application settings."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/application/settings')

    def upload_file(self, form_link_name: str, record_id: str, field_name: str, file_path: str) -> Dict[str, Any]:
        """Upload a file to a record field."""
        url = f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/file/{field_name}'
        with open(file_path, 'rb') as f:
            files = {'file': file_path}
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.post(url, files=files, headers=headers, timeout=self.timeout)

        if response.status_code >= 400:
            raise Exception(f"File upload failed: {response.text}")
        return response.json()

    def download_file(self, form_link_name: str, record_id: str, field_name: str) -> Dict[str, Any]:
        """Download a file from a record field."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/file/{field_name}')

    def trigger_workflow(self, form_link_name: str, workflow_name: str, record_id: Optional[str] = None) -> Dict[str, Any]:
        """Trigger a custom workflow."""
        data = {'workflow': workflow_name}
        if record_id:
            data['record_id'] = record_id
        return self._request('POST', f'/{self.owner}/{self.app_link_name}/workflow/trigger', json_data=data)

    def get_statistics(self, form_link_name: str) -> Dict[str, Any]:
        """Get form statistics."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/statistics')

    def search_records(
        self,
        form_link_name: str,
        search_field: str,
        search_text: str,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Search records by field."""
        params = {
            'search_field': search_field,
            'search_text': search_text,
            'limit': limit
        }
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/report/{form_link_name}/search', params=params)

    def get_related_records(
        self,
        form_link_name: str,
        record_id: str,
        related_form_link_name: str
    ) -> Dict[str, Any]:
        """Get related records."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/related/{related_form_link_name}')

    def add_comment(self, form_link_name: str, record_id: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a record."""
        data = {'content': comment}
        return self._request('POST', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/comments', json_data=data)

    def get_comments(self, form_link_name: str, record_id: str) -> List[Dict[str, Any]]:
        """Get all comments on a record."""
        return self._request('GET', f'/{self.owner}/{self.app_link_name}/form/{form_link_name}/{record_id}/comments')