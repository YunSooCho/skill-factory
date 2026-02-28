"""
Slack API Client

Supports 21+ API Actions including:
- User operations (get user info, find user by email)
- Channel operations (list, create, archive, invite members, list messages)
- Message operations (send, delete, get message details, get thread messages)
- User group operations (create, list, get users in group)
- Direct message operations (send DM)
- Member operations (remove from private channel, get channel members)
- Reaction operations (get message reactions)
- Message link operations
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class User:
    """Slack User representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    real_name: Optional[str] = None
    email: Optional[str] = None
    team_id: Optional[str] = None
    deleted: bool = False
    is_admin: bool = False
    is_bot: bool = False


@dataclass
class Channel:
    """Slack Channel representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    is_channel: bool = True
    is_private: bool = False
    is_archived: bool = False
    members: List[str] = None

    def __post_init__(self):
        if self.members is None:
            self.members = []


class SlackClient:
    """
    Slack API Client.

    Authentication: Bot Token (Header: Authorization: Bearer {token})
    Base URL: https://slack.com/api
    """

    BASE_URL = "https://slack.com/api"

    def __init__(self, bot_token: str):
        """
        Initialize Slack client.

        Args:
            bot_token: Slack Bot Token (starts with xoxb-)
        """
        self.bot_token = bot_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            if 'params' not in kwargs:
                kwargs['params'] = {}
            method_lower = method.lower()
            if method_lower == "get":
                response = self.session.get(url, **kwargs)
            elif method_lower == "post":
                response = self.session.post(url, **kwargs)
            elif method_lower == "delete":
                response = self.session.delete(url, **kwargs)
            else:
                response = requests.request(method, url, headers=kwargs.get('headers'), json=kwargs.get('json'), params=kwargs.get('params'))

            if response.status_code == 200:
                data = response.json()
                if not data.get("ok", False):
                    error = data.get("error", "Unknown error")
                    raise Exception(f"Slack API error: {error}")
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid bot token")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            else:
                raise Exception(f"Server error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== User Operations ====================

    def get_user_info(self, user_id: str) -> User:
        """
        Get user information.

        Args:
            user_id: User ID

        Returns:
            User object
        """
        result = self._request("GET", "/users.info", params={"user": user_id})
        user_data = result.get("user", {})

        return User(
            id=user_data.get("id"),
            name=user_data.get("name"),
            real_name=user_data.get("real_name"),
            email=user_data.get("profile", {}).get("email"),
            team_id=user_data.get("team_id"),
            deleted=user_data.get("deleted", False),
            is_admin=user_data.get("is_admin", False),
            is_bot=user_data.get("is_bot", False)
        )

    def find_user_by_email(self, email: str) -> User:
        """
        Find user by email address.

        Args:
            email: User email address

        Returns:
            User object
        """
        result = self._request("GET", "/users.lookupByEmail", params={"email": email})
        user_data = result.get("user", {})

        return User(
            id=user_data.get("id"),
            name=user_data.get("name"),
            real_name=user_data.get("real_name"),
            email=user_data.get("profile", {}).get("email")
        )

    # ==================== Channel Operations ====================

    def list_public_channels(
        self,
        limit: int = 100,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List public channels.

        Args:
            limit: Number of results per page
            cursor: Pagination cursor

        Returns:
            Dict with channels list
        """
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        return self._request("GET", "/conversations.list", params=params)

    def create_channel(self, name: str, is_private: bool = False) -> Channel:
        """
        Create a channel.

        Args:
            name: Channel name
            is_private: Whether to create private channel

        Returns:
            Channel object
        """
        result = self._request("GET", "/conversations.create", params={
            "name": name,
            "is_private": str(is_private).lower()
        })
        channel_data = result.get("channel", {})

        return Channel(
            id=channel_data.get("id"),
            name=channel_data.get("name"),
            is_channel=channel_data.get("is_channel", True),
            is_private=channel_data.get("is_private", False),
            is_archived=channel_data.get("is_archived", False)
        )

    def archive_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Archive a channel.

        Args:
            channel_id: Channel ID

        Returns:
            Response dict
        """
        return self._request("GET", "/conversations.archive", params={"channel": channel_id})

    def invite_to_channel(self, channel_id: str, user_ids: List[str]) -> Dict[str, Any]:
        """
        Invite users to a channel.

        Args:
            channel_id: Channel ID
            user_ids: List of user IDs to invite

        Returns:
            Response dict
        """
        users = ",".join(user_ids)
        return self._request("GET", "/conversations.invite", params={
            "channel": channel_id,
            "users": users
        })

    def remove_from_channel(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        """
        Remove member from private channel.

        Args:
            channel_id: Channel ID
            user_id: User ID to remove

        Returns:
            Response dict
        """
        return self._request("GET", "/conversations.kick", params={
            "channel": channel_id,
            "user": user_id
        })

    def get_channel_members(
        self,
        channel_id: str,
        limit: int = 100,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of members in a channel.

        Args:
            channel_id: Channel ID
            limit: Number of results per page
            cursor: Pagination cursor

        Returns:
            Dict with members list
        """
        params: Dict[str, Any] = {"channel": channel_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor

        return self._request("GET", "/conversations.members", params=params)

    # ==================== Message Operations ====================

    def send_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None,
        parse: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message to a channel.

        Args:
            channel: Channel ID or name
            text: Message text
            thread_ts: Thread timestamp for threaded messages
            parse: Parse mode (full, none)

        Returns:
            Response dict with message details
        """
        params: Dict[str, Any] = {
            "channel": channel,
            "text": text
        }

        if thread_ts:
            params["thread_ts"] = thread_ts
        if parse:
            params["parse"] = parse

        return self._request("GET", "/chat.postMessage", params=params)

    def send_direct_message(self, user_id: str, text: str) -> Dict[str, Any]:
        """
        Send direct message to a user.

        Args:
            user_id: User ID
            text: Message text

        Returns:
            Response dict with message details
        """
        params = {
            "channel": user_id,
            "text": text
        }

        return self._request("GET", "/chat.postMessage", params=params)

    def delete_message(self, channel: str, ts: str, as_user: bool = False) -> Dict[str, Any]:
        """
        Delete a message.

        Args:
            channel: Channel ID
            ts: Message timestamp
            as_user: Post as user

        Returns:
            Response dict
        """
        return self._request("GET", "/chat.delete", params={
            "channel": channel,
            "ts": ts,
            "as_user": str(as_user).lower()
        })

    def get_message(self, channel: str, ts: str, include_users: bool = False) -> Dict[str, Any]:
        """
        Get specific message details.

        Args:
            channel: Channel ID
            ts: Message timestamp
            include_users: Include user information

        Returns:
            Dict with message details
        """
        params: Dict[str, Any] = {
            "channel": channel,
            "ts": ts
        }

        if include_users:
            params["include_users"] = "true"

        return self._request("GET", "/conversations.history", params=params)

    def get_channel_messages(
        self,
        channel_id: str,
        limit: int = 100,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of messages in a channel.

        Args:
            channel_id: Channel ID
            limit: Number of results per page
            cursor: Pagination cursor

        Returns:
            Dict with messages list
        """
        params: Dict[str, Any] = {
            "channel": channel_id,
            "limit": limit
        }

        if cursor:
            params["cursor"] = cursor

        return self._request("GET", "/conversations.history", params=params)

    def get_thread_messages(
        self,
        channel: str,
        thread_ts: str
    ) -> Dict[str, Any]:
        """
        Get messages in a thread.

        Args:
            channel: Channel ID
            thread_ts: Thread parent timestamp

        Returns:
            Dict with thread messages
        """
        return self._request("GET", "/conversations.replies", params={
            "channel": channel,
            "ts": thread_ts
        })

    def send_message_with_attachments(
        self,
        channel: str,
        text: str,
        attachments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Send message with attachments.

        Args:
            channel: Channel ID or name
            text: Message text
            attachments: List of attachment dicts

        Returns:
            Response dict with message details
        """
        import json
        params: Dict[str, Any] = {
            "channel": channel,
            "text": text,
            "attachments": json.dumps(attachments)
        }

        return self._request("GET", "/chat.postMessage", params=params)

    def get_message_link(self, channel: str, ts: str) -> Dict[str, Any]:
        """
        Get permalink to a message.

        Args:
            channel: Channel ID
            ts: Message timestamp

        Returns:
            Dict with message link
        """
        return self._request("GET", "/chat.getPermalink", params={
            "channel": channel,
            "message_ts": ts
        })

    # ==================== Group Operations ====================

    def create_user_group(self, name: str, handle: str) -> Dict[str, Any]:
        """
        Create a user group.

        Args:
            name: Group name
            handle: Group handle

        Returns:
            Response dict with group info
        """
        return self._request("GET", "/usergroups.create", params={
            "name": name,
            "handle": handle
        })

    def list_user_groups(self, include_users: bool = False) -> Dict[str, Any]:
        """
        List user groups.

        Args:
            include_users: Include group members

        Returns:
            Dict with groups list
        """
        params = {"include_users": str(include_users).lower()}
        return self._request("GET", "/usergroups.list", params=params)

    def get_user_group_users(self, usergroup_id: str) -> Dict[str, Any]:
        """
        Get users in a user group.

        Args:
            usergroup_id: User group ID

        Returns:
            Dict with users list
        """
        return self._request("GET", "/usergroups.users.list", params={
            "usergroup": usergroup_id
        })

    # ==================== Reaction Operations ====================

    def get_message_reactions(self, channel: str, ts: str) -> Dict[str, Any]:
        """
        Get reactions for a message.

        Args:
            channel: Channel ID
            ts: Message timestamp

        Returns:
            Dict with reactions list
        """
        return self._request("GET", "/reactions.get", params={
            "channel": channel,
            "timestamp": ts
        })

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    bot_token = "xoxb-your-bot-token"

    client = SlackClient(bot_token=bot_token)

    try:
        # Get user info
        user = client.get_user_info("U1234567890")
        print(f"User: {user.real_name} ({user.name})")

        # Find user by email
        user = client.find_user_by_email("user@example.com")
        print(f"Found user: {user.name}")

        # List public channels
        channels = client.list_public_channels(limit=20)
        print(f"Channels: {channels}")

        # Create channel
        channel = client.create_channel("my-new-channel")
        print(f"Created channel: {channel.id}")

        # Send message
        result = client.send_message("C123456", "Hello from Slack API!")
        print(f"Message sent: {result}")

        # Send direct message
        result = client.send_direct_message("U123456", "DM from API")
        print(f"DM sent: {result}")

        # Get channel messages
        messages = client.get_channel_messages("C123456", limit=10)
        print(f"Messages: {messages}")

        # Get thread messages
        thread = client.get_thread_messages("C123456", "1234567890.123456")
        print(f"Thread: {thread}")

        # Send with attachments
        result = client.send_message_with_attachments(
            "C123456",
            "Message with attachments",
            [
                {
                    "title": "Attachment 1",
                    "text": "Attachment text",
                    "color": "#36a64f"
                }
            ]
        )

        # Delete message
        result = client.delete_message("C123456", "1234567890.123456")
        print(f"Message deleted: {result}")

        # List user groups
        groups = client.list_user_groups()
        print(f"User groups: {groups}")

        # Get message reactions
        reactions = client.get_message_reactions("C123456", "1234567890.123456")
        print(f"Reactions: {reactions}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()