"""
BotStar API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BotStarAPIError(Exception):
    """Base exception for BotStar API errors"""
    pass


class BotStarAuthError(BotStarAPIError):
    """Authentication error"""
    pass


class BotStarClient:
    """BotStar API Client for entity management"""

    BASE_URL = "https://api.botstar.com/v1"

    def __init__(self, access_token: str, namespace_id: Optional[str] = None):
        """
        Initialize BotStar client

        Args:
            access_token: Your BotStar API access token
            namespace_id: Namespace ID (optional, can be set per request)
        """
        self.access_token = access_token
        self.namespace_id = namespace_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-Botstar-Access-Token": access_token
        })

    # ===== Entity Management =====

    def create_entity_item(
        self,
        entity_type: str,
        entity_id: str,
        variables: Dict[str, Any],
        namespace_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create or update an entity item

        Args:
            entity_type: Entity type (e.g., "user", "conversation")
            entity_id: Entity ID
            variables: Variables dictionary
            namespace_id: Namespace ID (defaults to instance namespace_id)
            metadata: Optional metadata

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/entity"
        payload = {
            "entityType": entity_type,
            "entityId": entity_id,
            "variables": variables,
        }

        if metadata:
            payload["metadata"] = metadata

        params = {}
        if namespace_id or self.namespace_id:
            params["namespaceId"] = namespace_id or self.namespace_id

        try:
            response = self.session.post(endpoint, json=payload, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_entity_item(
        self,
        entity_type: str,
        entity_id: str,
        namespace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get an entity item

        Args:
            entity_type: Entity type
            entity_id: Entity ID
            namespace_id: Namespace ID

        Returns:
            Entity data
        """
        endpoint = f"{self.BASE_URL}/entity"
        params = {
            "entityType": entity_type,
            "entityId": entity_id,
        }

        if namespace_id or self.namespace_id:
            params["namespaceId"] = namespace_id or self.namespace_id

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_entity_item(
        self,
        entity_type: str,
        entity_id: str,
        variables: Dict[str, Any],
        namespace_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update an entity item

        Args:
            entity_type: Entity type
            entity_id: Entity ID
            variables: Variables to update
            namespace_id: Namespace ID
            metadata: Optional metadata

        Returns:
            Updated entity data
        """
        # BotStar uses POST to create/update entities
        return self.create_entity_item(
            entity_type=entity_type,
            entity_id=entity_id,
            variables=variables,
            namespace_id=namespace_id,
            metadata=metadata,
        )

    def delete_entity_item(
        self,
        entity_type: str,
        entity_id: str,
        namespace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete an entity item

        Args:
            entity_type: Entity type
            entity_id: Entity ID
            namespace_id: Namespace ID

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/entity"
        params = {
            "entityType": entity_type,
            "entityId": entity_id,
        }

        if namespace_id or self.namespace_id:
            params["namespaceId"] = namespace_id or self.namespace_id

        try:
            response = self.session.delete(endpoint, params=params)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def search_entity_items(
        self,
        entity_type: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        namespace_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search entity items

        Args:
            entity_type: Entity type
            filter_conditions: Filter conditions for variables
            namespace_id: Namespace ID
            limit: Maximum results
            offset: Result offset

        Returns:
            List of entities
        """
        endpoint = f"{self.BASE_URL}/entities"
        params = {"entityType": entity_type}

        if filter_conditions:
            # Convert filter conditions to query string
            for key, value in filter_conditions.items():
                params[f"filter[{key}]"] = str(value)

        if namespace_id or self.namespace_id:
            params["namespaceId"] = namespace_id or self.namespace_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("entities", data.get("data", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Bot Management =====

    def broadcast_message(
        self,
        message: str,
        channel: str,
        target_users: Optional[List[str]] = None,
        namespace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Broadcast a message to users

        Args:
            message: Message content
            channel: Channel (e.g., "messenger", "telegram")
            target_users: List of user IDs (default: all)
            namespace_id: Namespace ID

        Returns:
            Broadcast result
        """
        endpoint = f"{self.BASE_URL}/broadcast"
        payload = {
            "message": message,
            "channel": channel,
        }

        if target_users:
            payload["targetUsers"] = target_users

        params = {}
        if namespace_id or self.namespace_id:
            params["namespaceId"] = namespace_id or self.namespace_id

        try:
            response = self.session.post(endpoint, json=payload, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BotStarAuthError("Invalid access token")
        elif error.response.status_code == 403:
            raise BotStarAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 400:
            raise BotStarAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 404:
            raise BotStarAPIError("Resource not found")
        elif error.response.status_code == 429:
            raise BotStarAPIError("Rate limit exceeded")
        else:
            raise BotStarAPIError(f"HTTP {error.response.status_code}: {error.response.text}")