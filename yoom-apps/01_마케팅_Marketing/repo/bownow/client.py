"""
BoNow API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BoNowAPIError(Exception):
    """Base exception for BoNow API errors"""
    pass


class BoNowAuthError(BoNowAPIError):
    """Authentication error"""
    pass


class BoNowRateLimitError(BoNowAPIError):
    """Rate limit exceeded"""
    pass


class BoNowClient:
    """BoNow API Client for lead management"""

    BASE_URL = "https://api.bownow.jp/v1"

    def __init__(self, api_key: str, secret_token: Optional[str] = None):
        """
        Initialize BoNow client

        Args:
            api_key: Your BoNow API key
            secret_token: Optional secret token for additional security
        """
        self.api_key = api_key
        self.secret_token = secret_token
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        })
        if secret_token:
            self.session.headers["X-Secret-Token"] = secret_token

    # ===== Lead Management =====

    def create_lead(
        self,
        email: str,
        name: Optional[str] = None,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        memo: Optional[str] = None,
        reference_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new lead

        Args:
            email: Lead email (required)
            name: Lead name
            company: Company name
            phone: Phone number
            status: Lead status
            tags: List of tags
            custom_fields: Custom field key-value pairs
            memo: Memo/notes
            reference_url: Reference URL where lead came from

        Returns:
            Created lead data
        """
        endpoint = f"{self.BASE_URL}/leads"
        payload = {"email": email}

        if name:
            payload["name"] = name
        if company:
            payload["company"] = company
        if phone:
            payload["phone"] = phone
        if status:
            payload["status"] = status
        if tags:
            payload["tags"] = tags
        if memo:
            payload["memo"] = memo
        if reference_url:
            payload["reference_url"] = reference_url
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_lead(
        self,
        lead_id: str,
    ) -> Dict[str, Any]:
        """
        Retrieve a single lead

        Args:
            lead_id: Lead ID

        Returns:
            Lead data
        """
        endpoint = f"{self.BASE_URL}/leads/{lead_id}"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def search_leads(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        company: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for leads

        Args:
            email: Filter by email
            name: Filter by name (partial match)
            company: Filter by company
            status: Filter by status
            tags: Filter by tags
            offset: Result offset
            limit: Maximum number of results

        Returns:
            List of leads
        """
        endpoint = f"{self.BASE_URL}/leads"
        params = {}

        if email:
            params["email"] = email
        if name:
            params["name"] = name
        if company:
            params["company"] = company
        if status:
            params["status"] = status
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if tags:
            params["tags"] = ",".join(tags)

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("leads", data.get("data", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_lead(
        self,
        lead_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        memo: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update lead information

        Args:
            lead_id: Lead ID
            email: Updated email
            name: Updated name
            company: Updated company
            phone: Updated phone
            status: Updated status
            tags: Updated tags
            custom_fields: Updated custom fields
            memo: Updated memo

        Returns:
            Updated lead data
        """
        endpoint = f"{self.BASE_URL}/leads/{lead_id}"
        payload = {}

        if email:
            payload["email"] = email
        if name:
            payload["name"] = name
        if company:
            payload["company"] = company
        if phone:
            payload["phone"] = phone
        if status:
            payload["status"] = status
        if tags:
            payload["tags"] = tags
        if memo:
            payload["memo"] = memo
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            response = self.session.put(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_lead(
        self,
        lead_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a lead

        Args:
            lead_id: Lead ID

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/leads/{lead_id}"

        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Tag Management =====

    def add_tags_to_lead(
        self,
        lead_id: str,
        tags: List[str],
    ) -> Dict[str, Any]:
        """
        Add tags to a lead

        Args:
            lead_id: Lead ID
            tags: List of tags to add

        Returns:
            Updated lead data
        """
        endpoint = f"{self.BASE_URL}/leads/{lead_id}/tags"
        payload = {"tags": tags}

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def remove_tags_from_lead(
        self,
        lead_id: str,
        tags: List[str],
    ) -> Dict[str, Any]:
        """
        Remove tags from a lead

        Args:
            lead_id: Lead ID
            tags: List of tags to remove

        Returns:
            Updated lead data
        """
        endpoint = f"{self.BASE_URL}/leads/{lead_id}/tags"
        payload = {"tags": tags, "action": "remove"}

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Status Management =====

    def get_statuses(self) -> List[Dict[str, Any]]:
        """
        Get all available statuses

        Returns:
            List of statuses
        """
        endpoint = f"{self.BASE_URL}/statuses"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            return data.get("statuses", data.get("data", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BoNowAuthError("Invalid API key or secret token")
        elif error.response.status_code == 403:
            raise BoNowAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 429:
            raise BoNowRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BoNowAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 404:
            raise BoNowAPIError("Resource not found")
        else:
            raise BoNowAPIError(f"HTTP {error.response.status_code}: {error.response.text}")