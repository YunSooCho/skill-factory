"""
Fakturoid API Client - Czech Invoice Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class FakturoidError(Exception):
    """Base exception"""

class FakturoidRateLimitError(FakturoidError):
    """Rate limit"""

class FakturoidAuthenticationError(FakturoidError):
    """Auth failed"""

class FakturoidClient:
    BASE_URL = "https://app.fakturoid.cz/api/v2"

    def __init__(self, email: str, api_key: str, slug: Optional[str] = None, timeout: int = 30):
        self.email = email
        self.api_key = api_key
        self.slug = slug
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (email, api_key)
        self.session.headers.update({
            'User-Agent': 'Python Fakturoid Client',
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
            raise FakturoidRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise FakturoidAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            error_text = resp.text
            try:
                error_data = resp.json()
                error_text = error_data.get('error', resp.text)
            except:
                pass
            raise FakturoidError(f"Error ({resp.status_code}): {error_text}")
        return resp.json()

    def get_invoices(self, status: Optional[str] = None, page: int = 1) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {'page': page}
        if status:
            params['status'] = status
        url = f"{self.BASE_URL}/{self.slug}/invoices.json" if self.slug else f"{self.BASE_URL}/invoices.json"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices/{invoice_id}.json" if self.slug else f"{self.BASE_URL}/invoices/{invoice_id}.json"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices.json" if self.slug else f"{self.BASE_URL}/invoices.json"
        resp = self.session.post(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices/{invoice_id}.json" if self.slug else f"{self.BASE_URL}/invoices/{invoice_id}.json"
        resp = self.session.patch(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices/{invoice_id}.json" if self.slug else f"{self.BASE_URL}/invoices/{invoice_id}.json"
        resp = self.session.delete(url, timeout=self.timeout)
        return self._handle_response(resp)

    def get_subjects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/subjects.json" if self.slug else f"{self.BASE_URL}/subjects.json"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)

    def get_generators(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/generators.json" if self.slug else f"{self.BASE_URL}/generators.json"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)

    def get_account(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/account.json"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str, message: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices/{invoice_id}/fire.json" if self.slug else f"{self.BASE_URL}/invoices/{invoice_id}/fire.json"
        data = {'event': 'deliver', 'message': message} if message else {'event': 'deliver'}
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def pay_invoice(self, invoice_id: str, paid_at: str, variable_symbol: str, amount: float) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/{self.slug}/invoices/{invoice_id}/fire.json" if self.slug else f"{self.BASE_URL}/invoices/{invoice_id}/fire.json"
        data = {
            'event': 'pay',
            'paid_at': paid_at,
            'variable_symbol': variable_symbol,
            'amount': amount
        }
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)