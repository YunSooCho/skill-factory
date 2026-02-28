"""
Gmail API - Email Management Client

Supports:
- Search Emails
- Get Specific Message
- Add Labels to Message
- Remove Labels from Message
- Move Message to Trash
- Handle Webhook (for triggers)
"""

import aiohttp
import json
import base64
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Message:
    """Gmail message object"""
    id: str
    thread_id: str
    subject: str
    from_email: str
    to_email: Optional[str] = None
    date: Optional[str] = None
    body: Optional[str] = None
    snippet: Optional[str] = None
    labels: List[str] = None
    is_unread: bool = False
    is_starred: bool = False

    def __post_init__(self):
        if self.labels is None:
            self.labels = []


@dataclass
class Label:
    """Gmail label object"""
    id: str
    name: str
    message_list_visibility: str
    label_list_visibility: str


@dataclass
class WebhookEvent:
    """Webhook event object"""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    message_id: Optional[str] = None


class GmailClient:
    """
    Gmail API client for email management.

    Provides operations for searching, retrieving, and managing
    emails and labels in Gmail.

    API Documentation: https://lp.yoom.fun/apps/gmail
    Requires:
    - Google Cloud project with Gmail API enabled
    - OAuth credentials or service account
    """

    BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me"

    def __init__(
        self,
        access_token: str,
        webhook_secret: Optional[str] = None
    ):
        """
        Initialize Gmail client.

        Args:
            access_token: OAuth access token
            webhook_secret: Optional secret for webhook signature verification
        """
        self.access_token = access_token
        self.webhook_secret = webhook_secret
        self.session = None
        self._rate_limit_delay = 0.1

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                json=json_data
            ) as response:
                if response.status == 204:
                    return {}

                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Gmail API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            # Some operations return empty responses
            if response.status in [200, 204]:
                return {}
            raise Exception("Invalid JSON response")

    def _decode_base64(self, data: str) -> str:
        """Decode base64 string."""
        try:
            # URL-safe base64 decode
            padding = 4 - len(data) % 4
            if padding != 4:
                data += "=" * padding
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        except Exception:
            return ""

    # ==================== Search Emails ====================

    async def search_emails(
        self,
        query: str,
        max_results: int = 10,
        label_ids: Optional[List[str]] = None
    ) -> List[Message]:
        """
        Search for emails.

        Args:
            query: Search query (Gmail search syntax)
            max_results: Maximum number of results to return
            label_ids: Filter by label IDs

        Returns:
            List of Message objects

        Raises:
            Exception: If search fails
        """
        params = {
            "q": query,
            "maxResults": max_results
        }

        if label_ids:
            params["labelIds"] = label_ids

        response_data = await self._make_request(
            "GET",
            "/messages",
            params=params
        )

        messages_list = response_data.get("messages", [])
        messages = []

        # Fetch full message details for each
        for msg in messages_list:
            try:
                full_message = await self.get_message(msg["id"])
                messages.append(full_message)
            except Exception:
                continue

        return messages

    async def list_messages(
        self,
        max_results: int = 10,
        label_ids: Optional[List[str]] = None,
        include_spam_trash: bool = False
    ) -> List[Message]:
        """
        List messages in the mailbox.

        Args:
            max_results: Maximum number of results
            label_ids: Filter by label IDs
            include_spam_trash: Include messages in spam and trash

        Returns:
            List of Message objects

        Raises:
            Exception: If request fails
        """
        params = {
            "maxResults": max_results
        }

        if label_ids:
            params["labelIds"] = label_ids
        if include_spam_trash:
            params["includeSpamTrash"] = "true"

        response_data = await self._make_request(
            "GET",
            "/messages",
            params=params
        )

        messages_list = response_data.get("messages", [])
        messages = []

        for msg in messages_list:
            try:
                full_message = await self.get_message(msg["id"])
                messages.append(full_message)
            except Exception:
                continue

        return messages

    # ==================== Get Specific Message ====================

    async def get_message(
        self,
        message_id: str,
        format: str = "full"
    ) -> Message:
        """
        Get details of a specific message.

        Args:
            message_id: Message ID
            format: Format of the message (minimal, raw, full)

        Returns:
            Message object with full details

        Raises:
            Exception: If retrieval fails
            ValueError: If message_id is empty
        """
        if not message_id:
            raise ValueError("message_id is required")

        params = {"format": format}

        response_data = await self._make_request(
            "GET",
            f"/messages/{message_id}",
            params=params
        )

        # Parse message headers
        headers = {}
        payload = response_data.get("payload", {})
        headers_list = payload.get("headers", [])

        for header in headers_list:
            name = header.get("name", "").lower()
            if name:
                headers[name] = header.get("value", "")

        # Extract body
        body = ""
        if "body" in payload and "data" in payload["body"]:
            body = self._decode_base64(payload["body"]["data"])
        elif "parts" in payload:
            # Multipart message
            for part in payload["parts"]:
                if "body" in part and "data" in part["body"]:
                    body += self._decode_base64(part["body"]["data"])

        # Extract labels
        label_ids = response_data.get("labelIds", [])
        is_unread = "UNREAD" in label_ids
        is_starred = "STARRED" in label_ids

        return Message(
            id=response_data.get("id", ""),
            thread_id=response_data.get("threadId", ""),
            subject=headers.get("subject", ""),
            from_email=headers.get("from", ""),
            to_email=headers.get("to"),
            date=headers.get("date"),
            body=body,
            snippet=response_data.get("snippet", ""),
            labels=label_ids,
            is_unread=is_unread,
            is_starred=is_starred
        )

    async def get_message_raw(self, message_id: str) -> str:
        """
        Get raw message content.

        Args:
            message_id: Message ID

        Returns:
            Raw message as string

        Raises:
            Exception: If retrieval fails
        """
        response_data = await self._make_request(
            "GET",
            f"/messages/{message_id}",
            params={"format": "raw"}
        )

        raw_data = response_data.get("raw", "")
        return self._decode_base64(raw_data)

    async def get_thread(self, thread_id: str) -> List[Message]:
        """
        Get all messages in a thread.

        Args:
            thread_id: Thread ID

        Returns:
            List of Message objects

        Raises:
            Exception: If retrieval fails
        """
        response_data = await self._make_request(
            "GET",
            f"/threads/{thread_id}",
            params={"format": "full"}
        )

        messages_list = response_data.get("messages", [])
        messages = []

        for msg in messages_list:
            try:
                full_message = await self.get_message(msg["id"])
                messages.append(full_message)
            except Exception:
                continue

        return messages

    # ==================== Add Labels to Message ====================

    async def add_labels_to_message(
        self,
        message_id: str,
        label_ids: List[str]
    ) -> Message:
        """
        Add labels to a message.

        Args:
            message_id: Message ID
            label_ids: List of label IDs to add

        Returns:
            Updated Message object

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not message_id:
            raise ValueError("message_id is required")
        if not label_ids:
            raise ValueError("label_ids is required")

        payload = {"addLabelIds": label_ids}

        response_data = await self._make_request(
            "POST",
            f"/messages/{message_id}/modify",
            json_data=payload
        )

        return await self.get_message(response_data.get("id", message_id))

    # ==================== Remove Labels from Message ====================

    async def remove_labels_from_message(
        self,
        message_id: str,
        label_ids: List[str]
    ) -> Message:
        """
        Remove labels from a message.

        Args:
            message_id: Message ID
            label_ids: List of label IDs to remove

        Returns:
            Updated Message object

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not message_id:
            raise ValueError("message_id is required")
        if not label_ids:
            raise ValueError("label_ids is required")

        payload = {"removeLabelIds": label_ids}

        response_data = await self._make_request(
            "POST",
            f"/messages/{message_id}/modify",
            json_data=payload
        )

        return await self.get_message(response_data.get("id", message_id))

    async def modify_message_labels(
        self,
        message_id: str,
        add_label_ids: Optional[List[str]] = None,
        remove_label_ids: Optional[List[str]] = None
    ) -> Message:
        """
        Modify labels on a message.

        Args:
            message_id: Message ID
            add_label_ids: Labels to add
            remove_label_ids: Labels to remove

        Returns:
            Updated Message object

        Raises:
            Exception: If operation fails
        """
        payload = {}

        if add_label_ids:
            payload["addLabelIds"] = add_label_ids
        if remove_label_ids:
            payload["removeLabelIds"] = remove_label_ids

        response_data = await self._make_request(
            "POST",
            f"/messages/{message_id}/modify",
            json_data=payload
        )

        return await self.get_message(response_data.get("id", message_id))

    # ==================== Move Message to Trash ====================

    async def move_message_to_trash(self, message_id: str) -> Message:
        """
        Move a message to trash.

        Args:
            message_id: Message ID to move

        Returns:
            Updated Message object

        Raises:
            Exception: If operation fails
            ValueError: If message_id is empty
        """
        if not message_id:
            raise ValueError("message_id is required")

        response_data = await self._make_request(
            "POST",
            f"/messages/{message_id}/trash"
        )

        return await self.get_message(response_data.get("id", message_id))

    async def delete_message_permanently(self, message_id: str) -> None:
        """
        Permanently delete a message.

        Args:
            message_id: Message ID to delete

        Raises:
            Exception: If deletion fails
        """
        await self._make_request(
            "DELETE",
            f"/messages/{message_id}"
        )

    async def untrash_message(self, message_id: str) -> Message:
        """
        Move message out of trash.

        Args:
            message_id: Message ID to untrash

        Returns:
            Updated Message object

        Raises:
            Exception: If operation fails
        """
        response_data = await self._make_request(
            "POST",
            f"/messages/{message_id}/untrash"
        )

        return await self.get_message(response_data.get("id", message_id))

    # ==================== Label Operations ====================

    async def list_labels(self) -> List[Label]:
        """
        List all labels.

        Returns:
            List of Label objects

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            "/labels"
        )

        labels_list = response_data.get("labels", [])

        return [
            Label(
                id=label.get("id", ""),
                name=label.get("name", ""),
                message_list_visibility=label.get("messageListVisibility", ""),
                label_list_visibility=label.get("labelListVisibility", "")
            )
            for label in labels_list
        ]

    async def get_label(self, label_id: str) -> Optional[Label]:
        """
        Get details of a specific label.

        Args:
            label_id: Label ID

        Returns:
            Label object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/labels/{label_id}"
            )

            return Label(
                id=response_data.get("id", ""),
                name=response_data.get("name", ""),
                message_list_visibility=response_data.get("messageListVisibility", ""),
                label_list_visibility=response_data.get("labelListVisibility", "")
            )

        except Exception:
            return None

    # ==================== Webhook Handling ====================

    async def handle_webhook(
        self,
        payload: bytes,
        signature: Optional[str] = None
    ) -> WebhookEvent:
        """
        Handle incoming webhook events.

        Supported events:
        - email_received_with_label: When email with specific label is received
        - email_received_with_keyword: When email matching keyword is received

        Args:
            payload: Raw webhook payload
            signature: Optional signature for verification

        Returns:
            WebhookEvent object

        Raises:
            Exception: If webhook is invalid or verification fails
        """
        # Verify signature if secret is configured
        if self.webhook_secret and signature:
            import hmac
            import hashlib

            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, signature):
                raise Exception("Invalid webhook signature")

        try:
            event_data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid webhook payload: {str(e)}")

        # Parse Gmail notification format
        email_address = event_data.get("emailAddress")
        history_id = event_data.get("historyId")

        # If we have history ID, we can fetch the changes
        message_id = event_data.get("messageId")

        return WebhookEvent(
            event_type=event_data.get("eventType", "email_received"),
            timestamp=event_data.get("timestamp", datetime.utcnow().isoformat()),
            data={
                "email_address": email_address,
                "history_id": history_id
            },
            message_id=message_id
        )

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Raw webhook payload
            signature: Signature to verify

        Returns:
            True if signature is valid, False otherwise
        """
        if not self.webhook_secret:
            return False

        import hmac
        import hashlib

        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# ==================== Example Usage ====================

async def main():
    """Example usage of Gmail client"""

    # Replace with your actual OAuth access token
    ACCESS_TOKEN = "your_oauth_access_token"

    async with GmailClient(access_token=ACCESS_TOKEN) as client:
        try:
            # Search emails
            results = await client.search_emails(
                query="from:example.com important",
                max_results=5
            )
            print(f"Found {len(results)} emails")
            for msg in results[:3]:
                print(f"  - {msg.subject} from {msg.from_email}")

            # Get specific message
            if results:
                message = await client.get_message(results[0].id)
                print(f"\nMessage: {message.subject}")
                print(f"Body: {message.body[:200]}...")

            # List labels
            labels = await client.list_labels()
            print(f"\nLabels: {len(labels)}")
            for label in labels[:5]:
                print(f"  - {label.name} ({label.id})")

            # Add label to message
            if results:
                updated = await client.add_labels_to_message(
                    results[0].id,
                    ["IMPORTANT"]
                )
                print(f"\nAdded labels to message: {updated.labels}")

                # Remove label
                updated = await client.remove_labels_from_message(
                    results[0].id,
                    ["IMPORTANT"]
                )
                print(f"Removed labels: {updated.labels}")

            # Move to trash
            if results:
                trashed = await client.move_message_to_trash(results[0].id)
                print(f"Moved to trash: {trashed.is_unread}")

                # Untrash
                untrashed = await client.untrash_message(results[0].id)
                print(f"Recovered from trash")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())