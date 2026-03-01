"""
IPQualityScore API Client
Email, Phone, IP Reputation Verification API
"""

import requests
from typing import Dict, Optional, Any
import time


class IPQualityScoreClient:
    """IPQualityScore API Client for fraud detection and data validation"""

    def __init__(self, api_key: str, base_url: str = "https://www.ipqualityscore.com/api/json"):
        """
        Initialize IPQualityScore client

        Args:
            api_key: IPQualityScore API key
            base_url: Base URL for API requests
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Invalid API key")
        elif response.status_code == 403:
            raise ValueError("Access forbidden")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def search_email(
        self,
        email: str,
        timeout: int = None,
        user_agent: str = None,
        public_access: str = None,
        days_since_last_activity: str = None
    ) -> Dict[str, Any]:
        """
        Verify email address and check for fraud indicators

        Args:
            email: Email address to verify
            timeout: Timeout in seconds (optional)
            user_agent: User agent string for advanced checks (optional)
            public_access: Check if email is publicly available (optional)
            days_since_last_activity: Check activity within days (optional)

        Returns:
            Dict with email verification results including:
                - success: Boolean
                - email_address: Email address
                - deliverability: Deliverability status (deliverable, risky, undeliverable)
                - quality_score: Quality score (0-10)
                - is_disposable: Is disposable email (boolean)
                - is_free_provider: Is from free provider (boolean)
                - fraud_score: Fraud score (0-100)
                - recent_abuse: Recent abuse detected (boolean)
                - valid: Is email syntactically valid (boolean)
                - spam_trap: Is spam trap (boolean)
        """
        url = f"{self.base_url}/email/{self.api_key}/{email}"

        params = {
            'timeout': timeout if timeout is not None else self.timeout
        }

        if user_agent is not None:
            params['ua'] = user_agent
        if public_access is not None:
            params['public'] = public_access
        if days_since_last_activity is not None:
            params['days'] = days_since_last_activity

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Email verification failed: {str(e)}")

    def search_phone_number(
        self,
        phone: str,
        country_code: str = None,
        user_agent: str = None,
        public_access: str = None,
        days_since_last_activity: str = None
    ) -> Dict[str, Any]:
        """
        Validate phone number and check for fraud indicators

        Args:
            phone: Phone number (can include country code or use country_code parameter)
            country_code: Country code (e.g., 'US', 'GB', 'KR')
            user_agent: User agent string for advanced checks (optional)
            public_access: Check if phone is publicly available (optional)
            days_since_last_activity: Check activity within days (optional)

        Returns:
            Dict with phone validation results including:
                - success: Boolean
                - phone_number: Formatted phone number
                - country_code: Country code
                - national_format: National format
                - international_format: International format
                - valid: Is phone number valid (boolean)
                - active: Is phone number active (boolean)
                - carrier: Carrier name
                - line_type: Line type (mobile, landline, voip)
                - fraud_score: Fraud score (0-100)
                - recent_abuse: Recent abuse detected (boolean)
                - prepaid: Is prepaid (boolean)
                - ported: Has been ported (boolean)
        """
        url = f"{self.base_url}/phone/{self.api_key}/{phone}"

        params = {}

        if country_code is not None:
            params['country_code'] = country_code
        if user_agent is not None:
            params['ua'] = user_agent
        if public_access is not None:
            params['public'] = public_access
        if days_since_last_activity is not None:
            params['days'] = days_since_last_activity

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Phone number validation failed: {str(e)}")

    def search_proxy_vpn(
        self,
        ip_address: str,
        strictness: int = None,
        user_agent: str = None,
        public_access: str = None,
        days_since_last_activity: str = None
    ) -> Dict[str, Any]:
        """
        Check IP address for proxy, VPN, Tor, and other fraud indicators

        Args:
            ip_address: IP address to check
            strictness: Strictness level (0-3, default 1)
            user_agent: User agent string for advanced checks (optional)
            public_access: Check if IP is publicly available (optional)
            days_since_last_activity: Check activity within days (optional)

        Returns:
            Dict with IP reputation results including:
                - success: Boolean
                - ip_address: IP address
                - fraud_score: Fraud score (0-100)
                - is_mobile: Is mobile IP (boolean)
                - is_vpn: Is VPN/proxy connection (boolean)
                - is_tor: Is Tor exit node (boolean)
                - is_datacenter: Is datacenter IP (boolean)
                - proxy: Is proxy connection (boolean)
                - vpn: Is VPN connection (boolean)
                - tor: Is Tor network (boolean)
                - active_vpn: Active VPN detection (boolean)
                - active_tor: Active Tor detection (boolean)
                - active_server: Active server/proxy (boolean)
                - recent_abuse: Recent abuse detected (boolean)
                - connection_type: Connection type
                - ISP: ISP name
                - ASN: ASN number
                - country_code: Country code
                - region: Region/State
                - city: City name
                - latitude: Latitude
                - longitude: Longitude
        """
        url = f"{self.base_url}/ip/{self.api_key}/{ip_address}"

        params = {}

        if strictness is not None:
            params['strictness'] = strictness
        if user_agent is not None:
            params['ua'] = user_agent
        if public_access is not None:
            params['public'] = public_access
        if days_since_last_activity is not None:
            params['days'] = days_since_last_activity

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"IP reputation check failed: {str(e)}")


# CLI Example
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage:")
        print("  Email verification: python ipqualityscore_client.py email <api_key> <email>")
        print("  Phone verification: python ipqualityscore_client.py phone <api_key> <phone> [country_code]")
        print("  IP reputation: python ipqualityscore_client.py ip <api_key> <ip_address>")
        sys.exit(1)

    api_key = sys.argv[2]

    client = IPQualityScoreClient(api_key)

    if sys.argv[1] == "email":
        email = sys.argv[3]
        result = client.search_email(email)
        print(f"Email: {email}")
        print(f"Valid: {result.get('valid')}")
        print(f"Deliverability: {result.get('deliverability')}")
        print(f"Quality Score: {result.get('quality_score')}/10")
        print(f"Fraud Score: {result.get('fraud_score')}/100")
        print(f"Disposable: {result.get('is_disposable')}")
        print(f"Spam Trap: {result.get('spam_trap')}")

    elif sys.argv[1] == "phone":
        phone = sys.argv[3]
        country_code = sys.argv[4] if len(sys.argv) > 4 else None
        result = client.search_phone_number(phone, country_code=country_code)
        print(f"Phone: {result.get('phone_number')}")
        print(f"Valid: {result.get('valid')}")
        print(f"Active: {result.get('active')}")
        print(f"Carrier: {result.get('carrier')}")
        print(f"Line Type: {result.get('line_type')}")
        print(f"Fraud Score: {result.get('fraud_score')}/100")
        print(f"Recent Abuse: {result.get('recent_abuse')}")

    elif sys.argv[1] == "ip":
        ip_address = sys.argv[3]
        result = client.search_proxy_vpn(ip_address)
        print(f"IP: {ip_address}")
        print(f"Fraud Score: {result.get('fraud_score')}/100")
        print(f"VPN: {result.get('is_vpn')}")
        print(f"Proxy: {result.get('proxy')}")
        print(f"Tor: {result.get('is_tor')}")
        print(f"Datacenter: {result.get('is_datacenter')}")
        print(f"Recent Abuse: {result.get('recent_abuse')}")
        print(f"Location: {result.get('city')}, {result.get('region')}, {result.get('country_code')}")