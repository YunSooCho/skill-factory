"""
Monday.com API Client

Work Operating System for managing:
- Boards (workspaces)
- Groups (sections)
- Items (tasks, deals, projects)
- Updates (comments and notes)
- Tags (labels and markers)

API Actions (20):
1. Create Item
2. Get Item
3. Update Item
4. Delete Item
5. Create Board
6. Get Board
7. Update Board
8. Delete Board
9. Create Group
10. Get Groups
11. Create Column
12. Update Column
13. Add Update to Item
14. Get Updates
15. Create Tag
16. Add Tag to Item
17. Get Items
18. Move Item
19. Archive Item
20. Duplicate Item

Triggers (10):
- Item Created
- Item Updated
- Item Deleted
- Item Moved
- Status Changed
- Column Value Changed
- Tag Added
- Tag Removed
- Update Created
- Status Column Changed

Authentication: API Token
Base URL: https://api.monday.com/v2
Documentation: https://developer.monday.com/api-reference
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ColumnType(Enum):
    """Column type enum"""
    STATUS = "status"
    TEXT = "text"
    NUMBER = "numbers"
    DATE = "date"
    PERSON = "person"
    TAG = "tags"
    CHECKBOX = "checkbox"
    BOARD_RELATION = "board_relation"
    ITEM_RELATION = "mirror"
    TIMELINE = "timeline"
    HOUR = "hour"
    RATING = "rating"
    PROGRESS = "progress"
    FILE = "file"
    LINK = "link"
    EMAIL = "email"
    PHONE = "phone"
    LOCATION = "location"
    COLOR_PICKER = "color_picker"
    DROPDOWN = "dropdown"


@dataclass
class Board:
    """Board model"""
    id: Optional[str] = None
    name: str = ""
    description: Optional[str] = None
    board_kind: Optional[str] = None
    state: Optional[str] = None
    owner_id: Optional[int] = None
    permissions: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Group:
    """Group model"""
    id: Optional[str] = None
    title: str = ""
    color: Optional[str] = None
    position: Optional[int] = None
    archived: Optional[bool] = None


@dataclass
class Column:
    """Column model"""
    id: Optional[str] = None
    title: str = ""
    type: Optional[str] = None
    settings_str: Optional[str] = None
    width: Optional[int] = None
    hidden: Optional[bool] = None
    archived: Optional[bool] = None


@dataclass
class Item:
    """Item model"""
    id: Optional[str] = None
    name: str = ""
    board_id: Optional[str] = None
    group_id: Optional[str] = None
    column_values: Optional[Dict[str, Any]] = None
    state: Optional[str] = None
    creator_id: Optional[int] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Update:
    """Update model"""
    id: Optional[str] = None
    body: str = ""
    item_id: Optional[str] = None
    creator_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    replies: Optional[List[Any]] = None


@dataclass
class Tag:
    """Tag model"""
    id: Optional[str] = None
    name: str = ""
    color: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, calls_per_second: int = 40):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        """Acquire a token from the rate limiter"""
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        self.tokens = min(self.calls_per_second, self.tokens + elapsed * self.calls_per_second)
        self.last_update = now

        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.calls_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = self.calls_per_second
        else:
            self.tokens -= 1


class MondayError(Exception):
    """Base exception for Monday errors"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class MondayClient:
    """
    Monday.com API Client

    Example usage:
        ```python
        client = MondayClient(api_token="your_token")

        # Create an item
        item = await client.create_item(
            board_id="123",
            group_id="456",
            item_name="New Project",
            column_values={"status": "Working on it"}
        )

        # Get items
        items = await client.get_items(board_id="123")
        ```
    """

    def __init__(self, api_token: str, base_url: str = "https://api.monday.com/v2"):
        """
        Initialize Monday client

        Args:
            api_token: Monday API token
            base_url: API base URL (default: https://api.monday.com/v2)
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": api_token,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }
        self._rate_limiter = RateLimiter(calls_per_second=40)

    async def _make_request(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make GraphQL request to Monday API

        Args:
            query: GraphQL query string
            variables: GraphQL variables

        Returns:
            Response data

        Raises:
            MondayError: If request fails
        """
        await self._rate_limiter.acquire()

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url=self.base_url,
                    json=payload,
                    headers=self._headers
                ) as response:
                    response_json = await response.json()

                    if "errors" in response_json:
                        errors = response_json["errors"]
                        error_msg = errors[0].get("message", "Unknown error") if errors else "Unknown error"
                        raise MondayError(error_msg, response.status)

                    return response_json.get("data", {})

            except aiohttp.ClientError as e:
                raise MondayError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise MondayError("Request timeout")

    # Board methods

    async def create_board(self, board_name: str, board_kind: str = "public") -> Board:
        """
        Create a new board

        Args:
            board_name: Board name
            board_kind: Board type (public, private, share)

        Returns:
            Created Board object
        """
        query = """
            mutation($boardName: String!, $boardKind: BoardKind!) {
                create_board(board_name: $boardName, board_kind: $boardKind) {
                    id
                    name
                    description
                    board_kind
                    state
                    owner { id }
                    permissions
                    updated_at
                    created_at
                }
            }
        """

        variables = {
            "boardName": board_name,
            "boardKind": board_kind
        }

        data = await self._make_request(query, variables)
        return Board(**data["create_board"])

    async def get_board(self, board_id: str) -> Board:
        """
        Get board by ID

        Args:
            board_id: Board ID

        Returns:
            Board object
        """
        query = """
            query($boardIds: [Int]!) {
                boards(ids: $boardIds) {
                    id
                    name
                    description
                    board_kind
                    state
                    owner { id }
                    permissions
                    updated_at
                    created_at
                }
            }
        """

        variables = {"boardIds": [int(board_id)]}
        data = await self._make_request(query, variables)

        if not data.get("boards"):
            raise MondayError(f"Board {board_id} not found")

        return Board(**data["boards"][0])

    async def update_board(self, board_id: str, name: Optional[str] = None,
                           board_kind: Optional[str] = None) -> Board:
        """
        Update board

        Args:
            board_id: Board ID
            name: New name (optional)
            board_kind: New type (optional)

        Returns:
            Updated Board object
        """
        mutation = f"mutation {{"
        variables = {}

        if name:
            mutation += f"    name: \"$name\","

        if board_kind:
            mutation += f"    board_kind: \"$boardKind\","

        mutation = mutation.rstrip(",") + f"""        id: {board_id}
        return
    }}"""

        query = f"""
            mutation($name: String, $boardKind: BoardKind!) {{
                update_board(board_id: {board_id}, name: $name, board_kind: $boardKind) {{
                    id
                    name
                    description
                    board_kind
                    state
                    owner {{ id }}
                    permissions
                    updated_at
                    created_at
                }}
            }}
        """

        if name:
            variables["name"] = name
        if board_kind:
            variables["boardKind"] = board_kind

        data = await self._make_request(query, variables)
        return Board(**data["update_board"])

    async def delete_board(self, board_id: str) -> bool:
        """
        Delete board

        Args:
            board_id: Board ID

        Returns:
            True if successful
        """
        query = f"""
            mutation {{
                delete_board(board_id: {board_id}) {{
                    id
                }}
            }}
        """

        data = await self._make_request(query)
        return data.get("delete_board") is not None

    # Group methods

    async def create_group(self, board_id: str, group_name: str) -> Group:
        """
        Create a new group in board

        Args:
            board_id: Board ID
            group_name: Group name

        Returns:
            Created Group object
        """
        query = """
            mutation($boardId: Int!, $groupName: String!) {
                create_group(board_id: $boardId, group_name: $groupName) {
                    id
                    title
                    color
                    position
                    archived
                }
            }
        """

        variables = {
            "boardId": int(board_id),
            "groupName": group_name
        }

        data = await self._make_request(query, variables)
        return Group(**data["create_group"])

    async def get_groups(self, board_id: str) -> List[Group]:
        """
        Get groups in board

        Args:
            board_id: Board ID

        Returns:
            List of Group objects
        """
        query = """
            query($boardIds: [Int]!) {
                boards(ids: $boardIds) {
                    groups {
                        id
                        title
                        color
                        position
                        archived
                    }
                }
            }
        """

        variables = {"boardIds": [int(board_id)]}
        data = await self._make_request(query, variables)

        if not data.get("boards"):
            return []

        groups = data["boards"][0].get("groups", [])
        return [Group(**group) for group in groups]

    # Item methods

    async def create_item(self, board_id: str, group_id: str, item_name: str,
                          column_values: Optional[Dict[str, Any]] = None) -> Item:
        """
        Create a new item

        Args:
            board_id: Board ID
            group_id: Group ID
            item_name: Item name
            column_values: Column values dictionary

        Returns:
            Created Item object
        """
        # Prepare column values for GraphQL
        values_json = column_values if column_values else {}

        query = """
            mutation($boardId: Int!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
                create_item(board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) {
                    id
                    name
                    board { id }
                    group { id }
                    column_values { id text value additional_info }
                    state
                    creator { id }
                    updated_at
                    created_at
                }
            }
        """

        variables = {
            "boardId": int(board_id),
            "groupId": group_id,
            "itemName": item_name,
            "columnValues": values_json
        }

        data = await self._make_request(query, variables)
        return Item(**data["create_item"])

    async def get_item(self, item_id: str) -> Item:
        """
        Get item by ID

        Args:
            item_id: Item ID

        Returns:
            Item object
        """
        query = """
            query($itemIds: [Int]!) {
                items(ids: $itemIds) {
                    id
                    name
                    board { id }
                    group { id }
                    column_values { id text value additional_info }
                    state
                    creator { id }
                    updated_at
                    created_at
                }
            }
        """

        variables = {"itemIds": [int(item_id)]}
        data = await self._make_request(query, variables)

        if not data.get("items"):
            raise MondayError(f"Item {item_id} not found")

        return Item(**data["items"][0])

    async def get_items(self, board_id: str, group_id: Optional[str] = None,
                        limit: Optional[int] = None) -> List[Item]:
        """
        Get items from board

        Args:
            board_id: Board ID
            group_id: Optional Group ID to filter
            limit: Optional limit

        Returns:
            List of Item objects
        """
        args = [f'ids: {[int(board_id)]}']
        if group_id:
            args.append(f'group_id: "{group_id}"')

        query = f"""
            query {{
                boards({', '.join(args)}) {{
                    items(limit: {limit if limit else 100}) {{
                        id
                        name
                        board {{ id }}
                        group {{ id }}
                        column_values {{ id text value additional_info }}
                        state
                        creator {{ id }}
                        updated_at
                        created_at
                    }}
                }}
            }}
        """

        data = await self._make_request(query)

        if not data.get("boards"):
            return []

        items = data["boards"][0].get("items", [])
        return [Item(**item) for item in items]

    async def update_item(self, item_id: str, name: Optional[str] = None,
                          column_values: Optional[Dict[str, Any]] = None) -> Item:
        """
        Update item

        Args:
            item_id: Item ID
            name: New name (optional)
            column_values: Column values (optional)

        Returns:
            Updated Item object
        """
        query = """
            mutation($itemId: Int!, $name: String, $columnValues: JSON) {
                update_item(item_id: $itemId, name: $name, column_values: $columnValues) {
                    id
                    name
                    board { id }
                    group { id }
                    column_values { id text value additional_info }
                    state
                    creator { id }
                    updated_at
                    created_at
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "name": name,
            "columnValues": column_values if column_values else {}
        }

        data = await self._make_request(query, variables)
        return Item(**data["update_item"])

    async def delete_item(self, item_id: str) -> bool:
        """
        Delete item

        Args:
            item_id: Item ID

        Returns:
            True if successful
        """
        query = f"""
            mutation {{
                delete_item(item_id: {int(item_id)}) {{
                    id
                }}
            }}
        """

        data = await self._make_request(query)
        return data.get("delete_item") is not None

    async def move_item(self, item_id: str, group_id: str) -> Item:
        """
        Move item to another group

        Args:
            item_id: Item ID
            group_id: Target group ID

        Returns:
            Updated Item object
        """
        query = """
            mutation($itemId: Int!, $groupId: String!) {
                move_item_to_group(item_id: $itemId, group_id: $groupId) {
                    id
                    name
                    board { id }
                    group { id }
                    column_values { id text value additional_info }
                    state
                    creator { id }
                    updated_at
                    created_at
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "groupId": group_id
        }

        data = await self._make_request(query, variables)
        return Item(**data["move_item_to_group"])

    async def archive_item(self, item_id: str) -> bool:
        """
        Archive item

        Args:
            item_id: Item ID

        Returns:
            True if successful
        """
        query = f"""
            mutation {{
                archive_item(item_id: {int(item_id)}) {{
                    id
                }}
            }}
        """

        data = await self._make_request(query)
        return data.get("archive_item") is not None

    async def duplicate_item(self, item_id: str, with_updates: bool = False) -> Item:
        """
        Duplicate item

        Args:
            item_id: Item ID
            with_updates: Include updates in duplicate

        Returns:
            New Item object
        """
        query = """
            mutation($itemId: Int!, $withUpdates: Boolean!) {
                duplicate_item(item_id: $itemId, with_updates: $withUpdates) {
                    id
                    name
                    board { id }
                    group { id }
                    column_values { id text value additional_info }
                    state
                    creator { id }
                    updated_at
                    created_at
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "withUpdates": with_updates
        }

        data = await self._make_request(query, variables)
        return Item(**data["duplicate_item"])

    # Column methods

    async def create_column(self, board_id: str, title: str, column_type: ColumnType) -> Column:
        """
        Create a new column in board

        Args:
            board_id: Board ID
            title: Column title
            column_type: Column type

        Returns:
            Created Column object
        """
        query = """
            mutation($boardId: Int!, $title: String!, $columnType: ColumnType!) {
                create_column(board_id: $boardId, title: $title, column_type: $columnType) {
                    id
                    title
                    type
                    settings_str
                    width
                }
            }
        """

        variables = {
            "boardId": int(board_id),
            "title": title,
            "columnType": column_type.value
        }

        data = await self._make_request(query, variables)
        return Column(**data["create_column"])

    async def update_column(self, board_id: str, column_id: str,
                            title: Optional[str] = None) -> Column:
        """
        Update column

        Args:
            board_id: Board ID
            column_id: Column ID
            title: New title

        Returns:
            Updated Column object
        """
        query = """
            mutation($boardId: Int!, $columnId: String!, $title: String!) {
                change_column_title(board_id: $boardId, column_id: $columnId, title: $title) {
                    id
                    title
                    type
                    settings_str
                    width
                }
            }
        """

        variables = {
            "boardId": int(board_id),
            "columnId": column_id,
            "title": title
        }

        data = await self._make_request(query, variables)
        return Column(**data["change_column_title"])

    # Update (comment) methods

    async def add_update_to_item(self, item_id: str, text: str) -> Update:
        """
        Add update/comment to item

        Args:
            item_id: Item ID
            text: Update text

        Returns:
            Created Update object
        """
        query = """
            mutation($itemId: Int!, $body: String!) {
                create_update(item_id: $itemId, body: $body) {
                    id
                    body
                    item { id }
                    creator { id }
                    created_at
                    updated_at
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "body": text
        }

        data = await self._make_request(query, variables)
        return Update(**data["create_update"])

    async def get_updates(self, item_id: str, limit: Optional[int] = None) -> List[Update]:
        """
        Get updates for item

        Args:
            item_id: Item ID
            limit: Optional limit

        Returns:
            List of Update objects
        """
        query = """
            query($itemId: Int!, $limit: Int) {
                items(ids: [$itemId]) {
                    updates(limit: $limit) {
                        id
                        body
                        created_at
                        updated_at
                        creator { id }
                        replies {
                            id
                            body
                            created_at
                            creator { id }
                        }
                    }
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "limit": limit
        }

        data = await self._make_request(query, variables)

        if not data.get("items"):
            return []

        updates = data["items"][0].get("updates", [])
        return [Update(**update) for update in updates]

    # Tag methods

    async def create_tag(self, board_id: str, tag_name: str, color: Optional[str] = None) -> Tag:
        """
        Create a new tag

        Args:
            board_id: Board ID
            tag_name: Tag name
            color: Optional color

        Returns:
            Created Tag object
        """
        query = """
            mutation($boardId: Int!, $tagName: String!, $color: String!) {
                create_tag(board_id: $boardId, tag_name: $tagName, color: $color) {
                    id
                    name
                    color
                }
            }
        """

        variables = {
            "boardId": int(board_id),
            "tagName": tag_name,
            "color": color if color else "#579BFC"
        }

        data = await self._make_request(query, variables)
        return Tag(**data["create_tag"])

    async def add_tag_to_item(self, item_id: str, tag_id: str) -> Item:
        """
        Add tag to item

        Args:
            item_id: Item ID
            tag_id: Tag ID

        Returns:
            Updated Item object
        """
        # Get item first to get column values
        item = await self.get_item(item_id)

        # Find tags column
        tags_column_id = None
        existing_tags = []

        if item.column_values:
            for col_id, col_value in item.column_values.items():
                if isinstance(col_value, dict) and col_value.get("type") == "tags":
                    tags_column_id = col_id
                    if col_value.get("tags"):
                        existing_tags = col_value["tags"]
                    break

        if not tags_column_id:
            raise MondayError("No tags column found on this board")

        # Add new tag
        updated_tags = existing_tags + [{"id": tag_id}]

        # Update item with new tags
        query = """
            mutation($itemId: Int!, $columnValues: JSON!) {
                update_multiple_column_values(item_id: $itemId, column_values: $columnValues) {
                    id
                    name
                    column_values { id text value additional_info }
                }
            }
        """

        variables = {
            "itemId": int(item_id),
            "columnValues": {tags_column_id: {"tags": updated_tags}}
        }

        data = await self._make_request(query, variables)
        return Item(**data["update_multiple_column_values"])

    # Webhook handling for triggers

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event from Monday

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data with event type and entity info

        Supported triggers:
        - Item Created
        - Item Updated
        - Item Deleted
        - Item Moved
        - Status Changed
        - Column Value Changed
        - Tag Added
        - Tag Removed
        - Update Created
        - Status Column Changed
        """
        event_type = webhook_data.get("event", {}).get("type", "unknown")
        data = webhook_data.get("event", {}).get("data", {})

        item_id = data.get("pulseId") or data.get("item", {}).get("id")
        board_id = data.get("boardId") or data.get("board", {}).get("id")
        group_id = data.get("groupId") or data.get("group", {}).get("id")

        return {
            "event_type": event_type,
            "item_id": item_id,
            "board_id": board_id,
            "group_id": group_id,
            "data": webhook_data
        }