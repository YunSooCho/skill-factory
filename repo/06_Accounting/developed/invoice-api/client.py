"""
Invoice API Client - Generic Invoice Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class InvoiceAPIError(Exception):
    """Base exception"""

class InvoiceAPIRateLimitError(InvoiceAPIError):
    """Rate limit"""

class InvoiceAPIAuthenticationError(InvoiceAPIError):
    """Auth failed"""

class InvoiceAPIClient:
    BASE_URL = "https://api.invoice.example.com"

    def __init__(self, api_key: str, account_id: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
            raise InvoiceAPIRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise InvoiceAPIAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise InvoiceAPIError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise InvoiceAPIError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices/{invoice_id}"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices"
        resp = self.session.post(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices/{invoice_id}"
        resp = self.session.put(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices/{invoice_id}"
        resp = self.session.delete(url, timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/clients"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/clients"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/clients"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/clients"
        resp = self.session.post(url, json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/products"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/products"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str, email_data: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}/send"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/invoices/{invoice_id}/send"
        data = email_data if email_data else {}
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_payments(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/payments"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/payments"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_payment(self, payment_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/payments"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/payments"
        resp = self.session.post(url, json=payment_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_recurring_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/recurring_invoices"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/recurring_invoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_recurring_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/recurring_invoices"
        if self.account_id:
            url = f"{self.BASE_URL}/accounts/{self.account_id}/recurring_invoices"
        resp = self.session.post(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)