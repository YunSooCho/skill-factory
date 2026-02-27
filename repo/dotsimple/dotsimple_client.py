"""
Dotsimple API Client
Social media scheduling API for posts, media, accounts
"""

import requests
from typing import Dict, Optional, Any, List
import time
import json
from flask import Flask, request, jsonify


class DotsimpleClient:
    """Dotsimple API Client for social media management"""

    def __init__(self, api_key: str, base_url: str = "https://api.dotsimple.com/v1"):
        """
        Initialize Dotsimple client

        Args:
            api_key: Dotsimple API key
            base_url: Base URL for API requests
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Invalid API key or unauthorized")
        elif response.status_code == 403:
            raise ValueError("Forbidden - insufficient permissions")
        elif response.status_code == 404:
            raise ValueError("Resource not found")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    # ==================== Posts ====================

    def create_post(
        self,
        content: str,
        schedule_time: str = None,
        media_ids: List[str] = None,
        social_account_id: str = None
    ) -> Dict[str, Any]:
        """
        Create a new post

        Args:
            content: Post content
            schedule_time: Schedule time (ISO 8601 format, optional)
            media_ids: List of media file IDs (optional)
            social_account_id: Social account to post to (optional)

        Returns:
            Created post data
        """
        url = f"{self.base_url}/posts"

        post_data = {'content': content}

        if schedule_time:
            post_data['schedule_time'] = schedule_time
        if media_ids:
            post_data['media_ids'] = media_ids
        if social_account_id:
            post_data['social_account_id'] = social_account_id

        try:
            response = requests.post(url, json=post_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to create post: {str(e)}")

    def update_post(
        self,
        post_id: str,
        content: str = None,
        schedule_time: str = None,
        media_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Update post

        Args:
            post_id: Post ID
            content: New content (optional)
            schedule_time: New schedule time (optional)
            media_ids: New media IDs (optional)

        Returns:
            Updated post data
        """
        url = f"{self.base_url}/posts/{post_id}"

        update_data = {}

        if content is not None:
            update_data['content'] = content
        if schedule_time is not None:
            update_data['schedule_time'] = schedule_time
        if media_ids is not None:
            update_data['media_ids'] = media_ids

        try:
            response = requests.put(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update post: {str(e)}")

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """
        Get post by ID

        Args:
            post_id: Post ID

        Returns:
            Post data
        """
        url = f"{self.base_url}/posts/{post_id}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get post: {str(e)}")

    def list_posts(
        self,
        limit: int = 20,
        offset: int = 0,
        status: str = None
    ) -> Dict[str, Any]:
        """
        List posts

        Args:
            limit: Number of posts to return
            offset: Offset for pagination
            status: Filter by status (optional)

        Returns:
            Dict with posts list
        """
        url = f"{self.base_url}/posts"

        params = {'limit': limit, 'offset': offset}

        if status:
            params['status'] = status

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to list posts: {str(e)}")

    def schedule_post(
        self,
        post_id: str,
        schedule_time: str
    ) -> Dict[str, Any]:
        """
        Schedule post for specific time

        Args:
            post_id: Post ID
            schedule_time: Schedule time (ISO 8601 format)

        Returns:
            Scheduled post data
        """
        url = f"{self.base_url}/posts/{post_id}/schedule"

        data = {'schedule_time': schedule_time}

        try:
            response = requests.post(url, json=data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to schedule post: {str(e)}")

    def add_post_to_queue(self, post_id: str) -> Dict[str, Any]:
        """
        Add post to queue

        Args:
            post_id: Post ID

        Returns:
            Queued post data
        """
        url = f"{self.base_url}/posts/{post_id}/queue"

        try:
            response = requests.post(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to add post to queue: {str(e)}")

    # ==================== Media ====================

    def upload_media_file(
        self,
        file_path: str,
        file_type: str = None
    ) -> Dict[str, Any]:
        """
        Upload media file

        Args:
            file_path: Path to media file
            file_type: Media type (image/video/audio, optional)

        Returns:
            Uploaded media data with ID
        """
        url = f"{self.base_url}/media"

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {}

                if file_type:
                    data['type'] = file_type

                response = requests.post(url, files=files, data=data, headers=self._get_headers(), timeout=300)

            return self._handle_response(response)
        except IOError as e:
            raise ValueError(f"Failed to read file: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to upload media: {str(e)}")

    # ==================== Accounts ====================

    def list_accounts(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List social media accounts

        Args:
            limit: Number of accounts to return
            offset: Offset for pagination

        Returns:
            Dict with accounts list
        """
        url = f"{self.base_url}/accounts"

        params = {'limit': limit, 'offset': offset}

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to list accounts: {str(e)}")


class DotsimpleWebhookHandler:
    """Webhook handler for Dotsimple events"""

    @staticmethod
    def parse_webhook_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Dotsimple webhook event

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        return {
            'event_type': data.get('type'),
            'timestamp': data.get('timestamp'),
            'data': data.get('data', {})
        }

    @staticmethod
    def handle_new_account(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle new account webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed account data
        """
        account_data = data.get('data', {})
        return {
            'account_id': account_data.get('id'),
            'account_type': account_data.get('type'),
            'account_name': account_data.get('name'),
            'created_at': data.get('timestamp')
        }

    @staticmethod
    def handle_new_post(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle new post webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed post data
        """
        post_data = data.get('data', {})
        return {
            'post_id': post_data.get('id'),
            'content': post_data.get('content'),
            'schedule_time': post_data.get('schedule_time'),
            'status': post_data.get('status'),
            'created_at': data.get('timestamp')
        }

    @staticmethod
    def handle_uploaded_file(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle uploaded file webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed file data
        """
        file_data = data.get('data', {})
        return {
            'file_id': file_data.get('id'),
            'file_type': file_data.get('type'),
            'file_url': file_data.get('url'),
            'created_at': data.get('timestamp')
        }


# Flask Webhook Server Example
def create_webhook_server(webhook_secret: str = None, host: str = '0.0.0.0', port: int = 8080):
    """
    Create Flask server for Dotsimple webhooks

    Args:
        webhook_secret: Webhook secret for verification (optional)
        host: Server host
        port: Server port
    """
    app = Flask(__name__)

    @app.route('/webhook/dotsimple', methods=['POST'])
    def handle_webhook():
        """Handle Dotsimple webhook"""
        try:
            data = request.json
            event_type = data.get('type')

            if event_type == 'new_account':
                parsed = DotsimpleWebhookHandler.handle_new_account(data)
                print(f"New account: {parsed}")
            elif event_type == 'new_post':
                parsed = DotsimpleWebhookHandler.handle_new_post(data)
                print(f"New post: {parsed}")
            elif event_type == 'uploaded_file':
                parsed = DotsimpleWebhookHandler.handle_uploaded_file(data)
                print(f"Uploaded file: {parsed}")

            return jsonify({'status': 'success'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'}), 200

    app.run(host=host, port=port)


# CLI Example
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage:")
        print("  Create post: python dotsimple_client.py create <api_key> <content> [schedule_time]")
        print("  Update post: python dotsimple_client.py update <api_key> <post_id> [content] [schedule_time]")
        print("  Get post: python dotsimple_client.py get <api_key> <post_id>")
        print("  List posts: python dotsimple_client.py list <api_key>")
        print("  Schedule post: python dotsimple_client.py schedule <api_key> <post_id> <schedule_time>")
        print("  Add to queue: python dotsimple_client.py queue <api_key> <post_id>")
        print("  Upload media: python dotsimple_client.py upload <api_key> <file_path>")
        print("  List accounts: python dotsimple_client.py accounts <api_key>")
        print("  Start webhook server: python dotsimple_client.py webhook [port]")
        sys.exit(1)

    api_key = sys.argv[2]

    client = DotsimpleClient(api_key)

    if sys.argv[1] == "create":
        content = sys.argv[3]
        schedule_time = sys.argv[4] if len(sys.argv) > 4 else None
        post = client.create_post(content, schedule_time=schedule_time)
        print(f"Post created: {post}")

    elif sys.argv[1] == "update":
        post_id = sys.argv[3]
        content = sys.argv[4] if len(sys.argv) > 4 else None
        schedule_time = sys.argv[5] if len(sys.argv) > 5 else None
        post = client.update_post(post_id, content, schedule_time)
        print(f"Post updated: {post}")

    elif sys.argv[1] == "get":
        post_id = sys.argv[3]
        post = client.get_post(post_id)
        print(f"Post: {post}")

    elif sys.argv[1] == "list":
        posts = client.list_posts()
        print(f"Posts: {posts}")

    elif sys.argv[1] == "schedule":
        post_id = sys.argv[3]
        schedule_time = sys.argv[4]
        post = client.schedule_post(post_id, schedule_time)
        print(f"Post scheduled: {post}")

    elif sys.argv[1] == "queue":
        post_id = sys.argv[3]
        post = client.add_post_to_queue(post_id)
        print(f"Post added to queue: {post}")

    elif sys.argv[1] == "upload":
        file_path = sys.argv[3]
        file_type = sys.argv[4] if len(sys.argv) > 4 else None
        media = client.upload_media_file(file_path, file_type)
        print(f"Media uploaded: {media}")

    elif sys.argv[1] == "accounts":
        accounts = client.list_accounts()
        print(f"Accounts: {accounts}")

    elif sys.argv[1] == "webhook":
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        print(f"Starting webhook server on port {port}...")
        create_webhook_server(port=port)