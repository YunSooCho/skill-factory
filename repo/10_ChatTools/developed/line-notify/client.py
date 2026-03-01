"""
Line Notify API Client

Supports:
- Send message to talk room with image
- Send message to talk room
"""

import requests
from typing import Optional, Dict, Any
import os


class LineNotifyClient:
    """
    Line Notify API client for sending notifications.

    Authentication: API Token (Header: Authorization: Bearer {token})
    API Docs: https://notify-bot.line.me/doc/en/
    """

    API_URL = "https://notify-api.line.me/api/notify"

    def __init__(self, access_token: str):
        """
        Initialize Line Notify client.

        Args:
            access_token: Line Notify Access Token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}"
        })

    def _request(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"https://notify-api.line.me{endpoint}"

        try:
            response = self.session.request("POST", url, **kwargs)

            if response.status_code == 200:
                if response.content:
                    return response.json()
                return {"status": "success"}
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid access token")
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                raise Exception(f"Bad request: {error_data.get('message', 'Invalid request')}")
            elif response.status_code == 404:
                raise Exception("API endpoint not found")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_message_with_image(
        self,
        message: str,
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        sticker_package_id: Optional[int] = None,
        sticker_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send message with image to Line Notify.

        Args:
            message: Text message to send (required)
            image_path: Local path to image file (optional)
            image_url: URL of image file (optional)
            sticker_package_id: Sticker package ID (optional)
            sticker_id: Sticker ID (optional)

        Returns:
            Response dict with status

        Raises:
            ValueError: If message is empty
            Exception: If API request fails
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        form_data = {"message": message}

        files = None
        if image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            files = {"imageFile": open(image_path, "rb")}
        elif image_url:
            form_data["imageThumbnail"] = image_url
            form_data["imageFullsize"] = image_url

        if sticker_package_id and sticker_id:
            form_data["stickerPackageId"] = str(sticker_package_id)
            form_data["stickerId"] = str(sticker_id)

        result = self._request("/api/notify", data=form_data, files=files)

        if files:
            files["imageFile"].close()

        return result

    def send_message(
        self,
        message: str,
        sticker_package_id: Optional[int] = None,
        sticker_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send message to Line Notify.

        Args:
            message: Text message to send (required)
            sticker_package_id: Sticker package ID (optional)
            sticker_id: Sticker ID (optional)

        Returns:
            Response dict with status

        Raises:
            ValueError: If message is empty
            Exception: If API request fails
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        form_data = {"message": message}

        if sticker_package_id and sticker_id:
            form_data["stickerPackageId"] = str(sticker_package_id)
            form_data["stickerId"] = str(sticker_id)

        return self._request("/api/notify", data=form_data)

    def get_status(self) -> Dict[str, Any]:
        """
        Get connection status.

        Returns:
            Dict with status information
        """
        url = "https://notify-api.line.me/api/status"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get status: {response.status_code}")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    access_token = "your_line_notify_token"

    client = LineNotifyClient(access_token=access_token)

    try:
        # Send text message
        result = client.send_message("Hello from Line Notify!")
        print(f"Message sent: {result}")

        # Send message with sticker
        result = client.send_message(
            "Hello with sticker!",
            sticker_package_id=1,
            sticker_id=1
        )
        print(f"Sticker message sent: {result}")

        # Send message with image (from URL)
        result = client.send_message_with_image(
            "Hello with image!",
            image_url="https://example.com/image.jpg"
        )
        print(f"Message with image sent: {result}")

        # Send message with image (from local file)
        # result = client.send_message_with_image(
        #     "Hello with local image!",
        #     image_path="/path/to/image.jpg"
        # )
        # print(f"Message with local image sent: {result}")

        # Get status
        status = client.get_status()
        print(f"Status: {status}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()