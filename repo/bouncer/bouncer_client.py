"""
Bouncer API Client

Supports:
- Verify Email Address
- Verify Domain
"""

import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class EmailStatus(Enum):
    """Email verification status"""
    DELIVERABLE = "deliverable"
    UNDELIVERABLE = "undeliverable"
    RISKY = "risky"
    UNKNOWN = "unknown"


class DomainStatus(Enum):
    """Domain verification status"""
    VALID = "valid"
    INVALID = "invalid"
    RISKY = "risky"
    UNKNOWN = "unknown"


@dataclass
class EmailVerificationResult:
    """Email verification result"""
    email: Optional[str] = None
    status: Optional[EmailStatus] = None
    reason: Optional[str] = None
    is_disposable: bool = False
    is_role_account: bool = False
    is_free_provider: bool = False
    domain_status: Optional[DomainStatus] = None
    score: float = 0.0


@dataclass
class DomainVerificationResult:
    """Domain verification result"""
    domain: Optional[str] = None
    status: Optional[DomainStatus] = None
    mx_records: bool = True
    spf_record: Optional[str] = None
    dmarc_record: Optional[str] = None
    is_valid: bool = True


class BouncerClient:
    """
    Bouncer API client for email and domain verification.

    Authentication: API Key (Header: x-api-key)
    Base URL: https://api.usebouncer.com/v1
    """

    BASE_URL = "https://api.usebouncer.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Bouncer client.

        Args:
            api_key: Bouncer API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Verification Operations ====================

    def verify_email(self, email: str) -> EmailVerificationResult:
        """
        Verify an email address.

        Args:
            email: Email address to verify

        Returns:
            EmailVerificationResult with verification details
        """
        if not email:
            raise ValueError("Email address is required")

        result = self._request("GET", "/email", params={"email": email})
        return self._parse_email_verification(result)

    def verify_domain(self, domain: str) -> DomainVerificationResult:
        """
        Verify a domain.

        Args:
            domain: Domain name to verify

        Returns:
            DomainVerificationResult with domain details
        """
        if not domain:
            raise ValueError("Domain is required")

        result = self._request("GET", "/domain", params={"domain": domain})
        return self._parse_domain_verification(result)

    # ==================== Helper Methods ====================

    def _parse_email_verification(self, data: Dict[str, Any]) -> EmailVerificationResult:
        """Parse email verification result"""
        status_str = data.get("status", "unknown").lower()
        try:
            status = EmailStatus(status_str)
        except ValueError:
            status = EmailStatus.UNKNOWN

        domain_status_str = data.get("domain_status", "").lower()
        domain_status = None
        if domain_status_str:
            try:
                domain_status = DomainStatus(domain_status_str)
            except ValueError:
                pass

        return EmailVerificationResult(
            email=data.get("email"),
            status=status,
            reason=data.get("reason"),
            is_disposable=data.get("is_disposable", False),
            is_role_account=data.get("is_role_account", False),
            is_free_provider=data.get("is_free_provider", False),
            domain_status=domain_status,
            score=data.get("score", 0.0)
        )

    def _parse_domain_verification(self, data: Dict[str, Any]) -> DomainVerificationResult:
        """Parse domain verification result"""
        status_str = data.get("status", "unknown").lower()
        try:
            status = DomainStatus(status_str)
        except ValueError:
            status = DomainStatus.UNKNOWN

        return DomainVerificationResult(
            domain=data.get("domain"),
            status=status,
            mx_records=data.get("mx_records", True),
            spf_record=data.get("spf_record"),
            dmarc_record=data.get("dmarc_record"),
            is_valid=data.get("is_valid", True)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_bouncer_api_key"

    client = BouncerClient(api_key=api_key)

    try:
        # Verify an email
        email_result = client.verify_email("user@example.com")
        print(f"Email: {email_result.email}")
        print(f"Status: {email_result.status.value}")
        print(f"Reason: {email_result.reason}")
        print(f"Disposable: {email_result.is_disposable}")
        print(f"Score: {email_result.score}")

        # Verify a domain
        domain_result = client.verify_domain("example.com")
        print(f"\\nDomain: {domain_result.domain}")
        print(f"Status: {domain_result.status.value}")
        print(f"MX Records: {domain_result.mx_records}")
        print(f"SPF Record: {domain_result.spf_record}")
        print(f"DMARC Record: {domain_result.dmarc_record}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()