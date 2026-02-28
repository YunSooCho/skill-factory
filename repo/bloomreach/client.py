"""
Bloomreach API Client

Supports:
- Get Personalized Recommendations
- Track User Events
- Get User Profile
- Search Products
- Get Content
- Update User Profile
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Recommendation:
    """Product recommendation"""
    product_id: Optional[str] = None
    title: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    relevance_score: Optional[float] = None
    category: Optional[str] = None


@dataclass
class UserEvent:
    """User tracking event"""
    event_type: Optional[str] = None
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    timestamp: Optional[str] = None
    properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class UserProfile:
    """User profile data"""
    user_id: Optional[str] = None
    segments: List[str] = None
    interests: List[str] = None
    last_activity: Optional[str] = None
    affinities: Dict[str, float] = None

    def __post_init__(self):
        if self.segments is None:
            self.segments = []
        if self.interests is None:
            self.interests = []
        if self.affinities is None:
            self.affinities = {}


@dataclass
class SearchResult:
    """Search result"""
    product_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    score: Optional[float] = None


@dataclass
class ContentItem:
    """Content item"""
    content_id: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[str] = None


class BloomreachClient:
    """
    BloomReach API client for personalization and content delivery.

    Authentication: API Key (Header: Authorization: Basic {api_key})
    Base URL: https://api.bloomreach.com/v1
    """

    BASE_URL = "https://api.bloomreach.com/v1"

    def __init__(self, api_key: str, account_id: str):
        """
        Initialize BloomReach client.

        Args:
            api_key: BloomReach API key
            account_id: BloomReach account ID
        """
        self.api_key = api_key
        self.account_id = account_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Account-ID": self.account_id
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
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

    # ==================== Recommendations ====================

    def get_personalized_recommendations(
        self,
        user_id: Optional[str] = None,
        placement_id: Optional[str] = None,
        item_id: Optional[str] = None,
        limit: int = 10,
        strategy: Optional[str] = None
    ) -> List[Recommendation]:
        """
        Get personalized product recommendations.

        Args:
            user_id: User ID for personalization
            placement_id: Placement ID for recommendations
            item_id: Item ID for item-based recommendations
            limit: Number of recommendations to return
            strategy: Recommendation strategy (e.g., "personalized", "trending")

        Returns:
            List of Recommendation objects
        """
        params: Dict[str, Any] = {
            "limit": limit
        }

        if user_id:
            params["user_id"] = user_id
        if placement_id:
            params["placement_id"] = placement_id
        if item_id:
            params["item_id"] = item_id
        if strategy:
            params["strategy"] = strategy

        result = self._request("GET", "/recommendations", params=params)
        return [self._parse_recommendation(r) for r in result.get("items", [])]

    # ==================== Event Tracking ====================

    def track_event(
        self,
        event_type: str,
        user_id: str,
        properties: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Track a user event for personalization.

        Args:
            event_type: Event type (view, click, purchase, etc.)
            user_id: User ID
            properties: Event properties
            timestamp: Event timestamp (ISO format)

        Returns:
            Event tracking response
        """
        if not event_type:
            raise ValueError("Event type is required")
        if not user_id:
            raise ValueError("User ID is required")

        payload: Dict[str, Any] = {
            "event_type": event_type,
            "user_id": user_id
        }

        if properties:
            payload["properties"] = properties
        if timestamp:
            payload["timestamp"] = timestamp

        return self._request("POST", "/events", json=payload)

    # ==================== User Profile ====================

    def get_user_profile(self, user_id: str) -> UserProfile:
        """
        Get user profile for personalization.

        Args:
            user_id: User ID

        Returns:
            UserProfile object
        """
        if not user_id:
            raise ValueError("User ID is required")

        result = self._request("GET", f"/users/{user_id}")
        return self._parse_user_profile(result)

    def update_user_profile(
        self,
        user_id: str,
        attributes: Optional[Dict[str, Any]] = None,
        add_segments: Optional[List[str]] = None,
        remove_segments: Optional[List[str]] = None
    ) -> UserProfile:
        """
        Update user profile.

        Args:
            user_id: User ID
            attributes: User attributes
            add_segments: Segments to add
            remove_segments: Segments to remove

        Returns:
            Updated UserProfile object
        """
        if not user_id:
            raise ValueError("User ID is required")

        payload: Dict[str, Any] = {}

        if attributes:
            payload["attributes"] = attributes
        if add_segments:
            payload["add_segments"] = add_segments
        if remove_segments:
            payload["remove_segments"] = remove_segments

        result = self._request("PATCH", f"/users/{user_id}", json=payload)
        return self._parse_user_profile(result)

    # ==================== Search ====================

    def search_products(
        self,
        query: str,
        user_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for products.

        Args:
            query: Search query
            user_id: User ID for personalized search
            filters: Search filters
            sort: Sort field
            limit: Number of results
            offset: Pagination offset

        Returns:
            Search results with pagination info
        """
        if not query:
            raise ValueError("Search query is required")

        payload: Dict[str, Any] = {
            "query": query,
            "limit": limit,
            "offset": offset
        }

        if user_id:
            payload["user_id"] = user_id
        if filters:
            payload["filters"] = filters
        if sort:
            payload["sort"] = sort

        result = self._request("POST", "/search", json=payload)

        # Parse results
        results = [self._parse_search_result(r) for r in result.get("results", [])]
        total = result.get("total", 0)

        return {
            "results": results,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    # ==================== Content Management ====================

    def get_content(
        self,
        content_id: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get content items.

        Args:
            content_id: Specific content ID
            content_type: Filter by content type
            limit: Number of results
            offset: Pagination offset

        Returns:
            Content items and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if content_id:
            params["content_id"] = content_id
        if content_type:
            params["type"] = content_type

        result = self._request("GET", "/content", params=params)

        if content_id and len(result.get("items", [])) == 1:
            return {"content": self._parse_content(result["items"][0])}
        else:
            contents = [self._parse_content(c) for c in result.get("items", [])]
            return {
                "contents": contents,
                "total": result.get("total", 0)
            }

    # ==================== Helper Methods ====================

    def _parse_recommendation(self, data: Dict[str, Any]) -> Recommendation:
        """Parse recommendation data from API response"""
        return Recommendation(
            product_id=data.get("product_id"),
            title=data.get("title"),
            price=data.get("price"),
            image_url=data.get("image_url"),
            product_url=data.get("product_url"),
            relevance_score=data.get("relevance_score"),
            category=data.get("category")
        )

    def _parse_user_profile(self, data: Dict[str, Any]) -> UserProfile:
        """Parse user profile data from API response"""
        return UserProfile(
            user_id=data.get("user_id"),
            segments=data.get("segments", []),
            interests=data.get("interests", []),
            last_activity=data.get("last_activity"),
            affinities=data.get("affinities", {})
        )

    def _parse_search_result(self, data: Dict[str, Any]) -> SearchResult:
        """Parse search result data from API response"""
        return SearchResult(
            product_id=data.get("product_id"),
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            image_url=data.get("image_url"),
            product_url=data.get("product_url"),
            score=data.get("score")
        )

    def _parse_content(self, data: Dict[str, Any]) -> ContentItem:
        """Parse content item data from API response"""
        return ContentItem(
            content_id=data.get("content_id"),
            title=data.get("title"),
            body=data.get("body"),
            type=data.get("type"),
            url=data.get("url"),
            image_url=data.get("image_url"),
            published_at=data.get("published_at")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_bloomreach_api_key"
    account_id = "your_account_id"

    client = BloomreachClient(api_key=api_key, account_id=account_id)

    try:
        # Get personalized recommendations
        recommendations = client.get_personalized_recommendations(
            user_id="user123",
            placement_id="home_page_top",
            limit=5
        )
        print(f"Recommendations: {len(recommendations)} items")
        for r in recommendations[:3]:
            print(f"  - {r.title} (${r.price})")

        # Track user event
        client.track_event(
            event_type="view",
            user_id="user123",
            properties={"product_id": "prod123", "category": "electronics"}
        )
        print("Event tracked successfully")

        # Get user profile
        profile = client.get_user_profile("user123")
        print(f"Profile segments: {profile.segments}")
        print(f"Interests: {profile.interests}")

        # Search products
        search_results = client.search_products(
            query="wireless headphones",
            user_id="user123",
            limit=10
        )
        print(f"Search results: {search_results['total']} found")
        for r in search_results['results'][:3]:
            print(f"  - {r.title} (${r.price})")

        # Get content
        content = client.get_content(content_type="blog_post", limit=5)
        print(f"Content items: {len(content['contents'])}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()