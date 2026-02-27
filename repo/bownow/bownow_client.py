"""
Bownow API Client

Supports:
- Create Lead
- Get Lead
- Update Lead
- Delete Lead
- Search Leads
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Lead:
    """Bownow lead representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    score: Optional[int] = None
    source: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class BownowClient:
    """
    Bownow API client for lead management.

    Authentication: API Key (Header: Authorization: Bearer {token})
    Base URL: https://api.bownow.jp/v1
    """

    BASE_URL = "https://api.bownow.jp/v1"

    def __init__(self, api_token: str):
        """
        Initialize Bownow client.

        Args:
            api_token: Bownow API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
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
                raise Exception("Authentication failed: Invalid API token")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Lead Operations ====================

    def create_lead(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Lead:
        """
        Create a new lead.

        Args:
            name: Lead name
            email: Email address
            phone: Phone number
            company: Company name
            title: Job title
            status: Lead status
            source: Lead source
            custom_fields: Dictionary of custom field values
            **kwargs: Additional fields

        Returns:
            Lead object
        """
        payload = {}

        if name:
            payload["name"] = name
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if title:
            payload["title"] = title
        if status:
            payload["status"] = status
        if source:
            payload["source"] = source
        if custom_fields:
            payload["custom_fields"] = custom_fields
        payload.update(kwargs)

        result = self._request("POST", "/leads", json=payload)
        return self._parse_lead(result)

    def get_lead(self, lead_id: str) -> Lead:
        """
        Retrieve a lead by ID.

        Args:
            lead_id: Lead ID

        Returns:
            Lead object
        """
        result = self._request("GET", f"/leads/{lead_id}")
        return self._parse_lead(result)

    def update_lead(
        self,
        lead_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        score: Optional[int] = None,
        source: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Lead:
        """
        Update an existing lead.

        Args:
            lead_id: Lead ID
            name: Updated name
            email: Updated email
            phone: Updated phone
            company: Updated company
            title: Updated title
            status: Updated status
            score: Updated lead score
            source: Updated source
            custom_fields: Updated custom fields
            **kwargs: Additional fields to update

        Returns:
            Updated Lead object
        """
        payload = {}

        if name is not None:
            payload["name"] = name
        if email is not None:
            payload["email"] = email
        if phone is not None:
            payload["phone"] = phone
        if company is not None:
            payload["company"] = company
        if title is not None:
            payload["title"] = title
        if status is not None:
            payload["status"] = status
        if score is not None:
            payload["score"] = score
        if source is not None:
            payload["source"] = source
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields
        payload.update(kwargs)

        result = self._request("PUT", f"/leads/{lead_id}", json=payload)
        return self._parse_lead(result)

    def delete_lead(self, lead_id: str) -> None:
        """
        Delete a lead.

        Args:
            lead_id: Lead ID
        """
        self._request("DELETE", f"/leads/{lead_id}")

    def search_leads(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Lead]:
        """
        Search for leads.

        Args:
            name: Filter by name (partial match)
            email: Filter by email (exact match)
            company: Filter by company
            status: Filter by status
            source: Filter by source
            limit: Number of results
            offset: Pagination offset

        Returns:
            List of Lead objects
        """
        params = {"limit": limit, "offset": offset}

        if name:
            params["name"] = name
        if email:
            params["email"] = email
        if company:
            params["company"] = company
        if status:
            params["status"] = status
        if source:
            params["source"] = source

        result = self._request("GET", "/leads", params=params)

        leads = []
        if isinstance(result, dict) and "data" in result:
            for lead_data in result.get("data", []):
                leads.append(self._parse_lead(lead_data))
        elif isinstance(result, list):
            for lead_data in result:
                leads.append(self._parse_lead(lead_data))

        return leads

    # ==================== Webhook Operations ====================

    def verify_webhook(self, signature: str, payload: bytes, webhook_secret: str) -> bool:
        """
        Verify a webhook signature.

        Args:
            signature: Signature from X-Signature header
            payload: Raw webhook payload bytes
            webhook_secret: Your webhook secret

        Returns:
            True if signature is valid
        """
        import hmac
        import hashlib

        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    # ==================== Helper Methods ====================

    def _parse_lead(self, data: Dict[str, Any]) -> Lead:
        """Parse lead data from API response"""
        return Lead(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            title=data.get("title"),
            status=data.get("status"),
            score=data.get("score"),
            source=data.get("source"),
            custom_fields=data.get("custom_fields"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_bownow_api_token"

    client = BownowClient(api_token=api_token)

    try:
        # Create a lead
        lead = client.create_lead(
            name="山田 太郎",
            email="taro.yamada@example.com",
            phone="81-90-1234-5678",
            company="株式会社ABC",
            title="マネージャー",
            status="新規",
            source="Webフォーム"
        )
        print(f"Created: {lead.id} - {lead.name} ({lead.email})")

        # Get lead
        fetched = client.get_lead(lead.id)
        print(f"Fetched: {fetched.name} at {fetched.company}")

        # Search leads
        leads = client.search_leads(
            company="株式会社ABC",
            status="新規",
            limit=20
        )
        print(f"Found {len(leads)} leads")

        # Update lead
        updated = client.update_lead(
            lead.id,
            status="商談中",
            score=50,
            custom_fields={"last_contact": "2024-01-15"}
        )
        print(f"Updated: Status={updated.status}, Score={updated.score}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()