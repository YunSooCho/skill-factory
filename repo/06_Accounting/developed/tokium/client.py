"""
Tokium API Client - Financial Management Platform

Tokium provides financial management APIs for invoicing, expenses,
and accounting operations.
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TokiumError(Exception):
    """Base exception for Tokium errors"""

class TokiumRateLimitError(TokiumError):
    """Rate limit exceeded"""

class TokiumAuthenticationError(TokiumError):
    """Authentication failed"""

class TokiumClient:
    """
    Client for Tokium REST API.
    """

    BASE_URL = "https://api.tokium.com/v1"

    def __init__(self, api_key: str, account_id: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize Tokium client.

        Args:
            api_key: Tokium API key
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
            raise TokiumRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise TokiumAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise TokiumError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise TokiumError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of invoices.

        Args:
            params: Query parameters (page, limit, status, dates)

        Returns:
            List of invoices
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices"
        if self.account_id:
            url = f"{url}?account_id={self.account_id}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Get details of a specific invoice.

        Args:
            invoice_id: Invoice ID

        Returns:
            Invoice details
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices/{invoice_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """
        Create a new invoice.

        Args:
            invoice_data: Invoice data including customer, items, etc.

        Returns:
            Created invoice
        """
        self._enforce_rate_limit()
        if self.account_id:
            invoice_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/invoices",
                                json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        """
        Update an existing invoice.

        Args:
            invoice_id: Invoice ID
            invoice_data: Updated invoice data

        Returns:
            Updated invoice
        """
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/invoices/{invoice_id}",
                               json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Delete an invoice.

        Args:
            invoice_id: Invoice ID

        Returns:
            Deletion confirmation
        """
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/invoices/{invoice_id}",
                                  timeout=self.timeout)
        return self._handle_response(resp)

    def get_customers(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of customers.

        Args:
            params: Query parameters (page, limit, search)

        Returns:
            List of customers
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/customers",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_customer(self, customer_data: Dict) -> Dict[str, Any]:
        """
        Create a new customer.

        Args:
            customer_data: Customer data

        Returns:
            Created customer
        """
        self._enforce_rate_limit()
        if self.account_id:
            customer_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/customers",
                                json=customer_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_expenses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of expenses.

        Args:
            params: Query parameters (page, limit, category, dates)

        Returns:
            List of expenses
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/expenses",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_expense(self, expense_data: Dict) -> Dict[str, Any]:
        """
        Create a new expense.

        Args:
            expense_data: Expense data

        Returns:
            Created expense
        """
        self._enforce_rate_limit()
        if self.account_id:
            expense_data['account_id'] = self.account_id
        resp = self.session.post(f"{self.BASE_URL}/expenses",
                                json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_accounts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of accounts.

        Args:
            params: Query parameters

        Returns:
            List of accounts
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/accounts",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice_email(self, invoice_id: str) -> Dict[str, Any]:
        """
        Send invoice via email.

        Args:
            invoice_id: Invoice ID

        Returns:
            Email send confirmation
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/invoices/{invoice_id}/send"
        resp = self.session.post(url, timeout=self.timeout)
        return self._handle_response(resp)