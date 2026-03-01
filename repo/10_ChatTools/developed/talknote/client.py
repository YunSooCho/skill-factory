"""
Talknote API Client

Supports:
- スレッドにメッセージを投稿 (Post message to thread)
- ノートへメッセージを投稿 (Post message to note)
"""

import requests
from typing import Optional, Dict, Any


class TalknoteClient:
    """
    Talknote API client for messaging operations.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.talknote.com/v1
    """

    BASE_URL = "https://api.talknote.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Talknote API client.

        Args:
            api_key: Talknote API Key
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

    def post_message_to_thread(
        self,
        thread_id: str,
        message: str,
        mention_user_ids: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Post a message to a thread.

        Args:
            thread_id: Thread ID
            message: Message content (required)
            mention_user_ids: Optional list of user IDs to mention

        Returns:
            Dict containing posted message details

        Raises:
            ValueError: If message is empty
            Exception: If API request fails
        """
        if not message or not message.strip():
            raise ValueError("Message content cannot be empty")

        payload: Dict[str, Any] = {
            "thread_id": thread_id,
            "message": message
        }

        if mention_user_ids:
            payload["mentions"] = mention_user_ids

        return self._request("POST", "/threads/messages", json=payload)

    def post_message_to_note(
        self,
        note_id: str,
        message: str,
        mention_user_ids: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Post a message to a note.

        Args:
            note_id: Note ID
            message: Message content (required)
            mention_user_ids: Optional list of user IDs to mention

        Returns:
            Dict containing posted message details

        Raises:
            ValueError: If message is empty
            Exception: If API request fails
        """
        if not message or not message.strip():
            raise ValueError("Message content cannot be empty")

        payload: Dict[str, Any] = {
            "note_id": note_id,
            "message": message
        }

        if mention_user_ids:
            payload["mentions"] = mention_user_ids

        return self._request("POST", "/notes/messages", json=payload)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_talknote_api_key"

    client = TalknoteClient(api_key=api_key)

    try:
        # Post message to thread
        result = client.post_message_to_thread(
            thread_id="thread123",
            message="This is a message to the thread."
        )
        print(f"Thread message posted: {result}")

        # Post message to thread with mentions
        result = client.post_message_to_thread(
            thread_id="thread123",
            message="@user1 Please check this.",
            mention_user_ids=["user1", "user2"]
        )
        print(f"Thread message with mentions posted: {result}")

        # Post message to note
        result = client.post_message_to_note(
            note_id="note456",
            message="This is a message to the note."
        )
        print(f"Note message posted: {result}")

        # Post message to note with mentions
        result = client.post_message_to_note(
            note_id="note456",
            message="@team Important update!",
            mention_user_ids=["user1", "user2", "user3"]
        )
        print(f"Note message with mentions posted: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()