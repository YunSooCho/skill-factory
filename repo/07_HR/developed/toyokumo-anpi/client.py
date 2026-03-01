"""
Toyokumo Anpi Safety Confirmation API Client

This module provides a Python client for interacting with the Toyokumo Anpi
safety confirmation system API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class ToyokumoAnpiClient:
    """
    Client for Toyokumo Anpi Safety Confirmation System API.

    Toyokumo Anpi provides:
    - Employee safety confirmation during disasters
    - Emergency contact management
    - Location tracking
    - Status reporting
    """

    def __init__(
        self,
        api_key: str,
        organization_id: str,
        base_url: str = "https://api.toyokumo-anpi.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the Toyokumo Anpi client.

        Args:
            api_key: Your Toyokumo Anpi API key
            organization_id: Your organization ID
            base_url: API base URL (default: https://api.toyokumo-anpi.com/v1)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.organization_id = organization_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Organization-ID': organization_id
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_confirmation(
        self,
        title: str,
        message: str,
        deadline: Optional[str] = None,
        include_location: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new safety confirmation request.

        Args:
            title: Confirmation title
            message: Message to send to employees
            deadline: Deadline in ISO format (optional)
            include_location: Whether to request location information

        Returns:
            Confirmation request details
        """
        data = {
            'title': title,
            'message': message,
            'include_location': include_location
        }
        if deadline:
            data['deadline'] = deadline

        return self._request('POST', '/confirmations', data=data)

    def get_confirmation(self, confirmation_id: str) -> Dict[str, Any]:
        """
        Get confirmation details.

        Args:
            confirmation_id: Confirmation ID

        Returns:
            Confirmation details with all responses
        """
        return self._request('GET', f'/confirmations/{confirmation_id}')

    def list_confirmations(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List safety confirmations.

        Args:
            status: Filter by status (active, completed, expired)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of confirmations
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if status:
            params['status'] = status

        result = self._request('GET', '/confirmations', params=params)
        return result.get('confirmations', [])

    def get_responses(
        self,
        confirmation_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get responses for a confirmation.

        Args:
            confirmation_id: Confirmation ID
            status: Filter by response status (safe, injured, unknown)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of employee responses
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if status:
            params['status'] = status

        result = self._request(
            'GET',
            f'/confirmations/{confirmation_id}/responses',
            params=params
        )
        return result.get('responses', [])

    def get_employee_status(
        self,
        confirmation_id: str,
        employee_id: str
    ) -> Dict[str, Any]:
        """
        Get an employee's response status.

        Args:
            confirmation_id: Confirmation ID
            employee_id: Employee ID

        Returns:
            Employee's response status
        """
        return self._request(
            'GET',
            f'/confirmations/{confirmation_id}/employees/{employee_id}'
        )

    def send_reminder(
        self,
        confirmation_id: str,
        employee_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send reminder to employees who haven't responded.

        Args:
            confirmation_id: Confirmation ID
            employee_ids: List of employee IDs (if None, send to all pending)

        Returns:
            Reminder send result
        """
        data = {}
        if employee_ids:
            data['employee_ids'] = employee_ids

        return self._request(
            'POST',
            f'/confirmations/{confirmation_id}/remind',
            data=data
        )

    def close_confirmation(self, confirmation_id: str) -> Dict[str, Any]:
        """
        Close a confirmation request.

        Args:
            confirmation_id: Confirmation ID

        Returns:
            Updated confirmation
        """
        return self._request('POST', f'/confirmations/{confirmation_id}/close')

    def get_statistics(self, confirmation_id: str) -> Dict[str, Any]:
        """
        Get confirmation statistics.

        Args:
            confirmation_id: Confirmation ID

        Returns:
            Statistics including response rates and status breakdown
        """
        return self._request('GET', f'/confirmations/{confirmation_id}/statistics')

    def get_employee_contacts(self, employee_id: str) -> Dict[str, Any]:
        """
        Get emergency contact information for an employee.

        Args:
            employee_id: Employee ID

        Returns:
            Emergency contact information
        """
        return self._request('GET', f'/employees/{employee_id}/contacts')

    def update_employee_contacts(
        self,
        employee_id: str,
        contacts: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Update emergency contact information.

        Args:
            employee_id: Employee ID
            contacts: List of contacts with name, phone, relationship

        Returns:
            Updated contact information
        """
        data = {'contacts': contacts}
        return self._request(
            'PUT',
            f'/employees/{employee_id}/contacts',
            data=data
        )

    def get_locations(self, confirmation_id: str) -> List[Dict[str, Any]]:
        """
        Get location data from safety confirmation responses.

        Args:
            confirmation_id: Confirmation ID

        Returns:
            List of location data
        """
        result = self._request(
            'GET',
            f'/confirmations/{confirmation_id}/locations'
        )
        return result.get('locations', [])

    def export_responses(
        self,
        confirmation_id: str,
        format: str = "csv"
    ) -> Dict[str, Any]:
        """
        Export confirmation responses.

        Args:
            confirmation_id: Confirmation ID
            format: Export format (csv, excel)

        Returns:
            Export result with download URL
        """
        params = {'format': format}
        return self._request(
            'GET',
            f'/confirmations/{confirmation_id}/export',
            params=params
        )

    def list_employees(
        self,
        department: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List employees in the organization.

        Args:
            department: Filter by department (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of employees
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if department:
            params['department'] = department

        result = self._request('GET', '/employees', params=params)
        return result.get('employees', [])

    def check_employee_availability(
        self,
        employee_id: str
    ) -> Dict[str, Any]:
        """
        Check if an employee is available for safety confirmations.

        Args:
            employee_id: Employee ID

        Returns:
            Employee availability status
        """
        return self._request('GET', f'/employees/{employee_id}/availability')