import requests
from typing import Dict, List, Optional, Any


class WeclappClient:
    """Client for Weclapp cloud ERP API."""

    BASE_URL = "https://www.weclapp.com/webapp/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Weclapp client.

        Args:
            api_key: Your Weclapp API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "AuthenticationToken": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Weclapp API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_articles(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Get all articles/products."""
        return self._request("GET", f"/article?page={page}&pageSize={page_size}")

    def get_article(self, article_id: str) -> Dict[str, Any]:
        """Get article details."""
        return self._request("GET", f"/article/id/{article_id}")

    def create_article(self, title: str, description: str = None,
                      item_number: str = None, price: float = None) -> Dict[str, Any]:
        """Create article."""
        data = {"title": title}
        if description:
            data["description"] = description
        if item_number:
            data["itemNumber"] = item_number
        if price:
            data["price"] = price
        return self._request("POST", "/article", data=data)

    def update_article(self, article_id: str, data: Dict) -> Dict[str, Any]:
        """Update article."""
        return self._request("PUT", f"/article/id/{article_id}", data)

    def delete_article(self, article_id: str) -> Dict[str, Any]:
        """Delete article."""
        return self._request("DELETE", f"/article/id/{article_id}")

    def get_orders(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Get sales orders."""
        return self._request("GET", f"/salesOrder?page={page}&pageSize={page_size}")

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order details."""
        return self._request("GET", f"/salesOrder/id/{order_id}")

    def create_order(self, order_items: List[Dict], status: str = None) -> Dict[str, Any]:
        """Create sales order."""
        data = {"orderItems": order_items}
        if status:
            data["orderStatus"] = status
        return self._request("POST", "/salesOrder", data=data)

    def update_order(self, order_id: str, data: Dict) -> Dict[str, Any]:
        """Update order."""
        return self._request("PUT", f"/salesOrder/id/{order_id}", data)

    def delete_order(self, order_id: str) -> Dict[str, Any]:
        """Delete order."""
        return self._request("DELETE", f"/salesOrder/id/{order_id}")

    def get_invoices(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Get invoices."""
        return self._request("GET", f"/invoice?page={page}&pageSize={page_size}")

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details."""
        return self._request("GET", f"/invoice/id/{invoice_id}")

    def create_invoice(self, invoice_items: List[Dict], title: str) -> Dict[str, Any]:
        """Create invoice."""
        data = {
            "invoiceItems": invoice_items,
            "title": title
        }
        return self._request("POST", "/invoice", data=data)

    def get_customers(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Get customers."""
        return self._request("GET", f"/customer?page={page}&pageSize={page_size}")

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", f"/customer/id/{customer_id}")

    def create_customer(self, name: str, email: str = None, phone: str = None) -> Dict[str, Any]:
        """Create customer."""
        data = {"name": name}
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        return self._request("POST", "/customer", data=data)

    def get_stock(self, article_id: str = None) -> Dict[str, Any]:
        """Get stock levels."""
        if article_id:
            return self._request("GET", f"/stock/article/id/{article_id}")
        return self._request("GET", "/stock")

    def get_purchase_orders(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Get purchase orders."""
        return self._request("GET", f"/purchaseOrder?page={page}&pageSize={page_size}")