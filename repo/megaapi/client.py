"""
MEGA API Client

Supports:
- Send Text Message
- Delete Message
"""

import requests
from typing import Optional, Dict, Any


class MegaapiClient:
    """
    MEGA API client for messaging operations.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.mega.com/v1
    """

    BASE_URL = "https://api.mega.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize MEGA API client.

        Args:
            api_key: MEGA API Key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
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
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_text_message(
        self,
        chat_id: str,
        text: str,
        reply_to_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send text message to a chat.

        Args:
            chat_id: Chat ID or user ID
            text: Message text to send (required)
            reply_to_message_id: Optional message ID to reply to

        Returns:
            Dict containing sent message details

        Raises:
            ValueError: If text is empty
            Exception: If API request fails
        """
        if not text or not text.strip():
            raise ValueError("Message text cannot be empty")

        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text
        }

        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id

        return self._request("POST", "/messages/send", json=payload)

    def delete_message(
        self,
        chat_id: str,
        message_id: str,
        for_all_users: bool = False
    ) -> Dict[str, Any]:
        """
        Delete a message.

        Args:
            chat_id: Chat ID
            message_id: Message ID to delete
            for_all_users: Whether to delete for all users (True) or just for sender (False)

        Returns:
            Dict containing deletion result

        Raises:
            Exception: If API request fails
        """
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "revoke": for_all_users
        }

        return self._request("POST", "/messages/delete", json=payload)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_megaapi_key"

    client = MegaapiClient(api_key=api_key)

    try:
        # Send text message
        result = client.send_text_message(
            chat_id="chat123",
            text="Hello from MEGA API!"
        )
        print(f"Message sent: {result}")

        # Send reply message
        result = client.send_text_message(
            chat_id="chat123",
            text="This is a reply",
            reply_to_message_id="msg456"
        )
        print(f"Reply sent: {result}")

        # Delete message (for sender only)
        result = client.delete_message(
            chat_id="chat123",
            message_id="msg456",
            for_all_users=False
        )
        print(f"Message deleted: {result}")

        # Delete message for all users
        result = client.delete_message(
            chat_id="chat123",
            message_id="msg789",
            for_all_users=True
        )
        print(f"Message deleted for all: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()