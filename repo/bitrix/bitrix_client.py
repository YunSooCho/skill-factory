"""
Bitrix API Client

CRM and business platform for managing:
- Leads
- Deals
- Contacts
- Product Items
- Tasks

API Actions (20):
Full CRUD for leads, deals, contacts, product items
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Lead:
    id: Optional[str] = None
    title: Optional[str] = None
    status_id: Optional[str] = None
    status_semantic_id: Optional[str] = None
    opportunity: Optional[float] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    company_title: Optional[str] = None
    created_by: Optional[str] = None
    created_time: Optional[str] = None


@dataclass
class Deal:
    id: Optional[str] = None
    title: Optional[str] = None
    stage_id: Optional[str] = None
    opportunity: Optional[float] = None
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    created_time: Optional[str] = None


@dataclass
class Contact:
    id: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[List[str]] = None
    phone: Optional[List[Dict[str, str]]] = None

    def __post_init__(self):
        if self.email is None:
            self.email = []
        if self.phone is None:
            self.phone = []


@dataclass
class ProductItem:
    id: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class RateLimiter:
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        self.tokens = min(self.calls_per_second, self.tokens + elapsed * self.calls_per_second)
        self.last_update = now
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.calls_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = self.calls_per_second
        else:
            self.tokens -= 1


class BitrixError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class BitrixClient:
    """Bitrix API Client"""

    def __init__(self, webhook_url: str):
        """
        Initialize Bitrix client

        Args:
            webhook_url: Full Incoming webhook URL
        """
        self.webhook_url = webhook_url.rstrip('/')
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to Bitrix API"""
        await self._rate_limiter.acquire()
        url = f"{self.webhook_url}/{method}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=params) as response:
                    response_text = await response.text()
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("error_description", error_data.get("error", "Unknown error"))
                        except:
                            error_msg = response_text
                        raise BitrixError(error_msg, response.status)

                    result = await response.json()
                    if "error" in result:
                        raise BitrixError(result.get("error_description", result.get("error")))
                    if "result" in result:
                        return result["result"]
                    return result

            except aiohttp.ClientError as e:
                raise BitrixError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise BitrixError("Request timeout")

    # Lead methods
    async def create_lead(self, fields: Dict[str, Any]) -> Lead:
        """Create lead"""
        if not fields.get("TITLE"):
            raise BitrixError("Lead TITLE is required")
        result = await self._make_request("crm.lead.add", {"fields": fields})
        lead_id = result
        return await self.get_lead(lead_id)

    async def get_lead(self, lead_id: str) -> Lead:
        """Get lead by ID"""
        result = await self._make_request("crm.lead.get", {"id": lead_id})
        return Lead(
            id=result.get("ID"),
            title=result.get("TITLE"),
            status_id=result.get("STATUS_ID"),
            status_semantic_id=result.get("STATUS_SEMANTIC_ID"),
            opportunity=result.get("OPPORTUNITY"),
            name=result.get("NAME"),
            last_name=result.get("LAST_NAME"),
            company_title=result.get("COMPANY_TITLE"),
            created_by=result.get("CREATED_BY"),
            created_time=result.get("DATE_CREATE")
        )

    async def update_lead(self, lead_id: str, fields: Dict[str, Any]) -> Lead:
        """Update lead"""
        await self._make_request("crm.lead.update", {"id": lead_id, "fields": fields})
        return await self.get_lead(lead_id)

    async def delete_lead(self, lead_id: str) -> Dict[str, str]:
        """Delete lead"""
        await self._make_request("crm.lead.delete", {"id": lead_id})
        return {"status": "deleted", "lead_id": lead_id}

    async def search_lead(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Lead]:
        """Search leads"""
        params = filter_params if filter_params else {}
        result = await self._make_request("crm.lead.list", {"filter": params})
        if not result:
            return []
        return [Lead(
            id=item.get("ID"),
            title=item.get("TITLE"),
            status_id=item.get("STATUS_ID"),
            status_semantic_id=item.get("STATUS_SEMANTIC_ID"),
            opportunity=item.get("OPPORTUNITY"),
            name=item.get("NAME"),
            last_name=item.get("LAST_NAME"),
            company_title=item.get("COMPANY_TITLE")
        ) for item in result]

    # Deal methods
    async def create_deal(self, fields: Dict[str, Any]) -> Deal:
        """Create deal"""
        if not fields.get("TITLE"):
            raise BitrixError("Deal TITLE is required")
        result = await self._make_request("crm.deal.add", {"fields": fields})
        deal_id = result
        return await self.get_deal(deal_id)

    async def get_deal(self, deal_id: str) -> Deal:
        """Get deal by ID"""
        result = await self._make_request("crm.deal.get", {"id": deal_id})
        return Deal(
            id=result.get("ID"),
            title=result.get("TITLE"),
            stage_id=result.get("STAGE_ID"),
            opportunity=result.get("OPPORTUNITY"),
            contact_id=result.get("CONTACT_ID"),
            company_id=result.get("COMPANY_ID"),
            created_time=result.get("DATE_CREATE")
        )

    async def update_deal(self, deal_id: str, fields: Dict[str, Any]) -> Deal:
        """Update deal"""
        await self._make_request("crm.deal.update", {"id": deal_id, "fields": fields})
        return await self.get_deal(deal_id)

    async def delete_deal(self, deal_id: str) -> Dict[str, str]:
        """Delete deal"""
        await self._make_request("crm.deal.delete", {"id": deal_id})
        return {"status": "deleted", "deal_id": deal_id}

    async def search_deal(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Deal]:
        """Search deals"""
        params = filter_params if filter_params else {}
        result = await self._make_request("crm.deal.list", {"filter": params})
        if not result:
            return []
        return [Deal(
            id=item.get("ID"),
            title=item.get("TITLE"),
            stage_id=item.get("STAGE_ID"),
            opportunity=item.get("OPPORTUNITY"),
            contact_id=item.get("CONTACT_ID"),
            company_id=item.get("COMPANY_ID")
        ) for item in result]

    # Contact methods
    async def create_contact(self, fields: Dict[str, Any]) -> Contact:
        """Create contact"""
        result = await self._make_request("crm.contact.add", {"fields": fields})
        contact_id = result
        return await self.get_contact(contact_id)

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID"""
        result = await self._make_request("crm.contact.get", {"id": contact_id})
        return Contact(
            id=result.get("ID"),
            name=result.get("NAME"),
            last_name=result.get("LAST_NAME"),
            email=[item.get("VALUE") for item in (result.get("EMAIL") or [])],
            phone=[{"value": item.get("VALUE"), "type": item.get("VALUE_TYPE")} for item in (result.get("PHONE") or [])]
        )

    async def update_contact(self, contact_id: str, fields: Dict[str, Any]) -> Contact:
        """Update contact"""
        await self._make_request("crm.contact.update", {"id": contact_id, "fields": fields})
        return await self.get_contact(contact_id)

    async def delete_contact(self, contact_id: str) -> Dict[str, str]:
        """Delete contact"""
        await self._make_request("crm.contact.delete", {"id": contact_id})
        return {"status": "deleted", "contact_id": contact_id}

    async def search_contact(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Contact]:
        """Search contacts"""
        params = filter_params if filter_params else {}
        result = await self._make_request("crm.contact.list", {"filter": params})
        if not result:
            return []
        return [Contact(
            id=item.get("ID"),
            name=item.get("NAME"),
            last_name=item.get("LAST_NAME"),
            email=[e.get("VALUE") for e in (item.get("EMAIL") or [])]
        ) for item in result]

    # Product Item methods
    async def create_product_item(self, fields: Dict[str, Any]) -> ProductItem:
        """Create product item"""
        result = await self._make_request("crm.product.add", {"fields": fields})
        product_id = result
        return await self.get_product_item(product_id)

    async def get_product_item(self, product_id: str) -> ProductItem:
        """Get product item by ID"""
        result = await self._make_request("crm.product.get", {"id": product_id})
        return ProductItem(
            id=result.get("ID"),
            name=result.get("NAME"),
            price=result.get("PRICE"),
            currency=result.get("CURRENCY")
        )

    async def update_product_item(self, product_id: str, fields: Dict[str, Any]) -> ProductItem:
        """Update product item"""
        await self._make_request("crm.product.update", {"id": product_id, "fields": fields})
        return await self.get_product_item(product_id)

    async def delete_product_item(self, product_id: str) -> Dict[str, str]:
        """Delete product item"""
        await self._make_request("crm.product.delete", {"id": product_id})
        return {"status": "deleted", "product_id": product_id}

    async def search_product_item(self, filter_params: Optional[Dict[str, Any]] = None) -> List[ProductItem]:
        """Search product items"""
        params = filter_params if filter_params else {}
        result = await self._make_request("crm.product.list", {"filter": params})
        if not result:
            return []
        return [ProductItem(
            id=item.get("ID"),
            name=item.get("NAME"),
            price=item.get("PRICE"),
            currency=item.get("CURRENCY")
        ) for item in result]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process webhook event"""
        return {
            "event": webhook_data.get("event", "unknown"),
            "event_entity": webhook_data.get("event_entity", "unknown"),
            "event_entity_id": webhook_data.get("event_entity_id"),
            "data": webhook_data
        }