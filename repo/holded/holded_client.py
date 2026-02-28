"""
Holded API Client
Business management platform with CRM, billing, and inventory features

API Documentation: https://developers.holded.com/
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class HoldedAPIError(Exception):
    """Custom exception for Holded API errors"""
    pass


class HoldedRateLimitError(HoldedAPIError):
    """Rate limit exceeded error"""
    pass


class HoldedClient:
    """
    Holded REST API Client
    Supports contacts, products, and payments management
    """

    def __init__(self, api_key: str, api_url: str = "https://api.holded.com/api", timeout: int = 30):
        """
        Initialize Holded API client

        Args:
            api_key: API key for authentication
            api_url: Base URL of Holded API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'key': api_key
        })
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        # Rate limiting
        current_time = time.time()

        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            time.sleep(1)

        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise HoldedAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('error', error_data.get('message', response.text))
                raise HoldedAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise HoldedAPIError(f"Request failed: {str(e)}")

    # ========== CONTACT METHODS ==========

    def create_contact(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            name: Contact name
            **kwargs: Additional contact fields (email, phone, billingInfo, etc.)

        Returns:
            Created contact data

        Example:
            client.create_contact(
                name="John Doe",
                email="john@example.com",
                phone="+1234567890",
                billingInfo={"address": "123 Main St"}
            )
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/invoicing/v1/contacts', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact by ID

        Args:
            contact_id: Contact ID

        Returns:
            Contact data
        """
        return self._make_request('GET', f'/invoicing/v1/contacts/{contact_id}')

    def update_contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update contact

        Args:
            contact_id: Contact ID
            **kwargs: Fields to update

        Returns:
            Updated contact data
        """
        return self._make_request('PUT', f'/invoicing/v1/contacts/{contact_id}', data=kwargs)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete contact

        Args:
            contact_id: Contact ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/invoicing/v1/contacts/{contact_id}')

    def search_contact(self, query: Optional[str] = None, **filter_params) -> Dict[str, Any]:
        """
        Search contacts

        Args:
            query: Search query string
            **filter_params: Filter parameters (name, email, phone, etc.)

        Returns:
            List of contacts
        """
        params = {}
        if query:
            params['name'] = query
        params.update(filter_params)

        return self._make_request('GET', '/invoicing/v1/contacts', params=params)

    # ========== PRODUCT METHODS ==========

    def create_product(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new product

        Args:
            name: Product name
            **kwargs: Additional product fields (description, price, stock, etc.)

        Returns:
            Created product data

        Example:
            client.create_product(
                name="Widget",
                description="A useful widget",
                price=99.99,
                stock=100,
                tax=21
            )
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/products/v1/products', data=data)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get product by ID

        Args:
            product_id: Product ID

        Returns:
            Product data
        """
        return self._make_request('GET', f'/products/v1/products/{product_id}')

    def update_product(self, product_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update product

        Args:
            product_id: Product ID
            **kwargs: Fields to update

        Returns:
            Updated product data
        """
        return self._make_request('PUT', f'/products/v1/products/{product_id}', data=kwargs)

    # ========== PAYMENT METHODS ==========

    def create_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        """
        Create a new payment

        Args:
            amount: Payment amount
            **kwargs: Additional payment fields (date, method, contact_id, etc.)

        Returns:
            Created payment data

        Example:
            client.create_payment(
                amount=1000.00,
                date="2025-03-01",
                method="transfer",
                contact_id="contact_123"
            )
        """
        data = {'amount': amount, **kwargs}
        return self._make_request('POST', '/invoicing/v1/payments', data=data)

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment by ID

        Args:
            payment_id: Payment ID

        Returns:
            Payment data
        """
        return self._make_request('GET', f'/invoicing/v1/payments/{payment_id}')

    def search_payment(self, query: Optional[str] = None, **filter_params) -> Dict[str, Any]:
        """
        Search payments

        Args:
            query: Search query
            **filter_params: Filter parameters

        Returns:
            List of payments
        """
        params = {}
        if query:
            params['contact'] = query
        params.update(filter_params)

        return self._make_request('GET', '/invoicing/v1/payments', params=params)


if __name__ == '__main__':
    import os

    API_KEY = os.getenv('HOLDED_API_KEY', 'your_api_key')

    client = HoldedClient(api_key=API_KEY)

    try:
        # Example: Create a contact
        contact = client.create_contact(
            name="Acme Corporation",
            email="contact@acme.com",
            phone="+1234567890"
        )
        print(f"Created contact: {contact}")

        # Example: Create a product
        product = client.create_product(
            name="Product A",
            description="Description A",
            price=99.99,
            stock=50
        )
        print(f"Created product: {product}")

        # Example: Create a payment
        payment = client.create_payment(
            amount=500.00,
            date="2025-03-01",
            method="transfer"
        )
        print(f"Created payment: {payment}")

        # Example: Search contacts
        contacts = client.search_contact(name="Acme")
        print(f"Search results: {contacts}")

    except HoldedAPIError as e:
        print(f"Error: {e}")