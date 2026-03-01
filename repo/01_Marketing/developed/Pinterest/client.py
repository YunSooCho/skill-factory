"""
Pinterest API Client
https://developers.pinterest.com/docs/getting-started
"""

import requests
from typing import Optional, Dict, Any, List


class PinterestClient:
    """Pinterest API Client for Yoom integration"""

    BASE_URL = "https://api.pinterest.com/v5"

    def __init__(self, access_token: str):
        """
        Initialize Pinterest client with access token

        Args:
            access_token: Pinterest OAuth access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make authenticated request to Pinterest API

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            Response JSON data

        Raises:
            Exception: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if not response.ok:
            error_msg = response.text
            raise Exception(f"Pinterest API error: {response.status_code} - {error_msg}")

        return response.json()

    def get_pin(self, pin_id: str) -> Dict[str, Any]:
        """
        Get pin details

        Args:
            pin_id: Pin ID

        Returns:
            Pin details
        """
        return self._request("GET", f"/pins/{pin_id}")

    def create_pin(
        self,
        title: str,
        description: str,
        link: str,
        board_id: str,
        image_url: str,
        alt_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a pin

        Args:
            title: Pin title
            description: Pin description
            link: Pin link URL
            board_id: Board ID to pin to
            image_url: Image URL
            alt_text: Alt text for image

        Returns:
            Created pin data
        """
        data = {
            "title": title,
            "description": description,
            "link": link,
            "board_id": board_id,
            "media_source": {
                "source_type": "image_url",
                "url": image_url,
            },
        }

        if alt_text:
            data["alt_text"] = alt_text

        return self._request("POST", "/pins", json=data)

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        Get board details

        Args:
            board_id: Board ID

        Returns:
            Board details
        """
        return self._request("GET", f"/boards/{board_id}")

    def create_board(
        self,
        name: str,
        description: Optional[str] = None,
        privacy: str = "PUBLIC",
    ) -> Dict[str, Any]:
        """
        Create a board

        Args:
            name: Board name
            description: Board description
            privacy: Board privacy (PUBLIC or SECRET)

        Returns:
            Created board data
        """
        data = {
            "name": name,
            "privacy": privacy.upper(),
        }

        if description:
            data["description"] = description

        return self._request("POST", "/boards", json=data)

    def list_pins(
        self,
        board_id: Optional[str] = None,
        pin_batch_size: int = 25,
        page_size: int = 25,
    ) -> Dict[str, Any]:
        """
        List pins

        Args:
            board_id: Optional board ID to filter pins
            pin_batch_size: Number of pins to return
            page_size: Page size

        Returns:
            List of pins
        """
        params = {
            "pin_batch_size": pin_batch_size,
            "page_size": page_size,
        }

        if board_id:
            endpoint = f"/boards/{board_id}/pins"
        else:
            endpoint = "/pins"

        return self._request("GET", endpoint, params=params)

    def update_board(
        self,
        board_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        privacy: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update board

        Args:
            board_id: Board ID
            name: New board name
            description: New board description
            privacy: New board privacy

        Returns:
            Updated board data
        """
        data = {}

        if name is not None:
            data["name"] = name

        if description is not None:
            data["description"] = description

        if privacy is not None:
            data["privacy"] = privacy.upper()

        return self._request("PATCH", f"/boards/{board_id}", json=data)

    def list_boards(
        self,
        page_size: int = 25,
        privacy: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List boards

        Args:
            page_size: Number of boards to return
            privacy: Filter by privacy (all, public, protected, secret)

        Returns:
            List of boards
        """
        params = {
            "page_size": page_size,
        }

        if privacy:
            params["privacy"] = privacy

        return self._request("GET", "/boards", params=params)


if __name__ == "__main__":
    # Example usage
    import os

    access_token = os.environ.get("PINTEREST_ACCESS_TOKEN")

    if not access_token:
        print("PINTEREST_ACCESS_TOKEN environment variable not set")
        exit(1)

    client = PinterestClient(access_token)

    try:
        # List boards
        boards = client.list_boards(page_size=10)
        print(f"Boards: {len(boards.get('items', []))}")

        # Create a board
        board = client.create_board(name="Test Board", description="Test description")
        print(f"Created board: {board['name']} (ID: {board['id']})")

        board_id = board['id']

        # Get board details
        board_details = client.get_board(board_id)
        print(f"Board details: {board_details}")

    except Exception as e:
        print(f"Error: {e}")