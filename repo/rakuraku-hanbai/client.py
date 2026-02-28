"""
Rakuraku Hanbai API Client

This module provides a Python client for interacting with Rakuraku Hanbai sales platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class RakurakuHanbaiClient:
    """
    Client for Rakuraku Hanbai Sales Platform.

    Rakuraku Hanbai provides:
    - Customer management
    - Sales opportunity tracking
    - Quote management
    - Order management
    - Sales analytics
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.rakuraku-hanbai.jp/v1",
        timeout: int = 30
    ):
        """
        Initialize the Rakuraku Hanbai client.

        Args:
            api_key: Rakuraku Hanbai API key
            base_url: Base URL for the Rakuraku Hanbai API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        json_data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")

        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_customers(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all customers."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if status:
            params['status'] = status

        return self._request('GET', '/customers', params=params)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        company_name: Optional[str] = None,
        status: str = "active",
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new customer."""
        data = {
            'name': name,
            'status': status
        }

        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if company_name:
            data['company_name'] = company_name
        if notes:
            data['notes'] = notes

        return self._request('POST', '/customers', json_data=data)

    def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        company_name: Optional[str] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update customer details."""
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if company_name:
            data['company_name'] = company_name
        if status:
            data['status'] = status
        if notes:
            data['notes'] = notes

        return self._request('PUT', f'/customers/{customer_id}', json_data=data)

    def delete_customer(self, customer_id: str) -> Dict[str, Any]:
        """Delete a customer."""
        return self._request('DELETE', f'/customers/{customer_id}')

    def get_deals(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        customer_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all sales deals/opportunities."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if status:
            params['status'] = status
        if customer_id:
            params['customer_id'] = customer_id

        return self._request('GET', '/deals', params=params)

    def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """Get deal details."""
        return self._request('GET', f'/deals/{deal_id}')

    def create_deal(
        self,
        title: str,
        customer_id: str,
        amount: float,
        stage: str = "prospect",
        probability: int = 50,
        expected_close_date: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new sales deal."""
        data = {
            'title': title,
            'customer_id': customer_id,
            'amount': amount,
            'stage': stage,
            'probability': probability
        }

        if expected_close_date:
            data['expected_close_date'] = expected_close_date
        if description:
            data['description'] = description

        return self._request('POST', '/deals', json_data=data)

    def update_deal(
        self,
        deal_id: str,
        title: Optional[str] = None,
        amount: Optional[float] = None,
        stage: Optional[str] = None,
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update deal details."""
        data = {}
        if title:
            data['title'] = title
        if amount:
            data['amount'] = amount
        if stage:
            data['stage'] = stage
        if probability:
            data['probability'] = probability
        if expected_close_date:
            data['expected_close_date'] = expected_close_date
        if description:
            data['description'] = description

        return self._request('PUT', f'/deals/{deal_id}', json_data=data)

    def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """Delete a deal."""
        return self._request('DELETE', f'/deals/{deal_id}')

    def get_quotes(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        deal_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all quotes."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if status:
            params['status'] = status
        if deal_id:
            params['deal_id'] = deal_id

        return self._request('GET', '/quotes', params=params)

    def get_quote(self, quote_id: str) -> Dict[str, Any]:
        """Get quote details."""
        return self._request('GET', f'/quotes/{quote_id}')

    def create_quote(
        self,
        customer_id: str,
        title: str,
        valid_until: str,
        items: List[Dict[str, Any]],
        discount: float = 0,
        tax_rate: float = 0.1,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new quote."""
        data = {
            'customer_id': customer_id,
            'title': title,
            'valid_until': valid_until,
            'items': items,
            'discount': discount,
            'tax_rate': tax_rate
        }

        if notes:
            data['notes'] = notes

        return self._request('POST', '/quotes', json_data=data)

    def update_quote(
        self,
        quote_id: str,
        status: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None,
        discount: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update quote details."""
        data = {}
        if status:
            data['status'] = status
        if items:
            data['items'] = items
        if discount:
            data['discount'] = discount
        if notes:
            data['notes'] = notes

        return self._request('PUT', f'/quotes/{quote_id}', json_data=data)

    def delete_quote(self, quote_id: str) -> Dict[str, Any]:
        """Delete a quote."""
        return self._request('DELETE', f'/quotes/{quote_id}')

    def get_orders(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        customer_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all orders."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if status:
            params['status'] = status
        if customer_id:
            params['customer_id'] = customer_id

        return self._request('GET', '/orders', params=params)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request('GET', f'/orders/{order_id}')

    def create_order(
        self,
        customer_id: str,
        items: List[Dict[str, Any]],
        shipping_address: str,
        payment_method: str = "bank_transfer",
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new order."""
        data = {
            'customer_id': customer_id,
            'items': items,
            'shipping_address': shipping_address,
            'payment_method': payment_method
        }

        if notes:
            data['notes'] = notes

        return self._request('POST', '/orders', json_data=data)

    def update_order(
        self,
        order_id: str,
        status: Optional[str] = None,
        shipping_address: Optional[str] = None,
        payment_status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update order details."""
        data = {}
        if status:
            data['status'] = status
        if shipping_address:
            data['shipping_address'] = shipping_address
        if payment_status:
            data['payment_status'] = payment_status

        return self._request('PUT', f'/orders/{order_id}', json_data=data)

    def delete_order(self, order_id: str) -> Dict[str, Any]:
        """Delete an order."""
        return self._request('DELETE', f'/orders/{order_id}')

    def get_activities(
        self,
        page: int = 1,
        per_page: int = 50,
        customer_id: Optional[str] = None,
        deal_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all activities."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if customer_id:
            params['customer_id'] = customer_id
        if deal_id:
            params['deal_id'] = deal_id

        return self._request('GET', '/activities', params=params)

    def create_activity(
        self,
        type: str,
        customer_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        subject: str,
        description: Optional[str] = None,
        scheduled_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new activity."""
        data = {
            'type': type,
            'subject': subject
        }

        if customer_id:
            data['customer_id'] = customer_id
        if deal_id:
            data['deal_id'] = deal_id
        if description:
            data['description'] = description
        if scheduled_at:
            data['scheduled_at'] = scheduled_at

        return self._request('POST', '/activities', json_data=data)

    def update_activity(
        self,
        activity_id: str,
        status: Optional[str] = None,
        completed_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update activity status."""
        data = {}
        if status:
            data['status'] = status
        if completed_at:
            data['completed_at'] = completed_at

        return self._request('PUT', f'/activities/{activity_id}', json_data=data)

    def delete_activity(self, activity_id: str) -> Dict[str, Any]:
        """Delete an activity."""
        return self._request('DELETE', f'/activities/{activity_id}')

    def get_products(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Get all products."""
        params = {
            'page': page,
            'per_page': per_page
        }
        return self._request('GET', '/products', params=params)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request('GET', f'/products/{product_id}')

    def create_product(
        self,
        name: str,
        code: str,
        price: float,
        description: Optional[str] = None,
        stock_quantity: int = 0
    ) -> Dict[str, Any]:
        """Create a new product."""
        data = {
            'name': name,
            'code': code,
            'price': price,
            'stock_quantity': stock_quantity
        }

        if description:
            data['description'] = description

        return self._request('POST', '/products', json_data=data)

    def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        stock_quantity: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update product details."""
        data = {}
        if name:
            data['name'] = name
        if price:
            data['price'] = price
        if description:
            data['description'] = description
        if stock_quantity is not None:
            data['stock_quantity'] = stock_quantity

        return self._request('PUT', f'/products/{product_id}', json_data=data)

    def delete_product(self, product_id: str) -> Dict[str, Any]:
        """Delete a product."""
        return self._request('DELETE', f'/products/{product_id}')

    def get_sales_report(
        self,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Get sales analytics report."""
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        return self._request('GET', '/reports/sales', params=params)

    def get_pipeline_report(self) -> Dict[str, Any]:
        """Get sales pipeline report."""
        return self._request('GET', '/reports/pipeline')

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        return self._request('GET', '/user/me')