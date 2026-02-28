"""
Printify Client - REST API Implementation
Printify API documentation: https://developers.printify.com/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class PrintifyClient:
    """
    Complete client for Printify API.
    Supports Shops, Products, Orders, Uploads, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Printify client.
        
        Args:
            api_key: API key (from env: PRINTIFY_API_KEY)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            PRINTIFY_API_KEY: Your Printify API token
        """
        self.api_key = api_key or os.getenv("PRINTIFY_API_KEY")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set PRINTIFY_API_KEY environment variable."
            )
        
        self.base_url = "https://api.printify.com/v1"
        
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
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Printify API.
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        session_headers = dict(self.session.headers)
        if files:
            # Remove Content-Type for file uploads (let requests set it)
            session_headers = {k: v for k, v in session_headers.items() if k != "Content-Type"}
        
        if headers:
            session_headers.update(headers)
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            files=files,
            headers=session_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    # ============================================================================
    # Shops
    # ============================================================================
    
    def list_shops(self) -> List[Dict[str, Any]]:
        """
        List all shops connected to your account.
        """
        return self._request("GET", "shops.json")
    
    def get_shop(self, shop_id: str) -> Dict[str, Any]:
        """
        Get details of a specific shop.
        """
        return self._request("GET", f"shops/{shop_id}.json")
    
    # ============================================================================
    # Products
    # ============================================================================
    
    def list_products(self, shop_id: str) -> List[Dict[str, Any]]:
        """
        List all products in a shop.
        """
        return self._request("GET", f"shops/{shop_id}/products.json")
    
    def get_product(self, shop_id: str, product_id: str) -> Dict[str, Any]:
        """
        Get details of a specific product.
        """
        return self._request("GET", f"shops/{shop_id}/products/{product_id}.json")
    
    def create_product(self, shop_id: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in a shop.
        
        Args:
            shop_id: Shop ID
            product_data: Product data dict:
                - title: Product title
                - description: HTML description
                - tags: List of tags
                - variants: List of variant configurations
                - images: List of image configurations
                
        Returns:
            Created product response
        """
        return self._request("POST", f"shops/{shop_id}/products.json", data=product_data)
    
    def update_product(self, shop_id: str, product_id: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product.
        """
        return self._request("PUT", f"shops/{shop_id}/products/{product_id}.json", data=product_data)
    
    def delete_product(self, shop_id: str, product_id: str) -> None:
        """
        Delete a product. This action cannot be undone.
        """
        self._request("DELETE", f"shops/{shop_id}/products/{product_id}.json")
    
    def publish_product(self, shop_id: str, product_id: str, external: bool = False) -> Dict[str, Any]:
        """
        Publish a product to sales channel.
        
        Args:
            shop_id: Shop ID
            product_id: Product ID
            external: True to publish to external sales channels
            
        Returns:
            Publish status including external ID
        """
        data = {"external": external}
        return self._request("POST", f"shops/{shop_id}/products/{product_id}/publish.json", data=data)
    
    def unpublish_product(self, shop_id: str, product_id: str) -> None:
        """
        Unpublish a product from sales channels.
        """
        self._request("POST", f"shops/{shop_id}/products/{product_id}/unpublish.json")
    
    def set_product_visibility(self, shop_id: str, product_id: str, visible: bool) -> None:
        """
        Set product visibility in store.
        """
        data = {"visible": visible}
        self._request("PUT", f"shops/{shop_id}/products/{product_id}/visibility.json", data=data)
    
    # ============================================================================
    # Orders
    # ============================================================================
    
    def list_orders(self, shop_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all orders in a shop.
        
        Args:
            shop_id: Shop ID
            status: Filter by status (draft, processing())
            
        Returns:
            List of orders
        """
        params = {}
        if status:
            params["status"] = status
        
        return self._request("GET", f"shops/{shop_id}/orders.json", params=params)
    
    def get_order(self, shop_id: str, order_id: str) -> Dict[str, Any]:
        """
        Get details of a specific order.
        """
        return self._request("GET", f"shops/{shop_id}/orders/{order_id}.json")
    
    def create_order(
        self,
        shop_id: str,
        order_data: Dict[str, Any],
        send_shipping_notification: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            shop_id: Shop ID
            order_data: Order data dict:
                - external_id: Order ID from e-commerce platform
                - line_items: List of line items with:
                    - product_id: Printify product ID
                    - variant_id: Printify variant ID
                    - quantity: Item quantity
                - shipping_method: Shipping method ID
                - address_to: Shipping address dict
                - total_price: Total order amount
                - currency: Currency code
            send_shipping_notification: Send shipping confirmation email
            
        Returns:
            Created order response
        """
        params = {"send_shipping_notification": str(send_shipping_notification).lower()}
        return self._request("POST", f"shops/{shop_id}/orders.json", data=order_data, params=params)
    
    def submit_order_for_production(self, shop_id: str, order_id: str) -> Dict[str, Any]:
        """
        Submit a draft order for production.
        """
        return self._request("POST", f"shops/{shop_id}/orders/{order_id}/submit_for_production.json")
    
    def calculate_shipping_cost(self, shop_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate shipping cost for an order.
        """
        return self._request("POST", f"shops/{shop_id}/orders/shipping.json", data=order_data)
    
    def get_order_shipment_info(self, shop_id: str, order_id: str) -> Dict[str, Any]:
        """
        Get shipment tracking information for an order.
        """
        return self._request("GET", f"shops/{shop_id}/orders/{order_id}/shipment_info.json")
    
    # ============================================================================
    # Blueprints / Catalog
    # ============================================================================
    
    def list_blueprints(self) -> List[Dict[str, Any]]:
        """
        List all available product blueprints.
        """
        return self._request("GET", "catalog/blueprints.json")
    
    def get_blueprint(self, blueprint_id: str) -> Dict[str, Any]:
        """
        Get details of a specific blueprint.
        """
        return self._request("GET", f"catalog/blueprints/{blueprint_id}.json")
    
    def list_print_providers(self, blueprint_id: str) -> List[Dict[str, Any]]:
        """
        List print providers available for a blueprint.
        
        Args:
            blueprint_id: Blueprint ID
            
        Returns:
            List of print providers with their variants
        """
        return self._request("GET", f"catalog/blueprints/{blueprint_id}/print_providers.json")
    
    def get_print_provider_variants(
        self,
        blueprint_id: str,
        print_provider_id: str
    ) -> Dict[str, Any]:
        """
        Get variant configurations for a print provider.
        """
        return self._request(
            "GET",
            f"catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/variants.json"
        )
    
    def get_print_provider_mockups(
        self,
        blueprint_id: str,
        print_provider_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get available mockup configurations.
        """
        return self._request(
            "GET",
            f"catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/mockups.json"
        )
    
    # ============================================================================
    # File Uploads
    # ============================================================================
    
    def upload_image(self, file_path: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload an image file to Printify.
        
        Args:
            file_path: Path to the image file
            file_name: Optional custom file name
            
        Returns:
            Upload response with image URL
        """
        import os as os_module
        
        filename = file_name or os_module.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (filename, f, 'image/jpeg')
            }
            return self._request("POST", "uploads/images.json", files=files)
    
    def upload_image_from_url(self, image_url: str, file_name: str) -> Dict[str, Any]:
        """
        Upload an image from a URL.
        """
        data = {
            "url": image_url,
            "file_name": file_name
        }
        return self._request("POST", "uploads/images.json", data=data)
    
    # ============================================================================
    # Product Templates
    # ============================================================================
    
    def list_print_providers_for_blueprint(self, blueprint_id: str) -> List[Dict[str, Any]]:
        """
        Get all print providers for a blueprint with their variants and mockups.
        """
        return self.list_print_providers(blueprint_id)
    
    # ============================================================================
    # Webhooks
    # ============================================================================
    
    def list_webhooks(self, shop_id: str) -> List[Dict[str, Any]]:
        """
        List all webhooks for a shop.
        """
        return self._request("GET", f"shops/{shop_id}/webhooks.json")
    
    def get_webhook(self, shop_id: str, webhook_id: str) -> Dict[str, Any]:
        """
        Get a specific webhook.
        """
        return self._request("GET", f"shops/{shop_id}/webhooks/{webhook_id}.json")
    
    def create_webhook(
        self,
        shop_id: str,
        topic: str,
        url: str,
        signing_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook for a shop.
        
        Args:
            shop_id: Shop ID
            topic: Event topic (order.created, order.updated, order.fulfilled)
            url: Webhook URL
            signing_key: Optional signing key for event verification
            
        Returns:
            Created webhook response
        """
        data = {
            "topic": topic,
            "url": url
        }
        if signing_key:
            data["signing_key"] = signing_key
        
        return self._request("POST", f"shops/{shop_id}/webhooks.json", data=data)
    
    def delete_webhook(self, shop_id: str, webhook_id: str) -> None:
        """
        Delete a webhook.
        """
        self._request("DELETE", f"shops/{shop_id}/webhooks/{webhook_id}.json")
    
    # ============================================================================
    # Store Settings
    # ============================================================================
    
    def get_store_settings(self, shop_id: str) -> Dict[str, Any]:
        """
        Get store settings.
        """
        return self._request("GET", f"shops/{shop_id}/settings.json")
    
    def update_store_settings(self, shop_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update store settings.
        """
        return self._request("PUT", f"shops/{shop_id}/settings.json", data=settings)
    
    # ============================================================================
    # Catalog Filters
    # ============================================================================
    
    def filter_blueprints(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Filter blueprints with pagination.
        
        Args:
            limit: Number of results
            offset: Pagination offset
            category_id: Filter by category ID
            
        Returns:
            Filtered blueprints
        """
        params = {
            "limit": min(limit, 100),
            "offset": offset
        }
        
        if category_id:
            params["category_id"] = category_id
        
        return self._request("GET", "catalog/blueprints.json", params=params)
    
    def get_blueprint_print_providers(
        self,
        blueprint_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get print providers for blueprint with pagination.
        """
        params = {
            "limit": min(limit, 100),
            "offset": offset
        }
        return self._request(
            "GET",
            f"catalog/blueprints/{blueprint_id}/print_providers.json",
            params=params
        )
    
    # ============================================================================
    # Order Actions
    # ============================================================================
    
    def cancel_order(self, shop_id: str, order_id: str) -> None:
        """
        Cancel an order.
        """
        self._request("POST", f"shops/{shop_id}/orders/{order_id}/cancel.json")
    
    def update_order_shipping_info(
        self,
        shop_id: str,
        order_id: str,
        shipping_address: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update shipping address for an order.
        
        Args:
            shop_id: Shop ID
            order_id: Order ID (must draft status)
            shipping_address: New shipping address
            
        Returns:
            Updated order
        """
        return self._request(
            "PUT",
            f"shops/{shop_id}/orders/{order_id}/shipping_info.json",
            data={"address_to": shipping_address}
        )
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()