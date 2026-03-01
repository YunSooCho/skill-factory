"""
Gbiz-info API Client
API Documentation: https://info.gbiz.go.jp/
"""

import requests
from typing import Optional, Dict, List, Any


class GbizInfoAPIError(Exception):
    """Custom exception for Gbiz-info API errors."""
    pass


class GbizInfoClient:
    """Client for Gbiz-info API - Japanese corporate information lookup."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://info.gbiz.go.jp/api"):
        """
        Initialize Gbiz-info API client.

        Args:
            api_key: Your Gbiz-info API key (optional for some endpoints)
            base_url: API base URL (default: https://info.gbiz.go.jp/api)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
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

        # Add API key to params if provided
        if self.api_key:
            params = kwargs.get('params', {})
            params['apiKey'] = self.api_key
            kwargs['params'] = params

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
            raise GbizInfoAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise GbizInfoAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def search_by_corporation_number(
        self,
        corporate_number: str
    ) -> Dict[str, Any]:
        """
        Search corporation by corporate number (法人番号).

        API Reference: https://info.gbiz.go.jp/hojin/Search?corporateNumber

        Args:
            corporate_number: 13-digit corporate number (法人番号)

        Returns:
            Corporation information including:
            - corporate_number: Corporate number
            - name: Company name
            - address: Postal code and address
            - status: Company status
            - capital: Capital amount
            - establishment_date: Establishment date
        """
        endpoint = "/hojin/v1/hojin"

        params = {
            "corporateNumber": corporate_number
        }

        return self._make_request("GET", endpoint, params=params)

    def search_by_corporation_number_advanced(
        self,
        corporate_number: str,
        history: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetch detailed corporation information by corporate number.

        Args:
            corporate_number: 13-digit corporate number
            history: History flag (0: latest only, 1: include history)

        Returns:
            Detailed corporation information
        """
        endpoint = "/hojin/v1/hojin"

        params = {
            "corporateNumber": corporate_number
        }

        if history is not None:
            params["history"] = str(history)

        return self._make_request("GET", endpoint, params=params)

    def search_by_name(
        self,
        name: str,
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search corporations by name.

        API Reference: https://info.gbiz.go.jp/hojin/Search

        Args:
            name: Company name or partial name
            page: Page number (default: 1)
            limit: Results per page (default: 10, max: 100)
            status: Company status filter (01: active, 02: dissolved, 03: liquidated)

        Returns:
            List of matching corporations
        """
        endpoint = "/hojin/v1/search"

        params = {
            "name": name,
            "page": str(page),
            "limit": str(min(limit, 100))
        }

        if status:
            params["status"] = status

        return self._make_request("GET", endpoint, params=params)

    def search_by_name_advanced(
        self,
        name: str,
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None,
        exact_match: bool = False
    ) -> Dict[str, Any]:
        """
        Advanced search by company name.

        Args:
            name: Company name
            page: Page number
            limit: Results per page
            status: Company status filter
            exact_match: Exact name match flag

        Returns:
            List of matching corporations
        """
        endpoint = "/hojin/v1/search"

        params = {
            "name": name,
            "page": str(page),
            "limit": str(min(limit, 100))
        }

        if status:
            params["status"] = status
        if exact_match:
            params["exactMatch"] = "1"

        return self._make_request("GET", endpoint, params=params)

    def get_detailed_info(
        self,
        corporate_number: str
    ) -> Dict[str, Any]:
        """
        Get detailed corporation information.

        Args:
            corporate_number: 13-digit corporate number

        Returns:
            Detailed corporation information including:
            - Corporate details
            - Company history
            - Subsidiaries
            - Officers
            - Financial information
        """
        endpoint = f"/hojin/v1/hojin/{corporate_number}"

        return self._make_request("GET", endpoint)

    def search_by_corporation_name(
        self,
        corporate_name: str,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search by corporate name (Japanese).

        Args:
            corporate_name: Corporate name (Japanese)
            page: Page number

        Returns:
            Search results
        """
        endpoint = "/subjects/v1/subjects"

        params = {
            "q": corporate_name,
            "page": str(page)
        }

        return self._make_request("GET", endpoint, params=params)

    def search_by_corporation_number_simple(
        self,
        corporate_number: str
    ) -> Dict[str, Any]:
        """
        Simple search by corporate number (deprecated).

        Deprecated: Use search_by_corporate_number() instead.

        Args:
            corporate_number: Corporate number

        Returns:
            Basic corporation information
        """
        # This is the older/deprecated endpoint
        endpoint = "/subjects/v1/subjects"

        params = {
            "corporateNumber": corporate_number
        }

        return self._make_request("GET", endpoint, params=params)

    def search_by_name_simple(
        self,
        name: str
    ) -> Dict[str, Any]:
        """
        Simple search by name (deprecated).

        Deprecated: Use search_by_name() instead.

        Args:
            name: Company name

        Returns:
            Basic search results
        """
        endpoint = "/subjects/v1/subjects"

        params = {
            "q": name
        }

        return self._make_request("GET", endpoint, params=params)

    def search_by_corporate_number_old(
        self,
        corporate_number: str
    ) -> Dict[str, Any]:
        """
        Old endpoint search by corporate number (deprecated).

        Deprecated: Use search_by_corporate_number() instead.

        Args:
            corporate_number: Corporate number

        Returns:
            Corporation information
        """
        endpoint = "/subjects/v1/subjects"

        params = {
            "corporateNumber": corporate_number,
            "mode": "1"
        }

        return self._make_request("GET", endpoint, params=params)

    def get_corporation_status(self, corporate_number: str) -> Dict[str, Any]:
        """
        Get corporation status information.

        Args:
            corporate_number: 13-digit corporate number

        Returns:
            Status information:
            - status: Current status (01: active, etc.)
            - name: Company name
            - update_date: Last update date
        """
        endpoint = f"/hojin/v1/hojin/{corporate_number}"

        response = self._make_request("GET", endpoint)
        data = response.get('data', {})

        return {
            "status": "success",
            "data": {
                "corporate_number": data.get("corporateNumber"),
                "status": data.get("status"),
                "name": data.get("name"),
                "update_date": data.get("updateDate")
            }
        }