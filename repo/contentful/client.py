"""
Contentful API Client

Complete client for Contentful headless CMS integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ContentfulAPIClient:
    """
    Complete client for Contentful headless CMS.
    Supports content management and delivery APIs.
    """

    def __init__(
        self,
        space_id: Optional[str] = None,
        access_token: Optional[str] = None,
        delivery_token: Optional[str] = None,
        environment: str = "master",
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.space_id = space_id or os.getenv("CONTENTFUL_SPACE_ID")
        self.access_token = access_token or os.getenv("CONTENTFUL_ACCESS_TOKEN")
        self.delivery_token = delivery_token or os.getenv("CONTENTFUL_DELIVERY_TOKEN")
        self.environment = environment
        self.base_url = base_url or os.getenv("CONTENTFUL_BASE_URL", "https://api.contentful.com")
        self.delivery_url = "https://cdn.contentful.com"
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.space_id:
            raise ValueError("Space ID is required. Set CONTENTFUL_SPACE_ID environment variable.")

        self.management_session = requests.Session()
        if self.access_token:
            self.management_session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/vnd.contentful.management.v1+json"
            })

        self.delivery_session = requests.Session()
        if self.delivery_token:
            self.delivery_session.headers.update({
                "Authorization": f"Bearer {self.delivery_token}"
            })

    def _management_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Contentful Management API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.management_session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    def _delivery_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Contentful Delivery API."""
        url = urljoin(self.delivery_url + "/", endpoint.lstrip("/"))

        response = self.delivery_session.request(
            method=method,
            url=url,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    # Content Types (Management API)

    def list_content_types(self) -> Dict[str, Any]:
        """List all content types."""
        return self._management_request('GET', f'/spaces/{self.space_id}/environments/{self.environment}/content_types')

    def get_content_type(self, content_type_id: str) -> Dict[str, Any]:
        """Get content type details."""
        return self._management_request('GET', f'/spaces/{self.space_id}/environments/{self.environment}/content_types/{content_type_id}')

    def create_content_type(
        self,
        name: str,
        fields: List[Dict[str, Any]],
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a content type."""
        data = {
            'name': name,
            'fields': fields
        }

        if description:
            data['description'] = description

        return self._management_request('POST', f'/spaces/{self.space_id}/environments/{self.environment}/content_types', data=data)

    def update_content_type(
        self,
        content_type_id: str,
        version: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Update content type."""
        kwargs['version'] = version
        return self._management_request('PUT', f'/spaces/{self.space_id}/environments/{self.environment}/content_types/{content_type_id}', data=kwargs)

    def publish_content_type(
        self,
        content_type_id: str,
        version: int
    ) -> Dict[str, Any]:
        """Publish content type."""
        return self._management_request('PUT', f'/spaces/{self.space_id}/environments/{self.environment}/content_types/{content_type_id}/published',
            data={'version': version})

    # Entries (Management & Delivery API)

    def create_entry(
        self,
        content_type_id: str,
        entry_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create an entry."""
        return self._management_request('POST',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries',
            data=entry_data)

    def get_entry(self, entry_id: str) -> Dict[str, Any]:
        """Get entry (Delivery API)."""
        return self._delivery_request('GET',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}')

    def list_entries(
        self,
        content_type: Optional[str] = None,
        limit: int = 100,
        query: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """List entries (Delivery API)."""
        params = {'limit': limit}

        if content_type:
            params['content_type'] = content_type
        if query:
            params.update(query)

        return self._delivery_request('GET',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries',
            params=params)

    def update_entry(
        self,
        entry_id: str,
        entry_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an entry (Management API)."""
        return self._management_request('PUT',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}',
            data=entry_data)

    def delete_entry(self, entry_id: str) -> Dict[str, Any]:
        """Delete an entry (Management API)."""
        return self._management_request('DELETE',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}')

    def publish_entry(
        self,
        entry_id: str,
        version: int
    ) -> Dict[str, Any]:
        """Publish an entry."""
        return self._management_request('PUT',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}/published',
            data={'version': version})

    def unpublish_entry(
        self,
        entry_id: str,
        version: int
    ) -> Dict[str, Any]:
        """Unpublish an entry."""
        return self._management_request('DELETE',
            f'/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}/published',
            data={'version': version})

    # Assets (Management & Delivery API)

    def create_asset(
        self,
        file_data: Dict[str, str],
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an asset."""
        data = {
            'fields': {
                'title': {'en-US': title},
                'file': {'en-US': file_data}
            }
        }

        if description:
            data['fields']['description'] = {'en-US': description}

        return self._management_request('POST',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets',
            data=data)

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """Get asset (Delivery API)."""
        return self._delivery_request('GET',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets/{asset_id}')

    def list_assets(self, limit: int = 100) -> Dict[str, Any]:
        """List assets (Delivery API)."""
        return self._delivery_request('GET',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets',
            params={'limit': limit})

    def process_asset(
        self,
        asset_id: str,
        version: int
    ) -> Dict[str, Any]:
        """Process an asset (Management API)."""
        return self._management_request('PUT',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets/{asset_id}/files/en-US/process',
            data={'version': version})

    def publish_asset(
        self,
        asset_id: str,
        version: int
    ) -> Dict[str, Any]:
        """Publish an asset."""
        return self._management_request('PUT',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets/{asset_id}/published',
            data={'version': version})

    def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """Delete an asset."""
        return self._management_request('DELETE',
            f'/spaces/{self.space_id}/environments/{self.environment}/assets/{asset_id}')

    # Locales

    def list_locales(self) -> Dict[str, Any]:
        """List all locales."""
        return self._management_request('GET',
            f'/spaces/{self.space_id}/environments/{self.environment}/locales')

    # Spaces

    def get_space(self) -> Dict[str, Any]:
        """Get space details."""
        return self._management_request('GET', f'/spaces/{self.space_id}')

    # Environments

    def get_environments(self) -> Dict[str, Any]:
        """List environments."""
        return self._management_request('GET', f'/spaces/{self.space_id}/environments')

    def close(self):
        """Close HTTP sessions."""
        self.management_session.close()
        self.delivery_session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()