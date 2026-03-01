"""
Fatture in Cloud API Client - Italian Invoice Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class FattureInCloudError(Exception):
    """Base exception"""

class FattureInCloudRateLimitError(FattureInCloudError):
    """Rate limit"""

class FattureInCloudAuthenticationError(FattureInCloudError):
    """Auth failed"""

class FattureInCloudClient:
    BASE_URL = "https://api-v2.fattureincloud.it"

    def __init__(self, access_token: str, company_id: Optional[str] = None, timeout: int = 30):
        self.access_token = access_token
        self.company_id = company_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
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
            raise FattureInCloudRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise FattureInCloudAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise FattureInCloudError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise FattureInCloudError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_user_companies(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/user/companies", timeout=self.timeout)
        return self._handle_response(resp)

    def set_company(self, company_id: str):
        self.company_id = company_id

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/c/{self.company_id}/issued_documents"
        if params is None:
            params = {'type': 'invoice'}
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, document_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/c/{self.company_id}/issued_documents/{document_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {
            'data': {
                'type': 'invoice',
                'entity': {
                    'type': 'issued_doc'
                },
                **invoice_data
            }
        }
        resp = self.session.post(f"{self.BASE_URL}/c/{self.company_id}/issued_documents", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, document_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {
            'data': {
                **invoice_data
            }
        }
        resp = self.session.put(f"{self.BASE_URL}/c/{self.company_id}/issued_documents/{document_id}", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, document_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/c/{self.company_id}/issued_documents/{document_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, document_id: str, sender_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {
            'data': {
                'sender_id': sender_id
            }
        }
        resp = self.session.post(f"{self.BASE_URL}/c/{self.company_id}/issued_documents/{document_id}/email", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/c/{self.company_id}/entities/clients"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {'data': client_data}
        resp = self.session.post(f"{self.BASE_URL}/c/{self.company_id}/entities/clients", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/c/{self.company_id}/products"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_product(self, product_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {'data': product_data}
        resp = self.session.post(f"{self.BASE_URL}/c/{self.company_id}/products", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_received_documents(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/c/{self.company_id}/received_documents"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_received_document(self, document_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data = {'data': document_data}
        resp = self.session.post(f"{self.BASE_URL}/c/{self.company_id}/received_documents", json=data, timeout=self.timeout)
        return self._handle_response(resp)