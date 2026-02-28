"""
Shopify Client - REST Admin API Implementation
Shopify Store API documentation: https://shopify.dev/api/admin-rest
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ShopifyClient:
    """
    Complete client for Shopify Admin REST API.
    Supports Products, Orders, Customers, Inventory, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        password: Optional[str] = None,
        store_name: Optional[str] = None,
        access_token: Optional[str] = None,
        version: str = "2024-01",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Shopify client.
        
        Args:
            api_key: API key (from env: SHOPIFY_API_KEY)
            password: API password (from env: SHOPIFY_PASSWORD)
            store_name: Store name (from env: SHOPIFY_STORE_NAME)
            access_token: Admin API access token (from env: SHOPIFY_ACCESS_TOKEN)
            version: API version
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            SHOPIFY_STORE_NAME: Your store name (e.g., "mystore" from mystore.myshopify.com)
            SHOPIFY_ACCESS_TOKEN: Admin API access token
            SHOPIFY_API_KEY: API key (if using basic auth)
            SHOPIFY_PASSWORD: API password (if using basic auth)
        """
        self.store_name = store_name or os.getenv("SHOPIFY_STORE_NAME")
        self.access_token = access_token or os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.api_key = api_key or os.getenv("SHOPIFY_API_KEY")
        self.password = password or os.getenv("SHOPIFY_PASSWORD")
        self.version = version
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.store_name:
            raise ValueError(
                "Store name is required. Set SHOPIFY_STORE_NAME environment variable."
            )
        
        if not self.access_token and not (self.api_key and self.password):
            raise ValueError(
                "Either access_token or (api_key + password) is required. "
                "Set SHOPIFY_ACCESS_TOKEN or (SHOPIFY_API_KEY + SHOPIFY_PASSWORD)."
            )
        
        self.base_url = f"https://{self.store_name}.myshopify.com/admin/api/{self.version}"
        
        self.session = requests.Session()
        
        # Setup authentication
        if self.access_token:
            self.session.headers.update({
                "X-Shopify-Access-Token": self.access_token
            })
        else:
            self.session.auth = (self.api_key, self.password)
        
        self.session.headers.update({
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
        Make HTTP request to Shopify API.
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
    # Products
    # ============================================================================
    
    def list_products(
        self,
        limit: int = 50,
        since_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        created_at_min: Optional[str] = None,
        created_at_max: Optional[str] = None,
        updated_at_min: Optional[str] = None,
        updated_at_max: Optional[str] = None,
        vendor: Optional[str] = None,
        product_type: Optional[str] = None,
        status: str = "active"
    ) -> Dict[str, Any]:
        """
        List products.
        
        Args:
            limit: Number of results (max 250)
            since_id: Restrict results to after the specified ID
            collection_id: Filter by collection
            created_at_min: Show products created after this date
            created_at_max: Show products created before this date
            updated_at_min: Show products updated after this date
            updated_at_max: Show products updated before this date
            vendor: Filter by product vendor
            product_type: Filter by product type
            status: Filter by status (active, archived, draft)
            
        Returns:
            Products response dict
        """
        params = {
            "limit": min(limit, 250),
            "status": status
        }
        
        if since_id:
            params["since_id"] = since_id
        if collection_id:
            params["collection_id"] = collection_id
        if created_at_min:
            params["created_at_min"] = created_at_min
        if created_at_max:
            params["created_at_max"] = created_at_max
        if updated_at_min:
            params["updated_at_min"] = updated_at_min
        if updated_at_max:
            params["updated_at_max"] = updated_at_max
        if vendor:
            params["vendor"] = vendor
        if product_type:
            params["product_type"] = product_type
        
        return self._request("GET", "products.json", params=params)
    
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Get a specific product by ID.
        """
        return self._request("GET", f"products/{product_id}.json")
    
    def count_products(
        self,
        vendor: Optional[str] = None,
        product_type: Optional[str] = None,
        collection_id: Optional[str] = None,
        created_at_min: Optional[str] = None,
        created_at_max: Optional[str] = None,
        updated_at_min: Optional[str] = None,
        updated_at_max: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Count products.
        """
        params = {}
        if vendor:
            params["vendor"] = vendor
        if product_type:
            params["product_type"] = product_type
        if collection_id:
            params["collection_id"] = collection_id
        if created_at_min:
            params["created_at_min"] = created_at_min
        if created_at_max:
            params["created_at_max"] = created_at_max
        if updated_at_min:
            params["updated_at_min"] = updated_at_min
        if updated_at_max:
            params["updated_at_max"] = updated_at_max
        
        return self._request("GET", "products/count.json", params=params)
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product.
        
        Args:
            product_data: Product data dict with required fields:
                - title: Product title
                - body_html: HTML description
                - vendor: Vendor name
                - product_type: Product type
                - variants: List of variant objects
                - images: List of image objects
                
        Returns:
            Created product response
        """
        return self._request("POST", "products.json", data={"product": product_data})
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product.
        """
        return self._request("PUT", f"products/{product_id}.json", data={"product": product_data})
    
    def delete_product(self, product_id: int) -> None:
        """
        Delete a product.
        """
        self._request("DELETE", f"products/{product_id}.json")
    
    # ============================================================================
    # Orders
    # ============================================================================
    
    def list_orders(
        self,
        limit: int = 50,
        status: Optional[str] = None,
        fulfillment_status: Optional[str] = None,
        created_at_min: Optional[str] = None,
        created_at_max: Optional[str] = None,
        updated_at_min: Optional[str] = None,
        updated_at_max: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List orders.
        
        Args:
            limit: Number of results (max 250)
            status: Filter by status (open, closed, cancelled, any)
            fulfillment_status: Filter by fulfillment status (fulfilled, null, partial, rest)
            created_at_min: Show orders created after this date
            created_at_max: Show orders created before this date
            updated_at_min: Show orders updated after this date
            updated_at_max: Show orders updated before this date
            
        Returns:
            Orders response dict
        """
        params = {"limit": min(limit, 250)}
        
        if status:
            params["status"] = status
        if fulfillment_status:
            params["fulfillment_status"] = fulfillment_status
        if created_at_min:
            params["created_at_min"] = created_at_min
        if created_at_max:
            params["created_at_max"] = created_at_max
        if updated_at_min:
            params["updated_at_min"] = updated_at_min
        if updated_at_max:
            params["updated_at_max"] = updated_at_max
        
        return self._request("GET", "orders.json", params=params)
    
    def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Get a specific order by ID.
        """
        return self._request("GET", f"orders/{order_id}.json")
    
    def count_orders(
        self,
        status: Optional[str] = None,
        fulfillment_status: Optional[str] = None,
        created_at_min: Optional[str] = None,
        created_at_max: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Count orders.
        """
        params = {}
        if status:
            params["status"] = status
        if fulfillment_status:
            params["fulfillment_status"] = fulfillment_status
        if created_at_min:
            params["created_at_min"] = created_at_min
        if created_at_max:
            params["created_at_max"] = created_at_max
        
        return self._request("GET", "orders/count.json", params=params)
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            order_data: Order data dict with required fields:
                - line_items: List of line item objects
                - customer: Customer object (optional)
                - billing_address: Billing address (optional)
                - shipping_address: Shipping address (optional)
                - financial_status: Payment status (pending, paid, authorized, partially_paid, voided)
                
        Returns:
            Created order response
        """
        return self._request("POST", "orders.json", data={"order": order_data})
    
    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing order.
        """
        return self._request("PUT", f"orders/{order_id}.json", data={"order": order_data})
    
    def close_order(self, order_id: int) -> Dict[str, Any]:
        """
        Close an order.
        """
        return self._request("POST", f"orders/{order_id}/close.json")
    
    def open_order(self, order_id: int) -> Dict[str, Any]:
        """
        Reopen a closed order.
        """
        return self._request("POST", f"orders/{order_id}/open.json")
    
    def cancel_order(
        self,
        order_id: int,
        reason: Optional[str] = None,
        email: bool = True,
        restock: bool = True
    ) -> Dict[str, Any]:
        """
        Cancel an order.
        """
        data = {}
        if reason:
            data["reason"] = reason
        data["email"] = email
        data["restock"] = restock
        
        return self._request("POST", f"orders/{order_id}/cancel.json", data=data)
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(
        self,
        limit: int = 50,
        since_id: Optional[str] = None,
        created_at_min: Optional[str] = None,
        created_at_max: Optional[str] = None,
        updated_at_min: Optional[str] = None,
        updated_at_max: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List customers.
        """
        params = {"limit": min(limit, 250)}
        
        if since_id:
            params["since_id"] = since_id
        if created_at_min:
            params["created_at_min"] = created_at_min
        if created_at_max:
            params["created_at_max"] = created_at_max
        if updated_at_min:
            params["updated_at_min"] = updated_at_min
        if updated_at_max:
            params["updated_at_max"] = updated_at_max
        
        return self._request("GET", "customers.json", params=params)
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Get a specific customer by ID.
        """
        return self._request("GET", f"customers/{customer_id}.json")
    
    def search_customers(self, query: str) -> Dict[str, Any]:
        """
        Search for customers.
        
        Args:
            query: Search query string
            
        Returns:
            Search results
        """
        return self._request("GET", "customers/search.json", params={"query": query})
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer data dict with fields like:
                - first_name: Customer's first name
                - last_name: Customer's last name
                - email: Customer's email
                - phone: Customer's phone
                - accepts_marketing: Marketing opt-in
                
        Returns:
            Created customer response
        """
        return self._request("POST", "customers.json", data={"customer": customer_data})
    
    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing customer.
        """
        return self._request("PUT", f"customers/{customer_id}.json", data={"customer": customer_data})
    
    def delete_customer(self, customer_id: int) -> None:
        """
        Delete a customer.
        """
        self._request("DELETE", f"customers/{customer_id}.json")
    
    # ============================================================================
    # Inventory
    # ============================================================================
    
    def list_inventory_levels(
        self,
        inventory_item_ids: Optional[List[str]] = None,
        location_ids: Optional[List[str]] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        List inventory levels.
        
        Args:
            inventory_item_ids: Filter by inventory item IDs
            location_ids: Filter by location IDs
            limit: Number of results
            
        Returns:
            Inventory levels response
        """
        params = {"limit": min(limit, 250)}
        
        if inventory_item_ids:
            params["inventory_item_ids"] = ",".join(inventory_item_ids)
        if location_ids:
            params["location_ids"] = ",".join(location_ids)
        
        return self._request("GET", "inventory_levels.json", params=params)
    
    def update_inventory_levels(
        self,
        inventory_item_id: str,
        location_id: str,
        available: int
    ) -> Dict[str, Any]:
        """
        Adjust inventory level.
        """
        data = {
            "location_id": location_id,
            "inventory_item_id": inventory_item_id,
            "available_adjustment": available
        }
        
        return self._request("POST", "inventory_levels/adjust.json", data=data)
    
    # ============================================================================
    # Collections
    # ============================================================================
    
    def list_collections(
        self,
        limit: int = 50,
        since_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List collections.
        """
        params = {"limit": min(limit, 250)}
        if since_id:
            params["since_id"] = since_id
        
        return self._request("GET", "custom_collections.json", params=params)
    
    def get_collection(self, collection_id: int) -> Dict[str, Any]:
        """
        Get a specific collection.
        """
        return self._request("GET", f"custom_collections/{collection_id}.json")
    
    # ============================================================================
    # Locations
    # ============================================================================
    
    def list_locations(self) -> Dict[str, Any]:
        """
        List all locations.
        """
        return self._request("GET", "locations.json")
    
    def get_location(self, location_id: int) -> Dict[str, Any]:
        """
        Get a specific location.
        """
        return self._request("GET", f"locations/{location_id}.json")
    
    # ============================================================================
    # Metafields
    # ============================================================================
    
    def list_product_metafields(
        self,
        product_id: int,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        List metafields for a product.
        """
        params = {"limit": min(limit, 250)}
        return self._request("GET", f"products/{product_id}/metafields.json", params=params)
    
    def create_product_metafield(
        self,
        product_id: int,
        namespace: str,
        key: str,
        value: str,
        value_type: str = "string"
    ) -> Dict[str, Any]:
        """
        Create a metafield for a product.
        """
        data = {
            "metafield": {
                "namespace": namespace,
                "key": key,
                "value": value,
                "type": value_type
            }
        }
        
        return self._request("POST", f"products/{product_id}/metafields.json", data=data)
    
    # ============================================================================
    # Webhooks
    # ============================================================================
    
    def list_webhooks(self) -> Dict[str, Any]:
        """
        List all webhooks.
        """
        return self._request("GET", "webhooks.json")
    
    def create_webhook(
        self,
        topic: str,
        address: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            topic: Webhook topic (e.g., "orders/create", "products/update")
            address: Webhook URL
            format: Response format (json or xml)
            
        Returns:
            Created webhook response
        """
        data = {
            "webhook": {
                "topic": topic,
                "address": address,
                "format": format
            }
        }
        
        return self._request("POST", "webhooks.json", data=data)
    
    def delete_webhook(self, webhook_id: int) -> None:
        """
        Delete a webhook.
        """
        self._request("DELETE", f"webhooks/{webhook_id}.json")
    
    # ============================================================================
    # Shop Info
    # ============================================================================
    
    def get_shop_info(self) -> Dict[str, Any]:
        """
        Get shop information.
        """
        return self._request("GET", "shop.json")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()