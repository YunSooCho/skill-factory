"""
 Email List Verify API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any, Union
from urllib.parse import urljoin

from .models import (
    VerificationResult,
    DeliverabilityResult,
    BusinessEmailResult,
    DisposableEmailCheck,
    EmailStatus,
)
from .exceptions import (
    EmailListVerifyError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class EmailListVerifyClient:
    """Email List Verify API Client"""

    BASE_URL = "https://api.emaillistverify.com/"
    API_VERSION = "v1"

    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
    ):
        """
        Initialize Email List Verify client

        Args:
            api_key: Email List Verify API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 100ms between requests
        self._rate_limit_remaining = 1000
        self._rate_limit_reset = time.time() + 3600

    def _wait_for_rate_limit(self):
        """Apply rate limiting to requests"""
        now = time.time()
        time_since_last = now - self._last_request_time

        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Union[Dict, List]:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data

        Returns:
            JSON response data

        Raises:
            EmailListVerifyError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        url = urljoin(self.BASE_URL, endpoint)

        # API key in query params
        if params is None:
            params = {}
        params["apikey"] = self.api_key

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json_data,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise EmailListVerifyError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise EmailListVerifyError(f"Request failed: {str(e)}")

    def _update_rate_limit(self, headers: Dict):
        """Update rate limit information from response headers"""
        if "X-RateLimit-Remaining" in headers:
            self._rate_limit_remaining = int(headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in headers:
            self._rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            EmailListVerifyError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        try:
            response_text = response.text
            if response_text:
                data = response.json()
            else:
                data = {}
        except ValueError:
            return {"raw": response_text}

        # Handle error responses
        if isinstance(data, dict):
            success = data.get("success", data.get("Success"))
            if success is False:
                error_msg = data.get("error", data.get("message", "Unknown error"))
                raise EmailListVerifyError(error_msg, response=data)

        if response.status_code >= 200 and response.status_code < 300:
            return data
        elif response.status_code == 400:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 401:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 403:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 404:
            error_message = self._extract_error_message(data)
            raise ResourceNotFoundError(error_message, response=data)
        elif response.status_code == 422:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = self._extract_error_message(data)
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = self._extract_error_message(data)
            raise EmailListVerifyError(
                error_message or f"HTTP {response.status_code}",
                status_code=response.status_code,
                response=data,
            )

    def _extract_error_message(self, data: Union[Dict, List]) -> str:
        """Extract error message from response data"""
        if isinstance(data, dict):
            return (
                data.get("message")
                or data.get("error")
                or data.get("error_message")
                or data.get("errorMessage")
                or str(data)
            )
        return str(data)

    # ==================== EMAIL VERIFICATION ====================

    def verify_email(
        self,
        email: str,
        timeout: Optional[int] = None,
        check_dns: bool = True,
        check_smtp: bool = True,
    ) -> VerificationResult:
        """
        Verify an email address

        Args:
            email: Email address to verify
            timeout: Override default timeout (optional)
            check_dns: Whether to check DNS records
            check_smtp: Whether to check SMTP server

        Returns:
            VerificationResult with verification details

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If email is invalid
        """
        if not email or "@" not in email:
            raise ValidationError("Invalid email address")

        params = {"email": email}
        if check_dns is not None:
            params["check_dns"] = str(check_dns).lower()
        if check_smtp is not None:
            params["check_smtp"] = str(check_smtp).lower()

        request_timeout = timeout or self.timeout
        response = self._make_request("GET", "api/verifyEmail", params=params)
        return VerificationResult.from_api_response(response)

    def batch_verify_emails(
        self,
        emails: List[str],
        check_dns: bool = True,
        check_smtp: bool = True,
    ) -> List[VerificationResult]:
        """
        Verify multiple email addresses in batch

        Args:
            emails: List of email addresses to verify
            check_dns: Whether to check DNS records
            check_smtp: Whether to check SMTP server

        Returns:
            List of VerificationResult objects

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If validation fails
        """
        if not emails:
            raise ValidationError("Emails list cannot be empty")

        if len(emails) > 100:
            raise ValidationError("Cannot verify more than 100 emails in a single batch")

        data = {"emails": emails}
        if check_dns is not None:
            data["check_dns"] = check_dns
        if check_smtp is not None:
            data["check_smtp"] = check_smtp

        response = self._make_request("POST", "api/batchVerify", json_data=data)

        results = []
        if isinstance(response, list):
            results = [VerificationResult.from_api_response(item) for item in response]
        elif isinstance(response, dict):
            if "results" in response:
                results = [
                    VerificationResult.from_api_response(item)
                    for item in response["results"]
                ]
            elif "data" in response:
                results = [
                    VerificationResult.from_api_response(item)
                    for item in response["data"]
                ]
            else:
                # Single result wrapped in dict
                results = [VerificationResult.from_api_response(response)]

        return results

    # ==================== DELIVERABILITY EVALUATION ====================

    def evaluate_deliverability(
        self,
        email: str,
        include_provider_info: bool = True,
        include_inbox_prediction: bool = True,
    ) -> DeliverabilityResult:
        """
        Evaluate email deliverability

        Args:
            email: Email address to evaluate
            include_provider_info: Include email provider info
            include_inbox_prediction: Include inbox rate prediction

        Returns:
            DeliverabilityResult with deliverability details

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If email is invalid
        """
        if not email or "@" not in email:
            raise ValidationError("Invalid email address")

        params = {
            "email": email,
        }
        if include_provider_info is not None:
            params["include_provider"] = str(include_provider_info).lower()
        if include_inbox_prediction is not None:
            params["include_inbox"] = str(include_inbox_prediction).lower()

        response = self._make_request("GET", "api/evaluateDeliverability", params=params)
        return DeliverabilityResult.from_api_response(response)

    # ==================== BUSINESS EMAIL SEARCH ====================

    def find_business_email(
        self,
        domain: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        full_name: Optional[str] = None,
        company_name: Optional[str] = None,
    ) -> BusinessEmailResult:
        """
        Find business email address for a domain/person

        Args:
            domain: Company domain (e.g., "google.com")
            first_name: First name of person
            last_name: Last name of person
            full_name: Full name (overrides first_name/last_name)
            company_name: Company name

        Returns:
            BusinessEmailResult with found email and details

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If domain is invalid
        """
        if not domain or "." not in domain:
            raise ValidationError("Invalid domain")

        params = {"domain": domain}
        if full_name:
            params["name"] = full_name
        else:
            if first_name:
                params["first_name"] = first_name
            if last_name:
                params["last_name"] = last_name
        if company_name:
            params["company"] = company_name

        response = self._make_request("GET", "api/findBusinessEmail", params=params)
        return BusinessEmailResult.from_api_response(response)

    def find_business_emails_batch(
        self,
        searches: List[Dict[str, Any]],
    ) -> List[BusinessEmailResult]:
        """
        Find business emails for multiple searches in batch

        Args:
            searches: List of search dictionaries with 'domain' and optional 'first_name', 'last_name', etc.

        Returns:
            List of BusinessEmailResult objects

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If validation fails
        """
        if not searches:
            raise ValidationError("Searches list cannot be empty")

        if len(searches) > 50:
            raise ValidationError("Cannot perform more than 50 searches in a single batch")

        data = {"searches": searches}
        response = self._make_request("POST", "api/batchFindBusinessEmail", json_data=data)

        results = []
        if isinstance(response, list):
            results = [BusinessEmailResult.from_api_response(item) for item in response]
        elif isinstance(response, dict):
            if "results" in response:
                results = [
                    BusinessEmailResult.from_api_response(item)
                    for item in response["results"]
                ]
            elif "data" in response:
                results = [
                    BusinessEmailResult.from_api_response(item)
                    for item in response["data"]
                ]
            else:
                results = [BusinessEmailResult.from_api_response(response)]

        return results

    # ==================== DISPOSABLE EMAIL CHECK ====================

    def check_disposable_email(self, email: str) -> DisposableEmailCheck:
        """
        Check if email address is from disposable/throwaway domain

        Args:
            email: Email address to check

        Returns:
            DisposableEmailCheck with disposable status and details

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If email is invalid
        """
        if not email or "@" not in email:
            raise ValidationError("Invalid email address")

        params = {"email": email}
        response = self._make_request("GET", "api/checkDisposable", params=params)
        return DisposableEmailCheck.from_api_response(response)

    def is_disposable_email(self, email: str) -> bool:
        """
        Quick check if email is from disposable domain

        Args:
            email: Email address to check

        Returns:
            True if email is from disposable domain, False otherwise

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If email is invalid
        """
        result = self.check_disposable_email(email)
        return result.is_disposable

    def check_disposable_domain(self, domain: str) -> bool:
        """
        Check if domain is a disposable email domain

        Args:
            domain: Domain to check (e.g., "tempmail.com")

        Returns:
            True if domain is disposable, False otherwise

        Raises:
            EmailListVerifyError: If the request fails
            ValidationError: If domain is invalid
        """
        if not domain:
            raise ValidationError("Domain is required")

        # Strip @ if provided
        domain = domain.lstrip("@")

        params = {"domain": domain}
        response = self._make_request("GET", "api/checkDisposable", params=params)

        # Handle both full response and simplified
        if isinstance(response, dict):
            return response.get("is_disposable", response.get("disposable", False))
        return False

    # ==================== HELPER METHODS ====================

    def get_api_status(self) -> Dict:
        """
        Get API status and account info

        Returns:
            API status data

        Raises:
            EmailListVerifyError: If the request fails
        """
        data = self._make_request("GET", "api/status", params={})
        return data

    def get_credit_balance(self) -> Dict:
        """
        Get remaining credit balance

        Returns:
            Credit balance data

        Raises:
            EmailListVerifyError: If the request fails
        """
        data = self._make_request("GET", "api/credits", params={})
        return data

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()