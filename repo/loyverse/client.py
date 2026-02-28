"""
Loyverse Client - REST API Implementation
Loyverse POS API documentation: https://help.loyverse.com/help/en/Loyverse-POS-API
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class LoyverseClient:
    """
    Complete client for Loyverse POS API.
    Supports Items, Categories, Customers, Orders, Inventory, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Loyverse client.
        
        Args:
            api_key: API key (from env: LOYVERSE_API_KEY)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            LOYVERSE_API_KEY: Your Loyverse API key
        """
        self.api_key = api_key or os.getenv("LOYVERSE_API_KEY")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set LOYVERSE_API_KEY environment variable."
            )
        
        self.base_url = "https://loyverse.com/api"
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Loyverse API.
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        session_headers = dict(self.session.headers)
        if headers:
            session_headers.update(headers)
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=session_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    # ============================================================================
    # Items / Products
    # ============================================================================
    
    def list_items(self, start_index: int = 0, count: int = 100) -> Dict[str, Any]:
        """
        List items in inventory.
        
        Args:
            start_index: Pagination start index
            count: Number of items to return (max 100)
            
        Returns:
            Items response
        """
        params = {
            "start_index": start_index,
            "count": min(count, 100)
        }
        return self._request("GET", "items", params=params)
    
    def get_item(self, item_id: str) -> Dict[str, Any]:
        """
        Get details of a specific item.
        """
        return self._request("GET", f"items/{item_id}")
    
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new item.
        
        Args:
            item_data: Item data dict:
                - name: Item name (required)
                - category_id: Category ID
                - sku: SKU
                - price: Unit price
                - cost: Unit cost
                - tax_rate_id: Tax rate ID
                - unit_id: Measurement unit ID
                - mod_group_ids: Modifier group IDs
                - is_active: Active status
                
        Returns:
            Created item response
        """
        return self._request("POST", "items", data=item_data)
    
    def update_item(self, item_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing item.
        """
        return self._request("PUT", f"items/{item_id}", data=item_data)
    
    def delete_item(self, item_id: str) -> None:
        """
        Delete an item.
        """
        self._request("DELETE", f"items/{item_id}")
    
    # ============================================================================
    # Categories
    # ============================================================================
    
    def list_categories(self) -> List[Dict[str, Any]]:
        """
        List all item categories.
        """
        return self._request("GET", "categories")
    
    def get_category(self, category_id: str) -> Dict[str, Any]:
        """
        Get details of a specific category.
        """
        return self._request("GET", f"categories/{category_id}")
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new category.
        
        Args:
            category_data: Category data:
                - name: Category name (required)
                - color_hex: Color hex code
                
        Returns:
            Created category response
        """
        return self._request("POST", "categories", data=category_data)
    
    def update_category(self, category_id: str, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a category.
        """
        return self._request("PUT", f"categories/{category_id}", data=category_data)
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(self, start_index: int = 0, count: int = 100) -> Dict[str, Any]:
        """
        List customers.
        """
        params = {
            "start_index": start_index,
            "count": min(count, 100)
        }
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Get details of a specific customer.
        """
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer data:
                - name: Customer name (required)
                - phone: Phone number
                - email: Email address
                - note: Customer note
                - points: Loyalty points
                - comment: Additional comment
        """
        return self._request("POST", "customers", data=customer_data)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a customer.
        """
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    def delete_customer(self, customer_id: str) -> None:
        """Delete a customer."""
        self._request("DELETE", f"customers/{customer_id}")
    
    def add_customer_points(
        self,
        customer_id: str,
        points: int,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add loyalty points to a customer.
        
        Args:
            customer_id: Customer ID
            points: Points to add (positive or negative)
            reason: Reason for points adjustment
            
        Returns:
            Updated customer
        """
        data = {
            "points_change": points
        }
        if reason:
            data["comment"] = reason
        
        return self._request("POST", f"customers/{customer_id}/add_points", data=data)
    
    # ============================================================================
    # Orders
    # ============================================================================
    
    def list_orders(
        self,
        start_index: int = 0,
        count: int = 100,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List orders.
        
        Args:
            start_index: Pagination start index
            count: Number of orders (max 100)
            from_date: Filter orders from this date (unix timestamp)
            to_date: Filter orders to this date (unix timestamp)
            
        Returns:
            Orders response
        """
        params = {
            "start_index": start_index,
            "count": min(count, 100)
        }
        
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get details of a specific order.
        """
        return self._request("GET", f"orders/{order_id}")
    
    # ============================================================================
    # Inventory Tracks
    # ============================================================================
    
    def list_inventory_tracks(
        self,
        start_index: int = 0,
        count: int = 100
    ) -> Dict[str, Any]:
        """
        List inventory tracks (stock movements).
        """
        params = {
            "start_index": start_index,
            "count": min(count, 100)
        }
        return self._request("GET", "inventory_tracks", params=params)
    
    def get_inventory_track(self, track_id: str) -> Dict[str, Any]:
        """
        Get details of an inventory track.
        """
        return self._request("GET", f"inventory_tracks/{track_id}")
    
    # ============================================================================
    # Stores / Locations
    # ============================================================================
    
    def list_stores(self) -> List[Dict[str, Any]]:
        """
        List all stores.
        """
        return self._request("GET", "stores")
    
    def get_store(self, store_id: str) -> Dict[str, Any]:
        """
        Get details of a store.
        """
        return self._request("GET", f"stores/{store_id}")
    
    # ============================================================================
    # Tax Rates
    # ============================================================================
    
    def list_tax_rates(self) -> List[Dict[str, Any]]:
        """
        List tax rates.
        """
        return self._request("GET", "tax_rates")
    
    # ============================================================================
    # Units of Measurement
    # ============================================================================
    
    def list_units(self) -> List[Dict[str, Any]]:
        """
        List measurement units.
        """
        return self._request("GET", "units")
    
    # ============================================================================
    # Modifier Groups
    # ============================================================================
    
    def list_modifier_groups(self) -> List[Dict[str, Any]]:
        """
        List modifier groups.
        """
        return self._request("GET", "modifier_groups")
    
    def get_modifier_group(self, group_id: str) -> Dict[str, Any]:
        """
        Get details of a modifier group.
        """
        return self._request("GET", f"modifier_groups/{group_id}")
    
    # ============================================================================
    # Discounts
    # ============================================================================
    
    def list_discounts(self) -> List[Dict[str, Any]]:
        """
        List discounts.
        """
        return self._request("GET", "discounts")
    
    def get_discount(self, discount_id: str) -> Dict[str, Any]:
        """
        Get details of a discount.
        """
        return self._request("GET", f"discounts/{discount_id}")
    
    # ============================================================================
    # Payment Types
    # ============================================================================
    
    def list_payment_types(self) -> List[Dict[str, Any]]:
        """
        List payment types.
        """
        return self._request("GET", "payment_types")
    
    # ============================================================================
    # Shifts (Employee Sessions)
    # ============================================================================
    
    def list_shifts(
        self,
        start_index: int = 0,
        count: int = 100
    ) -> Dict[str, Any]:
        """
        List employee shifts.
        """
        params = {
            "start_index": start_index,
            "count": min(count, 100)
        }
        return self._request("GET", "shifts", params=params)
    
    def get_shift(self, shift_id: str) -> Dict[str, Any]:
        """
        Get details of a shift.
        """
        return self._request("GET", f"shifts/{shift_id}")
    
    def close_shift(self, shift_id: str) -> Dict[str, Any]:
        """
        Close an open shift.
        """
        return self._request("POST", f"shifts/{shift_id}/close")
    
    # ============================================================================
    # Receipt Templates
    # ============================================================================
    
    def list_receipt_templates(self) -> List[Dict[str, Any]]:
        """
        List receipt templates.
        """
        return self._request("GET", "receipt_templates")
    
    def get_receipt_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get details of a receipt template.
        """
        return self._request("GET", f"receipt_templates/{template_id}")
    
    # ============================================================================
    # Accounting Categories
    # ============================================================================
    
    def list_accounting_categories(self) -> List[Dict[str, Any]]:
        """
        List accounting categories (for export).
        """
        return self._request("GET", "accounting_categories")
    
    # ============================================================================
    # Inventory Levels
    # ============================================================================
    
    def get_inventory_levels(
        self,
        item_id: Optional[str] = None,
        store_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get current inventory levels.
        
        Args:
            item_id: Filter by item ID
            store_id: Filter by store ID
            
        Returns:
            Inventory levels response
        """
        params = {}
        if item_id:
            params["item_id"] = item_id
        if store_id:
            params["store_id"] = store_id
        
        return self._request("GET", "inventory_levels", params=params)
    
    def adjust_inventory(
        self,
        item_id: str,
        quantity: float,
        store_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Adjust inventory quantity.
        
        Args:
            item_id: Item ID
            quantity: Quantity change (positive or negative)
            store_id: Store ID
            reason: Adjustment reason (Sale, Purchase, Inventory, Return, etc.)
            
        Returns:
            Inventory track record
        """
        data = {
            "item_id": item_id,
            "quantity": quantity,
            "store_id": store_id,
            "reason": reason
        }
        
        return self._request("POST", "inventory_adjustments", data=data)
    
    # ============================================================================
    # Account Info
    # ============================================================================
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        """
        return self._request("GET", "merchant/account")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()