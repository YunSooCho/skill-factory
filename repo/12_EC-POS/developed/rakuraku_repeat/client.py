"""
Rakuraku Repeat Client - Japanese Recurring Billing Platform
https://rakuraku-repeat.jp/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class RakurakuRepeatClient:
    """Complete client for Rakuraku Repeat API - Japanese recurring billing platform."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("RAKURAKU_REPEAT_API_KEY")
        self.base_url = (base_url or os.getenv("RAKURAKU_REPEAT_BASE_URL", "https://api.rakuraku-repeat.jp/v1")).rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError("API key required. Set RAKURAKU_REPEAT_API_KEY")
        
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
    
    # Subscriptions
    def list_subscriptions(self, page: int = 1, status: Optional[str] = None, plan_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if status:
            params["status"] = status
        if plan_id:
            params["plan_id"] = plan_id
        return self._request("GET", "subscriptions", params=params)
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return self._request("GET", f"subscriptions/{subscription_id}")
    
    def create_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "subscriptions", data=data)
    
    def update_subscription(self, subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"subscriptions/{subscription_id}", data=data)
    
    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        data = {"cancel_at_period_end": at_period_end}
        if reason:
            data["cancellation_reason"] = reason
        return self._request("POST", f"subscriptions/{subscription_id}/cancel", data=data)
    
    def pause_subscription(self, subscription_id: str, resume_date: Optional[str] = None) -> Dict[str, Any]:
        data = {}
        if resume_date:
            data["resume_date"] = resume_date
        return self._request("POST", f"subscriptions/{subscription_id}/pause", data=data)
    
    def resume_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return self._request("POST", f"subscriptions/{subscription_id}/resume")
    
    # Subscription Plans
    def list_plans(self, page: int = 1, active: bool = True) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50, "active": active}
        return self._request("GET", "plans", params=params)
    
    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        return self._request("GET", f"plans/{plan_id}")
    
    def create_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "plans", data=data)
    
    def update_plan(self, plan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"plans/{plan_id}", data=data)
    
    def delete_plan(self, plan_id: str) -> None:
        self._request("DELETE", f"plans/{plan_id}")
    
    # Customers
    def list_customers(self, page: int = 1, email: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if email:
            params["email"] = email
        return self._request("GET", "customers", params=params)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}")
    
    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "customers", data=data)
    
    def update_customer(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", f"customers/{customer_id}", data=data)
    
    # Invoices
    def list_invoices(self, page: int = 1, customer_id: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if customer_id:
            params["customer_id"] = customer_id
        if status:
            params["status"] = status
        return self._request("GET", "invoices", params=params)
    
    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        return self._request("GET", f"invoices/{invoice_id}")
    
    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "invoices", data=data)
    
    def waive_invoice(self, invoice_id: str, reason: str) -> Dict[str, Any]:
        return self._request("POST", f"invoices/{invoice_id}/waive", data={"reason": reason})
    
    # Payments
    def list_payments(self, page: int = 1, subscription_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": 50}
        if subscription_id:
            params["subscription_id"] = subscription_id
        return self._request("GET", "payments", params=params)
    
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        return self._request("GET", f"payments/{payment_id}")
    
    def process_payment(self, subscription_id: str) -> Dict[str, Any]:
        return self._request("POST", f"subscriptions/{subscription_id}/charge")
    
    # Payment Methods
    def list_payment_methods(self, customer_id: str) -> Dict[str, Any]:
        return self._request("GET", f"customers/{customer_id}/payment_methods")
    
    def add_payment_method(self, customer_id: str, token: str) -> Dict[str, Any]:
        return self._request("POST", f"customers/{customer_id}/payment_methods", data={"token": token})
    
    def set_default_payment_method(self, customer_id: str, payment_method_id: str) -> Dict[str, Any]:
        return self._request("PUT", f"customers/{customer_id}/payment_methods/{payment_method_id}/default")
    
    def delete_payment_method(self, customer_id: str, payment_method_id: str) -> None:
        self._request("DELETE", f"customers/{customer_id}/payment_methods/{payment_method_id}")
    
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
    
    # Usage (for metered billing)
    def record_usage(self, subscription_id: str, quantity: int, timestamp: Optional[str] = None) -> Dict[str, Any]:
        data = {"quantity": quantity}
        if timestamp:
            data["timestamp"] = timestamp
        return self._request("POST", f"subscriptions/{subscription_id}/usage", data=data)
    
    def get_usage_records(
        self,
        subscription_id: str,
        period_start: str,
        period_end: str
    ) -> Dict[str, Any]:
        params = {"period_start": period_start, "period_end": period_end}
        return self._request("GET", f"subscriptions/{subscription_id}/usage", params=params)
    
    # Coupons/Promotions
    def list_coupons(self, active: bool = True) -> Dict[str, Any]:
        return self._request("GET", "coupons", params={"active": active})
    
    def create_coupon(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "coupons", data=data)
    
    def delete_coupon(self, coupon_id: str) -> None:
        self._request("DELETE", f"coupons/{coupon_id}")
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()