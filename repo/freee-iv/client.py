"""
Freee Invoice API Client - Japanese Invoice Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class FreeeIVError(Exception):
    """Base exception"""

class FreeeIVRateLimitError(FreeeIVError):
    """Rate limit"""

class FreeeIVAuthenticationError(FreeeIVError):
    """Auth failed"""

class FreeeIVClient:
    BASE_URL = "https://api.freee.co.jp"

    def __init__(self, access_token: str, company_id: Optional[str] = None, timeout: int = 30):
        self.access_token = access_token
        self.company_id = company_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
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
            raise FreeeIVRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise FreeeIVAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise FreeeIVError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise FreeeIVError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/api/1/deals"
        if params is None:
            params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.get(f"{self.BASE_URL}/api/1/deals/{invoice_id}", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        if self.company_id:
            invoice_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/api/1/deals", json={'deal': invoice_data}, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        if self.company_id:
            invoice_data['company_id'] = self.company_id
        resp = self.session.put(f"{self.BASE_URL}/api/1/deals/{invoice_id}", json={'deal': invoice_data}, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.delete(f"{self.BASE_URL}/api/1/deals/{invoice_id}", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_partners(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/api/1/partners"
        if params is None:
            params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_partner(self, partner_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        if self.company_id:
            partner_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/api/1/partners", json={'partner': partner_data}, timeout=self.timeout)
        return self._handle_response(resp)

    def get_items(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/api/1/items"
        if params is None:
            params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/api/1/deals/{invoice_id}/emails", json={}, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_companies(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/api/1/companies", timeout=self.timeout)
        return self._handle_response(resp)

    def get_wallet_txns(self, wallet_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/api/1/wallet_txns"
        if params is None:
            params = {}
        params['wallet_id'] = wallet_id
        if self.company_id:
            params['company_id'] = self.company_id
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_wallet_txn(self, txn_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        if self.company_id:
            txn_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/api/1/wallet_txns", json={'wallet_txn': txn_data}, timeout=self.timeout)
        return self._handle_response(resp)