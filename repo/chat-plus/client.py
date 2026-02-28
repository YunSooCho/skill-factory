import requests
from typing import Dict, Optional


class ChatPlusClient:
    """
    Client for ChatPlus API - Live Chat Platform
    """

    def __init__(self, api_key: str, base_url: str = "https://api.chatplus.jp"):
        """
        Initialize ChatPlus client

        Args:
            api_key: ChatPlus API key
            base_url: Base URL for ChatPlus API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-ChatPlus-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Internal method to make API requests

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def send_message(self, chat_id: str, message: str, **kwargs) -> Dict:
        """
        Send a message to a chat

        Args:
            chat_id: Chat ID
            message: Message text
            **kwargs: Additional message options

        Returns:
            sent message data
        """
        data = {'chatId': chat_id, 'message': message}
        data.update(kwargs)
        return self._request('POST', '/api/v1/messages', json=data)

    def get_visitor_info(self, visitor_id: str) -> Dict:
        """
        Get visitor information

        Args:
            visitor_id: Visitor ID

        Returns:
            Visitor information
        """
        return self._request('GET', f'/api/v1/visitors/{visitor_id}')