"""
ECForce Client - REST API Implementation
ECForce is a Japanese e-commerce platform (https://ecforce.jp/)
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class EcforceClient:
    """
    Complete client for ECForce API - Japanese EC platform.
    Supports Products, Orders, Customers, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize ECForce client.
        
        Args:
            api_key: API key (from env: ECFORCE_API_KEY)
            api_secret: API secret (from env: ECFORCE_API_SECRET)
            base_url: Base URL (from env: ECFORCE_BASE_URL)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            ECFORCE_API_KEY: Your API key
            ECFORCE_API_SECRET: Your API secret
            ECFORCE_BASE_URL: Base URL (default: https://{your-shop}.ec-force.com/api)
        """
        self.api_key = api_key or os.getenv("ECFORCE_API_KEY")
        self.api_secret = api_secret or os.getenv("ECFORCE_API_SECRET")
        self.base_url = base_url or os.getenv("ECFORCE_BASE_URL")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key is required. Set ECFORCE_API_KEY environment variable.")
        
        self.base_url = (self.base_url or "").rstrip("/")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-EC-Force-API-Access-Token": self.api_key,
            "X-EC-Force-API-Access-Token-Secret": self.api_secret,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to ECForce API."""
        url = urljoin(self.base_url + "/" if self.base_url else "https://api.ec-force.com/v1/", endpoint.lstrip("/"))
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()
        
        return response.json() if response.content else {}
    
    # Products
    def list_products(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        params = {"page": page, "per_page": min(limit, 100)}
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._request("GET", f"products/{product_id}")
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "products", data=product_data)
    
    def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"products/{product_id}", data=product_data)
    
    def delete_product(self, product_id: str) -> None:
        self._request("DELETE", f"products/{product_id}")
    
    # Orders
    def list_orders(
        self,
        page: int = 1,
        limit: int = 50,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"page": page, "per_page": min(limit, 100)}
        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._request("GET", f"orders/{order_id}")
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "orders", data=order_data)
    
    def update_order_status(
        self,
        order_id: str,
        status: str,
        email_customer: bool = False
    ) -> Dict[str, Any]:
        return self._request(
            "PUT",
            f"orders/{order_id}/status",
            data={"status": status, "send_email": email_customer}
        )
    
    # Customers
    def list_customers(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        params = {"page": page, "per_page": min(limit, 100)}
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "customers", data=customer_data)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    # Inventory
    def get_inventory(self, product_id: str) -> Dict[str, Any]:
        return self._request("GET", f"products/{product_id}/inventory")
    
    def update_inventory(
        self,
        product_id: str,
        quantity: int,
        warehouse_id: Optional[str] = None
    ) -> Dict[str, Any]:
        data = {"quantity": quantity}
        if warehouse_id:
            data["warehouse_id"] = warehouse_id
        return self._request("POST", f"products/{product_id}/inventory", data=data)
    
    # Categories
    def list_categories(self) -> Dict[str, Any]:
        return self._request("GET", "categories")
    
    # Webhooks
    def list_webhooks(self) -> Dict[str, Any]:
        return self._request("GET", "webhooks")
    
    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        data = {"url": url, "events": events}
        if secret:
            data["secret"] = secret
        return self._request("POST", "webhooks", data=data)
    
    def delete_webhook(self, webhook_id: str) -> None:
        self._request("DELETE", f"webhooks/{webhook_id}")
    
    close = lambda self: self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()