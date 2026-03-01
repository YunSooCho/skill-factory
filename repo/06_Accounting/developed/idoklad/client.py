"""
iDoklad API Client - Czech Accounting System
"""

import requests
import time
from typing import Optional, Dict, Any, List


class IdokladError(Exception):
    """Base exception"""

class IdokladRateLimitError(IdokladError):
    """Rate limit"""

class IdokladAuthenticationError(IdokladError):
    """Auth failed"""

class IdokladClient:
    BASE_URL = "https://app.idoklad.cz/development/v3"

    def __init__(self, client_id: str, client_secret: str, refresh_token: Optional[str] = None, timeout: int = 30):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.2
        self.last_request_time = 0

        if refresh_token:
            self._refresh_access_token()

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise IdokladRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise IdokladAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise IdokladError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise IdokladError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def _refresh_access_token(self) -> Dict[str, Any]:
        url = "https://app.idoklad.cz/identity/connect/token"
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        resp = requests.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        self.access_token = result.get('access_token')
        self.refresh_token = result.get('refresh_token', self.refresh_token)
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}'
        })
        return result

    def get_issued_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/IssuedInvoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_issued_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/IssuedInvoices/{invoice_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_issued_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/IssuedInvoices", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_issued_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.patch(f"{self.BASE_URL}/IssuedInvoices/{invoice_id}", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_issued_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/IssuedInvoices/{invoice_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_contacts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/Contacts"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Contacts/{contact_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_contact(self, contact_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/Contacts", json=contact_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_received_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/ReceivedInvoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_received_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/ReceivedInvoices", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_bank_accounts(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/BankAccounts", timeout=self.timeout)
        return self._handle_response(resp)

    def get_bank_movements(self, account_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/BankAccounts/{account_id}/BankMovements"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice_by_email(self, invoice_id: str, email_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/IssuedInvoices/{invoice_id}/SendByEmail", json=email_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_my_company(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/MyCompany", timeout=self.timeout)
        return self._handle_response(resp)