"""
Fireberry API Client
CRM platform for managing accounts, contacts, deals, and tasks

API Documentation: https://fireberry.com/api
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class FireberryAPIError(Exception):
    """Custom exception for Fireberry API errors"""
    pass


class FireberryRateLimitError(FireberryAPIError):
    """Rate limit exceeded error"""
    pass


class FireberryClient:
    """
    Fireberry REST API Client
    Supports full CRUD operations for CRM entities
    """

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        """
        Initialize Fireberry API client

        Args:
            api_url: Base URL of Fireberry API (e.g., https://api.fireberry.com)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        self.rate_limit_remaining = None
        self.rate_limit_reset = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            FireberryAPIError: For API errors
            FireberryRateLimitError: For rate limit exceeded
        """
        # Rate limiting
        current_time = time.time()

        # Check if we've hit rate limit
        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            if self.rate_limit_reset:
                wait_time = self.rate_limit_reset - current_time
                if wait_time > 0:
                    time.sleep(wait_time)

        # Enforce minimum interval
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise FireberryAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info from headers
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))
            self.rate_limit_reset = float(response.headers.get('X-RateLimit-Reset', '0'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('error', error_data.get('message', response.text))
                raise FireberryAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise FireberryAPIError(f"Request failed: {str(e)}")

    # ========== ACCOUNT METHODS ==========

    def create_account(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new account

        Args:
            name: Account name
            **kwargs: Additional account fields

        Returns:
            Created account data
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/accounts', data=data)

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get account by ID"""
        return self._make_request('GET', f'/accounts/{account_id}')

    def update_account(self, account_id: str, **kwargs) -> Dict[str, Any]:
        """Update account"""
        return self._make_request('PUT', f'/accounts/{account_id}', data=kwargs)

    def delete_account(self, account_id: str) -> Dict[str, Any]:
        """Delete account"""
        return self._make_request('DELETE', f'/accounts/{account_id}')

    def search_accounts(self, query: Optional[str] = None, filter_dict: Optional[Dict] = None,
                       limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Search accounts

        Args:
            query: Search query string
            filter_dict: Filter conditions
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of accounts
        """
        params = {'limit': limit, 'offset': offset}
        if query:
            params['q'] = query
        if filter_dict:
            params.update(filter_dict)

        return self._make_request('GET', '/accounts', params=params)

    # ========== CONTACT METHODS ==========

    def create_contact(self, first_name: str, last_name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            first_name: First name
            last_name: Last name
            **kwargs: Additional contact fields (email, phone, account_id, etc.)

        Returns:
            Created contact data
        """
        data = {'first_name': first_name, 'last_name': last_name, **kwargs}
        return self._make_request('POST', '/contacts', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact by ID"""
        return self._make_request('GET', f'/contacts/{contact_id}')

    def update_contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        """Update contact"""
        return self._make_request('PUT', f'/contacts/{contact_id}', data=kwargs)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        return self._make_request('DELETE', f'/contacts/{contact_id}')

    def search_contacts(self, query: Optional[str] = None, filter_dict: Optional[Dict] = None,
                       limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Search contacts

        Args:
            query: Search query string
            filter_dict: Filter conditions
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of contacts
        """
        params = {'limit': limit, 'offset': offset}
        if query:
            params['q'] = query
        if filter_dict:
            params.update(filter_dict)

        return self._make_request('GET', '/contacts', params=params)

    # ========== DEAL METHODS ==========

    def create_deal(self, name: str, value: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new deal

        Args:
            name: Deal name
            value: Deal value
            **kwargs: Additional deal fields (stage, account_id, close_date, etc.)

        Returns:
            Created deal data
        """
        data = {'name': name, 'value': value, **kwargs}
        return self._make_request('POST', '/deals', data=data)

    def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """Get deal by ID"""
        return self._make_request('GET', f'/deals/{deal_id}')

    def update_deal(self, deal_id: str, **kwargs) -> Dict[str, Any]:
        """Update deal"""
        return self._make_request('PUT', f'/deals/{deal_id}', data=kwargs)

    def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """Delete deal"""
        return self._make_request('DELETE', f'/deals/{deal_id}')

    def search_deals(self, query: Optional[str] = None, filter_dict: Optional[Dict] = None,
                    limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Search deals

        Args:
            query: Search query string
            filter_dict: Filter conditions
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of deals
        """
        params = {'limit': limit, 'offset': offset}
        if query:
            params['q'] = query
        if filter_dict:
            params.update(filter_dict)

        return self._make_request('GET', '/deals', params=params)

    # ========== TASK METHODS ==========

    def create_task(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new task

        Args:
            name: Task name
            **kwargs: Additional task fields (status, priority, due_date, etc.)

        Returns:
            Created task data
        """
        data = {'name': name, **kwargs}
        return self._make_request('POST', '/tasks', data=data)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task by ID"""
        return self._make_request('GET', f'/tasks/{task_id}')

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task"""
        return self._make_request('PUT', f'/tasks/{task_id}', data=kwargs)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete task"""
        return self._make_request('DELETE', f'/tasks/{task_id}')

    def search_tasks(self, query: Optional[str] = None, filter_dict: Optional[Dict] = None,
                    limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Search tasks

        Args:
            query: Search query string
            filter_dict: Filter conditions
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of tasks
        """
        params = {'limit': limit, 'offset': offset}
        if query:
            params['q'] = query
        if filter_dict:
            params.update(filter_dict)

        return self._make_request('GET', '/tasks', params=params)


if __name__ == '__main__':
    # Example usage
    import os

    API_URL = os.getenv('FIREBERRY_API_URL', 'https://api.fireberry.com')
    API_KEY = os.getenv('FIREBERRY_API_KEY', 'your_api_key')

    client = FireberryClient(api_url=API_URL, api_key=API_KEY)

    try:
        # Example: Create an account
        account = client.create_account(
            name="Example Company",
            website="https://example.com"
        )
        print(f"Created account: {account}")

        # Example: Create a contact
        contact = client.create_contact(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com"
        )
        print(f"Created contact: {contact}")

        # Example: Create a deal
        deal = client.create_deal(
            name="Big Deal",
            value="100000",
            stage="Negotiation"
        )
        print(f"Created deal: {deal}")

    except FireberryAPIError as e:
        print(f"Error: {e}")