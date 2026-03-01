"""
Next SFA API Client
API Documentation: Japanese SFA system for sales management
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
import hmac
import hashlib


class NextSFAAPIError(Exception):
    """Custom exception for Next SFA API errors."""
    pass


class NextSFAClient:
    """Client for Next SFA API - Sales Force Automation for Japanese market."""

    def __init__(self, api_key: str, base_url: str = "https://api.next-sfa.jp/v1"):
        """
        Initialize Next SFA API client.

        Args:
            api_key: Your Next SFA API key
            base_url: API base URL (default: https://api.next-sfa.jp/v1)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise NextSFAAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise NextSFAAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise NextSFAAPIError("Invalid JSON response")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"message": response.text}

    # Company Management

    def register_company(
        self,
        company_name: str,
        company_code: Optional[str] = None,
        company_type: Optional[str] = None,
        industry: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new company.

        Args:
            company_name: Company name (required)
            company_code: Company code
            company_type: Company type
            industry: Industry
            address: Address
            phone: Phone number
            email: Email
            website: Website URL

        Returns:
            Created company data
        """
        data = {
            "company_name": company_name,
            "registered_at": datetime.now().isoformat()
        }

        if company_code:
            data["company_code"] = company_code
        if company_type:
            data["company_type"] = company_type
        if industry:
            data["industry"] = industry
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if website:
            data["website"] = website

        return self._make_request("POST", "/companies", json=data)

    def update_company(
        self,
        company_id: str,
        company_name: Optional[str] = None,
        company_type: Optional[str] = None,
        industry: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update company information.

        Args:
            company_id: Company ID
            company_name: Company name
            company_type: Company type
            industry: Industry
            address: Address
            phone: Phone number
            email: Email
            website: Website URL

        Returns:
            Updated company data
        """
        data = {}
        if company_name:
            data["company_name"] = company_name
        if company_type:
            data["company_type"] = company_type
        if industry:
            data["industry"] = industry
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if website:
            data["website"] = website

        return self._make_request("PUT", f"/companies/{company_id}", json=data)

    def get_companies(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get list of companies.

        Args:
            limit: Max results
            offset: Pagination offset

        Returns:
            List of companies
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/companies", params=params)

    def get_company(self, company_id: str) -> Dict[str, Any]:
        """
        Get company details.

        Args:
            company_id: Company ID

        Returns:
            Company data
        """
        return self._make_request("GET", f"/companies/{company_id}")

    def search_companies(
        self,
        company_name: Optional[str] = None,
        company_code: Optional[str] = None,
        industry: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for companies.

        Args:
            company_name: Company name filter
            company_code: Company code filter
            industry: Industry filter
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching companies
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if company_name:
            params["company_name"] = company_name
        if company_code:
            params["company_code"] = company_code
        if industry:
            params["industry"] = industry

        return self._make_request("GET", "/companies/search", params=params)

    # Person/Contact Management

    def get_person(self, person_id: str) -> Dict[str, Any]:
        """
        Get person/contact details.

        Args:
            person_id: Person ID

        Returns:
            Person data
        """
        return self._make_request("GET", f"/persons/{person_id}")

    def search_persons(
        self,
        company_id: Optional[str] = None,
        person_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for persons/contacts.

        Args:
            company_id: Filter by company ID
            person_name: Person name filter
            email: Email filter
            phone: Phone filter
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching persons
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if company_id:
            params["company_id"] = company_id
        if person_name:
            params["person_name"] = person_name
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone

        return self._make_request("GET", "/persons/search", params=params)

    def get_persons(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of persons.

        Args:
            limit: Max results
            offset: Pagination offset

        Returns:
            List of persons
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/persons", params=params)

    # Deal/Opportunity Management

    def register_deal(
        self,
        company_id: str,
        deal_name: str,
        deal_amount: Optional[float] = None,
        deal_stage: Optional[str] = "new",
        expected_close_date: Optional[str] = None,
        probability: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Register a new deal/opportunity.

        Args:
            company_id: Company ID (required)
            deal_name: Deal name (required)
            deal_amount: Deal amount
            deal_stage: Deal stage (new, negotiating, won, lost, standby)
            expected_close_date: Expected close date (ISO format)
            probability: Close probability (0-100)

        Returns:
            Created deal data
        """
        data = {
            "company_id": company_id,
            "deal_name": deal_name,
            "registered_at": datetime.now().isoformat()
        }

        if deal_amount is not None:
            data["deal_amount"] = deal_amount
        if deal_stage:
            data["deal_stage"] = deal_stage
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if probability is not None:
            data["probability"] = probability

        return self._make_request("POST", "/deals", json=data)

    def update_deal(
        self,
        deal_id: str,
        deal_name: Optional[str] = None,
        deal_amount: Optional[float] = None,
        deal_stage: Optional[str] = None,
        expected_close_date: Optional[str] = None,
        probability: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update deal information.

        Args:
            deal_id: Deal ID
            deal_name: Deal name
            deal_amount: Deal amount
            deal_stage: Deal stage
            expected_close_date: Expected close date
            probability: Close probability (0-100)

        Returns:
            Updated deal data
        """
        data = {}
        if deal_name:
            data["deal_name"] = deal_name
        if deal_amount is not None:
            data["deal_amount"] = deal_amount
        if deal_stage:
            data["deal_stage"] = deal_stage
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if probability is not None:
            data["probability"] = probability

        return self._make_request("PUT", f"/deals/{deal_id}", json=data)

    def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Get deal details.

        Args:
            deal_id: Deal ID

        Returns:
            Deal data
        """
        return self._make_request("GET", f"/deals/{deal_id}")

    def get_deals(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of deals.

        Args:
            limit: Max results
            offset: Pagination offset

        Returns:
            List of deals
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/deals", params=params)

    def search_deals(
        self,
        company_id: Optional[str] = None,
        deal_stage: Optional[str] = None,
        deal_name: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for deals.

        Args:
            company_id: Filter by company ID
            deal_stage: Filter by deal stage
            deal_name: Filter by deal name
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching deals
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if company_id:
            params["company_id"] = company_id
        if deal_stage:
            params["deal_stage"] = deal_stage
        if deal_name:
            params["deal_name"] = deal_name

        return self._make_request("GET", "/deals/search", params=params)

    # Order/Contract Management

    def register_order(
        self,
        deal_id: str,
        order_number: str,
        order_amount: float,
        order_date: Optional[str] = None,
        delivery_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new order.

        Args:
            deal_id: Deal ID (required)
            order_number: Order number (required)
            order_amount: Order amount (required)
            order_date: Order date (ISO format)
            delivery_date: Expected delivery date (ISO format)

        Returns:
            Created order data
        """
        data = {
            "deal_id": deal_id,
            "order_number": order_number,
            "order_amount": order_amount,
            "ordered_at": datetime.now().isoformat()
        }

        if order_date:
            data["order_date"] = order_date
        if delivery_date:
            data["delivery_date"] = delivery_date

        return self._make_request("POST", "/orders", json=data)

    def update_order(
        self,
        order_id: str,
        order_number: Optional[str] = None,
        order_amount: Optional[float] = None,
        order_date: Optional[str] = None,
        delivery_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update order information.

        Args:
            order_id: Order ID
            order_number: Order number
            order_amount: Order amount
            order_date: Order date
            delivery_date: Delivery date

        Returns:
            Updated order data
        """
        data = {}
        if order_number:
            data["order_number"] = order_number
        if order_amount is not None:
            data["order_amount"] = order_amount
        if order_date:
            data["order_date"] = order_date
        if delivery_date:
            data["delivery_date"] = delivery_date

        return self._make_request("PUT", f"/orders/{order_id}", json=data)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get order details.

        Args:
            order_id: Order ID

        Returns:
            Order data
        """
        return self._make_request("GET", f"/orders/{order_id}")

    def get_orders(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of orders.

        Args:
            limit: Max results
            offset: Pagination offset

        Returns:
            List of orders
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/orders", params=params)

    def search_orders(
        self,
        deal_id: Optional[str] = None,
        order_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for orders.

        Args:
            deal_id: Filter by deal ID
            order_number: Filter by order number
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching orders
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if deal_id:
            params["deal_id"] = deal_id
        if order_number:
            params["order_number"] = order_number

        return self._make_request("GET", "/orders/search", params=params)

    def add_product_to_order(
        self,
        order_id: str,
        product_id: str,
        quantity: int,
        unit_price: float
    ) -> Dict[str, Any]:
        """
        Add a product to an order.

        Args:
            order_id: Order ID (required)
            product_id: Product ID (required)
            quantity: Quantity (required)
            unit_price: Unit price (required)

        Returns:
            Created order item data
        """
        data = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price
        }
        return self._make_request("POST", f"/orders/{order_id}/items", json=data)

    # Sales/Revenue Management

    def register_sales(
        self,
        order_id: str,
        sales_amount: float,
        sales_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register sales revenue.

        Args:
            order_id: Order ID (required)
            sales_amount: Sales amount (required)
            sales_date: Sales date (ISO format)

        Returns:
            Created sales data
        """
        data = {
            "order_id": order_id,
            "sales_amount": sales_amount,
            "recorded_at": datetime.now().isoformat()
        }

        if sales_date:
            data["sales_date"] = sales_date

        return self._make_request("POST", "/sales", json=data)

    def update_sales(
        self,
        sales_id: str,
        sales_amount: Optional[float] = None,
        sales_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update sales information.

        Args:
            sales_id: Sales ID
            sales_amount: Sales amount
            sales_date: Sales date

        Returns:
            Updated sales data
        """
        data = {}
        if sales_amount is not None:
            data["sales_amount"] = sales_amount
        if sales_date:
            data["sales_date"] = sales_date

        return self._make_request("PUT", f"/sales/{sales_id}", json=data)

    def get_sales(self, sales_id: str) -> Dict[str, Any]:
        """
        Get sales details.

        Args:
            sales_id: Sales ID

        Returns:
            Sales data
        """
        return self._make_request("GET", f"/sales/{sales_id}")

    def search_sales(
        self,
        order_id: Optional[str] = None,
        company_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for sales records.

        Args:
            order_id: Filter by order ID
            company_id: Filter by company ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of sales records
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if order_id:
            params["order_id"] = order_id
        if company_id:
            params["company_id"] = company_id

        return self._make_request("GET", "/sales/search", params=params)

    def delete_sales(self, sales_id: str) -> Dict[str, Any]:
        """
        Delete sales record.

        Args:
            sales_id: Sales ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/sales/{sales_id}")

    # Activity/Interaction Management

    def register_activity(
        self,
        company_id: str,
        activity_type: str,
        description: str,
        activity_date: Optional[str] = None,
        person_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a business activity/interaction.

        Args:
            company_id: Company ID (required)
            activity_type: Activity type (email, call, meeting, visit, etc.)
            description: Activity description (required)
            activity_date: Activity date (ISO format)
            person_id: Associated person ID

        Returns:
            Created activity data
        """
        data = {
            "company_id": company_id,
            "activity_type": activity_type,
            "description": description,
            "created_at": datetime.now().isoformat()
        }

        if activity_date:
            data["activity_date"] = activity_date
        if person_id:
            data["person_id"] = person_id

        return self._make_request("POST", "/activities", json=data)

    def update_activity(
        self,
        activity_id: str,
        activity_type: Optional[str] = None,
        description: Optional[str] = None,
        activity_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update activity information.

        Args:
            activity_id: Activity ID
            activity_type: Activity type
            description: Activity description
            activity_date: Activity date

        Returns:
            Updated activity data
        """
        data = {}
        if activity_type:
            data["activity_type"] = activity_type
        if description:
            data["description"] = description
        if activity_date:
            data["activity_date"] = activity_date

        return self._make_request("PUT", f"/activities/{activity_id}", json=data)

    def get_activity(self, activity_id: str) -> Dict[str, Any]:
        """
        Get activity details.

        Args:
            activity_id: Activity ID

        Returns:
            Activity data
        """
        return self._make_request("GET", f"/activities/{activity_id}")

    def get_activities(
        self,
        company_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get list of activities.

        Args:
            company_id: Filter by company ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of activities
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if company_id:
            params["company_id"] = company_id

        return self._make_request("GET", "/activities", params=params)

    def search_activities(
        self,
        company_id: Optional[str] = None,
        activity_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for activities.

        Args:
            company_id: Filter by company ID
            activity_type: Filter by activity type
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching activities
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if company_id:
            params["company_id"] = company_id
        if activity_type:
            params["activity_type"] = activity_type

        return self._make_request("GET", "/activities/search", params=params)

    # User Management

    def get_staff_list(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of staff/users.

        Args:
            limit: Max results
            offset: Pagination offset

        Returns:
            List of staff
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/staff", params=params)

    # Webhook Handling

    def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Supported events:
        - activity_registered
        - activity_updated
        - deal_registered
        - deal_updated
        - order_registered
        - order_updated
        - company_registered
        - sales_registered
        - sales_updated

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if not event_type:
            raise NextSFAAPIError("Missing event_type in webhook payload")

        return {
            "event": event_type,
            "data": event_data,
            "processed_at": datetime.now().isoformat()
        }

    def verify_webhook_signature(
        self,
        payload: str,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Verify webhook signature for security.

        Args:
            payload: Raw webhook payload string
            signature: Signature from webhook header
            webhook_secret: Your webhook secret

        Returns:
            True if signature is valid
        """
        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# Example usage
if __name__ == "__main__":
    client = NextSFAClient(api_key="your_api_key_here")

    try:
        result = client.register_company(
            company_name="株式会社サンプル",
            company_code="SAMPLE001",
            industry="IT・通信"
        )
        print("Company registered:", result)
    except NextSFAAPIError as e:
        print(f"Error: {e}")