"""
Riskanalyze API - Risk Analysis Client

Supports:
- Bulk search customers
- Get individual company information
- Bulk search companies
- Search reputation
- Get individual customer information
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class CustomerSearchResult:
    """Customer search result"""
    customer_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    risk_score: float
    risk_level: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class CompanyInfo:
    """Company information"""
    company_id: str
    name: str
    corporate_number: Optional[str]
    address: Optional[str]
    risk_score: float
    risk_level: str
    status: str
    business_type: Optional[str]
    established_date: Optional[str]


@dataclass
class ReputationInfo:
    """Reputation information"""
    entity_id: str
    entity_type: str
    reputation_score: float
    risk_indicators: List[str]
    positive_factors: List[str]
    negative_factors: List[str]
    overall_rating: str
    last_checked: str


@dataclass
class CustomerInfo:
    """Customer information"""
    customer_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    company_id: Optional[str]
    risk_score: float
    risk_level: str
    status: str
    credit_limit: Optional[float]
    payment_history: List[Dict[str, Any]]
    created_at: str
    updated_at: str


class RiskanalyzeClient:
    """
    Riskanalyze API client for risk analysis services.

    API Documentation: https://lp.yoom.fun/apps/riskanalyze
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.riskanalyze.com/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Riskanalyze client.

        Args:
            api_key: API key (defaults to YOOM_RISKANALYZE_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_RISKANALYZE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_RISKANALYZE_API_KEY environment variable")

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

    # ==================== Customer Operations ====================

    async def bulk_search_customers(
        self,
        emails: Optional[List[str]] = None,
        phones: Optional[List[str]] = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Bulk search customers by emails or phones.

        Args:
            emails: List of email addresses to search
            phones: List of phone numbers to search
            batch_size: Number of records per batch (max 100)

        Returns:
            Dictionary with search results and metadata

        Raises:
            ValueError: If neither emails nor phones provided
            Exception: If API request fails
        """
        if not emails and not phones:
            raise ValueError("Either emails or phones must be provided")

        if batch_size > 100:
            batch_size = 100

        payload = {
            "batch_size": batch_size,
            "emails": emails or [],
            "phones": phones or []
        }

        return await self._request("POST", "/customers/bulk-search", json=payload)

    async def get_customer_info(self, customer_id: str) -> CustomerInfo:
        """
        Get individual customer information.

        Args:
            customer_id: Customer ID to look up

        Returns:
            CustomerInfo with customer details

        Raises:
            Exception: If customer not found or API error
        """
        data = await self._request("GET", f"/customers/{customer_id}")

        return CustomerInfo(
            customer_id=data.get("customer_id", customer_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=data.get("company_id"),
            risk_score=data.get("risk_score", 0.0),
            risk_level=data.get("risk_level", "unknown"),
            status=data.get("status", "unknown"),
            credit_limit=data.get("credit_limit"),
            payment_history=data.get("payment_history", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Company Operations ====================

    async def get_company_info(self, company_id: str) -> CompanyInfo:
        """
        Get individual company information.

        Args:
            company_id: Company ID to look up

        Returns:
            CompanyInfo with company details

        Raises:
            Exception: If company not found or API error
        """
        data = await self._request("GET", f"/companies/{company_id}")

        return CompanyInfo(
            company_id=data.get("company_id", company_id),
            name=data.get("name", ""),
            corporate_number=data.get("corporate_number"),
            address=data.get("address"),
            risk_score=data.get("risk_score", 0.0),
            risk_level=data.get("risk_level", "unknown"),
            status=data.get("status", "unknown"),
            business_type=data.get("business_type"),
            established_date=data.get("established_date")
        )

    async def bulk_search_companies(
        self,
        corporate_numbers: Optional[List[str]] = None,
        company_names: Optional[List[str]] = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Bulk search companies by corporate numbers or names.

        Args:
            corporate_numbers: List of corporate registration numbers
            company_names: List of company names
            batch_size: Number of records per batch (max 100)

        Returns:
            Dictionary with search results and metadata

        Raises:
            ValueError: If neither corporate_numbers nor company_names provided
            Exception: If API request fails
        """
        if not corporate_numbers and not company_names:
            raise ValueError("Either corporate_numbers or company_names must be provided")

        if batch_size > 100:
            batch_size = 100

        payload = {
            "batch_size": batch_size,
            "corporate_numbers": corporate_numbers or [],
            "company_names": company_names or []
        }

        return await self._request("POST", "/companies/bulk-search", json=payload)

    # ==================== Reputation Operations ====================

    async def search_reputation(
        self,
        entity_id: str,
        entity_type: str = "customer"
    ) -> ReputationInfo:
        """
        Search reputation for an entity.

        Args:
            entity_id: Entity ID (customer or company ID)
            entity_type: Type of entity ('customer' or 'company')

        Returns:
            ReputationInfo with reputation analysis

        Raises:
            ValueError: If entity_type is invalid
            Exception: If API request fails
        """
        if entity_type not in ["customer", "company"]:
            raise ValueError("entity_type must be 'customer' or 'company'")

        params = {"entity_type": entity_type}
        data = await self._request("GET", f"/reputation/{entity_id}", params=params)

        return ReputationInfo(
            entity_id=data.get("entity_id", entity_id),
            entity_type=data.get("entity_type", entity_type),
            reputation_score=data.get("reputation_score", 0.0),
            risk_indicators=data.get("risk_indicators", []),
            positive_factors=data.get("positive_factors", []),
            negative_factors=data.get("negative_factors", []),
            overall_rating=data.get("overall_rating", "unknown"),
            last_checked=data.get("last_checked", "")
        )

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Args:
            payload: Webhook payload from Riskanalyze

        Returns:
            Acknowledgment response
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        # Process event based on type
        if event_type == "bulk_customer_search_completed":
            # Handle bulk customer search completion
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Bulk customer search completed"
            }
        elif event_type == "bulk_company_search_completed":
            # Handle bulk company search completion
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Bulk company search completed"
            }
        elif event_type == "reputation_search_completed":
            # Handle reputation search completion
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Reputation search completed"
            }
        else:
            return {
                "status": "acknowledged",
                "event_type": event_type,
                "message": "Event received"
            }