"""
Deel API Client - Global HR & Contractor Management Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class DeelError(Exception):
    """Base exception for Deel"""


class DeelClient:
    BASE_URL = "https://api.letsdeel.com/v2"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Deel client

        Args:
            api_key: Deel API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

        self.last_request_time = 0
        self.min_delay = 0.5

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise DeelError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise DeelError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    # Contracts
    def get_contracts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of contracts"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/contracts", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_contract(self, contract_id: str) -> Dict[str, Any]:
        """Get contract details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/contracts/{contract_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_contract(self, contract_data: Dict) -> Dict[str, Any]:
        """Create a contract"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/contracts", json=contract_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_contract(self, contract_id: str, contract_data: Dict) -> Dict[str, Any]:
        """Update contract"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/contracts/{contract_id}", json=contract_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Invoices
    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of invoices"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices/{invoice_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Contractors
    def get_contractors(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of contractors"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/contractors", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_contractor(self, contractor_id: str) -> Dict[str, Any]:
        """Get contractor details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/contractors/{contractor_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Clients
    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of clients"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/clients", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        """Create a client"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/clients", json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Off-cycle Payments
    def create_offcycle_payment(self, payment_data: Dict) -> Dict[str, Any]:
        """Create off-cycle payment"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/offcycle-payments", json=payment_data, timeout=self.timeout)
        return self._handle_response(resp)