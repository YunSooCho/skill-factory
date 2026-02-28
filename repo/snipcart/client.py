"""
Snipcart Client - REST API Implementation
Snipcart API documentation: https://docs.snipcart.com/v3/api-reference/introduction
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class SnipcartClient:
    """
    Complete client for Snipcart REST API.
    Supports Orders, Customers, Products, Subscriptions, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Snipcart client.
        
        Args:
            api_key: Public API key for storefront (optional)
            api_secret: Secret API key for backend operations
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            SNIPCART_API_SECRET: Your secret API key
            SNIPCART_API_KEY: Your public API key (optional)
        """
        self.api_key = api_key or os.getenv("SNIPCART_API_KEY")
        self.api_secret = api_secret or os.getenv("SNIPCART_API_SECRET")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_secret:
            raise ValueError(
                "API secret is required for most operations. "
                "Set SNIPCART_API_SECRET environment variable."
            )
        
        # Use secret key for backend operations
        self.base_url = "https://app.snipcart.com/api"
        
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        if self.api_secret:
            self.session.auth = (self.api_key or "", self.api_secret)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Snipcart API.
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
    # Orders
    # ============================================================================
    
    def list_orders(
        self,
        offset: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        invoice_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List orders.
        
        Args:
            offset: Pagination offset
            limit: Number of results (max 100)
            status: Filter by status (Processed, InProgress, Incomplete, Disputed)
            invoice_number: Filter by invoice number
            
        Returns:
            Paginated orders response
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if status:
            params["status"] = status
        if invoice_number:
            params["invoiceNumber"] = invoice_number
        
        return self._request("GET", "orders", params=params)
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get a specific order by token.
        """
        return self._request("GET", f"orders/{order_id}")
    
    def get_order_by_invoice(self, invoice_number: str) -> Dict[str, Any]:
        """
        Get order by invoice number.
        """
        return self._request("GET", f"orders/invoice/{invoice_number}")
    
    def update_order_status(
        self,
        order_id: str,
        status: str,
        email_customer: bool = False,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update order status.
        
        Args:
            order_id: Order token
            status: New status (Processed, InProgress, Incomplete, Disputed)
            email_customer: Send email notification
            comment: Optional comment for status change
            
        Returns:
            Updated order
        """
        data = {
            "status": status,
            "emailCustomer": email_customer
        }
        if comment:
            data["comment"] = comment
        
        return self._request("PUT", f"orders/{order_id}/status", data=data)
    
    def process_order(
        self,
        order_id: str,
        email_customer: bool = True,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark order as processed.
        """
        return self.update_order_status(order_id, "Processed", email_customer, comment)
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(
        self,
        offset: int = 0,
        limit: int = 20,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List customers.
        
        Args:
            offset: Pagination offset
            limit: Number of results (max 100)
            email: Filter by email address
            
        Returns:
            Paginated customers response
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if email:
            params["email"] = email
        
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Get a specific customer.
        """
        return self._request("GET", f"customers/{customer_id}")
    
    def get_customer_by_email(self, email: str) -> Dict[str, Any]:
        """
        Get customer by email address.
        """
        params = {"email": email}
        return self._request("GET", "customers", params=params)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update customer information.
        """
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    # ============================================================================
    # Products
    # ============================================================================
    
    def list_products(
        self,
        offset: int = 0,
        limit: int = 20,
        user_defined_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List products in your account.
        
        Args:
            offset: Pagination offset
            limit: Number of results (max 100)
            user_defined_id: Filter by user defined ID
            
        Returns:
            Paginated products response
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if user_defined_id:
            params["userDefinedId"] = user_defined_id
        
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get a specific product.
        """
        return self._request("GET", f"products/{product_id}")
    
    def get_product_by_user_id(self, user_defined_id: str) -> Dict[str, Any]:
        """
        Get product by user defined ID.
        """
        params = {"userDefinedId": user_defined_id}
        return self._request("GET", "products", params=params)
    
    def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update product information.
        """
        return self._request("PUT", f"products/{product_id}", data=product_data)
    
    def list_product_variants(
        self,
        product_id: str,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List variants of a product.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", f"products/{product_id}/variants", params=params)
    
    def get_product_variant(self, product_id: str, variant_id: str) -> Dict[str, Any]:
        """
        Get a specific variant of a product.
        """
        return self._request("GET", f"products/{product_id}/variants/{variant_id}")
    
    def update_product_variant(
        self,
        product_id: str,
        variant_id: str,
        variant_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update product variant.
        """
        return self._request(
            "PUT",
            f"products/{product_id}/variants/{variant_id}",
            data=variant_data
        )
    
    def list_product_discounts(
        self,
        product_id: str,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List discounts for a product.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", f"products/{product_id}/discounts", params=params)
    
    # ============================================================================
    # Discounts (Coupons)
    # ============================================================================
    
    def list_discounts(
        self,
        offset: int = 0,
        limit: int = 20,
        code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all discounts.
        
        Args:
            offset: Pagination offset
            limit: Number of results (max 100)
            code: Filter by discount code
            
        Returns:
            Paginated discounts response
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if code:
            params["code"] = code
        
        return self._request("GET", "discounts", params=params)
    
    def get_discount(self, discount_id: str) -> Dict[str, Any]:
        """
        Get a specific discount.
        """
        return self._request("GET", f"discounts/{discount_id}")
    
    def create_discount(self, discount_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new discount.
        
        Args:
            discount_data: Discount data dict:
                - name: Discount name
                - code: Discount code
                - type: FixedAmount, Percentage, Shipping, RatePerItem, PerQuantityTier
                - amount: Discount amount
                - triggers: Trigger conditions
                - maxNumberOfUsages: Max usage limit
                - shippingRateTypes: Shipping rate types
                - products: Applicable products
                - excludesShipping: Exclude from shipping
        """
        return self._request("POST", "discounts", data=discount_data)
    
    def update_discount(self, discount_id: str, discount_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing discount.
        """
        return self._request("PUT", f"discounts/{discount_id}", data=discount_data)
    
    def delete_discount(self, discount_id: str) -> None:
        """
        Delete a discount.
        """
        self._request("DELETE", f"discounts/{discount_id}")
    
    def archive_discount(self, discount_id: str) -> None:
        """
        Archive a discount.
        """
        self._request("POST", f"discounts/{discount_id}/archive")
    
    # ============================================================================
    # Subscriptions
    # ============================================================================
    
    def list_subscriptions(
        self,
        offset: int = 0,
        limit: int = 20,
        plan_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List subscriptions.
        
        Args:
            offset: Pagination offset
            limit: Number of results (max 100)
            plan_id: Filter by plan ID
            
        Returns:
            Paginated subscriptions response
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if plan_id:
            params["planId"] = plan_id
        
        return self._request("GET", "subscriptions", params=params)
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get a specific subscription.
        """
        return self._request("GET", f"subscriptions/{subscription_id}")
    
    def cancel_subscription(
        self,
        subscription_id: str,
        end_now: bool = False
    ) -> Dict[str, Any]:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Subscription ID
            end_now: True to end immediately, False to bill next cycle only
        """
        data = {"endNow": end_now}
        return self._request("POST", f"subscriptions/{subscription_id}/cancel", data=data)
    
    def pause_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Pause a subscription.
        """
        return self._request("POST", f"subscriptions/{subscription_id}/pause")
    
    def resume_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Resume a paused subscription.
        """
        return self._request("POST", f"subscriptions/{subscription_id}/resume")
    
    # ============================================================================
    # Subscription Plans
    # ============================================================================
    
    def list_plans(
        self,
        offset: int = 0,
        limit: int = 20,
        product_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List subscription plans.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if product_id:
            params["productId"] = product_id
        
        return self._request("GET", "subscriptions/plans", params=params)
    
    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        """
        Get a specific subscription plan.
        """
        return self._request("GET", f"subscriptions/plans/{plan_id}")
    
    def create_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new subscription plan.
        
        Args:
            plan_data: Plan data:
                - name: Plan name
                - productId: Product ID
                - variantId: Variant ID
                - interval: Frequency (Month, Week, Day)
                - intervalCount: Number of intervals
                - trialPeriodInDays: Trial period duration
                - initialCharge: Initial charge amount
                - gracePeriodInDays: Grace period duration
        """
        return self._request("POST", "subscriptions/plans", data=plan_data)
    
    def update_plan(self, plan_id: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a subscription plan.
        """
        return self._request("PUT", f"subscriptions/plans/{plan_id}", data=plan_data)
    
    def delete_plan(self, plan_id: str) -> None:
        """
        Delete a subscription plan.
        """
        self._request("DELETE", f"subscriptions/plans/{plan_id}")
    
    # ============================================================================
    # Refunds
    # ============================================================================
    
    def list_refunds(
        self,
        offset: int = 0,
        limit: int = 20,
        order_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List refunds.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        
        if order_id:
            params["orderId"] = order_id
        
        return self._request("GET", "refunds", params=params)
    
    def get_refund(self, refund_id: str) -> Dict[str, Any]:
        """
        Get a specific refund.
        """
        return self._request("GET", f"refunds/{refund_id}")
    
    def create_refund(
        self,
        order_id: str,
        items: List[Dict[str, Any]],
        notify_customer: bool = False
    ) -> Dict[str, Any]:
        """
        Create a refund.
        
        Args:
            order_id: Order token
            items: List of items to refund with:
                - itemId: Order item ID
                - quantity: Quantity to refund
                - amount: Amount to refund
            notify_customer: Send email notification
        """
        data = {
            "orderId": order_id,
            "items": items,
            "notifyCustomer": notify_customer
        }
        
        return self._request("POST", "refunds", data=data)
    
    # ============================================================================
    # Carts
    # ============================================================================
    
    def list_carts(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List active carts.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", "carts", params=params)
    
    def get_cart(self, cart_id: str) -> Dict[str, Any]:
        """
        Get a specific cart.
        """
        return self._request("GET", f"carts/{cart_id}")
    
    # ============================================================================
    # Taxes
    # ============================================================================
    
    def list_taxes(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List tax configurations.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", "taxes", params=params)
    
    def get_tax(self, tax_id: str) -> Dict[str, Any]:
        """
        Get a specific tax configuration.
        """
        return self._request("GET", f"taxes/{tax_id}")
    
    def update_tax(self, tax_id: str, tax_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update tax configuration.
        """
        return self._request("PUT", f"taxes/{tax_id}", data=tax_data)
    
    # ============================================================================
    # Shipping Rates
    # ============================================================================
    
    def list_shipping_rates(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List custom shipping rates.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", "shipping/customrates", params=params)
    
    def get_shipping_rate(self, rate_id: str) -> Dict[str, Any]:
        """
        Get a specific shipping rate.
        """
        return self._request("GET", f"shipping/customrates/{rate_id}")
    
    def create_shipping_rate(self, rate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a custom shipping rate.
        
        Args:
            rate_data: Shipping rate data:
                - description: Rate description
                - cost: Shipping cost
                - triggers: Trigger conditions
                - type: Fixed, PerItem, PerQuantityTier
                - destinations: Applicable destinations
        """
        return self._request("POST", "shipping/customrates", data=rate_data)
    
    def update_shipping_rate(self, rate_id: str, rate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a shipping rate.
        """
        return self._request("PUT", f"shipping/customrates/{rate_id}", data=rate_data)
    
    def delete_shipping_rate(self, rate_id: str) -> None:
        """
        Delete a shipping rate.
        """
        self._request("DELETE", f"shipping/customrates/{rate_id}")
    
    # ============================================================================
    # Webhooks
    # ============================================================================
    
    def list_webhooks(self) -> Dict[str, Any]:
        """
        List all webhooks.
        """
        return self._request("GET", "webhooks")
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Get a specific webhook.
        """
        return self._request("GET", f"webhooks/{webhook_id}")
    
    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            url: Webhook URL
            events: List of event types
            secret: Optional secret for signature verification
            headers: Optional custom headers
            
        Returns:
            Created webhook
        """
        data = {
            "url": url,
            "events": events
        }
        
        if secret:
            data["secret"] = secret
        if headers:
            data["headers"] = headers
        
        return self._request("POST", "webhooks", data=data)
    
    def update_webhook(self, webhook_id: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a webhook.
        """
        return self._request("PUT", f"webhooks/{webhook_id}", data=webhook_data)
    
    def delete_webhook(self, webhook_id: str) -> None:
        """
        Delete a webhook.
        """
        self._request("DELETE", f"webhooks/{webhook_id}")
    
    def test_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Send a test request to a webhook.
        """
        return self._request("POST", f"webhooks/{webhook_id}/test")
    
    # ============================================================================
    # Insights / Analytics
    # ============================================================================
    
    def get_sales_stats(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get sales statistics.
        
        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        return self._request("GET", "insights/sales", params=params)
    
    def get_orders_stats(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get order statistics.
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        return self._request("GET", "insights/orders", params=params)
    
    def get_top_products(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get top performing products.
        """
        params = {"limit": min(limit, 100)}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        return self._request("GET", "insights/topproducts", params=params)
    
    # ============================================================================
    # Categories
    # ============================================================================
    
    def list_categories(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List product categories.
        """
        params = {
            "offset": offset,
            "limit": min(limit, 100)
        }
        return self._request("GET", "categories", params=params)
    
    def get_category(self, category_id: str) -> Dict[str, Any]:
        """
        Get a specific category.
        """
        return self._request("GET", f"categories/{category_id}")
    
    def update_category(self, category_id: str, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a category.
        """
        return self._request("PUT", f"categories/{category_id}", data=category_data)
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()