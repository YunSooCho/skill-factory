"""
Bitly API Client
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse


class BitlyAPIError(Exception):
    """Base exception for Bitly API errors"""
    pass


class BitlyAuthError(BitlyAPIError):
    """Authentication error"""
    pass


class BitlyRateLimitError(BitlyAPIError):
    """Rate limit exceeded"""
    pass


class BitlyClient:
    """Bitly API Client for link management"""

    BASE_URL = "https://api-ssl.bitly.com/v4"

    def __init__(self, access_token: str):
        """
        Initialize Bitly client

        Args:
            access_token: Your Bitly access token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    # ===== Link Management =====

    def shorten_link(
        self,
        long_url: str,
        domain: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[list] = None,
        deep_link: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a shortened link (Bitlink)

        Args:
            long_url: Long URL to shorten
            domain: Custom domain (e.g., "bit.ly", "j.mp")
            title: Link title
            tags: List of tags
            deep_link: Whether to create deep link for mobile app

        Returns:
            Bitlink data
        """
        endpoint = f"{self.BASE_URL}/shorten"
        payload = {"long_url": long_url}

        if domain:
            payload["domain"] = domain
        if title:
            payload["title"] = title
        if tags:
            payload["tags"] = tags
        if deep_link is not None:
            payload["deeplinks"] = deep_link

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def create_bitlink(
        self,
        long_url: str,
        title: Optional[str] = None,
        tags: Optional[list] = None,
        deep_link: Optional[bool] = None,
        created_at: Optional[str] = None,
        notes: Optional[str] = None,
        group_guid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a Bitlink with more options

        Args:
            long_url: Long URL to shorten
            title: Link title
            tags: List of tags
            deep_link: Whether to create deep link
            created_at: Creation time (ISO 8601)
            notes: Link notes
            group_guid: Group GUID

        Returns:
            Bitlink data
        """
        endpoint = f"{self.BASE_URL}/bitlinks"
        payload = {
            "long_url": long_url,
        }

        if title:
            payload["title"] = title
        if tags:
            payload["tags"] = tags
        if deep_link is not None:
            payload["deeplinks"] = deep_link
        if created_at:
            payload["created_at"] = created_at
        if notes:
            payload["notes"] = notes
        if group_guid:
            payload["group_guid"] = group_guid

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def expand_bitlink(
        self,
        bitlink: str,
    ) -> Dict[str, Any]:
        """
        Expand a Bitlink to get the original URL

        Args:
            bitlink: Bitlink URL (e.g., "https://bit.ly/2XxYyZz")

        Returns:
            Expanded link data
        """
        endpoint = f"{self.BASE_URL}/expand"
        payload = {"bitlink_id": bitlink}

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def search_bitlinks(
        self,
        group_guid: Optional[str] = None,
        query: Optional[str] = None,
        domain: Optional[str] = None,
        tags: Optional[list] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Search for Bitlinks

        Args:
            group_guid: Group GUID to filter
            query: Search query
            domain: Domain filter
            tags: Tag filter
            created_after: Filter links created after (ISO 8601)
            created_before: Filter links created before (ISO 8601)
            limit: Maximum results

        Returns:
            Search results
        """
        endpoint = f"{self.BASE_URL}/groups/{group_guid}/bitlinks/search" if group_guid else f"{self.BASE_URL}/search"
        params = {}

        if query:
            params["query"] = query
        if group_guid:
            params["group_guid"] = group_guid
        if domain:
            params["domain"] = domain
        if tags:
            params["tags"] = ",".join(tags)
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if limit:
            params["limit"] = limit

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_bitlink(
        self,
        bitlink: str,
    ) -> Dict[str, Any]:
        """
        Delete a Bitlink

        Args:
            bitlink: Bitlink URL

        Returns:
            API response data
        """
        # Ensure bitlink starts with http:// or https://
        if not bitlink.startswith("http"):
            bitlink = f"https://{bitlink}"

        # Extract the bitlink ID
        parsed = urlparse(bitlink)
        bitlink_id = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        endpoint = f"{self.BASE_URL}/bitlinks/{bitlink_id}"

        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Click Tracking =====

    def get_clicks(
        self,
        bitlink: str,
        unit: Optional[str] = None,
        units: Optional[int] = None,
        unit_reference: Optional[str] = None,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get click count for a Bitlink

        Args:
            bitlink: Bitlink URL
            unit: Time unit (hour, day, week, month)
            units: Number of units
            unit_reference: Reference time (ISO 8601)
            size: Number of result points

        Returns:
            Click data
        """
        if not bitlink.startswith("http"):
            bitlink = f"https://{bitlink}"

        # Extract the bitlink ID
        parsed = urlparse(bitlink)
        bitlink_id = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        endpoint = f"{self.BASE_URL}/bitlinks/{bitlink_id}/clicks/summary"
        params = {}

        if unit:
            params["unit"] = unit
        if units:
            params["units"] = units
        if unit_reference:
            params["unit_reference"] = unit_reference

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_click_summary(
        self,
        bitlink: str,
        unit: str = "day",
        units: int = -1,
    ) -> Dict[str, Any]:
        """
        Get click summary for a Bitlink

        Args:
            bitlink: Bitlink URL
            unit: Time unit (hour, day, week, month)
            units: Number of units (-1 for all available)

        Returns:
            Click summary data
        """
        return self.get_clicks(bitlink, unit=unit, units=units)

    def get_clicks_by_country(
        self,
        bitlink: str,
        unit: Optional[str] = None,
        units: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get clicks by country for a Bitlink

        Args:
            bitlink: Bitlink URL
            unit: Time unit
            units: Number of units

        Returns:
            Clicks by country data
        """
        if not bitlink.startswith("http"):
            bitlink = f"https://{bitlink}"

        parsed = urlparse(bitlink)
        bitlink_id = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        endpoint = f"{self.BASE_URL}/bitlinks/{bitlink_id}/clicks/countries"
        params = {}

        if unit:
            params["unit"] = unit
        if units:
            params["units"] = units

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BitlyAuthError("Invalid access token")
        elif error.response.status_code == 403:
            raise BitlyAPIError("Forbidden - insufficient permissions or over quota")
        elif error.response.status_code == 429:
            raise BitlyRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BitlyAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 404:
            raise BitlyAPIError("Resource not found")
        else:
            raise BitlyAPIError(f"HTTP {error.response.status_code}: {error.response.text}")