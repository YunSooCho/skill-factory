import requests
from typing import Dict, List, Optional, Any


class KuraBugyoClient:
    """Client for Kura-Bugyo (Japanese WMS) API."""

    BASE_URL = "https://api.kura-bugyo.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Kura-Bugyo client.

        Args:
            api_key: Your Kura-Bugyo API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Kura-Bugyo API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def list_inventory(self, warehouse_code: str = None) -> Dict[str, Any]:
        """List all inventory items."""
        endpoint = "/inventory"
        if warehouse_code:
            endpoint += f"?warehouse_code={warehouse_code}"
        return self._request("GET", endpoint)

    def get_product(self, product_code: str) -> Dict[str, Any]:
        """Get product details by code."""
        return self._request("GET", f"/products/{product_code}")

    def list_products(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """List all products."""
        return self._request("GET", f"/products?page={page}&per_page={per_page}")

    def create_product(self, product_code: str, name: str,
                      unit: str = None, category_code: str = None) -> Dict[str, Any]:
        """Create a new product."""
        data = {
            "product_code": product_code,
            "name": name
        }
        if unit:
            data["unit"] = unit
        if category_code:
            data["category_code"] = category_code
        return self._request("POST", "/products", data=data)

    def update_product(self, product_code: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/products/{product_code}", data)

    def receive_goods(self, product_code: str, quantity: int,
                     location: str = None, lot_number: str = None) -> Dict[str, Any]:
        """Receive goods into inventory."""
        data = {
            "product_code": product_code,
            "quantity": quantity
        }
        if location:
            data["location"] = location
        if lot_number:
            data["lot_number"] = lot_number
        return self._request("POST", "/inventory/receive", data=data)

    def ship_goods(self, product_code: str, quantity: int,
                  destination: str = None) -> Dict[str, Any]:
        """Ship goods from inventory."""
        data = {
            "product_code": product_code,
            "quantity": quantity
        }
        if destination:
            data["destination"] = destination
        return self._request("POST", "/inventory/ship", data=data)

    def adjust_inventory(self, product_code: str, quantity: int,
                        reason: str, location: str = None) -> Dict[str, Any]:
        """Adjust inventory quantity."""
        data = {
            "product_code": product_code,
            "quantity": quantity,
            "reason": reason
        }
        if location:
            data["location"] = location
        return self._request("POST", "/inventory/adjust", data=data)

    def get_warehouses(self) -> Dict[str, Any]:
        """Get all warehouses."""
        return self._request("GET", "/warehouses")

    def get_locations(self, warehouse_code: str) -> Dict[str, Any]:
        """Get storage locations in warehouse."""
        return self._request("GET", f"/warehouses/{warehouse_code}/locations")

    def create_order(self, order_items: List[Dict], customer_code: str) -> Dict[str, Any]:
        """Create shipping order."""
        data = {
            "customer_code": customer_code,
            "items": order_items
        }
        return self._request("POST", "/orders", data=data)

    def get_order(self, order_number: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_number}")

    def update_order_status(self, order_number: str, status: str) -> Dict[str, Any]:
        """Update order status."""
        return self._request("PUT", f"/orders/{order_number}/status", {"status": status})