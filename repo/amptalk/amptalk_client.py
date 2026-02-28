"""
Amptalk API Client

Supports 5 API actions for call analysis operations:
- Get call summary (通話の要約を取得)
- Get analysis information (分析情報を取得)
- Get user list (ユーザーの一覧を取得)
- Search calls (通話を検索)
- Get call details (通話を取得)

And 1 trigger:
- Call completed (通話が完了したら)

API Reference: https://api.amptalk.ai (based on service name)
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class CallSummary:
    """Call summary representation"""
    call_id: Optional[str] = None
    participants: Optional[List[str]] = None
    duration: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    summary: Optional[str] = None
    key_topics: Optional[List[str]] = None
    sentiment: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class CallAnalysis:
    """Call analysis information"""
    call_id: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    keywords: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    action_items: Optional[List[Dict[str, Any]]] = None
    speaker_analysis: Optional[Dict[str, Any]] = None
    transcript_length: Optional[int] = None
    language: Optional[str] = None


@dataclass
class Call:
    """Call record representation"""
    id: Optional[str] = None
    phone_number: Optional[str] = None
    direction: Optional[str] = None
    duration: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    recording_url: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None


class AmptalkClient:
    """
    Amptalk API client for call analysis operations.

    Authentication: API Key (Header: X-API-Key: {api_key})
    Base URL: https://api.amptalk.ai
    """

    BASE_URL = "https://api.amptalk.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Amptalk client.

        Args:
            api_key: Amptalk API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
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

    # ==================== Call Operations ====================

    def get_call(self, call_id: str) -> Call:
        """
        Get call details by ID.
        通話を取得

        Args:
            call_id: Call ID

        Returns:
            Call object
        """
        if not call_id:
            raise ValueError("Call ID is required")

        result = self._request("GET", f"/calls/{call_id}")
        return self._parse_call(result)

    def search_calls(
        self,
        phone_number: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Call]:
        """
        Search calls with filters.
        通話を検索

        Args:
            phone_number: Filter by phone number
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)
            status: Filter by status (e.g., 'completed', 'missed')
            user_id: Filter by user ID
            limit: Maximum results to return

        Returns:
            List of Call objects
        """
        params = {}
        if phone_number:
            params["phone_number"] = phone_number
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if status:
            params["status"] = status
        if user_id:
            params["user_id"] = user_id
        params["limit"] = limit

        result = self._request("GET", "/calls", params=params)

        calls = []
        if isinstance(result, dict) and "data" in result:
            for call_data in result.get("data", []):
                calls.append(self._parse_call(call_data))
        elif isinstance(result, list):
            for call_data in result:
                calls.append(self._parse_call(call_data))

        return calls

    def get_call_summary(self, call_id: str) -> CallSummary:
        """
        Get AI-generated call summary.
        通話の要約を取得

        Args:
            call_id: Call ID

        Returns:
            CallSummary object
        """
        if not call_id:
            raise ValueError("Call ID is required")

        result = self._request("GET", f"/calls/{call_id}/summary")
        return self._parse_call_summary(result)

    def get_call_analysis(self, call_id: str) -> CallAnalysis:
        """
        Get detailed call analysis information.
        分析情報を取得

        Args:
            call_id: Call ID

        Returns:
            CallAnalysis object
        """
        if not call_id:
            raise ValueError("Call ID is required")

        result = self._request("GET", f"/calls/{call_id}/analysis")
        return self._parse_call_analysis(result)

    # ==================== User Operations ====================

    def get_users(self, limit: int = 100) -> List[User]:
        """
        Get list of users.
        ユーザーの一覧を取得

        Args:
            limit: Maximum results to return

        Returns:
            List of User objects
        """
        params = {"limit": limit}
        result = self._request("GET", "/users", params=params)

        users = []
        if isinstance(result, dict) and "data" in result:
            for user_data in result.get("data", []):
                users.append(self._parse_user(user_data))
        elif isinstance(result, list):
            for user_data in result:
                users.append(self._parse_user(user_data))

        return users

    # ==================== Webhook/Trigger Support ====================

    def register_webhook(
        self,
        callback_url: str,
        events: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Register webhook for event notifications.
        通話が完了したら (Call completed trigger)

        Args:
            callback_url: Your webhook endpoint URL
            events: List of events to subscribe to (e.g., ['call.completed'])

        Returns:
            Webhook registration response
        """
        if not callback_url:
            raise ValueError("Callback URL is required")

        if events is None:
            events = ["call.completed"]

        payload = {
            "callback_url": callback_url,
            "events": events
        }

        return self._request("POST", "/webhooks", json=payload)

    def delete_webhook(self, webhook_id: str) -> None:
        """
        Delete webhook registration.

        Args:
            webhook_id: Webhook ID to delete
        """
        self._request("DELETE", f"/webhooks/{webhook_id}")

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """
        Get list of registered webhooks.

        Returns:
            List of webhook registrations
        """
        result = self._request("GET", "/webhooks")

        if isinstance(result, dict) and "data" in result:
            return result.get("data", [])
        elif isinstance(result, list):
            return result

        return []

    # ==================== Helper Methods ====================

    def _parse_call(self, data: Dict[str, Any]) -> Call:
        """Parse call data from API response"""
        return Call(
            id=data.get("id"),
            phone_number=data.get("phone_number"),
            direction=data.get("direction"),
            duration=data.get("duration"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            recording_url=data.get("recording_url"),
            status=data.get("status"),
            user_id=data.get("user_id"),
            tags=data.get("tags", []),
            created_at=data.get("created_at")
        )

    def _parse_call_summary(self, data: Dict[str, Any]) -> CallSummary:
        """Parse call summary data from API response"""
        return CallSummary(
            call_id=data.get("call_id"),
            participants=data.get("participants", []),
            duration=data.get("duration"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            summary=data.get("summary"),
            key_topics=data.get("key_topics", []),
            sentiment=data.get("sentiment"),
            created_at=data.get("created_at")
        )

    def _parse_call_analysis(self, data: Dict[str, Any]) -> CallAnalysis:
        """Parse call analysis data from API response"""
        return CallAnalysis(
            call_id=data.get("call_id"),
            sentiment_score=data.get("sentiment_score"),
            sentiment_label=data.get("sentiment_label"),
            keywords=data.get("keywords", []),
            topics=data.get("topics", []),
            action_items=data.get("action_items", []),
            speaker_analysis=data.get("speaker_analysis", {}),
            transcript_length=data.get("transcript_length"),
            language=data.get("language")
        )

    def _parse_user(self, data: Dict[str, Any]) -> User:
        """Parse user data from API response"""
        return User(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            role=data.get("role"),
            created_at=data.get("created_at")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_amptalk_api_key"

    client = AmptalkClient(api_key=api_key)

    try:
        # Example: Get user list
        users = client.get_users()
        print(f"Found {len(users)} users")

        # Example: Search calls
        calls = client.search_calls(
            status="completed",
            limit=10
        )
        print(f"Found {len(calls)} calls")

        if calls:
            # Example: Get call summary
            call_summary = client.get_call_summary(calls[0].id)
            print(f"Call summary: {call_summary.summary[:100]}...")

            # Example: Get call analysis
            call_analysis = client.get_call_analysis(calls[0].id)
            print(f"Sentiment: {call_analysis.sentiment_label}")
            print(f"Keywords: {', '.join(call_analysis.keywords[:5])}")

        # Example: Register webhook for call completed events
        webhook = client.register_webhook(
            callback_url="https://your-server.com/webhook",
            events=["call.completed"]
        )
        print(f"Webhook registered: {webhook.get('id')}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()