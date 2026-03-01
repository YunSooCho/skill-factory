"""
RocketReach API Client Implementation

Provides methods for:
- Lookup Person: Find person information by email/name
- Lookup Company: Find company information
- Bulk People Lookup: Lookup multiple people at once
"""

import requests
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Rate limiter for API requests"""
    max_requests: int = 200  # Maximum requests per time window
    time_window: int = 60  # Time window in seconds
    requests: list = None

    def __post_init__(self):
        if self.requests is None:
            self.requests = []

    def wait_if_needed(self):
        """Wait if rate limit has been reached"""
        now = time.time()
        # Remove requests outside the time window
        self.requests = [r for r in self.requests if now - r < self.time_window]

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                # Clean up old requests after waiting
                self.requests = []

        # Add current request
        self.requests.append(now)


class RocketReachError(Exception):
    """Base exception for RocketReach API errors"""
    pass


class AuthenticationError(RocketReachError):
    """Raised when authentication fails"""
    pass


class RateLimitError(RocketReachError):
    """Raised when rate limit is exceeded"""
    pass


class InsufficientCreditsError(RocketReachError):
    """Raised when API credits are insufficient"""
    pass


class InvalidRequestError(RocketReachError):
    """Raised when request parameters are invalid"""
    pass


class APIError(RocketReachError):
    """Raised for general API errors"""
    pass


class RocketReachClient:
    """
    RocketReach API Client

    API for people and company lookup, contact enrichment.
    """

    BASE_URL = "https://api.rocketreach.co/api/v2"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize RocketReach client

        Args:
            api_key: Your RocketReach API key
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=200, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Api-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to RocketReach API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            InsufficientCreditsError: If API credits are insufficient
            InvalidRequestError: If request parameters are invalid
            APIError: For other API errors
        """
        self.rate_limiter.wait_if_needed()

        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )

                # Handle specific status codes
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")
                elif response.status_code == 403:
                    error_data = response.json() if response.content else {}
                    if 'credit' in str(error_data).lower():
                        raise InsufficientCreditsError("Insufficient API credits")
                    raise AuthenticationError("Access forbidden")
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise InvalidRequestError(f"Invalid request: {error_data.get('message', 'Unknown error')}")
                elif response.status_code == 404:
                    raise InvalidRequestError("Resource not found")
                elif response.status_code >= 500:
                    error_data = response.json() if response.content else {}
                    raise APIError(f"Server error: {error_data.get('message', 'Unknown error')}")

                response.raise_for_status()

                return response.json()

            except requests.Timeout:
                last_error = f"Request timeout after {self.timeout} seconds"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise APIError(last_error)

            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise APIError(f"Request failed: {last_error}")

        raise APIError(f"Max retries exceeded: {last_error}")

    def lookup_person(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        linkedin_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lookup person information

        Needs at least one of: email, name, or linkedin_url

        Args:
            email: Email address to lookup
            name: Full name (first and last name)
            linkedin_url: LinkedIn profile URL

        Returns:
            Dictionary containing person information:
                - id: Person ID
                - name: Full name
                - email: Email address
                - linkedin: LinkedIn profile URL
                - title: Job title
                - company: Current company
                - location: Location
                - phones: Phone numbers
                - social_media: Other social media profiles
                - status: Lookup status

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If parameters are invalid
            APIError: For other API errors

        Example:
            >>> client = RocketReachClient(api_key="your-api-key")
            >>> result = client.lookup_person(email="john@example.com")
            >>> print(result['name'])
        """
        if not any([email, name, linkedin_url]):
            raise InvalidRequestError("At least one of email, name, or linkedin_url is required")

        params = {}
        if email:
            params['email'] = email
        if name:
            params['name'] = name
        if linkedin_url:
            params['linkedin_url'] = linkedin_url

        return self._make_request("GET", "/person/lookup", params=params)

    def lookup_company(
        self,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        linkedin_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lookup company information

        Needs at least one of: name, domain, or linkedin_url

        Args:
            name: Company name
            domain: Company domain (e.g., "example.com")
            linkedin_url: LinkedIn company page URL

        Returns:
            Dictionary containing company information:
                - id: Company ID
                - name: Company name
                - domain: Company domain
                - website: Website URL
                - linkedin: LinkedIn company URL
                - location: Location
                - size: Company size (employee count)
                - industry: Industry
                - description: Company description
                - founded: Year founded
                - status: Lookup status

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If parameters are invalid
            APIError: For other API errors

        Example:
            >>> client = RocketReachClient(api_key="your-api-key")
            >>> result = client.lookup_company(domain="example.com")
            >>> print(result['name'])
        """
        if not any([name, domain, linkedin_url]):
            raise InvalidRequestError("At least one of name, domain, or linkedin_url is required")

        params = {}
        if name:
            params['name'] = name
        if domain:
            params['domain'] = domain
        if linkedin_url:
            params['linkedin_url'] = linkedin_url

        return self._make_request("GET", "/company/lookup/", params=params)

    def bulk_people_lookup(
        self,
        queries: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Bulk lookup multiple people at once

        Args:
            queries: List of lookup queries. Each query should contain
                     at least one of: email, name, or linkedin_url

        Returns:
            Dictionary containing:
                - request_id: Bulk lookup request ID
                - status: Status of the bulk request
                - results: List of person information
                - failed: List of failed lookups

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If parameters are invalid
            InsufficientCreditsError: If API credits are insufficient
            APIError: For other API errors

        Example:
            >>> client = RocketReachClient(api_key="your-api-key")
            >>> queries = [
            ...     {"email": "john@example.com"},
            ...     {"email": "jane@example.com"}
            ... ]
            >>> result = client.bulk_people_lookup(queries)
            >>> for person in result['results']:
            ...     print(person['name'])
        """
        if not queries or not isinstance(queries, list):
            raise InvalidRequestError("queries must be a non-empty list")

        if len(queries) > 100:
            raise InvalidRequestError("Maximum 100 queries per bulk request")

        # Validate each query
        for i, query in enumerate(queries):
            if not isinstance(query, dict):
                raise InvalidRequestError(f"Query at index {i} must be a dictionary")
            if not any([query.get('email'), query.get('name'), query.get('linkedin_url')]):
                raise InvalidRequestError(
                    f"Query at index {i} must contain at least one of: email, name, linkedin_url"
                )

        data = {"requests": queries}

        return self._make_request("POST", "/bulkLookup", data=data)

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()