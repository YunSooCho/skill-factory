"""
Pinterest API v5 Client
Documentation: https://developers.pinterest.com/docs/api/
"""

import requests
import logging
from typing import List, Optional, Dict, Any, Union
from .models import Pin, Board, PinCreateRequest, BoardCreateRequest

logger = logging.getLogger(__name__)


class PinterestClient:
    """
    Pinterest API v5 Client for Yoom Integration

    API Actions:
    - Get Pin
    - Create Pin
    - Get Board
    - Create Board
    - List Pins
    - Update Board
    - List Boards
    """

    BASE_URL = "https://api.pinterest.com/v5"
    API_VERSION = "v5"

    def __init__(self, access_token: str, app_id: Optional[str] = None):
        """
        Initialize Pinterest Client

        Args:
            access_token: OAuth2 access token
            app_id: Pinterest App ID (optional)
        """
        self.access_token = access_token
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to Pinterest API

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response data

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Pinterest API Error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    # ========== PIN OPERATIONS ==========

    def get_pin(self, pin_id: str) -> Pin:
        """
        Get Pin details

        Args:
            pin_id: Pinterest Pin ID

        Returns:
            Pin object
        """
        endpoint = f"/pins/{pin_id}"
        data = self._request('GET', endpoint)
        return Pin.from_dict(data)

    def create_pin(self, request: Union[PinCreateRequest, Dict[str, Any]]) -> Pin:
        """
        Create a new Pin

        Args:
            request: PinCreateRequest object or dictionary

        Returns:
            Created Pin object
        """
        if isinstance(request, dict):
            request = PinCreateRequest(**request)

        # Prepare media source format
        data = request.to_dict()
        return self._request('POST', '/pins', json=data)
        # Note: Use POST /pins with application/json for direct API
        # For multipart/form-data with image upload, use different endpoint

    def list_pins(
        self,
        board_id: Optional[str] = None,
        cursor: Optional[str] = None,
        page_size: int = 25
    ) -> Dict[str, Any]:
        """
        List Pins

        Args:
            board_id: Filter by board ID (optional)
            cursor: Pagination cursor (optional)
            page_size: Number of pins per page (default: 25, max: 100)

        Returns:
            Dictionary with 'items' (pins) and 'cursor' for pagination
        """
        params = {'page_size': min(page_size, 100)}
        if board_id:
            params['board_id'] = board_id
        if cursor:
            params['bookmark'] = cursor

        endpoint = f"/boards/{board_id}/pins" if board_id else "/pins"
        data = self._request('GET', endpoint, params=params)
        return {
            'items': [Pin.from_dict(item) for item in data.get('items', [])],
            'cursor': data.get('bookmark')
        }

    # ========== BOARD OPERATIONS ==========

    def get_board(self, board_id: str) -> Board:
        """
        Get Board details

        Args:
            board_id: Pinterest Board ID

        Returns:
            Board object
        """
        endpoint = f"/boards/{board_id}"
        data = self._request('GET', endpoint)
        return Board.from_dict(data)

    def create_board(self, request: Union[BoardCreateRequest, Dict[str, Any]]) -> Board:
        """
        Create a new Board

        Args:
            request: BoardCreateRequest object or dictionary

        Returns:
            Created Board object
        """
        if isinstance(request, dict):
            request = BoardCreateRequest(**request)

        data = request.to_dict()
        result = self._request('POST', '/boards', json=data)
        return Board.from_dict(result)

    def update_board(
        self,
        board_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        privacy: Optional[str] = None
    ) -> Board:
        """
        Update Board

        Args:
            board_id: Pinterest Board ID
            name: New board name (optional)
            description: New board description (optional)
            privacy: Privacy setting ('public' or 'secret', optional)

        Returns:
            Updated Board object
        """
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if privacy is not None:
            data['privacy'] = privacy

        endpoint = f"/boards/{board_id}"
        result = self._request('PATCH', endpoint, json=data)
        return Board.from_dict(result)

    def list_boards(
        self,
        cursor: Optional[str] = None,
        page_size: int = 25
    ) -> Dict[str, Any]:
        """
        List Boards

        Args:
            cursor: Pagination cursor (optional)
            page_size: Number of boards per page (default: 25, max: 100)

        Returns:
            Dictionary with 'items' (boards) and 'cursor' for pagination
        """
        params = {'page_size': min(page_size, 100)}
        if cursor:
            params['bookmark'] = cursor

        data = self._request('GET', '/boards', params=params)
        return {
            'items': [Board.from_dict(item) for item in data.get('items', [])],
            'cursor': data.get('bookmark')
        }

    # ========== UTILITY METHODS ==========

    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information"""
        return self._request('GET', '/user_account')

    def test_connection(self) -> bool:
        """
        Test API connection

        Returns:
            True if connection successful
        """
        try:
            self.get_user_info()
            return True
        except Exception:
            return False