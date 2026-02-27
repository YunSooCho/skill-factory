"""
Bitly API Client

Supports:
- Create Bitlink
- Get Bitlink
- Search Bitlinks
- Delete Bitlink
- Expand Bitlink
- Get Click Counts
- Get Click Summary
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Bitlink:
    """Bitly link representation"""
    id: Optional[str] = None
    link: Optional[str] = None
    long_url: Optional[str] = None
    title: Optional[str] = None
    created_at: Optional[str] = None
    tags: List[str] = None
    archived: bool = False

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ClickSummary:
    """Click statistics summary"""
    total_clicks: int = 0
    units: int = 0
    unit: str = ""
    unit_reference: Optional[str] = None


@dataclass
class ClickCounts:
    """Click counts by time period"""
    clicks: List[Dict[str, Any]]
    unit: str = ""
    unit_reference: Optional[str] = None


class BitlyClient:
    """
    Bitly API client for URL shortening and analytics.

    Authentication: API Key (Header: Authorization: Bearer {token})
    Base URL: https://api-ssl.bitly.com/v4
    """

    BASE_URL = "https://api-ssl.bitly.com/v4"

    def __init__(self, access_token: str):
        """
        Initialize Bitly client.

        Args:
            access_token: Bitly access token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 204:
                return {}
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid access token")
            elif response.status_code == 403:
                raise Exception("Forbidden: Insufficient permissions")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Bitlink Operations ====================

    def create_bitlink(
        self,
        long_url: str,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        domain: Optional[str] = None
    ) -> Bitlink:
        """
        Create a shortened Bitlink.

        Args:
            long_url: Original long URL to shorten
            title: Custom title for the link
            tags: List of tags for categorization
            domain: Custom domain (default: bit.ly)

        Returns:
            Bitlink object
        """
        if not long_url:
            raise ValueError("Long URL is required")

        payload = {"long_url": long_url}

        if title:
            payload["title"] = title
        if tags:
            payload["tags"] = tags
        if domain:
            payload["domain"] = domain

        result = self._request("POST", "/bitlinks", json=payload)
        return self._parse_bitlink(result)

    def get_bitlink(self, bitlink_id: str) -> Bitlink:
        """
        Retrieve a Bitlink by ID.

        Args:
            bitlink_id: Bitlink ID (e.g., bit.ly/abc1234 or the full ID)

        Returns:
            Bitlink object
        """
        result = self._request("GET", f"/bitlinks/{bitlink_id}")
        return self._parse_bitlink(result)

    def search_bitlinks(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50
    ) -> List[Bitlink]:
        """
        Search for Bitlinks.

        Args:
            query: Search query string
            tags: Filter by tags
            created_after: ISO date to filter after
            created_before: ISO date to filter before
            search_query: Deep search query
            limit: Number of results (max 1000)

        Returns:
            List of Bitlink objects
        """
        params = {}
        if query:
            params["query"] = query
        if tags:
            params["tags"] = ",".join(tags)
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if search_query:
            params["search_query"] = search_query
        params["size"] = min(limit, 1000)

        result = self._request("GET", "/organizations/default/bitlinks", params=params)

        bitlinks = []
        if isinstance(result, dict) and "links" in result:
            for link_data in result.get("links", []):
                bitlinks.append(self._parse_bitlink(link_data))
        elif isinstance(result, list):
            for link_data in result:
                bitlinks.append(self._parse_bitlink(link_data))

        return bitlinks

    def delete_bitlink(self, bitlink_id: str) -> None:
        """
        Delete a Bitlink.

        Args:
            bitlink_id: Bitlink ID
        """
        self._request("DELETE", f"/bitlinks/{bitlink_id}")

    def expand_bitlink(self, bitlink_id: str) -> str:
        """
        Expand a Bitlink to get the original long URL.

        Args:
            bitlink_id: Bitlink ID

        Returns:
            Original long URL
        """
        result = self._request("GET", f"/expand?bitlink_id={bitlink_id}")
        return result.get("long_url", "")

    # ==================== Analytics Operations ====================

    def get_click_counts(
        self,
        bitlink_id: str,
        unit: str = "day",
        units: int = 7,
        unit_reference: Optional[str] = None,
        size: int = 50
    ) -> ClickCounts:
        """
        Get click counts for a Bitlink over time.

        Args:
            bitlink_id: Bitlink ID
            unit: Time unit (hour, day, week, month)
            units: Number of units
            unit_reference: ISO date to start from
            size: Maximum results

        Returns:
            ClickCounts object
        """
        params = {
            "unit": unit,
            "units": units,
            "size": size
        }
        if unit_reference:
            params["unit_reference"] = unit_reference

        result = self._request(
            "GET",
            f"/bitlinks/{bitlink_id}/clicks",
            params=params
        )

        return ClickCounts(
            clicks=result.get("link_clicks", []),
            unit=unit,
            unit_reference=unit_reference
        )

    def get_click_summary(
        self,
        bitlink_id: str,
        unit: str = "day",
        units: int = 7,
        unit_reference: Optional[str] = None
    ) -> ClickSummary:
        """
        Get click summary for a Bitlink.

        Args:
            bitlink_id: Bitlink ID
            unit: Time unit (hour, day, week, month)
            units: Number of units
            unit_reference: ISO date to start from

        Returns:
            ClickSummary object
        """
        params = {
            "unit": unit,
            "units": units
        }
        if unit_reference:
            params["unit_reference"] = unit_reference

        result = self._request(
            "GET",
            f"/bitlinks/{bitlink_id}/clicks/summary",
            params=params
        )

        return ClickSummary(
            total_clicks=result.get("total_clicks", 0),
            units=units,
            unit=unit,
            unit_reference=unit_reference
        )

    # ==================== Helper Methods ====================

    def _parse_bitlink(self, data: Dict[str, Any]) -> Bitlink:
        """Parse bitlink data from API response"""
        return Bitlink(
            id=data.get("id"),
            link=data.get("link"),
            long_url=data.get("long_url"),
            title=data.get("title"),
            created_at=data.get("created_at"),
            tags=data.get("tags", []),
            archived=data.get("archived", False)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    access_token = "your_bitly_access_token"

    client = BitlyClient(access_token=access_token)

    try:
        # Create a bitlink
        bitlink = client.create_bitlink(
            long_url="https://www.example.com/very/long/url/that/needs/shortening",
            title="Example Link",
            tags=["marketing", "social"]
        )
        print(f"Created: {bitlink.link} -> {bitlink.long_url}")

        # Get bitlink details
        details = client.get_bitlink(bitlink.id)
        print(f"Title: {details.title}, Tags: {details.tags}")

        # Search bitlinks
        bitlinks = client.search_bitlinks(
            tags=["marketing"],
            limit=10
        )
        print(f"Found {len(bitlinks)} bitlinks")

        # Get click summary
        summary = client.get_click_summary(bitlink.id, unit="day", units=7)
        print(f"Total clicks (7 days): {summary.total_clicks}")

        # Get click counts by day
        clicks = client.get_click_counts(bitlink.id, unit="day", units=7)
        print(f"Clicks per day: {len(clicks.clicks)} data points")

        # Expand bitlink
        long_url = client.expand_bitlink(bitlink.id)
        print(f"Expanded: {long_url}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()