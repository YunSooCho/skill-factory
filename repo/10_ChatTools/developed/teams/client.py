"""
Microsoft Teams API Client

Supports 18+ API Actions including:
- Team operations (list teams, add members, get team members)
- Channel operations (list, create, send message, reply, get messages)
- Chat operations (list chats, send message)
- User operations (get user info, get user presence)
- Calendar operations (create events)
- File operations (get folder info, download files)
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class User:
    """Teams User representation"""
    id: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    user_principal_name: Optional[str] = None


@dataclass
class Presence:
    """Teams User Presence representation"""
    availability: Optional[str] = None
    activity: Optional[str] = None


class TeamsClient:
    """
    Microsoft Teams API Client using Microsoft Graph API.

    Authentication: OAuth 2.0 Access Token (Header: Authorization: Bearer {token})
    Base URL: https://graph.microsoft.com/v1.0
    """

    BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: str):
        """
        Initialize Teams client.

        Args:
            access_token: Microsoft Graph Access Token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid access token")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Team Operations ====================

    def list_teams(self) -> Dict[str, Any]:
        """
        Get list of teams.

        Returns:
            Dict with teams list
        """
        return self._request("GET", "/me/joinedTeams")

    def add_team_member(self, team_id: str, userPrincipalName: str, role: str = "member") -> Dict[str, Any]:
        """
        Add member to a team.

        Args:
            team_id: Team ID
            userPrincipalName: User principal name (email)
            role: Role (member or owner)

        Returns:
            Response dict
        """
        url = f"/groups/{team_id}/members"
        payload = {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": [role],
            "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{userPrincipalName}')"
        }

        return self._request("POST", url, json=payload)

    def get_team_members(self, team_id: str) -> Dict[str, Any]:
        """
        Get members of a team.

        Args:
            team_id: Team ID

        Returns:
            Dict with members list
        """
        return self._request("GET", f"/groups/{team_id}/members")

    # ==================== Channel Operations ====================

    def list_channels(self, team_id: str) -> Dict[str, Any]:
        """
        Get channels in a team.

        Args:
            team_id: Team ID

        Returns:
            Dict with channels list
        """
        return self._request("GET", f"/teams/{team_id}/channels")

    def create_channel(self, team_id: str, display_name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a channel in a team.

        Args:
            team_id: Team ID
            display_name: Channel display name
            description: Channel description

        Returns:
            Dict with created channel info
        """
        payload: Dict[str, Any] = {"displayName": display_name}

        if description:
            payload["description"] = description

        return self._request("POST", f"/teams/{team_id}/channels", json=payload)

    def send_channel_message(
        self,
        team_id: str,
        channel_id: str,
        content: str,
        mention_user_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send message to a channel.

        Args:
            team_id: Team ID
            channel_id: Channel ID
            content: Message content
            mention_user_ids: List of user IDs to mention

        Returns:
            Dict with created message
        """
        endpoint = f"/teams/{team_id}/channels/{channel_id}/messages"
        payload = {"body": {"contentType": "text", "content": content}}

        if mention_user_ids:
            mentions = []
            for user_id in mention_user_ids:
                mentions.append({
                    "@odata.type": "microsoft.graph.mention",
                    "id": 0,
                    "mentionText": f"<at id=\"{user_id}\">User</at>",
                    "mentioned": {"user": {"id": user_id}}
                })
            payload["mentions"] = mentions

        return self._request("POST", endpoint, json=payload)

    def send_channel_message_with_mention(
        self,
        team_id: str,
        channel_id: str,
        content: str,
        mention_text: str
    ) -> Dict[str, Any]:
        """
        Send message to a channel with mention.

        Args:
            team_id: Team ID
            channel_id: Channel ID
            content: Message content
            mention_text: Text to wrap with mention tags

        Returns:
            Dict with created message
        """
        import re
        mentioned_pattern = r'<at[^>]*>(.+?)<\/at>'

        # Extract entities
        text_parts = re.split(mention_text, content)
        mentions = []
        mention_counter = 0

        for part in text_parts:
            if part.startswith("<at") or part.endswith("</at>"):
                match = re.search(r'id="([^"]+)"', part)
                if match:
                    user_id = match.group(1)
                    mentions.append({
                        "@odata.type": "microsoft.graph.mention",
                        "id": mention_counter,
                        "mentionText": part,
                        "mentioned": {"user": {"id": user_id}}
                    })
                    mention_counter += 1

        payload = {
            "body": {"contentType": "html", "content": content}
        }

        if mentions:
            payload["mentions"] = mentions

        endpoint = f"/teams/{team_id}/channels/{channel_id}/messages"
        return self._request("POST", endpoint, json=payload)

    def get_channel_messages(
        self,
        team_id: str,
        channel_id: str
    ) -> Dict[str, Any]:
        """
        Get messages in a channel.

        Args:
            team_id: Team ID
            channel_id: Channel ID

        Returns:
            Dict with messages list
        """
        return self._request("GET", f"/teams/{team_id}/channels/{channel_id}/messages")

    def reply_to_channel_message(
        self,
        team_id: str,
        channel_id: str,
        message_id: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Reply to a message in a channel.

        Args:
            team_id: Team ID
            channel_id: Channel ID
            message_id: Parent message ID
            content: Reply content

        Returns:
            Dict with created reply
        """
        endpoint = f"/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies"
        payload = {"body": {"contentType": "text", "content": content}}

        return self._request("POST", endpoint, json=payload)

    def get_message_replies(
        self,
        team_id: str,
        channel_id: str,
        message_id: str
    ) -> Dict[str, Any]:
        """
        Get replies to a specific message.

        Args:
            team_id: Team ID
            channel_id: Channel ID
            message_id: Parent message ID

        Returns:
            Dict with replies list
        """
        return self._request("GET", f"/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies")

    # ==================== Chat Operations ====================

    def list_chats(self) -> Dict[str, Any]:
        """
        Get list of chats.

        Returns:
            Dict with chats list
        """
        return self._request("GET", "/me/chats")

    def send_chat_message(
        self,
        chat_id: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Send message to a chat.

        Args:
            chat_id: Chat ID
            content: Message content

        Returns:
            Dict with created message
        """
        endpoint = f"/chats/{chat_id}/messages"
        payload = {"body": {"contentType": "text", "content": content}}

        return self._request("POST", endpoint, json=payload)

    # ==================== User Operations ====================

    def get_user_info(self, user_id: Optional[str] = None) -> User:
        """
        Get user information.

        Args:
            user_id: User ID (None for current user)

        Returns:
            User object
        """
        endpoint = "/me" if not user_id else f"/users/{user_id}"
        result = self._request("GET", endpoint)

        return User(
            id=result.get("id"),
            display_name=result.get("displayName"),
            email=result.get("mail"),
            user_principal_name=result.get("userPrincipalName")
        )

    def get_user_presence(self, user_id: str) -> Presence:
        """
        Get user presence information.

        Args:
            user_id: User ID

        Returns:
            Presence object
        """
        result = self._request("GET", f"/users/{user_id}/presence")

        return Presence(
            availability=result.get("availability"),
            activity=result.get("activity")
        )

    # ==================== Calendar Operations ====================

    def create_calendar_event(
        self,
        subject: str,
        start: str,
        end: str,
        attendees: Optional[List[str]] = None,
        location: Optional[str] = None,
        body: Optional[str] = None,
        is_online: bool = False
    ) -> Dict[str, Any]:
        """
        Create a calendar event (recommended).

        Args:
            subject: Event subject
            start: Start time in ISO format (YYYY-MM-DDTHH:mm:ss)
            end: End time in ISO format (YYYY-MM-DDTHH:mm:ss)
            attendees: List of attendee email addresses
            location: Event location
            body: Event body/description
            is_online: Whether this is an online meeting

        Returns:
            Dict with created event
        """
        import re

        # Fix ISO format if needed
        def ensure_iso_format(timestr: str) -> str:
            if 'Z' not in timestr and '+' not in timestr:
                return timestr + 'Z'
            return timestr

        start_iso = ensure_iso_format(start)
        end_iso = ensure_iso_format(end)

        payload: Dict[str, Any] = {
            "subject": subject,
            "start": {"dateTime": start_iso, "timeZone": "UTC"},
            "end": {"dateTime": end_iso, "timeZone": "UTC"}
        }

        if attendees:
            payload["attendees"] = [
                {"emailAddress": {"address": email, "name": email}} for email in attendees
            ]

        if location:
            payload["location": {"displayName": location}]

        if body:
            payload["body": {"contentType": "HTML", "content": body}]

        if is_online:
            payload["isOnlineMeeting"] = True
            payload["onlineMeetingProvider"] = "teamsForBusiness"

        return self._request("POST", "/me/events", json=payload)

    # ==================== File Operations ====================

    def get_folder_info(self, drive_id: str, item_id: str) -> Dict[str, Any]:
        """
        Get folder/drive information.

        Args:
            drive_id: Drive ID
            item_id: Folder item ID

        Returns:
            Dict with folder information
        """
        return self._request("GET", f"/drives/{drive_id}/items/{item_id}")

    def download_file(self, drive_id: str, item_id: str) -> bytes:
        """
        Download a file.

        Args:
            drive_id: Drive ID
            item_id: File item ID

        Returns:
            File content as bytes
        """
        url = f"{self.BASE_URL}/drives/{drive_id}/items/{item_id}/content"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download file: {response.status_code}")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    access_token = "your_ms_graph_access_token"

    client = TeamsClient(access_token=access_token)

    try:
        # List teams
        teams = client.list_teams()
        print(f"Teams: {teams}")

        # Get team members
        if teams.get("value"):
            team_id = teams["value"][0]["id"]
            members = client.get_team_members(team_id)
            print(f"Team members: {members}")

        # List channels
        if teams.get("value"):
            team_id = teams["value"][0]["id"]
            channels = client.list_channels(team_id)
            print(f"Channels: {channels}")

        # Send message to channel
        if channels.get("value"):
            channel = channels["value"][0]
            result = client.send_channel_message(
                team_id=channel["teamId"],
                channel_id=channel["id"],
                content="Hello from Teams API!"
            )
            print(f"Message sent: {result}")

        # Create calendar event
        event = client.create_calendar_event(
            subject="Team Meeting",
            start="2024-01-15T14:00:00Z",
            end="2024-01-15T15:00:00Z",
            attendees=["user1@example.com", "user2@example.com"],
            is_online=True
        )
        print(f"Event created: {event}")

        # Get user info
        user = client.get_user_info()
        print(f"User: {user.display_name}")

        # Get user presence
        presence = client.get_user_presence(user.id)
        print(f"Presence: {presence.activity} ({presence.availability})")

        # List chats
        chats = client.list_chats()
        print(f"Chats: {chats}")

        # Send chat message
        if chats.get("value"):
            chat_id = chats["value"][0]["id"]
            result = client.send_chat_message(chat_id, "Hello from API!")
            print(f"Chat message sent: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()