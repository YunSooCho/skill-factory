"""
Clearout Email Validator & Finder API Client

Supports:
- Check Email Address for Business Account
- Instant Email Finder
- Check Email Address for Catch All
- Check Progress Status of Bulk Customer List
- Check Email Address for Free Account
- Check Progress Status of Bulk Email Finder
- Bulk Customer List
- Check Email Address for Disposable Email
- Bulk Email Finder
- Check Email Address for Role Account
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json


@dataclass
class EmailValidationResult:
    """Email validation result"""
    email: str
    is_valid: bool
    status: str
    result: str
    reason: Optional[str]
    score: Optional[float]
    is_disposable: bool
    is_free: bool
    is_role_account: bool
    is_catch_all: bool
    domain: Optional[str]
    mx_records: Optional[List[str]]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmailFindResult:
    """Email finder result"""
    email: Optional[str]
    confidence_score: float
    first_name: Optional[str]
    last_name: Optional[str]
    domain: Optional[str]
    domain_status: str
    verification_status: str
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class BulkJobStatus:
    """Bulk job status"""
    job_id: str
    status: str
    total_emails: int
    processed: int
    valid: int
    invalid: int
    risk_stats: Optional[Dict[str, int]]
    created_at: Optional[str]
    completed_at: Optional[str]
    raw_response: Optional[Dict[str, Any]] = None


class ClearoutClient:
    """
    Clearout Email Validator & Finder client.

    API Documentation: https://apidocs.clearout.io/
    This service provides email validation, finding, and bulk processing.
    """

    BASE_URL = "https://api.clearout.io/v2"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Clearout client.

        Args:
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "User-Agent": "ClearoutClient/1.0",
            "Accept": "application/json"
        }

    # ==================== Email Validation ====================

    async def validate_email(self, email: str) -> EmailValidationResult:
        """
        Validate a single email address.

        Args:
            email: Email address to validate

        Returns:
            EmailValidationResult: Validation result with detailed information

        Raises:
            ValueError: If email is empty or invalid
            aiohttp.ClientError: If API request fails
        """
        if not email or not email.strip():
            raise ValueError("Email address is required")

        url = f"{self.BASE_URL}/email_validator/instant"
        params = {
            "api_token": self.api_key,
            "email": email.strip()
        }

        try:
            async with self.session.get(
                url,
                params=params,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_validation_response(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            elif e.status == 403:
                raise ValueError("API key does not have access to this resource")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def check_email_for_business_account(self, email: str) -> bool:
        """
        Check if email is from a business account (not free email service).

        Args:
            email: Email address to check

        Returns:
            bool: True if it's a business account email
        """
        result = await self.validate_email(email)
        return not result.is_free

    async def check_email_for_free_account(self, email: str) -> bool:
        """
        Check if email is from a free email service (Gmail, Yahoo, etc.).

        Args:
            email: Email address to check

        Returns:
            bool: True if it's a free account email
        """
        result = await self.validate_email(email)
        return result.is_free

    async def check_email_for_role_account(self, email: str) -> bool:
        """
        Check if email is a role account (admin, support, info, etc.).

        Args:
            email: Email address to check

        Returns:
            bool: True if it's a role account
        """
        result = await self.validate_email(email)
        return result.is_role_account

    async def check_email_for_disposable_email(self, email: str) -> bool:
        """
        Check if email is from a disposable email service.

        Args:
            email: Email address to check

        Returns:
            bool: True if it's a disposable email
        """
        result = await self.validate_email(email)
        return result.is_disposable

    async def check_email_for_catch_all(self, email: str) -> bool:
        """
        Check if email domain has catch-all enabled.

        Args:
            email: Email address to check

        Returns:
            bool: True if domain has catch-all enabled
        """
        result = await self.validate_email(email)
        return result.is_catch_all

    # ==================== Email Finder ====================

    async def find_email(
        self,
        *,
        first_name: str,
        last_name: str,
        domain: str
    ) -> EmailFindResult:
        """
        Find email address from first name, last name, and domain.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            domain: Company domain (e.g., "company.com")

        Returns:
            EmailFindResult: Email finder result with confidence score

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not all([first_name, last_name, domain]):
            raise ValueError("first_name, last_name, and domain are required")

        url = f"{self.BASE_URL}/email_finder/instant"
        params = {
            "api_token": self.api_key,
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "domain": domain.strip()
        }

        try:
            async with self.session.get(
                url,
                params=params,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_find_result(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def instant_email_finder(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> EmailFindResult:
        """
        Instant email finder - alias for find_email.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            domain: Company domain

        Returns:
            EmailFindResult: Email finder result
        """
        return await self.find_email(
            first_name=first_name,
            last_name=last_name,
            domain=domain
        )

    # ==================== Bulk Processing ====================

    async def bulk_customer_list(
        self,
        emails: List[str],
        name: Optional[str] = None
    ) -> BulkJobStatus:
        """
        Upload a list of emails for bulk validation.

        Args:
            emails: List of email addresses to validate
            name: Optional name for this batch job

        Returns:
            BulkJobStatus: Job status with job_id

        Raises:
            ValueError: If emails list is empty
        """
        if not emails:
            raise ValueError("Emails list is required")

        url = f"{self.BASE_URL}/email_validator/bulk"
        data = {
            "api_token": self.api_key,
            "data": "\n".join(emails)
        }
        if name:
            data["name"] = name

        try:
            async with self.session.post(
                url,
                data=data,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                result_data = await response.json()

                return self._parse_bulk_status(result_data)

        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def bulk_email_finder(
        self,
        contacts: List[Dict[str, str]],
        name: Optional[str] = None
    ) -> BulkJobStatus:
        """
        Bulk find emails from list of contacts.

        Args:
            contacts: List of dicts with 'first_name', 'last_name', 'domain'
            name: Optional name for this batch job

        Returns:
            BulkJobStatus: Job status with job_id
        """
        if not contacts:
            raise ValueError("Contacts list is required")

        url = f"{self.BASE_URL}/email_finder/bulk"
        data = {
            "api_token": self.api_key,
            "data": json.dumps(contacts)
        }
        if name:
            data["name"] = name

        try:
            async with self.session.post(
                url,
                data=data,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                result_data = await response.json()

                return self._parse_bulk_status(result_data)

        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def check_bulk_status(self, job_id: str) -> BulkJobStatus:
        """
        Check progress status of a bulk job.

        Args:
            job_id: The ID of the bulk job

        Returns:
            BulkJobStatus: Current job status
        """
        url = f"{self.BASE_URL}/bulk/status/{job_id}"
        params = {"api_token": self.api_key}

        try:
            async with self.session.get(
                url,
                params=params,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                result_data = await response.json()

                return self._parse_bulk_status(result_data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Job ID {job_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def check_progress_status_bulk_customer_list(self, job_id: str) -> BulkJobStatus:
        """Alias for check_bulk_status."""
        return await self.check_bulk_status(job_id)

    async def check_progress_status_bulk_email_finder(self, job_id: str) -> BulkJobStatus:
        """Alias for check_bulk_status."""
        return await self.check_bulk_status(job_id)

    # ==================== Helpers ====================

    def _parse_validation_response(self, data: Dict[str, Any]) -> EmailValidationResult:
        """Parse validation response"""
        data_dict = data.get("data", {})

        return EmailValidationResult(
            email=data_dict.get("email", ""),
            is_valid=data_dict.get("status") == "valid",
            status=data_dict.get("status", "unknown"),
            result=data_dict.get("result", ""),
            reason=data_dict.get("reason"),
            score=data_dict.get("score"),
            is_disposable=data_dict.get("is_disposable", False),
            is_free=data_dict.get("is_free", False),
            is_role_account=data_dict.get("is_role_account", False),
            is_catch_all=data_dict.get("catch_all", False),
            domain=data_dict.get("domain"),
            mx_records=data_dict.get("mx_records"),
            raw_response=data
        )

    def _parse_find_result(self, data: Dict[str, Any]) -> EmailFindResult:
        """Parse email finder result"""
        data_dict = data.get("data", {})

        return EmailFindResult(
            email=data_dict.get("email"),
            confidence_score=data_dict.get("confidence", 0),
            first_name=data_dict.get("first_name"),
            last_name=data_dict.get("last_name"),
            domain=data_dict.get("domain"),
            domain_status=data_dict.get("domain_status"),
            verification_status=data_dict.get("verification_status"),
            raw_response=data
        )

    def _parse_bulk_status(self, data: Dict[str, Any]) -> BulkJobStatus:
        """Parse bulk job status"""
        data_dict = data.get("data", {})

        return BulkJobStatus(
            job_id=data_dict.get("job_id", ""),
            status=data_dict.get("status", "unknown"),
            total_emails=data_dict.get("total_count", 0),
            processed=data_dict.get("processed_count", 0),
            valid=data_dict.get("valid_count", 0),
            invalid=data_dict.get("invalid_count", 0),
            risk_stats=data_dict.get("risk_stats"),
            created_at=data_dict.get("created_at"),
            completed_at=data_dict.get("completed_at"),
            raw_response=data
        )


# Convenience functions
async def validate_email_simple(api_key: str, email: str) -> bool:
    """Simple email validation - returns True/False"""
    async with ClearoutClient(api_key=api_key) as client:
        result = await client.validate_email(email)
        return result.is_valid