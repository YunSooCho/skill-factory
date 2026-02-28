import requests
from typing import Dict, List, Optional, Any


class SendcloudClient:
    """Client for Sendcloud shipping platform API."""

    BASE_URL = "https://panel.sendcloud.com/api/v2"

    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Sendcloud client.

        Args:
            api_key: Your Sendcloud API key
            api_secret: Your Sendcloud API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.auth = (api_key, api_secret)
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Sendcloud API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_parcel(self, parcel_id: int) -> Dict[str, Any]:
        """Get parcel details."""
        return self._request("GET", f"/parcels/{parcel_id}")

    def get_parcels(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Get all parcels."""
        return self._request("GET", f"/parcels?page={page}&limit={limit}")

    def create_parcel(self, address: Dict, parcels: List[Dict],
                     weight: float = None, phone: str = None, email: str = None) -> Dict[str, Any]:
        """Create a new parcel."""
        data = {
            "address": address,
            "parcels": parcels
        }
        if weight:
            data["weight"] = weight
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        return self._request("POST", "/parcels", data=data)

    def update_parcel(self, parcel_id: int, data: Dict) -> Dict[str, Any]:
        """Update parcel."""
        return self._request("PUT", f"/parcels/{parcel_id}", data)

    def cancel_parcel(self, parcel_id: int) -> Dict[str, Any]:
        """Cancel parcel."""
        return self._request("DELETE", f"/parcels/{parcel_id}")

    def get_carriers(self) -> Dict[str, Any]:
        """Get available carriers."""
        return self._request("GET", "/carriers")

    def get_carrier(self, carrier_id: int) -> Dict[str, Any]:
        """Get carrier details."""
        return self._request("GET", f"/carriers/{carrier_id}")

    def get_shipping_methods(self) -> Dict[str, Any]:
        """Get shipping methods."""
        return self._request("GET", "/shipping_methods")

    def get_label(self, parcel_id: int) -> Dict[str, Any]:
        """Get label for parcel."""
        return self._request("POST", f"/parcels/{parcel_id}/labels")

    def create_return_portal(self, order_id: str, email: str = None) -> Dict[str, Any]:
        """Create return portal."""
        data = {"order_id": order_id}
        if email:
            data["email"] = email
        return self._request("POST", "/user/returns", data=data)

    def get_shipments(self, page: int = 1) -> Dict[str, Any]:
        """Get shipments."""
        return self._request("GET", f"/shipments?page={page}")

    def get_shipment(self, shipment_id: int) -> Dict[str, Any]:
        """Get shipment details."""
        return self._request("GET", f"/shipments/{shipment_id}")

    def webhooks(self) -> Dict[str, Any]:
        """Get webhook settings."""
        return self._request("GET", "/webhooks")

    def create_webhook(self, event: str, url: str, secret: str = None) -> Dict[str, Any]:
        """Create webhook."""
        data = {
            "event": event,
            "url": url
        }
        if secret:
            data["secret"] = secret
        return self._request("POST", "/webhooks", data=data)

    def delete_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request("DELETE", f"/webhooks/{webhook_id}")