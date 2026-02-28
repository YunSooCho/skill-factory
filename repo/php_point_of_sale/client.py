"""
PHP Point of Sale Client - Open Source POS System
https://phppointofsale.com/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class PhppointofsaleClient:
    """Complete client for PHP Point of Sale API - Open source POS system."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("PHPPOS_API_KEY")
        self.username = username or os.getenv("PHPPOS_USERNAME")
        self.password = password or os.getenv("PHPPOS_PASSWORD")
        self.base_url = (base_url or os.getenv("PHPPOS_BASE_URL")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key and not (self.username and self.password):
            raise ValueError("API key or username/password required")
        
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({"X-API-KEY": self.api_key})
        else:
            # Basic auth
            import base64
            auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            self.session.headers.update({"Authorization": f"Basic {auth}"})
        
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _request(self, method: str, endpoint: str, data=None, params=None) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        response = self.session.request(
            method=method, url=url, json=data, params=params,
            timeout=self.timeout, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    # Items/Products
    def list_items(self, limit: int = 50, offset: int = 0, category_id: Optional[int] = None) -> Dict[str, Any]:
        params = {"limit": limit, "offset": offset}
        if category_id:
            params["category_id"] = category_id
        return self._request("GET", "items", params=params)
    
    def get_item(self, item_id: int) -> Dict[str, Any]:
        return self._request("GET", f"items/{item_id}")
    
    def create_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "items", data=data)
    
    def update_item(self, item_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"items/{item_id}", data=data)
    
    def delete_item(self, item_id: int) -> None:
        self._request("DELETE", f"items/{item_id}")
    
    # Sales/Orders
    def list_sales(self, limit: int = 50, offset: int = 0, date_from: Optional[str] = None) -> Dict[str, Any]:
        params = {"limit": limit, "offset": offset}
        if date_from:
            params["start_date"] = date_from
        return self._request("GET", "sales", params=params)
    
    def get_sale(self, sale_id: int) -> Dict[str, Any]:
        return self._request("GET", f"sales/{sale_id}")
    
    def create_sale(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "sales", data=data)
    
    def suspend_sale(self, sale_id: int) -> Dict[str, Any]:
        return self._request("POST", f"sales/{sale_id}/suspend")
    
    def unsuspend_sale(self, sale_id: int) -> Dict[str, Any]:
        return self._request("POST", f"sales/{sale_id}/unsuspend")
    
    # Customers
    def list_customers(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        return self._request("GET", "customers", params={"limit": limit, "offset": offset})
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "customers", data=data)
    
    def update_customer(self, customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"customers/{customer_id}", data=data)
    
    # Suppliers
    def list_suppliers(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        return self._request("GET", "suppliers", params={"limit": limit, "offset": offset})
    
    def get_supplier(self, supplier_id: int) -> Dict[str, Any]:
        return self._request("GET", f"suppliers/{supplier_id}")
    
    def create_supplier(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "suppliers", data=data)
    
    # Inventory
    def get_inventory(self, item_id: int) -> Dict[str, Any]:
        return self._request("GET", f"items/{item_id}/inventory")
    
    def adjust_inventory(self, item_id: int, quantity: int, reason: str) -> Dict[str, Any]:
        return self._request("POST", f"items/{item_id}/inventory/adjust", data={"quantity": quantity, "reason": reason})
    
    # Categories
    def list_categories(self) -> Dict[str, Any]:
        return self._request("GET", "categories")
    
    # Employees
    def list_employees(self) -> Dict[str, Any]:
        return self._request("GET", "employees")
    
    # Locations/Stores
    def list_locations(self) -> Dict[str, Any]:
        return self._request("GET", "locations")
    
    # Reports
    def get_daily_report(self, date: str) -> Dict[str, Any]:
        return self._request("GET", "reports/daily", params={"date": date})
    
    def get_sales_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._request("GET", "reports/sales", params={"start_date": start_date, "end_date": end_date})
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()