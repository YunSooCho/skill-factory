"""
ZeroBounce API Client
Email validation and verification service
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class EmailValidationResult:
    """Email validation result data model"""
    address: str
    status: str
    sub_status: Optional[str] = None
    free_email: Optional[bool] = None
    did_you_mean: Optional[str] = None
    account: Optional[str] = None
    domain: Optional[str] = None
    safe_to_send: Optional[bool] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    creation_date: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 3000, per_seconds: int = 3600):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class ZeroBounceClient:
    """
    ZeroBounce API client for email validation.

    Rate Limit: 3000 requests per hour (3600 seconds)
    """

    BASE_URL = "https://api.zerobounce.net/v2"

    def __init__(self, api_key: str):
        """
        Initialize ZeroBounce API client.

        Args:
            api_key: Your ZeroBounce API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=3000, per_seconds=3600)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Accept": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"
        final_params = params or {}

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=final_params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"ZeroBounce API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during ZeroBounce API request: {str(e)}")

    # ==================== Email Validation ====================

    async def validate_email(
        self,
        email: str,
        ip_address: Optional[str] = None
    ) -> EmailValidationResult:
        """
        Validate a single email address.

        Args:
            email: Email address to validate
            ip_address: Optional IP address of the user

        Returns:
            EmailValidationResult with validation data

        Raises:
            Exception: If request fails
        """
        params = {
            "email": email,
            "api_key": self.api_key
        }

        if ip_address:
            params["ip_address"] = ip_address

        data = await self._request("GET", "/validate", params=params)

        return EmailValidationResult(
            address=data.get("address", email),
            status=data.get("status", ""),
            sub_status=data.get("sub_status"),
            free_email=data.get("free_email"),
            did_you_mean=data.get("did_you_mean"),
            account=data.get("account"),
            domain=data.get("domain"),
            safe_to_send=data.get("disposable") == "false" and data.get("catch_all") == "true",
            ip_address=data.get("ip_address"),
            location=data.get("location"),
            creation_date=data.get("creation_date")
        )

    async def bulk_validate(
        self,
        email_batch: List[str],
        ip_address: Optional[str] = None
    ) -> List[EmailValidationResult]:
        """
        Validate multiple email addresses in bulk.

        Args:
            email_batch: List of email addresses to validate
            ip_address: Optional IP address of the user

        Returns:
            List of EmailValidationResult

        Raises:
            Exception: If request fails
        """
        # Process emails individually (ZeroBounce has a separate bulk API)
        # This is a simplified implementation
        results = []

        for email in email_batch:
            try:
                result = await self.validate_email(email, ip_address)
                results.append(result)
            except Exception as e:
                # Add failed result
                results.append(EmailValidationResult(
                    address=email,
                    status="error",
                    sub_status=str(e)
                ))

        return results

    async def get_credits(self) -> Dict[str, Any]:
        """
        Get remaining API credits.

        Returns:
            Credits information

        Raises:
            Exception: If request fails
        """
        params = {"api_key": self.api_key}

        return await self._request("GET", "/getcredits", params=params)

    async def get_activity_data(
        self,
        email: str
    ) -> Dict[str, Any]:
        """
        Get activity data for an email address.

        Args:
            email: Email address to check

        Returns:
            Activity data including found, active dates

        Raises:
            Exception: If request fails
        """
        params = {
            "email": email,
            "api_key": self.api_key
        }

        return await self._request("GET", "/getactivitydata", params=params)