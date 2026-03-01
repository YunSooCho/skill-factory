"""
Bitrix API Client

Bitrix24 is a comprehensive CRM and collaboration platform.

Supports:
- Create Lead
- Get Lead
- Update Lead
- Delete Lead
- Search Lead
- Create Deal
- Get Deal
- Update Deal
- Delete Deal
- Search Deal
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Search Contact
- Create Product Item
- Get Product Item
- Update Product Item
- Delete Product Item
- Search Product Item
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Lead:
    """Lead object"""
    id: int
    title: str
    name: str
    status_id: str
    status_name: str
    opportunity: float
    currency: str
    contact_id: Optional[int]
    created_by: int
    date_create: str
    date_modify: str


@dataclass
class Deal:
    """Deal object"""
    id: int
    title: str
    stage_id: str
    stage_name: str
    opportunity: float
    currency: str
    contact_id: Optional[int]
    lead_id: Optional[int]
    created_by: int
    date_create: str
    date_modify: str


@dataclass
class Contact:
    """Contact object"""
    id: int
    name: str
    first_name: str
    last_name: str
    type: str
    phone: Optional[List[str]]
    email: Optional[List[str]]
    created_by: int
    date_create: str
    date_modify: str


@dataclass
class ProductItem:
    """Product Item object"""
    id: int
    name: str
    code: Optional[str]
    price: float
    currency: str
    xml_id: Optional[str]
    created_by: int
    date_create: str
    date_modify: str


class BitrixAPIClient:
    """
    Bitrix24 API client for CRM operations.

    Authentication: REST API (inbound webhook or OAuth)
    Documentation: https://dev.1c-bitrix.ru/rest_help/

    Format: https://{domain}.bitrix24.ru/rest/{user_id}/{access_token}/
    """

    def __init__(self, domain: str, user_id: str, access_token: str):
        """
        Initialize Bitrix API client.

        Args:
            domain: Bitrix24 domain (e.g., "mycompany.bitrix24.com")
            user_id: User ID for webhook
            access_token: API access token
        """
        self.domain = domain.replace("https://", "").replace("http://", "")
        self.user_id = user_id
        self.access_token = access_token
        self.base_url = f"https://{self.domain}/rest/{self.user_id}/{self.access_token}"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Bitrix API.

        Args:
            method: API method name (e.g., "crm.lead.add")
            params: Request parameters

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        url = f"{self.base_url}/{method}"

        async with self.session.post(url, json=params) as response:
            data = await response.json()

            if "error" in data:
                raise Exception(f"Bitrix API error: {data.get('error_description', data.get('error'))}")

            return data.get("result", {})

    async def _batch_request(
        self,
        commands: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Make batch request to Bitrix API.

        Args:
            commands: Dictionary of command_name: {method: "api.method", params: {...}}

        Returns:
            Batch response with result for each command
        """
        batch_params = {
            "halt": 0,
            "cmd": {}
        }

        for cmd_name, cmd in commands.items():
            batch_params["cmd"][cmd_name] = f"{cmd['method']}?{self._params_to_string(cmd.get('params', {}))}"

        return await self._request("batch", batch_params)

    def _params_to_string(self, params: Dict[str, Any]) -> str:
        """Convert params dictionary to query string"""
        return "&".join([f"{k}={v}" for k, v in params.items()])

    # ==================== Leads ====================

    async def create_lead(
        self,
        title: str,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        opportunity: Optional[float] = None,
        status_id: Optional[str] = None,
        comments: Optional[str] = None,
        source_id: Optional[str] = None,
        assigned_by_id: Optional[int] = None
    ) -> Lead:
        """
        Create a new lead.

        Args:
            title: Lead title
            name: Contact person name
            phone: Phone number
            email: Email address
            opportunity: Estimated deal amount
            status_id: Lead status ID
            comments: Additional comments
            source_id: Lead source ID
            assigned_by_id: User ID to assign lead to

        Returns:
            Lead object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {
            "TITLE": title,
            "NAME": name
        }

        if phone:
            fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
        if email:
            fields["EMAIL"] = [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        if opportunity is not None:
            fields["OPPORTUNITY"] = opportunity
        if status_id:
            fields["STATUS_ID"] = status_id
        if comments:
            fields["COMMENTS"] = comments
        if source_id:
            fields["SOURCE_ID"] = source_id
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id

        result = await self._request("crm.lead.add", {"fields": fields})

        return await self.get_lead(result)

    async def get_lead(self, lead_id: int) -> Lead:
        """
        Get a lead by ID.

        Args:
            lead_id: Lead ID

        Returns:
            Lead object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        result = await self._request("crm.lead.get", {"id": lead_id})

        return Lead(
            id=result.get("ID", 0),
            title=result.get("TITLE", ""),
            name=f"{result.get('NAME', '')} {result.get('LAST_NAME', '')}".strip(),
            status_id=result.get("STATUS_ID", ""),
            status_name=result.get("STATUS_NAME", ""),
            opportunity=float(result.get("OPPORTUNITY", 0)),
            currency=result.get("CURRENCY_ID", "USD"),
            contact_id=int(result.get("CONTACT_ID")) if result.get("CONTACT_ID") else None,
            created_by=int(result.get("CREATED_BY_ID", 0)),
            date_create=result.get("DATE_CREATE", ""),
            date_modify=result.get("DATE_MODIFY", "")
        )

    async def update_lead(
        self,
        lead_id: int,
        title: Optional[str] = None,
        status_id: Optional[str] = None,
        opportunity: Optional[float] = None,
        comments: Optional[str] = None,
        assigned_by_id: Optional[int] = None
    ) -> bool:
        """
        Update a lead.

        Args:
            lead_id: Lead ID
            title: New title
            status_id: New status ID
            opportunity: New opportunity amount
            comments: New comments
            assigned_by_id: New assigned user ID

        Returns:
            True if updated successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {}

        if title:
            fields["TITLE"] = title
        if status_id:
            fields["STATUS_ID"] = status_id
        if opportunity is not None:
            fields["OPPORTUNITY"] = opportunity
        if comments:
            fields["COMMENTS"] = comments
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id

        await self._request("crm.lead.update", {"id": lead_id, "fields": fields})
        return True

    async def delete_lead(self, lead_id: int) -> bool:
        """
        Delete a lead.

        Args:
            lead_id: Lead ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("crm.lead.delete", {"id": lead_id})
        return True

    async def search_leads(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        limit: int = 50
    ) -> List[Lead]:
        """
        Search for leads.

        Args:
            filter_params: Filter conditions
            select: Fields to return
            order: Sort order
            limit: Maximum number of leads to return

        Returns:
            List of Lead objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {}

        if filter_params:
            params["filter"] = filter_params
        if select:
            params["select"] = select
        if order:
            params["order"] = order

        result = await self._request("crm.lead.list", params)

        leads = result if isinstance(result, list) else []
        return [
            Lead(
                id=lead.get("ID", 0),
                title=lead.get("TITLE", ""),
                name=f"{lead.get('NAME', '')} {lead.get('LAST_NAME', '')}".strip(),
                status_id=lead.get("STATUS_ID", ""),
                status_name=lead.get("STATUS_NAME", ""),
                opportunity=float(lead.get("OPPORTUNITY", 0)),
                currency=lead.get("CURRENCY_ID", "USD"),
                contact_id=int(lead["CONTACT_ID"]) if lead.get("CONTACT_ID") else None,
                created_by=int(lead.get("CREATED_BY_ID", 0)),
                date_create=lead.get("DATE_CREATE", ""),
                date_modify=lead.get("DATE_MODIFY", "")
            )
            for lead in leads[:limit]
        ]

    # ==================== Deals ====================

    async def create_deal(
        self,
        title: str,
        stage_id: str,
        opportunity: Optional[float] = None,
        currency: str = "USD",
        contact_id: Optional[int] = None,
        lead_id: Optional[int] = None,
        assigned_by_id: Optional[int] = None,
        comments: Optional[str] = None
    ) -> Deal:
        """
        Create a new deal.

        Args:
            title: Deal title
            stage_id: Deal stage ID
            opportunity: Deal amount
            currency: Currency code (default: USD)
            contact_id: Contact ID
            lead_id: Lead ID
            assigned_by_id: User ID to assign deal to
            comments: Additional comments

        Returns:
            Deal object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {
            "TITLE": title,
            "STAGE_ID": stage_id,
            "CURRENCY_ID": currency
        }

        if opportunity is not None:
            fields["OPPORTUNITY"] = opportunity
        if contact_id:
            fields["CONTACT_ID"] = contact_id
        if lead_id:
            fields["LEAD_ID"] = lead_id
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id
        if comments:
            fields["COMMENTS"] = comments

        result = await self._request("crm.deal.add", {"fields": fields})

        return await self.get_deal(result)

    async def get_deal(self, deal_id: int) -> Deal:
        """
        Get a deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            Deal object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        result = await self._request("crm.deal.get", {"id": deal_id})

        return Deal(
            id=result.get("ID", 0),
            title=result.get("TITLE", ""),
            stage_id=result.get("STAGE_ID", ""),
            stage_name=result.get("STAGE_NAME", ""),
            opportunity=float(result.get("OPPORTUNITY", 0)),
            currency=result.get("CURRENCY_ID", "USD"),
            contact_id=int(result["CONTACT_ID"]) if result.get("CONTACT_ID") else None,
            lead_id=int(result["LEAD_ID"]) if result.get("LEAD_ID") else None,
            created_by=int(result.get("CREATED_BY_ID", 0)),
            date_create=result.get("DATE_CREATE", ""),
            date_modify=result.get("DATE_MODIFY", "")
        )

    async def update_deal(
        self,
        deal_id: int,
        title: Optional[str] = None,
        stage_id: Optional[str] = None,
        opportunity: Optional[float] = None,
        contact_id: Optional[int] = None,
        assigned_by_id: Optional[int] = None
    ) -> bool:
        """
        Update a deal.

        Args:
            deal_id: Deal ID
            title: New title
            stage_id: New stage ID
            opportunity: New opportunity amount
            contact_id: New contact ID
            assigned_by_id: New assigned user ID

        Returns:
            True if updated successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {}

        if title:
            fields["TITLE"] = title
        if stage_id:
            fields["STAGE_ID"] = stage_id
        if opportunity is not None:
            fields["OPPORTUNITY"] = opportunity
        if contact_id:
            fields["CONTACT_ID"] = contact_id
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id

        await self._request("crm.deal.update", {"id": deal_id, "fields": fields})
        return True

    async def delete_deal(self, deal_id: int) -> bool:
        """
        Delete a deal.

        Args:
            deal_id: Deal ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("crm.deal.delete", {"id": deal_id})
        return True

    async def search_deals(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        limit: int = 50
    ) -> List[Deal]:
        """
        Search for deals.

        Args:
            filter_params: Filter conditions
            select: Fields to return
            order: Sort order
            limit: Maximum number of deals to return

        Returns:
            List of Deal objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {}

        if filter_params:
            params["filter"] = filter_params
        if select:
            params["select"] = select
        if order:
            params["order"] = order

        result = await self._request("crm.deal.list", params)

        deals = result if isinstance(result, list) else []
        return [
            Deal(
                id=deal.get("ID", 0),
                title=deal.get("TITLE", ""),
                stage_id=deal.get("STAGE_ID", ""),
                stage_name=deal.get("STAGE_NAME", ""),
                opportunity=float(deal.get("OPPORTUNITY", 0)),
                currency=deal.get("CURRENCY_ID", "USD"),
                contact_id=int(deal["CONTACT_ID"]) if deal.get("CONTACT_ID") else None,
                lead_id=int(deal["LEAD_ID"]) if deal.get("LEAD_ID") else None,
                created_by=int(deal.get("CREATED_BY_ID", 0)),
                date_create=deal.get("DATE_CREATE", ""),
                date_modify=deal.get("DATE_MODIFY", "")
            )
            for deal in deals[:limit]
        ]

    # ==================== Contacts ====================

    async def create_contact(
        self,
        name: str,
        first_name: str,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        type_id: str = "CLIENT",
        assigned_by_id: Optional[int] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            name: Contact full name
            first_name: First name
            last_name: Last name
            phone: Phone number
            email: Email address
            type_id: Contact type ID (default: CLIENT)
            assigned_by_id: User ID to assign contact to

        Returns:
            Contact object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {
            "NAME": first_name,
            "LAST_NAME": last_name or "",
            "TYPE_ID": type_id
        }

        if phone:
            fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
        if email:
            fields["EMAIL"] = [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id

        result = await self._request("crm.contact.add", {"fields": fields})

        return await self.get_contact(result)

    async def get_contact(self, contact_id: int) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        result = await self._request("crm.contact.get", {"id": contact_id})

        # Extract phones and emails
        phones = []
        emails = []
        if result.get("PHONE"):
            phones = [p.get("VALUE", "") for p in result["PHONE"]]
        if result.get("EMAIL"):
            emails = [e.get("VALUE", "") for e in result["EMAIL"]]

        return Contact(
            id=result.get("ID", 0),
            name=f"{result.get('NAME', '')} {result.get('LAST_NAME', '')}".strip(),
            first_name=result.get("NAME", ""),
            last_name=result.get("LAST_NAME", ""),
            type=result.get("TYPE_ID", ""),
            phone=phones if phones else None,
            email=emails if emails else None,
            created_by=int(result.get("CREATED_BY_ID", 0)),
            date_create=result.get("DATE_CREATE", ""),
            date_modify=result.get("DATE_MODIFY", "")
        )

    async def update_contact(
        self,
        contact_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        assigned_by_id: Optional[int] = None
    ) -> bool:
        """
        Update a contact.

        Args:
            contact_id: Contact ID
            first_name: New first name
            last_name: New last name
            phone: New phone number
            email: New email address
            assigned_by_id: New assigned user ID

        Returns:
            True if updated successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {}

        if first_name:
            fields["NAME"] = first_name
        if last_name:
            fields["LAST_NAME"] = last_name
        if phone:
            fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
        if email:
            fields["EMAIL"] = [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        if assigned_by_id:
            fields["ASSIGNED_BY_ID"] = assigned_by_id

        await self._request("crm.contact.update", {"id": contact_id, "fields": fields})
        return True

    async def delete_contact(self, contact_id: int) -> bool:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("crm.contact.delete", {"id": contact_id})
        return True

    async def search_contacts(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        limit: int = 50
    ) -> List[Contact]:
        """
        Search for contacts.

        Args:
            filter_params: Filter conditions
            select: Fields to return
            order: Sort order
            limit: Maximum number of contacts to return

        Returns:
            List of Contact objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {}

        if filter_params:
            params["filter"] = filter_params
        if select:
            params["select"] = select
        if order:
            params["order"] = order

        result = await self._request("crm.contact.list", params)

        contacts = result if isinstance(result, list) else []
        return [
            Contact(
                id=contact.get("ID", 0),
                name=f"{contact.get('NAME', '')} {contact.get('LAST_NAME', '')}".strip(),
                first_name=contact.get("NAME", ""),
                last_name=contact.get("LAST_NAME", ""),
                type=contact.get("TYPE_ID", ""),
                phone=[p.get("VALUE", "") for p in contact.get("PHONE", [])] if contact.get("PHONE") else None,
                email=[e.get("VALUE", "") for e in contact.get("EMAIL", [])] if contact.get("EMAIL") else None,
                created_by=int(contact.get("CREATED_BY_ID", 0)),
                date_create=contact.get("DATE_CREATE", ""),
                date_modify=contact.get("DATE_MODIFY", "")
            )
            for contact in contacts[:limit]
        ]

    # ==================== Products ====================

    async def create_product_item(
        self,
        name: str,
        price: float,
        currency: str = "USD",
        code: Optional[str] = None,
        xml_id: Optional[str] = None,
        description: Optional[str] = None
    ) -> ProductItem:
        """
        Create a new product item.

        Args:
            name: Product name
            price: Product price
            currency: Currency code (default: USD)
            code: Product code
            xml_id: XML ID for integration
            description: Product description

        Returns:
            ProductItem object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {
            "NAME": name,
            "PRICE": price,
            "CURRENCY_ID": currency
        }

        if code:
            fields["CODE"] = code
        if xml_id:
            fields["XML_ID"] = xml_id
        if description:
            fields["DESCRIPTION"] = description

        result = await self._request("crm.product.add", {"fields": fields})

        return await self.get_product_item(result)

    async def get_product_item(self, product_id: int) -> ProductItem:
        """
        Get a product item by ID.

        Args:
            product_id: Product ID

        Returns:
            ProductItem object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        result = await self._request("crm.product.get", {"id": product_id})

        return ProductItem(
            id=result.get("ID", 0),
            name=result.get("NAME", ""),
            code=result.get("CODE"),
            price=float(result.get("PRICE", 0)),
            currency=result.get("CURRENCY_ID", "USD"),
            xml_id=result.get("XML_ID"),
            created_by=int(result.get("CREATED_BY_ID", 0)),
            date_create=result.get("DATE_CREATE", ""),
            date_modify=result.get("DATE_MODIFY", "")
        )

    async def update_product_item(
        self,
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        code: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """
        Update a product item.

        Args:
            product_id: Product ID
            name: New product name
            price: New product price
            code: New product code
            description: New description

        Returns:
            True if updated successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        fields = {}

        if name:
            fields["NAME"] = name
        if price is not None:
            fields["PRICE"] = price
        if code:
            fields["CODE"] = code
        if description:
            fields["DESCRIPTION"] = description

        await self._request("crm.product.update", {"id": product_id, "fields": fields})
        return True

    async def delete_product_item(self, product_id: int) -> bool:
        """
        Delete a product item.

        Args:
            product_id: Product ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("crm.product.delete", {"id": product_id})
        return True

    async def search_product_items(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        limit: int = 50
    ) -> List[ProductItem]:
        """
        Search for product items.

        Args:
            filter_params: Filter conditions
            select: Fields to return
            order: Sort order
            limit: Maximum number of products to return

        Returns:
            List of ProductItem objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {}

        if filter_params:
            params["filter"] = filter_params
        if select:
            params["select"] = select
        if order:
            params["order"] = order

        result = await self._request("crm.product.list", params)

        products = result if isinstance(result, list) else []
        return [
            ProductItem(
                id=product.get("ID", 0),
                name=product.get("NAME", ""),
                code=product.get("CODE"),
                price=float(product.get("PRICE", 0)),
                currency=product.get("CURRENCY_ID", "USD"),
                xml_id=product.get("XML_ID"),
                created_by=int(product.get("CREATED_BY_ID", 0)),
                date_create=product.get("DATE_CREATE", ""),
                date_modify=product.get("DATE_MODIFY", "")
            )
            for product in products[:limit]
        ]


# ==================== Webhook Support ====================

class BitrixWebhookHandler:
    """
    Bitrix webhook handler for processing incoming events.

    Supported webhook events:
    - New Lead
    - Updated Lead
    - New Deal
    - Updated Deal
    - New Contact
    - Updated Contact
    - New Task
    """

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate webhook payload.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed event data with event_type and data
        """
        event_type = payload.get("event", payload.get("event_type", ""))
        entity_type = payload.get("entity", "")

        return {
            "event_type": event_type,
            "entity_type": entity_type,
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            "data": payload.get("data", {})
        }

    @staticmethod
    def handle_new_lead(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new lead event"""
        return {
            "lead_id": payload.get("ID"),
            "title": payload.get("TITLE"),
            "name": payload.get("NAME"),
            "status_id": payload.get("STATUS_ID"),
            "opportunity": payload.get("OPPORTUNITY"),
            "timestamp": payload.get("DATE_CREATE")
        }

    @staticmethod
    def handle_new_deal(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new deal event"""
        return {
            "deal_id": payload.get("ID"),
            "title": payload.get("TITLE"),
            "stage_id": payload.get("STAGE_ID"),
            "opportunity": payload.get("OPPORTUNITY"),
            "contact_id": payload.get("CONTACT_ID"),
            "timestamp": payload.get("DATE_CREATE")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Bitrix API client"""

    # Example configuration
    domain = "mycompany.bitrix24.com"
    user_id = "your_user_id"
    access_token = "your_access_token"

    async with BitrixAPIClient(domain, user_id, access_token) as client:
        # Create a lead
        lead = await client.create_lead(
            title="New Sales Lead",
            name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            opportunity=10000.0
        )
        print(f"Created lead: {lead.id}")

        # Search leads
        leads = await client.search_leads(limit=10)
        print(f"Found {len(leads)} leads")

        # Create a deal
        deal = await client.create_deal(
            title="Website Development",
            stage_id="NEW",
            opportunity=50000.0,
            contact_id=lead.id
        )
        print(f"Created deal: {deal.id}")

        # Create a contact
        contact = await client.create_contact(
            name="Jane Smith",
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com"
        )
        print(f"Created contact: {contact.id}")

        # Create a product
        product = await client.create_product_item(
            name="Premium Service",
            price=299.99,
            currency="USD"
        )
        print(f"Created product: {product.id}")


if __name__ == "__main__":
    asyncio.run(main())