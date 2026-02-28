"""
Apptivo API Client

CRM and business process automation platform for managing:
- Leads, Contacts, Customers
- Projects, Tasks
- Invoicing
- Contracts

API Actions (estimated 15-20):
1. Create Lead
2. Update Lead
3. Get Lead
4. Search Leads
5. Convert Lead to Customer
6. Create Contact
7. Update Contact
8. Get Contact
9. Create Project
10. Update Project
11. Get Project
12. Create Task
13. Update Task
14. Get Invoice
15. Create Invoice

Triggers (estimated 5-8):
- New Lead Created
- Lead Converted
- New Contact Added
- Project Status Changed
- Task Completed
- Invoice Paid

Authentication: API Key
Base URL: https://www.apptivo.com/app/dao
Documentation: https://www.apptivo.com/public/apidocs.jsp
Rate Limiting: 1000 requests per day
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Lead:
    """Lead model"""
    lead_id: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    status: str = ""
    lead_source: Optional[str] = None
    created_time: Optional[str] = None
    modified_time: Optional[str] = None


@dataclass
class Contact:
    """Contact model"""
    contact_id: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    is_active: bool = True
    created_time: Optional[str] = None


@dataclass
class Customer:
    """Customer model"""
    customer_id: str
    name: str = ""
    email: str = ""
    phone: str = ""
    address: Optional[Dict[str, str]] = None
    created_time: Optional[str] = None


@dataclass
class Project:
    """Project model"""
    project_id: str
    name: str = ""
    description: str = ""
    status: str = ""
    priority: str = "Medium"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    assigned_to: Optional[str] = None


@dataclass
class Task:
    """Task model"""
    task_id: str
    title: str = ""
    description: str = ""
    status: str = ""
    priority: str = "Medium"
    due_date: Optional[str] = None
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None


class ApptivoClient:
    """
    Apptivo API client for CRM and business operations.

    Supports: Leads, Contacts, Customers, Projects, Tasks, Invoices
    Rate limit: 1000 requests/day
    """

    BASE_URL = "https://www.apptivo.com/app/dao"

    def __init__(self, api_key: str, office_key: str):
        """
        Initialize Apptivo client.

        Args:
            api_key: Your Apptivo API key
            office_key: Your Apptivo office key
        """
        self.api_key = api_key
        self.office_key = office_key
        self.session = None
        self._headers = {
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        service: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request.

        Args:
            method: HTTP method
            service: Apptivo service name
            data: Request body data
            params: Query parameters (apiKey, officeKey added automatically)

        Returns:
            Response JSON
        """
        url = f"{self.BASE_URL}/{service}"

        request_params = params or {}
        request_params["apiKey"] = self.api_key
        request_params["officeKey"] = self.office_key
        request_params["jsonData"] = "true"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=request_params
        ) as response:
            result = await response.json()

            response_code = result.get("responseCode", "")
            if response_code != "0":
                error = result.get("responseMessage", "Unknown error")
                raise Exception(
                    f"Apptivo API error: {error}"
                )

            return result

    # ==================== Lead Operations ====================

    async def create_lead(
        self,
        first_name: str,
        last_name: str,
        email: str = "",
        phone: str = "",
        company: str = ""
    ) -> Lead:
        """Create a new lead"""
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "company": company
        }
        response = await self._make_request("GET", "lead", data=data)
        lead_data = response.get("lead", {})
        return Lead(
            lead_id=lead_data.get("leadId", ""),
            first_name=lead_data.get("firstName", first_name),
            last_name=lead_data.get("lastName", last_name),
            email=lead_data.get("email", email or lead_data.get("email", "")),
            phone=lead_data.get("phone", phone or lead_data.get("phone", "")),
            company=lead_data.get("company", company or lead_data.get("company", "")),
            status=lead_data.get("leadStatus", ""),
            lead_source=lead_data.get("leadSource")
        )

    async def get_lead(self, lead_id: str) -> Lead:
        """Get lead by ID"""
        params = {"leadId": lead_id}
        response = await self._make_request("GET", "lead", params=params)
        lead_data = response.get("lead", {})
        return Lead(
            lead_id=lead_data.get("leadId", ""),
            first_name=lead_data.get("firstName", ""),
            last_name=lead_data.get("lastName", ""),
            email=lead_data.get("email", ""),
            phone=lead_data.get("phone", ""),
            company=lead_data.get("company", ""),
            status=lead_data.get("leadStatus", ""),
            created_time=lead_data.get("createdTime"),
            modified_time=lead_data.get("modifiedTime")
        )

    async def update_lead(
        self,
        lead_id: str,
        **fields
    ) -> Lead:
        """Update a lead"""
        data = {"leadId": lead_id, **fields}
        response = await self._make_request("POST", "lead", data=data)
        lead_data = response.get("lead", {})
        return Lead(
            lead_id=lead_data.get("leadId", ""),
            first_name=lead_data.get("firstName", ""),
            last_name=lead_data.get("lastName", ""),
            email=lead_data.get("email", ""),
            phone=lead_data.get("phone", ""),
            company=lead_data.get("company", ""),
            status=lead_data.get("leadStatus", "")
        )

    async def search_leads(
        self,
        email: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50
    ) -> List[Lead]:
        """Search for leads"""
        params = {}
        if email:
            params["email"] = email
        if company:
            params["company"] = company

        response = await self._make_request("GET", "lead", params=params)
        leads_data = response.get("data", {}).get("leads", [])
        leads = []
        for lead_data in leads_data[:limit]:
            leads.append(Lead(
                lead_id=lead_data.get("leadId", ""),
                first_name=lead_data.get("firstName", ""),
                last_name=lead_data.get("lastName", ""),
                email=lead_data.get("email", ""),
                phone=lead_data.get("phone", ""),
                company=lead_data.get("company", ""),
                status=lead_data.get("leadStatus", ""),
                created_time=lead_data.get("createdTime")
            ))
        return leads

    async def convert_lead_to_customer(
        self,
        lead_id: str,
        customer_name: str
    ) -> Customer:
        """Convert lead to customer"""
        data = {
            "leadId": lead_id,
            "customerName": customer_name
        }
        response = await self._make_request("GET", "lead/converttocustomer", data=data)
        customer_data = response.get("customer", {})
        return Customer(
            customer_id=customer_data.get("customerId", ""),
            name=customer_data.get("name", ""),
            email=customer_data.get("email", ""),
            phone=customer_data.get("phone", ""),
            address=customer_data.get("address"),
            created_time=customer_data.get("createdTime")
        )

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str = "",
        phone: str = "",
        company: str = ""
    ) -> Contact:
        """Create a contact"""
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "company": company
        }
        response = await self._make_request("GET", "contact", data=data)
        contact_data = response.get("contact", {})
        return Contact(
            contact_id=contact_data.get("contactId", ""),
            first_name=contact_data.get("firstName", first_name),
            last_name=contact_data.get("lastName", last_name),
            email=contact_data.get("email", email or contact_data.get("email", "")),
            phone=contact_data.get("phone", phone or contact_data.get("phone", "")),
            company=contact_data.get("company", company or contact_data.get("company", "")),
            created_time=contact_data.get("createdTime")
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID"""
        params = {"contactId": contact_id}
        response = await self._make_request("GET", "contact", params=params)
        contact_data = response.get("contact", {})
        return Contact(
            contact_id=contact_data.get("contactId", ""),
            first_name=contact_data.get("firstName", ""),
            last_name=contact_data.get("lastName", ""),
            email=contact_data.get("email", ""),
            phone=contact_data.get("phone", ""),
            company=contact_data.get("company", ""),
            is_active=contact_data.get("isActive", True),
            created_time=contact_data.get("createdTime")
        )

    async def update_contact(
        self,
        contact_id: str,
        **fields
    ) -> Contact:
        """Update a contact"""
        data = {"contactId": contact_id, **fields}
        response = await self._make_request("POST", "contact", data=data)
        contact_data = response.get("contact", {})
        return Contact(
            contact_id=contact_data.get("contactId", ""),
            first_name=contact_data.get("firstName", ""),
            last_name=contact_data.get("lastName", ""),
            email=contact_data.get("email", ""),
            phone=contact_data.get("phone", ""),
            company=contact_data.get("company", "")
        )

    # ==================== Project Operations ====================

    async def create_project(
        self,
        name: str,
        description: str = "",
        **fields
    ) -> Project:
        """Create a project"""
        data = {
            "name": name,
            "description": description,
            **fields
        }
        response = await self._make_request("GET", "project", data=data)
        project_data = response.get("project", {})
        return Project(
            project_id=project_data.get("projectId", ""),
            name=project_data.get("name", name),
            description=project_data.get("description", description),
            status=project_data.get("status", ""),
            priority=project_data.get("priority", "Medium"),
            start_date=project_data.get("startDate"),
            end_date=project_data.get("endDate"),
            assigned_to=project_data.get("assignedTo")
        )

    async def get_project(self, project_id: str) -> Project:
        """Get project by ID"""
        params = {"projectId": project_id}
        response = await self._make_request("GET", "project", params=params)
        project_data = response.get("project", {})
        return Project(
            project_id=project_data.get("projectId", ""),
            name=project_data.get("name", ""),
            description=project_data.get("description", ""),
            status=project_data.get("status", ""),
            priority=project_data.get("priority", "Medium"),
            start_date=project_data.get("startDate"),
            end_date=project_data.get("endDate"),
            assigned_to=project_data.get("assignedTo")
        )

    async def update_project(
        self,
        project_id: str,
        **fields
    ) -> Project:
        """Update a project"""
        data = {"projectId": project_id, **fields}
        response = await self._make_request("POST", "project", data=data)
        project_data = response.get("project", {})
        return Project(
            project_id=project_data.get("projectId", ""),
            name=project_data.get("name", ""),
            description=project_data.get("description", ""),
            status=project_data.get("status", ""),
            priority=project_data.get("priority", "Medium")
        )

    # ==================== Task Operations ====================

    async def create_task(
        self,
        title: str,
        project_id: Optional[str] = None,
        **fields
    ) -> Task:
        """Create a task"""
        data = {
            "title": title,
            **fields
        }
        if project_id:
            data["projectId"] = project_id

        response = await self._make_request("GET", "task", data=data)
        task_data = response.get("task", {})
        return Task(
            task_id=task_data.get("taskId", ""),
            title=task_data.get("title", title),
            description=task_data.get("description", ""),
            status=task_data.get("status", ""),
            priority=task_data.get("priority", "Medium"),
            due_date=task_data.get("dueDate"),
            project_id=task_data.get("projectId"),
            assigned_to=task_data.get("assignedTo")
        )

    async def update_task(
        self,
        task_id: str,
        **fields
    ) -> Task:
        """Update a task"""
        data = {"taskId": task_id, **fields}
        response = await self._make_request("POST", "task", data=data)
        task_data = response.get("task", {})
        return Task(
            task_id=task_data.get("taskId", ""),
            title=task_data.get("title", ""),
            description=task_data.get("description", ""),
            status=task_data.get("status", ""),
            priority=task_data.get("priority", "Medium"),
            due_date=task_data.get("dueDate"),
            project_id=task_data.get("projectId")
        )

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events from Apptivo"""
        entity_type = webhook_data.get("entityType", "unknown")
        event_type = webhook_data.get("eventType", "unknown")
        entity_id = webhook_data.get("entityId")

        return {
            "entity_type": entity_type,
            "event_type": event_type,
            "entity_id": entity_id,
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    api_key = "your_api_key"
    office_key = "your_office_key"

    async with ApptivoClient(api_key, office_key) as client:
        # Create a lead
        lead = await client.create_lead(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Example Corp"
        )
        print(f"Created lead: {lead.lead_id}")

        # Get the lead
        retrieved = await client.get_lead(lead.lead_id)
        print(f"Lead status: {retrieved.status}")

if __name__ == "__main__":
    asyncio.run(main())