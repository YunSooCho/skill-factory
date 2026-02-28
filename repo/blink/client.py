"""
Blink API Client

Supports:
- Create Shortened Link
- Get Link Details
- Update Link
- Delete Link
- List Links
- Get Link Analytics
- Get QR Code
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlinkLink:
    """Blink shortened link representation"""
    id: Optional[int] = None
    short_url: Optional[str] = None
    original_url: Optional[str] = None
    title: Optional[str] = None
    domain: Optional[str] = None
    tags: List[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    expires_at: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class LinkAnalytics:
    """Link analytics data"""
    clicks: int = 0
    unique_clicks: int = 0
    last_click_at: Optional[str] = None
    top_countries: Optional[Dict[str, int]] = None
    top_referrers: Optional[Dict[str, int]] = None


class BlinkClient:
    """
    Blink API client for URL shortening and analytics.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.blink.com/v1
    """

    BASE_URL = "https://api.blink.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Blink client.

        Args:
            api_key: Blink API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Link Operations ====================

    def create_shortened_link(
        self,
        original_url: str,
        title: Optional[str] = None,
        domain: Optional[str] = None,
        tags: Optional[List[str]] = None,
        expires_at: Optional[str] = None,
        custom_slug: Optional[str] = None
    ) -> BlinkLink:
        """
        Create a shortened link.

        Args:
            original_url: Original long URL (required)
            title: Custom title for the link
            domain: Custom domain
            tags: List of tags for organization
            expires_at: Expiration date (ISO format)
            custom_slug: Custom slug for the short URL

        Returns:
            BlinkLink object
        """
        if not original_url:
            raise ValueError("Original URL is required")

        payload: Dict[str, Any] = {"url": original_url}

        if title:
            payload["title"] = title
        if domain:
            payload["domain"] = domain
        if tags:
            payload["tags"] = tags
        if expires_at:
            payload["expires_at"] = expires_at
        if custom_slug:
            payload["slug"] = custom_slug

        result = self._request("POST", "/links", json=payload)
        return self._parse_link(result)

    def get_link(self, link_id: int) -> BlinkLink:
        """
        Retrieve link details by ID.

        Args:
            link_id: Link ID

        Returns:
            BlinkLink object
        """
        result = self._request("GET", f"/links/{link_id}")
        return self._parse_link(result)

    def update_link(
        self,
        link_id: int,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        expires_at: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> BlinkLink:
        """
        Update an existing link.

        Args:
            link_id: Link ID
            title: Updated title
            tags: Updated tags list
            expires_at: Updated expiration date
            is_active: Active status

        Returns:
            Updated BlinkLink object
        """
        payload: Dict[str, Any] = {}

        if title is not None:
            payload["title"] = title
        if tags is not None:
            payload["tags"] = tags
        if expires_at is not None:
            payload["expires_at"] = expires_at
        if is_active is not None:
            payload["is_active"] = is_active

        result = self._request("PATCH", f"/links/{link_id}", json=payload)
        return self._parse_link(result)

    def delete_link(self, link_id: int) -> Dict[str, Any]:
        """
        Delete a link permanently.

        Args:
            link_id: Link ID

        Returns:
            Deletion response
        """
        return self._request("DELETE", f"/links/{link_id}")

    def list_links(
        self,
        limit: int = 20,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all links with filtering.

        Args:
            limit: Number of results per page
            offset: Pagination offset
            tags: Filter by tags
            search: Search in title or URL

        Returns:
            Dictionary containing links list and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if tags:
            params["tags"] = ",".join(tags)
        if search:
            params["search"] = search

        return self._request("GET", "/links", params=params)

    # ==================== Analytics Operations ====================

    def get_link_analytics(
        self,
        link_id: int,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> LinkAnalytics:
        """
        Get analytics data for a link.

        Args:
            link_id: Link ID
            from_date: Start date (ISO format)
            to_date: End date (ISO format)
            group_by: Group results by (day, week, month)

        Returns:
            LinkAnalytics object
        """
        params: Dict[str, Any] = {}

        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if group_by:
            params["group_by"] = group_by

        result = self._request("GET", f"/links/{link_id}/analytics", params=params)

        return LinkAnalytics(
            clicks=result.get("clicks", 0),
            unique_clicks=result.get("unique_clicks", 0),
            last_click_at=result.get("last_click_at"),
            top_countries=result.get("top_countries"),
            top_referrers=result.get("top_referrers")
        )

    # ==================== QR Code Operations ====================

    def get_qr_code(
        self,
        link_id: int,
        size: int = 300,
        format: str = "png",
        color: Optional[str] = None,
        logo: Optional[str] = None
    ) -> bytes:
        """
        Generate a QR code for a link.

        Args:
            link_id: Link ID
            size: QR code size in pixels
            format: Image format (png, jpg, svg)
            color: QR code color (hex)
            logo: URL to logo image

        Returns:
            QR code image bytes
        """
        params: Dict[str, Any] = {
            "size": size,
            "format": format
        }

        if color:
            params["color"] = color
        if logo:
            params["logo"] = logo

        response = self.session.get(
            f"{self.BASE_URL}/links/{link_id}/qr",
            params=params
        )

        if response.status_code == 200:
            return response.content
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded")
        else:
            raise Exception(f"Failed to generate QR code: {response.status_code}")

    # ==================== Helper Methods ====================

    def _parse_link(self, data: Dict[str, Any]) -> BlinkLink:
        """Parse link data from API response"""
        return BlinkLink(
            id=data.get("id"),
            short_url=data.get("short_url"),
            original_url=data.get("original_url"),
            title=data.get("title"),
            domain=data.get("domain"),
            tags=data.get("tags", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            expires_at=data.get("expires_at"),
            is_active=data.get("is_active", True)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_blink_api_key"

    client = BlinkClient(api_key=api_key)

    try:
        # Create shortened link
        link = client.create_shortened_link(
            original_url="https://www.example.com/very/long/url",
            title="Product Page",
            tags=["marketing", "campaign"],
            custom_slug="product-launch"
        )
        print(f"Link created: {link.short_url} (ID: {link.id})")

        # Get link details
        fetched = client.get_link(link.id)
        print(f"Fetched: {fetched.title} - {fetched.short_url}")

        # Update link
        updated = client.update_link(
            fetched.id,
            tags=["marketing", "campaign", "q1-2024"]
        )
        print(f"Updated tags: {updated.tags}")

        # Get analytics
        analytics = client.get_link_analytics(
            fetched.id,
            from_date="2024-01-01T00:00:00Z",
            to_date="2024-01-31T23:59:59Z"
        )
        print(f"Analytics - Clicks: {analytics.clicks}, Unique: {analytics.unique_clicks}")

        # Generate QR code
        qr_bytes = client.get_qr_code(fetched.id, size=400, format="png")
        print(f"QR code generated ({len(qr_bytes)} bytes)")

        # List all links
        links_response = client.list_links(limit=10, tags=["marketing"])
        print(f"Found {len(links_response.get('links', []))} marketing links")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()