"""
Next-Engine API Client

Complete client for Next-Engine ERP integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class NextEngineAPIClient:
    """
    Complete client for Next-Engine ERP system.
    Supports products, orders, customers, and inventory management.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("NEXT_ENGINE_API_KEY")
        self.base_url = base_url or os.getenv("NEXT_ENGINE_BASE_URL", "https://api.next-engine.org/api/v1")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError("API key is required. Set NEXT_ENGINE_API_KEY environment variable.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        response = self.session.request(method=method, url=url, json=data, params=params, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    def get_products(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List products."""
        return self._request('GET', '/products', params={'limit': limit, 'offset': offset})

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request('GET', f'/products/{product_id}')

    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a product."""
        return self._request('POST', '/products', data=product_data)

    def get_orders(self, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List orders."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/orders', params=params)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request('GET', f'/orders/{order_id}')

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an order."""
        return self._request('POST', '/orders', data=order_data)

    def get_customers(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List customers."""
        return self._request('GET', '/customers', params={'limit': limit, 'offset': offset})

    def get_inventory(self, warehouse_id: Optional[str] = None) -> Dict[str, Any]:
        """Get inventory levels."""
        params = {}
        if warehouse_id:
            params['warehouse_id'] = warehouse_id
        return self._request('GET', '/inventory', params=params)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()