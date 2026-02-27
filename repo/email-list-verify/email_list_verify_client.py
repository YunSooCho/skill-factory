"""
Email List Verify API - Email Validation Service Client

Supports 4 API Actions:
- Email address verification
- Email deliverability evaluation
- Find business email address
- Check disposable email domain

Triggers:
- No triggers supported
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailVerification:
    """Email verification result"""
    email: str
    is_valid: bool
    score: float  # 0.0 to 1.0
    domain: str
    is_disposable: bool = False
    is_free_provider: bool = False
    is_role_email: bool = False
    mx_record: bool = False
    smtp_check: bool = False
    reason: Optional[str] = None


@dataclass
class DeliverabilityResult:
    """Email deliverability evaluation result"""
    email: str
    deliverable: bool
    confidence_score: float
    issues: List[str]
    suggestions: List[str]


@dataclass
class BusinessEmail:
    """Business email search result"""
    email: str
    confidence: float
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    company: Optional[str] = None
    domain: Optional[str] = None


@dataclass
class DisposableCheck:
    """Disposable email domain check result"""
    domain: str
    is_disposable: bool
    provider: Optional[str] = None


class EmailListVerifyClient:
    """
    Email List Verify API client for email validation.

    API Documentation: https://emaillistverify.com/api
    Uses API Key for authentication.
    """

    BASE_URL = "https://apps.emaillistverify.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Email List Verify client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        if response.status in (200, 201, 202):
            data = await response.json()
            return data
        else:
            try:
                data = await response.json()
                error_msg = data.get('error', data.get('message', 'Unknown error'))
            except:
                error_msg = f"HTTP {response.status}"
            raise Exception(f"API Error [{response.status}]: {error_msg}")

    # ==================== Email Verification ====================

    async def verify_email(
        self,
        email: str
    ) -> EmailVerification:
        """
        Verify a single email address

        Args:
            email: Email address to verify

        Returns:
            EmailVerification with validation status and details
        """
        async with self.session.get(
            f"{self.BASE_URL}/verifyEmail",
            params={
                "secret": self.api_key,
                "email": email
            }
        ) as response:
            data = await self._handle_response(response)

            return EmailVerification(
                email=data.get("email", email),
                is_valid=data.get("status", "invalid").lower() == "ok",
                score=float(data.get("score", 0.0)),
                domain=data.get("domain", ""),
                is_disposable=data.get("disposable", "false").lower() == "true",
                is_free_provider=data.get("freemail", "false").lower() == "true",
                is_role_email=data.get("role", "false").lower() == "true",
                mx_record=data.get("mx", "false").lower() == "true",
                smtp_check=data.get("smtp", "false").lower() == "true",
                reason=data.get("reason")
            )

    # ==================== Email Deliverability ====================

    async def evaluate_deliverability(
        self,
        email: str
    ) -> DeliverabilityResult:
        """
        Evaluate email deliverability

        Args:
            email: Email address to evaluate

        Returns:
            DeliverabilityResult with deliverability status and insights
        """
        async with self.session.get(
            f"{self.BASE_URL}/checkEmail",
            params={
                "secret": self.api_key,
                "email": email,
                "full": "true"
            }
        ) as response:
            data = await self._handle_response(response)

            issues = []
            suggestions = []

            # Extract issues from response
            if data.get("disposable") == "true":
                issues.append("Domain is a disposable email provider")
                suggestions.append("Request a business email instead")

            if data.get("freemail") == "true":
                issues.append("Free email provider detected")
                suggestions.append("Consider asking for a business email")

            if data.get("role") == "true":
                issues.append("Role-based email address (e.g., info@, support@)")
                suggestions.append("Request a personal business email")

            if data.get("mx") == "false":
                issues.append("No MX records found for domain")
                suggestions.append("Verify the domain name")

            if data.get("smtp") == "false":
                issues.append("SMTP check failed")
                suggestions.append("Email may not exist or has delivery issues")

            return DeliverabilityResult(
                email=data.get("email", email),
                deliverable=data.get("status", "invalid").lower() == "ok",
                confidence_score=float(data.get("score", 0.0)),
                issues=issues,
                suggestions=suggestions
            )

    # ==================== Business Email Finder ====================

    async def find_business_email(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> List[BusinessEmail]:
        """
        Find business email address for a person

        Args:
            first_name: First name
            last_name: Last name
            domain: Company domain

        Returns:
            List of BusinessEmail candidates with confidence scores
        """
        async with self.session.get(
            f"{self.BASE_URL}/findEmail",
            params={
                "secret": self.api_key,
                "firstName": first_name,
                "lastName": last_name,
                "domain": domain
            }
        ) as response:
            data = await self._handle_response(response)
            results = data.get("results", [])

            return [
                BusinessEmail(
                    email=r.get("email", ""),
                    confidence=float(r.get("confidence", 0.0)),
                    first_name=r.get("firstName"),
                    last_name=r.get("lastName"),
                    full_name=r.get("fullName"),
                    company=r.get("company"),
                    domain=r.get("domain", domain)
                )
                for r in results
            ]

    # ==================== Disposable Email Check ====================

    async def check_disposable_domain(
        self,
        domain: str
    ) -> DisposableCheck:
        """
        Check if email domain is a disposable email provider

        Args:
            domain: Domain to check (with or without @)

        Returns:
            DisposableCheck with domain status
        """
        # Remove @ if present
        domain_clean = domain.lstrip("@")

        async with self.session.get(
            f"{self.BASE_URL}/checkDisposable",
            params={
                "secret": self.api_key,
                "domain": domain_clean
            }
        ) as response:
            data = await self._handle_response(response)

            return DisposableCheck(
                domain=domain_clean,
                is_disposable=data.get("disposable", "false").lower() == "true",
                provider=data.get("provider")
            )


# ==================== Example Usage ====================

async def main():
    """Example usage of Email List Verify client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"

    async with EmailListVerifyClient(api_key=api_key) as client:
        # Verify email
        verification = await client.verify_email("test@example.com")
        print(f"Email: {verification.email}")
        print(f"Valid: {verification.is_valid}")
        print(f"Score: {verification.score}")
        print(f"Disposable: {verification.is_disposable}")

        # Evaluate deliverability
        deliverability = await client.evaluate_deliverability("test@example.com")
        print(f"\nDeliverable: {deliverability.deliverable}")
        print(f"Confidence: {deliverability.confidence_score}")
        if deliverability.issues:
            print("Issues:")
            for issue in deliverability.issues:
                print(f"  - {issue}")

        # Find business email
        business_emails = await client.find_business_email(
            first_name="John",
            last_name="Doe",
            domain="company.com"
        )
        print(f"\nBusiness emails found: {len(business_emails)}")
        for email in business_emails:
            print(f"  {email.email} (confidence: {email.confidence})")

        # Check disposable domain
        disposable = await client.check_disposable_domain("tempmail.com")
        print(f"\nDomain disposable: {disposable.is_disposable}")
        if disposable.provider:
            print(f"Provider: {disposable.provider}")


if __name__ == "__main__":
    asyncio.run(main())