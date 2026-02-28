"""
Commerce Robo Client - Japanese E-commerce Automation
https://commerce-robo.com/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class CommerceRoboClient:
    """Complete client for Commerce Robo API - Japanese e-commerce automation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("COMMERCE_ROBO_API_KEY")
        self.base_url = (base_url or os.getenv("COMMERCE_ROBO_BASE_URL", "https://api.commerce-robo.com/v1")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key required. Set COMMERCE_ROBO_API_KEY")
        
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
    
    # Products
    def list_products(self, page: int = 1, marketplace: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if marketplace:
            params["marketplace"] = marketplace
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._request("GET", f"products/{product_id}")
    
    def sync_product(self, product_id: str, marketplaces: List[str]) -> Dict[str, Any]:
        return self._request("POST", f"products/{product_id}/sync", data={"marketplaces": marketplaces})
    
    # Orders
    def list_orders(self, page: int = 1, status: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if status:
            params["status"] = status
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._request("GET", f"orders/{order_id}")
    
    def sync_order(self, order_id: str) -> Dict[str, Any]:
        return self._request("POST", f"orders/{order_id}/sync")
    
    # Marketplaces
    def list_marketplaces(self) -> Dict[str, Any]:
        return self._request("GET", "marketplaces")
    
    def connect_marketplace(self, marketplace: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"marketplaces/{marketplace}/connect", data=credentials)
    
    # Automation Rules
    def list_automation_rules(self) -> Dict[str, Any]:
        return self._request("GET", "automation/rules")
    
    def create_automation_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "automation/rules", data=rule_data)
    
    def update_automation_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"automation/rules/{rule_id}", data=rule_data)
    
    def delete_automation_rule(self, rule_id: str) -> None:
        self._request("DELETE", f"automation/rules/{rule_id}")
    
    # Inventory Sync
    def sync_inventory(self, product_id: str) -> Dict[str, Any]:
        return self._request("POST", f"inventory/{product_id}/sync")
    
    def bulk_sync_inventory(self, product_ids: List[str]) -> Dict[str, Any]:
        return self._request("POST", "inventory/bulk-sync", data={"product_ids": product_ids})
    
    # Tasks/Jobs
    def list_tasks(self, page: int = 1) -> Dict[str, Any]:
        return self._request("GET", "tasks", params={"page": page, "per_page": 50})
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        return self._request("GET", f"tasks/{task_id}")
    
    # Reports
    def get_sales_report(self, from_date: str, to_date: str) -> Dict[str, Any]:
        return self._request("GET", "reports/sales", params={"from_date": from_date, "to_date": to_date})
    
    def get_inventory_report(self) -> Dict[str, Any]:
        return self._request("GET", "reports/inventory")
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()