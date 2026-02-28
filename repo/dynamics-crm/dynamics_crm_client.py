"""
Dynamics CRM API Client

Complete client for Microsoft Dynamics CRM.
Supports leads, opportunities (案件), companies (取引先企業), and contacts (取引先担当者).
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


class DynamicsCrmAPIError(Exception):
    """Base exception for Dynamics CRM API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class DynamicsCrmRateLimitError(DynamicsCrmAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Lead:
    lead_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Contact:
    contact_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    company_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Company:
    company_id: str
    name: str
    website: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Opportunity:
    opportunity_id: str
    name: str
    value: float
    currency: str
    status: str
    lead_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class DynamicsCRMClient:
    """Microsoft Dynamics CRM API Client."""

    BASE_API_PATH = "/api/data/v9.2"

    def __init__(
        self,
        api_key: str,
        organization_url: str,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.organization_url = organization_url.rstrip("/")
        self.base_url = f"{self.organization_url}{self.BASE_API_PATH}"
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_requests_per_minute = max_requests_per_minute
        self._request_times: List[float] = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        now = asyncio.get_event_loop().time()
        self._request_times = [t for t in self._request_times if now - t < 60]

        if len(self._request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self._request_times = []

        self._request_times.append(now)

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        await self._check_rate_limit()
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0"
        }

        if not self.session:
            raise RuntimeError("Client must be used as async context manager")

        try:
            async with self.session.request(
                method, url, json=data, params=params, headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise DynamicsCrmRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", {}).get("message", str(response_data))
                    raise DynamicsCrmAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise DynamicsCrmAPIError(f"Network error: {str(e)}")

    # ==================== Leads (リード) ====================

    async def create_lead(self, lead_data: Dict[str, Any]) -> Lead:
        data = await self._request("POST", "/leads", data=lead_data)
        return Lead(
            lead_id=data.get("leadid", ""),
            name=data.get("fullname", ""),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            company=data.get("companyname"),
            status=data.get("statecode"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["leadid", "fullname", "emailaddress1", "telephone1", "companyname", "statecode", "createdon", "modifiedon"]}
        )

    async def get_lead(self, lead_id: str) -> Lead:
        data = await self._request("GET", f"/leads({lead_id})")
        return Lead(
            lead_id=data.get("leadid", lead_id),
            name=data.get("fullname", ""),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            company=data.get("companyname"),
            status=data.get("statecode"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["leadid", "fullname", "emailaddress1", "telephone1", "companyname", "statecode", "createdon", "modifiedon"]}
        )

    async def update_lead(self, lead_id: str, update_data: Dict[str, Any]) -> Lead:
        data = await self._request("PATCH", f"/leads({lead_id})", data=update_data)
        return Lead(
            lead_id=lead_id,
            name=data.get("fullname", update_data.get("fullname", "")),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            company=data.get("companyname"),
            status=data.get("statecode"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["fullname", "emailaddress1", "telephone1", "companyname", "statecode", "createdon", "modifiedon"]}
        )

    async def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/leads({lead_id})")

    async def search_leads(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Lead]:
        params = {"$top": limit, "$skip": offset}
        if query:
            params["$filter"] = query

        data = await self._request("GET", "/leads", params=params)
        results = data.get("value", [])

        return [Lead(
            lead_id=r.get("leadid", ""),
            name=r.get("fullname", ""),
            email=r.get("emailaddress1"),
            phone=r.get("telephone1"),
            company=r.get("companyname"),
            status=r.get("statecode"),
            created_at=r.get("createdon"),
            updated_at=r.get("modifiedon"),
            additional_data={k: v for k, v in r.items() if k not in ["leadid", "fullname", "emailaddress1", "telephone1", "companyname", "statecode", "createdon", "modifiedon"]}
        ) for r in results]

    async def update_lead_custom_field(
        self,
        lead_id: str,
        field_name: str,
        field_value: Any
    ) -> Lead:
        return await self.update_lead(lead_id, {field_name: field_value})

    # ==================== Opportunities (案件) ====================

    async def create_opportunity(self, opportunity_data: Dict[str, Any]) -> Opportunity:
        data = await self._request("POST", "/opportunities", data=opportunity_data)
        return Opportunity(
            opportunity_id=data.get("opportunityid", ""),
            name=data.get("name", ""),
            value=data.get("estimatedvalue", 0.0),
            currency=data.get("transactioncurrencyid", ""),
            status=data.get("statecode", ""),
            lead_id=data.get("leadid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["opportunityid", "name", "estimatedvalue", "transactioncurrencyid", "statecode", "leadid", "createdon", "modifiedon"]}
        )

    async def get_opportunity(self, opportunity_id: str) -> Opportunity:
        data = await self._request("GET", f"/opportunities({opportunity_id})")
        return Opportunity(
            opportunity_id=data.get("opportunityid", opportunity_id),
            name=data.get("name", ""),
            value=data.get("estimatedvalue", 0.0),
            currency=data.get("transactioncurrencyid", ""),
            status=data.get("statecode", ""),
            lead_id=data.get("leadid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["opportunityid", "name", "estimatedvalue", "transactioncurrencyid", "statecode", "leadid", "createdon", "modifiedon"]}
        )

    async def update_opportunity(self, opportunity_id: str, update_data: Dict[str, Any]) -> Opportunity:
        data = await self._request("PATCH", f"/opportunities({opportunity_id})", data=update_data)
        return Opportunity(
            opportunity_id=opportunity_id,
            name=data.get("name", update_data.get("name", "")),
            value=data.get("estimatedvalue", 0.0),
            currency=data.get("transactioncurrencyid", ""),
            status=data.get("statecode", ""),
            lead_id=data.get("leadid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "estimatedvalue", "transactioncurrencyid", "statecode", "leadid", "createdon", "modifiedon"]}
        )

    async def delete_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/opportunities({opportunity_id})")

    async def search_opportunities(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Opportunity]:
        params = {"$top": limit, "$skip": offset}
        if query:
            params["$filter"] = query

        data = await self._request("GET", "/opportunities", params=params)
        results = data.get("value", [])

        return [Opportunity(
            opportunity_id=r.get("opportunityid", ""),
            name=r.get("name", ""),
            value=r.get("estimatedvalue", 0.0),
            currency=r.get("transactioncurrencyid", ""),
            status=r.get("statecode", ""),
            lead_id=r.get("leadid"),
            created_at=r.get("createdon"),
            updated_at=r.get("modifiedon"),
            additional_data={k: v for k, v in r.items() if k not in ["opportunityid", "name", "estimatedvalue", "transactioncurrencyid", "statecode", "leadid", "createdon", "modifiedon"]}
        ) for r in results]

    async def update_opportunity_custom_field(
        self,
        opportunity_id: str,
        field_name: str,
        field_value: Any
    ) -> Opportunity:
        return await self.update_opportunity(opportunity_id, {field_name: field_value})

    # ==================== Companies (取引先企業) ====================

    async def create_company(self, company_data: Dict[str, Any]) -> Company:
        data = await self._request("POST", "/accounts", data=company_data)
        return Company(
            company_id=data.get("accountid", ""),
            name=data.get("name", ""),
            website=data.get("websiteurl"),
            address=data.get("address1_composite"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["accountid", "name", "websiteurl", "address1_composite", "createdon", "modifiedon"]}
        )

    async def get_company(self, company_id: str) -> Company:
        data = await self._request("GET", f"/accounts({company_id})")
        return Company(
            company_id=data.get("accountid", company_id),
            name=data.get("name", ""),
            website=data.get("websiteurl"),
            address=data.get("address1_composite"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["accountid", "name", "websiteurl", "address1_composite", "createdon", "modifiedon"]}
        )

    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> Company:
        data = await self._request("PATCH", f"/accounts({company_id})", data=update_data)
        return Company(
            company_id=company_id,
            name=data.get("name", update_data.get("name", "")),
            website=data.get("websiteurl"),
            address=data.get("address1_composite"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "websiteurl", "address1_composite", "createdon", "modifiedon"]}
        )

    async def delete_company(self, company_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/accounts({company_id})")

    async def search_companies(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Company]:
        params = {"$top": limit, "$skip": offset}
        if query:
            params["$filter"] = query

        data = await self._request("GET", "/accounts", params=params)
        results = data.get("value", [])

        return [Company(
            company_id=r.get("accountid", ""),
            name=r.get("name", ""),
            website=r.get("websiteurl"),
            address=r.get("address1_composite"),
            created_at=r.get("createdon"),
            updated_at=r.get("modifiedon"),
            additional_data={k: v for k, v in r.items() if k not in ["accountid", "name", "websiteurl", "address1_composite", "createdon", "modifiedon"]}
        ) for r in results]

    async def update_company_custom_field(
        self,
        company_id: str,
        field_name: str,
        field_value: Any
    ) -> Company:
        return await self.update_company(company_id, {field_name: field_value})

    # ==================== Contacts (取引先担当者) ====================

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        data = await self._request("POST", "/contacts", data=contact_data)
        return Contact(
            contact_id=data.get("contactid", ""),
            name=data.get("fullname", ""),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            title=data.get("jobtitle"),
            company_id=data.get("parentcustomerid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["contactid", "fullname", "emailaddress1", "telephone1", "jobtitle", "parentcustomerid", "createdon", "modifiedon"]}
        )

    async def get_contact(self, contact_id: str) -> Contact:
        data = await self._request("GET", f"/contacts({contact_id})")
        return Contact(
            contact_id=data.get("contactid", contact_id),
            name=data.get("fullname", ""),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            title=data.get("jobtitle"),
            company_id=data.get("parentcustomerid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["contactid", "fullname", "emailaddress1", "telephone1", "jobtitle", "parentcustomerid", "createdon", "modifiedon"]}
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        data = await self._request("PATCH", f"/contacts({contact_id})", data=update_data)
        return Contact(
            contact_id=contact_id,
            name=data.get("fullname", update_data.get("fullname", "")),
            email=data.get("emailaddress1"),
            phone=data.get("telephone1"),
            title=data.get("jobtitle"),
            company_id=data.get("parentcustomerid"),
            created_at=data.get("createdon"),
            updated_at=data.get("modifiedon"),
            additional_data={k: v for k, v in data.items() if k not in ["fullname", "emailaddress1", "telephone1", "jobtitle", "parentcustomerid", "createdon", "modifiedon"]}
        )

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/contacts({contact_id})")

    async def search_contacts(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contact]:
        params = {"$top": limit, "$skip": offset}
        if query:
            params["$filter"] = query

        data = await self._request("GET", "/contacts", params=params)
        results = data.get("value", [])

        return [Contact(
            contact_id=r.get("contactid", ""),
            name=r.get("fullname", ""),
            email=r.get("emailaddress1"),
            phone=r.get("telephone1"),
            title=r.get("jobtitle"),
            company_id=r.get("parentcustomerid"),
            created_at=r.get("createdon"),
            updated_at=r.get("modifiedon"),
            additional_data={k: v for k, v in r.items() if k not in ["contactid", "fullname", "emailaddress1", "telephone1", "jobtitle", "parentcustomerid", "createdon", "modifiedon"]}
        ) for r in results]

    async def get_contact_info(self, contact_id: str) -> Contact:
        """Get contact information (duplicate of get_contact)."""
        return await self.get_contact(contact_id)

    async def update_contact_info(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update contact information (duplicate of update_contact)."""
        return await self.update_contact(contact_id, update_data)

    async def update_contact_custom_field(
        self,
        contact_id: str,
        field_name: str,
        field_value: Any
    ) -> Contact:
        return await self.update_contact(contact_id, {field_name: field_value})

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with DynamicsCRMClient(
        api_key="your_api_key",
        organization_url="https://yourorg.api.crm.dynamics.com"
    ) as client:
        lead = await client.create_lead({
            "fullname": "John Smith",
            "emailaddress1": "john@example.com",
            "companyname": "Acme Corp"
        })
        print(f"Created lead: {lead.lead_id}")


if __name__ == "__main__":
    asyncio.run(main())