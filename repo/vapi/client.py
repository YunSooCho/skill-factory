"""
Vapi API Client - Voice Call Automation
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, List, Union, BinaryIO


class VapiError(Exception):
    """Base exception for Vapi errors"""
    pass


class VapiRateLimitError(VapiError):
    """Rate limit exceeded"""
    pass


class VapiAuthenticationError(VapiError):
    """Authentication failed"""
    pass


class VapiClient:
    """Client for Vapi Voice Call Automation API"""

    BASE_URL = "https://api.vapi.ai/v1"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Vapi client

        Args:
            api_key: Vapi API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if response.status_code == 429:
            raise VapiRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise VapiAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise VapiError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def create_outbound_call(self, phone_number: str, assistant_id: str,
                              name: Optional[str] = None,
                              customer_name: Optional[str] = None,
                              metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create an outbound call

        Args:
            phone_number: Phone number to call
            assistant_id: Assistant ID to use
            name: Call name (optional)
            customer_name: Customer name (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dictionary containing call details

        Raises:
            VapiError: If call creation fails
        """
        self._enforce_rate_limit()

        payload = {
            "phoneNumber": phone_number,
            "assistantId": assistant_id
        }

        if name:
            payload["name"] = name

        if customer_name:
            payload["customer"]["name"] = customer_name

        if metadata:
            payload["metadata"] = metadata

        try:
            response = self.session.post(
                f"{self.BASE_URL}/call",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")

    def search_calls(self, limit: int = 20, offset: int = 0,
                     status: Optional[str] = None,
                     assistant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for calls

        Args:
            limit: Number of results
            offset: Pagination offset
            status: Filter by status (optional)
            assistant_id: Filter by assistant (optional)

        Returns:
            Dictionary containing call search results

        Raises:
            VapiError: If search fails
        """
        self._enforce_rate_limit()

        params = {"limit": limit, "offset": offset}

        if status:
            params["status"] = status

        if assistant_id:
            params["assistantId"] = assistant_id

        try:
            response = self.session.get(
                f"{self.BASE_URL}/calls",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")

    def search_logs(self, call_id: Optional[str] = None,
                    level: Optional[str] = None,
                    limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Search for call logs

        Args:
            call_id: Filter by call ID (optional)
            level: Filter by log level (optional)
            limit: Number of results
            offset: Pagination offset

        Returns:
            Dictionary containing log search results

        Raises:
            VapiError: If search fails
        """
        self._enforce_rate_limit()

        params = {"limit": limit, "offset": offset}

        if call_id:
            params["callId"] = call_id

        if level:
            params["level"] = level

        try:
            response = self.session.get(
                f"{self.BASE_URL}/logs",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")

    def search_data_analytics(self, start_date: str, end_date: str,
                               metrics: Optional[List[str]] = None,
                               group_by: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for data analytics

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            metrics: List of metrics to retrieve (optional)
            group_by: Field to group by (optional)

        Returns:
            Dictionary containing analytics data

        Raises:
            VapiError: If search fails
        """
        self._enforce_rate_limit()

        params = {
            "startDate": start_date,
            "endDate": end_date
        }

        if metrics:
            params["metrics"] = ",".join(metrics)

        if group_by:
            params["groupBy"] = group_by

        try:
            response = self.session.get(
                f"{self.BASE_URL}/analytics",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")

    def upload_file(self, file: Union[str, bytes, BinaryIO],
                    file_type: str = "audio",
                    name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file

        Args:
            file: File to upload (path, bytes, or file object)
            file_type: File type (audio, text, etc.)
            name: File name (optional)

        Returns:
            Dictionary containing upload result

        Raises:
            VapiError: If upload fails
        """
        self._enforce_rate_limit()

        payload = {
            "type": file_type
        }

        if name:
            payload["name"] = name

        if isinstance(file, str):
            try:
                with open(file, 'rb') as f:
                    file_b64 = base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                raise VapiError(f"Failed to read file: {str(e)}")
        elif isinstance(file, bytes):
            file_b64 = base64.b64encode(file).decode('utf-8')
        else:
            file_b64 = base64.b64encode(file.read()).decode('utf-8')

        payload["file"] = f"data:audio/mpeg;base64,{file_b64}"

        try:
            response = self.session.post(
                f"{self.BASE_URL}/files",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")

    def get_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get details of a call

        Args:
            call_id: Call ID to retrieve

        Returns:
            Dictionary containing call details

        Raises:
            VapiError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/call/{call_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VapiError(f"Request failed: {str(e)}")