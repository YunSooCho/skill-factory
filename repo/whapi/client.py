"""
Whapi API Client

Supports:
- Send messages
- Send templates
- Check message status
- Webhook management
"""

import requests
from typing import Optional, Dict, Any, List


class WhapiClient:
    """
    Whapi client for WhatsApp messaging.

    Authentication: API Token
    Base URL: https://wa.me/api/v1
    """

    def __init__(self, api_token: str):
        """
        Initialize Whapi client.

        Args:
            api_token: Whapi API Token
        """
        self.api_token = api_token
        self.base_url = "https://wa.me/api/v1"
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
        preview_url: bool = False
    ) -> Dict[str, Any]:
        """
        Send message via WhatsApp.

        Args:
            phone_number: Recipient phone number
            message: Message content
            preview_url: Whether to generate link previews

        Returns:
            Dict containing message details
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        data = {
            "phone_number": phone_number,
            "type": "text",
            "text": message,
            "preview_url": preview_url
        }

        return self._request("POST", "messages", data=data)

    def send_template(
        self,
        phone_number: str,
        template_name: str,
        template_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send WhatsApp template message.

        Args:
            phone_number: Recipient phone number
            template_name: Template name
            template_params: Template parameters

        Returns:
            Dict containing message details
        """
        data = {
            "phone_number": phone_number,
            "type": "template",
            "template_name": template_name
        }

        if template_params:
            data["template_params"] = template_params

        return self._request("POST", "messages", data=data)

    def send_file(
        self,
        phone_number: str,
        file_url: str,
        file_type: str = "document",
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send file message.

        Args:
            phone_number: Recipient phone number
            file_url: URL of the file
            file_type: Type of file (image, video, document, audio)
            caption: Optional caption

        Returns:
            Dict containing message details
        """
        data = {
            "phone_number": phone_number,
            "type": file_type,
            "media_url": file_url
        }

        if caption:
            data["caption"] = caption

        return self._request("POST", "messages", data=data)

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get message status.

        Args:
            message_id: Message ID

        Returns:
            Dict with message status
        """
        return self._request("GET", f"messages/{message_id}")

    def list_messages(
        self,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List messages.

        Args:
            limit: Maximum number of messages
            skip: Number of messages to skip

        Returns:
            List of messages
        """
        params = {"limit": limit, "skip": skip}
        result = self._request("GET", "messages", params=params)
        return result.get("messages", [])

    def set_webhook(self, webhook_url: str, webhook_events: List[str]) -> Dict[str, Any]:
        """
        Set webhook.

        Args:
            webhook_url: Webhook URL
            webhook_events: List of events to subscribe to

        Returns:
            Dict with webhook details
        """
        data = {
            "webhook_url": webhook_url,
            "webhook_events": webhook_events
        }
        return self._request("POST", "webhook", data=data)

    def delete_webhook(self) -> Dict[str, Any]:
        """Delete webhook"""
        return self._request("DELETE", "webhook")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_whapi_token"

    client = WhapiClient(api_token=api_token)

    try:
        # Send message
        result = client.send_message(
            phone_number="+1234567890",
            message="Hello from Whapi API!"
        )
        print(f"Message sent: {result}")

        # Send template
        result = client.send_template(
            phone_number="+1234567890",
            template_name="welcome_template",
            template_params={"name": "John"}
        )
        print(f"Template sent: {result}")

        # Send file
        result = client.send_file(
            phone_number="+1234567890",
            file_url="https://example.com/file.pdf",
            file_type="document",
            caption="Here's your file"
        )
        print(f"File sent: {result}")

        # Check status
        message_id = result.get("message_id")
        if message_id:
            status = client.get_message_status(message_id)
            print(f"Status: {status}")

        # List messages
        messages = client.list_messages(limit=10)
        print(f"Messages: {messages}")

        # Set webhook
        result = client.set_webhook(
            webhook_url="https://yourwebhook.com",
            webhook_events=["messages", "delivery"]
        )
        print(f"Webhook set: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()