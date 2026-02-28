"""
TwoChat API Client

Supports:
- Send messages
- List conversations
- Get conversation history
"""

import requests
from typing import Optional, Dict, Any, List


class TwoChatClient:
    """
    TwoChat client for messaging operations.

    Authentication: API Key
    Base URL: https://api.twochat.com/v1
    """

    def __init__(self, api_key: str):
        """
        Initialize TwoChat API client.

        Args:
            api_key: TwoChat API Key
        """
        self.api_key = api_key
        self.base_url = "https://api.twochat.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
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
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_message(
        self,
        recipient_id: str,
        message: str,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Send message to a recipient.

        Args:
            recipient_id: Recipient ID
            message: Message content
            message_type: Type of message (text, image, file)

        Returns:
            Dict containing sent message details
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        data = {
            "recipient_id": recipient_id,
            "message": message,
            "message_type": message_type
        }

        return self._request("POST", "messages/send", data=data)

    def list_conversations(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all conversations.

        Args:
            limit: Maximum number of conversations
            offset: Offset for pagination

        Returns:
            List of conversations
        """
        params = {"limit": limit, "offset": offset}
        result = self._request("GET", "conversations", params=params)
        return result.get("conversations", [])

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get conversation message history.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages

        Returns:
            List of messages
        """
        params = {"limit": limit}
        result = self._request("GET", f"conversations/{conversation_id}/messages", params=params)
        return result.get("messages", [])

    def create_conversation(self, participant_ids: List[str]) -> Dict[str, Any]:
        """
        Create a new conversation.

        Args:
            participant_ids: List of participant IDs

        Returns:
            Dict with conversation details
        """
        data = {"participant_ids": participant_ids}
        return self._request("POST", "conversations", data=data)

    def mark_message_read(self, message_id: str) -> Dict[str, Any]:
        """
        Mark a message as read.

        Args:
            message_id: Message ID

        Returns:
            Dict with result
        """
        return self._request("PUT", f"messages/{message_id}/read")

    def delete_message(self, message_id: str) -> Dict[str, Any]:
        """
        Delete a message.

        Args:
            message_id: Message ID

        Returns:
            Dict with result
        """
        return self._request("DELETE", f"messages/{message_id}")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_twochat_api_key"

    client = TwoChatClient(api_key=api_key)

    try:
        # List conversations
        conversations = client.list_conversations()
        print(f"Conversations: {conversations}")

        # Create conversation
        result = client.create_conversation(["user1", "user2"])
        print(f"Conversation created: {result}")

        # Send message
        if conversations:
            recipient_id = conversations[0]["participant_id"]
            result = client.send_message(
                recipient_id=recipient_id,
                message="Hello from TwoChat API!"
            )
            print(f"Message sent: {result}")

        # Get conversation history
        if conversations:
            conversation_id = conversations[0]["id"]
            messages = client.get_conversation_history(conversation_id)
            print(f"History: {messages}")

        # Mark message as read
        result = client.mark_message_read("message_123")
        print(f"Marked read: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()