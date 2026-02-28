"""
QuickBase API Client

This module provides a Python client for interacting with QuickBase low-code platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class QuickBaseClient:
    """
    Client for QuickBase Low-Code Platform.

    QuickBase provides:
    - Table and record management
    - Field CRUD operations
    - Reporting and analytics
    - User and role management
    - App and form management
    """

    def __init__(
        self,
        user_token: str,
        realm_hostname: str = "quickbase.com",
        base_url: str = "https://api.quickbase.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the QuickBase client.

        Args:
            user_token: QuickBase user token
            realm_hostname: QuickBase realm hostname (e.g., mycompany.quickbase.com)
            base_url: Base URL for the QuickBase API
            timeout: Request timeout in seconds
        """
        self.user_token = user_token
        self.realm_hostname = realm_hostname
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'QB-Realm-Hostname': realm_hostname,
            'Authorization': f'Bearer {user_token}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        json_data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")

        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_apps(self) -> List[Dict[str, Any]]:
        """Get all apps in the realm."""
        response = self.session.get(
            f"{self.base_url}/apps",
            params={'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_app(self, app_id: str) -> Dict[str, Any]:
        """Get app details."""
        response = self.session.get(f"{self.base_url}/apps/{app_id}")
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def create_app(
        self,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new app."""
        data = {
            "name": name,
            "description": description
        }
        response = self.session.post(
            f"{self.base_url}/apps",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def update_app(
        self,
        app_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update app properties."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        response = self.session.patch(
            f"{self.base_url}/apps/{app_id}",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def delete_app(self, app_id: str) -> Dict[str, Any]:
        """Delete an app."""
        response = self.session.delete(f"{self.base_url}/apps/{app_id}")
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_tables(self, app_id: str) -> List[Dict[str, Any]]:
        """Get all tables in an app."""
        response = self.session.get(
            f"{self.base_url}/tables",
            params={'appId': app_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_table(self, table_id: str, app_id: str) -> Dict[str, Any]:
        """Get table details."""
        response = self.session.get(f"{self.base_url}/tables/{table_id}", params={'appId': app_id})
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def create_table(
        self,
        app_id: str,
        name: str,
        description: str = "",
        singleton: bool = False
    ) -> Dict[str, Any]:
        """Create a new table."""
        data = {
            "appId": app_id,
            "name": name,
            "description": description,
            "singletonRecord": singleton
        }
        response = self.session.post(
            f"{self.base_url}/tables",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def update_table(
        self,
        table_id: str,
        app_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update table properties."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        response = self.session.patch(
            f"{self.base_url}/tables/{table_id}",
            params={'appId': app_id},
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def delete_table(self, table_id: str, app_id: str) -> Dict[str, Any]:
        """Delete a table."""
        response = self.session.delete(f"{self.base_url}/tables/{table_id}", params={'appId': app_id})
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_fields(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all fields in a table."""
        response = self.session.get(
            f"{self.base_url}/fields",
            params={'tableId': table_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_field(self, field_id: str, table_id: str) -> Dict[str, Any]:
        """Get field details."""
        response = self.session.get(
            f"{self.base_url}/fields/{field_id}",
            params={'tableId': table_id}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def create_field(
        self,
        table_id: str,
        type: str,
        label: str,
        description: str = "",
        required: bool = False,
        field_help: str = ""
    ) -> Dict[str, Any]:
        """Create a new field."""
        data = {
            "tableId": table_id,
            "type": type,
            "label": label,
            "description": description,
            "required": required,
            "fieldHelp": field_help
        }
        response = self.session.post(
            f"{self.base_url}/fields",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def update_field(
        self,
        field_id: str,
        table_id: str,
        label: Optional[str] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update field properties."""
        data = {}
        if label:
            data['label'] = label
        if description:
            data['description'] = description
        if required is not None:
            data['required'] = required

        response = self.session.patch(
            f"{self.base_url}/fields/{field_id}",
            params={'tableId': table_id},
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def delete_field(self, field_id: str, table_id: str) -> Dict[str, Any]:
        """Delete a field."""
        response = self.session.delete(
            f"{self.base_url}/fields/{field_id}",
            params={'tableId': table_id}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_records(
        self,
        table_id: str,
        fields: Optional[List[str]] = None,
        where: Optional[str] = None,
        sort_by: Optional[List[str]] = None,
        skip: int = 0,
        top: int = 100
    ) -> Dict[str, Any]:
        """Get records from a table."""
        params = {
            'tableId': table_id,
            'skip': skip,
            'top': top
        }
        if fields:
            params['select'] = ','.join(fields)
        if where:
            params['where'] = where
        if sort_by:
            params['sortBy'] = ','.join(sort_by)

        return self._request('GET', '/records', params=params)

    def get_record(self, record_id: str, table_id: str) -> Dict[str, Any]:
        """Get a specific record."""
        response = self.session.get(
            f"{self.base_url}/records/{record_id}",
            params={'tableId': table_id}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def add_record(
        self,
        table_id: str,
        data: Dict[str, Any],
        fields_to_return: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Add a new record."""
        payload = {
            "to": table_id,
            "data": [data]
        }
        if fields_to_return:
            payload['fieldsToReturn'] = fields_to_return

        response = self.session.post(
            f"{self.base_url}/records",
            json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def update_record(
        self,
        record_id: str,
        table_id: str,
        data: Dict[str, Any],
        fields_to_return: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update a record."""
        payload = {
            "to": table_id,
            "data": [
                {
                    "6": {"value": record_id},
                    **data
                }
            ]
        }
        if fields_to_return:
            payload['fieldsToReturn'] = fields_to_return

        response = self.session.put(
            f"{self.base_url}/records",
            json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def update_records(
        self,
        table_id: str,
        records: List[Dict[str, Any]],
        fields_to_return: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update multiple records."""
        payload = {
            "to": table_id,
            "data": records
        }
        if fields_to_return:
            payload['fieldsToReturn'] = fields_to_return

        response = self.session.put(
            f"{self.base_url}/records",
            json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def delete_record(self, record_id: str, table_id: str) -> Dict[str, Any]:
        """Delete a record."""
        response = self.session.delete(
            f"{self.base_url}/records/{record_id}",
            params={'tableId': table_id}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def delete_records(self, table_id: str, record_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple records."""
        payload = {
            "tableId": table_id,
            "recordIds": record_ids
        }
        response = self.session.delete(
            f"{self.base_url}/records",
            json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def query(
        self,
        table_id: str,
        where: str,
        select: Optional[List[str]] = None,
        sort_by: Optional[List[str]] = None,
        skip: int = 0,
        top: int = 100
    ) -> Dict[str, Any]:
        """Query records with a WHERE clause."""
        return self.get_records(
            table_id=table_id,
            fields=select,
            where=where,
            sort_by=sort_by,
            skip=skip,
            top=top
        )

    def run_report(self, table_id: str, report_id: str, skip: int = 0, top: int = 100) -> Dict[str, Any]:
        """Run a report."""
        params = {
            'tableId': table_id,
            'skip': skip,
            'top': top
        }
        response = self.session.get(
            f"{self.base_url}/reports/{report_id}",
            params=params
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_reports(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all reports for a table."""
        response = self.session.get(
            f"{self.base_url}/reports",
            params={'tableId': table_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_users(self, app_id: str) -> List[Dict[str, Any]]:
        """Get all users in an app."""
        response = self.session.get(
            f"{self.base_url}/users",
            params={'appId': app_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_user(self, user_id: str, app_id: str) -> Dict[str, Any]:
        """Get user details."""
        response = self.session.get(
            f"{self.base_url}/users/{user_id}",
            params={'appId': app_id}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def invite_user(
        self,
        email: str,
        app_id: str,
        role_id: str
    ) -> Dict[str, Any]:
        """Invite a user to an app."""
        data = {
            "appId": app_id,
            "email": email,
            "roleId": role_id
        }
        response = self.session.post(
            f"{self.base_url}/users/invite",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_roles(self, app_id: str) -> List[Dict[str, Any]]:
        """Get all roles in an app."""
        response = self.session.get(
            f"{self.base_url}/roles",
            params={'appId': app_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information."""
        response = self.session.get(f"{self.base_url}/user")
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def create_form(
        self,
        table_id: str,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new form."""
        data = {
            "tableId": table_id,
            "name": name,
            "description": description
        }
        response = self.session.post(
            f"{self.base_url}/forms",
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()

    def get_forms(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all forms for a table."""
        response = self.session.get(
            f"{self.base_url}/forms",
            params={'tableId': table_id, 'top': 500}
        )
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}")
        return response.json()