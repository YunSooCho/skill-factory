"""
Wamm App API Client

Supports:
- Send WhatsApp messages
- Send media messages
- Check message status
"""

import requests
from typing import Optional, Dict, Any, List


class WammAppClient:
    """
    Wamm App client for WhatsApp messaging.

    Authentication: API Token
    Base URL: https://app.wamm.chat/api
    """

    def __init__(self, api_token: str):
        """
        Initialize Wamm App client.

        Args:
            api_token: Wamm App API Token
        """
        self.api_token = api_token
        self.base_url = "https://app.wamm.chat/api"
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
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_text_message(
        self,
        phone_number: str,
        message: str,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Send text message via WhatsApp.

        Args:
            phone_number: Recipient phone number (with country code)
            message: Message content
            priority: Message priority (low, normal, high)

        Returns:
            Dict containing message details
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        data = {
            "phone_number": phone_number,
            "type": "text",
            "content": message,
            "priority": priority
        }

        return self._request("POST", "send", data=data)

    def send_media_message(
        self,
        phone_number: str,
        media_url: str,
        media_type: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send media message (image, video, document).

        Args:
            phone_number: Recipient phone number
            media_url: URL of the media file
            media_type: Type of media (image, video, document)
            caption: Optional caption for the media

        Returns:
            Dict containing message details
        """
        data = {
            "phone_number": phone_number,
            "type": media_type,
            "content": media_url
        }

        if caption:
            data["caption"] = caption

        return self._request("POST", "send", data=data)

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get message delivery status.

        Args:
            message_id: Message ID

        Returns:
            Dict with message status
        """
        return self._request("GET", f"messages/{message_id}/status")

    def list_messages(
        self,
        phone_number: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List sent messages.

        Args:
            phone_number: Filter by phone number
            limit: Maximum number of messages
            offset: Pagination offset

        Returns:
            List of messages
        """
        params = {"limit": limit, "offset": offset}
        if phone_number:
            params["phone_number"] = phone_number

        result = self._request("GET", "messages", params=params)
        return result.get("messages", [])

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.

        Returns:
            Dict with account details
        """
        return self._request("GET", "account")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_wamm_api_token"

    client = WammAppClient(api_token=api_token)

    try:
        # Get account info
        account = client.get_account_info()
        print(f"Account: {account}")

        # Send text message
        result = client.send_text_message(
            phone_number="+1234567890",
            message="Hello from Wamm App API!"
        )
        print(f"Message sent: {result}")

        # Send image
        result = client.send_media_message(
            phone_number="+1234567890",
            media_url="https://example.com/image.jpg",
            media_type="image",
            caption="Check this image!"
        )
        print(f"Image sent: {result}")

        # Check message status
        message_id = result.get("message_id")
        if message_id:
            status = client.get_message_status(message_id)
            print(f"Message status: {status}")

        # List messages
        messages = client.list_messages(limit=10)
        print(f"Messages: {messages}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()