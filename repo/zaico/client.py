import requests
from typing import Dict, List, Optional, Any


class ZaicoClient:
    """Client for Zaico Japanese inventory management API."""

    BASE_URL = "https://api.zaico.co.jp/api/v1"

    def __init__(self, api_token: str):
        """
        Initialize Zaico client.

        Args:
            api_token: Your Zaico API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Zaico API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_inventory(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """Get all inventory items."""
        return self._request("GET", f"/items?page={page}&per_page={per_page}")

    def get_item(self, item_id: str) -> Dict[str, Any]:
        """Get item by ID."""
        return self._request("GET", f"/items/{item_id}")

    def create_item(self, title: str, quantity: int = 0, sku: str = None,
                    description: str = None) -> Dict[str, Any]:
        """Create inventory item."""
        data = {
            "title": title,
            "quantity": quantity
        }
        if sku:
            data["sku"] = sku
        if description:
            data["description"] = description
        return self._request("POST", "/items", data=data)

    def update_item(self, item_id: str, data: Dict) -> Dict[str, Any]:
        """Update item."""
        return self._request("PUT", f"/items/{item_id}", data)

    def delete_item(self, item_id: str) -> Dict[str, Any]:
        """Delete item."""
        return self._request("DELETE", f"/items/{item_id}")

    def adjust_quantity(self, item_id: str, quantity: int,
                       note: str = None) -> Dict[str, Any]:
        """Adjust item quantity."""
        data = {
            "quantity": quantity
        }
        if note:
            data["note"] = note
        return self._request("POST", f"/items/{item_id}/adjust_quantity", data=data)

    def get_categories(self) -> Dict[str, Any]:
        """Get all categories."""
        return self._request("GET", "/categories")

    def get_category(self, category_id: str) -> Dict[str, Any]:
        """Get category details."""
        return self._request("GET", f"/categories/{category_id}")

    def create_category(self, name: str, color: str = None) -> Dict[str, Any]:
        """Create category."""
        data = {"name": name}
        if color:
            data["color"] = color
        return self._request("POST", "/categories", data=data)

    def get_locations(self) -> Dict[str, Any]:
        """Get all locations."""
        return self._request("GET", "/locations")

    def create_location(self, name: str) -> Dict[str, Any]:
        """Create location."""
        data = {"name": name}
        return self._request("POST", "/locations", data=data)

    def get_inventory_history(self, item_id: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get inventory adjustment history."""
        endpoint = f"/inventory_history?limit={limit}"
        if item_id:
            endpoint += f"&item_id={item_id}"
        return self._request("GET", endpoint)

    def export_inventory(self) -> Dict[str, Any]:
        """Export inventory."""
        return self._request("GET", "/export")

    def import_inventory(self, data: List[Dict]) -> Dict[str, Any]:
        """Import inventory items."""
        return self._request("POST", "/import", {"items": data})

    def search_items(self, keyword: str, page: int = 1) -> Dict[str, Any]:
        """Search items by keyword."""
        return self._request("GET", f"/items/search?keyword={keyword}&page={page}")