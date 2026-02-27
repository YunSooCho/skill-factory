"""
Botstar API Client

Supports:
- Create Entity Item
- Get Entity Item
- Update Entity Item
- Delete Entity Item
- Search Entity Items
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class EntityItem:
    """Botstar entity item representation"""
    id: Optional[str] = None
    entity_name: Optional[str] = None
    value: Optional[str] = None
    synonyms: List[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []


class BotstarClient:
    """
    Botstar API client for chatbot entity management.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.botstar.com/v1
    """

    BASE_URL = "https://api.botstar.com/v1"

    def __init__(self, api_key: str, bot_id: str):
        """
        Initialize Botstar client.

        Args:
            api_key: Botstar API key
            bot_id: Bot ID
        """
        self.api_key = api_key
        self.bot_id = bot_id
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 204:
                return {}
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Entity Operations ====================

    def create_entity_item(
        self,
        entity_name: str,
        value: str,
        synonyms: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EntityItem:
        """
        Create a new entity item.

        Args:
            entity_name: Name of the entity (e.g., "intent", "city", "color")
            value: The primary value of the entity
            synonyms: List of alternative values/synonyms
            metadata: Additional metadata as key-value pairs

        Returns:
            EntityItem object
        """
        if not entity_name:
            raise ValueError("Entity name is required")
        if not value:
            raise ValueError("Value is required")

        payload = {
            "botId": self.bot_id,
            "entityName": entity_name,
            "value": value
        }

        if synonyms:
            payload["synonyms"] = synonyms
        if metadata:
            payload["metadata"] = metadata

        result = self._request("POST", "/entities/items", json=payload)
        return self._parse_entity_item(result)

    def get_entity_item(self, item_id: str) -> EntityItem:
        """
        Retrieve a specific entity item.

        Args:
            item_id: Entity item ID

        Returns:
            EntityItem object
        """
        result = self._request("GET", f"/entities/items/{item_id}")
        return self._parse_entity_item(result)

    def update_entity_item(
        self,
        item_id: str,
        value: Optional[str] = None,
        synonyms: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EntityItem:
        """
        Update an existing entity item.

        Args:
            item_id: Entity item ID
            value: New value (optional)
            synonyms: New list of synonyms (optional)
            metadata: New metadata (optional)

        Returns:
            Updated EntityItem object
        """
        payload: Dict[str, Any] = {"botId": self.bot_id}

        if value is not None:
            payload["value"] = value
        if synonyms is not None:
            payload["synonyms"] = synonyms
        if metadata is not None:
            payload["metadata"] = metadata

        result = self._request("PUT", f"/entities/items/{item_id}", json=payload)
        return self._parse_entity_item(result)

    def delete_entity_item(self, item_id: str) -> None:
        """
        Delete an entity item.

        Args:
            item_id: Entity item ID
        """
        self._request("DELETE", f"/entities/items/{item_id}")

    def search_entity_items(
        self,
        entity_name: str,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EntityItem]:
        """
        Search for entity items.

        Args:
            entity_name: Name of the entity to search
            query: Search query string
            limit: Number of results
            offset: Pagination offset

        Returns:
            List of EntityItem objects
        """
        if not entity_name:
            raise ValueError("Entity name is required")

        params = {
            "botId": self.bot_id,
            "entityName": entity_name,
            "limit": limit,
            "offset": offset
        }

        if query:
            params["query"] = query

        result = self._request("GET", "/entities/items/search", params=params)

        items = []
        if isinstance(result, dict) and "data" in result:
            for item_data in result.get("data", []):
                items.append(self._parse_entity_item(item_data))
        elif isinstance(result, list):
            for item_data in result:
                items.append(self._parse_entity_item(item_data))

        return items

    # ==================== Helper Methods ====================

    def _parse_entity_item(self, data: Dict[str, Any]) -> EntityItem:
        """Parse entity item data from API response"""
        return EntityItem(
            id=data.get("id"),
            entity_name=data.get("entityName"),
            value=data.get("value"),
            synonyms=data.get("synonyms", []),
            metadata=data.get("metadata"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_botstar_api_key"
    bot_id = "your_bot_id"

    client = BotstarClient(api_key=api_key, bot_id=bot_id)

    try:
        # Create entity item
        entity = client.create_entity_item(
            entity_name="city",
            value="Tokyo",
            synonyms=["東京", "Tokyo City", "Tōkyō"],
            metadata={"country": "Japan", "population": 13960000}
        )
        print(f"Created: {entity.value} (ID: {entity.id})")

        # Get entity item
        fetched = client.get_entity_item(entity.id)
        print(f"Fetched: {fetched.value}, Synonyms: {fetched.synonyms}")

        # Search entity items
        items = client.search_entity_items(
            entity_name="city",
            query="Tokyo",
            limit=10
        )
        print(f"Found {len(items)} items")

        # Update entity item
        updated = client.update_entity_item(
            entity.id,
            synonyms=["東京", "Tokyo City", "Tōkyō", "東京都"],
            metadata={"country": "Japan", "population": 14000000}
        )
        print(f"Updated: {len(updated.synonyms)} synonyms")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()