"""
EspoCRM API Client
Full-featured CRM with accounts, contacts, leads, tasks, and opportunities

API Documentation: https://docs.espocrm.com/development/rest-api/
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class EspoCRMAPIError(Exception):
    """Custom exception for EspoCRM API errors"""
    pass


class EspoCRMRateLimitError(EspoCRMAPIError):
    """Rate limit exceeded error"""
    pass


class EspoCRMClient:
    """
    EspoCRM REST API Client
    Supports full CRUD operations for CRM entities
    """

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        """
        Initialize EspoCRM API client

        Args:
            api_url: Base URL of EspoCRM instance (e.g., https://crm.example.com)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests for rate limiting

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (e.g., /Account)
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            EspoCRMAPIError: For API errors
            EspoCRMRateLimitError: For rate limit exceeded
        """
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.api_url}/api/v1{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise EspoCRMAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('message', response.text)
                raise EspoCRMAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise EspoCRMAPIError(f"Request failed: {str(e)}")

    # ========== ACCOUNT METHODS ==========

    def create_account(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new account

        Args:
            name: Account name
            **kwargs: Additional account fields (billingAddress, shippingAddress, etc.)

        Returns:
            Created account data
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/Account', data=data)

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get account by ID

        Args:
            account_id: Account ID

        Returns:
            Account data
        """
        return self._make_request('GET', f'/Account/{account_id}')

    def update_account(self, account_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update account

        Args:
            account_id: Account ID
            **kwargs: Fields to update

        Returns:
            Updated account data
        """
        return self._make_request('PUT', f'/Account/{account_id}', data=kwargs)

    def delete_account(self, account_id: str) -> Dict[str, Any]:
        """
        Delete account

        Args:
            account_id: Account ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/Account/{account_id}')

    def list_accounts(self, select: Optional[str] = None, where: Optional[List] = None,
                     offset: int = 0, max_size: int = 20) -> Dict[str, Any]:
        """
        List accounts with filtering and pagination

        Args:
            select: Comma-separated fields to select
            where: Filter conditions (EspoCRM format)
            offset: Pagination offset
            max_size: Maximum results per page

        Returns:
            List of accounts
        """
        params = {'offset': offset, 'maxSize': max_size}
        if select:
            params['select'] = select
        if where:
            params['where'] = str(where)

        return self._make_request('GET', '/Account', params=params)

    # ========== CONTACT METHODS ==========

    def create_contact(self, first_name: str, last_name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            first_name: First name
            last_name: Last name
            **kwargs: Additional contact fields (email, phone, accountId, etc.)

        Returns:
            Created contact data
        """
        data = {'firstName': first_name, 'lastName': last_name, **kwargs}
        return self._make_request('POST', '/Contact', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact by ID

        Args:
            contact_id: Contact ID

        Returns:
            Contact data
        """
        return self._make_request('GET', f'/Contact/{contact_id}')

    def update_contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update contact

        Args:
            contact_id: Contact ID
            **kwargs: Fields to update

        Returns:
            Updated contact data
        """
        return self._make_request('PUT', f'/Contact/{contact_id}', data=kwargs)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete contact

        Args:
            contact_id: Contact ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/Contact/{contact_id}')

    def list_contacts(self, select: Optional[str] = None, where: Optional[List] = None,
                     offset: int = 0, max_size: int = 20) -> Dict[str, Any]:
        """
        List contacts with filtering and pagination

        Args:
            select: Comma-separated fields to select
            where: Filter conditions
            offset: Pagination offset
            max_size: Maximum results per page

        Returns:
            List of contacts
        """
        params = {'offset': offset, 'maxSize': max_size}
        if select:
            params['select'] = select
        if where:
            params['where'] = str(where)

        return self._make_request('GET', '/Contact', params=params)

    # ========== LEAD METHODS ==========

    def create_lead(self, last_name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new lead

        Args:
            last_name: Last name (required)
            **kwargs: Additional lead fields (firstName, status, source, etc.)

        Returns:
            Created lead data
        """
        data = {'lastName': last_name, **kwargs}
        return self._make_request('POST', '/Lead', data=data)

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Get lead by ID

        Args:
            lead_id: Lead ID

        Returns:
            Lead data
        """
        return self._make_request('GET', f'/Lead/{lead_id}')

    def update_lead(self, lead_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update lead

        Args:
            lead_id: Lead ID
            **kwargs: Fields to update

        Returns:
            Updated lead data
        """
        return self._make_request('PUT', f'/Lead/{lead_id}', data=kwargs)

    def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Delete lead

        Args:
            lead_id: Lead ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/Lead/{lead_id}')

    def list_leads(self, select: Optional[str] = None, where: Optional[List] = None,
                  offset: int = 0, max_size: int = 20) -> Dict[str, Any]:
        """
        List leads with filtering and pagination

        Args:
            select: Comma-separated fields to select
            where: Filter conditions
            offset: Pagination offset
            max_size: Maximum results per page

        Returns:
            List of leads
        """
        params = {'offset': offset, 'maxSize': max_size}
        if select:
            params['select'] = select
        if where:
            params['where'] = str(where)

        return self._make_request('GET', '/Lead', params=params)

    # ========== OPPORTUNITY METHODS ==========

    def create_opportunity(self, name: str, amount: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new opportunity

        Args:
            name: Opportunity name
            amount: Opportunity amount
            **kwargs: Additional opportunity fields (stage, accountId, closeDate, etc.)

        Returns:
            Created opportunity data
        """
        data = {'name': name, 'amount': amount, **kwargs}
        return self._make_request('POST', '/Opportunity', data=data)

    def get_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """
        Get opportunity by ID

        Args:
            opportunity_id: Opportunity ID

        Returns:
            Opportunity data
        """
        return self._make_request('GET', f'/Opportunity/{opportunity_id}')

    def update_opportunity(self, opportunity_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update opportunity

        Args:
            opportunity_id: Opportunity ID
            **kwargs: Fields to update

        Returns:
            Updated opportunity data
        """
        return self._make_request('PUT', f'/Opportunity/{opportunity_id}', data=kwargs)

    def delete_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """
        Delete opportunity

        Args:
            opportunity_id: Opportunity ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/Opportunity/{opportunity_id}')

    def list_opportunities(self, select: Optional[str] = None, where: Optional[List] = None,
                         offset: int = 0, max_size: int = 20) -> Dict[str, Any]:
        """
        List opportunities with filtering and pagination

        Args:
            select: Comma-separated fields to select
            where: Filter conditions
            offset: Pagination offset
            max_size: Maximum results per page

        Returns:
            List of opportunities
        """
        params = {'offset': offset, 'maxSize': max_size}
        if select:
            params['select'] = select
        if where:
            params['where'] = str(where)

        return self._make_request('GET', '/Opportunity', params=params)

    # ========== TASK METHODS ==========

    def create_task(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new task

        Args:
            name: Task name
            **kwargs: Additional task fields (status, priority, dueDate, assignedUserId, etc.)

        Returns:
            Created task data
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/Task', data=data)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get task by ID

        Args:
            task_id: Task ID

        Returns:
            Task data
        """
        return self._make_request('GET', f'/Task/{task_id}')

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update task

        Args:
            task_id: Task ID
            **kwargs: Fields to update

        Returns:
            Updated task data
        """
        return self._make_request('PUT', f'/Task/{task_id}', data=kwargs)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete task

        Args:
            task_id: Task ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/Task/{task_id}')

    def list_tasks(self, select: Optional[str] = None, where: Optional[List] = None,
                  offset: int = 0, max_size: int = 20) -> Dict[str, Any]:
        """
        List tasks with filtering and pagination

        Args:
            select: Comma-separated fields to select
            where: Filter conditions
            offset: Pagination offset
            max_size: Maximum results per page

        Returns:
            List of tasks
        """
        params = {'offset': offset, 'maxSize': max_size}
        if select:
            params['select'] = select
        if where:
            params['where'] = str(where)

        return self._make_request('GET', '/Task', params=params)


if __name__ == '__main__':
    # Example usage
    import os

    # Get configuration from environment
    API_URL = os.getenv('ESPO_CRM_API_URL', 'https://your-espocrm-instance.com')
    API_KEY = os.getenv('ESPO_CRM_API_KEY', 'your_api_key')

    client = EspoCRMClient(api_url=API_URL, api_key=API_KEY)

    try:
        # Example: Create an account
        account = client.create_account(
            name="Example Corporation",
            website="https://example.com"
        )
        print(f"Created account: {account}")

        # Example: Create a contact
        contact = client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        print(f"Created contact: {contact}")

        # Example: Create an opportunity
        opportunity = client.create_opportunity(
            name="New Deal",
            amount="50000",
            stage="Prospecting"
        )
        print(f"Created opportunity: {opportunity}")

    except EspoCRMAPIError as e:
        print(f"Error: {e}")