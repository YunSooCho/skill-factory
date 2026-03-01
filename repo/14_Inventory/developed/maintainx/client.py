import requests
from typing import Dict, List, Optional, Any


class MaintainXClient:
    """Client for MaintainX facility maintenance API."""

    BASE_URL = "https://api.maintainx.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize MaintainX client.

        Args:
            api_key: Your MaintainX API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to MaintainX API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def list_work_orders(self, status: str = None, assignee_id: str = None,
                        limit: int = 100) -> Dict[str, Any]:
        """List all work orders."""
        endpoint = f"/work-orders?limit={limit}"
        if status:
            endpoint += f"&status={status}"
        if assignee_id:
            endpoint += f"&assignee_id={assignee_id}"
        return self._request("GET", endpoint)

    def get_work_order(self, work_order_id: str) -> Dict[str, Any]:
        """Get work order details."""
        return self._request("GET", f"/work-orders/{work_order_id}")

    def create_work_order(self, title: str, description: str = None,
                         priority: str = "medium", assignee_id: str = None,
                         location_id: str = None) -> Dict[str, Any]:
        """Create a new work order."""
        data = {
            "title": title,
            "priority": priority
        }
        if description:
            data["description"] = description
        if assignee_id:
            data["assignee_id"] = assignee_id
        if location_id:
            data["location_id"] = location_id
        return self._request("POST", "/work-orders", data=data)

    def update_work_order(self, work_order_id: str, data: Dict) -> Dict[str, Any]:
        """Update work order."""
        return self._request("PUT", f"/work-orders/{work_order_id}", data)

    def close_work_order(self, work_order_id: str, resolution: str = None) -> Dict[str, Any]:
        """Close a work order."""
        data = {}
        if resolution:
            data["resolution"] = resolution
        return self._request("POST", f"/work-orders/{work_order_id}/close", data=data)

    def list_locations(self) -> Dict[str, Any]:
        """Get all locations."""
        return self._request("GET", "/locations")

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get location details."""
        return self._request("GET", f"/locations/{location_id}")

    def create_location(self, name: str, address: Dict = None,
                       location_type: str = None) -> Dict[str, Any]:
        """Create a new location."""
        data = {"name": name}
        if address:
            data["address"] = address
        if location_type:
            data["location_type"] = location_type
        return self._request("POST", "/locations", data=data)

    def list_users(self) -> Dict[str, Any]:
        """Get all users."""
        return self._request("GET", "/users")

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details."""
        return self._request("GET", f"/users/{user_id}")

    def list_parts(self) -> Dict[str, Any]:
        """Get inventory parts."""
        return self._request("GET", "/parts")

    def create_part(self, name: str, sku: str, quantity: int,
                   cost: float = None) -> Dict[str, Any]:
        """Create inventory part."""
        data = {
            "name": name,
            "sku": sku,
            "quantity": quantity
        }
        if cost:
            data["cost"] = cost
        return self._request("POST", "/parts", data=data)

    def request_part(self, work_order_id: str, part_id: str, quantity: int) -> Dict[str, Any]:
        """Request part for work order."""
        data = {
            "part_id": part_id,
            "quantity": quantity
        }
        return self._request("POST", f"/work-orders/{work_order_id}/parts", data=data)