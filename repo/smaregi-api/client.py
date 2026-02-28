"""
Smaregi API Client - REST API Implementation
Smaregi API documentation: https://dev.smaregi.com/
Japanese comprehensive retail management system.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin
import time


class SmaregiApiClient:
    """
    Complete client for Smaregi API - Japanese retail management system.
    Supports Products, Sales, Inventory, Customers, Staff, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        contract_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Smaregi API client.
        
        Args:
            api_key: API access token (from env: SMAREGI_API_KEY)
            contract_id: Contract ID (from env: SMAREGI_CONTRACT_ID)
            base_url: Base URL (from env: SMAREGI_BASE_URL)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            SMAREGI_API_KEY: Your Smaregi API access token
            SMAREGI_CONTRACT_ID: Your contract ID
            SMAREGI_BASE_URL: Base URL (default: https://api.smaregi.jp/pos)
        """
        self.api_key = api_key or os.getenv("SMAREGI_API_KEY")
        self.contract_id = contract_id or os.getenv("SMAREGI_CONTRACT_ID")
        self.base_url = base_url or os.getenv("SMAREGI_BASE_URL", "https://api.smaregi.jp/pos")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set SMAREGI_API_KEY environment variable."
            )
        
        if not self.contract_id:
            raise ValueError(
                "Contract ID is required. Set SMAREGI_CONTRACT_ID environment variable."
            )
        
        self.base_url = self.base_url.rstrip("/")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-contract-id": self.contract_id
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
        Make HTTP request to Smaregi API.
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
    # Stores / Locations
    # ============================================================================
    
    def list_stores(self) -> Dict[str, Any]:
        """
        List all stores.
        """
        return self._request("GET", "stores")
    
    def get_store(self, store_id: str) -> Dict[str, Any]:
        """
        Get details of a specific store.
        """
        return self._request("GET", f"stores/{store_id}")
    
    # ============================================================================
    # Products / Items
    # ============================================================================
    
    def list_products(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 100,
        barcode: Optional[str] = None,
        product_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List products in a store.
        
        Args:
            store_id: Store ID
            page: Page number
            limit: Items per page (max 100)
            barcode: Filter by barcode
            product_name: Filter by product name
            
        Returns:
            Products response
        """
        params = {
            "storeId": store_id,
            "page": page,
            "limit": min(limit, 100)
        }
        
        if barcode:
            params["barcode"] = barcode
        if product_name:
            params["productName"] = product_name
        
        return self._request("GET", "products", params=params)
    
    def get_product(self, store_id: str, product_id: str) -> Dict[str, Any]:
        """
        Get details of a specific product.
        """
        params = {"storeId": store_id}
        return self._request("GET", f"products/{product_id}", params=params)
    
    def create_product(
        self,
        store_id: str,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new product.
        
        Args:
            store_id: Store ID
            product_data: Product data dict:
                - productId: Product ID (required)
                - productName: Product name (required)
                - categoryId: Category ID
                - categoryIdSub: Sub category ID
                - retailPrice: Retail price
                - costPrice: Cost price
                - taxRate: Tax rate
                - unitId: Unit ID
                - barcode: Barcode
                
        Returns:
            Created product response
        """
        return self._request("POST", "products", data={**product_data, "storeId": store_id})
    
    def update_product(
        self,
        store_id: str,
        product_id: str,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing product.
        """
        return self._request(
            "PUT",
            f"products/{product_id}",
            data={**product_data, "storeId": store_id}
        )
    
    # ============================================================================
    # Stock / Inventory
    # ============================================================================
    
    def list_stock(
        self,
        store_id: str,
        product_id: Optional[str] = None,
        storage_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get stock information.
        
        Args:
            store_id: Store ID
            product_id: Filter by product ID
            storage_id: Filter by storage location ID
            
        Returns:
            Stock response
        """
        params = {"storeId": store_id}
        
        if product_id:
            params["productId"] = product_id
        if storage_id:
            params["storageId"] = storage_id
        
        return self._request("GET", "stock", params=params)
    
    def adjust_stock(
        self,
        stock_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Adjust stock levels.
        
        Args:
            stock_data: List of stock adjustments:
                - storeId: Store ID
                - productId: Product ID
                - storageId: Storage location ID (optional)
                - stock: New stock quantity
                - stockType: Stock type (for tracking)
                
        Returns:
            Adjustment result
        """
        return self._request("POST", "stock", data={"items": stock_data})
    
    # ============================================================================
    # Sales / Transactions
    # ============================================================================
    
    def list_sales(
        self,
        store_id: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        List sales transactions.
        
        Args:
            store_id: Store ID
            date_from: From date (YYYY-MM-DD)
            date_to: To date (YYYY-MM-DD)
            page: Page number
            limit: Items per page (max 100)
            
        Returns:
            Sales response
        """
        params = {
            "storeId": store_id,
            "page": page,
            "limit": min(limit, 100)
        }
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        return self._request("GET", "sales", params=params)
    
    def get_sale(self, sale_id: str) -> Dict[str, Any]:
        """
        Get details of a specific sale.
        """
        return self._request("GET", f"sales/{sale_id}")
    
    def create_sale(self, sale_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new sale transaction.
        
        Args:
            sale_data: Sale data dict:
                - storeId: Store ID (required)
                - terminalId: Terminal ID (required)
                - saleDate: Sale date (required)
                - sales: Array of sale items:
                    - productId: Product ID
                    - quantity: Quantity
                    - retailPrice: Unit price
                    - taxRate: Tax rate
                - paymentMethodId: Payment method ID
                - customerId: Customer ID (optional)
                
        Returns:
            Created sale response
        """
        return self._request("POST", "sales", data=sale_data)
    
    # ============================================================================
    # Categories
    # ============================================================================
    
    def list_categories(self, store_id: str) -> Dict[str, Any]:
        """
        List product categories.
        """
        params = {"storeId": store_id}
        return self._request("GET", "categories", params=params)
    
    def get_category(self, category_id: str) -> Dict[str, Any]:
        """
        Get details of a specific category.
        """
        return self._request("GET", f"categories/{category_id}")
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 100,
        customer_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List customers.
        
        Args:
            store_id: Store ID
            page: Page number
            limit: Items per page (max 100)
            customer_code: Filter by customer code
            
        Returns:
            Customers response
        """
        params = {
            "storeId": store_id,
            "page": page,
            "limit": min(limit, 100)
        }
        
        if customer_code:
            params["customerCode"] = customer_code
        
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
            customer_data: Customer data dict:
                - storeId: Store ID (required)
                - customerCode: Customer code (required)
                - customerName: Customer name (required)
                - customerNameKana: Customer name (kana)
                - phoneNumber: Phone number
                - mailAddress: Email address
                - postCode: Postal code
                - address1: Address 1
                - address2: Address 2
                - birthday: Birthday
                
        Returns:
            Created customer response
        """
        return self._request("POST", "customers", data=customer_data)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing customer.
        """
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    # ============================================================================
    # Staff
    # ============================================================================
    
    def list_staff(self, store_id: str) -> Dict[str, Any]:
        """
        List staff members.
        """
        params = {"storeId": store_id}
        return self._request("GET", "staff", params=params)
    
    def get_staff(self, staff_id: str) -> Dict[str, Any]:
        """
        Get details of a specific staff member.
        """
        return self._request("GET", f"staff/{staff_id}")
    
    # ============================================================================
    # Terminals
    # ============================================================================
    
    def list_terminals(self, store_id: str) -> Dict[str, Any]:
        """
        List POS terminals.
        """
        params = {"storeId": store_id}
        return self._request("GET", "terminals", params=params)
    
    def get_terminal(self, terminal_id: str) -> Dict[str, Any]:
        """
        Get details of a specific terminal.
        """
        return self._request("GET", f"terminals/{terminal_id}")
    
    # ============================================================================
    # Payments
    # ============================================================================
    
    def list_payment_methods(self, store_id: str) -> Dict[str, Any]:
        """
        List payment methods.
        """
        params = {"storeId": store_id}
        return self._request("GET", "payments", params=params)
    
    # ============================================================================
    # Storage Locations
    # ============================================================================
    
    def list_storages(self, store_id: str) -> Dict[str, Any]:
        """
        List storage locations.
        """
        params = {"storeId": store_id}
        return self._request("GET", "storages", params=params)
    
    # ============================================================================
    # Analytics / Reports
    # ============================================================================
    
    def get_daily_report(
        self,
        store_id: str,
        date: str
    ) -> Dict[str, Any]:
        """
        Get daily sales report.
        
        Args:
            store_id: Store ID
            date: Report date (YYYY-MM-DD)
            
        Returns:
            Daily report data
        """
        params = {"storeId": store_id, "date": date}
        return self._request("GET", "reports/daily", params=params)
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()