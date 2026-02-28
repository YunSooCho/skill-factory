"""
RD Station CRM API Client
API Documentation: https://developers.rdstation.com/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class RdStationCrmAPIError(Exception):
    """Custom exception for RD Station CRM API errors."""
    pass


class RdStationCrmClient:
    """Client for RD Station CRM API."""

    def __init__(self, api_token: str, base_url: str = "https://plugcrm.net/api/v1"):
        """
        Initialize RD Station CRM API client.

        Args:
            api_token: Your RD Station CRM API token
            base_url: API base URL (default: https://plugcrm.net/api/v1)
        """
        self.api_token = api_token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
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
            raise RdStationCrmAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise RdStationCrmAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_deal(
        self,
        name: str,
        deal_stage_id: str,
        user_id: str,
        value: Optional[float] = None,
        currency: str = "BRL",
        organization_id: Optional[str] = None,
        expected_close_date: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new deal (Create Deal).

        API Reference: Deals endpoint

        Args:
            name: Deal name
            deal_stage_id: Deal stage ID
            user_id: Owner user ID
            value: Deal value
            currency: Currency code (default: BRL)
            organization_id: Associated organization ID
            expected_close_date: Expected close date (YYYY-MM-DD)
            custom_fields: Custom field values

        Returns:
            Created deal information with ID
        """
        endpoint = "/deals"

        data = {
            "name": name,
            "deal_stage_id": deal_stage_id,
            "user_id": user_id,
            "amount": value,
            "currency": currency
        }

        if organization_id:
            data["organization_id"] = organization_id
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", endpoint, json=data)

    def get_deal(self, deal_id: int) -> Dict[str, Any]:
        """
        Get deal details (Get Deal).

        API Reference: Deals GET endpoint

        Args:
            deal_id: Deal ID

        Returns:
            Deal details
        """
        endpoint = f"/deals/{deal_id}"
        return self._make_request("GET", endpoint)

    def update_deal(
        self,
        deal_id: int,
        name: Optional[str] = None,
        deal_stage_id: Optional[str] = None,
        value: Optional[float] = None,
        expected_close_date: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update a deal (Update Deal).

        API Reference: Deals PUT endpoint

        Args:
            deal_id: Deal ID
            name: Deal name
            deal_stage_id: Deal stage ID
            value: Deal value
            expected_close_date: Expected close date (YYYY-MM-DD)
            custom_fields: Custom field values

        Returns:
            Updated deal information
        """
        endpoint = f"/deals/{deal_id}"

        data = {}

        if name:
            data["name"] = name
        if deal_stage_id:
            data["deal_stage_id"] = deal_stage_id
        if value is not None:
            data["amount"] = value
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", endpoint, json=data)

    def delete_deal(self, deal_id: int) -> Dict[str, Any]:
        """
        Delete a deal (Delete Deal).

        API Reference: Deals DELETE endpoint

        Args:
            deal_id: Deal ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/deals/{deal_id}"
        return self._make_request("DELETE", endpoint)

    def search_deals(
        self,
        user_id: Optional[str] = None,
        deal_stage_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        per_page: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search deals (Search Deal).

        API Reference: Deals search endpoint

        Args:
            user_id: Filter by owner user ID
            deal_stage_id: Filter by deal stage ID
            organization_id: Filter by organization ID
            per_page: Results per page (default: 20)
            page: Page number (default: 1)

        Returns:
            List of deals
        """
        endpoint = "/deals"

        params = {
            "per_page": str(per_page),
            "page": str(page)
        }

        if user_id:
            params["user_id"] = user_id
        if deal_stage_id:
            params["deal_stage_id"] = deal_stage_id
        if organization_id:
            params["organization_id"] = organization_id

        return self._make_request("GET", endpoint, params=params)

    def create_lead(
        self,
        name: str,
        email: str,
        organization_id: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new lead (Create Lead).

        API Reference: Leads endpoint

        Args:
            name: Lead name
            email: Email address
            organization_id: Associated organization ID
            custom_fields: Custom field values

        Returns:
            Created lead information with ID
        """
        endpoint = "/leads"

        data = {
            "name": name,
            "emails": [{"email": email}]
        }

        if organization_id:
            data["organization_id"] = organization_id
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", endpoint, json=data)

    def get_lead(self, lead_id: int) -> Dict[str, Any]:
        """
        Get lead details (Get Lead).

        API Reference: Leads GET endpoint

        Args:
            lead_id: Lead ID

        Returns:
            Lead details
        """
        endpoint = f"/leads/{lead_id}"
        return self._make_request("GET", endpoint)

    def update_lead(
        self,
        lead_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update a lead (Update Lead).

        API Reference: Leads PUT endpoint

        Args:
            lead_id: Lead ID
            name: Lead name
            email: Email address
            custom_fields: Custom field values

        Returns:
            Updated lead information
        """
        endpoint = f"/leads/{lead_id}"

        data = {}

        if name:
            data["name"] = name
        if email:
            data["emails"] = [{"email": email}]
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", endpoint, json=data)

    def delete_lead(self, lead_id: int) -> Dict[str, Any]:
        """
        Delete a lead (Delete Lead).

        API Reference: Leads DELETE endpoint

        Args:
            lead_id: Lead ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/leads/{lead_id}"
        return self._make_request("DELETE", endpoint)

    def search_leads(
        self,
        q: Optional[str] = None,
        per_page: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search leads (Search Lead).

        API Reference: Leads search endpoint

        Args:
            q: Search query
            per_page: Results per page (default: 20)
            page: Page number (default: 1)

        Returns:
            List of leads
        """
        endpoint = "/leads"

        params = {
            "per_page": str(per_page),
            "page": str(page)
        }

        if q:
            params["q"] = q

        return self._make_request("GET", endpoint, params=params)

    def create_organization(
        self,
        name: str,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new organization (Create Organization).

        API Reference: Organizations endpoint

        Args:
            name: Organization name
            website: Website URL
            phone: Phone number
            custom_fields: Custom field values

        Returns:
            Created organization information with ID
        """
        endpoint = "/organizations"

        data = {"name": name}

        if website:
            data["website"] = website
        if phone:
            data["phone"] = phone
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", endpoint, json=data)

    def get_organization(self, organization_id: int) -> Dict[str, Any]:
        """
        Get organization details (Get Organization).

        API Reference: Organizations GET endpoint

        Args:
            organization_id: Organization ID

        Returns:
            Organization details
        """
        endpoint = f"/organizations/{organization_id}"
        return self._make_request("GET", endpoint)

    def update_organization(
        self,
        organization_id: int,
        name: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an organization (Update Organization).

        API Reference: Organizations PUT endpoint

        Args:
            organization_id: Organization ID
            name: Organization name
            website: Website URL
            phone: Phone number
            custom_fields: Custom field values

        Returns:
            Updated organization information
        """
        endpoint = f"/organizations/{organization_id}"

        data = {}

        if name:
            data["name"] = name
        if website:
            data["website"] = website
        if phone:
            data["phone"] = phone
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", endpoint, json=data)

    def search_organizations(
        self,
        q: Optional[str] = None,
        per_page: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search organizations (Search Organization).

        API Reference: Organizations search endpoint

        Args:
            q: Search query
            per_page: Results per page (default: 20)
            page: Page number (default: 1)

        Returns:
            List of organizations
        """
        endpoint = "/organizations"

        params = {
            "per_page": str(per_page),
            "page": str(page)
        }

        if q:
            params["q"] = q

        return self._make_request("GET", endpoint, params=params)

    def create_task(
        self,
        description: str,
        type: str,
        deadline: str
    ) -> Dict[str, Any]:
        """
        Create a new task (Create Task).

        API Reference: Tasks endpoint

        Args:
            description: Task description
            type: Task type (call, email, meeting, task)
            deadline: Deadline date and time (ISO 8601 format)

        Returns:
            Created task information with ID
        """
        endpoint = "/tasks"

        data = {
            "description": description,
            "type": type,
            "deadline": deadline
        }

        return self._make_request("POST", endpoint, json=data)

    def update_task(
        self,
        task_id: int,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a task (Update Task).

        API Reference: Tasks PUT endpoint

        Args:
            task_id: Task ID
            description: Task description
            status: Task status (open, completed)

        Returns:
            Updated task information
        """
        endpoint = f"/tasks/{task_id}"

        data = {}

        if description:
            data["description"] = description
        if status:
            data["status"] = status

        return self._make_request("PUT", endpoint, json=data)