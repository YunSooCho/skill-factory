"""
WooCommerce Client - REST API Implementation
WooCommerce API documentation: https://woocommerce.github.io/woocommerce-rest-api-docs/
"""

import os
import requests
import base64
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class WooCommerceClient:
    """
    Complete client for WooCommerce REST API.
    Supports Products, Orders, Customers, Coupons, and more.
    """
    
    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        store_url: Optional[str] = None,
        version: str = "v3",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize WooCommerce client.
        
        Args:
            consumer_key: Consumer key (from env: WOOCOMMERCE_CONSUMER_KEY)
            consumer_secret: Consumer secret (from env: WOOCOMMERCE_CONSUMER_SECRET)
            store_url: Store URL (from env: WOOCOMMERCE_STORE_URL)
            version: API version (v1, v2, v3)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            WOOCOMMERCE_STORE_URL: Your store URL (e.g., "https://mystore.com")
            WOOCOMMERCE_CONSUMER_KEY: API consumer key
            WOOCOMMERCE_CONSUMER_SECRET: API consumer secret
        """
        self.consumer_key = consumer_key or os.getenv("WOOCOMMERCE_CONSUMER_KEY")
        self.consumer_secret = consumer_secret or os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
        self.store_url = store_url or os.getenv("WOOCOMMERCE_STORE_URL")
        self.version = version
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.store_url:
            raise ValueError(
                "Store URL is required. Set WOOCOMMERCE_STORE_URL environment variable."
            )
        
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError(
                "Consumer key and secret are required. "
                "Set WOOCOMMERCE_CONSUMER_KEY and WOOCOMMERCE_CONSUMER_SECRET."
            )
        
        # Ensure store URL has no trailing slash
        self.store_url = self.store_url.rstrip('/')
        self.base_url = f"{self.store_url}/wp-json/wc/{self.version}"
        
        self.session = requests.Session()
        
        # Setup HTTP Basic Auth
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()
        self.session.headers.update({
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json"
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
        Make HTTP request to WooCommerce API.
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
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        category: Optional[int] = None,
        tag: Optional[int] = None,
        sku: Optional[str] = None,
        type: Optional[str] = None,
        status: str = "publish",
        stock_status: Optional[str] = None,
        on_sale: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        order: str = "desc",
        orderby: str = "date"
    ) -> Dict[str, Any]:
        """
        List products.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            search: Search query
            category: Filter by category ID
            tag: Filter by tag ID
            sku: Filter by SKU
            type: Filter by type (simple, variable, grouped, external)
            status: Filter by status (publish, draft, pending, private)
            stock_status: Filter by stock status (instock, outofstock, onbackorder)
            on_sale: Filter for products on sale
            min_price: Minimum price
            max_price: Maximum price
            order: Order direction (asc, desc)
            orderby: Order by (id, date, modified, include, title, slug, price, popularity, rating)
            
        Returns:
            List of products
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100),
            "status": status,
            "order": order,
            "orderby": orderby
        }
        
        if search:
            params["search"] = search
        if category:
            params["category"] = category
        if tag:
            params["tag"] = tag
        if sku:
            params["sku"] = sku
        if type:
            params["type"] = type
        if stock_status:
            params["stock_status"] = stock_status
        if on_sale is not None:
            params["on_sale"] = str(on_sale).lower()
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Get a specific product by ID.
        """
        return self._request("GET", f"products/{product_id}")
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product.
        
        Args:
            product_data: Product data dict with fields:
                - name: Product name (required)
                - type: Product type (simple, variable, grouped, external)
                - regular_price: Regular price
                - sale_price: Sale price
                - description: Product description
                - short_description: Short description
                - sku: SKU
                - stock_quantity: Stock quantity
                - manage_stock: True/False
                - categories: List of category objects
                - images: List of image objects
                
        Returns:
            Created product response
        """
        return self._request("POST", "products", data=product_data)
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product.
        """
        return self._request("PUT", f"products/{product_id}", data=product_data)
    
    def delete_product(self, product_id: int, force: bool = False) -> Dict[str, Any]:
        """
        Delete a product.
        
        Args:
            product_id: Product ID
            force: True to permanently delete, False to move to trash
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"products/{product_id}", params=params)
    
    def batch_products(self, batch_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Batch create/update/delete products.
        
        Args:
            batch_data: Dict with 'create', 'update', 'delete' arrays
            
        Returns:
            Batch operation results
        """
        return self._request("POST", "products/batch", data=batch_data)
    
    # ============================================================================
    # Product Variations
    # ============================================================================
    
    def list_variations(self, product_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        List product variations.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", f"products/{product_id}/variations", params=params)
    
    def get_variation(self, product_id: int, variation_id: int) -> Dict[str, Any]:
        """
        Get a specific variation.
        """
        return self._request("GET", f"products/{product_id}/variations/{variation_id}")
    
    def create_variation(self, product_id: int, variation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a product variation.
        """
        return self._request("POST", f"products/{product_id}/variations", data=variation_data)
    
    def update_variation(self, product_id: int, variation_id: int, variation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a product variation.
        """
        return self._request("PUT", f"products/{product_id}/variations/{variation_id}", data=variation_data)
    
    def delete_variation(self, product_id: int, variation_id: int, force: bool = False) -> Dict[str, Any]:
        """
        Delete a product variation.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"products/{product_id}/variations/{variation_id}", params=params)
    
    # ============================================================================
    # Orders
    # ============================================================================
    
    def list_orders(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        status: Optional[str] = None,
        customer: Optional[int] = None,
        product: Optional[int] = None,
        order: str = "desc",
        orderby: str = "date"
    ) -> Dict[str, Any]:
        """
        List orders.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            search: Search query
            after: YYYY-MM-DD date to filter orders created after
            before: YYYY-MM-DD date to filter orders created before
            status: Order status (pending, processing, on-hold, completed, cancelled, refunded, failed)
            customer: Filter by customer ID
            product: Filter by product ID
            order: Order direction (asc, desc)
            orderby: Order by (date, id, include, title, slug, modified)
            
        Returns:
            List of orders
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100),
            "order": order,
            "orderby": orderby
        }
        
        if search:
            params["search"] = search
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if status:
            params["status"] = status
        if customer:
            params["customer"] = customer
        if product:
            params["product"] = product
        
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Get a specific order by ID.
        """
        return self._request("GET", f"orders/{order_id}")
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            order_data: Order data dict:
                - payment_method: Payment method
                - payment_method_title: Payment method title
                - set_paid: True if order is paid
                - billing: Billing address object
                - shipping: Shipping address object
                - line_items: Array of line items (product_id, quantity)
                - shipping_lines: Array of shipping lines
                - customer_id: Customer ID (optional)
                
        Returns:
            Created order response
        """
        return self._request("POST", "orders", data=order_data)
    
    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing order.
        """
        return self._request("PUT", f"orders/{order_id}", data=order_data)
    
    def delete_order(self, order_id: int, force: bool = False) -> Dict[str, Any]:
        """
        Delete an order.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"orders/{order_id}", params=params)
    
    def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            status: New status (pending, processing, on-hold, completed, cancelled, refunded, failed)
        """
        return self.update_order(order_id, {"status": status})
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        role: Optional[str] = None,
        order: str = "desc",
        orderby: str = "registered_date"
    ) -> Dict[str, Any]:
        """
        List customers.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            search: Search query
            role: Filter by role (all, customer, subscriber)
            order: Order direction (asc, desc)
            orderby: Order by (id, include, name, registered_date, email)
            
        Returns:
            List of customers
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100),
            "order": order,
            "orderby": orderby
        }
        
        if search:
            params["search"] = search
        if role:
            params["role"] = role
        
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Get a specific customer by ID.
        """
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer data:
                - email: Customer email (required)
                - first_name: First name
                - last_name: Last name
                - username: Username
                - billing: Billing address
                - shipping: Shipping address
                - password: Customer password
                
        Returns:
            Created customer response
        """
        return self._request("POST", "customers", data=customer_data)
    
    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing customer.
        """
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    def delete_customer(self, customer_id: int, force: bool = True) -> Dict[str, Any]:
        """
        Delete a customer.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"customers/{customer_id}", params=params)
    
    # ============================================================================
    # Coupons
    # ============================================================================
    
    def list_coupons(
        self,
        page: int = 1,
        per_page: int = 10,
        code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List coupons.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        if code:
            params["code"] = code
        
        return self._request("GET", "coupons", params=params)
    
    def get_coupon(self, coupon_id: int) -> Dict[str, Any]:
        """
        Get a specific coupon.
        """
        return self._request("GET", f"coupons/{coupon_id}")
    
    def create_coupon(self, coupon_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new coupon.
        
        Args:
            coupon_data: Coupon data:
                - code: Coupon code (required)
                - amount: Discount amount
                - discount_type: Type (percent, fixed_cart, fixed_product)
                - description: Coupon description
                - individual_use: TrueFalse
                - usage_limit: Usage limit
                - free_shipping: TrueFalse
        """
        return self._request("POST", "coupons", data=coupon_data)
    
    def update_coupon(self, coupon_id: int, coupon_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a coupon.
        """
        return self._request("PUT", f"coupons/{coupon_id}", data=coupon_data)
    
    def delete_coupon(self, coupon_id: int, force: bool = True) -> Dict[str, Any]:
        """
        Delete a coupon.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"coupons/{coupon_id}", params=params)
    
    # ============================================================================
    # Product Categories
    # ============================================================================
    
    def list_categories(self, page: int = 1, per_page: int = 10, parent: Optional[int] = None) -> Dict[str, Any]:
        """
        List product categories.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        if parent:
            params["parent"] = parent
        
        return self._request("GET", "products/categories", params=params)
    
    def get_category(self, category_id: int) -> Dict[str, Any]:
        """
        Get a specific category.
        """
        return self._request("GET", f"products/categories/{category_id}")
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new category.
        
        Args:
            category_data: Category data:
                - name: Category name (required)
                - slug: Category slug
                - parent: Parent category ID
                - description: Category description
                - display: Display type (default, products, subcategories, both)
        """
        return self._request("POST", "products/categories", data=category_data)
    
    def update_category(self, category_id: int, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a category.
        """
        return self._request("PUT", f"products/categories/{category_id}", data=category_data)
    
    def delete_category(self, category_id: int, force: bool = True) -> Dict[str, Any]:
        """
        Delete a category.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"products/categories/{category_id}", params=params)
    
    # ============================================================================
    # Reports
    # ============================================================================
    
    def get_sales_report(self, period: str = "7days") -> Dict[str, Any]:
        """
        Get sales report.
        
        Args:
            period: Time period (today, yesterday, last_7_days, last_30_days, this_month, last_month, this_year, last_year)
        """
        return self._request("GET", f"reports/sales?period={period}")
    
    def get_top_sellers_report(self, period: str = "7days", limit: int = 5) -> Dict[str, Any]:
        """
        Get top sellers report.
        """
        return self._request("GET", f"reports/top_sellers?period={period}&limit={limit}")
    
    # ============================================================================
    # Webhooks
    # ============================================================================
    
    def list_webhooks(self) -> Dict[str, Any]:
        """
        List all webhooks.
        """
        return self._request("GET", "webhooks")
    
    def get_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Get a specific webhook.
        """
        return self._request("GET", f"webhooks/{webhook_id}")
    
    def create_webhook(
        self,
        name: str,
        topic: str,
        delivery_url: str,
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            name: Webhook name
            topic: Event topic (order.created, order.updated, product.created, etc.)
            delivery_url: Webhook URL
            secret: Secret for HMAC signature
        """
        data = {
            "name": name,
            "topic": topic,
            "delivery_url": delivery_url
        }
        if secret:
            data["secret"] = secret
        
        return self._request("POST", "webhooks", data=data)
    
    def update_webhook(self, webhook_id: int, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a webhook.
        """
        return self._request("PUT", f"webhooks/{webhook_id}", data=webhook_data)
    
    def delete_webhook(self, webhook_id: int, force: bool = True) -> Dict[str, Any]:
        """
        Delete a webhook.
        """
        params = {"force": str(force).lower()}
        return self._request("DELETE", f"webhooks/{webhook_id}", params=params)
    
    def get_webhook_delivery(self, webhook_id: int, delivery_id: int) -> Dict[str, Any]:
        """
        Get webhook delivery details.
        """
        return self._request("GET", f"webhooks/{webhook_id}/deliveries/{delivery_id}")
    
    # ============================================================================
    # Payment Gateways
    # ============================================================================
    
    def list_payment_gateways(self) -> Dict[str, Any]:
        """
        List payment gateways.
        """
        return self._request("GET", "payment_gateways")
    
    def get_payment_gateway(self, gateway_id: str) -> Dict[str, Any]:
        """
        Get a specific payment gateway.
        """
        return self._request("GET", f"payment_gateways/{gateway_id}")
    
    def update_payment_gateway(self, gateway_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update payment gateway settings.
        """
        return self._request("PUT", f"payment_gateways/{gateway_id}", data=settings)
    
    # ============================================================================
    # Shipping Methods
    # ============================================================================
    
    def list_shipping_methods(self) -> Dict[str, Any]:
        """
        List shipping methods.
        """
        return self._request("GET", "shipping_methods")
    
    def get_shipping_method(self, method_id: int) -> Dict[str, Any]:
        """
        Get a specific shipping method.
        """
        return self._request("GET", f"shipping_methods/{method_id}")
    
    # ============================================================================
    # Tax Classes
    # ============================================================================
    
    def list_tax_classes(self) -> Dict[str, Any]:
        """
        List tax classes.
        """
        return self._request("GET", "taxes/classes")
    
    def get_tax_class(self, class_id: int) -> Dict[str, Any]:
        """
        Get a specific tax class.
        """
        return self._request("GET", f"taxes/classes/{class_id}")
    
    # ============================================================================
    # Settings
    # ============================================================================
    
    def get_settings(self, group: str = "") -> Dict[str, Any]:
        """
        Get store settings.
        
        Args:
            group: Settings group (general, products, payment, shipping, etc.)
        """
        endpoint = "settings" if not group else f"settings/{group}"
        return self._request("GET", endpoint)
    
    def update_settings(self, group: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update store settings.
        """
        return self._request("PUT", f"settings/{group}", data=settings)
    
    # ============================================================================
    # System Status
    # ============================================================================
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system status.
        """
        return self._request("GET", "system_status")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()