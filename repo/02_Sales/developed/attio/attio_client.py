"""
Attio API Client

Modern CRM platform for managing:
- Records (companies, people, deals)
- Lists
- Entries
- Notes
- Comments
- Tasks

API Actions (13):
1. Create Note
2. Create Comment
3. Search Entry
4. Get List Entry
5. Create Entry
6. Search Record
7. Update Record
8. Get Record
9. Delete Record
10. Delete List Entry
11. Update List Entry
12. Create Record
13. Create Task

Triggers (13):
- Updated Note
- Deleted Record
- Deleted Entry
- Resolved Comment
- New Record
- New Comment
- Unresolved Comment
- Updated Record
- New Note
- Updated Entry
- New Entry
- New Task
- Updated Task

Authentication: Bearer Token
Base URL: https://api.attio.com/v1
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Record:
    """Record model"""
    id: Optional[str] = None
    object_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ListEntry:
    """List entry model"""
    id: Optional[str] = None
    list_id: Optional[str] = None
    record_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


@dataclass
class Note:
    """Note model"""
    id: Optional[str] = None
    record_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Comment:
    """Comment model"""
    id: Optional[str] = None
    parent_id: Optional[str] = None
    record_id: Optional[str] = None
    content: Optional[str] = None
    is_resolved: Optional[bool] = None


@dataclass
class Task:
    """Task model"""
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None


class RateLimiter:
    """Simple rate limiter"""
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


class AttioError(Exception):
    """Base exception for Attio errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class AttioClient:
    """Attio API Client"""

    def __init__(self, bearer_token: str, base_url: str = "https://api.attio.com/v1"):
        self.bearer_token = bearer_token
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to Attio API"""
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=method, url=url, headers=self._headers, json=data, params=params) as response:
                    response_text = await response.text()

                    if response.status == 204:
                        return {"status": "success"}

                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
                        except:
                            error_msg = response_text if response_text else "HTTP error"
                        raise AttioError(error_msg, response.status)

                    return await response.json()

            except aiohttp.ClientError as e:
                raise AttioError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise AttioError("Request timeout")

    async def create_record(self, object_type: str, data: Dict[str, Any]) -> Record:
        """Create a new record"""
        response = await self._make_request("POST", f"/objects/{object_type}/records", data={"data": data})
        return Record(**response.get("record", {}))

    async def get_record(self, object_type: str, record_id: str) -> Record:
        """Get record by ID"""
        response = await self._make_request("GET", f"/objects/{object_type}/records/{record_id}")
        return Record(id=record_id, object_type=object_type, data=response.get("data", {}))

    async def update_record(self, object_type: str, record_id: str, data: Dict[str, Any]) -> Record:
        """Update record"""
        response = await self._make_request("PATCH", f"/objects/{object_type}/records/{record_id}", data={"data": data})
        return Record(id=record_id, object_type=object_type, data=response.get("data", {}))

    async def delete_record(self, object_type: str, record_id: str) -> Dict[str, str]:
        """Delete record"""
        await self._make_request("DELETE", f"/objects/{object_type}/records/{record_id}")
        return {"status": "deleted", "record_id": record_id}

    async def search_record(self, object_type: str, **params) -> List[Record]:
        """Search records"""
        response = await self._make_request("GET", f"/objects/{object_type}/records", params=params)
        if "data" in response:
            return [Record(id=item.get("id"), object_type=object_type, data=item.get("data", {})) for item in response["data"]]
        return []

    async def create_entry(self, list_id: str, record_id: str, data: Dict[str, Any]) -> ListEntry:
        """Create list entry"""
        payload = {"record_id": record_id, "data": data}
        response = await self._make_request("POST", f"/lists/{list_id}/entries", data=payload)
        return ListEntry(**response.get("entry", {}))

    async def get_list_entry(self, list_id: str, entry_id: str) -> ListEntry:
        """Get list entry by ID"""
        response = await self._make_request("GET", f"/lists/{list_id}/entries/{entry_id}")
        return ListEntry(**response.get("entry", {}))

    async def update_list_entry(self, list_id: str, entry_id: str, data: Dict[str, Any]) -> ListEntry:
        """Update list entry"""
        response = await self._make_request("PATCH", f"/lists/{list_id}/entries/{entry_id}", data={"data": data})
        return ListEntry(**response.get("entry", {}))

    async def delete_list_entry(self, list_id: str, entry_id: str) -> Dict[str, str]:
        """Delete list entry"""
        await self._make_request("DELETE", f"/lists/{list_id}/entries/{entry_id}")
        return {"status": "deleted", "entry_id": entry_id}

    async def search_entry(self, list_id: str, **params) -> List[ListEntry]:
        """Search list entries"""
        response = await self._make_request("GET", f"/lists/{list_id}/entries", params=params)
        if "data" in response:
            return [ListEntry(**item) for item in response["data"]]
        return []

    async def create_note(self, record_id: str, data: Dict[str, Any]) -> Note:
        """Create note for record"""
        payload = {"record_id": record_id, **data}
        response = await self._make_request("POST", "/notes", data=payload)
        return Note(**response.get("note", {}))

    async def create_comment(self, parent_id: str, data: Dict[str, Any]) -> Comment:
        """Create comment"""
        payload = {"parent_id": parent_id, **data}
        response = await self._make_request("POST", "/comments", data=payload)
        return Comment(**response.get("comment", {}))

    async def create_task(self, data: Dict[str, Any]) -> Task:
        """Create task"""
        response = await self._make_request("POST", "/tasks", data=data)
        return Task(**response.get("task", {}))

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process webhook event"""
        event_type = webhook_data.get("event_type", "unknown")
        entity_type = webhook_data.get("entity_type", "unknown")
        entity_id = webhook_data.get("entity_id")

        return {
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": webhook_data
        }