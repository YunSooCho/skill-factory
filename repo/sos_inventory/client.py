import requests
from typing import Dict, List, Optional, Any


class SOSInventoryClient:
    """Client for SOS Inventory API."""

    BASE_URL = "https://api.sosinventory.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize SOS Inventory client.

        Args:
            api_key: Your SOS Inventory API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to SOS Inventory API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_inventory(self, location_id: str = None) -> Dict[str, Any]:
        """Get inventory levels."""
        endpoint = "/Inventory"
        if location_id:
            endpoint += f"?locationId={location_id}"
        return self._request("GET", endpoint)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product by ID."""
        return self._request("GET", f"/Products/{product_id}")

    def get_products(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """Get all products."""
        return self._request("GET", f"/Products?page={page}&perPage={per_page}")

    def create_product(self, name: str, sku: str, cost: float = None,
                      price: float = None) -> Dict[str, Any]:
        """Create product."""
        data = {
            "name": name,
            "sku": sku
        }
        if cost:
            data["cost"] = cost
        if price:
            data["price"] = price
        return self._request("POST", "/Products", data=data)

    def update_product(self, product_id: str, data: Dict) -> Dict[str, Any]:
        """Update product."""
        return self._request("PUT", f"/Products/{product_id}", data)

    def get_sales_order(self, order_id: str) -> Dict[str, Any]:
        """Get sales order."""
        return self._request("GET", f"/SalesOrders/{order_id}")

    def get_sales_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get sales orders."""
        endpoint = f"/SalesOrders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def create_sales_order(self, customer_id: str, items: List[Dict],
                          location_id: str = None) -> Dict[str, Any]:
        """Create sales order."""
        data = {
            "customerId": customer_id,
            "items": items
        }
        if location_id:
            data["locationId"] = location_id
        return self._request("POST", "/SalesOrders", data=data)

    def update_sales_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update sales order."""
        return self._request("PUT", f"/SalesOrders/{order_id}", data)

    def get_purchase_order(self, order_id: str) -> Dict[str, Any]:
        """Get purchase order."""
        return self._request("GET", f"/PurchaseOrders/{order_id}")

    def get_purchase_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get purchase orders."""
        endpoint = f"/PurchaseOrders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def create_purchase_order(self, vendor_id: str, items: List[Dict],
                             location_id: str = None) -> Dict[str, Any]:
        """Create purchase order."""
        data = {
            "vendorId": vendor_id,
            "items": items
        }
        if location_id:
            data["locationId"] = location_id
        return self._request("POST", "/PurchaseOrders", data=data)

    def get_locations(self) -> Dict[str, Any]:
        """Get all locations."""
        return self._request("GET", "/Locations")

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get location details."""
        return self._request("GET", f"/Locations/{location_id}")

    def get_customers(self, page: int = 1) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", f"/Customers?page={page}")

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/Customers/{customer_id}")

    def get_vendors(self, page: int = 1) -> Dict[str, Any]:
        """Get vendors."""
        return self._request("GET", f"/Vendors?page={page}")

    def get_vendor(self, vendor_id: str) -> Dict[str, Any]:
        """Get vendor details."""
        return self._request("GET", f"/Vendors/{vendor_id}")