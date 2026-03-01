"""
Moneybird API Client - Dutch Accounting Platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class MoneybirdError(Exception):
    """Base exception"""

class MoneybirdRateLimitError(MoneybirdError):
    """Rate limit"""

class MoneybirdAuthenticationError(MoneybirdError):
    """Auth failed"""

class MoneybirdClient:
    BASE_URL = "https://moneybird.com/api/v2"

    def __init__(self, api_key: str, account_id: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.2
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise MoneybirdRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise MoneybirdAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise MoneybirdError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise MoneybirdError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices/{invoice_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/invoices", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/invoices/{invoice_id}", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/invoices/{invoice_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/clients"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/clients", json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/products"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str, email_data: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}/send"
        data = email_data if email_data else {}
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)
