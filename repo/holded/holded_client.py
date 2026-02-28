"""
Holded API Client
API Documentation: https://developers.holded.com/reference/overview
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class HoldedAPIError(Exception):
    """Custom exception for Holded API errors."""
    pass


class HoldedClient:
    """Client for Holded API - CRM and ERP platform."""

    def __init__(self, api_key: str, base_url: str = "https://api.holded.com/api"):
        """
        Initialize Holded API client.

        Args:
            api_key: Your Holded API key
            base_url: API base URL (default: https://api.holded.com/api)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "key": api_key,
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
            raise HoldedAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise HoldedAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_contact(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        postalcode: Optional[str] = None,
        country: Optional[str] = None,
        type: str = "person",
        taxid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new contact (Create Contact).

        API Reference: https://developers.holded.com/reference/create-contact

        Args:
            name: Contact name
            email: Email address
            phone: Phone number
            mobile: Mobile phone number
            address: Street address
            city: City
            province: Province or state
            postalcode: Postal code
            country: Country code (e.g., ES, US)
            type: Type (person or company)
            taxid: Tax ID / VAT number

        Returns:
            Created contact information with ID
        """
        endpoint = "/invoicing/v1/contacts"

        data = {"name": name, "type": type}

        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if mobile:
            data["mobile"] = mobile
        if address:
            data["address"] = address
        if city:
            data["city"] = city
        if province:
            data["province"] = province
        if postalcode:
            data["postalcode"] = postalcode
        if country:
            data["country"] = country
        if taxid:
            data["taxid"] = taxid

        return self._make_request("POST", endpoint, json=data)

    def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        postalcode: Optional[str] = None,
        country: Optional[str] = None,
        taxid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing contact (Update Contact).

        API Reference: https://developers.holded.com/reference/update-contact

        Args:
            contact_id: Contact ID
            name: Contact name
            email: Email address
            phone: Phone number
            mobile: Mobile phone number
            address: Street address
            city: City
            province: Province or state
            postalcode: Postal code
            country: Country code
            taxid: Tax ID / VAT number

        Returns:
            Updated contact information
        """
        endpoint = f"/invoicing/v1/contacts/{contact_id}"

        data = {}

        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if mobile:
            data["mobile"] = mobile
        if address:
            data["address"] = address
        if city:
            data["city"] = city
        if province:
            data["province"] = province
        if postalcode:
            data["postalcode"] = postalcode
        if country:
            data["country"] = country
        if taxid:
            data["taxid"] = taxid

        return self._make_request("PUT", endpoint, json=data)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete a contact (Delete Contact).

        API Reference: https://developers.holded.com/reference/delete-contact

        Args:
            contact_id: Contact ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/invoicing/v1/contacts/{contact_id}"
        return self._make_request("DELETE", endpoint)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact details (Get Contact).

        API Reference: https://developers.holded.com/reference/get-contact

        Args:
            contact_id: Contact ID

        Returns:
            Contact details
        """
        endpoint = f"/invoicing/v1/contacts/{contact_id}"
        return self._make_request("GET", endpoint)

    def search_contacts(
        self,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search contacts (Search Contact).

        API Reference: https://developers.holded.com/reference/list-contacts

        Args:
            search: Search query (name, email, phone, etc.)
            limit: Maximum number of results (default: 20)
            offset: Offset for pagination (default: 0)

        Returns:
            List of matching contacts
        """
        endpoint = "/invoicing/v1/contacts"

        params = {}

        if search:
            params["search"] = search
        params["limit"] = str(limit)
        params["offset"] = str(offset)

        return self._make_request("GET", endpoint, params=params)

    def create_product(
        self,
        name: str,
        description: Optional[str] = None,
        sale_price: Optional[float] = None,
        cost: Optional[float] = None,
        tax_id: Optional[str] = None,
        stock: Optional[int] = None,
        sku: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new product (Create Product).

        API Reference: https://developers.holded.com/reference/create-product

        Args:
            name: Product name
            description: Product description
            sale_price: Sale price
            cost: Cost price
            tax_id: Tax ID (get from tax configuration)
            stock: Stock quantity
            sku: SKU code

        Returns:
            Created product information with ID
        """
        endpoint = "/invoicing/v1/products"

        data = {"name": name}

        if description:
            data["description"] = description
        if sale_price is not None:
            data["sale_price"] = sale_price
        if cost is not None:
            data["cost"] = cost
        if tax_id:
            data["tax_id"] = tax_id
        if stock is not None:
            data["stock"] = stock
        if sku:
            data["sku"] = sku

        return self._make_request("POST", endpoint, json=data)

    def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        sale_price: Optional[float] = None,
        cost: Optional[float] = None,
        tax_id: Optional[str] = None,
        stock: Optional[int] = None,
        sku: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing product (Update Product).

        API Reference: https://developers.holded.com/reference/update-product

        Args:
            product_id: Product ID
            name: Product name
            description: Product description
            sale_price: Sale price
            cost: Cost price
            tax_id: Tax ID
            stock: Stock quantity
            sku: SKU code

        Returns:
            Updated product information
        """
        endpoint = f"/invoicing/v1/products/{product_id}"

        data = {}

        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if sale_price is not None:
            data["sale_price"] = sale_price
        if cost is not None:
            data["cost"] = cost
        if tax_id:
            data["tax_id"] = tax_id
        if stock is not None:
            data["stock"] = stock
        if sku:
            data["sku"] = sku

        return self._make_request("PUT", endpoint, json=data)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get product details (Get Product).

        API Reference: https://developers.holded.com/reference/get-product

        Args:
            product_id: Product ID

        Returns:
            Product details
        """
        endpoint = f"/invoicing/v1/products/{product_id}"
        return self._make_request("GET", endpoint)

    def create_payment(
        self,
        invoice_id: str,
        amount: float,
        date: Optional[str] = None,
        notes: Optional[str] = None,
        method: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a payment (Create Payment).

        API Reference: https://developers.holded.com/reference/create-payment

        Args:
            invoice_id: Invoice ID
            amount: Payment amount
            date: Payment date (YYYY-MM-DD format, default: today)
            notes: Notes or description
            method: Payment method (cash, card, transfer, etc.)

        Returns:
            Created payment information with ID
        """
        endpoint = "/invoicing/v1/payments"

        data = {
            "invoiceid": invoice_id,
            "amount": amount
        }

        if date:
            data["date"] = date
        if notes:
            data["notes"] = notes
        if method:
            data["method"] = method

        return self._make_request("POST", endpoint, json=data)

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment details (Get Payment).

        API Reference: https://developers.holded.com/reference/get-payment

        Args:
            payment_id: Payment ID

        Returns:
            Payment details
        """
        endpoint = f"/invoicing/v1/payments/{payment_id}"
        return self._make_request("GET", endpoint)

    def search_payments(
        self,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search payments (Search Payment).

        API Reference: https://developers.holded.com/reference/list-payments

        Args:
            search: Search query
            limit: Maximum number of results (default: 20)
            offset: Offset for pagination (default: 0)

        Returns:
            List of matching payments
        """
        endpoint = "/invoicing/v1/payments"

        params = {}

        if search:
            params["search"] = search
        params["limit"] = str(limit)
        params["offset"] = str(offset)

        return self._make_request("GET", endpoint, params=params)