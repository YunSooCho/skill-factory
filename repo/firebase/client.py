"""
Firebase API Client

This module provides a Python client for interacting with Firebase
Realtime Database and Firestore.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class FirebaseClient:
    """
    Client for Firebase Database API.

    Firebase provides:
    - Realtime Database
    - Firestore (NoSQL)
    - Offline support
    - Automatic scaling
    - Real-time synchronization
    """

    def __init__(
        self,
        project_id: str,
        api_key: str,
        db_type: str = "firestore",
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the Firebase client."""
        self.project_id = project_id
        self.api_key = api_key
        self.db_type = db_type.lower()
        self.timeout = timeout

        if db_type.lower() == "firestore":
            if base_url:
                self.base_url = base_url
            else:
                self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"
        else:
            if base_url:
                self.base_url = base_url
            else:
                self.base_url = f"https://{project_id}-default-rtdb.firebaseio.com"

        self.session = requests.Session()

    def _firestore_request(
        self,
        method: str,
        path: str,
        params=None,
        data=None,
        headers=None
    ) -> Dict[str, Any]:
        """Make request to Firestore API."""
        url = f"{self.base_url}{path}"
        request_headers = {}
        if headers:
            request_headers.update(headers)

        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            headers=request_headers,
            timeout=self.timeout
        )
        response.raise_for_status()

        if response.status_code == 204:
            return {}
        return response.json()

    def _rtdb_request(
        self,
        method: str,
        path: str,
        params=None,
        data=None,
        query_auth: bool = True
    ) -> Any:
        """Make request to Realtime Database API."""
        url = f"{self.base_url}{path}"
        request_params = params or {}
        if query_auth:
            request_params['auth'] = self.api_key

        response = self.session.request(
            method,
            url,
            params=request_params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()

        if response.status_code == 204:
            return None
        return response.json()

    # Firebase Realtime Database methods

    def rtdb_get(self, path: str) -> Dict[str, Any]:
        """Get data from Realtime Database."""
        return self._rtdb_request('GET', f"/{path}.json")

    def rtdb_set(self, path: str, data: Any) -> None:
        """Set data at path (overwrite)."""
        self._rtdb_request('PUT', f"/{path}.json", data=data)

    def rtdb_update(self, path: str, data: Dict[str, Any]) -> None:
        """Update data at path (partial update)."""
        self._rtdb_request('PATCH', f"/{path}.json", data=data)

    def rtdb_push(self, path: str, data: Any) -> Dict[str, str]:
        """Push data to path (creates new key)."""
        response = self._rtdb_request('POST', f"/{path}.json", data=data)
        return {'name': response['name']}

    def rtdb_delete(self, path: str) -> None:
        """Delete data at path."""
        self._rtdb_request('DELETE', f"/{path}.json")

    def rtdb_list(self, path: str) -> List[str]:
        """List keys at path."""
        return self._rtdb_request('GET', f"/{path}.json?shallow=true")

    def rtdb_query(
        self,
        path: str,
        order_by: Optional[str] = None,
        limit_to_first: Optional[int] = None,
        limit_to_last: Optional[int] = None,
        start_at: Optional[str] = None,
        end_at: Optional[str] = None,
        equal_to: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query Realtime Database with filters."""
        params = {}
        if order_by:
            params['orderBy'] = f'"{order_by}"'
        if limit_to_first:
            params['limitToFirst'] = limit_to_first
        if limit_to_last:
            params['limitToLast'] = limit_to_last
        if start_at:
            params['startAt'] = f'"{start_at}"'
        if end_at:
            params['endAt'] = f'"{end_at}"'
        if equal_to:
            params['equalTo'] = f'"{equal_to}"'

        return self._rtdb_request('GET', f"/{path}.json", params=params)

    # Firestore methods

    def firestore_get_document(self, document_path: str) -> Optional[Dict[str, Any]]:
        """Get a Firestore document."""
        try:
            return self._firestore_request('GET', f"/{document_path}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def firestore_create_document(
        self,
        collection: str,
        document_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a Firestore document."""
        document_path = f"{collection}/{document_id}"
        firestore_data = {}

        for key, value in data.items():
            if isinstance(value, bool):
                firestore_data[key] = {'booleanValue': value}
            elif isinstance(value, int):
                firestore_data[key] = {'integerValue': str(value)}
            elif isinstance(value, float):
                firestore_data[key] = {'doubleValue': value}
            elif isinstance(value, str):
                firestore_data[key] = {'stringValue': value}
            elif isinstance(value, dict):
                firestore_data[key] = {'mapValue': {'fields': value}}
            elif isinstance(value, list):
                firestore_data[key] = {'arrayValue': {'values': value}}
            elif value is None:
                firestore_data[key] = {'nullValue': 'NULL_VALUE'}
            else:
                firestore_data[key] = {'stringValue': str(value)}

        payload = {'fields': firestore_data}
        return self._firestore_request('PUT', f"/{document_path}", data=payload)

    def firestore_add_document(
        self,
        collection: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a document with auto-generated ID."""
        firestore_data = {}

        for key, value in data.items():
            if isinstance(value, bool):
                firestore_data[key] = {'booleanValue': value}
            elif isinstance(value, int):
                firestore_data[key] = {'integerValue': str(value)}
            elif isinstance(value, float):
                firestore_data[key] = {'doubleValue': value}
            elif isinstance(value, str):
                firestore_data[key] = {'stringValue': value}
            elif isinstance(value, dict):
                firestore_data[key] = {'mapValue': {'fields': value}}
            elif isinstance(value, list):
                firestore_data[key] = {'arrayValue': {'values': value}}
            elif value is None:
                firestore_data[key] = {'nullValue': 'NULL_VALUE'}
            else:
                firestore_data[key] = {'stringValue': str(value)}

        payload = {'fields': firestore_data}
        result = self._firestore_request('POST', f"/{collection}", data=payload)
        return {'name': result.get('name', '').split('/')[-1]}

    def firestore_update_document(
        self,
        document_path: str,
        data: Dict[str, Any],
        mask: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update a Firestore document (partial)."""
        firestore_data = {}

        for key, value in data.items():
            if isinstance(value, bool):
                firestore_data[key] = {'booleanValue': value}
            elif isinstance(value, int):
                firestore_data[key] = {'integerValue': str(value)}
            elif isinstance(value, float):
                firestore_data[key] = {'doubleValue': value}
            elif isinstance(value, str):
                firestore_data[key] = {'stringValue': value}
            elif isinstance(value, dict):
                firestore_data[key] = {'mapValue': {'fields': value}}
            elif isinstance(value, list):
                firestore_data[key] = {'arrayValue': {'values': value}}
            elif value is None:
                firestore_data[key] = {'nullValue': 'NULL_VALUE'}
            else:
                firestore_data[key] = {'stringValue': str(value)}

        payload = {'fields': firestore_data}
        if mask:
            payload['updateMask'] = mask

        return self._firestore_request('PATCH', f"/{document_path}", data=payload)

    def firestore_delete_document(self, document_path: str) -> None:
        """Delete a Firestore document."""
        self._firestore_request('DELETE', f"/{document_path}")

    def firestore_list_documents(
        self,
        collection: str,
        page_size: int = 100,
        page_token: Optional[str] = None,
        order_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """List documents in a collection."""
        params = {'pageSize': page_size}
        if page_token:
            params['pageToken'] = page_token
        if order_by:
            params['orderBy'] = order_by

        return self._firestore_request('GET', f"/{collection}", params=params)

    def firestore_query(
        self,
        collection: str,
        filters: List[Dict[str, Any]],
        limit: int = 100,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query Firestore collection with filters."""
        structured_query = {
            'from': [{'collectionId': collection}],
            'where': filters,
            'limit': limit
        }

        if order_by:
            structured_query['orderBy'] = [
                {'field': {'fieldPath': order_by}, 'direction': 'ASCENDING'}
            ]

        payload = {'structuredQuery': structured_query}
        result = self._firestore_request('POST', f":runQuery", data=payload)

        documents = []
        for item in result:
            if 'document' in item:
                documents.append(item['document'])

        return documents

    def firestore_batch_write(self, writes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch write operations to Firestore."""
        payload = {'writes': writes}
        return self._firestore_request('POST', ":commit", data=payload)

    def firestore_transaction(self, read_only: bool = False) -> str:
        """Begin a new transaction."""
        payload = {'options': {'readOnly': read_only}}
        result = self._firestore_request('POST', ":beginTransaction", data=payload)
        return result.get('transaction')

    def firestore_run_transaction(
        self,
        transaction: str,
        reads: List[str],
        writes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute a transaction."""
        payload = {
            'transaction': transaction,
            'reads': reads,
            'writes': writes
        }
        return self._firestore_request('POST', ":commit", data=payload)

    def firestore_listen(self, document_path: str) -> str:
        """Start listening to document changes (returns channel ID)."""
        payload = {
            'documents': [document_path],
            'addTarget': {
                'documents': [document_path]
            }
        }
        result = self._firestore_request('POST', ":listen", data=payload)
        return result.get('targetChange', {}).get('resumeToken', '')

    def firestore_export(
        self,
        output_uri_prefix: str,
        collection_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Export Firestore data."""
        payload = {
            'outputUriPrefix': output_uri_prefix
        }
        if collection_ids:
            payload['collectionIds'] = collection_ids

        return self._firestore_request(
            'POST',
            f"/databases/(default)/operations:exportDocuments",
            data=payload
        )

    def firestore_import(
        self,
        input_uri_prefix: str,
        collection_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Import Firestore data."""
        payload = {
            'inputUriPrefix': input_uri_prefix
        }
        if collection_ids:
            payload['collectionIds'] = collection_ids

        return self._firestore_request(
            'POST',
            f"/databases/(default)/operations:importDocuments",
            data=payload
        )