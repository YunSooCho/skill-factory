import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, date


class DetrackClient:
    """Client for Detrack delivery tracking API."""

    BASE_URL = "https://api.detrack.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Detrack client.

        Args:
            api_key: Your Detrack API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Detrack API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def create_delivery(self, order_no: str, address: str, deliver_to: str,
                       tel: str = None, deliver_date: str = None,
                       deliver_time: str = None, instructions: str = None) -> Dict[str, Any]:
        """Create a new delivery."""
        data = {
            "do": [{
                "order_no": order_no,
                "address": address,
                "deliver_to": deliver_to
            }]
        }
        if tel:
            data["do"][0]["tel"] = tel
        if deliver_date:
            data["do"][0]["deliver_date"] = deliver_date
        if deliver_time:
            data["do"][0]["deliver_time"] = deliver_time
        if instructions:
            data["do"][0]["instructions"] = instructions
        return self._request("POST", "/deliveries", data=data)

    def batch_create_deliveries(self, deliveries: List[Dict]) -> Dict[str, Any]:
        """Create multiple deliveries in batch."""
        data = {"do": deliveries}
        return self._request("POST", "/deliveries", data=data)

    def get_delivery(self, order_no: str) -> Dict[str, Any]:
        """Get delivery status."""
        return self._request("GET", f"/deliveries/{order_no}")

    def update_delivery(self, order_no: str, data: Dict) -> Dict[str, Any]:
        """Update delivery details."""
        return self._request("PUT", f"/deliveries/{order_no}", data)

    def delete_delivery(self, order_no: str) -> Dict[str, Any]:
        """Delete/cancel delivery."""
        return self._request("DELETE", f"/deliveries/{order_no}")

    def list_deliveries(self, date: str = None, status: str = None) -> Dict[str, Any]:
        """List all deliveries."""
        endpoint = "/deliveries"
        params = []
        if date:
            params.append(f"date={date}")
        if status:
            params.append(f"status={status}")
        if params:
            endpoint += "?" + "&".join(params)
        return self._request("GET", endpoint)

    def list_drivers(self) -> Dict[str, Any]:
        """List all drivers."""
        return self._request("GET", "/drivers")

    def get_driver(self, driver_id: str) -> Dict[str, Any]:
        """Get driver details."""
        return self._request("GET", f"/drivers/{driver_id}")

    def assign_delivery(self, order_no: str, driver_id: str) -> Dict[str, Any]:
        """Assign delivery to driver."""
        data = {"driver_id": driver_id}
        return self._request("POST", f"/deliveries/{order_no}/assign", data=data)

    def unassign_delivery(self, order_no: str) -> Dict[str, Any]:
        """Unassign delivery from driver."""
        return self._request("POST", f"/deliveries/{order_no}/unassign")

    def get_delivery_proof(self, order_no: str) -> Dict[str, Any]:
        """Get delivery proof (POD)."""
        return self._request("GET", f"/deliveries/{order_no}/proof")