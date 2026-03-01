"""
Creatomate API Client

Complete client for Creatomate video generation integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class CreatomateAPIClient:
    """
    Complete client for Creatomate automated video generation.
    Supports templates, renderings, and video creation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("CREATOMATE_API_KEY")
        self.base_url = base_url or os.getenv("CREATOMATE_BASE_URL", "https://api.creatomate.com/v1")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError("API key is required. Set CREATOMATE_API_KEY environment variable.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Creatomate API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

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

    # Templates

    def list_templates(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List all templates."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/templates', params=params)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/templates/{template_id}')

    # Renderings

    def create_render(
        self,
        template_id: str,
        modifications: Dict[str, Any],
        format: str = "mp4",
        quality: str = "standard"
    ) -> Dict[str, Any]:
        """
        Create a video rendering.

        Args:
            template_id: Template ID to use
            modifications: Modifications to apply (text, images, etc.)
            format: Output format (mp4, gif, png)
            quality: Quality level (standard, high, pro)

        Returns:
            Rendering information with status
        """
        data = {
            'template_id': template_id,
            'modifications': modifications,
            'format': format,
            'quality': quality
        }

        return self._request('POST', '/renderings', data=data)

    def get_render(self, rendering_id: str) -> Dict[str, Any]:
        """Get rendering details and status."""
        return self._request('GET', f'/renderings/{rendering_id}')

    def list_renderings(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List renderings."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/renderings', params=params)

    def cancel_render(self, rendering_id: str) -> Dict[str, Any]:
        """Cancel a rendering."""
        return self._request('DELETE', f'/renderings/{rendering_id}')

    # Download

    def download_render(self, rendering_id: str) -> bytes:
        """Download rendered video."""
        render = self.get_render(rendering_id)

        if render.get('status') != 'succeeded':
            raise ValueError(f"Rendering not completed. Status: {render.get('status')}")

        download_url = render.get('url')
        if not download_url:
            raise ValueError("No download URL available")

        response = requests.get(
            download_url,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()

        return response.content

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook subscription."""
        data = {
            'url': url,
            'events': events
        }
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Account

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/account')

    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self._request('GET', '/account/usage')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()