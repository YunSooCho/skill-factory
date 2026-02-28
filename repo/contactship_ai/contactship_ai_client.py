"""
Contactship AI API Client

Complete client for Contactship AI - AI-powered contact management with phone calls.
Supports contacts, AI phone calls, and agents.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


class ContactshipAPIError(Exception):
    """Base exception for Contactship AI API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ContactshipRateLimitError(ContactshipAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Contact:
    contact_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Agent:
    agent_id: str
    name: str
    status: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PhoneCallResult:
    call_id: str
    contact_id: str
    agent_id: str
    status: str
    duration: Optional[int] = None
    transcript: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class ContactshipAIClient:
    """Contactship AI API Client."""

    BASE_URL = "https://api.contactship.ai/v1"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
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
            "Accept": "application/json"
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
                    raise ContactshipRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise ContactshipAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise ContactshipAPIError(f"Network error: {str(e)}")

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        data = await self._request("POST", "/contacts", data=contact_data)
        return Contact(
            contact_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def search_contact(self, query: str, limit: int = 100) -> List[Contact]:
        params = {"query": query, "limit": limit}
        data = await self._request("GET", "/contacts/search", params=params)
        results = data.get("results", [])

        return [Contact(
            contact_id=r.get("id", ""),
            name=r.get("name", ""),
            email=r.get("email"),
            phone=r.get("phone"),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        ) for r in results]

    async def get_contact(self, contact_id: str) -> Contact:
        data = await self._request("GET", f"/contacts/{contact_id}")
        return Contact(
            contact_id=data.get("id", contact_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        data = await self._request("PUT", f"/contacts/{contact_id}", data=update_data)
        return Contact(
            contact_id=contact_id,
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "email", "phone", "created_at", "updated_at"]}
        )

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/contacts/{contact_id}")

    async def list_agents(self, limit: int = 100, offset: int = 0) -> List[Agent]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/agents", params=params)
        results = data.get("results", [])

        return [Agent(
            agent_id=r.get("id", ""),
            name=r.get("name", ""),
            status=r.get("status", ""),
            created_at=r.get("created_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "status", "created_at"]}
        ) for r in results]

    async def ai_phone_call(self, call_data: Dict[str, Any]) -> PhoneCallResult:
        data = await self._request("POST", "/phone-call", data=call_data)
        return PhoneCallResult(
            call_id=data.get("id", ""),
            contact_id=data.get("contact_id", ""),
            agent_id=data.get("agent_id", ""),
            status=data.get("status", ""),
            duration=data.get("duration"),
            transcript=data.get("transcript"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "contact_id", "agent_id", "status", "duration", "transcript", "created_at"]}
        )

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with ContactshipAIClient(api_key="your_api_key") as client:
        contact = await client.create_contact({
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "555-1234"
        })
        print(f"Created contact: {contact.contact_id}")

        result = await client.ai_phone_call({
            "contact_id": contact.contact_id,
            "script": "Business introduction",
            "agent_id": "agent_123"
        })
        print(f"Phone call result: {result.call_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())