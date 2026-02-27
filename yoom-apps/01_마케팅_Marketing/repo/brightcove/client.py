"""
Brightcove API Client
"""

import requests
from typing import Optional, Dict, Any, List
import json


class BrightcoveAPIError(Exception):
    """Base exception for Brightcove API errors"""
    pass


class BrightcoveAuthError(BrightcoveAPIError):
    """Authentication error"""
    pass


class BrightcoveRateLimitError(BrightcoveAPIError):
    """Rate limit exceeded"""
    pass


class BrightcoveClient:
    """Brightcove API Client for video management"""

    BASE_URL = "https://cms.api.brightcove.com/v1"
    INGEST_URL = "https://ingest.api.brightcove.com/v1"
    DYNAMIC_INGEST_URL = "https://ingest.api.brightcove.com/v1/accounts"

    def __init__(self, account_id: str, client_id: str, client_secret: str):
        """
        Initialize Brightcove client

        Args:
            account_id: Brightcove account ID
            client_id: OAuth client ID
            client_secret: OAuth client secret
        """
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.session = requests.Session()
        self._authenticate()

    def _authenticate(self):
        """Authenticate and get access token"""
        auth_url = "https://oauth.brightcove.com/v4/access_token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(auth_url, data=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            })
        except requests.exceptions.HTTPError as e:
            raise BrightcoveAuthError("Authentication failed")

    # ===== Video Management =====

    def create_video(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        reference_id: Optional[str] = None,
        state: Optional[str] = None,
        custom_fields: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a video object (without actual video file)

        Args:
            name: Video name (required)
            description: Video description
            tags: List of tags
            reference_id: Custom reference ID
            state: Video state (ACTIVE, INACTIVE)
            custom_fields: Custom field key-value pairs

        Returns:
            Created video data
        """
        endpoint = f"{self.BASE_URL}/accounts/{self.account_id}/videos"
        payload = {"name": name}

        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if reference_id:
            payload["reference_id"] = reference_id
        if state:
            payload["state"] = state
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_video(
        self,
        video_id: str,
    ) -> Dict[str, Any]:
        """
        Get a single video

        Args:
            video_id: Video ID

        Returns:
            Video data
        """
        endpoint = f"{self.BASE_URL}/accounts/{self.account_id}/videos/{video_id}"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def list_videos(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        List videos

        Args:
            limit: Maximum number of videos
            offset: Result offset
            sort: Sort order (e.g., "-created_at")
            query: Search query
            tags: Filter by tags

        Returns:
            Videos data with items list
        """
        endpoint = f"{self.BASE_URL}/accounts/{self.account_id}/videos"
        params = {}

        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort
        if query:
            params["q"] = query
        if tags:
            params["tags"] = ",".join(tags)

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_video(
        self,
        video_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        reference_id: Optional[str] = None,
        state: Optional[str] = None,
        custom_fields: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Update video metadata

        Args:
            video_id: Video ID
            name: Updated name
            description: Updated description
            tags: Updated tags
            reference_id: Updated reference ID
            state: Updated state
            custom_fields: Updated custom fields

        Returns:
            Updated video data
        """
        endpoint = f"{self.BASE_URL}/accounts/{self.account_id}/videos/{video_id}"
        payload = {}

        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if reference_id:
            payload["reference_id"] = reference_id
        if state:
            payload["state"] = state
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            response = self.session.patch(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_video(
        self,
        video_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a video

        Args:
            video_id: Video ID

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/accounts/{self.account_id}/videos/{video_id}"

        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Ingest/Upload =====

    def get_upload_url(
        self,
        video_id: str,
        profile: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a temporary upload URL for ingesting video

        Args:
            video_id: Video ID
            profile: Ingest profile ID (optional)

        Returns:
            Upload URL and related information
        """
        endpoint = f"{self.INGEST_URL}/accounts/{self.account_id}/videos/{video_id}/upload-urls"
        payload = {}

        if profile:
            payload["profile"] = profile

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def upload_file_to_url(
        self,
        upload_url: str,
        file_path: str,
    ) -> Dict[str, Any]:
        """
        Upload a file to a signed upload URL

        Args:
            upload_url: Signed upload URL
            file_path: Path to local file

        Returns:
            Upload result
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(upload_url, files=files)
                response.raise_for_status()
                return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            raise BrightcoveAPIError(f"Upload failed: {e.response.text}")
        except Exception as e:
            raise BrightcoveAPIError(f"Upload failed: {str(e)}")

    def ingest_media(
        self,
        video_id: str,
        video_source: str,
        source_type: str = "vod",
        profile: Optional[str] = None,
        capture_images: Optional[bool] = None,
        callbacks: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Ingest media (Dynamic Ingest)

        Args:
            video_id: Video ID
            video_source: Source URL or blob storage path
            source_type: Source type ("vod", "live", etc.)
            profile: Ingest profile ID
            capture_images: Whether to capture poster/thumbnail images
            callbacks: List of callback URLs

        Returns:
            Ingest job data
        """
        endpoint = f"{self.DYNAMIC_INGEST_URL}/{self.account_id}/videos/{video_id}/ingest-requests"
        payload = {
            "master": {
                "url": video_source
            },
            "profile": profile or "multi-platform-standard-static"
        }

        if source_type:
            payload["master"]["type"] = source_type
        if capture_images is not None:
            payload["capture-images"] = capture_images
        if callbacks:
            payload["callbacks"] = callbacks

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Complete Workflow =====

    def upload_and_ingest_video(
        self,
        video_name: str,
        video_file_path: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Complete workflow: Create video, upload file, and ingest

        Args:
            video_name: Video name
            video_file_path: Path to local video file
            description: Video description
            tags: List of tags

        Returns:
            Ingest job data
        """
        # 1. Create video object
        video = self.create_video(
            name=video_name,
            description=description,
            tags=tags
        )
        video_id = video["id"]

        # 2. Get upload URL
        upload_info = self.get_upload_url(video_id)
        upload_url = upload_info["upload_endpoint"]

        # 3. Upload file
        self.upload_file_to_url(upload_url, video_file_path)

        # 4. Ingest from blob storage
        video_source = upload_info["video_source"]
        ingest_result = self.ingest_media(video_id, video_source)

        return {
            "video_id": video_id,
            "video": video,
            "ingest": ingest_result
        }

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BrightcoveAuthError("Authentication failed - token expired")
        elif error.response.status_code == 403:
            raise BrightcoveAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 404:
            raise BrightcoveAPIError("Resource not found")
        elif error.response.status_code == 429:
            raise BrightcoveRateLimitError("Rate limit exceeded")
        else:
            try:
                error_data = error.response.json()
                raise BrightcoveAPIError(f"API error: {error_data}")
            except:
                raise BrightcoveAPIError(f"HTTP {error.response.status_code}: {error.response.text}")