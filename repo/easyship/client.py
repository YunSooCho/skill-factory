import requests
from typing import Dict, List, Optional, Any


class EasyshipClient:
    """Client for EasyShip shipping logistics API."""

    BASE_URL = "https://api.easyship.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize EasyShip client.

        Args:
            api_key: Your EasyShip API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to EasyShip API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_rates(self, origin_address: Dict, destination_address: Dict,
                 parcels: List[Dict], currency: str = "USD") -> Dict[str, Any]:
        """Get shipping rates."""
        data = {
            "origin_address": origin_address,
            "destination_address": destination_address,
            "parcels": parcels,
            "currency": currency
        }
        return self._request("POST", "/rates", data=data)

    def create_shipment(self, origin_address: Dict, destination_address: Dict,
                       parcels: List[Dict], selected_rate_id: str,
                       customs_items: List[Dict] = None) -> Dict[str, Any]:
        """Create a shipment."""
        data = {
            "origin_address": origin_address,
            "destination_address": destination_address,
            "parcels": parcels,
            "selected_rate_id": selected_rate_id
        }
        if customs_items:
            data["customs_items"] = customs_items
        return self._request("POST", "/shipments", data=data)

    def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Get shipment details."""
        return self._request("GET", f"/shipments/{shipment_id}")

    def list_shipments(self, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """List all shipments."""
        return self._request("GET", f"/shipments?page={page}&per_page={per_page}")

    def update_shipment(self, shipment_id: str, data: Dict) -> Dict[str, Any]:
        """Update shipment."""
        return self._request("PUT", f"/shipments/{shipment_id}", data)

    def cancel_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Cancel shipment."""
        return self._request("DELETE", f"/shipments/{shipment_id}")

    def get_label(self, shipment_id: str) -> Dict[str, Any]:
        """Get shipping label."""
        return self._request("GET", f"/shipments/{shipment_id}/label")

    def track_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Track shipment status."""
        return self._request("GET", f"/shipments/{shipment_id}/track")

    def get_tracking_history(self, tracking_number: str) -> Dict[str, Any]:
        """Get tracking history by tracking number."""
        return self._request("GET", f"/tracking/{tracking_number}")

    def get_addresses(self) -> Dict[str, Any]:
        """Get saved addresses."""
        return self._request("GET", "/addresses")

    def create_address(self, address: Dict) -> Dict[str, Any]:
        """Create address."""
        return self._request("POST", "/addresses", data=address)