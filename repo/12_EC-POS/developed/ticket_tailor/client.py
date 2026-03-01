"""
Ticket Tailor Client - REST API Implementation
Ticket Tailor API documentation: https://developers.tickettailor.com/
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class TicketTailorClient:
    """
    Complete client for Ticket Tailor REST API.
    Supports Events, Tickets, Orders, Attendees, and more.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Ticket Tailor client.
        
        Args:
            api_key: API key (from env: TICKETTAILOR_API_KEY)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Environment variables:
            TICKETTAILOR_API_KEY: Your Ticket Tailor API key
        """
        self.api_key = api_key or os.getenv("TICKETTAILOR_API_KEY")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set TICKETTAILOR_API_KEY environment variable."
            )
        
        self.base_url = "https://api.tickettailor.com/v1"
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
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
        Make HTTP request to Ticket Tailor API.
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
    
    def _get_all_pages(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all pages of a paginated endpoint.
        """
        items = []
        page = 1
        per_page = 100
        
        while True:
            current_params = {**(params or {}), "page": page, "per_page": per_page}
            response = self._request("GET", endpoint, params=current_params)
            
            data_key = endpoint.split("/")[-1]
            data = response.get("data", [])
            
            if not data:
                break
            
            items.extend(data)
            
            if len(data) < per_page:
                break
            
            page += 1
        
        return items
    
    # ============================================================================
    # Events
    # ============================================================================
    
    def list_events(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List events.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            status: Filter by status (upcoming, live, past, draft)
            search: Search query
            
        Returns:
            Paginated events response
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        
        return self._request("GET", "events", params=params)
    
    def get_event(self, event_id: str) -> Dict[str, Any]:
        """
        Get details of a specific event.
        """
        return self._request("GET", f"events/{event_id}")
    
    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new event.
        
        Args:
            event_data: Event data dict:
                - name: Event name (required)
                - start_date: Start date (ISO 8601)
                - end_date: End date (ISO 8601)
                - venue: Venue information
                - description: Event description
                - is_virtual: Is virtual event
                - virtual_event_url: Virtual event URL
                
        Returns:
            Created event response
        """
        return self._request("POST", "events", data=event_data)
    
    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing event.
        """
        return self._request("PUT", f"events/{event_id}", data=event_data)
    
    def list_event_tickets(
        self,
        event_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        List tickets for an event.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", f"events/{event_id}/tickets", params=params)
    
    # ============================================================================
    # Tickets
    # ============================================================================
    
    def list_tickets(
        self,
        page: int = 1,
        per_page: int = 20,
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all tickets across all events.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        
        if event_id:
            params["event_id"] = event_id
        
        return self._request("GET", "tickets", params=params)
    
    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get details of a specific ticket type.
        """
        return self._request("GET", f"tickets/{ticket_id}")
    
    def create_ticket(
        self,
        event_id: str,
        ticket_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new ticket type for an event.
        
        Args:
            event_id: Event ID
            ticket_data: Ticket data dict:
                - name: Ticket name (required)
                - price: Ticket price in cents (required)
                - max_per_order: Max tickets per order
                - total_quantity: Total available quantity
                - description: Ticket description
                - display_order: Display order
                - is_hidden: Hide ticket type
                - is_virtual: Is virtual ticket
                
        Returns:
            Created ticket response
        """
        return self._request("POST", f"events/{event_id}/tickets", data=ticket_data)
    
    def update_ticket(self, ticket_id: str, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing ticket type.
        """
        return self._request("PUT", f"tickets/{ticket_id}", data=ticket_data)
    
    def delete_ticket(self, ticket_id: str) -> None:
        """
        Delete a ticket type.
        """
        self._request("DELETE", f"tickets/{ticket_id}")
    
    # ============================================================================
    # Orders
    # ============================================================================
    
    def list_orders(
        self,
        page: int = 1,
        per_page: int = 20,
        event_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List orders.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            event_id: Filter by event ID
            status: Filter by status (pending, paid, refunded, cancelled)
            search: Search query
            from_date: Filter orders after this date
            to_date: Filter orders before this date
            
        Returns:
            Paginated orders response
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        
        if event_id:
            params["event_id"] = event_id
        if status:
            params["status"] = status
        if search:
            params["search"] = search
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
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            order_data: Order data dict:
                - event_id: Event ID (required)
                - currency: Currency code (e.g., "USD")
                - status: Order status
                - billing_address: Billing address object
                - tickets: Array of tickets with:
                    - ticket_id: Ticket type ID (required)
                    - quantity: Quantity (required)
                    - first_name: Attendee first name
                    - last_name: Attendee last name
                    - email: Attendee email
                    
        Returns:
            Created order response
        """
        return self._request("POST", "orders", data=order_data)
    
    def update_order(self, order_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing order.
        """
        return self._request("PUT", f"orders/{order_id}", data=order_data)
    
    def refund_order(self, order_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Refund an order.
        
        Args:
            order_id: Order ID
            reason: Optional refund reason
            
        Returns:
            Updated order
        """
        data = {"status": "refunded"}
        if reason:
            data["refund_reason"] = reason
        
        return self._request("PUT", f"orders/{order_id}", data=data)
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order.
        """
        return self._request("PUT", f"orders/{order_id}", data={"status": "cancelled"})
    
    # ============================================================================
    # Attendees
    # ============================================================================
    
    def list_attendees(
        self,
        page: int = 1,
        per_page: int = 20,
        event_id: Optional[str] = None,
        order_id: Optional[str] = None,
        ticket_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        check_in: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        List attendees.
        
        Args:
            page: Page number
            per_page: Items per page (max 100)
            event_id: Filter by event ID
            order_id: Filter by order ID
            ticket_id: Filter by ticket ID
            status: Filter by status (active, refunded, etc.)
            search: Search query
            check_in: Filter by check-in status
            
        Returns:
            Paginated attendees response
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        
        if event_id:
            params["event_id"] = event_id
        if order_id:
            params["order_id"] = order_id
        if ticket_id:
            params["ticket_id"] = ticket_id
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        if check_in is not None:
            params["check_in"] = str(check_in).lower()
        
        return self._request("GET", "attendees", params=params)
    
    def get_attendee(self, attendee_id: str) -> Dict[str, Any]:
        """
        Get details of a specific attendee.
        """
        return self._request("GET", f"attendees/{attendee_id}")
    
    def update_attendee(self, attendee_id: str, attendee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update attendee information.
        
        Args:
            attendee_id: Attendee ID
            attendee_data: Updated data:
                - first_name: First name
                - last_name: Last name
                - email: Email address
                - phone: Phone number
                - has_checked_in: Check-in status
        """
        return self._request("PUT", f"attendees/{attendee_id}", data=attendee_data)
    
    def check_in_attendee(self, attendee_id: str) -> Dict[str, Any]:
        """
        Mark attendee as checked in.
        """
        return self._request("PUT", f"attendees/{attendee_id}", data={"has_checked_in": True})
    
    def undo_check_in(self, attendee_id: str) -> Dict[str, Any]:
        """
        Undo attendee check-in.
        """
        return self._request("PUT", f"attendees/{attendee_id}", data={"has_checked_in": False})
    
    def bulk_check_in(
        self,
        attendee_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Bulk check in multiple attendees.
        
        Args:
            attendee_ids: List of attendee IDs
            
        Returns:
            Bulk operation results
        """
        return self._request(
            "POST",
            "attendees/bulk_check_in",
            data={"attendee_ids": attendee_ids}
        )
    
    # ============================================================================
    # Venues
    # ============================================================================
    
    def list_venues(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        List venues.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", "venues", params=params)
    
    def get_venue(self, venue_id: str) -> Dict[str, Any]:
        """
        Get details of a specific venue.
        """
        return self._request("GET", f"venues/{venue_id}")
    
    def create_venue(self, venue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new venue.
        
        Args:
            venue_data: Venue data dict:
                - name: Venue name (required)
                - address: Address object with:
                    - line1: Street address
                    - line2: (optional)
                    - city: City
                    - state: State/region
                    - postcode: Postal code
                    - country: Country code (ISO 3166-1 alpha-2)
                - latitude: Latitude
                - longitude: Longitude
                - website: Website URL
                - description: Venue description
                
        Returns:
            Created venue response
        """
        return self._request("POST", "venues", data=venue_data)
    
    def update_venue(self, venue_id: str, venue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing venue.
        """
        return self._request("PUT", f"venues/{venue_id}", data=venue_data)
    
    # ============================================================================
    # Organisations
    # ============================================================================
    
    def get_organisation(self) -> Dict[str, Any]:
        """
        Get organisation details.
        """
        return self._request("GET", "organisation")
    
    def update_organisation(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update organisation details.
        
        Args:
            org_data: Organisation data:
                - name: Organisation name
                - email: Contact email
                - phone: Phone number
                - website: Website URL
                - description: Description
                - currency: Default currency
        """
        return self._request("PUT", "organisation", data=org_data)
    
    # ============================================================================
    # Webhooks
    # ============================================================================
    
    def list_webhooks(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        List all webhooks.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", "webhooks", params=params)
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Get details of a specific webhook.
        """
        return self._request("GET", f"webhooks/{webhook_id}")
    
    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            url: Webhook URL (required)
            events: List of event types (required)
            secret: Optional secret for signature verification
            description: Optional webhook description
            
        Returns:
            Created webhook response
        """
        data = {
            "url": url,
            "events": events
        }
        
        if secret:
            data["secret"] = secret
        if description:
            data["description"] = description
        
        return self._request("POST", "webhooks", data=data)
    
    def update_webhook(self, webhook_id: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing webhook.
        """
        return self._request("PUT", f"webhooks/{webhook_id}", data=webhook_data)
    
    def delete_webhook(self, webhook_id: str) -> None:
        """
        Delete a webhook.
        """
        self._request("DELETE", f"webhooks/{webhook_id}")
    
    def test_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Send a test notification to a webhook.
        """
        return self._request("POST", f"webhooks/{webhook_id}/test")
    
    # ============================================================================
    # Discounts / Promo Codes
    # ============================================================================
    
    def list_discounts(
        self,
        page: int = 1,
        per_page: int = 20,
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List discounts/promo codes.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        
        if event_id:
            params["event_id"] = event_id
        
        return self._request("GET", "discounts", params=params)
    
    def get_discount(self, discount_id: str) -> Dict[str, Any]:
        """
        Get details of a specific discount.
        """
        return self._request("GET", f"discounts/{discount_id}")
    
    def create_discount(self, discount_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new discount/promo code.
        
        Args:
            discount_data: Discount data dict:
                - code: Promo code (required)
                - discount_type: Type (percentage, fixed)
                - discount_amount: Discount amount (required)
                - event_id: Apply to specific event (optional)
                - max_uses: Maximum usage limit
                - expiry_date: Expiry date (ISO 8601)
                - minimum_spend: Minimum spend to apply
                - description: Discount description
                
        Returns:
            Created discount response
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
    
    # ============================================================================
    # Series (Recurring Events)
    # ============================================================================
    
    def list_series(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        List event series.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", "series", params=params)
    
    def get_series(self, series_id: str) -> Dict[str, Any]:
        """
        Get details of a specific series.
        """
        return self._request("GET", f"series/{series_id}")
    
    def list_series_events(
        self,
        series_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        List events in a series.
        """
        params = {
            "page": page,
            "per_page": min(per_page, 100)
        }
        return self._request("GET", f"series/{series_id}/events", params=params)
    
    # ============================================================================
    # Analytics / Reports
    # ============================================================================
    
    def get_event_sales_summary(
        self,
        event_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get sales summary for an event.
        
        Args:
            event_id: Event ID
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
        """
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        
        return self._request("GET", f"events/{event_id}/sales_summary", params=params)
    
    def get_attendee_statistics(
        self,
        event_id: str
    ) -> Dict[str, Any]:
        """
        Get attendee statistics for an event.
        """
        return self._request("GET", f"events/{event_id}/attendee_statistics")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()