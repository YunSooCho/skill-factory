import requests
from typing import Dict, List, Optional, Any


class PCACloudKonkanClient:
    """Client for PCA Cloud Konkan Japanese warehouse management API."""

    BASE_URL = "https://api.pca-cloud.co.jp/api/v1"

    def __init__(self, api_key: str, client_id: str):
        """
        Initialize PCA Cloud Konkan client.

        Args:
            api_key: Your PCA Cloud API key
            client_id: Your PCA Cloud client ID
        """
        self.api_key = api_key
        self.client_id = client_id
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "X-Client-ID": client_id,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to PCA Cloud API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_inventory(self, warehouse_code: str = None) -> Dict[str, Any]:
        """Get inventory levels."""
        endpoint = "/inventory"
        if warehouse_code:
            endpoint += f"?warehouse_code={warehouse_code}"
        return self._request("GET", endpoint)

    def get_product(self, product_code: str) -> Dict[str, Any]:
        """Get product by code."""
        return self._request("GET", f"/products/{product_code}")

    def list_products(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """List all products."""
        return self._request("GET", f"/products?page={page}&per_page={per_page}")

    def create_product(self, product_code: str, name: str,
                      description: str = None) -> Dict[str, Any]:
        """Create product."""
        data = {
            "product_code": product_code,
            "name": name
        }
        if description:
            data["description"] = description
        return self._request("POST", "/products", data=data)

    def update_product(self, product_code: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/products/{product_code}", data)

    def adjust_stock(self, product_code: str, quantity: int,
                    reason: str = None) -> Dict[str, Any]:
        """Adjust stock quantity."""
        data = {
            "product_code": product_code,
            "quantity": quantity
        }
        if reason:
            data["reason"] = reason
        return self._request("POST", "/inventory/adjust", data=data)

    def get_warehouses(self) -> Dict[str, Any]:
        """Get all warehouses."""
        return self._request("GET", "/warehouses")

    def get_warehouse(self, warehouse_code: str) -> Dict[str, Any]:
        """Get warehouse details."""
        return self._request("GET", f"/warehouses/{warehouse_code}")

    def get_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/orders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_number: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_number}")

    def create_order(self, customer_code: str, items: List[Dict],
                    shipping_address: Dict = None) -> Dict[str, Any]:
        """Create order."""
        data = {
            "customer_code": customer_code,
            "items": items
        }
        if shipping_address:
            data["shipping_address"] = shipping_address
        return self._request("POST", "/orders", data=data)

    def update_order_status(self, order_number: str, status: str) -> Dict[str, Any]:
        """Update order status."""
        return self._request("PUT", f"/orders/{order_number}/status", {"status": status})

    def get_customers(self, page: int = 1) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", f"/customers?page={page}")

    def create_customer(self, customer_code: str, name: str, email: str = None) -> Dict[str, Any]:
        """Create customer."""
        data = {
            "customer_code": customer_code,
            "name": name
        }
        if email:
            data["email"] = email
        return self._request("POST", "/customers", data=data)