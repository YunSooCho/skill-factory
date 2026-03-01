import requests
from typing import Dict, List, Optional, Any


class OrderDeskClient:
    """Client for Order Desk order management API."""

    BASE_URL = "https://app.orderdesk.me/api/v2"

    def __init__(self, api_key: str, store_id: str):
        """
        Initialize Order Desk client.

        Args:
            api_key: Your Order Desk API key
            store_id: Your Order Desk store ID
        """
        self.api_key = api_key
        self.store_id = store_id
        self.session = requests.Session()
        self.session.headers.update({
            "ORDERDESK-API-KEY": api_key,
            "ORDERDESK-STORE-ID": store_id,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Order Desk API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_orders(self, search: str = None, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/orders?page={page}"
        if search:
            endpoint += f"&search={search}"
        if status:
            endpoint += f"&order_status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_id}")

    def create_order(self, order_data: Dict) -> Dict[str, Any]:
        """Create a new order."""
        return self._request("POST", "/orders", order_data)

    def update_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update order."""
        return self._request("PUT", f"/orders/{order_id}", data)

    def delete_order(self, order_id: str) -> Dict[str, Any]:
        """Delete order."""
        return self._request("DELETE", f"/orders/{order_id}")

    def get_products(self, search: str = None, page: int = 1) -> Dict[str, Any]:
        """Get products."""
        endpoint = f"/products?page={page}"
        if search:
            endpoint += f"&search={search}"
        return self._request("GET", endpoint)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request("GET", f"/products/{product_id}")

    def create_product(self, code: str, name: str, price: float,
                      sku: str = None) -> Dict[str, Any]:
        """Create a new product."""
        data = {
            "code": code,
            "name": name,
            "price": price
        }
        if sku:
            data["sku"] = sku
        return self._request("POST", "/products", data=data)

    def update_product(self, product_id: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/products/{product_id}", data)

    def get_inventory(self, sku: str = None) -> Dict[str, Any]:
        """Get inventory levels."""
        if sku:
            return self._request("GET", f"/inventory/{sku}")
        return self._request("GET", "/inventory")

    def update_inventory(self, sku: str, quantity: int) -> Dict[str, Any]:
        """Update inventory quantity."""
        data = {
            "sku": sku,
            "quantity": quantity
        }
        return self._request("POST", "/inventory", data=data)

    def get_customers(self, search: str = None) -> Dict[str, Any]:
        """Get customers."""
        endpoint = "/customers"
        if search:
            endpoint += f"?search={search}"
        return self._request("GET", endpoint)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/customers/{customer_id}")

    def get_shipments(self, order_id: str = None) -> Dict[str, Any]:
        """Get shipments."""
        endpoint = "/shipments"
        if order_id:
            endpoint += f"?order_id={order_id}"
        return self._request("GET", endpoint)

    def create_shipment(self, order_id: str, tracking_number: str,
                       carrier: str) -> Dict[str, Any]:
        """Create shipment."""
        data = {
            "order_id": order_id,
            "tracking_number": tracking_number,
            "carrier": carrier
        }
        return self._request("POST", "/shipments", data=data)