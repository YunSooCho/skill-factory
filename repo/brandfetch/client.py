"""
Brandfetch API Client

Supports:
- Get Brand Information
- Search Brands
- Get Brand Logos
- Get Brand Colors
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Brand:
    """Brand information"""
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    icon_url: Optional[str] = None
    colors: List[str] = None
    social_links: Dict[str, str] = None

    def __post_init__(self):
        if self.colors is None:
            self.colors = []
        if self.social_links is None:
            self.social_links = {}


@dataclass
class BrandLogo:
    """Brand logo information"""
    type: Optional[str] = None
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    size_kb: Optional[float] = None


@dataclass
class BrandColor:
    """Brand color information"""
    hex: Optional[str] = None
    rgb: Optional[str] = None
    type: Optional[str] = None
    brightness: Optional[str] = None


class BrandfetchClient:
    """
    Brandfetch API client for brand information, logos, and colors.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.brandfetch.io/v1
    """

    BASE_URL = "https://api.brandfetch.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Brandfetch client.

        Args:
            api_key: Brandfetch API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
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
                raise Exception(f"Brand not found")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Brand Information ====================

    def get_brand_info(self, domain: str) -> Brand:
        """
        Get comprehensive brand information for a domain.

        Args:
            domain: Brand domain (e.g., "apple.com")

        Returns:
            Brand object
        """
        if not domain:
            raise ValueError("Domain is required")

        result = self._request("GET", f"/brands/{domain}")
        return self._parse_brand(result)

    def search_brands(self, query: str, limit: int = 5) -> List[Brand]:
        """
        Search for brands by query.

        Args:
            query: Search query (brand name or domain)
            limit: Number of results to return

        Returns:
            List of Brand objects
        """
        if not query:
            raise ValueError("Search query is required")

        result = self._request("GET", "/brands/search", params={
            "q": query,
            "limit": limit
        })

        return [self._parse_brand(b) for b in result.get("results", [])]

    # ==================== Brand Logos ====================

    def get_brand_logos(self, domain: str) -> List[BrandLogo]:
        """
        Get all available logos for a brand.

        Args:
            domain: Brand domain

        Returns:
            List of BrandLogo objects
        """
        if not domain:
            raise ValueError("Domain is required")

        result = self._request("GET", f"/brands/{domain}/logos")
        return [self._parse_logo(logo) for logo in result.get("logos", [])]

    def get_primary_logo(self, domain: str, size: str = "large") -> BrandLogo:
        """
        Get the primary logo for a brand.

        Args:
            domain: Brand domain
            size: Logo size (small, medium, large)

        Returns:
            BrandLogo object
        """
        if not domain:
            raise ValueError("Domain is required")

        result = self._request("GET", f"/brands/{domain}/logo", params={"size": size})
        return self._parse_logo(result)

    # ==================== Brand Colors ====================

    def get_brand_colors(self, domain: str) -> List[BrandColor]:
        """
        Get brand colors.

        Args:
            domain: Brand domain

        Returns:
            List of BrandColor objects
        """
        if not domain:
            raise ValueError("Domain is required")

        result = self._request("GET", f"/brands/{domain}/colors")
        return [self._parse_color(color) for color in result.get("colors", [])]

    # ==================== Helper Methods ====================

    def _parse_brand(self, data: Dict[str, Any]) -> Brand:
        """Parse brand data from API response"""
        return Brand(
            name=data.get("name"),
            domain=data.get("domain"),
            description=data.get("description"),
            website=data.get("website"),
            logo_url=data.get("logo_url"),
            icon_url=data.get("icon_url"),
            colors=data.get("colors", []),
            social_links=data.get("social_links", {})
        )

    def _parse_logo(self, data: Dict[str, Any]) -> BrandLogo:
        """Parse logo data from API response"""
        return BrandLogo(
            type=data.get("type"),
            url=data.get("url"),
            width=data.get("width"),
            height=data.get("height"),
            format=data.get("format"),
            size_kb=data.get("size_kb")
        )

    def _parse_color(self, data: Dict[str, Any]) -> BrandColor:
        """Parse color data from API response"""
        return BrandColor(
            hex=data.get("hex"),
            rgb=data.get("rgb"),
            type=data.get("type"),
            brightness=data.get("brightness")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_brandfetch_api_key"

    client = BrandfetchClient(api_key=api_key)

    try:
        # Get brand information
        brand = client.get_brand_info("apple.com")
        print(f"Brand: {brand.name}")
        print(f"Website: {brand.website}")
        print(f"Description: {brand.description}")

        # Get logos
        logos = client.get_brand_logos("apple.com")
        print(f"\nLogos: {len(logos)} found")
        for logo in logos:
            print(f"  - {logo.type} ({logo.width}x{logo.height}): {logo.url}")

        # Get primary logo
        primary_logo = client.get_primary_logo("apple.com", size="large")
        print(f"\nPrimary logo: {primary_logo.url}")

        # Get colors
        colors = client.get_brand_colors("apple.com")
        print(f"\nBrand colors: {len(colors)}")
        for color in colors:
            print(f"  - {color.hex} ({color.type})")

        # Search brands
        search_results = client.search_brands("google", limit=3)
        print(f"\nSearch results: {len(search_results)}")
        for b in search_results:
            print(f"  - {b.name} ({b.domain})")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()