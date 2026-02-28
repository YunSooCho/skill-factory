import requests
from typing import Dict, List, Optional, Any


class OpenlogiClient:
    """Client for Openlogi fulfillment service API."""

    BASE_URL = "https://api.openlogi.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Openlogi client.

        Args:
            api_key: Your Openlogi API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Openlogi API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_inventory(self, warehouse_code: str = None) -> Dict[str, Any]:
        """Get warehouse inventory."""
        endpoint = "/items"
        if warehouse_code:
            endpoint += f"?warehouse_code={warehouse_code}"
        return self._request("GET", endpoint)

    def get_item(self, item_code: str) -> Dict[str, Any]:
        """Get item details by code."""
        return self._request("GET", f"/items/{item_code}")

    def create_item(self, item_code: str, name: str, unit: str = "EA",
                   price: float = None) -> Dict[str, Any]:
        """Create a new item."""
        data = {
            "item_code": item_code,
            "name": name,
            "unit": unit
        }
        if price:
            data["price"] = price
        return self._request("POST", "/items", data=data)

    def update_item(self, item_code: str, data: Dict) -> Dict[str, Any]:
        """Update item."""
        return self._request("PUT", f"/items/{item_code}", data)

    def get_warehouses(self) -> Dict[str, Any]:
        """Get all warehouses."""
        return self._request("GET", "/warehouses")

    def get_warehouse(self, warehouse_code: str) -> Dict[str, Any]:
        """Get warehouse details."""
        return self._request("GET", f"/warehouses/{warehouse_code}")

    def get_orders(self, status: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/orders?limit={limit}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_code: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_code}")

    def create_shipment(self, order_code: str, items: List[Dict],
                       recipient_address: Dict) -> Dict[str, Any]:
        """Create shipment order."""
        data = {
            "order_code": order_code,
            "items": items,
            "recipient_address": recipient_address
        }
        return self._request("POST", "/shipments", data=data)

    def update_shipment(self, shipment_id: str, data: Dict) -> Dict[str, Any]:
        """Update shipment."""
        return self._request("PUT", f"/shipments/{shipment_id}", data)

    def cancel_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Cancel shipment."""
        return self._request("DELETE", f"/shipments/{shipment_id}")

    def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Get shipment details."""
        return self._request("GET", f"/shipments/{shipment_id}")

    def get_customers(self, limit: int = 100) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", f"/customers?limit={limit}")

    def get_customer(self, customer_code: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/customers/{customer_code}")

    def create_customer(self, customer_code: str, name: str, email: str = None,
                       phone: str = None, address: Dict = None) -> Dict[str, Any]:
        """Create customer."""
        data = {
            "customer_code": customer_code,
            "name": name
        }
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
        return self._request("POST", "/customers", data=data)