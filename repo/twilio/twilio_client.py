"""
Twilio API Client
API Documentation: https://www.twilio.com/docs/voice/api/ and https://www.twilio.com/docs/sms/api/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import base64


class TwilioAPIError(Exception):
    """Custom exception for Twilio API errors."""
    pass


class TwilioClient:
    """Client for Twilio API - SMS and Voice communication."""

    def __init__(self, account_sid: str, auth_token: str, base_url: Optional[str] = None):
        """
        Initialize Twilio API client.

        Args:
            account_sid: Your Twilio Account SID
            auth_token: Your Twilio Auth Token
            base_url: API base URL (default: https://api.twilio.com)
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.base_url = base_url or "https://api.twilio.com"
        self.session = requests.Session()

        # Basic authentication
        auth_str = f"{account_sid}:{auth_token}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        self.session.headers.update({
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            # Parse XML or JSON response
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = response.json()
            else:
                # Twilio returns XML by default
                data = {"content": response.text, "status_code": response.status_code}

            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise TwilioAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise TwilioAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def send_sms(
        self,
        to: str,
        from_: str,
        body: str,
        messaging_service_sid: Optional[str] = None,
        status_callback: Optional[str] = None,
        media_url: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send an SMS message.

        API Reference: https://www.twilio.com/docs/sms/api/message-resource#create-a-message-resource

        Args:
            to: Phone number to send to (E.164 format, e.g., +819012345678)
            from_: Twilio phone number or messaging service SID to send from
            body: Message body text
            messaging_service_sid: Messaging service SID (overrides from_)
            status_callback: URL for status callback notifications
            media_url: List of media URLs to include in message

        Returns:
            Message creation response with SID and status
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Messages.json"

        data = {
            "To": to,
            "From": from_,
            "Body": body
        }

        if messaging_service_sid:
            data["MessagingServiceSid"] = messaging_service_sid

        if status_callback:
            data["StatusCallback"] = status_callback

        if media_url:
            data["MediaUrl"] = media_url

        return self._make_request("POST", endpoint, data=data)

    def make_call(
        self,
        to: str,
        from_: str,
        url: Optional[str] = None,
        twiml: Optional[str] = None,
        method: str = "POST",
        status_callback: Optional[str] = None,
        status_callback_event: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        record: bool = False,
        recording_url: Optional[str] = None,
        recording_status_callback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make a phone call.

        API Reference: https://www.twilio.com/docs/voice/api/call-resource#create-a-call-resource

        Args:
            to: Phone number to call (E.164 format)
            from_: Twilio phone number to call from
            url: URL that contains TwiML instructions
            twiml: TwiML instructions as string
            method: HTTP method to use for URL request
            status_callback: URL for status callback notifications
            status_callback_event: List of events to trigger callback
            timeout: Time in seconds to wait for answer
            record: Whether to record the call
            recording_url: URL to send recording information
            recording_status_callback: URL for recording status callback

        Returns:
            Call creation response with SID and status
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Calls.json"

        if not url and not twiml:
            raise TwilioAPIError("Either 'url' or 'twiml' parameter is required")

        data = {
            "To": to,
            "From": from_,
            "Method": method.upper()
        }

        if url:
            data["Url"] = url
        if twiml:
            data["Twiml"] = twiml

        if status_callback:
            data["StatusCallback"] = status_callback

        if status_callback_event:
            data["StatusCallbackEvent"] = ",".join(status_callback_event)

        if timeout is not None:
            data["Timeout"] = str(timeout)

        data["Record"] = "true" if record else "false"

        if recording_url:
            data["RecordingUrl"] = recording_url

        if recording_status_callback:
            data["RecordingStatusCallback"] = recording_status_callback

        return self._make_request("POST", endpoint, data=data)

    def get_message(self, message_sid: str) -> Dict[str, Any]:
        """
        Retrieve message details.

        API Reference: https://www.twilio.com/docs/sms/api/message-resource#fetch-a-message-resource

        Args:
            message_sid: Message SID

        Returns:
            Message details
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Messages/{message_sid}.json"
        return self._make_request("GET", endpoint)

    def get_call(self, call_sid: str) -> Dict[str, Any]:
        """
        Retrieve call details.

        API Reference: https://www.twilio.com/docs/voice/api/call-resource#fetch-a-call-resource

        Args:
            call_sid: Call SID

        Returns:
            Call details
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Calls/{call_sid}.json"
        return self._make_request("GET", endpoint)

    def list_messages(
        self,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        date_sent: Optional[datetime] = None,
        date_sent_before: Optional[datetime] = None,
        date_sent_after: Optional[datetime] = None,
        limit: int = 20,
        page_size: int = 50
    ) -> Dict[str, Any]:
        """
        List sent messages.

        API Reference: https://www.twilio.com/docs/sms/api/message-resource#read-multiple-message-resources

        Args:
            to: Filter by recipient phone number
            from_: Filter by sender phone number
            date_sent: Filter by exact date sent
            date_sent_before: Filter messages sent before this date
            date_sent_after: Filter messages sent after this date
            limit: Maximum number of results to return (max 1000)
            page_size: Number of results per page (max 1000)

        Returns:
            List of messages
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Messages.json"

        params = {
            "PageSize": min(page_size, 1000),
            "Limit": min(limit, 1000)
        }

        if to:
            params["To"] = to
        if from_:
            params["From"] = from_

        if date_sent:
            params["DateSent"] = date_sent.strftime("%Y-%m-%d")
        if date_sent_before:
            params["DateSent<"] = date_sent_before.strftime("%Y-%m-%d")
        if date_sent_after:
            params["DateSent>"] = date_sent_after.strftime("%Y-%m-%d")

        return self._make_request("GET", endpoint, params=params)

    def list_calls(
        self,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 20,
        page_size: int = 50
    ) -> Dict[str, Any]:
        """
        List calls.

        API Reference: https://www.twilio.com/docs/voice/api/call-resource#read-multiple-call-resources

        Args:
            to: Filter by recipient phone number
            from_: Filter by caller phone number
            status: Filter by call status (queued, ringing, in-progress, completed, failed, etc.)
            start_time: Filter calls started after this time
            end_time: Filter calls started before this time
            limit: Maximum number of results to return (max 1000)
            page_size: Number of results per page (max 1000)

        Returns:
            List of calls
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Calls.json"

        params = {
            "PageSize": min(page_size, 1000),
            "Limit": min(limit, 1000)
        }

        if to:
            params["To"] = to
        if from_:
            params["From"] = from_
        if status:
            params["Status"] = status

        if start_time:
            params["StartTime>"] = start_time.strftime("%Y-%m-%d")
        if end_time:
            params["StartTime<"] = end_time.strftime("%Y-%m-%d")

        return self._make_request("GET", endpoint, params=params)

    def get_call_recording(self, recording_sid: str) -> Dict[str, Any]:
        """
        Get call recording details.

        API Reference: https://www.twilio.com/docs/voice/api/recording-resource#fetch-a-recording-resource

        Args:
            recording_sid: Recording SID

        Returns:
            Recording details
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Recordings/{recording_sid}.json"
        return self._make_request("GET", endpoint)

    def delete_call_recording(self, recording_sid: str) -> Dict[str, Any]:
        """
        Delete a call recording.

        API Reference: https://www.twilio.com/docs/voice/api/recording-resource#delete-a-recording-resource

        Args:
            recording_sid: Recording SID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/2010-04-01/Accounts/{self.account_sid}/Recordings/{recording_sid}.json"
        return self._make_request("DELETE", endpoint)