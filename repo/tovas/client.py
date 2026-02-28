"""
Tovas API Client - Business Management Platform

Tovas provides business management APIs for invoicing, inventory,
and financial operations.
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TovasError(Exception):
    """Base exception for Tovas errors"""

class TovasRateLimitError(TovasError):
    """Rate limit exceeded"""

class TovasAuthenticationError(TovasError):
    """Authentication failed"""

class TovasClient:
    """
    Client for Tovas REST API.
    """

    BASE_URL = "https://api.tovas.com/v2"

    def __init__(self, api_key: str, account_id: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize Tovas client.

        Args:
            api_key: Tovas API key
            account_id: Account ID (optional)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.min_delay = 0.2
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise TovasRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise TovasAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise TovasError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise TovasError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of invoices."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get specific invoice details."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices/{invoice_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """Create a new invoice."""
        self._enforce_rate_limit()
        if self.account_id:
            invoice_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/invoices",
                                json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        """Update an existing invoice."""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/invoices/{invoice_id}",
                               json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of clients."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/clients",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        """Create a new client."""
        self._enforce_rate_limit()
        if self.account_id:
            client_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/clients",
                                json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of products."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/products",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_product(self, product_data: Dict) -> Dict[str, Any]:
        """Create a new product."""
        self._enforce_rate_limit()
        if self.account_id:
            product_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/products",
                                json=product_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_orders(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of orders."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/orders",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_order(self, order_data: Dict) -> Dict[str, Any]:
        """Create a new order."""
        self._enforce_rate_limit()
        if self.account_id:
            order_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/orders",
                                json=order_data, timeout=self.timeout)
        return self._handle_response(resp)