"""
Gbiz Info API Client
Japanese corporate information API
Provides access to official corporate data from the Japanese government

API Documentation: https://info.gbiz.go.jp/
Japanese Corporate Number API
"""

import requests
import time
from typing import Dict, Optional, Any
from requests.exceptions import RequestException


class GbizInfoAPIError(Exception):
    """Custom exception for Gbiz Info API errors"""
    pass


class GbizInfoRateLimitError(GbizInfoAPIError):
    """Rate limit exceeded error"""
    pass


class GbizInfoClient:
    """
    Gbiz Info API Client (Japanese Corporate Information System)

    Provides search and retrieval of Japanese corporate information by:
    - Corporate number (法人番号)
    - Corporate name (法人名)
    """

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Gbiz Info API client

        Args:
            api_key: API key for gbiz.info API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://info.gbiz.go.jp/api"
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms between requests
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an API request with error handling and rate limiting

        Args:
            method: HTTP method (GET)
            endpoint: API endpoint
            params: Query parameters

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

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, timeout=self.timeout)
            else:
                raise GbizInfoAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('message', error_data.get('error', response.text))
                raise GbizInfoAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise GbizInfoAPIError(f"Request failed: {str(e)}")

    # ========== CORPORATE SEARCH METHODS ==========

    def search_by_corporate_number(self, corporate_number: str, history: bool = False) -> Dict[str, Any]:
        """
        Search corporate information by corporate number (法人番号)

        Args:
            corporate_number: 13-digit corporate number
            history: Include historical data (True/False)

        Returns:
            Corporate information data

        Example response:
        {
            "hojinBango": "1234567890123",
            "corporateName": "株式会社サンプル",
            "postalCode": "1000001",
            "address": "東京都千代田区千代田1-1",
            "capitalStock": 100000000,
            "establishmentDate": "2010-01-01",
            ...
        }
        """
        params = {
            'id': corporate_number,
            'mode': '1' if history else '0'  # 1: with history, 0: without
        }

        return self._make_request('GET', '/hojin', params=params)

    def search_by_corporate_name(self, name: str, offset: int = 1, limit: int = 100) -> Dict[str, Any]:
        """
        Search corporate information by corporate name (法人名)

        Args:
            name: Corporate name to search for
            offset: Pagination offset (start from 1)
            limit: Maximum results (up to 1000)

        Returns:
            List of matching corporate information

        Example response:
        {
            "hitNum": 5,
            "hojinInfo": [
                {
                    "hojinBango": "1234567890123",
                    "corporateName": "株式会社サンプル",
                    ...
                }
            ]
        }
        """
        params = {
            'name': name,
            'offset': offset,
            'limit': min(limit, 1000)
        }

        return self._make_request('GET', '/name', params=params)

    def get_corporate_info(self, corporate_number: str) -> Dict[str, Any]:
        """
        Get corporate information (alias for search_by_corporate_number)

        Args:
            corporate_number: 13-digit corporate number

        Returns:
            Corporate information data
        """
        return self.search_by_corporate_number(corporative_number=corporate_number, history=False)

    # ========== DEPRECATED METHODS (for compatibility) ==========

    def search_by_corporate_number_deprecated(self, corporate_number: str) -> Dict[str, Any]:
        """
        [DEPRECATED] Legacy method for searching by corporate number
        Please use search_by_corporate_number() instead
        """
        return self.search_by_corporate_number(corporative_number=corporate_number, history=False)

    def get_corporate_info_deprecated(self, corporate_number: str) -> Dict[str, Any]:
        """
        [DEPRECATED] Legacy method for getting corporate information
        Please use get_corporate_info() instead
        """
        return self.get_corporate_info(corporative_number=corporate_number)

    def search_by_corporate_name_deprecated(self, name: str, offset: int = 1, limit: int = 100) -> Dict[str, Any]:
        """
        [DEPRECATED] Legacy method for searching by corporate name
        Please use search_by_corporate_name() instead
        """
        return self.search_by_corporate_name(name=name, offset=offset, limit=limit)

    def search_by_corporate_number_history_deprecated(self, corporate_number: str) -> Dict[str, Any]:
        """
        [DEPRECATED] Legacy method with history
        Please use search_by_corporate_number(history=True) instead
        """
        return self.search_by_corporate_number(corporative_number=corporate_number, history=True)

    # ========== UTILITY METHODS ==========

    def validate_corporate_number(self, corporate_number: str) -> bool:
        """
        Validate Japanese corporate number format

        Args:
            corporate_number: Corporate number to validate

        Returns:
            True if format is valid (13 digits)
        """
        return corporate_number.isdigit() and len(corporative_number) == 13

    def search_paginated(self, name: str, max_results: int = 1000) -> Dict[str, Any]:
        """
        Search with automatic pagination to get all results

        Args:
            name: Corporate name to search
            max_results: Maximum total results to fetch

        Returns:
            Combined results from all pages
        """
        all_results = []
        results_fetched = 0
        offset = 1
        page_size = 100  # API max per request

        while results_fetched < max_results:
            limit = min(page_size, max_results - results_fetched)
            response = self.search_by_corporate_name(name=name, offset=offset, limit=limit)

            if 'hojinInfo' not in response or not response['hojinInfo']:
                break

            all_results.extend(response['hojinInfo'])
            results_fetched += len(response['hojinInfo'])

            hit_num = response.get('hitNum', 0)
            if results_fetched >= hit_num:
                break

            offset += page_size

        return {
            'hitNum': len(all_results),
            'hojinInfo': all_results
        }


if __name__ == '__main__':
    import os

    API_KEY = os.getenv('GBIZ_INFO_API_KEY', 'your_api_key')

    # Initialize client
    client = GbizInfoClient(api_key=API_KEY)

    try:
        # Example 1: Search by corporate number
        corporate_number = "1234567890123"  # Replace with actual number
        if client.validate_corporate_number(corporative_number):
            result = client.search_by_corporate_number(corporative_number)
            print(f"Corporate info for {corporate_number}:")
            print(f"  Name: {result.get('hojinInfo', {}).get('corporateName', 'N/A')}")
            print(f"  Address: {result.get('hojinInfo', {}).get('address', 'N/A')}")

        # Example 2: Search by corporate name
        company_name = "株式会社サンプル"  # Replace with actual name
        search_result = client.search_by_corporate_name(name=company_name, limit=10)
        print(f"\nSearch results for '{company_name}':")
        print(f"  Found: {search_result.get('hitNum', 0)} results")

        if 'hojinInfo' in search_result:
            for company in search_result['hojinInfo'][:3]:  # Show first 3
                print(f"    - {company.get('corporateName')}: {company.get('hojinBango')}")

        # Example 3: Get corporate info directly
        # corporate_info = client.get_corporate_info(corporative_number)
        # print(f"\nCorporate info: {corporate_info}")

        # Example 4: Paginated search
        # all_results = client.search_paginated(name=company_name, max_results=500)
        # print(f"\nTotal results fetched: {all_results.get('hitNum', 0)}")

    except GbizInfoAPIError as e:
        print(f"Error: {e}")