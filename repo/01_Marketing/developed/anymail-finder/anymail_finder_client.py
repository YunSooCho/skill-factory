"""
Anymail Finder - Email Discovery Client

Supports:
- Search for Person's Email
- Search for Company's Email
- Validate Email
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class EmailResult:
    """Email search result"""
    email: str
    confidence: float
    source: str = ""


@dataclass
class EmailValidation:
    """Email validation result"""
    email: str
    is_valid: bool
    is_deliverable: bool
    score: float


class AnymailFinderClient:
    """
    Anymail Finder client for email discovery.
    Uses API key authentication.
    """

    BASE_URL = "https://api.anymailfinder.com"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Email Operations ====================

    async def search_person_email(
        self,
        first_name: str,
        last_name: str,
        company_domain: str
    ) -> Optional[EmailResult]:
        """Search for person's email"""
        async with self.session.get(
            f"{self.BASE_URL}/v1/person",
            params={
                "first_name": first_name,
                "last_name": last_name,
                "company_domain": company_domain
            }
        ) as response:
            data = await response.json()

            if response.status == 200 and data.get("is_reachable"):
                return EmailResult(
                    email=data.get("email", ""),
                    confidence=data.get("score", 0.0),
                    source=data.get("sources", [""])[0] if data.get("sources") else ""
                )
            return None

    async def search_company_email(
        self,
        company_domain: str,
        full_name: Optional[str] = None
    ) -> List[EmailResult]:
        """Search for company emails"""
        params = {"company_domain": company_domain}
        if full_name:
            params["full_name"] = full_name

        async with self.session.get(
            f"{self.BASE_URL}/v1/company",
            params=params
        ) as response:
            data = await response.json()

            results = []
            if isinstance(data, list):
                for email in data:
                    results.append(EmailResult(
                        email=email.get("email", ""),
                        confidence=email.get("score", 0.0),
                        source=email.get("sources", [""])[0] if email.get("sources") else ""
                    ))
            return results

    async def validate_email(self, email: str) -> EmailValidation:
        """Validate an email address"""
        async with self.session.get(
            f"{self.BASE_URL}/v1/validation",
            params={"email": email}
        ) as response:
            data = await response.json()

            return EmailValidation(
                email=email,
                is_valid=data.get("is_reachable", "") == "safe",
                is_deliverable=data.get("validation", {}).get("is_deliverable", False),
                score=data.get("score", data.get("value", 0.0))
            )


async def main():
    async with AnymailFinderClient(api_key="test") as client:
        result = await client.search_person_email(
            "John", "Doe", "example.com"
        )
        if result:
            print(f"Found: {result.email}")

        validation = await client.validate_email("test@example.com")
        print(f"Valid: {validation.is_valid}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())