"""
Freshsales API Client
CRM platform for managing contacts, accounts, deals, and tasks

API Documentation: https://developers.freshworks.com/crm/api/
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class FreshsalesAPIError(Exception):
    """Custom exception for Freshsales API errors"""
    pass


class FreshsalesRateLimitError(FreshsalesAPIError):
    """Rate limit exceeded error"""
    pass


class FreshsalesClient:
    """
    Freshsales REST API Client
    Supports full CRUD operations and file uploads for CRM entities
    """

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        """
        Initialize Freshsales API client

        Args:
            api_url: Base URL of your Freshsales domain (e.g., https://domain.myfreshworks.com)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Token token={api_key}'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests (Freshsales recommends 10 req/sec)
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            files: Files to upload

        Returns:
            Response data as dictionary
        """
        # Rate limiting
        current_time = time.time()

        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            time.sleep(1)  # Wait briefly

        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                if files:
                    headers = {'Authorization': self.session.headers['Authorization']}
                    response = requests.post(url, data=data, files=files, headers=headers, timeout=self.timeout)
                else:
                    response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise FreshsalesAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                if response.headers.get('X-RateLimit-Reset'):
                    wait_until = int(response.headers['X-RateLimit-Reset'])
                    wait_time = min(wait_until - current_time, 60)
                    time.sleep(wait_time)
                else:
                    time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('errors', error_data.get('message', response.text))
                raise FreshsalesAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise FreshsalesAPIError(f"Request failed: {str(e)}")

    # ========== CONTACT METHODS ==========

    def create_contact(self, first_name: Optional[str] = None, last_name: Optional[str] = None,
                      email: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            **kwargs: Additional contact fields

        Returns:
            Created contact data
        """
        contact_data = {}
        if first_name:
            contact_data['first_name'] = first_name
        if last_name:
            contact_data['last_name'] = last_name
        if email:
            contact_data['email'] = email
        contact_data.update(kwargs)

        return self._make_request('POST', '/api/contacts', data={'contact': contact_data})

    def get_contact(self, contact_id: str, include: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get contact by ID

        Args:
            contact_id: Contact ID
            include: Include related data (e.g., ['company', 'deals'])

        Returns:
            Contact data
        """
        params = {}
        if include:
            params['include'] = ','.join(include)

        return self._make_request('GET', f'/api/contacts/{contact_id}', params=params)

    def update_contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        """Update contact"""
        return self._make_request('PUT', f'/api/contacts/{contact_id}', data={'contact': kwargs})

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        return self._make_request('DELETE', f'/api/contacts/{contact_id}')

    def search_contacts(self, query: Optional[str] = None, filter_params: Optional[Dict] = None,
                       page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        Search contacts

        Args:
            query: Search query
            filter_params: Filter conditions
            page: Page number
            per_page: Results per page

        Returns:
            List of contacts
        """
        params = {'page': page, 'per_page': per_page}
        if query:
            params['q'] = query
        if filter_params:
            params.update(filter_params)

        return self._make_request('GET', '/api/contacts', params=params)

    # ========== COMPANY/ACCOUNT METHODS ==========

    def create_account(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new account/company

        Args:
            name: Company name
            **kwargs: Additional company fields

        Returns:
            Created account data
        """
        return self._make_request('POST', '/api/sales_accounts', data={'sales_account': {'name': name, **kwargs}})

    def get_account(self, account_id: str, include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get account by ID"""
        params = {}
        if include:
            params['include'] = ','.join(include)

        return self._make_request('GET', f'/api/sales_accounts/{account_id}', params=params)

    def update_account(self, account_id: str, **kwargs) -> Dict[str, Any]:
        """Update account"""
        return self._make_request('PUT', f'/api/sales_accounts/{account_id}', data={'sales_account': kwargs})

    def search_accounts(self, query: Optional[str] = None, filter_params: Optional[Dict] = None,
                       page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Search accounts"""
        params = {'page': page, 'per_page': per_page}
        if query:
            params['q'] = query
        if filter_params:
            params.update(filter_params)

        return self._make_request('GET', '/api/sales_accounts', params=params)

    # ========== DEAL METHODS ==========

    def create_deal(self, amount: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new deal

        Args:
            amount: Deal amount
            **kwargs: Additional deal fields (name, stage, deal_owner_id, etc.)

        Returns:
            Created deal data
        """
        deal_data = {'amount': amount, **kwargs}
        return self._make_request('POST', '/api/deals', data={'deal': deal_data})

    def update_deal(self, deal_id: str, **kwargs) -> Dict[str, Any]:
        """Update deal"""
        return self._make_request('PUT', f'/api/deals/{deal_id}', data={'deal': kwargs})

    def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """Delete deal"""
        return self._make_request('DELETE', f'/api/deals/{deal_id}')

    def get_deal(self, deal_id: str, include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get deal by ID"""
        params = {}
        if include:
            params['include'] = ','.join(include)

        return self._make_request('GET', f'/api/deals/{deal_id}', params=params)

    # ========== TASK METHODS ==========

    def create_task(self, title: str, **kwargs) -> Dict[str, Any]:
        """Create a new task"""
        return self._make_request('POST', '/api/tasks', data={'task': {'title': title, **kwargs}})

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task by ID"""
        return self._make_request('GET', f'/api/tasks/{task_id}')

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task"""
        return self._make_request('PUT', f'/api/tasks/{task_id}', data={'task': kwargs})

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete task"""
        return self._make_request('DELETE', f'/api/tasks/{task_id}')

    # ========== NOTE METHODS ==========

    def create_note(self, description: str, targetable_type: str, targetable_id: str,
                    **kwargs) -> Dict[str, Any]:
        """
        Create a new note

        Args:
            description: Note content
            targetable_type: Type of entity (e.g., 'Contact', 'Deal')
            targetable_id: ID of the entity
            **kwargs: Additional note fields

        Returns:
            Created note data
        """
        note_data = {
            'description': description,
            'targetable_type': targetable_type,
            'targetable_id': targetable_id,
            **kwargs
        }
        return self._make_request('POST', '/api/notes', data={'note': note_data})

    # ========== FILE UPLOAD METHODS ==========

    def upload_file(self, file_path: str, targetable_type: str, targetable_id: str) -> Dict[str, Any]:
        """
        Upload a file

        Args:
            file_path: Path to the file to upload
            targetable_type: Type of entity (e.g., 'Contact', 'Deal')
            targetable_id: ID of the entity

        Returns:
            Uploaded file data
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'targetable_type': targetable_type,
                'targetable_id': targetable_id
            }
            return self._make_request('POST', '/api/files', data=data, files=files)

    # ========== SEARCH/VIEW METHODS ==========

    def search_entities(self, query: str, filters: Optional[Dict] = None,
                       page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        Search across multiple entity types

        Args:
            query: Search query
            filters: Filter conditions
            page: Page number
            per_page: Results per page

        Returns:
            Search results from multiple entity types
        """
        params = {'q': query, 'page': page, 'per_page': per_page}
        if filters:
            params.update(filters)

        return self._make_request('GET', '/api/search', params=params)


if __name__ == '__main__':
    import os

    API_URL = os.getenv('FRESHSALES_API_URL', 'https://your-domain.myfreshworks.com')
    API_KEY = os.getenv('FRESHSALES_API_KEY', 'your_api_key')

    client = FreshsalesClient(api_url=API_URL, api_key=API_KEY)

    try:
        # Example: Create a contact
        contact = client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        print(f"Created contact: {contact}")

        # Example: Create a deal
        deal = client.create_deal(
            amount="50000",
            name="New Opportunity",
            stage="Qualification"
        )
        print(f"Created deal: {deal}")

        # Example: Create a task
        task = client.create_task(
            title="Follow up with customer",
            due_date="2025-03-01"
        )
        print(f"Created task: {task}")

        # Example: Upload a file
        # file_result = client.upload_file(
        #     file_path="/path/to/file.pdf",
        #     targetable_type="Contact",
        #     targetable_id=contact['contact']['id']
        # )
        # print(f"Uploaded file: {file_result}")

    except FreshsalesAPIError as e:
        print(f"Error: {e}")