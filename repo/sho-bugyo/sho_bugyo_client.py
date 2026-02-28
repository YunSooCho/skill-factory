"""
Sho Bugyo API Client
API Documentation: https://www.sho-bugyo.com/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class ShoBugyoAPIError(Exception):
    """Custom exception for Sho Bugyo API errors."""
    pass


class ShoBugyoClient:
    """Client for Sho Bugyo (商簿君) API - Japanese accounting and sales system."""

    def __init__(self, api_key: str, company_id: str, base_url: str = "https://api.sho-bugyo.com/v1"):
        """
        Initialize Sho Bugyo API client.

        Args:
            api_key: Your Sho Bugyo API key
            company_id: Your company ID
            base_url: API base URL (default: https://api.sho-bugyo.com/v1)
        """
        self.api_key = api_key
        self.company_id = company_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "X-Company-ID": company_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise ShoBugyoAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise ShoBugyoAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_estimate(
        self,
        customer_code: str,
        issue_date: str,
        items: List[Dict[str, Any]],
        estimate_number: Optional[str] = None,
        expiration_date: Optional[str] = None,
        remarks: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register an estimate (見積書情報を登録).

        API Reference: Estimates endpoint

        Args:
            customer_code: Customer code (得意先コード)
            issue_date: Issue date (YYYY-MM-DD format)
            items: List of items with following structure:
                [
                    {
                        "item_code": "ITEM001",
                        "item_name": "商品名",
                        "quantity": 10,
                        "unit_price": 1000,
                        "tax_type": "01"  # 01: included, 02: excluded
                    },
                    ...
                ]
            estimate_number: Estimate number (optional, system generates if not provided)
            expiration_date: Expiration date (YYYY-MM-DD format)
            remarks: Remarks or notes

        Returns:
            Created estimate information with estimate number
        """
        endpoint = "/estimates"

        data = {
            "customerCode": customer_code,
            "issueDate": issue_date,
            "items": items
        }

        if estimate_number:
            data["estimateNumber"] = estimate_number
        if expiration_date:
            data["expirationDate"] = expiration_date
        if remarks:
            data["remarks"] = remarks

        return self._make_request("POST", endpoint, json=data)

    def create_sales_order(
        self,
        customer_code: str,
        issue_date: str,
        items: List[Dict[str, Any]],
        order_number: Optional[str] = None,
        delivery_date: Optional[str] = None,
        remarks: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a sales order (受注伝票を登録).

        API Reference: Sales orders endpoint

        Args:
            customer_code: Customer code (得意先コード)
            issue_date: Issue date (YYYY-MM-DD format)
            items: List of items with following structure:
                [
                    {
                        "item_code": "ITEM001",
                        "item_name": "商品名",
                        "quantity": 10,
                        "unit_price": 1000,
                        "tax_type": "01"
                    },
                    ...
                ]
            order_number: Order number (optional, system generates if not provided)
            delivery_date: Delivery date (YYYY-MM-DD format)
            remarks: Remarks or notes

        Returns:
            Created sales order information with order number
        """
        endpoint = "/sales-orders"

        data = {
            "customerCode": customer_code,
            "issueDate": issue_date,
            "items": items
        }

        if order_number:
            data["orderNumber"] = order_number
        if delivery_date:
            data["deliveryDate"] = delivery_date
        if remarks:
            data["remarks"] = remarks

        return self._make_request("POST", endpoint, json=data)

    def get_sales_order(self, order_number: str) -> Dict[str, Any]:
        """
        Get sales order information (受注伝票情報を取得).

        API Reference: Sales orders GET endpoint

        Args:
            order_number: Sales order number

        Returns:
            Sales order details including:
            - orderNumber: Order number
            - customerCode: Customer code
            - issueDate: Issue date
            - items: Order items
            - totalAmount: Total amount including tax
            - status: Order status
        """
        endpoint = f"/sales-orders/{order_number}"
        return self._make_request("GET", endpoint)

    def search_sales_orders(
        self,
        customer_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search sales orders (受注伝票を検索).

        API Reference: Sales orders search endpoint

        Args:
            customer_code: Filter by customer code
            start_date: Filter orders from this date (YYYY-MM-DD)
            end_date: Filter orders until this date (YYYY-MM-DD)
            status: Filter by status (01: draft, 02: confirmed, 03: shipped, 04: canceled)
            limit: Maximum number of results (default: 20)

        Returns:
            List of matching sales orders
        """
        endpoint = "/sales-orders"

        params = {"limit": str(limit)}

        if customer_code:
            params["customerCode"] = customer_code
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if status:
            params["status"] = status

        return self._make_request("GET", endpoint, params=params)

    def create_sales_invoice(
        self,
        customer_code: str,
        issue_date: str,
        items: List[Dict[str, Any]],
        invoice_number: Optional[str] = None,
        due_date: Optional[str] = None,
        remarks: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a sales invoice (売上伝票を登録).

        API Reference: Sales invoices endpoint

        Args:
            customer_code: Customer code
            issue_date: Issue date (YYYY-MM-DD format)
            items: List of items with quantity and unit price
            invoice_number: Invoice number (optional, system generates if not provided)
            due_date: Due date for payment (YYYY-MM-DD format)
            remarks: Remarks or notes

        Returns:
            Created sales invoice information with invoice number
        """
        endpoint = "/sales-invoices"

        data = {
            "customerCode": customer_code,
            "issueDate": issue_date,
            "items": items
        }

        if invoice_number:
            data["invoiceNumber"] = invoice_number
        if due_date:
            data["dueDate"] = due_date
        if remarks:
            data["remarks"] = remarks

        return self._make_request("POST", endpoint, json=data)

    def get_sales_invoice(self, invoice_number: str) -> Dict[str, Any]:
        """
        Get sales invoice information (売上伝票情報を取得).

        API Reference: Sales invoices GET endpoint

        Args:
            invoice_number: Sales invoice number

        Returns:
            Sales invoice details including items and totals
        """
        endpoint = f"/sales-invoices/{invoice_number}"
        return self._make_request("GET", endpoint)

    def create_or_update_customer(
        self,
        customer_code: str,
        customer_name: str,
        postal_code: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        payment_terms: Optional[str] = None,
        tax_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update customer (得意先を登録・更新).

        API Reference: Customers endpoint

        Args:
            customer_code: Unique customer code
            customer_name: Customer name
            postal_code: Postal code (XXX-XXXX format)
            address: Address
            phone: Phone number
            email: Email address
            payment_terms: Payment terms code
            tax_type: Tax type (01: included, 02: excluded)

        Returns:
            Created or updated customer information
        """
        endpoint = "/customers"

        data = {
            "customerCode": customer_code,
            "customerName": customer_name
        }

        if postal_code:
            data["postalCode"] = postal_code
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if payment_terms:
            data["paymentTerms"] = payment_terms
        if tax_type:
            data["taxType"] = tax_type

        return self._make_request("POST", endpoint, json=data)

    def search_customers(
        self,
        customer_name: Optional[str] = None,
        customer_code: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search customers (得意先を検索).

        API Reference: Customers search endpoint

        Args:
            customer_name: Filter by customer name (partial match)
            customer_code: Filter by customer code
            limit: Maximum number of results (default: 20)

        Returns:
            List of matching customers
        """
        endpoint = "/customers"

        params = {"limit": str(limit)}

        if customer_name:
            params["customerName"] = customer_name
        if customer_code:
            params["customerCode"] = customer_code

        return self._make_request("GET", endpoint, params=params)

    def create_or_update_product(
        self,
        item_code: str,
        item_name: str,
        sales_price: Optional[int] = None,
        purchase_price: Optional[int] = None,
        tax_type: Optional[str] = "01",
        unit: Optional[str] = None,
        unit_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update product (商品を登録・更新).

        API Reference: Products endpoint

        Args:
            item_code: Unique item code
            item_name: Item name
            sales_price: Sales unit price
            purchase_price: Purchase unit price
            tax_type: Tax type (01: included, 02: excluded)
            unit: Unit code
            unit_name: Unit name (個, 枚, 箱, etc.)

        Returns:
            Created or updated product information
        """
        endpoint = "/products"

        data = {
            "itemCode": item_code,
            "itemName": item_name
        }

        if sales_price is not None:
            data["salesPrice"] = sales_price
        if purchase_price is not None:
            data["purchasePrice"] = purchase_price
        if tax_type:
            data["taxType"] = tax_type
        if unit:
            data["unit"] = unit
        if unit_name:
            data["unitName"] = unit_name

        return self._make_request("POST", endpoint, json=data)

    def search_products(
        self,
        item_name: Optional[str] = None,
        item_code: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search products (商品を検索).

        API Reference: Products search endpoint

        Args:
            item_name: Filter by item name (partial match)
            item_code: Filter by item code
            limit: Maximum number of results (default: 20)

        Returns:
            List of matching products
        """
        endpoint = "/products"

        params = {"limit": str(limit)}

        if item_name:
            params["itemName"] = item_name
        if item_code:
            params["itemCode"] = item_code

        return self._make_request("GET", endpoint, params=params)