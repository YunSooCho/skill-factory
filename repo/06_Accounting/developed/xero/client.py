"""
Xero API Client - Cloud Accounting Platform

Xero is a leading cloud-based accounting platform that provides comprehensive
APIs for managing invoices, contacts, bank transactions, reports, and more.
"""

import requests
import time
import uuid
from typing import Optional, Dict, Any, List


class XeroError(Exception):
    """Base exception for Xero errors"""

class XeroRateLimitError(XeroError):
    """Rate limit exceeded"""

class XeroAuthenticationError(XeroError):
    """Authentication failed"""

class XeroClient:
    """
    Client for Xero REST API v2.0.
    API: https://developer.xero.com/documentation/api/accounting-and-tax/overview
    """

    BASE_URL = "https://api.xero.com/api.xro/2.0"

    def __init__(self, client_id: str, client_secret: str, tenant_id: str,
                 access_token: Optional[str] = None, timeout: int = 30):
        """
        Initialize Xero client.

        Args:
            client_id: OAuth 2.0 client ID
            client_secret: OAuth 2.0 client secret
            tenant_id: Xero tenant ID (organization)
            access_token: OAuth 2.0 access token (optional)
            timeout: Request timeout in seconds
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Xero-Tenant-Id': tenant_id
        })
        if access_token:
            self.session.headers['Authorization'] = f'Bearer {access_token}'
        self.min_delay = 0.5
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
            raise XeroRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise XeroAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise XeroError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise XeroError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of invoices.

        Args:
            params: Query parameters (IDs, Status, Page, etc.)

        Returns:
            List of invoices
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Invoices",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get details of a specific invoice.

        Args:
            invoice_id: Invoice ID (GUID)
            params: Additional query parameters (UnitDP)

        Returns:
            Invoice details
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Invoices/{invoice_id}",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """
        Create a new invoice.

        Args:
            invoice_data: Invoice data including type, contact, line items, etc.

        Returns:
            Created invoice
        """
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/Invoices",
                               json={'Invoices': [invoice_data]},
                               timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        """
        Update an existing invoice.

        Args:
            invoice_id: Invoice ID (GUID)
            invoice_data: Updated invoice data

        Returns:
            Updated invoice
        """
        self._enforce_rate_limit()
        invoice_data['InvoiceID'] = invoice_id
        resp = self.session.post(f"{self.BASE_URL}/Invoices",
                                json={'Invoices': [invoice_data]},
                                timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Delete an invoice.

        Args:
            invoice_id: Invoice ID (GUID)

        Returns:
            Deletion confirmation
        """
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/Invoices/{invoice_id}",
                                  timeout=self.timeout)
        return self._handle_response(resp)

    def get_contacts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of contacts (customers and suppliers).

        Args:
            params: Query parameters (IDs, Where, Order, Page)

        Returns:
            List of contacts
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Contacts",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get details of a specific contact.

        Args:
            contact_id: Contact ID (GUID)

        Returns:
            Contact details
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Contacts/{contact_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def create_contact(self, contact_data: Dict) -> Dict[str, Any]:
        """
        Create a new contact.

        Args:
            contact_data: Contact data (name, email, phone number, addresses)

        Returns:
            Created contact
        """
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/Contacts",
                               json={'Contacts': [contact_data]},
                               timeout=self.timeout)
        return self._handle_response(resp)

    def update_contact(self, contact_id: str, contact_data: Dict) -> Dict[str, Any]:
        """
        Update an existing contact.

        Args:
            contact_id: Contact ID (GUID)
            contact_data: Updated contact data

        Returns:
            Updated contact
        """
        self._enforce_rate_limit()
        contact_data['ContactID'] = contact_id
        resp = self.session.post(f"{self.BASE_URL}/Contacts",
                                json={'Contacts': [contact_data]},
                                timeout=self.timeout)
        return self._handle_response(resp)

    def get_accounts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of accounts from the chart of accounts.

        Args:
            params: Query parameters (IDs, Where, Order, Page)

        Returns:
            List of accounts
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Accounts",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_bank_transactions(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of bank transactions.

        Args:
            params: Query parameters (Where, Order, Page)

        Returns:
            List of bank transactions
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/BankTransactions",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_bank_transaction(self, transaction_data: Dict) -> Dict[str, Any]:
        """
        Create a bank transaction (spend or receive).

        Args:
            transaction_data: Transaction data (type, contact, line items, bank account)

        Returns:
            Created transaction
        """
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/BankTransactions",
                               json={'BankTransactions': [transaction_data]},
                               timeout=self.timeout)
        return self._handle_response(resp)

    def get_items(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of items (products and services).

        Args:
            params: Query parameters (IDs, Where, Order, Page)

        Returns:
            List of items
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Items",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_item(self, item_data: Dict) -> Dict[str, Any]:
        """
        Create a new item.

        Args:
            item_data: Item data (code, description, purchase/sales details)

        Returns:
            Created item
        """
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/Items",
                               json={'Items': [item_data]},
                               timeout=self.timeout)
        return self._handle_response(resp)

    def get_tracking_categories(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get tracking categories for cost center tracking.

        Args:
            params: Query parameters

        Returns:
            List of tracking categories
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/TrackingCategories",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_reports(self, report_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get financial reports.

        Args:
            report_id: Report ID (e.g., BalanceSheet, ProfitAndLoss)
            params: Query parameters (Date, Periods, etc.)

        Returns:
            Report data
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/Reports/{report_id}",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_organisations(self) -> Dict[str, Any]:
        """
        Get list of organizations the user has access to.

        Returns:
            List of organizations
        """
        if not self.access_token:
            raise XeroAuthenticationError("Access token required")
        self._enforce_rate_limit()
        resp = self.session.get("https://api.xero.com/connections",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def email_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Email an invoice to the customer.

        Args:
            invoice_id: Invoice ID (GUID)

        Returns:
            Email send confirmation
        """
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/Invoices/{invoice_id}/Email",
                                timeout=self.timeout)
        return self._handle_response(resp)