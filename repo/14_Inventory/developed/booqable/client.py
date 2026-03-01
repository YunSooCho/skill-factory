import requests
from typing import Dict, List, Optional, Any


class BooqableClient:
    """Client for Booqable rental inventory API."""

    BASE_URL = "https://api.booqable.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Booqable client.

        Args:
            api_key: Your Booqable API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Booqable API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def list_products(self, page: int = 1) -> Dict[str, Any]:
        """List all products."""
        return self._request("GET", f"/products?page={page}")

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request("GET", f"/products/{product_id}")

    def list_orders(self, status: str = None, page: int = 1) -> Dict[str, Any]:
        """List orders."""
        endpoint = f"/orders?page={page}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_id}")

    def create_order(self, product_id: str, quantity: int, customer_id: str,
                    start_date: str, end_date: str) -> Dict[str, Any]:
        """Create a rental order."""
        data = {
            "order": {
                "customer_id": customer_id,
                "start_at": start_date,
                "stop_at": end_date,
                "order_items": [{
                    "product_id": product_id,
                    "quantity": quantity
                }]
            }
        }
        return self._request("POST", "/orders", data=data)

    def update_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update order."""
        return self._request("PUT", f"/orders/{order_id}", {"order": data})

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel order."""
        return self._request("DELETE", f"/orders/{order_id}")

    def list_customers(self, page: int = 1) -> Dict[str, Any]:
        """List customers."""
        return self._request("GET", f"/customers?page={page}")

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/customers/{customer_id}")

    def create_customer(self, email: str, first_name: str, last_name: str,
                       phone: str = None, company: str = None) -> Dict[str, Any]:
        """Create customer."""
        data = {
            "customer": {
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        }
        if phone:
            data["customer"]["phone"] = phone
        if company:
            data["customer"]["company"] = company
        return self._request("POST", "/customers", data=data)

    def get_inventory(self, product_id: str) -> Dict[str, Any]:
        """Get inventory availability for product."""
        return self._request("GET", f"/products/{product_id}/inventory")