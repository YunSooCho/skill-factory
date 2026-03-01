"""
Zoho Invoice API Client - Invoicing & Billing Platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ZohoInvoiceError(Exception):
    """Base exception for Zoho Invoice"""

class ZohoInvoiceRateLimitError(ZohoInvoiceError):
    """Rate limit exceeded"""

class ZohoInvoiceAuthenticationError(ZohoInvoiceError):
    """Authentication failed"""

class ZohoInvoiceClient:
    # Zoho Invoice has different domains for different data centers
    DOMAINS = {
        'us': 'https://www.zohoapis.com/invoice/v3',
        'eu': 'https://www.zohoapis.eu/invoice/v3',
        'in': 'https://www.zohoapis.in/invoice/v3',
        'au': 'https://www.zohoapis.com.au/invoice/v3',
        'jp': 'https://www.zohoapis.jp/invoice/v3',
        'ca': 'https://www.zohoapis.ca/invoice/v3',
        'cn': 'https://www.zohoapis.com.cn/invoice/v3',
        'sa': 'https://www.zohoapis.sa/invoice/v3',
    }

    def __init__(self, auth_token: str, organization_id: str, domain: str = 'us', timeout: int = 30):
        """
        Initialize Zoho Invoice client

        Args:
            auth_token: Zoho OAuth token (Zoho-oauthtoken <token>)
            organization_id: Organization ID from Zoho Invoice
            domain: Data center domain (us, eu, in, au, jp, ca, cn, sa)
            timeout: Request timeout in seconds
        """
        if domain not in self.DOMAINS:
            raise ValueError(f"Invalid domain. Must be one of: {list(self.DOMAINS.keys())}")

        self.base_url = self.DOMAINS[domain]
        self.auth_token = auth_token
        self.organization_id = organization_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Zoho-oauthtoken {auth_token}',
            'Content-Type': 'application/json'
        })

        # Rate limiting: 100 requests per minute
        self.min_delay = 0.6
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise ZohoInvoiceRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise ZohoInvoiceAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise ZohoInvoiceError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise ZohoInvoiceError(f"Error ({resp.status_code}): {resp.text}")

        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add organization_id to params"""
        if params is None:
            params = {}
        params['organization_id'] = self.organization_id
        return params

    # Organizations
    def get_organizations(self) -> Dict[str, Any]:
        """Get list of organizations"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/organizations", timeout=self.timeout)
        return self._handle_response(resp)

    def get_organization(self, organization_id: str) -> Dict[str, Any]:
        """Get organization details"""
        self._enforce_rate_limit()
        params = {'organization_id': organization_id}
        resp = self.session.get(f"{self.base_url}/organizations/{organization_id}", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Invoices
    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of invoices"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/invoices", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/invoices/{invoice_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """Create an invoice"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/invoices", params=self._get_params(), json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        """Update an invoice"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.base_url}/invoices/{invoice_id}", params=self._get_params(), json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Delete an invoice"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.base_url}/invoices/{invoice_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str, email_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Send invoice to customer"""
        self._enforce_rate_limit()
        data = email_data if email_data else {}
        resp = self.session.post(f"{self.base_url}/invoices/{invoice_id}/email", params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def mark_invoice_as_sent(self, invoice_id: str) -> Dict[str, Any]:
        """Mark invoice as sent"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/invoices/{invoice_id}/status/sent", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Customers / Contacts
    def get_contacts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of contacts/customers"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/contacts", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/contacts/{contact_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_contact(self, contact_data: Dict) -> Dict[str, Any]:
        """Create a contact"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/contacts", params=self._get_params(), json=contact_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_contact(self, contact_id: str, contact_data: Dict) -> Dict[str, Any]:
        """Update a contact"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.base_url}/contacts/{contact_id}", params=self._get_params(), json=contact_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Items
    def get_items(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of items"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/items", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_item(self, item_id: str) -> Dict[str, Any]:
        """Get item details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/items/{item_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_item(self, item_data: Dict) -> Dict[str, Any]:
        """Create an item"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/items", params=self._get_params(), json=item_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_item(self, item_id: str, item_data: Dict) -> Dict[str, Any]:
        """Update an item"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.base_url}/items/{item_id}", params=self._get_params(), json=item_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Estimates
    def get_estimates(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of estimates"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/estimates", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_estimate(self, estimate_id: str) -> Dict[str, Any]:
        """Get estimate details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/estimates/{estimate_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_estimate(self, estimate_data: Dict) -> Dict[str, Any]:
        """Create an estimate"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/estimates", params=self._get_params(), json=estimate_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_estimate(self, estimate_id: str, estimate_data: Dict) -> Dict[str, Any]:
        """Update an estimate"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.base_url}/estimates/{estimate_id}", params=self._get_params(), json=estimate_data, timeout=self.timeout)
        return self._handle_response(resp)

    def convert_estimate_to_invoice(self, estimate_id: str, invoice_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Convert estimate to invoice"""
        self._enforce_rate_limit()
        data = invoice_data if invoice_data else {}
        resp = self.session.post(f"{self.base_url}/estimates/{estimate_id}/converttoinvoice", params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Recurring Invoices
    def get_recurring_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of recurring invoices"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/recurringinvoices", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def create_recurring_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """Create a recurring invoice"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/recurringinvoices", params=self._get_params(), json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Payments
    def get_payments(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of payments received"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/customerpayments", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Get payment details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/customerpayments/{payment_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def record_payment(self, payment_data: Dict) -> Dict[str, Any]:
        """Record a payment received"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/customerpayments", params=self._get_params(), json=payment_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Expenses
    def get_expenses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of expenses"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/expenses", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def create_expense(self, expense_data: Dict) -> Dict[str, Any]:
        """Create an expense"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/expenses", params=self._get_params(), json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Expenses Recurring
    def get_recurring_expenses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of recurring expenses"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/recurringexpenses", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def create_recurring_expense(self, expense_data: Dict) -> Dict[str, Any]:
        """Create a recurring expense"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.base_url}/recurringexpenses", params=self._get_params(), json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Reports
    def get_reports(self) -> Dict[str, Any]:
        """Get available reports"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/reports", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice_report(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get invoice report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/reports/invoicesales", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_sales_report(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get sales report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.base_url}/reports/salesbyperson", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)