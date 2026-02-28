"""
UpBooks API Client - Cloud Accounting Platform

UpBooks is a cloud accounting platform providing APIs for invoicing,
expenses, billing, and financial reporting.
"""

import requests
import time
from typing import Optional, Dict, Any, List


class UpBooksError(Exception):
    """Base exception for UpBooks errors"""

class UpBooksRateLimitError(UpBooksError):
    """Rate limit exceeded"""

class UpBooksAuthenticationError(UpBooksError):
    """Authentication failed"""

class UpBooksClient:
    """
    Client for UpBooks REST API.
    """

    BASE_URL = "https://api.upbooks.com/v3"

    def __init__(self, api_key: str, company_id: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize UpBooks client.

        Args:
            api_key: UpBooks API key
            company_id: Company ID (optional)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_id = company_id
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
            raise UpBooksRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise UpBooksAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise UpBooksError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise UpBooksError(f"Error ({resp.status_code}): {resp.text}")
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
        if self.company_id:
            invoice_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/invoices",
                                json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        """Update an existing invoice."""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/invoices/{invoice_id}",
                               json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Delete an invoice."""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/invoices/{invoice_id}",
                                  timeout=self.timeout)
        return self._handle_response(resp)

    def get_vendors(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of vendors."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/vendors",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_vendor(self, vendor_data: Dict) -> Dict[str, Any]:
        """Create a new vendor."""
        self._enforce_rate_limit()
        if self.company_id:
            vendor_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/vendors",
                                json=vendor_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_expenses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of expenses."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/expenses",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_expense(self, expense_data: Dict) -> Dict[str, Any]:
        """Create a new expense."""
        self._enforce_rate_limit()
        if self.company_id:
            expense_data['company_id'] = self.company_id
        resp = self.session.post(f"{self.BASE_URL}/expenses",
                                json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_reports(self, report_type: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get financial reports."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports/{report_type}",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_ledger_entries(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get ledger entries."""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/ledger",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)