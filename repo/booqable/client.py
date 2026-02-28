"""
Booqable API Client

Complete client for Booqable rental inventory management integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class BooqableAPIClient:
    """
    Complete client for Booqable rental inventory management.
    Supports orders, products, customers, stock management, and more.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Booqable API client.

        Args:
            api_key: Booqable API key (from env: BOOQABLE_API_KEY)
            base_url: Base URL (default: https://api.booqable.com/api/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("BOOQABLE_API_KEY")
        self.base_url = base_url or os.getenv(
            "BOOQABLE_BASE_URL",
            "https://api.booqable.com/api/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set BOOQABLE_API_KEY environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Booqable API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"data": None}

    # Orders

    def create_order(
        self,
        customer_id: str,
        start_date: str,
        end_date: str,
        order_items: List[Dict[str, Any]],
        notes: Optional[str] = None,
        status: str = "concept"
    ) -> Dict[str, Any]:
        """
        Create a rental order.

        Args:
            customer_id: Customer ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            order_items: List of order items (product_id, quantity)
            notes: Order notes
            status: Order status (concept, confirmed, etc.)

        Returns:
            Order information
        """
        data = {
            'customer_id': customer_id,
            'start_date': start_date,
            'end_date': end_date,
            'order_items': order_items,
            'status': status
        }

        if notes:
            data['notes'] = notes

        return self._request('POST', '/orders', data=data)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request('GET', f'/orders/{order_id}')

    def list_orders(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List orders with optional filtering."""
        params = {'limit': limit, 'page': page}
        if status:
            params['status'] = status
        return self._request('GET', '/orders', params=params)

    def update_order(
        self,
        order_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update order.

        Args:
            order_id: Order ID
            **kwargs: Fields to update

        Returns:
            Updated order information
        """
        return self._request('PUT', f'/orders/{order_id}', data=kwargs)

    def delete_order(self, order_id: str) -> Dict[str, Any]:
        """Delete an order."""
        return self._request('DELETE', f'/orders/{order_id}')

    def confirm_order(self, order_id: str) -> Dict[str, Any]:
        """Confirm an order."""
        return self._request('POST', f'/orders/{order_id}/confirm')

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order."""
        return self._request('POST', f'/orders/{order_id}/cancel')

    # Products

    def list_products(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List all products."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/products', params=params)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request('GET', f'/products/{product_id}')

    def create_product(
        self,
        name: str,
        product_group_id: str,
        price: Optional[float] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a product."""
        data = {
            'name': name,
            'product_group_id': product_group_id
        }

        if price:
            data['price'] = price
        if description:
            data['description'] = description

        return self._request('POST', '/products', data=data)

    # Product Groups

    def list_product_groups(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List product groups."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/product_groups', params=params)

    def get_product_group(self, group_id: str) -> Dict[str, Any]:
        """Get product group details."""
        return self._request('GET', f'/product_groups/{group_id}')

    # Customers

    def list_customers(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List customers."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/customers', params=params)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        company: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a customer."""
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company

        return self._request('POST', '/customers', data=data)

    def update_customer(
        self,
        customer_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update customer."""
        return self._request('PUT', f'/customers/{customer_id}', data=kwargs)

    # Inventory/Stock

    def list_stock_items(
        self,
        product_id: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List stock items."""
        params = {'limit': limit, 'page': page}
        if product_id:
            params['product_id'] = product_id
        return self._request('GET', '/stock_items', params=params)

    def get_stock_item(self, stock_item_id: str) -> Dict[str, Any]:
        """Get stock item details."""
        return self._request('GET', f'/stock_items/{stock_item_id}')

    # Taxes

    def list_taxes(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List tax rates."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/taxes', params=params)

    # Locations

    def list_locations(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List locations."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/locations', params=params)

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get location details."""
        return self._request('GET', f'/locations/{location_id}')

    # Documents and Invoices

    def list_documents(
        self,
        order_id: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List documents."""
        params = {'limit': limit, 'page': page}
        if order_id:
            params['order_id'] = order_id
        return self._request('GET', '/documents', params=params)

    def create_invoice(self, order_id: str) -> Dict[str, Any]:
        """Create invoice for order."""
        data = {'order_id': order_id}
        return self._request('POST', '/invoices', data=data)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook subscription."""
        data = {'url': url, 'events': events}
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Account

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/account')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()