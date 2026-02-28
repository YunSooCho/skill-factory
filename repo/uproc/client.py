"""
Uproc API Client - Data Processing Service
"""

import requests
import time
from typing import Optional, Dict, Any, List


class UprocError(Exception):
    """Base exception for Uproc errors"""
    pass


class UprocRateLimitError(UprocError):
    """Rate limit exceeded"""
    pass


class UprocAuthenticationError(UprocError):
    """Authentication failed"""
    pass


class UprocClient:
    """Client for Uproc Data Processing API"""

    BASE_URL = "https://api.uproc.com/v1"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Uproc client

        Args:
            api_key: Uproc API key
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
            raise UprocRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise UprocAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise UprocError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def process_row(self, row_data: Dict[str, Any],
                    process_type: str = "standard",
                    **kwargs) -> Dict[str, Any]:
        """
        Process a single row of data

        Args:
            row_data: Dictionary containing row data to process
            process_type: Type of processing (default: "standard")
            **kwargs: Additional processing parameters

        Returns:
            Dictionary containing processed results

        Raises:
            UprocError: If processing fails
        """
        self._enforce_rate_limit()

        payload = {
            "row": row_data,
            "process_type": process_type
        }
        payload.update(kwargs)

        try:
            response = self.session.post(
                f"{self.BASE_URL}/process",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise UprocError(f"Request failed: {str(e)}")

    def process_multiple_rows(self, rows: List[Dict[str, Any]],
                               process_type: str = "batch",
                               **kwargs) -> Dict[str, Any]:
        """
        Process multiple rows of data

        Args:
            rows: List of dictionaries containing row data to process
            process_type: Type of batch processing (default: "batch")
            **kwargs: Additional processing parameters

        Returns:
            Dictionary containing batch processing results

        Raises:
            UprocError: If processing fails
        """
        self._enforce_rate_limit()

        payload = {
            "rows": rows,
            "process_type": process_type
        }
        payload.update(kwargs)

        try:
            response = self.session.post(
                f"{self.BASE_URL}/process/batch",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise UprocError(f"Request failed: {str(e)}")

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a processing job

        Args:
            job_id: Job ID to check

        Returns:
            Dictionary containing job status

        Raises:
            UprocError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/jobs/{job_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise UprocError(f"Request failed: {str(e)}")