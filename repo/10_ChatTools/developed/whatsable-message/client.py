"""
Whatsable Message API Client

Supports:
- Send messages
- Send bulk messages
- Get delivery status
- Account management
"""

import requests
from typing import Optional, Dict, Any, List


class WhatsableMessageClient:
    """
    Whatsable Message client for WhatsApp messaging.

    Authentication: API Key
    Base URL: https://api.whatsable.com/v1
    """

    def __init__(self, api_key: str):
        """
        Initialize Whatsable Message client.

        Args:
            api_key: Whatsable Message API Key
        """
        self.api_key = api_key
        self.base_url = "https://api.whatsable.com/v1"
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
        phone_number: str,
        message: str,
        message_type: str = "text",
        media_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message via WhatsApp.

        Args:
            phone_number: Recipient phone number
            message: Message content
            message_type: Type of message (text, image, video, document)
            media_url: URL for media messages

        Returns:
            Dict containing message details
        """
        if message_type == "text" and not message:
            raise ValueError("Message cannot be empty")
        if message_type != "text" and not media_url:
            raise ValueError("Media URL required for media messages")

        data = {
            "phone_number": phone_number,
            "type": message_type
        }

        if message:
            data["content"] = message
        if media_url:
            data["media_url"] = media_url

        return self._request("POST", "messages/send", data=data)

    def send_bulk_messages(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Send bulk messages.

        Args:
            messages: List of message dictionaries

        Returns:
            Dict containing batch results
        """
        data = {"messages": messages}
        return self._request("POST", "messages/bulk", data=data)

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get message delivery status.

        Args:
            message_id: Message ID

        Returns:
            Dict with message status
        """
        return self._request("GET", f"messages/{message_id}/status")

    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance.

        Returns:
            Dict with balance information
        """
        return self._request("GET", "account/balance")

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.

        Returns:
            Dict with account details
        """
        return self._request("GET", "account")

    def list_messages(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        List sent messages.

        Args:
            date_from: Filter by start date (YYYY-MM-DD)
            date_to: Filter by end date (YYYY-MM-DD)
            limit: Maximum number of messages

        Returns:
            List of messages
        """
        params = {"limit": limit}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        result = self._request("GET", "messages", params=params)
        return result.get("messages", [])

    def cancel_message(self, message_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled message.

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
    api_key = "your_whatsable_api_key"

    client = WhatsableMessageClient(api_key=api_key)

    try:
        # Get account info
        account = client.get_account_info()
        print(f"Account: {account}")

        # Check balance
        balance = client.get_account_balance()
        print(f"Balance: {balance}")

        # Send text message
        result = client.send_message(
            phone_number="+1234567890",
            message="Hello from Whatsable API!",
            message_type="text"
        )
        print(f"Message sent: {result}")

        # Send image
        result = client.send_message(
            phone_number="+1234567890",
            message_type="image",
            media_url="https://example.com/image.jpg"
        )
        print(f"Image sent: {result}")

        # Send bulk messages
        bulk_messages = [
            {"phone_number": "+1234567890", "type": "text", "content": "Message 1"},
            {"phone_number": "+0987654321", "type": "text", "content": "Message 2"}
        ]
        result = client.send_bulk_messages(bulk_messages)
        print(f"Bulk sent: {result}")

        # Check status
        message_id = result.get("message_id")
        if message_id:
            status = client.get_message_status(message_id)
            print(f"Status: {status}")

        # List messages
        messages = client.list_messages(limit=10)
        print(f"Messages: {messages}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()