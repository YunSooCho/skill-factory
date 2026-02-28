import requests
from typing import Dict, List, Optional, Any


class ZohoInventoryClient:
    """Client for Zoho Inventory API."""

    BASE_URL = "https://inventory.zoho.com/api/v1"

    def __init__(self, authtoken: str, organization_id: str):
        """
        Initialize Zoho Inventory client.

        Args:
            authtoken: Your Zoho Inventory authtoken
            organization_id: Your Zoho Inventory organization ID
        """
        self.authtoken = authtoken
        self.organization_id = organization_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {authtoken}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Zoho Inventory API."""
        url = f"{self.BASE_URL}{endpoint}"
        if params is None:
            params = {}
        params["organization_id"] = self.organization_id
        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_items(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get all items/inventory."""
        return self._request("GET", "/items", params={
            "page": page,
            "per_page": per_page
        })

    def get_item(self, item_id: str) -> Dict[str, Any]:
        """Get item details."""
        return self._request("GET", f"/items/{item_id}")

    def create_item(self, item_name: str, item_type: str = "goods",
                   unit: str = "pcs", rate: float = 0) -> Dict[str, Any]:
        """Create inventory item."""
        data = {
            "item_name": item_name,
            "item_type": item_type,
            "sku": f"SKU-{item_name}".upper().replace(" ", "-"),
            "unit": unit,
            "purchase_rate": rate,
            "sale_rate": rate
        }
        return self._request("POST", "/items", data=data)

    def update_item(self, item_id: str, data: Dict) -> Dict[str, Any]:
        """Update item."""
        return self._request("PUT", f"/items/{item_id}", data=data)

    def delete_item(self, item_id: str) -> Dict[str, Any]:
        """Delete item."""
        return self._request("DELETE", f"/items/{item_id}")

    def get_sales_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get sales orders."""
        params = {"page": page}
        if status:
            params["status"] = status
        return self._request("GET", "/salesorders", params=params)

    def get_sales_order(self, salesorder_id: str) -> Dict[str, Any]:
        """Get sales order details."""
        return self._request("GET", f"/salesorders/{salesorder_id}")

    def create_sales_order(self, customer_id: str, line_items: List[Dict],
                          template_id: str = None) -> Dict[str, Any]:
        """Create sales order."""
        data = {
            "customer_id": customer_id,
            "line_items": line_items
        }
        if template_id:
            data["template_id"] = template_id
        return self._request("POST", "/salesorders", data=data)

    def update_sales_order(self, salesorder_id: str, data: Dict) -> Dict[str, Any]:
        """Update sales order."""
        return self._request("PUT", f"/salesorders/{salesorder_id}", data=data)

    def delete_sales_order(self, salesorder_id: str) -> Dict[str, Any]:
        """Delete sales order."""
        return self._request("DELETE", f"/salesorders/{salesorder_id}")

    def get_purchase_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get purchase orders."""
        params = {"page": page}
        if status:
            params["status"] = status
        return self._request("GET", "/purchaseorders", params=params)

    def get_purchase_order(self, purchaseorder_id: str) -> Dict[str, Any]:
        """Get purchase order details."""
        return self._request("GET", f"/purchaseorders/{purchaseorder_id}")

    def create_purchase_order(self, vendor_id: str, line_items: List[Dict]) -> Dict[str, Any]:
        """Create purchase order."""
        data = {
            "vendor_id": vendor_id,
            "line_items": line_items
        }
        return self._request("POST", "/purchaseorders", data=data)

    def update_purchase_order(self, purchaseorder_id: str, data: Dict) -> Dict[str, Any]:
        """Update purchase order."""
        return self._request("PUT", f"/purchaseorders/{purchaseorder_id}", data=data)

    def get_customers(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", "/contacts", params={
            "page": page,
            "per_page": per_page,
            "contact_type": "customer"
        })

    def get_customer(self, contact_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/contacts/{contact_id}")

    def create_customer(self, contact_name: str, email: str = None,
                       phone: str = None, billing_address: Dict = None) -> Dict[str, Any]:
        """Create customer."""
        data = {
            "contact_name": contact_name,
            "contact_type": "customer"
        }
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if billing_address:
            data["billing_address"] = billing_address
        return self._request("POST", "/contacts", data=data)

    def get_vendors(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get vendors."""
        return self._request("GET", "/contacts", params={
            "page": page,
            "per_page": per_page,
            "contact_type": "vendor"
        })

    def get_vendor(self, contact_id: str) -> Dict[str, Any]:
        """Get vendor details."""
        return self._request("GET", f"/contacts/{contact_id}")

    def create_vendor(self, contact_name: str, email: str = None,
                     phone: str = None, billing_address: Dict = None) -> Dict[str, Any]:
        """Create vendor."""
        data = {
            "contact_name": contact_name,
            "contact_type": "vendor"
        }
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if billing_address:
            data["billing_address"] = billing_address
        return self._request("POST", "/contacts", data=data)

    def get_shipments(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """Get shipments."""
        params = {"page": page}
        if status:
            params["status"] = status
        return self._request("GET", "/shipments", params=params)

    def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Get shipment details."""
        return self._request("GET", f"/shipments/{shipment_id}")

    def create_shipment_from_salesorder(self, salesorder_id: str) -> Dict[str, Any]:
        """Create shipment from sales order."""
        return self._request("POST", f"/salesorders/{salesorder_id}/shipments")

    def get_packages(self, page: int = 1) -> Dict[str, Any]:
        """Get package types."""
        return self._request("GET", "/packages", params={"page": page})