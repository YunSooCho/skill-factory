"""
Twist API Client

Supports:
- Send messages
- List channels
- Search messages
"""

import requests
from typing import Optional, Dict, Any, List


class TwistClient:
    """
    Twist client for messaging operations.

    Authentication: API Token
    Base URL: https://api.twist.com/api/v3
    """

    def __init__(self, api_token: str):
        """
        Initialize Twist API client.

        Args:
            api_token: Twist API Token
        """
        self.api_token = api_token
        self.base_url = "https://api.twist.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
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
        content: str,
        conversation_id: int,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send message to a conversation.

        Args:
            content: Message content
            conversation_id: Target conversation ID
            attachments: List of attachment URLs

        Returns:
            Dict containing sent message details
        """
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        data = {
            "content": content,
            "conversation_id": conversation_id
        }

        if attachments:
            data["attachments"] = attachments

        return self._request("POST", "messages/add", data=data)

    def list_channels(self, workspace_id: int) -> List[Dict[str, Any]]:
        """
        List channels in a workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            List of channels
        """
        result = self._request("GET", f"workspaces/{workspace_id}/channels/list")
        return result.get("channels", [])

    def list_conversations(self, channel_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List conversations in a channel.

        Args:
            channel_id: Channel ID
            limit: Maximum number of conversations

        Returns:
            List of conversations
        """
        params = {"limit": limit}
        result = self._request("GET", f"channels/{channel_id}/conversations/list", params=params)
        return result.get("conversations", [])

    def search_messages(self, query: str, workspace_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search messages.

        Args:
            query: Search query
            workspace_id: Workspace ID (optional)

        Returns:
            List of messages
        """
        params = {"query": query}
        if workspace_id:
            params["workspace_id"] = workspace_id

        result = self._request("GET", "messages/search", params=params)
        return result.get("messages", [])

    def get_thread(self, thread_id: int) -> Dict[str, Any]:
        """
        Get thread details.

        Args:
            thread_id: Thread ID

        Returns:
            Dict with thread information
        """
        return self._request("GET", f"threads/get/{thread_id}")

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """
        List user's workspaces.

        Returns:
            List of workspaces
        """
        result = self._request("GET", "workspaces/list")
        return result.get("workspaces", [])

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_twist_api_token"

    client = TwistClient(api_token=api_token)

    try:
        # List workspaces
        workspaces = client.list_workspaces()
        print(f"Workspaces: {workspaces}")

        # List channels in a workspace
        workspace_id = 12345
        channels = client.list_channels(workspace_id)
        print(f"Channels: {channels}")

        # List conversations
        channel_id = 67890
        conversations = client.list_conversations(channel_id)
        print(f"Conversations: {conversations}")

        # Send message
        if conversations:
            conversation_id = conversations[0]["id"]
            result = client.send_message(
                content="Hello from Twist API!",
                conversation_id=conversation_id
            )
            print(f"Message sent: {result}")

        # Search messages
        messages = client.search_messages("search query", workspace_id)
        print(f"Search results: {messages}")

        # Get thread
        thread_id = 11111
        thread = client.get_thread(thread_id)
        print(f"Thread: {thread}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()