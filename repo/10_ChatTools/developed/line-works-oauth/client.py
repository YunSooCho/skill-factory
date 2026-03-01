"""
LINE WORKS OAuth API Client

Supports:
39 API Actions including:
- User management (list, get, create, update, delete, suspend, unsuspend)
- Message operations (send message, send file, send with button)
- Calendar operations (list, get, create, update, delete events)
- Group operations (create, list, update members)
- File operations (upload, list, duplicate)
- Mail operations (get, send, folder operations)
- Bulletin board operations (create, post)
- External browser settings (enable, disable, get status)
- Bot operations (create talk room)
- Incoming webhook
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class User:
    """LINE WORKS User representation"""
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None

@dataclass
class Event:
    """LINE WORKS Calendar Event representation"""
    event_id: Optional[str] = None
    title: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_all_day: bool = False
    location: Optional[str] = None
    description: Optional[str] = None


class LineWorksOAuthClient:
    """
    LINE WORKS OAuth API client.

    Authentication: OAuth 2.0 (Bearer Token)
    API Docs: https://developers.works.mobile.co.kr/reference
    """

    def __init__(
        self,
        access_token: str,
        api_id: Optional[str] = None,
        base_url: str = "https://www.worksapis.com/v1.0"
    ):
        """
        Initialize LINE WORKS OAuth client.

        Args:
            access_token: OAuth 2.0 Access Token
            api_id: API ID (from LINE WORKS Developer Console)
            base_url: LINE WORKS API base URL
        """
        self.access_token = access_token
        self.api_id = api_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid access token")
            elif response.status_code == 403:
                raise Exception("Forbidden: Insufficient permissions")
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

    # ==================== User Management ====================

    def list_users(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of users.

        Args:
            limit: Number of results
            offset: Pagination offset

        Returns:
            Dict with users list
        """
        params = {"limit": limit, "offset": offset}
        return self._request("GET", "/users", params=params)

    def get_user(self, user_id: str) -> User:
        """
        Get user details by ID.

        Args:
            user_id: User ID

        Returns:
            User object
        """
        result = self._request("GET", f"/users/{user_id}")
        return User(
            user_id=result.get("userId"),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            department=result.get("department"),
            position=result.get("position"),
            status=result.get("status")
        )

    def create_user(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None
    ) -> User:
        """
        Create a new user.

        Args:
            name: User name (required)
            email: User email (required)
            phone: Phone number
            department: Department name
            position: Position/Job title

        Returns:
            User object
        """
        payload: Dict[str, Any] = {
            "name": name,
            "email": email
        }

        if phone:
            payload["phone"] = phone
        if department:
            payload["department"] = department
        if position:
            payload["position"] = position

        result = self._request("POST", "/users", json=payload)
        return User(
            user_id=result.get("userId"),
            name=result.get("name"),
            email=result.get("email")
        )

    def update_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None
    ) -> User:
        """
        Update user information.

        Args:
            user_id: User ID
            name: Updated name
            phone: Updated phone
            department: Updated department
            position: Updated position

        Returns:
            Updated User object
        """
        payload: Dict[str, Any] = {}

        if name:
            payload["name"] = name
        if phone:
            payload["phone"] = phone
        if department:
            payload["department"] = department
        if position:
            payload["position"] = position

        result = self._request("PATCH", f"/users/{user_id}", json=payload)
        return User(
            user_id=result.get("userId"),
            name=result.get("name")
        )

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            Deletion response
        """
        return self._request("DELETE", f"/users/{user_id}")

    def suspend_user(self, user_id: str) -> Dict[str, Any]:
        """
        Suspend a user account.

        Args:
            user_id: User ID

        Returns:
            Response dict
        """
        return self._request("POST", f"/users/{user_id}/suspend")

    def unsuspend_user(self, user_id: str) -> Dict[str, Any]:
        """
        Unsuspend a user account.

        Args:
            user_id: User ID

        Returns:
            Response dict
        """
        return self._request("POST", f"/users/{user_id}/unsuspend")

    # ==================== Message Operations ====================

    def send_message_to_user(
        self,
        user_id: str,
        text: str,
        bot_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message to a specific user.

        Args:
            user_id: Target user ID
            text: Message text
            bot_id: Bot ID (uses default if not specified)

        Returns:
            Response dict
        """
        payload = {
            "content": {"type": "text", "text": text}
        }

        if bot_id:
            payload["botId"] = bot_id

        return self._request("POST", f"/users/{user_id}/messages", json=payload)

    def send_message_to_room(
        self,
        room_id: str,
        text: str,
        bot_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message to a talk room.

        Args:
            room_id: Talk room ID
            text: Message text
            bot_id: Bot ID

        Returns:
            Response dict
        """
        payload = {
            "content": {"type": "text", "text": text}
        }

        if bot_id:
            payload["botId"] = bot_id

        return self._request("POST", f"/rooms/{room_id}/messages", json=payload)

    def send_message_with_button(
        self,
        target_id: str,
        text: str,
        buttons: List[Dict[str, str]],
        is_user: bool = True
    ) -> Dict[str, Any]:
        """
        Send message with button template.

        Args:
            target_id: Target user or room ID
            text: Message text
            buttons: List of button dicts with 'text' and 'type'
            is_user: True if target is user, False if room

        Returns:
            Response dict
        """
        payload = {
            "content": {
                "type": "template",
                "templateType": "buttons",
                "text": text,
                "actions": buttons
            }
        }

        if is_user:
            return self._request("POST", f"/users/{target_id}/messages", json=payload)
        else:
            return self._request("POST", f"/rooms/{target_id}/messages", json=payload)

    def send_message_via_webhook(
        self,
        webhook_url: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Send message via incoming webhook.

        Args:
            webhook_url: Incoming webhook URL
            text: Message text

        Returns:
            Response dict
        """
        payload = {"content": {"type": "text", "text": text}}

        response = self.session.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return response.json() if response.content else {}
        else:
            raise Exception(f"Webhook error {response.status_code}: {response.text}")

    def send_file_to_user(
        self,
        user_id: str,
        file_path: str,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send file to a user.

        Args:
            user_id: Target user ID
            file_path: Path to file
            file_name: Optional file name

        Returns:
            Response dict
        """
        if not file_name:
            import os
            file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {"file": (file_name, f)}
            payload = {"resourceName": file_name}

            return self._request(
                "POST",
                f"/users/{user_id}/files",
                data=payload,
                files=files
            )

    def send_file_to_room(
        self,
        room_id: str,
        file_path: str,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send file to a talk room.

        Args:
            room_id: Talk room ID
            file_path: Path to file
            file_name: Optional file name

        Returns:
            Response dict
        """
        if not file_name:
            import os
            file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {"file": (file_name, f)}
            payload = {"resourceName": file_name}

            return self._request(
                "POST",
                f"/rooms/{room_id}/files",
                data=payload,
                files=files
            )

    # ==================== Calendar Operations ====================

    def list_calendars(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's calendar list.

        Args:
            user_id: User ID

        Returns:
            List of calendars
        """
        return self._request("GET", f"/users/{user_id}/calendars").get("calendars", [])

    def get_calendar_events(
        self,
        calendar_id: str,
        from_date: str,
        to_date: str
    ) -> Dict[str, Any]:
        """
        Get events for a calendar.

        Args:
            calendar_id: Calendar ID
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            Dict with events list
        """
        params = {
            "from": from_date,
            "to": to_date
        }
        return self._request("GET", f"/calendars/{calendar_id}/events", params=params)

    def create_event(
        self,
        calendar_id: str,
        title: str,
        start_time: str,
        end_time: str,
        is_all_day: bool = False,
        location: Optional[str] = None,
        description: Optional[str] = None
    ) -> Event:
        """
        Create a calendar event.

        Args:
            calendar_id: Calendar ID
            title: Event title
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            is_all_day: Whether it's an all-day event
            location: Event location
            description: Event description

        Returns:
            Event object
        """
        payload: Dict[str, Any] = {
            "title": title,
            "start": {"dateTime": start_time} if not is_all_day else {"date": start_time.split("T")[0]},
            "end": {"dateTime": end_time} if not is_all_day else {"date": end_time.split("T")[0]}
        }

        if location:
            payload["location"] = location
        if description:
            payload["description"] = description

        result = self._request("POST", f"/calendars/{calendar_id}/events", json=payload)
        return Event(
            event_id=result.get("uid"),
            title=result.get("title"),
            start_time=result.get("start"),
            end_time=result.get("end"),
            is_all_day=is_all_day,
            location=result.get("location"),
            description=result.get("description")
        )

    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        title: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None
    ) -> Event:
        """
        Update a calendar event.

        Args:
            calendar_id: Calendar ID
            event_id: Event ID
            title: Updated title
            start_time: Updated start time
            end_time: Updated end time
            location: Updated location
            description: Updated description

        Returns:
            Updated Event object
        """
        payload: Dict[str, Any] = {}

        if title:
            payload["title"] = title
        if start_time:
            payload["start"] = {"dateTime": start_time}
        if end_time:
            payload["end"] = {"dateTime": end_time}
        if location:
            payload["location"] = location
        if description:
            payload["description"] = description

        result = self._request("PATCH", f"/calendars/{calendar_id}/events/{event_id}", json=payload)
        return Event(
            event_id=result.get("uid"),
            title=result.get("title")
        )

    def delete_event(self, calendar_id: str, event_id: str) -> Dict[str, Any]:
        """
        Delete a calendar event.

        Args:
            calendar_id: Calendar ID
            event_id: Event ID

        Returns:
            Deletion response
        """
        return self._request("DELETE", f"/calendars/{calendar_id}/events/{event_id}")

    def get_event_detail(self, calendar_id: str, event_id: str) -> Event:
        """
        Get event details.

        Args:
            calendar_id: Calendar ID
            event_id: Event ID

        Returns:
            Event object with details
        """
        result = self._request("GET", f"/calendars/{calendar_id}/events/{event_id}")
        return Event(
            event_id=result.get("uid"),
            title=result.get("title"),
            start_time=result.get("start"),
            end_time=result.get("end"),
            location=result.get("location"),
            description=result.get("description")
        )

    # ==================== Group Operations ====================

    def create_group(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new group.

        Args:
            name: Group name
            description: Group description

        Returns:
            Response dict with group info
        """
        payload: Dict[str, Any] = {"name": name}

        if description:
            payload["description"] = description

        return self._request("POST", "/groups", json=payload)

    def update_group_members(
        self,
        group_id: str,
        add_user_ids: Optional[List[str]] = None,
        remove_user_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update group member list.

        Args:
            group_id: Group ID
            add_user_ids: List of user IDs to add
            remove_user_ids: List of user IDs to remove

        Returns:
            Response dict
        """
        payload: Dict[str, Any] = {}

        if add_user_ids:
            payload["add"] = add_user_ids
        if remove_user_ids:
            payload["remove"] = remove_user_ids

        return self._request("POST", f"/groups/{group_id}/members", json=payload)

    # ==================== File Operations ====================

    def get_upload_url(self, file_name: str, file_size: int) -> Dict[str, Any]:
        """
        Get upload URL for file upload.

        Args:
            file_name: File name
            file_size: File size in bytes

        Returns:
            Dict with upload URL and session key
        """
        payload = {
            "resourceName": file_name,
            "resourceSize": file_size
        }

        return self._request("POST", "/files/upload/url", json=payload)

    def upload_file(self, upload_url: str, file_path: str) -> Dict[str, Any]:
        """
        Upload file using upload URL.

        Args:
            upload_url: Upload URL from get_upload_url
            file_path: Path to file

        Returns:
            Response dict
        """
        import os
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {"file": (file_name, f)}
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                return response.json() if response.content else {}
            else:
                raise Exception(f"Upload failed: {response.status_code}")

    def list_group_files(self, group_id: str, folder_path: Optional[str] = None) -> Dict[str, Any]:
        """
        List files in group root folder.

        Args:
            group_id: Group ID
            folder_path: Optional folder path

        Returns:
            Dict with files list
        """
        params = {}
        if folder_path:
            params["path"] = folder_path

        return self._request("GET", f"/groups/{group_id}/files", params=params)

    def list_group_folder_files(self, group_id: str, folder_id: str) -> Dict[str, Any]:
        """
        List files in a specific group folder.

        Args:
            group_id: Group ID
            folder_id: Folder ID

        Returns:
            Dict with files list
        """
        return self._request("GET", f"/groups/{group_id}/folders/{folder_id}/files")

    def create_group_folder(
        self,
        group_id: str,
        folder_name: str,
        parent_folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a folder in group.

        Args:
            group_id: Group ID
            folder_name: Folder name
            parent_folder_id: Parent folder ID (None for root)

        Returns:
            Response dict with folder info
        """
        payload: Dict[str, Any] = {"name": folder_name}

        if parent_folder_id:
            payload["parentFolderId"] = parent_folder_id

        return self._request("POST", f"/groups/{group_id}/folders", json=payload)

    def duplicate_group_file(
        self,
        group_id: str,
        file_id: str,
        destination_folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Duplicate a file in group.

        Args:
            group_id: Group ID
            file_id: File ID to duplicate
            destination_folder_id: Destination folder ID (None for same folder)

        Returns:
            Response dict
        """
        payload: Dict[str, Any] = {}

        if destination_folder_id:
            payload["destinationFolderId"] = destination_folder_id

        return self._request("POST", f"/groups/{group_id}/files/{file_id}/duplicate", json=payload)

    # ==================== Mail Operations ====================

    def get_mails(
        self,
        folder_path: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get mail list.

        Args:
            folder_path: Mail folder path
            from_date: Start date filter
            to_date: End date filter

        Returns:
            Dict with mail list
        """
        params: Dict[str, Any] = {}

        if folder_path:
            params["folderPath"] = folder_path
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self._request("GET", "/mails", params=params)

    def get_mail(self, mail_id: str) -> Dict[str, Any]:
        """
        Get mail details.

        Args:
            mail_id: Mail ID

        Returns:
            Dict with mail details
        """
        return self._request("GET", f"/mails/{mail_id}")

    def send_mail(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send mail.

        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients

        Returns:
            Response dict
        """
        payload: Dict[str, Any] = {
            "to": to,
            "subject": subject,
            "body": body
        }

        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc

        return self._request("POST", "/mails", json=payload)

    # ==================== Bulletin Board Operations ====================

    def create_bulletin_board(
        self,
        group_id: str,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Create a bulletin board.

        Args:
            group_id: Group ID
            title: Board title
            content: Board content

        Returns:
            Response dict
        """
        payload = {
            "title": title,
            "content": content
        }

        return self._request("POST", f"/groups/{group_id}/bulletinBoards", json=payload)

    def create_bulletin_post(
        self,
        board_id: str,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Create a post in bulletin board.

        Args:
            board_id: Board ID
            title: Post title
            content: Post content

        Returns:
            Response dict
        """
        payload = {
            "title": title,
            "content": content
        }

        return self._request("POST", f"/bulletinBoards/{board_id}/posts", json=payload)

    # ==================== External Browser Settings ====================

    def enable_external_browser(self) -> Dict[str, Any]:
        """
        Enable external browser settings.

        Returns:
            Response dict
        """
        return self._request("POST", "/externalBrowser/enable")

    def disable_external_browser(self) -> Dict[str, Any]:
        """
        Disable external browser settings.

        Returns:
            Response dict
        """
        return self._request("POST", "/externalBrowser/disable")

    def get_external_browser_status(self) -> Dict[str, Any]:
        """
        Get external browser usage status.

        Returns:
            Dict with external browser status
        """
        return self._request("GET", "/externalBrowser/status")

    # ==================== Bot Operations ====================

    def create_bot_talk_room(self, bot_id: str, room_name: str) -> Dict[str, Any]:
        """
        Create a talk room with bot.

        Args:
            bot_id: Bot ID
            room_name: Room name

        Returns:
            Response dict with room ID
        """
        payload = {
            "botId": bot_id,
            "name": room_name
        }

        return self._request("POST", "/bot/rooms", json=payload)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    access_token = "your_line_works_access_token"
    api_id = "your_api_id"

    client = LineWorksOAuthClient(access_token=access_token, api_id=api_id)

    try:
        # List users
        users = client.list_users()
        print(f"Users: {users}")

        # Get user info
        if users.get("users"):
            user = client.get_user(users["users"][0]["userId"])
            print(f"User: {user.name}")

        # Send message to user
        if users.get("users"):
            result = client.send_message_to_user(
                users["users"][0]["userId"],
                "Hello from LINE WORKS!"
            )
            print(f"Message sent: {result}")

        # Get calendar events
        calendars = client.list_calendars(user_id="your_user_id")
        if calendars:
            events = client.get_calendar_events(
                calendars[0]["calendarId"],
                "2024-01-01",
                "2024-01-31"
            )
            print(f"Events: {events}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()