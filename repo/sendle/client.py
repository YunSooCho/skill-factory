import requests
from typing import Dict, List, Optional, Any


class SendleClient:
    """Client for Sendle parcel delivery API."""

    BASE_URL = "https://api.sendle.com/api"

    def __init__(self, api_key: str, sendle_id: str):
        """
        Initialize Sendle client.

        Args:
            api_key: Your Sendle API key
            sendle_id: Your Sendle ID
        """
        self.api_key = api_key
        self.sendle_id = sendle_id
        self.session = requests.Session()
        self.session.auth = (sendle_id, api_key)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Sendle API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/orders/{order_id}")

    def get_orders(self, status: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get orders."""
        endpoint = f"/Orders?per_page={limit}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)

    def create_order(self, pickup_address: Dict, delivery_address: Dict,
                     parcel: Dict, description: str = None, currency: str = "AUD") -> Dict[str, Any]:
        """Create a new order."""
        data = {
            "pickup_address": pickup_address,
            "delivery_address": delivery_address,
            "parcel": parcel,
            "currency": currency
        }
        if description:
            data["description"] = description
        return self._request("POST", "/Orders", data=data)

    def update_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update order."""
        return self._request("PUT", f"/orders/{order_id}", data)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel order."""
        return self._request("DELETE", f"/orders/{order_id}")

    def get_tracking(self, order_id: str) -> Dict[str, Any]:
        """Get tracking information."""
        return self._request("GET", f"/tracking/{order_id}")

    def get_quote(self, pickup_suburb: str, pickup_postcode: str,
                  delivery_suburb: str, delivery_postcode: str,
                  weight: float, volume: float = None) -> Dict[str, Any]:
        """Get shipping quote."""
        data = {
            "pickup_suburb": pickup_suburb,
            "pickup_postcode": pickup_postcode,
            "delivery_suburb": delivery_suburb,
            "delivery_postcode": delivery_postcode,
            "kilogram_weight": weight,
            "cubic_metre_volume": volume
        }
        return self._request("POST", "/quote", data=data)

    def get_parcels(self) -> Dict[str, Any]:
        """Get parcel templates."""
        return self._request("GET", "/parcels")

    def get_manifest(self, order_id: str) -> Dict[str, Any]:
        """Get shipping manifest."""
        return self._request("GET", f"/orders/{order_id}/manifest")

    def get_webhooks(self) -> Dict[str, Any]:
        """Get registered webhooks."""
        return self._request("GET", "/webhooks")

    def create_webhook(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Create webhook."""
        data = {
            "url": url,
            "events": events
        }
        return self._request("POST", "/webhooks", data=data)

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request("DELETE", f"/webhooks/{webhook_id}")