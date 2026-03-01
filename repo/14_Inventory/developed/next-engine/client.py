import requests
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any


class NextEngineClient:
    """Client for Next-Engine Japanese ERP API."""

    BASE_URL = "https://api.next-engine.org/api_neauth"
    API_BASE = "https://api.next-engine.org/api_v1_master_"

    def __init__(self, api_key: str, sign_key: str, client_id: str = None):
        """
        Initialize Next-Engine client.

        Args:
            api_key: Your Next-Engine API key
            sign_key: Your Next-Engine sign key
            client_id: Client ID (optional)
        """
        self.api_key = api_key
        self.sign_key = sign_key
        self.client_id = client_id
        self.access_token = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _generate_signature(self, path: str, timestamp: str) -> str:
        """Generate HMAC signature for authentication."""
        message = f"{path}&{timestamp}"
        signature = hmac.new(
            bytes(self.sign_key, 'UTF-8'),
            bytes(message, 'UTF-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _auth_request(self, data: Dict) -> Dict[str, Any]:
        """Make auth request."""
        url = self.BASE_URL
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def authenticate(self) -> Dict[str, Any]:
        """Authenticate and get access token."""
        data = {
            "api_key": self.api_key,
            "sign_key": self.sign_key
        }
        if self.client_id:
            data["client_id"] = self.client_id
        result = self._auth_request(data)
        if "access_token" in result:
            self.access_token = result["access_token"]
        return result

    def _api_request(self, endpoint: str, body: List[Dict] = None) -> Dict[str, Any]:
        """Make API request."""
        timestamp = str(int(time.time()))
        path = endpoint
        signature = self._generate_signature(path, timestamp)

        data = {
            "api_key": self.api_key,
            "sign_key": self.sign_key,
            "access_token": self.access_token,
            "signature": signature,
            "timestamp": timestamp,
            "path": path
        }
        if body:
            data["body"] = body
            data["data"] = body[0] if len(body) == 1 else body

        url = f"{self.API_BASE}{endpoint}"
        try:
            response = self.session.post(url, json=data)
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_products(self, fields: str = "all", search: Dict = None) -> Dict[str, Any]:
        """Get products."""
        params = f"/fields/{fields}"
        return self._api_request(f"products{params}")

    def get_product(self, goods_id: str) -> Dict[str, Any]:
        """Get product by ID."""
        return self._api_request(f"/goods/{goods_id}")

    def get_inventory(self, stock_id: str = None) -> Dict[str, Any]:
        """Get inventory."""
        if stock_id:
            return self._api_request(f"/stock/{stock_id}")
        return self._api_request("/stock")

    def get_orders(self, search: Dict = None) -> Dict[str, Any]:
        """Get orders."""
        return self._api_request("/orders")

    def register_order(self, order_data: Dict) -> Dict[str, Any]:
        """Register new order."""
        return self._api_request("/receiveorder/register", [order_data])

    def update_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update order."""
        data["order_id"] = order_id
        return self._api_request("/receiveorder/update", [data])

    def get_customers(self, search: Dict = None) -> Dict[str, Any]:
        """Get customers."""
        return self._api_request("/customer")

    def register_customer(self, customer_data: Dict) -> Dict[str, Any]:
        """Register new customer."""
        return self._api_request("/customer/register", [customer_data])

    def get_shipments(self, order_id: str = None) -> Dict[str, Any]:
        """Get shipments."""
        if order_id:
            return self._api_request(f"/shipment?receive_order_id={order_id}")
        return self._api_request("/shipment")

    def register_shipment(self, shipment_data: Dict) -> Dict[str, Any]:
        """Register shipment."""
        return self._api_request("/shipment/register", [shipment_data])