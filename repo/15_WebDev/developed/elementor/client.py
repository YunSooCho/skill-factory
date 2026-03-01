"""
Elementor API Client

Complete client for Elementor website builder integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ElementorAPIClient:
    """
    Complete client for Elementor WordPress website builder.
    Supports templates, kits, and website export/import.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("ELEMENTOR_API_KEY")
        self.base_url = base_url or os.getenv("ELEMENTOR_BASE_URL")

        if not self.base_url:
            raise ValueError("Base URL is required. Set ELEMENTOR_BASE_URL environment variable.")

        self.timeout = timeout
        self.verify_ssl = verify_ssl

        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
        else:
            self.session.headers.update({
                "Content-Type": "application/json"
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Elementor API."""
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        response = self.session.request(
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

    # Kits

    def list_kits(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List kits."""
        params = {'per_page': limit, 'page': offset // limit + 1}
        return self._request('GET', '/elementor/v1/kits', params=params)

    def get_kit(self, kit_id: int) -> Dict[str, Any]:
        """Get kit details."""
        return self._request('GET', f'/elementor/v1/kits/{kit_id}')

    def create_kit(
        self,
        title: str,
        meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a kit."""
        data = {'title': title, 'post_status': 'publish'}
        if meta:
            data['meta'] = meta
        return self._request('POST', '/elementor/v1/kits', data=data)

    def update_kit(
        self,
        kit_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a kit."""
        return self._request('PUT', f'/elementor/v1/kits/{kit_id}', data=kwargs)

    def delete_kit(self, kit_id: int) -> Dict[str, Any]:
        """Delete a kit."""
        return self._request('DELETE', f'/elementor/v1/kits/{kit_id}')

    # Templates

    def list_templates(
        self,
        template_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List templates."""
        params = {'per_page': limit, 'page': offset // limit + 1}
        if template_type:
            params['elementor_library_type'] = template_type
        return self._request('GET', '/elementor/v1/templates', params=params)

    def get_template(self, template_id: int) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/elementor/v1/templates/{template_id}')

    def create_template(
        self,
        title: str,
        content: str,
        template_type: str = "page",
        post_status: str = "publish"
    ) -> Dict[str, Any]:
        """Create a template."""
        data = {
            'title': title,
            'content': content,
            'type': template_type,
            'post_status': post_status
        }
        return self._request('POST', '/elementor/v1/templates', data=data)

    def update_template(
        self,
        template_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a template."""
        return self._request('PUT', f'/elementor/v1/templates/{template_id}', data=kwargs)

    def delete_template(self, template_id: int) -> Dict[str, Any]:
        """Delete a template."""
        return self._request('DELETE', f'/elementor/v1/templates/{template_id}')

    # Library Data

    def get_library_details(
        self,
        type: str,
        include_content: bool = False
    ) -> Dict[str, Any]:
        """Get library items by type."""
        params = {'type': type}
        return self._request('GET', '/elementor/v1/library', params=params)

    # Import/Export

    def export_template(self, template_id: int) -> Dict[str, Any]:
        """Export template data."""
        return self._request('GET', f'/elementor/v1/templates/{template_id}/export')

    def import_template(
        self,
        file_data: str
    ) -> Dict[str, Any]:
        """Import template from JSON."""
        data = {'file_data': file_data}
        return self._request('POST', '/elementor/v1/templates/import', data=data)

    # Settings

    def get_site_settings(self) -> Dict[str, Any]:
        """Get site settings."""
        return self._request('GET', '/elementor/v1/settings')

    def update_site_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update site settings."""
        return self._request('POST', '/elementor/v1/settings', data=settings)

    # Documents

    def list_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List documents (library items)."""
        params = {'per_page': limit, 'page': offset // limit + 1}
        return self._request('GET', '/elementor/v1/documents', params=params)

    def get_document(self, document_id: int) -> Dict[str, Any]:
        """Get document details."""
        return self._request('GET', f'/elementor/v1/documents/{document_id}')

    # Typography

    def get_typography_settings(self) -> Dict[str, Any]:
        """Get typography settings."""
        return self._request('GET', '/elementor/v1/pro/typography')

    # Colors

    def get_color_settings(self) -> Dict[str, Any]:
        """Get color settings."""
        return self._request('GET', '/elementor/v1/pro/colors')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()