"""
Reverse Contact API Client Implementation

Provides methods for:
- Email Lookup: Find person and company information by email
- Domain Lookup: Get company information by domain
- Get LinkedIn Profile: Retrieve LinkedIn profile details
- Get LinkedIn Company: Retrieve LinkedIn company details
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Rate limiter for API requests"""
    max_requests: int = 100  # Maximum requests per time window
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


class ReverseContactError(Exception):
    """Base exception for Reverse Contact API errors"""
    pass


class AuthenticationError(ReverseContactError):
    """Raised when authentication fails"""
    pass


class RateLimitError(ReverseContactError):
    """Raised when rate limit is exceeded"""
    pass


class InvalidRequestError(ReverseContactError):
    """Raised when request parameters are invalid"""
    pass


class APIError(ReverseContactError):
    """Raised for general API errors"""
    pass


class ReverseContactClient:
    """
    Reverse Contact API Client

    API for reverse email lookup, domain search, and LinkedIn profile enrichment.
    """

    BASE_URL = "https://www.reversecontact.com/api"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Reverse Contact client

        Args:
            api_key: Your Reverse Contact API key
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
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
        Make HTTP request to Reverse Contact API

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

    def email_lookup(self, email: str) -> Dict[str, Any]:
        """
        Lookup person and company information by email address

        Args:
            email: Email address to lookup

        Returns:
            Dictionary containing:
                - person: Personal information (name, job title, location, LinkedIn URL)
                - company: Company information (name, website, industry, description)
                - social_media: Social media profiles
                - status: Lookup status ('found' or 'not_found')

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If email is invalid
            APIError: For other API errors

        Example:
            >>> client = ReverseContactClient(api_key="your-api-key")
            >>> result = client.email_lookup("john@example.com")
            >>> print(result['person']['name'])
        """
        if not email or '@' not in email:
            raise InvalidRequestError("Invalid email address")

        params = {"email": email}

        return self._make_request("GET", "/v1/lookup", params=params)

    def domain_lookup(self, domain: str) -> Dict[str, Any]:
        """
        Lookup company information by domain name

        Args:
            domain: Domain name (e.g., "example.com")

        Returns:
            Dictionary containing:
                - company: Company details (name, description, industry, location)
                - employees: Employee statistics
                - linkedin: LinkedIn company information (URL, company ID)
                - website: Website details
                - social_media: Social media profiles
                - status: Lookup status ('found' or 'not_found')

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If domain is invalid
            APIError: For other API errors

        Example:
            >>> client = ReverseContactClient(api_key="your-api-key")
            >>> result = client.domain_lookup("example.com")
            >>> print(result['company']['name'])
        """
        if not domain:
            raise InvalidRequestError("Domain is required")

        # Clean up domain
        domain = domain.strip().lower()
        if domain.startswith(('http://', 'https://', 'www.')):
            import re
            domain = re.sub(r'^https?://(www\.)?', '', domain)

        params = {"domain": domain}

        return self._make_request("GET", "/v1/domain", params=params)

    def get_linkedin_profile(self, email: str) -> Dict[str, Any]:
        """
        Get LinkedIn profile information for an email address

        Args:
            email: Email address to find LinkedIn profile for

        Returns:
            Dictionary containing:
                - profile_url: LinkedIn profile URL
                - profile_id: LinkedIn profile ID
                - name: Full name
                - headline: Professional headline/job title
                - location: Location
                - profile_picture: Profile picture URL
                - followers: Number of followers
                - employment: Employment history
                - education: Education history
                - skills: List of skills
                - status: Lookup status ('found' or 'not_found')

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If email is invalid
            APIError: For other API errors

        Example:
            >>> client = ReverseContactClient(api_key="your-api-key")
            >>> result = client.get_linkedin_profile("john@example.com")
            >>> print(result['profile_url'])
        """
        if not email or '@' not in email:
            raise InvalidRequestError("Invalid email address")

        params = {"email": email}

        return self._make_request("GET", "/v1/linkedin/profile", params=params)

    def get_linkedin_company(self, domain: str) -> Dict[str, Any]:
        """
        Get LinkedIn company information for a domain

        Args:
            domain: Domain name (e.g., "example.com")

        Returns:
            Dictionary containing:
                - company_url: LinkedIn company page URL
                - company_id: LinkedIn company ID
                - name: Company name
                - description: Company description
                - industry: Industry
                - size: Company size (employee count)
                - headquarters: Headquarters location
                - founded: Year founded
                - specialties: List of specialties
                - followers: Number of followers
                - logo: Company logo URL
                - status: Lookup status ('found' or 'not_found')

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If domain is invalid
            APIError: For other API errors

        Example:
            >>> client = ReverseContactClient(api_key="your-api-key")
            >>> result = client.get_linkedin_company("example.com")
            >>> print(result['company_url'])
        """
        if not domain:
            raise InvalidRequestError("Domain is required")

        # Clean up domain
        domain = domain.strip().lower()
        if domain.startswith(('http://', 'https://', 'www.')):
            import re
            domain = re.sub(r'^https?://(www\.)?', '', domain)

        params = {"domain": domain}

        return self._make_request("GET", "/v1/linkedin/company", params=params)

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()