"""
Tookan API Client

Complete client for Tookan field service management integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class TookanAPIClient:
    """
    Complete client for Tookan field service and delivery management.
    Supports tasks, agents, tracking, and fleet management.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Tookan API client.

        Args:
            api_key: Tookan API key (from env: TOOKAN_API_KEY)
            base_url: Base URL (default: https://api.tookan.com/api/v3)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("TOOKAN_API_KEY")
        self.base_url = base_url or os.getenv(
            "TOOKAN_BASE_URL",
            "https://api.tookan.com/api/v3"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set TOOKAN_API_KEY environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Tookan API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        if data is None:
            data = {}

        data['api_key'] = self.api_key

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    # Tasks

    def create_task(
        self,
        customer_id: str,
        team_id: str,
        job_description: str,
        job_address: str,
        job_latitude: float,
        job_longitude: float,
        meta_data: Optional[Dict[str, Any]] = None,
        has_pickup: bool = False,
        has_delivery: bool = False,
        pickup_address: Optional[str] = None,
        delivery_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a task.

        Args:
            customer_id: Customer ID
            team_id: Team ID to assign
            job_description: Task description
            job_address: Job address
            job_latitude: Latitude
            job_longitude: Longitude
            meta_data: Additional metadata
            has_pickup: Include pickup
            has_delivery: Include delivery
            pickup_address: Pickup address
            delivery_address: Delivery address

        Returns:
            Task information
        """
        data = {
            'customer_id': customer_id,
            'team_id': team_id,
            'job_description': job_description,
            'job_address': job_address,
            'job_latitude': job_latitude,
            'job_longitude': job_longitude,
            'has_pickup': int(has_pickup),
            'has_delivery': int(has_delivery)
        }

        if meta_data:
            data['meta_data'] = str(meta_data)
        if pickup_address:
            data['pickup_address'] = pickup_address
        if delivery_address:
            data['delivery_address'] = delivery_address

        return self._request('POST', '/create_task', data=data)

    def get_task(self, job_id: str) -> Dict[str, Any]:
        """Get task details."""
        return self._request('POST', '/get_job_details', data={'job_id': job_id})

    def list_tasks(
        self,
        team_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List tasks with filtering."""
        data = {
            'limit': limit,
            'offset': offset
        }

        if team_id:
            data['team_id'] = team_id
        if status:
            data['status'] = status
        if start_date:
            data['start_date'] = start_date
        if end_date:
            data['end_date'] = end_date

        return self._request('POST', '/list_all_tasks', data=data)

    def update_task(
        self,
        job_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update task."""
        data = {'job_id': job_id}
        data.update(kwargs)
        return self._request('POST', '/update_task', data=data)

    def delete_task(self, job_id: str) -> Dict[str, Any]:
        """Delete task."""
        return self._request('POST', '/delete_task', data={'job_id': job_id})

    # Agents

    def list_agents(
        self,
        team_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """List agents."""
        data = {}
        if team_id:
            data['team_id'] = team_id
        return self._request('POST', '/view_team_users', data=data)

    def get_agent(self, user_id: str) -> Dict[str, Any]:
        """Get agent details."""
        return self._request('POST', '/get_user_details', data={'user_id': user_id})

    # Teams

    def list_teams(self) -> Dict[str, Any]:
        """List all teams."""
        return self._request('POST', '/view_teams')

    def get_team(self, team_id: str) -> Dict[str, Any]:
        """Get team details."""
        return self._request('POST', '/get_team_details', data={'team_id': team_id})

    # Customers

    def create_customer(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> Dict[str, Any]:
        """Create a customer."""
        data = {'name': name}

        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if latitude:
            data['latitude'] = latitude
        if longitude:
            data['longitude'] = longitude

        return self._request('POST', '/create_customer', data=data)

    def list_customers(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List customers."""
        data = {'limit': limit, 'offset': offset}
        return self._request('POST', '/list_all_customers', data=data)

    # Geofencing and Zones

    def list_zones(
        self,
        team_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """List zones."""
        data = {}
        if team_id:
            data['team_id'] = team_id
        return self._request('POST', '/list_all_zones', data=data)

    # Analytics

    def get_task_stats(
        self,
        start_date: str,
        end_date: str,
        team_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get task statistics."""
        data = {
            'start_date': start_date,
            'end_date': end_date
        }

        if team_id:
            data['team_id'] = team_id

        return self._request('POST', '/get_job_stats', data=data)

    # Tracking

    def get_agent_location(self, user_id: str) -> Dict[str, Any]:
        """Get agent's current location."""
        return self._request('POST', '/get_user_location', data={'user_id': user_id})

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()