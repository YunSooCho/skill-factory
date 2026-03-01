"""
Bettercontact API Client

Contact enrichment platform.

API Actions (2):
1. Get Enrichment Results
2. Enrich Contact

Triggers: None
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EnrichmentResult:
    """Enrichment result model"""
    id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    LinkedIn: Optional[str] = None
    status: Optional[str] = None
    confidence_score: Optional[float] = None
    data: Optional[Dict[str, Any]] = None


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


class BettercontactError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class BettercontactClient:
    """Bettercontact API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.bettercontact.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=method, url=url, headers=self._headers, json=data, params=params) as response:
                    if response.status == 204:
                        return {"status": "success"}
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", "Unknown error")
                        except:
                            error_msg = await response.text()
                        raise BettercontactError(error_msg, response.status)
                    return await response.json()
            except aiohttp.ClientError as e:
                raise BettercontactError(f"Network error: {str(e)}")

    async def enrich_contact(self, data: Dict[str, Any]) -> EnrichmentResult:
        """
        Enrich Contact

        Args:
            data: Contact data to enrich (email, name, company, etc.)

        Returns:
            EnrichmentResult object
        """
        response = await self._make_request("POST", "/enrich", data=data)
        return EnrichmentResult(
            id=response.get("id"),
            email=response.get("email"),
            name=response.get("name"),
            phone=response.get("phone"),
            company=response.get("company"),
            LinkedIn=response.get("linkedin"),
            status=response.get("status"),
            confidence_score=response.get("confidence_score"),
            data=response
        )

    async def get_enrichment_result(self, result_id: str) -> EnrichmentResult:
        """
        Get Enrichment Results

        Args:
            result_id: Enrichment result ID

        Returns:
            EnrichmentResult object
        """
        response = await self._make_request("GET", f"/enrich/{result_id}")
        return EnrichmentResult(
            id=response.get("id"),
            email=response.get("email"),
            name=response.get("name"),
            phone=response.get("phone"),
            company=response.get("company"),
            LinkedIn=response.get("linkedin"),
            status=response.get("status"),
            confidence_score=response.get("confidence_score"),
            data=response
        )