"""
Digistore Client - Digital Goods Platform
https://digistore24.com/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class DigistoreClient:
    """Complete client for Digistore24 API - Digital goods platform."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("DIGISTORE_API_KEY")
        self.base_url = (base_url or os.getenv("DIGISTORE_BASE_URL", "https://api.digistore24.com/v1")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key required. Set DIGISTORE_API_KEY")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, data=None, params=None) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        response = self.session.request(
            method=method, url=url, json=data, params=params,
            timeout=self.timeout, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    # Products (Digital Products)
    def list_products(self, page: int = 1, product_type: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if product_type:
            params["product_type"] = product_type
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._request("GET", f"products/{product_id}")
    
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "products", data=data)
    
    def update_product(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"products/{product_id}", data=data)
    
    def delete_product(self, product_id: str) -> None:
        self._request("DELETE", f"products/{product_id}")
    
    # Orders
    def list_orders(self, page: int = 1, status: Optional[str] = None, from_date: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._request("GET", f"orders/{order_id}")
    
    def refund_order(self, order_id: str, reason: str) -> Dict[str, Any]:
        return self._request("POST", f"orders/{order_id}/refund", data={"reason": reason})
    
    # Customers
    def list_customers(self, page: int = 1, email: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if email:
            params["email"] = email
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}")
    
    # Affiliates
    def list_affiliates(self, page: int = 1) -> Dict[str, Any]:
        return self._request("GET", "affiliates", params={"page": page, "per_page": 50})
    
    def get_affiliate(self, affiliate_id: str) -> Dict[str, Any]:
        return self._request("GET", f"affiliates/{affiliate_id}")
    
    # Sales/Commissions
    def list_sales(self, page: int = 1, product_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if product_id:
            params["product_id"] = product_id
        return self._request("GET", "sales", params=params)
    
    # Payouts
    def list_payouts(self, page: int = 1) -> Dict[str, Any]:
        return self._request("GET", "payouts", params={"page": page, "per_page": 50})
    
    # Webhooks
    def list_webhooks(self) -> Dict[str, Any]:
        return self._request("GET", "webhooks")
    
    def create_webhook(self, url: str, events: List[str], secret: Optional[str] = None) -> Dict[str, Any]:
        data = {"url": url, "events": events}
        if secret:
            data["secret"] = secret
        return self._request("POST", "webhooks", data=data)
    
    def delete_webhook(self, webhook_id: str) -> None:
        self._request("DELETE", f"webhooks/{webhook_id}")
    
    # Reports
    def get_revenue_report(self, from_date: str, to_date: str) -> Dict[str, Any]:
        return self._request("GET", "reports/revenue", params={"from_date": from_date, "to_date": to_date})
    
    def get_affiliate_report(self, from_date: str, to_date: str) -> Dict[str, Any]:
        return self._request("GET", "reports/affiliate", params={"from_date": from_date, "to_date": to_date})
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()