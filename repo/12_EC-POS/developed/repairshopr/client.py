"""
RepairShopr Client - REST API Implementation
RepairShopr API documentation: https://www.repairshopr.com/api/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class RepairShoprClient:
    """
    Complete client for RepairShopr API.
    Supports Customers, Tickets, Tickets Items, Estimates, Invoices, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize RepairShopr client.
        
        Args:
            api_key: API key (from env: REPAIRSHOPR_API_KEY)
            base_url: Base URL (from env: REPAIRSHOPR_BASE_URL)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            REPAIRSHOPR_API_KEY: Your RepairShopr API token
            REPAIRSHOPR_BASE_URL: Base URL (default: https://app.repairshopr.com/api)
        """
        self.api_key = api_key or os.getenv("REPAIRSHOPR_API_KEY")
        self.base_url = base_url or os.getenv("REPAIRSHOPR_BASE_URL", "https://app.repairshopr.com/api")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set REPAIRSHOPR_API_KEY environment variable."
            )
        
        # Remove trailing slash
        self.base_url = self.base_url.rstrip("/")
        
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
        Make HTTP request to RepairShopr API.
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
    # Tickets
    # ============================================================================
    
    def list_tickets(
        self,
        page: int = 1,
        limit: int = 50,
        status_id: Optional[str] = None,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List tickets.
        
        Args:
            page: Page number
            limit: Items per page (max 500)
            status_id: Filter by status ID
            customer_id: Filter by customer ID
            
        Returns:
            Tickets response
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        
        if status_id:
            params["status_id"] = status_id
        if customer_id:
            params["customer_id"] = customer_id
        
        return self._request("GET", "tickets", params=params)
    
    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get details of a specific ticket.
        """
        return self._request("GET", f"tickets/{ticket_id}")
    
    def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new ticket.
        
        Args:
            ticket_data: Ticket data dict:
                - customer_id: Customer ID (required)
                - status_id: Status ID
                - problem_category_id: Problem category ID
                - subject: Subject line
                - description: Description
                - device_brand_id: Device brand ID
                - device_model_id: Device model ID
                - device_serial: Serial number
                - device_condition: Device condition
                - device_password: Device password
                
        Returns:
            Created ticket response
        """
        return self._request("POST", "tickets", data=ticket_data)
    
    def update_ticket(self, ticket_id: str, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing ticket.
        """
        return self._request("PUT", f"tickets/{ticket_id}", data=ticket_data)
    
    def delete_ticket(self, ticket_id: str) -> None:
        """
        Delete a ticket.
        """
        self._request("DELETE", f"tickets/{ticket_id}")
    
    def update_ticket_status(self, ticket_id: str, status_id: str) -> Dict[str, Any]:
        """
        Update ticket status.
        """
        return self.update_ticket(ticket_id, {"status_id": status_id})
    
    # ============================================================================
    # Ticket Items / Line Items
    # ============================================================================
    
    def list_ticket_items(self, ticket_id: str) -> List[Dict[str, Any]]:
        """
        List line items for a ticket.
        """
        return self._request("GET", f"tickets/{ticket_id}/ticket_items")
    
    def create_ticket_item(
        self,
        ticket_id: str,
        item_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a line item for a ticket.
        
        Args:
            ticket_id: Ticket ID
            item_data: Item data:
                - product_id: Product ID (for inventory item)
                - service_id: Service ID (for service)
                - quantity: Quantity
                - price: Unit price
                - name: Custom name
                - description: Description
        """
        return self._request("POST", f"tickets/{ticket_id}/ticket_items", data=item_data)
    
    def update_ticket_item(
        self,
        ticket_id: str,
        item_id: str,
        item_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a line item.
        """
        return self._request(
            "PUT",
            f"tickets/{ticket_id}/ticket_items/{item_id}",
            data=item_data
        )
    
    def delete_ticket_item(self, ticket_id: str, item_id: str) -> None:
        """
        Delete a line item.
        """
        self._request("DELETE", f"tickets/{ticket_id}/ticket_items/{item_id}")
    
    # ============================================================================
    # Customers
    # ============================================================================
    
    def list_customers(
        self,
        page: int = 1,
        limit: int = 50,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List customers.
        
        Args:
            page: Page number
            limit: Items per page (max 500)
            search: Search query
            
        Returns:
            Customers response
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        
        if search:
            params["q"] = search
        
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
                - first_name: First name (required)
                - last_name: Last name (required)
                - email: Email address
                - phone: Phone number
                - mobile: Mobile phone
                - address: Address
                - city: City
                - state: State/Province
                - zip: Postal code
                - country: Country
                - business_name: Business name
                - customer_type_id: Customer type ID
                - notes: Notes
        """
        return self._request("POST", "customers", data=customer_data)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing customer.
        """
        return self._request("PUT", f"customers/{customer_id}", data=customer_data)
    
    def delete_customer(self, customer_id: str) -> None:
        """
        Delete a customer.
        """
        self._request("DELETE", f"customers/{customer_id}")
    
    # ============================================================================
    # Products / Inventory
    # ============================================================================
    
    def list_products(
        self,
        page: int = 1,
        limit: int = 50,
        category_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List products.
        
        Args:
            page: Page number
            limit: Items per page (max 500)
            category_id: Filter by category ID
            
        Returns:
            Products response
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        
        if category_id:
            params["category_id"] = category_id
        
        return self._request("GET", "products", params=params)
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get details of a specific product.
        """
        return self._request("GET", f"products/{product_id}")
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product.
        
        Args:
            product_data: Product data dict:
                - name: Product name (required)
                - sku: SKU
                - category_id: Category ID
                - cost: Unit cost
                - price: Unit price
                - quantity: Initial quantity
                - taxable: Taxable status
                - description: Description
        """
        return self._request("POST", "products", data=product_data)
    
    def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product.
        """
        return self._request("PUT", f"products/{product_id}", data=product_data)
    
    def adjust_product_inventory(
        self,
        product_id: str,
        quantity: int,
        note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Adjust product inventory.
        
        Args:
            product_id: Product ID
            quantity: Quantity adjustment (positive or negative)
            note: Adjustment note
            
        Returns:
            Updated product
        """
        data = {
            "quantity_change": quantity
        }
        if note:
            data["note"] = note
        
        return self._request("POST", f"products/{product_id}/adjust_inventory", data=data)
    
    # ============================================================================
    # Services
    # ============================================================================
    
    def list_services(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """
        List services.
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        return self._request("GET", "services", params=params)
    
    def get_service(self, service_id: str) -> Dict[str, Any]:
        """
        Get details of a specific service.
        """
        return self._request("GET", f"services/{service_id}")
    
    def create_service(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new service.
        
        Args:
            service_data: Service data:
                - name: Service name (required)
                - price: Service price
                - duration: Duration in minutes
                - taxable: Taxable status
                - description: Description
        """
        return self._request("POST", "services", data=service_data)
    
    def update_service(self, service_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a service.
        """
        return self._request("PUT", f"services/{service_id}", data=service_data)
    
    # ============================================================================
    # Invoices
    # ============================================================================
    
    def list_invoices(
        self,
        page: int = 1,
        limit: int = 50,
        customer_id: Optional[str] = None,
        status_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List invoices.
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        
        if customer_id:
            params["customer_id"] = customer_id
        if status_id:
            params["status_id"] = status_id
        
        return self._request("GET", "invoices", params=params)
    
    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Get details of an invoice.
        """
        return self._request("GET", f"invoices/{invoice_id}")
    
    def convert_ticket_to_invoice(self, ticket_id: str) -> Dict[str, Any]:
        """
        Convert a ticket to an invoice.
        """
        return self._request("POST", f"tickets/{ticket_id}/convert_to_invoice")
    
    def email_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Send invoice to customer via email.
        """
        return self._request("POST", f"invoices/{invoice_id}/email")
    
    # ============================================================================
    # Estimates
    # ============================================================================
    
    def list_estimates(
        self,
        page: int = 1,
        limit: int = 50,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List estimates.
        """
        params = {
            "page": page,
            "limit": min(limit, 500)
        }
        
        if customer_id:
            params["customer_id"] = customer_id
        
        return self._request("GET", "estimates", params=params)
    
    def get_estimate(self, estimate_id: str) -> Dict[str, Any]:
        """
        Get details of an estimate.
        """
        return self._request("GET", f"estimates/{estimate_id}")
    
    def convert_estimate_to_invoice(self, estimate_id: str) -> Dict[str, Any]:
        """
        Convert an estimate to an invoice.
        """
        return self._request("POST", f"estimates/{estimate_id}/convert_to_invoice")
    
    # ============================================================================
    # Lead Sources
    # ============================================================================
    
    def list_lead_sources(self) -> List[Dict[str, Any]]:
        """
        List lead sources.
        """
        return self._request("GET", "lead_sources")
    
    # ============================================================================
    # Statuses
    # ============================================================================
    
    def list_statuses(self) -> List[Dict[str, Any]]:
        """
        List ticket statuses.
        """
        return self._request("GET", "statuses")
    
    def get_status(self, status_id: str) -> Dict[str, Any]:
        """
        Get details of a status.
        """
        return self._request("GET", f"statuses/{status_id}")
    
    # ============================================================================
    # Brands
    # ============================================================================
    
    def list_brands(self) -> List[Dict[str, Any]]:
        """
        List device brands.
        """
        return self._request("GET", "brands")
    
    # ============================================================================
    # Locations
    # ============================================================================
    
    def list_locations(self) -> List[Dict[str, Any]]:
        """
        List shop locations.
        """
        return self._request("GET", "locations")
    
    # ============================================================================
    # Staff
    # ============================================================================
    
    def list_staff(self) -> List[Dict[str, Any]]:
        """
        List staff members.
        """
        return self._request("GET", "users")
    
    # ============================================================================
    # Search
    # ============================================================================
    
    def search(self, query: str, resource: Optional[str] = None) -> Dict[str, Any]:
        """
        Search across resources.
        
        Args:
            query: Search query
            resource: Specific resource to search (customers, tickets, products, services)
            
        Returns:
            Search results
        """
        params = {"q": query}
        if resource:
            params["type"] = resource
        
        return self._request("GET", "search", params=params)
    
    # ============================================================================
    # Account
    # ============================================================================
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        """
        return self._request("GET", "account")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()