"""
Emailable API - Email Verification Service Client

Supports 1 API Action:
- Email address verification

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
    deliverable: bool
    score: float  # 0 to 10
    state: str  # deliverable, undeliverable, risky, unknown
    reason: Optional[str] = None
    free_email: bool = False
    role_email: bool = False
    disposable: bool = False
    accept_all: bool = False
    mailbox_active: bool = False
    domain: Optional[str] = None
    mx_record: bool = False
    smtp_check: bool = False
    processed_at: str = ""


class EmailableClient:
    """
    Emailable API client for email verification.

    API Documentation: https://emailable.com/docs/api
    Uses API Key for authentication.
    """

    BASE_URL = "https://api.emailable.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Emailable client.

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
        email: str,
        smtp_timeout: int = 10,
        hygiene: bool = True
    ) -> EmailVerification:
        """
        Verify a single email address

        Args:
            email: Email address to verify
            smtp_timeout: SMTP connection timeout in seconds (default: 10)
            hygiene: Perform hygiene check (default: True)

        Returns:
            EmailVerification with validation status and details
        """
        async with self.session.get(
            f"{self.BASE_URL}/verify",
            params={
                "apikey": self.api_key,
                "email": email,
                "timeout": smtp_timeout,
                "hygiene": "true" if hygiene else "false"
            }
        ) as response:
            data = await self._handle_response(response)

            return EmailVerification(
                email=data.get("email", email),
                deliverable=data.get("deliverable", "").lower() == "true",
                score=float(data.get("score", 0)),
                state=data.get("state", "unknown"),
                reason=data.get("reason"),
                free_email=data.get("free_email", "").lower() == "true",
                role_email=data.get("role_email", "").lower() == "true",
                disposable=data.get("disposable", "").lower() == "true",
                accept_all=data.get("accept_all", "").lower() == "true",
                mailbox_active=data.get("active_mailbox", "").lower() == "true",
                domain=data.get("domain"),
                mx_record=data.get("mx_record", "").lower() == "true",
                smtp_check=data.get("smtp_check", "").lower() == "true",
                processed_at=data.get("creation_date", "")
            )


# ==================== Example Usage ====================

async def main():
    """Example usage of Emailable client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"

    async with EmailableClient(api_key=api_key) as client:
        # Verify email
        verification = await client.verify_email("test@example.com")
        print(f"Email: {verification.email}")
        print(f"Deliverable: {verification.deliverable}")
        print(f"Score: {verification.score}/10")
        print(f"State: {verification.state}")
        print(f"Free Email: {verification.free_email}")
        print(f"Role Email: {verification.role_email}")
        print(f"Disposable: {verification.disposable}")
        print(f"Accept All: {verification.accept_all}")
        print(f"Mailbox Active: {verification.mailbox_active}")


if __name__ == "__main__":
    asyncio.run(main())