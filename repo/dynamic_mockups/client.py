"""
Dynamic Mockups Client - Mockup Generation API
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class DynamicMockupsClient:
    """Complete client for Dynamic Mockups API - Product mockup generation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("DYNAMIC_MOCKUPS_API_KEY")
        self.base_url = (base_url or os.getenv("DYNAMIC_MOCKUPS_BASE_URL", "https://api.dynamicmockups.com/v1")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key required. Set DYNAMIC_MOCKUPS_API_KEY")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, data=None, params=None, files=None) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        headers = dict(self.session.headers)
        if files:
            del headers["Content-Type"]
        
        response = self.session.request(
            method=method, url=url, json=data, params=params, files=files,
            timeout=self.timeout, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    # Mockups
    def list_templates(self, category: Optional[str] = None) -> Dict[str, Any]:
        params = {"category": category} if category else {}
        return self._request("GET", "templates", params=params)
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        return self._request("GET", f"templates/{template_id}")
    
    def generate_mockup(
        self,
        template_id: str,
        image_url: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        data = {"template_id": template_id, "image_url": image_url}
        if options:
            data["options"] = options
        return self._request("POST", "mockups/generate", data=data)
    
    def get_mockup(self, mockup_id: str) -> Dict[str, Any]:
        return self._request("GET", f"mockups/{mockup_id}")
    
    def download_mockup(self, mockup_id: str, format: str = "png") -> bytes:
        response = self.session.get(
            f"{self.base_url}/mockups/{mockup_id}/download",
            params={"format": format},
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.content
    
    # Categories
    def list_categories(self) -> Dict[str, Any]:
        return self._request("GET", "categories")
    
    # Batch Operations
    def generate_batch(self, template_id: str, image_urls: List[str]) -> Dict[str, Any]:
        return self._request("POST", "mockups/batch", data={"template_id": template_id, "image_urls": image_urls})
    
    def get_batch_status(self, batch_id: str) -> Dict[str, Any]:
        return self._request("GET", f"batch/{batch_id}")
    
    # Webhooks
    def create_webhook(self, url: str, events: List[str]) -> Dict[str, Any]:
        return self._request("POST", "webhooks", data={"url": url, "events": events})
    
    def delete_webhook(self, webhook_id: str) -> None:
        self._request("DELETE", f"webhooks/{webhook_id}")
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()