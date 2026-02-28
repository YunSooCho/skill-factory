"""
Rakuraku BtoB Client - Japanese B2B E-commerce Platform
https://rakuraku-btob.jp/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class RakurakuBtobClient:
    """Complete client for Rakuraku BtoB API - Japanese B2B platform."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("RAKURAKU_BTOB_API_KEY")
        self.base_url = (base_url or os.getenv("RAKURAKU_BTOB_BASE_URL", "https://api.rakuraku-btob.jp/v1")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key required. Set RAKURAKU_BTOB_API_KEY")
        
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
    def list_products(self, page: int = 1, category: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if category:
            params["category"] = category
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._request("GET", f"products/{product_id}")
    
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "products", data=data)
    
    def update_product(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"products/{product_id}", data=data)
    
    # Orders
    def list_orders(self, page: int = 1, status: Optional[str] = None, customer_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if status:
            params["status"] = status
        if customer_id:
            params["customer_id"] = customer_id
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._request("GET", f"orders/{order_id}")
    
    def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "orders", data=data)
    
    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        return self._request("PUT", f"orders/{order_id}/status", data={"status": status})
    
    # B2B Customers (Business Clients)
    def list_customers(self, page: int = 1) -> Dict[str, Any]:
        return self._request("GET", "customers", params={"page": page, "per_page": 50})
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "customers", data=data)
    
    def update_customer(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"customers/{customer_id}", data=data)
    
    # Billing/Invoicing
    def list_invoices(self, page: int = 1, status: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if status:
            params["status"] = status
        return self._request("GET", "invoices", params=params)
    
    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        return self._request("GET", f"invoices/{invoice_id}")
    
    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "invoices", data=data)
    
    # Bulk Orders
    def create_bulk_order(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._request("POST", "orders/bulk", data={"products": products})
    
    # Inventory
    def get_stock_levels(self, product_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"product_id": product_id} if product_id else {}
        return self._request("GET", "inventory", params=params)
    
    def update_stock(self, product_id: str, quantity: int) -> Dict[str, Any]:
        return self._request("POST", f"products/{product_id}/stock", data={"quantity": quantity})
    
    # Categories
    def list_categories(self) -> Dict[str, Any]:
        return self._request("GET", "categories")
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()