"""
Beamer API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BeamerAPIError(Exception):
    """Base exception for Beamer API errors"""
    pass


class BeamerAuthError(BeamerAPIError):
    """Authentication error"""
    pass


class BeamerRateLimitError(BeamerAPIError):
    """Rate limit exceeded"""
    pass


class BeamerClient:
    """Beamer API Client for managing posts"""

    BASE_URL = "https://api.getbeamer.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Beamer client

        Args:
            api_key: Your Beamer API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def create_post(
        self,
        headline: str,
        content: str,
        category: Optional[str] = None,
        date: Optional[str] = None,
        link: Optional[str] = None,
        linkText: Optional[str] = None,
        linkIcon: Optional[str] = None,
        publish: Optional[bool] = None,
        top: Optional[bool] = None,
        user_segment_external_id: Optional[str] = None,
        user_segments_external_ids: Optional[List[str]] = None,
        language: Optional[str] = None,
        image_url: Optional[str] = None,
        change_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new Beamer post

        Args:
            headline: The post headline
            content: The post HTML content
            category: Optional category (e.g., 'new', 'improvement', 'fix')
            date: Optional date in ISO 8601 format
            link: Optional external link URL
            linkText: Optional link text
            linkIcon: Optional link icon URL
            publish: Whether to publish immediately (default: false)
            top: Whether to pin to top
            user_segment_external_id: Single user segment ID
            user_segments_external_ids: List of user segment IDs
            language: Language code (e.g., 'en', 'es', 'ja')
            image_url: Cover image URL
            change_type: Type of change

        Returns:
            API response data

        Raises:
            BeamerAPIError: For general API errors
            BeamerAuthError: For authentication issues
            BeamerRateLimitError: For rate limit issues
        """
        endpoint = f"{self.BASE_URL}/posts"
        payload = {
            "headline": headline,
            "content": content,
        }

        # Add optional parameters
        if category:
            payload["category"] = category
        if date:
            payload["date"] = date
        if link:
            payload["link"] = link
        if linkText:
            payload["linkText"] = linkText
        if linkIcon:
            payload["linkIcon"] = linkIcon
        if publish is not None:
            payload["publish"] = publish
        if top is not None:
            payload["top"] = top
        if user_segment_external_id:
            payload["userSegmentExternalId"] = user_segment_external_id
        if user_segments_external_ids:
            payload["userSegmentsExternalIds"] = user_segments_external_ids
        if language:
            payload["language"] = language
        if image_url:
            payload["imageUrl"] = image_url
        if change_type:
            payload["changeType"] = change_type

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise BeamerAuthError("Invalid API key")
            elif e.response.status_code == 429:
                raise BeamerRateLimitError("Rate limit exceeded")
            elif e.response.status_code == 400:
                raise BeamerAPIError(f"Invalid request: {e.response.text}")
            elif e.response.status_code == 403:
                raise BeamerAPIError("Forbidden - insufficient permissions")
            elif e.response.status_code == 404:
                raise BeamerAPIError("Resource not found")
            else:
                raise BeamerAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise BeamerAPIError(f"Request failed: {str(e)}")

    def list_posts(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        published: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        List posts

        Args:
            limit: Number of posts to return
            page: Page number
            published: Filter by published status

        Returns:
            List of posts
        """
        endpoint = f"{self.BASE_URL}/posts"
        params = {}
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        if published is not None:
            params["published"] = str(published).lower()

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise BeamerAuthError("Invalid API key")
            elif e.response.status_code == 429:
                raise BeamerRateLimitError("Rate limit exceeded")
            else:
                raise BeamerAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise BeamerAPIError(f"Request failed: {str(e)}")

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a post

        Args:
            post_id: The ID of the post to delete

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/posts/{post_id}"

        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise BeamerAuthError("Invalid API key")
            elif e.response.status_code == 404:
                raise BeamerAPIError(f"Post {post_id} not found")
            else:
                raise BeamerAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise BeamerAPIError(f"Request failed: {str(e)}")