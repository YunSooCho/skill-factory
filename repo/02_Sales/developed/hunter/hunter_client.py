"""
Hunter API Client
Email finder and verifier platform for lead management

API Documentation: https://hunter.io/api
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class HunterAPIError(Exception):
    """Custom exception for Hunter API errors"""
    pass


class HunterRateLimitError(HunterAPIError):
    """Rate limit exceeded error"""
    pass


class HunterClient:
    """
    Hunter REST API Client
    Supports email search, verification, and lead management
    """

    def __init__(self, api_key: str, api_url: str = "https://api.hunter.io/v2", timeout: int = 30):
        """
        Initialize Hunter API client

        Args:
            api_key: Hunter.io API key
            api_url: Base URL of Hunter API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests (Free tier: ~10 requests/second)
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                     data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary
        """
        # Rate limiting
        current_time = time.time()

        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            time.sleep(1)

        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        # Add API key to params
        if params is None:
            params = {}
        params['api_key'] = self.api_key

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, params=params, timeout=self.timeout)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, json=data, params=params, timeout=self.timeout)
            else:
                raise HunterAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, params, data)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                errors = error_data.get('errors', [])
                error_msg = errors[0] if errors else error_data.get('message', response.text)
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get('message', str(error_msg))
                raise HunterAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise HunterAPIError(f"Request failed: {str(e)}")

    # ========== EMAIL SEARCH METHODS ==========

    def search_emails_from_domain(self, domain: str, company: Optional[str] = None,
                                  limit: int = 10, offset: int = 0,
                                  email_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for emails associated with a domain

        Args:
            domain: Domain to search (e.g., "stripe.com")
            company: Company name (optional)
            limit: Maximum number of results (max 100)
            offset: Pagination offset
            email_type: Type of emails to return ("personal" or "generic")

        Returns:
            Email search results with data and meta information

        Example response:
        {
            "data": {
                "domain": "stripe.com",
                "webmail": false,
                "pattern": "{first}.{last}",
                "emails": [
                    {
                        "value": "patrick@stripe.com",
                        "type": "personal",
                        "confidence": 92,
                        "sources": [...],
                        ...
                    }
                ]
            }
        }
        """
        params = {
            'domain': domain,
            'limit': min(limit, 100),
            'offset': offset
        }
        if company:
            params['company'] = company
        if email_type:
            params['type'] = email_type

        return self._make_request('GET', '/email-finder', params=params)

    def email_verifier(self, email: str) -> Dict[str, Any]:
        """
        Verify an email address

        Args:
            email: Email address to verify

        Returns:
            Email verification result with status, score, and details

        Example response:
        {
            "data": {
                "email": "test@stripe.com",
                "status": "valid",
                "score": 80,
                "regexp": true,
                "gibberish": false,
                "disposable": false,
                ...
            }
        }
        """
        params = {'email': email}
        return self._make_request('GET', '/email-verifier', params=params)

    # ========== LEAD METHODS ==========

    def create_lead(self, first_name: str, last_name: str, email: str,
                    domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new lead

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            domain: Domain (optional)
            **kwargs: Additional lead fields (company_name, linkedin, etc.)

        Returns:
            Created lead data
        """
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        if domain:
            data['domain'] = domain
        data.update(kwargs)

        return self._make_request('POST', '/leads', data=data)

    def update_lead(self, lead_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a lead

        Args:
            lead_id: Lead ID
            **kwargs: Fields to update

        Returns:
            Updated lead data
        """
        return self._make_request('PATCH', f'/leads/{lead_id}', data=kwargs)

    def search_leads(self, domain: Optional[str] = None, email: Optional[str] = None,
                    limit: int = 20, offset: int = 0, **filters) -> Dict[str, Any]:
        """
        Search leads

        Args:
            domain: Filter by domain
            email: Filter by email
            limit: Maximum results per page
            offset: Pagination offset
            **filters: Additional filters

        Returns:
            List of leads
        """
        params = {
            'limit': min(limit, 100),
            'offset': offset
        }

        if domain:
            params['domain'] = domain
        if email:
            params['email'] = email
        params.update(filters)

        return self._make_request('GET', '/leads', params=params)

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Get lead by ID

        Args:
            lead_id: Lead ID

        Returns:
            Lead data
        """
        return self._make_request('GET', f'/leads/{lead_id}')

    def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Delete lead

        Args:
            lead_id: Lead ID

        Returns:
            Deletion response
        """
        return self._make_request('DELETE', f'/leads/{lead_id}')

    # ========== ADDITIONAL METHODS ==========

    def email_count(self, domain: Optional[str] = None, company: Optional[str] = None,
                   email_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the number of emails for a domain

        Args:
            domain: Domain to check
            company: Company name
            email_type: Type of emails ("personal" or "generic")

        Returns:
            Email count information
        """
        params = {}
        if domain:
            params['domain'] = domain
        if company:
            params['company'] = company
        if email_type:
            params['type'] = email_type

        return self._make_request('GET', '/email-count', params=params)


if __name__ == '__main__':
    import os

    API_KEY = os.getenv('HUNTER_API_KEY', 'your_api_key')

    client = HunterClient(api_key=API_KEY)

    try:
        # Example: Search emails from a domain
        email_result = client.search_emails_from_domain('stripe.com')
        print(f"Emails found: {email_result.get('data', {}).get('emails', [])}")

        # Example: Verify an email
        verification = client.email_verifier('test@stripe.com')
        print(f"Email status: {verification.get('data', {}).get('status')}")
        print(f"Email score: {verification.get('data', {}).get('score')}")

        # Example: Create a lead
        lead = client.create_lead(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            domain='example.com',
            company_name='Example Corp'
        )
        print(f"Created lead: {lead}")

        # Example: Search leads
        leads = client.search_leads(domain='example.com', limit=10)
        print(f"Search leads: {leads}")

        # Example: Update lead
        # updated_lead = client.update_lead(lead_id='123', linkedin='https://linkedin.com/in/johndoe')
        # print(f"Updated lead: {updated_lead}")

    except HunterAPIError as e:
        print(f"Error: {e}")