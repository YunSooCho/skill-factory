"""
Bouncer API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BouncerAPIError(Exception):
    """Base exception for Bouncer API errors"""
    pass


class BouncerAuthError(BouncerAPIError):
    """Authentication error"""
    pass


class BouncerRateLimitError(BouncerAPIError):
    """Rate limit exceeded"""
    pass


class BouncerClient:
    """Bouncer API Client for email verification"""

    BASE_URL = "https://api.usebouncer.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Bouncer client

        Args:
            api_key: Your Bouncer API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json"
        })

    # ===== Email Verification =====

    def verify_email(
        self,
        email: str,
        timeout: Optional[int] = None,
        retry_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Verify a single email address

        Args:
            email: Email address to verify
            timeout: Request timeout in seconds
            retry_count: Number of retries for temporary failures

        Returns:
            Verification result with fields:
            - email: the verified email
            - status: deliverable, undeliverable, risky, or unknown
            - reason: reason for the status
            - domain: domain part of the email
            - is_free: if it's a free email provider
            - is_disposable: if it's a disposable email
            - is_rolebased: if it's a role-based email (admin@, support@, etc.)
            - mailbox_exists: if the mailbox exists
            - mx_record: MX records for the domain
            - creation_date: when the email was created (if available)
        """
        endpoint = f"{self.BASE_URL}/email/verify"
        payload = {"email": email}

        if timeout:
            payload["timeout"] = timeout
        if retry_count:
            payload["retry_count"] = retry_count

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def verify_emails(
        self,
        emails: List[str],
        timeout: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Verify multiple email addresses

        Args:
            emails: List of email addresses
            timeout: Request timeout in seconds

        Returns:
            List of verification results
        """
        endpoint = f"{self.BASE_URL}/email/verify/batch"
        payload = {"emails": emails}

        if timeout:
            payload["timeout"] = timeout

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Domain Verification =====

    def verify_domain(
        self,
        domain: str,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Verify a domain's email infrastructure

        Args:
            domain: Domain to verify (e.g., "example.com")
            timeout: Request timeout in seconds

        Returns:
            Domain verification result with fields:
            - domain: the verified domain
            - status: deliverable, undeliverable, risky, or unknown
            - mx_records: list of MX records
            - mx_valid: if MX records are valid
            - spf_record: SPF record
            - spf_valid: if SPF is valid
            - dmarc_record: DMARC record
            - dmarc_valid: if DMARC is valid
            - dmarc_policy: DMARC policy (none, quarantine, reject)
        """
        endpoint = f"{self.BASE_URL}/domain/verify"
        payload = {"domain": domain}

        if timeout:
            payload["timeout"] = timeout

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Account Management =====

    def get_credits(self) -> Dict[str, Any]:
        """
        Get remaining verification credits

        Returns:
            Account credit information
        """
        endpoint = f"{self.BASE_URL}/account/credits"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information

        Returns:
            Account details including plan, usage, etc.
        """
        endpoint = f"{self.BASE_URL}/account"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Validation Helpers =====

    def is_deliverable(self, email: str, **kwargs) -> bool:
        """
        Check if email is deliverable

        Args:
            email: Email address to check
            **kwargs: Additional arguments for verify_email()

        Returns:
            True if email is deliverable, False otherwise
        """
        result = self.verify_email(email, **kwargs)
        return result.lower().get("status") == "deliverable"

    def is_risky(self, email: str, **kwargs) -> bool:
        """
        Check if email is risky

        Args:
            email: Email address to check
            **kwargs: Additional arguments for verify_email()

        Returns:
            True if email is risky, False otherwise
        """
        result = self.verify_email(email, **kwargs)
        return result.lower().get("status") == "risky"

    def is_undeliverable(self, email: str, **kwargs) -> bool:
        """
        Check if email is undeliverable

        Args:
            email: Email address to check
            **kwargs: Additional arguments for verify_email()

        Returns:
            True if email is undeliverable, False otherwise
        """
        result = self.verify_email(email, **kwargs)
        return result.lower().get("status") == "undeliverable"

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BouncerAuthError("Invalid API key")
        elif error.response.status_code == 429:
            raise BouncerRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BouncerAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 403:
            raise BouncerAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 402:
            raise BouncerAPIError("Insufficient credits")
        else:
            raise BouncerAPIError(f"HTTP {error.response.status_code}: {error.response.text}")