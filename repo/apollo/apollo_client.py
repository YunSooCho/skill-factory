"""
Apollo API Client

Supports 9 API actions for B2B sales intelligence:
- Update account (アカウントを更新)
- Search contacts (コンタクトを検索)
- Enrich person data (人物情報のエンリッチメント)
- Enrich organization data (組織情報のエンリッチメント)
- Search people (人物情報を検索)
- Search accounts (アカウントを検索)
- Create contact (コンタクトを作成)
- Update contact (コンタクトを更新)
- Create account (アカウントを作成)

And 3 triggers:
- Contact created (コンタクトが作成されたら)
- Contact updated (コンタクトが更新されたら)
- Account created (アカウントが作成されたら)

API Reference: https://api.apollo.io/v1
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Account:
    """Account (organization/company) representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    revenue: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Contact:
    """Contact (person) representation"""
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    organization_id: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class EnrichedPerson:
    """Enriched person data"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    organization_name: Optional[str] = None
    organization_id: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    confirmed_at: Optional[str] = None
    confidence_score: Optional[float] = None


@dataclass
class EnrichedOrganization:
    """Enriched organization data"""
    name: Optional[str] = None
    id: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    revenue: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None


class ApolloClient:
    """
    Apollo API client for B2B sales intelligence.

    Authentication: API Key (Header: Api-Key: {api_key})
    Base URL: https://api.apollo.io/v1
    """

    BASE_URL = "https://api.apollo.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Apollo client.

        Args:
            api_key: Apollo API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Api-Key": self.api_key,
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

    # ==================== Account Operations ====================

    def create_account(
        self,
        name: str,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        revenue: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None
    ) -> Account:
        """
        Create a new account.
        アカウントを作成

        Args:
            name: Account/company name (required)
            website: Company website
            industry: Industry
            size: Company size (e.g., "11-50", "51-200")
            revenue: Annual revenue
            linkedin_url: LinkedIn URL
            phone: Phone number
            address: Address information

        Returns:
            Account object
        """
        if not name:
            raise ValueError("Account name is required")

        payload = {"name": name}

        if website:
            payload["website"] = website
        if industry:
            payload["industry"] = industry
        if size:
            payload["size"] = size
        if revenue:
            payload["revenue"] = revenue
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if phone:
            payload["phone"] = phone
        if address:
            payload["address"] = address

        result = self._request("POST", "/accounts", json=payload)
        return self._parse_account(result.get("account", result))

    def get_account(self, account_id: str) -> Account:
        """Get account by ID"""
        result = self._request("GET", f"/accounts/{account_id}")
        return self._parse_account(result.get("account", result))

    def update_account(
        self,
        account_id: str,
        name: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        revenue: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None
    ) -> Account:
        """
        Update account.
        アカウントを更新

        Args:
            account_id: Account ID (required)
            name: Account/company name
            website: Company website
            industry: Industry
            size: Company size
            revenue: Annual revenue
            linkedin_url: LinkedIn URL
            phone: Phone number
            address: Address information

        Returns:
            Account object
        """
        if not account_id:
            raise ValueError("Account ID is required")

        payload = {}
        if name:
            payload["name"] = name
        if website:
            payload["website"] = website
        if industry:
            payload["industry"] = industry
        if size:
            payload["size"] = size
        if revenue:
            payload["revenue"] = revenue
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if phone:
            payload["phone"] = phone
        if address:
            payload["address"] = address

        result = self._request("PATCH", f"/accounts/{account_id}", json=payload)
        return self._parse_account(result.get("account", result))

    def search_accounts(
        self,
        name: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 50
    ) -> List[Account]:
        """
        Search accounts.
        アカウントを検索

        Args:
            name: Filter by company name
            website: Filter by website
            industry: Filter by industry
            size: Filter by company size
            limit: Maximum results to return

        Returns:
            List of Account objects
        """
        params = {}
        if name:
            params["name"] = name
        if website:
            params["website"] = website
        if industry:
            params["industry"] = industry
        if size:
            params["size"] = size
        params["page_size"] = limit

        result = self._request("GET", "/accounts/search", params=params)

        accounts = []
        if isinstance(result, dict) and "accounts" in result:
            for account_data in result.get("accounts", []):
                accounts.append(self._parse_account(account_data))
        elif isinstance(result, list):
            for account_data in result:
                accounts.append(self._parse_account(account_data))

        return accounts

    # ==================== Contact Operations ====================

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        title: Optional[str] = None,
        department: Optional[str] = None,
        organization_id: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        phone: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.
        コンタクトを作成

        Args:
            first_name: First name (required)
            last_name: Last name (required)
            email: Email address
            title: Job title
            department: Department
            organization_id: Organization ID
            linkedin_url: LinkedIn URL
            phone: Phone number
            location: Location information

        Returns:
            Contact object
        """
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")

        payload = {
            "first_name": first_name,
            "last_name": last_name
        }

        if email:
            payload["email"] = email
        if title:
            payload["title"] = title
        if department:
            payload["department"] = department
        if organization_id:
            payload["organization_id"] = organization_id
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if phone:
            payload["phone"] = phone
        if location:
            payload["location"] = location

        result = self._request("POST", "/contacts", json=payload)
        return self._parse_contact(result.get("contact", result))

    def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID"""
        result = self._request("GET", f"/contacts/{contact_id}")
        return self._parse_contact(result.get("contact", result))

    def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        title: Optional[str] = None,
        department: Optional[str] = None,
        organization_id: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        phone: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None
    ) -> Contact:
        """
        Update contact.
        コンタクトを更新

        Args:
            contact_id: Contact ID (required)
            first_name: First name
            last_name: Last name
            email: Email address
            title: Job title
            department: Department
            organization_id: Organization ID
            linkedin_url: LinkedIn URL
            phone: Phone number
            location: Location information
            status: Contact status

        Returns:
            Contact object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        payload = {}
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if email:
            payload["email"] = email
        if title:
            payload["title"] = title
        if department:
            payload["department"] = department
        if organization_id:
            payload["organization_id"] = organization_id
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if phone:
            payload["phone"] = phone
        if location:
            payload["location"] = location
        if status:
            payload["status"] = status

        result = self._request("PATCH", f"/contacts/{contact_id}", json=payload)
        return self._parse_contact(result.get("contact", result))

    def search_contacts(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        title: Optional[str] = None,
        organization_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """
        Search contacts.
        コンタクトを検索

        Args:
            first_name: Filter by first name
            last_name: Filter by last name
            email: Filter by email
            title: Filter by job title
            organization_id: Filter by organization ID
            limit: Maximum results to return

        Returns:
            List of Contact objects
        """
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if email:
            params["email"] = email
        if title:
            params["title"] = title
        if organization_id:
            params["organization_id"] = organization_id
        params["page_size"] = limit

        result = self._request("GET", "/contacts/search", params=params)

        contacts = []
        if isinstance(result, dict) and "contacts" in result:
            for contact_data in result.get("contacts", []):
                contacts.append(self._parse_contact(contact_data))
        elif isinstance(result, list):
            for contact_data in result:
                contacts.append(self._parse_contact(contact_data))

        return contacts

    # ==================== Enrichment Operations ====================

    def search_people(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        title: Optional[str] = None,
        limit: int = 50
    ) -> List[EnrichedPerson]:
        """
        Search people for enrichment.
        人物情報を検索

        Args:
            first_name: Filter by first name
            last_name: Filter by last name
            organization_name: Filter by organization name
            title: Filter by job title
            limit: Maximum results to return

        Returns:
            List of EnrichedPerson objects
        """
        params = {}
        if first_name:
            params["q_first_name"] = first_name
        if last_name:
            params["q_last_name"] = last_name
        if organization_name:
            params["q_organization_name"] = organization_name
        if title:
            params["q_title"] = title
        params["page_size"] = limit

        result = self._request("GET", "/people/search", params=params)

        people = []
        if isinstance(result, dict) and "people" in result:
            for person_data in result.get("people", []):
                people.append(self._parse_enriched_person(person_data))
        elif isinstance(result, list):
            for person_data in result:
                people.append(self._parse_enriched_person(person_data))

        return people

    def enrich_person(
        self,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None
    ) -> EnrichedPerson:
        """
        Enrich person data.
        人物情報のエンリッチメント

        Args:
            email: Email address to enrich
            linkedin_url: LinkedIn URL to enrich
            first_name: First name
            last_name: Last name
            organization_name: Organization name

        Returns:
            EnrichedPerson object
        """
        payload = {}
        if email:
            payload["email"] = email
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if organization_name:
            payload["organization_name"] = organization_name

        result = self._request("POST", "/people/enrich", json=payload)
        return self._parse_enriched_person(result.get("person", result))

    def enrich_organization(
        self,
        website: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        name: Optional[str] = None
    ) -> EnrichedOrganization:
        """
        Enrich organization data.
        組織情報のエンリッチメント

        Args:
            website: Website to enrich
            linkedin_url: LinkedIn URL to enrich
            name: Organization name

        Returns:
            EnrichedOrganization object
        """
        payload = {}
        if website:
            payload["website"] = website
        if linkedin_url:
            payload["linkedin_url"] = linkedin_url
        if name:
            payload["name"] = name

        result = self._request("POST", "/organizations/enrich", json=payload)
        return self._parse_enriched_organization(result.get("organization", result))

    # ==================== Webhook/Trigger Support ====================

    def register_webhook(
        self,
        callback_url: str,
        events: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Register webhook for event notifications.
        
        Args:
            callback_url: Your webhook endpoint URL
            events: List of events to subscribe to

        Returns:
            Webhook registration response
        """
        if not callback_url:
            raise ValueError("Callback URL is required")

        if events is None:
            events = ["contact.created", "contact.updated", "account.created"]

        payload = {
            "callback_url": callback_url,
            "events": events
        }

        return self._request("POST", "/webhooks", json=payload)

    def delete_webhook(self, webhook_id: str) -> None:
        """Delete webhook registration"""
        self._request("DELETE", f"/webhooks/{webhook_id}")

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """Get list of registered webhooks"""
        result = self._request("GET", "/webhooks")
        if isinstance(result, dict) and "webhooks" in result:
            return result.get("webhooks", [])
        elif isinstance(result, list):
            return result
        return []

    # ==================== Helper Methods ====================

    def _parse_account(self, data: Dict[str, Any]) -> Account:
        """Parse account data from API response"""
        return Account(
            id=data.get("id"),
            name=data.get("name"),
            website=data.get("website"),
            industry=data.get("industry"),
            size=data.get("size"),
            revenue=data.get("revenue"),
            linkedin_url=data.get("linkedin_url"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response"""
        return Contact(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            title=data.get("title"),
            department=data.get("department"),
            organization_id=data.get("organization_id"),
            linkedin_url=data.get("linkedin_url"),
            phone=data.get("phone"),
            location=data.get("location"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def _parse_enriched_person(self, data: Dict[str, Any]) -> EnrichedPerson:
        """Parse enriched person data from API response"""
        return EnrichedPerson(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            title=data.get("title"),
            organization_name=data.get("organization_name"),
            organization_id=data.get("organization_id"),
            linkedin_url=data.get("linkedin_url"),
            phone=data.get("phone"),
            location=data.get("location"),
            confirmed_at=data.get("confirmed_at"),
            confidence_score=data.get("confidence_score")
        )

    def _parse_enriched_organization(self, data: Dict[str, Any]) -> EnrichedOrganization:
        """Parse enriched organization data from API response"""
        return EnrichedOrganization(
            name=data.get("name"),
            id=data.get("id"),
            website=data.get("website"),
            industry=data.get("industry"),
            size=data.get("size"),
            revenue=data.get("revenue"),
            linkedin_url=data.get("linkedin_url"),
            phone=data.get("phone"),
            address=data.get("address"),
            confidence_score=data.get("confidence_score")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_apollo_api_key"

    client = ApolloClient(api_key=api_key)

    try:
        # Example: Create account
        account = client.create_account(
            name="Example Corp",
            website="https://example.com",
            industry="Technology",
            size="51-200"
        )
        print(f"Created account: {account.name} (ID: {account.id})")

        # Example: Create contact
        contact = client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            title="Sales Manager",
            organization_id=account.id
        )
        print(f"Created contact: {contact.first_name} {contact.last_name} (ID: {contact.id})")

        # Example: Search contacts
        contacts = client.search_contacts(organization_id=account.id)
        print(f"Found {len(contacts)} contacts")

        # Example: Enrich person data
        enriched = client.enrich_person(email="john.doe@example.com")
        print(f"Enriched: {enriched.first_name} {enriched.last_name} - {enriched.title}")

        # Example: Search people
        people = client.search_people(organization_name="Example Corp")
        print(f"Found {len(people)} people")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()