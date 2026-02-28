import requests
from typing import Dict, List, Optional, Any


class LogilessClient:
    """Client for Logiless e-commerce inventory API."""

    BASE_URL = "https://api.logiless.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Logiless client.

        Args:
            api_key: Your Logiless API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Logiless API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_products(self, page: int = 1, limit: int = 100) -> Dict[str, Any]:
        """Get all products."""
        return self._request("GET", f"/products?page={page}&limit={limit}")

    def get_product(self, item_id: str) -> Dict[str, Any]:
        """Get product by item ID."""
        return self._request("GET", f"/products/{item_id}")

    def create_product(self, name: str, sku: str, price: float,
                      description: str = None) -> Dict[str, Any]:
        """Create a new product."""
        data = {
            "name": name,
            "sku": sku,
            "price": price
        }
        if description:
            data["description"] = description
        return self._request("POST", "/products", data=data)

    def update_product(self, item_id: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/products/{item_id}", data)

    def get_inventory(self, item_id: str = None) -> Dict[str, Any]:
        """Get inventory levels."""
        if item_id:
            return self._request("GET", f"/inventory/{item_id}")
        return self._request("GET", "/inventory")

    def update_inventory(self, item_id: str, quantity: int) -> Dict[str, Any]:
        """Update inventory quantity."""
        data = {"quantity": quantity}
        return self._request("PUT", f"/inventory/{item_id}", data)

    def get_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/orders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_id}")

    def create_order(self, customer: Dict, items: List[Dict],
                    shipping_address: Dict = None) -> Dict[str, Any]:
        """Create a new order."""
        data = {
            "customer": customer,
            "items": items
        }
        if shipping_address:
            data["shipping_address"] = shipping_address
        return self._request("POST", "/orders", data=data)

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update order status."""
        return self._request("PUT", f"/orders/{order_id}/status", {"status": status})

    def get_customers(self, page: int = 1) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", f"/customers?page={page}")

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/customers/{customer_id}")

    def create_customer(self, email: str, name: str, phone: str = None) -> Dict[str, Any]:
        """Create customer."""
        data = {
            "email": email,
            "name": name
        }
        if phone:
            data["phone"] = phone
        return self._request("POST", "/customers", data=data)

    def get_shipments(self, status: str = None) -> Dict[str, Any]:
        """Get shipments."""
        endpoint = "/shipments"
        if status:
            endpoint += f"?status={status}"
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