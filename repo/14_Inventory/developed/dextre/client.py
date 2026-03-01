import requests
from typing import Dict, List, Optional, Any


class DextreClient:
    """Client for Dextre warehouse and inventory API."""

    BASE_URL = "https://api.dextre.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Dextre client.

        Args:
            api_key: Your Dextre API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Dextre API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_inventory(self, warehouse_id: str = None) -> Dict[str, Any]:
        """Get all inventory items."""
        endpoint = "/inventory"
        if warehouse_id:
            endpoint += f"?warehouse_id={warehouse_id}"
        return self._request("GET", endpoint)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request("GET", f"/products/{product_id}")

    def list_products(self, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """List all products."""
        return self._request("GET", f"/products?page={page}&per_page={per_page}")

    def create_product(self, sku: str, name: str, description: str = None,
                      stock_quantity: int = 0, price: float = None) -> Dict[str, Any]:
        """Create a new product."""
        data = {
            "sku": sku,
            "name": name,
            "stock_quantity": stock_quantity
        }
        if description:
            data["description"] = description
        if price:
            data["price"] = price
        return self._request("POST", "/products", data=data)

    def update_product(self, product_id: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/products/{product_id}", data)

    def adjust_stock(self, product_id: str, quantity: int, reason: str = None) -> Dict[str, Any]:
        """Adjust product stock quantity."""
        data = {
            "quantity": quantity,
            "reason": reason
        }
        return self._request("POST", f"/products/{product_id}/stock", data=data)

    def get_warehouses(self) -> Dict[str, Any]:
        """Get all warehouses."""
        return self._request("GET", "/warehouses")

    def get_warehouse(self, warehouse_id: str) -> Dict[str, Any]:
        """Get warehouse details."""
        return self._request("GET", f"/warehouses/{warehouse_id}")

    def create_warehouse(self, name: str, address: str, location: Dict = None) -> Dict[str, Any]:
        """Create a new warehouse."""
        data = {
            "name": name,
            "address": address
        }
        if location:
            data["location"] = location
        return self._request("POST", "/warehouses", data=data)

    def get_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/orders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_id}")

    def create_order(self, items: List[Dict], customer_id: str = None) -> Dict[str, Any]:
        """Create a new order."""
        data = {
            "items": items
        }
        if customer_id:
            data["customer_id"] = customer_id
        return self._request("POST", "/orders", data=data)

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update order status."""
        data = {"status": status}
        return self._request("PUT", f"/orders/{order_id}/status", data=data)