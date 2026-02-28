"""
Agendor API Client

Supports 27 API actions and 13 triggers for CRM operations:
- Organizations
- People
- Deals
- Tasks/Activities
- Products

API Reference: https://api.agendor.com.br
Documentation: https://api.agendor.com.br/docs/
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Organization:
    """Organization (company) representation"""
    id: Optional[int] = None
    name: Optional[str] = None
    cnpj: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Person:
    """Person (contact) representation"""
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    job_title: Optional[str] = None
    organization_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Deal:
    """Deal (交易/商读) representation"""
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    stage_id: Optional[int] = None
    stage_name: Optional[str] = None
    status: Optional[str] = None
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    user_id: Optional[int] = None
    close_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Task:
    """Task/Activity representation"""
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    deal_id: Optional[int] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Product:
    """Product representation"""
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    unit: Optional[str] = None
    active: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class AgendorClient:
    """
    Agendor API client for CRM/PaaS operations.

    Authentication: API Token (Header: Authorization: Token {api_token})
    Base URL: https://api.agendor.com.br/v3
    """

    BASE_URL = "https://api.agendor.com.br/v3"

    def __init__(self, api_token: str):
        """
        Initialize Agendor client.

        Args:
            api_token: Agendor API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.api_token}",
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
                raise Exception("Authentication failed: Invalid API token")
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

    # ==================== Organization Operations ====================

    def create_organization(
        self,
        name: str,
        cnpj: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None
    ) -> Organization:
        """Create a new organization"""
        if not name:
            raise ValueError("Organization name is required")

        payload = {"name": name}

        if cnpj:
            payload["cnpj"] = cnpj
        if website:
            payload["website"] = website
        if phone:
            payload["phone"] = phone
        if email:
            payload["email"] = email
        if description:
            payload["description"] = description
        if address:
            payload["address"] = address

        result = self._request("POST", "/organizations", json=payload)
        return self._parse_organization(result)

    def get_organization(self, organization_id: int) -> Organization:
        """Get organization by ID"""
        result = self._request("GET", f"/organizations/{organization_id}")
        return self._parse_organization(result)

    def update_organization(
        self,
        organization_id: int,
        name: Optional[str] = None,
        cnpj: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None
    ) -> Organization:
        """Update organization"""
        payload = {}
        if name:
            payload["name"] = name
        if cnpj:
            payload["cnpj"] = cnpj
        if website:
            payload["website"] = website
        if phone:
            payload["phone"] = phone
        if email:
            payload["email"] = email
        if description:
            payload["description"] = description
        if address:
            payload["address"] = address

        result = self._request("PATCH", f"/organizations/{organization_id}", json=payload)
        return self._parse_organization(result)

    def search_organizations(
        self,
        name: Optional[str] = None,
        cnpj: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 50
    ) -> List[Organization]:
        """Search organizations"""
        params = {}
        if name:
            params["name"] = name
        if cnpj:
            params["cnpj"] = cnpj
        if email:
            params["email"] = email
        params["limit"] = limit

        result = self._request("GET", "/organizations", params=params)

        organizations = []
        if isinstance(result, dict) and "data" in result:
            for org_data in result.get("data", []):
                organizations.append(self._parse_organization(org_data))
        elif isinstance(result, list):
            for org_data in result:
                organizations.append(self._parse_organization(org_data))

        return organizations

    # ==================== Person Operations ====================

    def create_person(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        job_title: Optional[str] = None,
        organization_id: Optional[int] = None
    ) -> Person:
        """Create a new person"""
        if not name:
            raise ValueError("Person name is required")

        payload = {"name": name}

        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if cpf:
            payload["cpf"] = cpf
        if job_title:
            payload["jobTitle"] = job_title
        if organization_id:
            payload["organizationId"] = organization_id

        result = self._request("POST", "/people", json=payload)
        return self._parse_person(result)

    def get_person(self, person_id: int) -> Person:
        """Get person by ID"""
        result = self._request("GET", f"/people/{person_id}")
        return self._parse_person(result)

    def update_person(
        self,
        person_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        job_title: Optional[str] = None,
        organization_id: Optional[int] = None
    ) -> Person:
        """Update person"""
        payload = {}
        if name:
            payload["name"] = name
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if cpf:
            payload["cpf"] = cpf
        if job_title:
            payload["jobTitle"] = job_title
        if organization_id:
            payload["organizationId"] = organization_id

        result = self._request("PATCH", f"/people/{person_id}", json=payload)
        return self._parse_person(result)

    def search_people(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        organization_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Person]:
        """Search people"""
        params = {}
        if name:
            params["name"] = name
        if email:
            params["email"] = email
        if organization_id:
            params["organizationId"] = organization_id
        params["limit"] = limit

        result = self._request("GET", "/people", params=params)

        people = []
        if isinstance(result, dict) and "data" in result:
            for person_data in result.get("data", []):
                people.append(self._parse_person(person_data))
        elif isinstance(result, list):
            for person_data in result:
                people.append(self._parse_person(person_data))

        return people

    # ==================== Deal Operations ====================

    def create_deal_for_person(
        self,
        person_id: int,
        title: str,
        value: Optional[float] = None,
        stage_id: Optional[int] = None,
        description: Optional[str] = None,
        close_date: Optional[str] = None
    ) -> Deal:
        """Create deal for a person"""
        if not person_id:
            raise ValueError("Person ID is required")
        if not title:
            raise ValueError("Deal title is required")

        payload = {
            "personId": person_id,
            "title": title
        }

        if value:
            payload["value"] = value
        if stage_id:
            payload["stageId"] = stage_id
        if description:
            payload["description"] = description
        if close_date:
            payload["closeDate"] = close_date

        result = self._request("POST", "/deals", json=payload)
        return self._parse_deal(result)

    def create_deal_for_organization(
        self,
        organization_id: int,
        title: str,
        value: Optional[float] = None,
        stage_id: Optional[int] = None,
        description: Optional[str] = None,
        close_date: Optional[str] = None
    ) -> Deal:
        """Create deal for an organization"""
        if not organization_id:
            raise ValueError("Organization ID is required")
        if not title:
            raise ValueError("Deal title is required")

        payload = {
            "organizationId": organization_id,
            "title": title
        }

        if value:
            payload["value"] = value
        if stage_id:
            payload["stageId"] = stage_id
        if description:
            payload["description"] = description
        if close_date:
            payload["closeDate"] = close_date

        result = self._request("POST", "/deals", json=payload)
        return self._parse_deal(result)

    def get_deal(self, deal_id: int) -> Deal:
        """Get deal by ID"""
        result = self._request("GET", f"/deals/{deal_id}")
        return self._parse_deal(result)

    def get_deal_of_person(self, person_id: int) -> Deal:
        """Get deal associated with a person"""
        result = self._request("GET", f"/people/{person_id}/deals")
        if isinstance(result, dict) and "data" in result and result["data"]:
            return self._parse_deal(result["data"][0])
        return None

    def get_deal_of_organization(self, organization_id: int) -> Deal:
        """Get deal associated with an organization"""
        result = self._request("GET", f"/organizations/{organization_id}/deals")
        if isinstance(result, dict) and "data" in result and result["data"]:
            return self._parse_deal(result["data"][0])
        return None

    def update_deal(
        self,
        deal_id: int,
        title: Optional[str] = None,
        value: Optional[float] = None,
        stage_id: Optional[int] = None,
        description: Optional[str] = None,
        close_date: Optional[str] = None
    ) -> Deal:
        """Update deal"""
        payload = {}
        if title:
            payload["title"] = title
        if value:
            payload["value"] = value
        if stage_id:
            payload["stageId"] = stage_id
        if description:
            payload["description"] = description
        if close_date:
            payload["closeDate"] = close_date

        result = self._request("PATCH", f"/deals/{deal_id}", json=payload)
        return self._parse_deal(result)

    def update_deal_stage(self, deal_id: int, stage_id: int) -> Deal:
        """Update deal stage"""
        if not stage_id:
            raise ValueError("Stage ID is required")

        payload = {"stageId": stage_id}
        result = self._request("PATCH", f"/deals/{deal_id}", json=payload)
        return self._parse_deal(result)

    def update_deal_status(self, deal_id: int, status: str) -> Deal:
        """Update deal status (e.g., 'won', 'lost', 'open')"""
        valid_statuses = ['won', 'lost', 'open']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

        payload = {"status": status}
        result = self._request("PATCH", f"/deals/{deal_id}", json=payload)
        return self._parse_deal(result)

    def search_deals(
        self,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Deal]:
        """Search deals"""
        params = {}
        if person_id:
            params["personId"] = person_id
        if organization_id:
            params["organizationId"] = organization_id
        if stage_id:
            params["stageId"] = stage_id
        if status:
            params["status"] = status
        params["limit"] = limit

        result = self._request("GET", "/deals", params=params)

        deals = []
        if isinstance(result, dict) and "data" in result:
            for deal_data in result.get("data", []):
                deals.append(self._parse_deal(deal_data))
        elif isinstance(result, list):
            for deal_data in result:
                deals.append(self._parse_deal(deal_data))

        return deals

    # ==================== Task/Activity Operations ====================

    def create_task_for_person(
        self,
        person_id: int,
        title: str,
        description: Optional[str] = None,
        task_type: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """Create task for a person"""
        if not person_id:
            raise ValueError("Person ID is required")
        if not title:
            raise ValueError("Task title is required")

        payload = {
            "personId": person_id,
            "title": title
        }

        if description:
            payload["description"] = description
        if task_type:
            payload["type"] = task_type
        if due_date:
            payload["dueDate"] = due_date

        result = self._request("POST", "/tasks", json=payload)
        return self._parse_task(result)

    def create_task_for_organization(
        self,
        organization_id: int,
        title: str,
        description: Optional[str] = None,
        task_type: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """Create task for an organization"""
        if not organization_id:
            raise ValueError("Organization ID is required")
        if not title:
            raise ValueError("Task title is required")

        payload = {
            "organizationId": organization_id,
            "title": title
        }

        if description:
            payload["description"] = description
        if task_type:
            payload["type"] = task_type
        if due_date:
            payload["dueDate"] = due_date

        result = self._request("POST", "/tasks", json=payload)
        return self._parse_task(result)

    def create_task_for_deal(
        self,
        deal_id: int,
        title: str,
        description: Optional[str] = None,
        task_type: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """Create task for a deal"""
        if not deal_id:
            raise ValueError("Deal ID is required")
        if not title:
            raise ValueError("Task title is required")

        payload = {
            "dealId": deal_id,
            "title": title
        }

        if description:
            payload["description"] = description
        if task_type:
            payload["type"] = task_type
        if due_date:
            payload["dueDate"] = due_date

        result = self._request("POST", "/tasks", json=payload)
        return self._parse_task(result)

    def search_tasks_of_person(self, person_id: int, limit: int = 50) -> List[Task]:
        """Search tasks for a person"""
        result = self._request("GET", f"/people/{person_id}/tasks", params={"limit": limit})

        tasks = []
        if isinstance(result, dict) and "data" in result:
            for task_data in result.get("data", []):
                tasks.append(self._parse_task(task_data))
        elif isinstance(result, list):
            for task_data in result:
                tasks.append(self._parse_task(task_data))

        return tasks

    def search_tasks_of_organization(self, organization_id: int, limit: int = 50) -> List[Task]:
        """Search tasks for an organization"""
        result = self._request("GET", f"/organizations/{organization_id}/tasks", params={"limit": limit})

        tasks = []
        if isinstance(result, dict) and "data" in result:
            for task_data in result.get("data", []):
                tasks.append(self._parse_task(task_data))
        elif isinstance(result, list):
            for task_data in result:
                tasks.append(self._parse_task(task_data))

        return tasks

    def search_tasks_of_deals(self, deal_id: int, limit: int = 50) -> List[Task]:
        """Search tasks for a deal"""
        result = self._request("GET", f"/deals/{deal_id}/tasks", params={"limit": limit})

        tasks = []
        if isinstance(result, dict) and "data" in result:
            for task_data in result.get("data", []):
                tasks.append(self._parse_task(task_data))
        elif isinstance(result, list):
            for task_data in result:
                tasks.append(self._parse_task(task_data))

        return tasks

    # ==================== Product Operations ====================

    def create_product(
        self,
        name: str,
        description: Optional[str] = None,
        code: Optional[str] = None,
        price: Optional[float] = None,
        cost: Optional[float] = None,
        unit: Optional[str] = None
    ) -> Product:
        """Create a new product"""
        if not name:
            raise ValueError("Product name is required")

        payload = {"name": name}

        if description:
            payload["description"] = description
        if code:
            payload["code"] = code
        if price:
            payload["price"] = price
        if cost:
            payload["cost"] = cost
        if unit:
            payload["unit"] = unit

        result = self._request("POST", "/products", json=payload)
        return self._parse_product(result)

    def get_product(self, product_id: int) -> Product:
        """Get product by ID"""
        result = self._request("GET", f"/products/{product_id}")
        return self._parse_product(result)

    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        code: Optional[str] = None,
        price: Optional[float] = None,
        cost: Optional[float] = None,
        unit: Optional[str] = None,
        active: Optional[bool] = None
    ) -> Product:
        """Update product"""
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if code:
            payload["code"] = code
        if price:
            payload["price"] = price
        if cost:
            payload["cost"] = cost
        if unit:
            payload["unit"] = unit
        if active is not None:
            payload["active"] = active

        result = self._request("PATCH", f"/products/{product_id}", json=payload)
        return self._parse_product(result)

    def search_products(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        limit: int = 50
    ) -> List[Product]:
        """Search products"""
        params = {}
        if name:
            params["name"] = name
        if code:
            params["code"] = code
        params["limit"] = limit

        result = self._request("GET", "/products", params=params)

        products = []
        if isinstance(result, dict) and "data" in result:
            for product_data in result.get("data", []):
                products.append(self._parse_product(product_data))
        elif isinstance(result, list):
            for product_data in result:
                products.append(self._parse_product(product_data))

        return products

    # ==================== Helper Methods ====================

    def _parse_organization(self, data: Dict[str, Any]) -> Organization:
        """Parse organization data from API response"""
        return Organization(
            id=data.get("id"),
            name=data.get("name"),
            cnpj=data.get("cnpj"),
            website=data.get("website"),
            phone=data.get("phone"),
            email=data.get("email"),
            description=data.get("description"),
            address=data.get("address"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def _parse_person(self, data: Dict[str, Any]) -> Person:
        """Parse person data from API response"""
        return Person(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            cpf=data.get("cpf"),
            job_title=data.get("jobTitle"),
            organization_id=data.get("organizationId"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def _parse_deal(self, data: Dict[str, Any]) -> Deal:
        """Parse deal data from API response"""
        return Deal(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            value=data.get("value"),
            stage_id=data.get("stageId"),
            stage_name=data.get("stage", {}).get("name") if data.get("stage") else None,
            status=data.get("status"),
            person_id=data.get("personId"),
            organization_id=data.get("organizationId"),
            user_id=data.get("userId"),
            close_date=data.get("closeDate"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data from API response"""
        return Task(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            task_type=data.get("type"),
            due_date=data.get("dueDate"),
            status=data.get("status"),
            person_id=data.get("personId"),
            organization_id=data.get("organizationId"),
            deal_id=data.get("dealId"),
            completed_at=data.get("completedAt"),
            created_at=data.get("createdAt")
        )

    def _parse_product(self, data: Dict[str, Any]) -> Product:
        """Parse product data from API response"""
        return Product(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            code=data.get("code"),
            price=data.get("price"),
            cost=data.get("cost"),
            unit=data.get("unit"),
            active=data.get("active"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_agendor_api_token"

    client = AgendorClient(api_token=api_token)

    try:
        # Example: Create an organization
        org = client.create_organization(
            name="Example Company",
            cnpj="12.345.678/0001-90",
            email="contact@example.com",
            phone="+55 11 1234-5678"
        )
        print(f"Created organization: {org.name} (ID: {org.id})")

        # Example: Search organizations
        orgs = client.search_organizations(name="Example")
        print(f"Found {len(orgs)} organizations")

        # Example: Create a person
        person = client.create_person(
            name="John Doe",
            email="john@example.com",
            phone="+55 11 98765-4321",
            organization_id=org.id
        )
        print(f"Created person: {person.name} (ID: {person.id})")

        # Example: Create a deal
        deal = client.create_deal_for_organization(
            organization_id=org.id,
            title="Software License",
            value=10000.0
        )
        print(f"Created deal: {deal.title} (ID: {deal.id})")

        # Example: Create a task
        task = client.create_task_for_deal(
            deal_id=deal.id,
            title="Send proposal",
            due_date="2026-03-15"
        )
        print(f"Created task: {task.title} (ID: {task.id})")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()