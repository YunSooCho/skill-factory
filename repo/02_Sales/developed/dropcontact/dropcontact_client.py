"""
Dropcontact API Client

Complete client for Dropcontact - email and contact enrichment service.
Supports enrichment job submission and result retrieval.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json


class DropcontactAPIError(Exception):
    """Base exception for Dropcontact API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class DropcontactRateLimitError(DropcontactAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Enrichment:
    enrichment_id: str
    status: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnrichmentResult:
    enrichment_id: str
    status: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    confidence: Optional[float] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class DropcontactClient:
    """Dropcontact API Client for email and contact enrichment."""

    BASE_URL = "https://api.dropcontact.io/v2"

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
                    raise DropcontactRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise DropcontactAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise DropcontactAPIError(f"Network error: {str(e)}")

    async def run_enrichment(self, enrichment_data: Dict[str, Any]) -> Enrichment:
        """
        Run an enrichment job.

        Args:
            enrichment_data: Data to enrich (name, company, domain, etc.)

        Returns:
            Enrichment object with job ID
        """
        data = await self._request("POST", "/enrichment", data=enrichment_data)
        return Enrichment(
            enrichment_id=data.get("enrichment_id", ""),
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["enrichment_id", "status", "created_at"]}
        )

    async def get_result(self, enrichment_id: str) -> EnrichmentResult:
        """
        Get enrichment result.

        Args:
            enrichment_id: Enrichment job ID

        Returns:
            EnrichmentResult with found contact information
        """
        data = await self._request("GET", f"/enrichment/{enrichment_id}/result")
        return EnrichmentResult(
            enrichment_id=data.get("enrichment_id", enrichment_id),
            status=data.get("status", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            linkedin=data.get("linkedin"),
            confidence=data.get("confidence"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["enrichment_id", "status", "email", "phone", "linkedin", "confidence", "created_at"]}
        )

    async def wait_for_result(
        self,
        enrichment_id: str,
        max_wait_seconds: int = 300,
        poll_interval: int = 5
    ) -> EnrichmentResult:
        """
        Poll for enrichment result until complete or timeout.

        Args:
            enrichment_id: Enrichment job ID
            max_wait_seconds: Maximum time to wait for result
            poll_interval: Seconds between polls

        Returns:
            EnrichmentResult with final results

        Raises:
            DropcontactAPIError: If timeout occurs
        """
        import time
        start_time = asyncio.get_event_loop().time()

        while True:
            result = await self.get_result(enrichment_id)

            if result.status in ["completed", "failed", "error"]:
                return result

            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= max_wait_seconds:
                raise DropcontactAPIError(f"Enrichment timeout after {max_wait_seconds} seconds")

            await asyncio.sleep(poll_interval)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with DropcontactClient(api_key="your_api_key") as client:
        enrichment = await client.run_enrichment({
            "name": "John Smith",
            "company": "Acme Corp",
            "domain": "acme.com"
        })
        print(f"Started enrichment: {enrichment.enrichment_id}")

        result = await client.wait_for_result(enrichment.enrichment_id)
        print(f"Result status: {result.status}")
        if result.email:
            print(f"Found email: {result.email}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())