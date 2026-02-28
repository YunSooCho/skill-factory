"""
SmartBill API Client - Romanian Invoicing & Accounting Platform

SmartBill is a popular Romanian invoicing and accounting platform that provides
APIs for managing invoices, clients, products, and tax compliance.
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SmartBillError(Exception):
    """Base exception for SmartBill errors"""

class SmartBillRateLimitError(SmartBillError):
    """Rate limit exceeded"""

class SmartBillAuthenticationError(SmartBillError):
    """Authentication failed"""

class SmartBillClient:
    """
    Client for SmartBill REST API.
    API: https://www.smartbill.ro/API/v.2.0/
    """

    BASE_URL = "https://api.smartbill.ro/SB/api"

    def __init__(self, api_key: str, company_vat_code: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize SmartBill client.

        Args:
            api_key: SmartBill API key
            company_vat_code: VAT code of the company (for API access)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_vat_code = company_vat_code
        self.timeout = timeout
        self.session = requests.Session()
        # SmartBill uses Basic Auth with API key
        self.session.auth = (api_key, '')
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.min_delay = 0.3
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
            raise SmartBillRateLimitError("Rate limit exceeded")
        if resp.status_code == 401 or resp.status_code == 403:
            raise SmartBillAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise SmartBillError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise SmartBillError(f"Error ({resp.status_code}): {resp.text}")

        # SmartBill returns XML in some cases
        content_type = resp.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return resp.json()
        else:
            return {'data': resp.text, 'status': resp.status_code}

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of invoices.

        Args:
            params: Query parameters (dateStart, dateEnd, page, itemsPerPage, etc.)

        Returns:
            List of invoices
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura/list"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_number: str, series: str) -> Dict[str, Any]:
        """
        Get details of a specific invoice.

        Args:
            invoice_number: Invoice number
            series: Invoice series

        Returns:
            Invoice details
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura"
        params = {
            'cif': self.company_vat_code,
            'numar': invoice_number,
            'serie': series
        }
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """
        Create a new invoice.

        Args:
            invoice_data: Invoice data including client info, items, etc.

        Returns:
            Created invoice with number and issue date
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura"
        invoice_data['cif'] = self.company_vat_code
        resp = self.session.post(url, json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_number: str, series: str,
                      invoice_data: Dict) -> Dict[str, Any]:
        """
        Update an existing invoice.

        Args:
            invoice_number: Invoice number
            series: Invoice series
            invoice_data: Updated invoice data

        Returns:
            Updated invoice
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura"
        params = {
            'cif': self.company_vat_code,
            'numar': invoice_number,
            'serie': series
        }
        resp = self.session.put(url, json=invoice_data, params=params,
                               timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_number: str, series: str) -> Dict[str, Any]:
        """
        Delete an invoice.

        Args:
            invoice_number: Invoice number
            series: Invoice series

        Returns:
            Deletion confirmation
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura"
        params = {
            'cif': self.company_vat_code,
            'numar': invoice_number,
            'serie': series
        }
        resp = self.session.delete(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of clients.

        Args:
            params: Query parameters (page, itemsPerPage, search term)

        Returns:
            List of clients
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/client/list"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        """
        Create a new client.

        Args:
            client_data: Client data (name, vat code, address, etc.)

        Returns:
            Created client
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/client"
        client_data['cif'] = self.company_vat_code
        resp = self.session.post(url, json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_client(self, client_id: str, client_data: Dict) -> Dict[str, Any]:
        """
        Update an existing client.

        Args:
            client_id: Client ID
            client_data: Updated client data

        Returns:
            Updated client
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/client/{client_id}"
        resp = self.session.put(url, json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of products/services.

        Args:
            params: Query parameters (page, itemsPerPage, search term)

        Returns:
            List of products
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/produs/list"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_product(self, product_data: Dict) -> Dict[str, Any]:
        """
        Create a new product/service.

        Args:
            product_data: Product data (name, code, unit price, tax, etc.)

        Returns:
            Created product
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/produs"
        product_data['cif'] = self.company_vat_code
        resp = self.session.post(url, json=product_data, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice_email(self, invoice_number: str, series: str,
                          email: str, message: Optional[str] = None) -> Dict[str, Any]:
        """
        Send invoice to client via email.

        Args:
            invoice_number: Invoice number
            series: Invoice series
            email: Recipient email address
            message: Optional email message

        Returns:
            Email send confirmation
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura/sendemail"
        data = {
            'cif': self.company_vat_code,
            'numar': invoice_number,
            'serie': series,
            'email': email
        }
        if message:
            data['mesaj'] = message
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice_pdf(self, invoice_number: str, series: str) -> bytes:
        """
        Get invoice as PDF.

        Args:
            invoice_number: Invoice number
            series: Invoice series

        Returns:
            PDF file content as bytes
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/factura/pdf"
        params = {
            'cif': self.company_vat_code,
            'numar': invoice_number,
            'serie': series
        }
        resp = self.session.get(url, params=params, timeout=self.timeout)
        if resp.status_code >= 400:
            raise SmartBillError(f"Error ({resp.status_code}): {resp.text}")
        return resp.content

    def get_series(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get list of invoice series.

        Args:
            params: Query parameters

        Returns:
            List of invoice series
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/seriefactura/list"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)