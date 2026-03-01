"""
Roborobo API - Document Analysis Client

Supports:
- PDF article download
- Company check execution
- Check result retrieval
- Transaction decision updates
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class CheckResult:
    """Check result information"""
    check_id: str
    company_id: str
    status: str
    risk_score: Optional[float]
    risk_level: Optional[str]
    decision: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class PDFDownloadURL:
    """PDF download URL information"""
    url: str
    expires_at: str
    file_name: Optional[str]


@dataclass
class TransactionInfo:
    """Transaction information"""
    transaction_id: str
    company_id: str
    status: str
    decision: str
    created_at: str
    updated_at: str


class RoboroboClient:
    """
    Roborobo API client for document analysis and risk checks.

    API Documentation: https://lp.yoom.fun/apps/roborobo
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.roborobo.co/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Roborobo client.

        Args:
            api_key: API key (defaults to YOOM_ROBOROBO_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_ROBOROBO_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_ROBOROBO_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.5  # 500ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== PDF Download Operations ====================

    async def get_pdf_download_url(self, article_id: str) -> PDFDownloadURL:
        """
        Get PDF download URL for an article.

        Args:
            article_id: Article ID to get PDF for

        Returns:
            PDFDownloadURL with download URL and expiry

        Raises:
            ValueError: If article_id is empty
            Exception: If API request fails
        """
        if not article_id:
            raise ValueError("Article ID cannot be empty")

        data = await self._request("GET", f"/articles/{article_id}/pdf-url")

        return PDFDownloadURL(
            url=data.get("url", ""),
            expires_at=data.get("expires_at", ""),
            file_name=data.get("file_name")
        )

    async def download_pdf(self, url: str) -> bytes:
        """
        Download PDF file from URL.

        Args:
            url: Download URL

        Returns:
            PDF content as bytes

        Raises:
            Exception: If download fails
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    # ==================== Company Check Operations ====================

    async def execute_company_check(self, company_data: Dict[str, Any]) -> CheckResult:
        """
        Execute company registration check.

        Args:
            company_data: Company information for check

        Returns:
            CheckResult with check information

        Raises:
            ValueError: If required fields missing
            Exception: If API request fails
        """
        if not company_data.get("company_name"):
            raise ValueError("Company name is required")

        data = await self._request("POST", "/checks", json=company_data)

        return CheckResult(
            check_id=data.get("check_id", ""),
            company_id=data.get("company_id", ""),
            status=data.get("status", "pending"),
            risk_score=data.get("risk_score"),
            risk_level=data.get("risk_level"),
            decision=data.get("decision"),
            notes=data.get("notes"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    # ==================== Check Result Operations ====================

    async def get_check_result(self, check_id: str) -> CheckResult:
        """
        Get check result by ID.

        Args:
            check_id: Check ID

        Returns:
            CheckResult with check details

        Raises:
            ValueError: If check_id is empty
            Exception: If API request fails
        """
        if not check_id:
            raise ValueError("Check ID cannot be empty")

        data = await self._request("GET", f"/checks/{check_id}")

        return CheckResult(
            check_id=data.get("check_id", check_id),
            company_id=data.get("company_id", ""),
            status=data.get("status", "pending"),
            risk_score=data.get("risk_score"),
            risk_level=data.get("risk_level"),
            decision=data.get("decision"),
            notes=data.get("notes"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def poll_check_result(
        self,
        check_id: str,
        max_attempts: int = 20,
        poll_interval: int = 5
    ) -> CheckResult:
        """
        Poll for check result until completion.

        Args:
            check_id: Check ID
            max_attempts: Maximum number of poll attempts
            poll_interval: Seconds between polls

        Returns:
            CheckResult when check is complete

        Raises:
            Exception: If polling times out or fails
        """
        for attempt in range(max_attempts):
            result = await self.get_check_result(check_id)

            if result.status in ["completed", "failed"]:
                return result

            await asyncio.sleep(poll_interval)

        raise Exception(f"Check completion polling timed out after {max_attempts} attempts")

    # ==================== Transaction Decision Operations ====================

    async def update_transaction_decision(
        self,
        check_id: str,
        decision: str,
        notes: Optional[str] = None
    ) -> CheckResult:
        """
        Update transaction/transfer decision.

        Args:
            check_id: Check ID
            decision: Decision ('approve', 'reject', 'review')
            notes: Optional notes explaining the decision

        Returns:
            Updated CheckResult

        Raises:
            ValueError: If decision is invalid
            Exception: If API request fails
        """
        if decision not in ["approve", "reject", "review"]:
            raise ValueError("Decision must be 'approve', 'reject', or 'review'")

        update_data = {"decision": decision}
        if notes:
            update_data["notes"] = notes

        data = await self._request("PUT", f"/checks/{check_id}/decision", json=update_data)

        return CheckResult(
            check_id=data.get("check_id", check_id),
            company_id=data.get("company_id", ""),
            status=data.get("status", ""),
            risk_score=data.get("risk_score"),
            risk_level=data.get("risk_level"),
            decision=data.get("decision", decision),
            notes=data.get("notes", notes),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Args:
            payload: Webhook payload

        Returns:
            Acknowledgment response
        """
        event_type = payload.get("event_type")

        if event_type == "check_completed":
            # Process check completion
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Check completed"
            }
        else:
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Event received"
            }