"""
Zoho CRM OAuth API - CRM Management Client

Supports:
- Accounts management
- Leads management
- Contacts management
- Deals management
- Tasks and events
- Attachments
- Custom fields
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os
import json


@dataclass
class Record:
    """Generic CRM record"""
    id: str
    module: str
    data: Dict[str, Any]
    created_by: Optional[str]
    modified_by: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Deal:
    """Deal information"""
    deal_id: str
    deal_name: str
    stage: str
    amount: Optional[float]
    closing_date: Optional[str]
    account_id: Optional[str]
    contact_id: Optional[str]
    probability: Optional[int]
    description: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Contact:
    """Contact information"""
    contact_id: str
    first_name: Optional[str]
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    account_id: Optional[str]
    title: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Lead:
    """Lead information"""
    lead_id: str
    first_name: Optional[str]
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    status: Optional[str]
    lead_source: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Account:
    """Account information"""
    account_id: str
    account_name: str
    website: Optional[str]
    phone: Optional[str]
    billing_city: Optional[str]
    billing_state: Optional[str]
    billing_country: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Task:
    """Task information"""
    task_id: str
    subject: str
    status: str
    priority: Optional[str]
    due_date: Optional[str]
    description: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Event:
    """Event information"""
    event_id: str
    event_title: str
    start_datetime: str
    end_datetime: str
    location: Optional[str]
    description: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Call:
    """Call information"""
    call_id: str
    subject: str
    call_type: str
    call_duration: Optional[int]
    call_start_time: Optional[str]
    description: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]


@dataclass
class Attachment:
    """Attachment information"""
    attachment_id: str
    file_name: str
    size: int
    owner_id: Optional[str]
    created_time: Optional[str]


class ZohoCrmOauthClient:
    """
    Zoho CRM OAuth API client for CRM management.

    API Documentation: https://lp.yoom.fun/apps/zoho-crm-oauth
    Requires OAuth access token from Yoom integration.
    """

    BASE_URL = "https://www.zohoapis.com/crm/v2"

    def __init__(
        self,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize Zoho CRM OAuth client.

        Args:
            access_token: OAuth access token (defaults to YOOM_ZOHO_CRM_ACCESS_TOKEN env var)
            refresh_token: OAuth refresh token for token refresh
            client_id: OAuth client ID
            client_secret: OAuth client secret
            base_url: Custom base URL for testing
        """
        self.access_token = access_token or os.environ.get("YOOM_ZOHO_CRM_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("Access token must be provided or set YOOM_ZOHO_CRM_ACCESS_TOKEN environment variable")

        self.refresh_token = refresh_token or os.environ.get("YOOM_ZOHO_CRM_REFRESH_TOKEN")
        self.client_id = client_id or os.environ.get("YOOM_ZOHO_CRM_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("YOOM_ZOHO_CRM_CLIENT_SECRET")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.3  # 300ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Zoho-oauthtoken {self.access_token}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 401 and self.refresh_token:
                # Try to refresh token
                await self._refresh_token()
                headers["Authorization"] = f"Zoho-oauthtoken {self.access_token}"
                async with self.session.request(method, url, headers=headers, **kwargs) as retry_response:
                    if retry_response.status >= 400:
                        error_text = await retry_response.text()
                        raise Exception(f"API error {retry_response.status}: {error_text}")
                    return await retry_response.json()

            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    async def _refresh_token(self):
        """Refresh OAuth access token"""
        if not self.refresh_token or not self.client_id or not self.client_secret:
            raise Exception("Cannot refresh token: refresh_token, client_id, and client_secret required")

        params = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token"
        }

        async with self.session.post("https://accounts.zoho.com/oauth/v2/token", params=params) as response:
            data = await response.json()
            if "access_token" in data:
                self.access_token = data["access_token"]
            else:
                raise Exception(f"Token refresh failed: {data}")

    # ==================== Deal Operations ====================

    async def get_deal(self, deal_id: str) -> Deal:
        """Get deal by ID"""
        data = await self._request("GET", f"/Deals/{deal_id}")
        record = data.get("data", [{}])[0]

        return Deal(
            deal_id=record.get("id", deal_id),
            deal_name=record.get("Deal_Name", ""),
            stage=record.get("Stage", ""),
            amount=record.get("Amount"),
            closing_date=record.get("Closing_Date"),
            account_id=record.get("Account_Name", {}).get("id") if record.get("Account_Name") else None,
            contact_id=record.get("Contact_Name", {}).get("id") if record.get("Contact_Name") else None,
            probability=record.get("Probability"),
            description=record.get("Description"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_deals(self, **criteria) -> List[Deal]:
        """Search deals with criteria"""
        data = await self._request("GET", "/Deals/search", params=criteria)

        deals = []
        for record in data.get("data", []):
            deals.append(Deal(
                deal_id=record.get("id", ""),
                deal_name=record.get("Deal_Name", ""),
                stage=record.get("Stage", ""),
                amount=record.get("Amount"),
                closing_date=record.get("Closing_Date"),
                account_id=record.get("Account_Name", {}).get("id") if record.get("Account_Name") else None,
                contact_id=record.get("Contact_Name", {}).get("id") if record.get("Contact_Name") else None,
                probability=record.get("Probability"),
                description=record.get("Description"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return deals

    async def create_deal(self, deal_data: Dict[str, Any]) -> Deal:
        """Create a new deal"""
        data = await self._request("POST", "/Deals", json={"data": [deal_data]})
        record = data.get("data", [{}])[0]

        return Deal(
            deal_id=record.get("details", {}).get("id", ""),
            deal_name=record.get("details", {}).get("Deal_Name", ""),
            stage=record.get("details", {}).get("Stage", ""),
            amount=record.get("details", {}).get("Amount"),
            closing_date=record.get("details", {}).get("Closing_Date"),
            account_id=record.get("details", {}).get("Account_Name", {}).get("id") if record.get("details", {}).get("Account_Name") else None,
            contact_id=record.get("details", {}).get("Contact_Name", {}).get("id") if record.get("details", {}).get("Contact_Name") else None,
            probability=record.get("details", {}).get("Probability"),
            description=record.get("details", {}).get("Description"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def update_deal(self, deal_id: str, update_data: Dict[str, Any]) -> Deal:
        """Update deal"""
        data = await self._request("PUT", f"/Deals/{deal_id}", json={"data": [update_data]})
        record = data.get("data", [{}])[0]

        return Deal(
            deal_id=record.get("details", {}).get("id", deal_id),
            deal_name=record.get("details", {}).get("Deal_Name", ""),
            stage=record.get("details", {}).get("Stage", ""),
            amount=record.get("details", {}).get("Amount"),
            closing_date=record.get("details", {}).get("Closing_Date"),
            account_id=record.get("details", {}).get("Account_Name", {}).get("id") if record.get("details", {}).get("Account_Name") else None,
            contact_id=record.get("details", {}).get("Contact_Name", {}).get("id") if record.get("details", {}).get("Contact_Name") else None,
            probability=record.get("details", {}).get("Probability"),
            description=record.get("details", {}).get("Description"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_deal_ids(self) -> List[str]:
        """Get list of deal IDs"""
        data = await self._request("GET", "/Deals", params={"fields": "id"})
        return [record.get("id", "") for record in data.get("data", [])]

    # ==================== Contact Operations ====================

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new contact"""
        data = await self._request("POST", "/Contacts", json={"data": [contact_data]})
        record = data.get("data", [{}])[0]

        return Contact(
            contact_id=record.get("details", {}).get("id", ""),
            first_name=record.get("details", {}).get("First_Name"),
            last_name=record.get("details", {}).get("Last_Name", ""),
            email=record.get("details", {}).get("Email"),
            phone=record.get("details", {}).get("Phone"),
            account_id=record.get("details", {}).get("Account_Name", {}).get("id") if record.get("details", {}).get("Account_Name") else None,
            title=record.get("details", {}).get("Title"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update contact"""
        data = await self._request("PUT", f"/Contacts/{contact_id}", json={"data": [update_data]})
        record = data.get("data", [{}])[0]

        return Contact(
            contact_id=record.get("details", {}).get("id", contact_id),
            first_name=record.get("details", {}).get("First_Name"),
            last_name=record.get("details", {}).get("Last_Name", ""),
            email=record.get("details", {}).get("Email"),
            phone=record.get("details", {}).get("Phone"),
            account_id=record.get("details", {}).get("Account_Name", {}).get("id") if record.get("details", {}).get("Account_Name") else None,
            title=record.get("details", {}).get("Title"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID"""
        data = await self._request("GET", f"/Contacts/{contact_id}")
        record = data.get("data", [{}])[0]

        return Contact(
            contact_id=record.get("id", contact_id),
            first_name=record.get("First_Name"),
            last_name=record.get("Last_Name", ""),
            email=record.get("Email"),
            phone=record.get("Phone"),
            account_id=record.get("Account_Name", {}).get("id") if record.get("Account_Name") else None,
            title=record.get("Title"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_contacts(self, **criteria) -> List[Contact]:
        """Search contacts with criteria"""
        data = await self._request("GET", "/Contacts/search", params=criteria)

        contacts = []
        for record in data.get("data", []):
            contacts.append(Contact(
                contact_id=record.get("id", ""),
                first_name=record.get("First_Name"),
                last_name=record.get("Last_Name", ""),
                email=record.get("Email"),
                phone=record.get("Phone"),
                account_id=record.get("Account_Name", {}).get("id") if record.get("Account_Name") else None,
                title=record.get("Title"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return contacts

    async def get_contact_ids(self) -> List[str]:
        """Get list of contact IDs"""
        data = await self._request("GET", "/Contacts", params={"fields": "id"})
        return [record.get("id", "") for record in data.get("data", [])]

    async def get_contact_info(self, contact_id: str) -> Contact:
        """Get contact information (alias for get_contact)"""
        return await self.get_contact(contact_id)

    async def contact_link_company(self, contact_id: str, company_id: str) -> Dict[str, Any]:
        """Link contact to company"""
        return await self.update_contact(contact_id, {"Account_Name": {"id": company_id}})

    async def add_contact_note(self, contact_id: str, note: str) -> Dict[str, Any]:
        """Add note to contact"""
        note_data = {
            "Note_Title": "Note",
            "Note_Content": note,
            "Parent_Id": {"id": contact_id}
        }
        return await self._request("POST", "/Notes", json={"data": [note_data]})

    async def contact_get_attachment_info(self, contact_id: str) -> List[Attachment]:
        """Get contact attachment information"""
        data = await self._request("GET", f"/Contacts/{contact_id}/Attachments")

        attachments = []
        for record in data.get("data", []):
            attachments.append(Attachment(
                attachment_id=record.get("id", ""),
                file_name=record.get("File_Name", ""),
                size=record.get("Size", 0),
                owner_id=record.get("Owner", {}).get("id") if record.get("Owner") else None,
                created_time=record.get("Created_Time")
            ))

        return attachments

    async def contact_download_attachment(self, attachment_id: str) -> bytes:
        """Download contact attachment"""
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        url = f"{self.base_url}/Contacts/{attachment_id}/Attachments"

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    async def contact_upload_file(self, contact_id: str, file_path: str) -> Dict[str, Any]:
        """Upload file to contact"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

            async with self.session.post(
                f"{self.base_url}/Contacts/{contact_id}/Attachments",
                headers=headers,
                files=files
            ) as response:
                return await response.json()

    # ==================== Lead Operations ====================

    async def create_lead(self, lead_data: Dict[str, Any]) -> Lead:
        """Create a new lead"""
        data = await self._request("POST", "/Leads", json={"data": [lead_data]})
        record = data.get("data", [{}])[0]

        return Lead(
            lead_id=record.get("details", {}).get("id", ""),
            first_name=record.get("details", {}).get("First_Name"),
            last_name=record.get("details", {}).get("Last_Name", ""),
            email=record.get("details", {}).get("Email"),
            phone=record.get("details", {}).get("Phone"),
            company=record.get("details", {}).get("Company"),
            status=record.get("details", {}).get("Lead_Status"),
            lead_source=record.get("details", {}).get("Lead_Source"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_lead(self, lead_id: str) -> Lead:
        """Get lead by ID"""
        data = await self._request("GET", f"/Leads/{lead_id}")
        record = data.get("data", [{}])[0]

        return Lead(
            lead_id=record.get("id", lead_id),
            first_name=record.get("First_Name"),
            last_name=record.get("Last_Name", ""),
            email=record.get("Email"),
            phone=record.get("Phone"),
            company=record.get("Company"),
            status=record.get("Lead_Status"),
            lead_source=record.get("Lead_Source"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_leads(self, **criteria) -> List[Lead]:
        """Search leads with criteria"""
        data = await self._request("GET", "/Leads/search", params=criteria)

        leads = []
        for record in data.get("data", []):
            leads.append(Lead(
                lead_id=record.get("id", ""),
                first_name=record.get("First_Name"),
                last_name=record.get("Last_Name", ""),
                email=record.get("Email"),
                phone=record.get("Phone"),
                company=record.get("Company"),
                status=record.get("Lead_Status"),
                lead_source=record.get("Lead_Source"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return leads

    async def get_lead_ids(self) -> List[str]:
        """Get list of lead IDs"""
        data = await self._request("GET", "/Leads", params={"fields": "id"})
        return [record.get("id", "") for record in data.get("data", [])]

    async def lead_link_campaign(self, lead_id: str, campaign_id: str) -> Dict[str, Any]:
        """Link lead to campaign"""
        return await self.update_lead(lead_id, {"Campaign_Source": {"id": campaign_id}})

    async def update_lead(self, lead_id: str, update_data: Dict[str, Any]) -> Lead:
        """Update lead"""
        data = await self._request("PUT", f"/Leads/{lead_id}", json={"data": [update_data]})
        record = data.get("data", [{}])[0]

        return Lead(
            lead_id=record.get("details", {}).get("id", lead_id),
            first_name=record.get("details", {}).get("First_Name"),
            last_name=record.get("details", {}).get("Last_Name", ""),
            email=record.get("details", {}).get("Email"),
            phone=record.get("details", {}).get("Phone"),
            company=record.get("details", {}).get("Company"),
            status=record.get("details", {}).get("Lead_Status"),
            lead_source=record.get("details", {}).get("Lead_Source"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def lead_get_attachment_info(self, lead_id: str) -> List[Attachment]:
        """Get lead attachment information"""
        data = await self._request("GET", f"/Leads/{lead_id}/Attachments")

        attachments = []
        for record in data.get("data", []):
            attachments.append(Attachment(
                attachment_id=record.get("id", ""),
                file_name=record.get("File_Name", ""),
                size=record.get("Size", 0),
                owner_id=record.get("Owner", {}).get("id") if record.get("Owner") else None,
                created_time=record.get("Created_Time")
            ))

        return attachments

    async def lead_download_attachment(self, attachment_id: str) -> bytes:
        """Download lead attachment"""
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        url = f"{self.base_url}/Leads/{attachment_id}/Attachments"

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    async def lead_upload_file(self, lead_id: str, file_path: str) -> Dict[str, Any]:
        """Upload file to lead"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

            async with self.session.post(
                f"{self.base_url}/Leads/{lead_id}/Attachments",
                headers=headers,
                files=files
            ) as response:
                return await response.json()

    # ==================== Account Operations ====================

    async def create_account(self, account_data: Dict[str, Any]) -> Account:
        """Create a new account"""
        data = await self._request("POST", "/Accounts", json={"data": [account_data]})
        record = data.get("data", [{}])[0]

        return Account(
            account_id=record.get("details", {}).get("id", ""),
            account_name=record.get("details", {}).get("Account_Name", ""),
            website=record.get("details", {}).get("Website"),
            phone=record.get("details", {}).get("Phone"),
            billing_city=record.get("details", {}).get("Billing_City"),
            billing_state=record.get("details", {}).get("Billing_State"),
            billing_country=record.get("details", {}).get("Billing_Country"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def update_account(self, account_id: str, update_data: Dict[str, Any]) -> Account:
        """Update account"""
        data = await self._request("PUT", f"/Accounts/{account_id}", json={"data": [update_data]})
        record = data.get("data", [{}])[0]

        return Account(
            account_id=record.get("details", {}).get("id", account_id),
            account_name=record.get("details", {}).get("Account_Name", ""),
            website=record.get("details", {}).get("Website"),
            phone=record.get("details", {}).get("Phone"),
            billing_city=record.get("details", {}).get("Billing_City"),
            billing_state=record.get("details", {}).get("Billing_State"),
            billing_country=record.get("details", {}).get("Billing_Country"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_account(self, account_id: str) -> Account:
        """Get account by ID"""
        data = await self._request("GET", f"/Accounts/{account_id}")
        record = data.get("data", [{}])[0]

        return Account(
            account_id=record.get("id", account_id),
            account_name=record.get("Account_Name", ""),
            website=record.get("Website"),
            phone=record.get("Phone"),
            billing_city=record.get("Billing_City"),
            billing_state=record.get("Billing_State"),
            billing_country=record.get("Billing_Country"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_accounts(self, **criteria) -> List[Account]:
        """Search accounts with criteria"""
        data = await self._request("GET", "/Accounts/search", params=criteria)

        accounts = []
        for record in data.get("data", []):
            accounts.append(Account(
                account_id=record.get("id", ""),
                account_name=record.get("Account_Name", ""),
                website=record.get("Website"),
                phone=record.get("Phone"),
                billing_city=record.get("Billing_City"),
                billing_state=record.get("Billing_State"),
                billing_country=record.get("Billing_Country"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return accounts

    async def get_account_ids(self) -> List[str]:
        """Get list of account IDs"""
        data = await self._request("GET", "/Accounts", params={"fields": "id"})
        return [record.get("id", "") for record in data.get("data", [])]

    async def account_get_attachment_info(self, account_id: str) -> List[Attachment]:
        """Get account attachment information"""
        data = await self._request("GET", f"/Accounts/{account_id}/Attachments")

        attachments = []
        for record in data.get("data", []):
            attachments.append(Attachment(
                attachment_id=record.get("id", ""),
                file_name=record.get("File_Name", ""),
                size=record.get("Size", 0),
                owner_id=record.get("Owner", {}).get("id") if record.get("Owner") else None,
                created_time=record.get("Created_Time")
            ))

        return attachments

    async def account_download_attachment(self, attachment_id: str) -> bytes:
        """Download account attachment"""
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        url = f"{self.base_url}/Accounts/{attachment_id}/Attachments"

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    async def account_upload_file(self, account_id: str, file_path: str) -> Dict[str, Any]:
        """Upload file to account"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

            async with self.session.post(
                f"{self.base_url}/Accounts/{account_id}/Attachments",
                headers=headers,
                files=files
            ) as response:
                return await response.json()

    # ==================== Task Operations ====================

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task"""
        data = await self._request("POST", "/Tasks", json={"data": [task_data]})
        record = data.get("data", [{}])[0]

        return Task(
            task_id=record.get("details", {}).get("id", ""),
            subject=record.get("details", {}).get("Subject", ""),
            status=record.get("details", {}).get("Status", ""),
            priority=record.get("details", {}).get("Priority"),
            due_date=record.get("details", {}).get("Due_Date"),
            description=record.get("details", {}).get("Description"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_task(self, task_id: str) -> Task:
        """Get task by ID"""
        data = await self._request("GET", f"/Tasks/{task_id}")
        record = data.get("data", [{}])[0]

        return Task(
            task_id=record.get("id", task_id),
            subject=record.get("Subject", ""),
            status=record.get("Status", ""),
            priority=record.get("Priority"),
            due_date=record.get("Due_Date"),
            description=record.get("Description"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_tasks(self, **criteria) -> List[Task]:
        """Search tasks with criteria"""
        data = await self._request("GET", "/Tasks/search", params=criteria)

        tasks = []
        for record in data.get("data", []):
            tasks.append(Task(
                task_id=record.get("id", ""),
                subject=record.get("Subject", ""),
                status=record.get("Status", ""),
                priority=record.get("Priority"),
                due_date=record.get("Due_Date"),
                description=record.get("Description"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return tasks

    # ==================== Event Operations ====================

    async def create_event(self, event_data: Dict[str, Any]) -> Event:
        """Create a new event"""
        data = await self._request("POST", "/Events", json={"data": [event_data]})
        record = data.get("data", [{}])[0]

        return Event(
            event_id=record.get("details", {}).get("id", ""),
            event_title=record.get("details", {}).get("Event_Title", ""),
            start_datetime=record.get("details", {}).get("Start_DateTime", ""),
            end_datetime=record.get("details", {}).get("End_DateTime", ""),
            location=record.get("details", {}).get("Location"),
            description=record.get("details", {}).get("Description"),
            created_time=record.get("details", {}).get("Created_Time"),
            modified_time=record.get("details", {}).get("Modified_Time")
        )

    async def get_event(self, event_id: str) -> Event:
        """Get event by ID"""
        data = await self._request("GET", f"/Events/{event_id}")
        record = data.get("data", [{}])[0]

        return Event(
            event_id=record.get("id", event_id),
            event_title=record.get("Event_Title", ""),
            start_datetime=record.get("Start_DateTime", ""),
            end_datetime=record.get("End_DateTime", ""),
            location=record.get("Location"),
            description=record.get("Description"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def search_events(self, **criteria) -> List[Event]:
        """Search events with criteria"""
        data = await self._request("GET", "/Events/search", params=criteria)

        events = []
        for record in data.get("data", []):
            events.append(Event(
                event_id=record.get("id", ""),
                event_title=record.get("Event_Title", ""),
                start_datetime=record.get("Start_DateTime", ""),
                end_datetime=record.get("End_DateTime", ""),
                location=record.get("Location"),
                description=record.get("Description"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return events

    # ==================== Call Operations ====================

    async def get_call(self, call_id: str) -> Call:
        """Get call by ID"""
        data = await self._request("GET", f"/Calls/{call_id}")
        record = data.get("data", [{}])[0]

        return Call(
            call_id=record.get("id", call_id),
            subject=record.get("Subject", ""),
            call_type=record.get("Call_Type", ""),
            call_duration=record.get("Call_Duration"),
            call_start_time=record.get("Call_Start_Time"),
            description=record.get("Description"),
            created_time=record.get("Created_Time"),
            modified_time=record.get("Modified_Time")
        )

    async def get_call_info(self, call_id: str) -> Call:
        """Get call information (alias for get_call)"""
        return await self.get_call(call_id)

    async def search_calls(self, **criteria) -> List[Call]:
        """Search calls with criteria"""
        data = await self._request("GET", "/Calls/search", params=criteria)

        calls = []
        for record in data.get("data", []):
            calls.append(Call(
                call_id=record.get("id", ""),
                subject=record.get("Subject", ""),
                call_type=record.get("Call_Type", ""),
                call_duration=record.get("Call_Duration"),
                call_start_time=record.get("Call_Start_Time"),
                description=record.get("Description"),
                created_time=record.get("Created_Time"),
                modified_time=record.get("Modified_Time")
            ))

        return calls

    # ==================== Deal Attachment Operations ====================

    async def deal_get_attachment_info(self, deal_id: str) -> List[Attachment]:
        """Get deal attachment information"""
        data = await self._request("GET", f"/Deals/{deal_id}/Attachments")

        attachments = []
        for record in data.get("data", []):
            attachments.append(Attachment(
                attachment_id=record.get("id", ""),
                file_name=record.get("File_Name", ""),
                size=record.get("Size", 0),
                owner_id=record.get("Owner", {}).get("id") if record.get("Owner") else None,
                created_time=record.get("Created_Time")
            ))

        return attachments

    async def deal_download_attachment(self, attachment_id: str) -> bytes:
        """Download deal attachment"""
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        url = f"{self.base_url}/Deals/{attachment_id}/Attachments"

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    async def deal_upload_file(self, deal_id: str, file_path: str) -> Dict[str, Any]:
        """Upload file to deal"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

            async with self.session.post(
                f"{self.base_url}/Deals/{deal_id}/Attachments",
                headers=headers,
                files=files
            ) as response:
                return await response.json()

    # ==================== Webhook Operations ====================

    async def search_webhooks(self) -> List[Dict[str, Any]]:
        """Search webhooks"""
        data = await self._request("GET", "/settings/webhooks")
        return data.get("webhooks", [])

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        return {"status": "acknowledged", "event_type": event_type}

    # ==================== COQL Query ====================

    async def execute_coql_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute COQL query"""
        data = await self._request("POST", "/coql", json={"select_query": query})
        return data.get("data", [])