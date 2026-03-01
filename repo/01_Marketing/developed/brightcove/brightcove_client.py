"""
Brightcove API Client
Video Cloud CMS API and Dynamic Ingest API
"""

import requests
from typing import Dict, Optional, Any, List
import time
import json


def get_access_token(client_id: str, client_secret: str, account_id: str) -> str:
    """
    Get OAuth access token for Brightcove API

    Args:
        client_id: Brightcove OAuth client ID
        client_secret: Brightcove OAuth client secret
        account_id: Brightcove account ID

    Returns:
        Access token string
    """
    auth_url = f"https://oauth.brightcove.com/v4/access_token"

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(auth_url, data=data)
    response.raise_for_status()

    return response.json()['access_token']


class BrightcoveClient:
    """Brightcove Video Cloud API Client"""

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
        self.base_url = f"https://cms.api.brightcove.com/v1/accounts/{account_id}"
        self.ingest_url = f"https://ingest.api.brightcove.com/v1/accounts/{account_id}"
        self.timeout = 30
        self.token_expires_at = 0

    def _refresh_token(self):
        """Refresh access token if needed"""
        if self.access_token and time.time() < self.token_expires_at:
            return

        self.access_token = get_access_token(self.client_id, self.client_secret, self.account_id)
        self.token_expires_at = time.time() + 3000  # Token valid for ~50 minutes

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with access token"""
        self._refresh_token()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Authentication failed - check credentials")
        elif response.status_code == 403:
            raise ValueError("Access forbidden - insufficient permissions")
        elif response.status_code == 404:
            raise ValueError("Resource not found")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def list_videos(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str = None,
        sort: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get list of videos

        Args:
            limit: Number of videos to return (max 100)
            offset: Offset for pagination
            search: Search query string
            sort: Sort field (e.g., 'updated_at', 'created_at', 'plays_total')

        Returns:
            List of video dictionaries
        """
        url = f"{self.base_url}/videos"

        params = {
            'limit': min(limit, 100),
            'offset': offset
        }

        if search:
            params['q'] = search
        if sort:
            params['sort'] = sort

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to list videos: {str(e)}")

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """
        Get video by ID

        Args:
            video_id: Video ID

        Returns:
            Video dictionary
        """
        url = f"{self.base_url}/videos/{video_id}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get video: {str(e)}")

    def create_video(
        self,
        name: str,
        description: str = None,
        tags: List[str] = None,
        state: str = "ACTIVE"
    ) -> Dict[str, Any]:
        """
        Create video object (without uploading)

        Args:
            name: Video name
            description: Video description
            tags: List of tags
            state: Video state (ACTIVE, INACTIVE, DRAFT)

        Returns:
            Created video dictionary containing video ID and ingest URLs
        """
        url = f"{self.base_url}/videos"

        video_data = {
            'name': name,
            'state': state
        }

        if description:
            video_data['description'] = description
        if tags:
            video_data['tags'] = tags

        try:
            response = requests.post(url, json=video_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to create video: {str(e)}")

    def update_video(
        self,
        video_id: str,
        name: str = None,
        description: str = None,
        tags: List[str] = None,
        state: str = None
    ) -> Dict[str, Any]:
        """
        Update video metadata

        Args:
            video_id: Video ID
            name: New video name (optional)
            description: New description (optional)
            tags: New tags (optional)
            state: New state (optional)

        Returns:
            Updated video dictionary
        """
        url = f"{self.base_url}/videos/{video_id}"

        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description
        if tags is not None:
            update_data['tags'] = tags
        if state is not None:
            update_data['state'] = state

        try:
            response = requests.patch(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update video: {str(e)}")

    def get_upload_url(
        self,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Get temporary upload URL for video file

        Args:
            video_id: Video ID

        Returns:
            Dictionary with:
                - URL: Signed upload URL
                - api_request_url: API request URL for the video
                - video_id: Video ID
        """
        url = f"{self.base_url}/videos/{video_id}/upload-urls/mp4"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get upload URL: {str(e)}")

    def upload_video_file(
        self,
        upload_url: str,
        file_path: str
    ) -> bool:
        """
        Upload video file to signed upload URL

        Args:
            upload_url: Signed upload URL from get_upload_url()
            file_path: Path to video file

        Returns:
            True if upload succeeded
        """
        try:
            with open(file_path, 'rb') as f:
                response = requests.put(upload_url, data=f, timeout=300)

            if response.status_code in [200, 201]:
                return True
            else:
                raise ValueError(f"Upload failed with status {response.status_code}: {response.text}")
        except IOError as e:
            raise ValueError(f"Failed to read file: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Upload failed: {str(e)}")

    def ingest_media(
        self,
        video_id: str,
        video_url: str = None,
        file_location: str = None,
        master_url: str = None
    ) -> Dict[str, Any]:
        """
        Ingest media into Brightcove

        Args:
            video_id: Video ID
            video_url: URL of video file (optional)
            file_location: File location reference (optional)
            master_url: Master URL for cloud storage (optional)

        Returns:
            Ingest job response
        """
        url = f"{self.ingest_url}/videos/{video_id}/ingest-requests"

        ingest_data = {}

        if video_url:
            ingest_data['video_url'] = video_url
        if file_location:
            ingest_data['file_location'] = file_location
        if master_url:
            ingest_data['master-url'] = master_url

        # Add profile for default transcoding
        ingest_data['profile'] = 'multi-platform-standard-static'

        try:
            response = requests.post(url, json=ingest_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to ingest media: {str(e)}")

    def delete_video(self, video_id: str) -> bool:
        """
        Delete video

        Args:
            video_id: Video ID

        Returns:
            True if deleted successfully
        """
        url = f"{self.base_url}/videos/{video_id}"

        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            if response.status_code == 204:
                return True
            raise ValueError(f"Delete failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to delete video: {str(e)}")


# CLI Example
if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 4:
        print("Usage:")
        print("  List videos: python brightcove_client.py list <account_id> <client_id> <client_secret>")
        print("  Get video: python brightcove_client.py get <account_id> <client_id> <client_secret> <video_id>")
        print("  Create video: python brightcove_client.py create <account_id> <client_id> <client_secret> <name>")
        print("  Update video: python brightcove_client.py update <account_id> <client_id> <client_secret> <video_id> <name>")
        print("  Get upload URL: python brightcove_client.py upload-url <account_id> <client_id> <client_secret> <video_id>")
        print("  Ingest media: python brightcove_client.py ingest <account_id> <client_id> <client_secret> <video_id> <video_url>")
        print("  Upload file: python brightcove_client.py upload-file <account_id> <client_id> <client_secret> <video_id> <file_path>")
        print("  Delete video: python brightcove_client.py delete <account_id> <client_id> <client_secret> <video_id>")
        sys.exit(1)

    command = sys.argv[1]
    account_id = sys.argv[2]
    client_id = sys.argv[3]
    client_secret = sys.argv[4]

    client = BrightcoveClient(account_id, client_id, client_secret)

    if command == "list":
        videos = client.list_videos()
        print(f"Total videos: {len(videos)}")
        for video in videos:
            print(f"  - {video.get('id')}: {video.get('name')}")

    elif command == "get":
        video_id = sys.argv[5]
        video = client.get_video(video_id)
        print(f"Video ID: {video.get('id')}")
        print(f"Name: {video.get('name')}")
        print(f"Description: {video.get('description', 'N/A')}")
        print(f"State: {video.get('state')}")
        print(f"Duration: {video.get('duration')} ms")
        print(f"Tags: {', '.join(video.get('tags', []))}")

    elif command == "create":
        name = sys.argv[5]
        video = client.create_video(name)
        print(f"Video created:")
        print(f"  ID: {video.get('id')}")
        print(f"  Name: {video.get('name')}")

    elif command == "update":
        video_id = sys.argv[5]
        name = sys.argv[6] if len(sys.argv) > 6 else None
        video = client.update_video(video_id, name=name)
        print(f"Video updated: {video.get('id')}")

    elif command == "upload-url":
        video_id = sys.argv[5]
        upload_info = client.get_upload_url(video_id)
        print(f"Upload URL: {upload_info.get('URL')}")
        print(f"API Request URL: {upload_info.get('api_request_url')}")
        print("You can now PUT the file to the upload URL.")

    elif command == "ingest":
        video_id = sys.argv[5]
        video_url = sys.argv[6] if len(sys.argv) > 6 else None
        result = client.ingest_media(video_id, video_url=video_url)
        print(f"Ingest job created: {result.get('id')}")

    elif command == "upload-file":
        video_id = sys.argv[5]
        file_path = sys.argv[6]
        # First get upload URL
        upload_info = client.get_upload_url(video_id)
        upload_url = upload_info.get('URL')
        # Upload file
        success = client.upload_video_file(upload_url, file_path)
        if success:
            print(f"File uploaded successfully. Trigger ingest to process.")

    elif command == "delete":
        video_id = sys.argv[5]
        success = client.delete_video(video_id)
        if success:
            print(f"Video {video_id} deleted successfully")