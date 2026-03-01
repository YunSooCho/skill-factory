"""
HIF API - Credit Scoring Client

Supports 3 API Actions:
- Get Screening Details (審査の詳細を取得)
- Request Screening (審査を依頼)
- Get Company Score (企業スコアを取得)

Triggers:
- None
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScreeningRequest:
    """Screening request entity"""
    id: str
    company_name: str
    company_number: Optional[str] = None
    status: Optional[str] = None
    created_at: str = ""


@dataclass
class ScreeningDetail:
    """Screening detail entity"""
    request_id: str
    score: int
    risk_level: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    created_at: str = ""


@dataclass
class CompanyScore:
    """Company score entity"""
    company_number: str
    score: int
    rank: Optional[str] = None
    industry: Optional[str] = None
    updated_at: str = ""


class HIFClientError(Exception):
    """Base exception for HIF client errors"""
    pass


class HIFRateLimitError(HIFClientError):
    """Raised when rate limit is exceeded"""
    pass


class HIFClient:
    """
    HIF API client for credit scoring and screening.

    API Documentation: contact HIF for API documentation
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.hif.jp/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize HIF client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("hif")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self._logger = logger

    async def __aenter__(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting."""
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                self._logger.debug(f"Request: {method} {url}")
                if data:
                    self._logger.debug(f"Data: {data}")

                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    await self._update_rate_limit(response)

                    if response.status in [200, 201]:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise HIFClientError("Authentication failed")

                    elif response.status == 403:
                        raise HIFClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise HIFClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise HIFClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise HIFClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise HIFClientError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

    async def _check_rate_limit(self):
        """Check if rate limit allows request"""
        if self._rate_limit_remaining <= 1:
            now = int(datetime.now().timestamp())
            if now < self._rate_limit_reset:
                wait_time = self._rate_limit_reset - now
                self._logger.warning(f"Rate limit reached, waiting {wait_time}s")
                await asyncio.sleep(wait_time)

    async def _update_rate_limit(self, response: aiohttp.ClientResponse):
        """Update rate limit info from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def request_screening(
        self,
        company_name: str,
        company_number: Optional[str] = None
    ) -> ScreeningRequest:
        """
        Request credit screening for a company.

        Args:
            company_name: Name of the company to screen
            company_number: Company registration number (optional)

        Returns:
            Screening request object with request ID

        Raises:
            HIFClientError: On API errors
        """
        data = {"company_name": company_name}
        if company_number:
            data["company_number"] = company_number

        self._logger.info(f"Requesting screening for company: {company_name}")
        result = await self._request("POST", "/screenings", data=data)

        return ScreeningRequest(
            id=str(result.get("id", "")),
            company_name=company_name,
            company_number=company_number,
            status=result.get("status"),
            created_at=result.get("created_at", "")
        )

    async def get_screening_details(
        self,
        request_id: str
    ) -> ScreeningDetail:
        """
        Get detailed screening results.

        Args:
            request_id: ID of the screening request

        Returns:
            Screening detail object with score and risk information

        Raises:
            HIFClientError: On API errors
        """
        self._logger.info(f"Getting screening details for request {request_id}")
        result = await self._request("GET", f"/screenings/{request_id}")

        return ScreeningDetail(
            request_id=request_id,
            score=result.get("score", 0),
            risk_level=result.get("risk_level"),
            details=result.get("details"),
            created_at=result.get("created_at", "")
        )

    async def get_company_score(
        self,
        company_number: str
    ) -> CompanyScore:
        """
        Get credit score for a company.

        Args:
            company_number: Company registration number

        Returns:
            Company score object with credit score and ranking

        Raises:
            HIFClientError: On API errors
        """
        self._logger.info(f"Getting score for company {company_number}")
        result = await self._request("GET", f"/companies/{company_number}/score".format(company_number=company_number))

        return CompanyScore(
            company_number=company_number,
            score=result.get("score", 0),
            rank=result.get("rank"),
            industry=result.get("industry"),
            updated_at=result.get("updated_at", "")
        )