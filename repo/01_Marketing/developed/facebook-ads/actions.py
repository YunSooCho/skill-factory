"""
Facebook Ads (Meta Marketing API) Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .models import (
    AdAccount,
    Campaign,
    AdSet,
    Ad,
    AdInsight,
)
from .exceptions import (
    FacebookAdsError,
    FacebookAdsAuthenticationError,
    FacebookAdsRateLimitError,
    FacebookAdsNotFoundError,
    FacebookAdsValidationError,
)


class FacebookAdsActions:
    """Facebook Ads API actions for Yoom integration."""

    BASE_URL = "https://graph.facebook.com"
    API_VERSION = "v19.0"

    def __init__(self, access_token: str, app_id: str, app_secret: str, timeout: int = 30):
        """
        Initialize Facebook Ads API client.

        Args:
            access_token: OAuth access token
            app_id: Facebook App ID
            app_secret: Facebook App Secret
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting state
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms between requests
        self.rate_limit_remaining = 200

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Facebook Graph API with rate limiting.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data (for POST requests)
            retry_on_rate_limit: Whether to retry on 429 errors

        Returns:
            Response JSON as dict

        Raises:
            FacebookAdsError: For API errors
            FacebookAdsAuthenticationError: For auth errors
            FacebookAdsRateLimitError: For rate limit errors
            FacebookAdsNotFoundError: For 404 errors
        """
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        url = f"{self.BASE_URL}/{self.API_VERSION}{endpoint}"

        # Ensure access token is in params
        if params is None:
            params = {}
        params["access_token"] = self.access_token

        try:
            if data:
                response = self.session.post(url, params=params, data=data, timeout=self.timeout)
            else:
                response = self.session.get(url, params=params, timeout=self.timeout)

            self.last_request_time = time.time()

            # Update rate limit info from headers
            if "X-Business-Use-Case-Usage" in response.headers:
                self.rate_limit_remaining = min(
                    self.rate_limit_remaining,
                    int(response.headers.get("X-Ad-Account-Usage", "200").split(":")[0]),
                )

            # Handle error responses
            response_data = response.json() if response.text else {}

            if response.status_code == 401:
                raise FacebookAdsAuthenticationError(
                    message=response_data.get("error", {}).get(
                        "message", "Authentication failed"
                    ),
                    status_code=401,
                    response=response_data.get("error"),
                )
            elif response.status_code == 404:
                raise FacebookAdsNotFoundError(
                    message="Resource not found",
                    status_code=404,
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(
                        endpoint, params, data, retry_on_rate_limit=False
                    )
                raise FacebookAdsRateLimitError(
                    message=response_data.get("error", {}).get(
                        "message", "Rate limit exceeded"
                    ),
                    status_code=429,
                )
            elif response.status_code >= 400:
                error_msg = (
                    response_data.get("error", {})
                    .get("message", f"API Error: {response.status_code}")
                    .replace('"', "'")
                )
                raise FacebookAdsError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response_data.get("error"),
                )

            return response_data

        except requests.Timeout:
            raise FacebookAdsError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise FacebookAdsError(f"Request failed: {str(e)}")

    def _get_insights(
        self,
        object_type: str,
        object_ids: Optional[List[str]] = None,
        account_id: Optional[str] = None,
        date_start: str = None,
        date_end: str = None,
        fields: Optional[List[str]] = None,
    ) -> List[AdInsight]:
        """
        Generic method to get insights for various object types.

        Args:
            object_type: Type of object (account, campaign, adset, ad)
            object_ids: List of object IDs (optional, uses account_id if not provided)
            account_id: Account ID (used if object_ids not provided)
            date_start: Start date (ISO 8601 format)
            date_end: End date (ISO 8601 format)
            fields: List of fields to retrieve

        Returns:
            List of AdInsight objects
        """
        if not date_start or not date_end:
            raise FacebookAdsValidationError("date_start and date_end are required")

        # Default fields for insights
        if fields is None:
            fields = [
                "campaign_id",
                "campaign_name",
                "adset_id",
                "adset_name",
                "ad_id",
                "ad_name",
                "impressions",
                "clicks",
                "spend",
                "cpc",
                "ctr",
                "cpm",
                "reach",
                "conversions",
                "cost_per_conversion",
                "date_start",
                "date_stop",
            ]

        params = {
            "fields": ",".join(fields),
            "date_preset": "lifetime",
            "time_range": f'{{"since":"{date_start}","until":"{date_end}"}}',
            "level": object_type,
        }

        if object_ids:
            params["ids"] = ",".join(object_ids)
        elif account_id:
            endpoint = f"/{account_id}/insights"
            response = self._make_request(endpoint, params=params)
        else:
            raise FacebookAdsValidationError(
                "Either object_ids or account_id must be provided"
            )

        endpoint = f"/insights"
        response = self._make_request(endpoint, params=params)

        insights = []
        if "data" in response:
            insights_data = response["data"]
            if not object_ids and not account_id:
                # Single object result
                if "data" in insights_data:
                    for item in insights_data["data"]:
                        insights.append(AdInsight.from_dict(item))
            else:
                # Multiple objects result
                for item in insights_data:
                    insights.append(AdInsight.from_dict(item))

        return insights

    # ==================== API Actions ====================

    def create_account_report(
        self,
        account_id: str,
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Create and retrieve account-level report.

        Args:
            account_id: Facebook Ad Account ID (act_xxxxxxxxx)
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the account

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not account_id:
            raise FacebookAdsValidationError("account_id is required")

        return self._get_insights(
            object_type="account",
            account_id=account_id,
            date_start=date_start,
            date_end=date_end,
        )

    def get_adset_report(
        self,
        adset_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Get ad set level reports.

        Args:
            adset_ids: List of Ad Set IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the ad sets

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not adset_ids:
            raise FacebookAdsValidationError("adset_ids is required")

        return self._get_insights(
            object_type="adset",
            object_ids=adset_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def get_account_report(
        self,
        account_id: str,
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Get account level reports.

        Args:
            account_id: Facebook Ad Account ID (act_xxxxxxxxx)
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the account

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not account_id:
            raise FacebookAdsValidationError("account_id is required")

        return self._get_insights(
            object_type="account",
            account_id=account_id,
            date_start=date_start,
            date_end=date_end,
        )

    def get_ad_report(
        self,
        ad_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Get ad level reports.

        Args:
            ad_ids: List of Ad IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the ads

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not ad_ids:
            raise FacebookAdsValidationError("ad_ids is required")

        return self._get_insights(
            object_type="ad",
            object_ids=ad_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def create_campaign_report(
        self,
        campaign_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Create and retrieve campaign-level reports.

        Args:
            campaign_ids: List of Campaign IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the campaigns

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not campaign_ids:
            raise FacebookAdsValidationError("campaign_ids is required")

        return self._get_insights(
            object_type="campaign",
            object_ids=campaign_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def get_campaign_report(
        self,
        campaign_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Get campaign level reports.

        Args:
            campaign_ids: List of Campaign IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the campaigns

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not campaign_ids:
            raise FacebookAdsValidationError("campaign_ids is required")

        return self._get_insights(
            object_type="campaign",
            object_ids=campaign_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def create_ad_report(
        self,
        ad_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Create and retrieve ad-level reports.

        Args:
            ad_ids: List of Ad IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the ads

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not ad_ids:
            raise FacebookAdsValidationError("ad_ids is required")

        return self._get_insights(
            object_type="ad",
            object_ids=ad_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def create_adset_report(
        self,
        adset_ids: List[str],
        date_start: str,
        date_end: str,
    ) -> List[AdInsight]:
        """
        Create and retrieve ad set-level reports.

        Args:
            adset_ids: List of Ad Set IDs
            date_start: Report start date (YYYY-MM-DD)
            date_end: Report end date (YYYY-MM-DD)

        Returns:
            List of AdInsight objects for the ad sets

        Raises:
            FacebookAdsValidationError: If required fields missing
            FacebookAdsError: For API errors
        """
        if not adset_ids:
            raise FacebookAdsValidationError("adset_ids is required")

        return self._get_insights(
            object_type="adset",
            object_ids=adset_ids,
            date_start=date_start,
            date_end=date_end,
        )

    def close(self):
        """Close the session."""
        self.session.close()