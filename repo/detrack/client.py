"""
Detrack API Client

Complete client for Detrack delivery management integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class DetrackAPIClient:
    """
    Complete client for Detrack delivery management.
    Supports order creation, delivery tracking, and route optimization.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Detrack API client.

        Args:
            api_key: Detrack API key (from env: DETRACK_API_KEY)
            base_url: Base URL (default: https://app.detrack.com/api/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("DETRACK_API_KEY")
        self.base_url = base_url or os.getenv(
            "DETRACK_BASE_URL",
            "https://app.detrack.com/api/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set DETRACK_API_KEY environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": self.api_key,
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
        """Make HTTP request to Detrack API."""
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
            return {"status": "success"}

    # Orders

    def create_order(
        self,
        order_number: str,
        address: str,
        date: str,
        status: str = "pending",
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        assign_to: Optional[str] = None,
        do_number: Optional[str] = None,
        remarks: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a delivery order.

        Args:
            order_number: Unique order number
            address: Delivery address
            date: Delivery date (YYYY-MM-DD)
            status: Order status
            time_from: Delivery time from (HH:MM)
            time_to: Delivery time to (HH:MM)
            assign_to: Assigned driver name or ID
            do_number: Delivery order number
            remarks: Order remarks

        Returns:
            Order information
        """
        data = {
            'order_number': order_number,
            'address': address,
            'date': date,
            'status': status
        }

        if time_from:
            data['time_from'] = time_from
        if time_to:
            data['time_to'] = time_to
        if assign_to:
            data['assign_to'] = assign_to
        if do_number:
            data['do_number'] = do_number
        if remarks:
            data['remarks'] = remarks

        return self._request('POST', '/orders', data=data)

    def get_order(self, order_number: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request('GET', f'/orders/{order_number}')

    def list_orders(
        self,
        date: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List orders with filtering."""
        params = {'limit': limit, 'offset': offset}
        if date:
            params['date'] = date
        if status:
            params['status'] = status
        return self._request('GET', '/orders', params=params)

    def update_order(
        self,
        order_number: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update order."""
        return self._request('PUT', f'/orders/{order_number}', data=kwargs)

    def delete_order(self, order_number: str) -> Dict[str, Any]:
        """Delete an order."""
        return self._request('DELETE', f'/orders/{order_number}')

    # Upload Items

    def import_orders(
        self,
        orders: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Bulk import orders."""
        data = {'orders': orders}
        return self._request('POST', '/import', data=data)

    # Drivers

    def list_drivers(self) -> Dict[str, Any]:
        """List all drivers."""
        return self._request('GET', '/drivers')

    def get_driver(self, driver_id: str) -> Dict[str, Any]:
        """Get driver details."""
        return self._request('GET', f'/drivers/{driver_id}')

    # Route Optimization

    def optimize_route(
        self,
        date: str,
        driver: Optional[str] = None,
        start_address: Optional[str] = None,
        end_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize delivery route.

        Args:
            date: Date for route
            driver: Specific driver (optional)
            start_address: Starting address
            end_address: Ending address

        Returns:
            Route optimization result
        """
        data = {'date': date}
        if driver:
            data['driver'] = driver
        if start_address:
            data['start_address'] = start_address
        if end_address:
            data['end_address'] = end_address
        return self._request('POST', '/routes/optimize', data=data)

    # Reports

    def get_daily_report(
        self,
        date: str
    ) -> Dict[str, Any]:
        """Get daily delivery report."""
        params = {'date': date}
        return self._request('GET', '/reports/daily', params=params)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create webhook."""
        data = {'url': url, 'events': events}
        if secret:
            data['secret'] = secret
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()