"""
Zoho Cliq API Client

Supports:
- Send messages
- List channels
- Get user information
- File upload
"""

import requests
from typing import Optional, Dict, Any, List


class ZohoCliqClient:
    """
    Zoho Cliq client for team communication.

    Authentication: OAuth Token
    Base URL: https://cliq.zoho.com/api/v2
    """

    def __init__(self, oauth_token: str):
        """
        Initialize Zoho Cliq client.

        Args:
            oauth_token: Zoho OAuth Token
        """
        self.oauth_token = oauth_token
        self.base_url = "https://cliq.zoho.com/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {oauth_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_message(
        self,
        chat_id: str,
        message: str,
        message_format: str = "text"
    ) -> Dict[str, Any]:
        """
        Send message to a chat.

        Args:
            chat_id: Chat ID or user ID
            message: Message content
            message_format: Format of message (text, markdown, html)

        Returns:
            Dict containing message details
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        data = {
            "chat_id": chat_id,
            "message": message,
            "message_format": message_format
        }

        return self._request("POST", "message", data=data)

    def send_channel_message(
        self,
        channel_name: str,
        message: str,
        message_format: str = "text"
    ) -> Dict[str, Any]:
        """
        Send message to a channel.

        Args:
            channel_name: Channel name
            message: Message content
            message_format: Format of message

        Returns:
            Dict containing message details
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        data = {
            "channel_name": channel_name,
            "message": message,
            "message_format": message_format
        }

        return self._request("POST", "channel/message", data=data)

    def list_channels(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List user's channels.

        Args:
            limit: Maximum number of channels

        Returns:
            List of channels
        """
        params = {"limit": limit}
        result = self._request("GET", "channels", params=params)
        return result.get("channels", [])

    def get_channel_detail(self, channel_id: str) -> Dict[str, Any]:
        """
        Get channel details.

        Args:
            channel_id: Channel ID

        Returns:
            Dict with channel information
        """
        return self._request("GET", f"channels/{channel_id}")

    def get_user_info(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user information.

        Args:
            user_id: User ID (optional, defaults to current user)

        Returns:
            Dict with user information
        """
        endpoint = "users/profile" if user_id else "users/me"
        return self._request("GET", endpoint)

    def upload_file(
        self,
        chat_id: str,
        file_path: str,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload file to chat.

        Args:
            chat_id: Chat ID
            file_path: Path to file to upload
            message: Optional message with file

        Returns:
            Dict with upload result
        """
        url = f"{self.base_url}/message/file"

        try:
            with open(file_path, 'rb') as file:

                files = {'file': file}
                data = {'chat_id': chat_id}
                if message:
                    data['message'] = message

                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    headers={
                        "Authorization": f"Zoho-oauthtoken {self.oauth_token}"
                    }
                )
                response.raise_for_status()
                return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Upload failed: {str(e)}")
        except IOError as e:
            raise Exception(f"File error: {str(e)}")

    def create_channel(
        self,
        channel_name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a channel.

        Args:
            channel_name: Channel name
            description: Channel description

        Returns:
            Dict with channel details
        """
        data = {"channel_name": channel_name}
        if description:
            data["description"] = description

        return self._request("POST", "channels", data=data)

    def get_unread_count(self) -> Dict[str, Any]:
        """
        Get unread message count.

        Returns:
            Dict with unread count information
        """
        return self._request("GET", "messages/unread/count")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    oauth_token = "your_zoho_oauth_token"

    client = ZohoCliqClient(oauth_token=oauth_token)

    try:
        # Get user info
        user = client.get_user_info()
        print(f"User: {user}")

        # List channels
        channels = client.list_channels()
        print(f"Channels: {channels}")

        # Send message to a user
        result = client.send_message(
            chat_id="user_123",
            message="Hello from Zoho Cliq API!"
        )
        print(f"Message sent: {result}")

        # Send message to channel
        result = client.send_channel_message(
            channel_name="general",
            message="Hello channel!",
            message_format="text"
        )
        print(f"Channel message sent: {result}")

        # Get unread count
        unread = client.get_unread_count()
        print(f"Unread: {unread}")

        # Create channel
        result = client.create_channel(
            channel_name="new-channel",
            description="A new channel"
        )
        print(f"Channel created: {result}")

        # Upload file
        try:
            result = client.upload_file(
                chat_id="user_123",
                file_path="/path/to/file.jpg",
                message="Here's the file"
            )
            print(f"File uploaded: {result}")
        except Exception as e:
            print(f"Upload skipped: {e}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()