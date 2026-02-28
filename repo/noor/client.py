"""
Noor API Client

Supports:
- Get Members
- Post Message
"""

import requests
from typing import Optional, Dict, Any, List


class NoorClient:
    """
    Noor API client for messaging operations.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.noor.com/v1
    """

    BASE_URL = "https://api.noor.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Noor API client.

        Args:
            api_key: Noor API Key
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

    def get_members(
        self,
        group_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get list of members.

        Args:
            group_id: Optional group ID to filter members
            limit: Number of results to return (default: 50)
            offset: Pagination offset (default: 0)

        Returns:
            Dict containing members list

        Raises:
            Exception: If API request fails
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if group_id:
            params["group_id"] = group_id

        return self._request("GET", "/members", params=params)

    def post_message(
        self,
        chat_id: str,
        text: str,
        mention_user_ids: Optional[List[str]] = None,
        reply_to_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a message to a chat.

        Args:
            chat_id: Chat ID
            text: Message text to post (required)
            mention_user_ids: Optional list of user IDs to mention
            reply_to_message_id: Optional message ID to reply to

        Returns:
            Dict containing posted message details

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

        if mention_user_ids:
            payload["mentions"] = mention_user_ids

        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id

        return self._request("POST", "/messages", json=payload)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_noor_api_key"

    client = NoorClient(api_key=api_key)

    try:
        # Get all members
        members = client.get_members(limit=20)
        print(f"Members: {members}")

        # Get members of a specific group
        group_members = client.get_members(group_id="group123", limit=10)
        print(f"Group Members: {group_members}")

        # Post a simple message
        result = client.post_message(
            chat_id="chat123",
            text="Hello from Noor API!"
        )
        print(f"Message posted: {result}")

        # Post message with mentions
        result = client.post_message(
            chat_id="chat123",
            text="Hello @user1 and @user2!",
            mention_user_ids=["user1", "user2"]
        )
        print(f"Message with mentions posted: {result}")

        # Post reply message
        result = client.post_message(
            chat_id="chat123",
            text="This is a reply",
            reply_to_message_id="msg456"
        )
        print(f"Reply posted: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()