"""
Abstract API Client
Documentation: https://docs.abstractapi.com/
"""

import logging
from typing import List, Optional, Dict, Any
import requests
from .models import (
    ExchangeRate, PhoneNumberValidation, TimeInfo,
    GeolocationInfo, EmailValidation, Holiday, CountryHolidays
)

logger = logging.getLogger(__name__)


class AbstractClient:
    """
    Abstract API Client for Yoom Integration

    API Actions:
    - Live Exchange Rates
    - Convert Exchange Rates
    - Phone Number Validation
    - Get Current Time
    - Convert Time
    - IP Geolocation Information
    - Email Validation
    - Country Holidays
    """

    BASE_URL = "https://api.abstractapi.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Abstract API Client

        Args:
            api_key: Abstract API key
        """
        self.api_key = api_key
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Abstract API

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        if params is None:
            params = {}

        params['api_key'] = self.api_key

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Abstract API Error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    # ========== EXCHANGE RATES ==========

    def live_exchange_rates(self, base: str) -> Dict[str, float]:
        """
        Get Live Exchange Rates

        Args:
            base: Base currency code (e.g., USD, EUR)

        Returns:
            Dictionary of currency codes to exchange rates
        """
        data = self._request('exchange', {'base': base})
        return data.get('exchange_rates', {})

    def convert_exchange_rates(
        self,
        base: str,
        target: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Convert Exchange Rates

        Args:
            base: Base currency code
            target: Target currency code
            amount: Amount to convert

        Returns:
            Dictionary with rate, last_updated, and converted_amount
        """
        params = {
            'base': base,
            'target': target,
            'amount': amount
        }
        data = self._request('convert', params)
        return {
            'base': data.get('base'),
            'target': data.get('target'),
            'rate': data.get('rate'),
            'last_updated': data.get('last_updated'),
            'converted_amount': data.get('converted_amount')
        }

    # ========== PHONE NUMBER VALIDATION ==========

    def validate_phone_number(self, phone: str, country: Optional[str] = None) -> PhoneNumberValidation:
        """
        Validate Phone Number

        Args:
            phone: Phone number (e.g., +14155552671)
            country: ISO 3166 country code (optional, helps with parsing)

        Returns:
            PhoneNumberValidation object
        """
        params = {'phone': phone}
        if country:
            params['country'] = country

        data = self._request('phone', params)
        return PhoneNumberValidation(
            phone_number=data.get('phone_number'),
            country_code=data.get('country_code'),
            national_format=data.get('national_format'),
            international_format=data.get('international_format'),
            country_name=data.get('country_name'),
            country_prefix=data.get('country_prefix'),
            line_type=data.get('line_type'),
            line_type_intelligence=data.get('line_type_intelligence'),
            location=data.get('location'),
            is_valid=data.get('is_valid', False),
            carrier=data.get('carrier')
        )

    # ========== TIME ==========

    def get_current_time(
        self,
        location: Optional[str] = None,
        timezone: Optional[str] = None
    ) -> TimeInfo:
        """
        Get Current Time

        Args:
            location: City name (e.g., 'New York')
            timezone: Timezone name (e.g., 'America/New_York')

        Returns:
            TimeInfo object
        """
        params = {}
        if location:
            params['location'] = location
        if timezone:
            params['timezone'] = timezone

        data = self._request('timezone', params)
        return TimeInfo(
            datetime=data.get('datetime'),
            timezone=data.get('timezone'),
            timezone_name=data.get('timezone_name'),
            utc_offset=data.get('utc_offset'),
            week_number=data.get('week_number'),
            day_of_year=data.get('day_of_year'),
            day_of_week=data.get('day_of_week')
        )

    def convert_time(
        self,
        base_location: str,
        base_datetime: str,
        target_location: str
    ) -> Dict[str, Any]:
        """
        Convert Time betweenzones

        Args:
            base_location: Base location (e.g., 'New York')
            base_datetime: Base datetime (e.g., '2024-01-15 14:30')
            target_location: Target location (e.g., 'Paris')

        Returns:
            Dictionary with converted datetime information
        """
        params = {
            'base_location': base_location,
            'base_datetime': base_datetime,
            'target_location': target_location
        }
        data = self._request('convert', params)
        return {
            'datetime': data.get('datetime'),
            'timezone': data.get('timezone'),
            'timezone_name': data.get('timezone_name'),
            'base_location': data.get('base_location'),
            'target_location': data.get('target_location')
        }

    # ========== IP GEOLOCATION ==========

    def get_geolocation(self, ip_address: str) -> GeolocationInfo:
        """
        Get IP Geolocation Information

        Args:
            ip_address: IP address (IPv4 or IPv6)

        Returns:
            GeolocationInfo object
        """
        data = self._request('ip', {'ip_address': ip_address})
        return GeolocationInfo(
            ip_address=data.get('ip_address'),
            city=data.get('city'),
            region=data.get('region'),
            region_iso_code=data.get('region_iso_code'),
            country=data.get('country'),
            country_code=data.get('country_code'),
            country_iso_code=data.get('country_iso_code'),
            continent=data.get('continent'),
            continent_code=data.get('continent_code'),
            postal_code=data.get('postal_code'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone'),
            flag=data.get('flag'),
            connection=data.get('connection'),
            security=data.get('security')
        )

    # ========== EMAIL VALIDATION ==========

    def validate_email(self, email: str) -> EmailValidation:
        """
        Validate Email Address

        Args:
            email: Email address to validate

        Returns:
            EmailValidation object
        """
        data = self._request('email', {'email': email})
        return EmailValidation(
            email=data.get('email'),
            is_valid=data.get('is_valid', False),
            is_deliverable=data.get('is_deliverable', False),
            is_free_email=data.get('is_free_email', False),
            is_mx_found=data.get('is_mx_found', False),
            is_smtp_valid=data.get('is_smtp_valid', False),
            quality_score=data.get('quality_score', 0.0),
            is_catchall=data.get('is_catchall'),
            is_role_email=data.get('is_role_email'),
            is_disposable=data.get('is_disposable'),
            is_system_email=data.get('is_system_email'),
            mx_records=data.get('mx_records'),
            smtp_provider=data.get('smtp_provider')
        )

    # ========== HOLIDAYS ==========

    def get_country_holidays(self, country: str, year: int) -> CountryHolidays:
        """
        Get Country Holidays

        Args:
            country: ISO 3166 country code (e.g., US, GB, JP)
            year: Year

        Returns:
            CountryHolidays object
        """
        data = self._request('holidays', {'country': country, 'year': year})
        holidays = [Holiday(**holiday) for holiday in data.get('holidays', [])]
        return CountryHolidays(
            country=data.get('country'),
            country_code=data.get('country_code'),
            year=data.get('year'),
            holidays=holidays
        )

    # ========== UTILITY ==========

    def test_connection(self) -> bool:
        """
        Test API connection

        Returns:
            True if connection successful
        """
        try:
            self.get_current_time(timezone='UTC')
            return True
        except Exception:
            return False