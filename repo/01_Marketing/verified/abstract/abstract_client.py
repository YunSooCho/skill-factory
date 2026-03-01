"""
Abstract API - Utility API Client

Supports:
- Live Exchange Rates
- Convert Exchange Rates
- Phone Number Validation
- Get Current Time
- Convert Time
- IP Geolocation Information
- Email Validation
- Country Holidays
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExchangeRateResponse:
    """Exchange rate response"""
    base: str
    date: str
    rates: Dict[str, float]
    last_updated: str


@dataclass
class ConvertedAmount:
    """Converted amount response"""
    original_amount: float
    original_currency: str
    target_currency: str
    converted_amount: float
    rate: float
    date: str


@dataclass
class PhoneValidation:
    """Phone number validation response"""
    phone_number: str
    is_valid: bool
    type: str
    format: str
    country_code: str
    country_name: str
    location: str
    carrier: str
    line_type: str


@dataclass
class TimeInfo:
    """Time information response"""
    date_time: str
    timezone: str
    timezone_name: str
    utc_offset: str
    day_of_year: int
    day_of_week: int
    week_number: int


@dataclass
class IPGeolocation:
    """IP geolocation response"""
    ip_address: str
    city: str
    region: str
    country: str
    country_code: str
    continent: str
    latitude: float
    longitude: float
    timezone: str
    flag: str


@dataclass
class EmailValidation:
    """Email validation response"""
    email: str
    is_valid: bool
    is_deliverable: bool
    is_disposable: bool
    is_free: str
    quality_score: float
    score: float


@dataclass
class CountryHoliday:
    """Country holiday response"""
    holiday_name: str
    date: str
    observed_on: str
    type: str
    nation_wide: bool


class AbstractAPIClient:
    """
    Abstract API client for utility services.

    API Documentation: https://app.abstractapi.com/api
    Each endpoint requires a specific API key from the Abstract API dashboard.
    """

    BASE_URL = "https://api.abstractapi.com/v1"

    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize Abstract API client.

        Args:
            api_keys: Dictionary of API keys for each service.
                      Required keys: 'exchange_rates', 'phone_validation',
                                  'timezone', 'ip_geolocation', 'email_validation',
                                  'holidays'
        """
        self.api_keys = api_keys or {}
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_key(self, service: str) -> str:
        """Get API key for specific service"""
        if service not in self.api_keys:
            raise ValueError(f"API key for '{service}' not provided")
        return self.api_keys[service]

    # ==================== Exchange Rates ====================

    async def live_exchange_rates(self, base: str = "USD") -> ExchangeRateResponse:
        """
        Get live exchange rates.

        Args:
            base: Base currency code (default: USD)

        Returns:
            ExchangeRateResponse with current rates

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("exchange_rates"),
            "base": base
        }

        async with self.session.get(
            f"{self.BASE_URL}/exchange-rates",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Exchange rates API error: {data}")

            return ExchangeRateResponse(
                base=data.get("base", base),
                date=data.get("date", ""),
                rates=data.get("exchange_rates", {}),
                last_updated=data.get("last_updated", "")
            )

    async def convert_exchange_rates(
        self,
        amount: float,
        base: str,
        target: str
    ) -> ConvertedAmount:
        """
        Convert amount between currencies.

        Args:
            amount: Amount to convert
            base: Source currency code
            target: Target currency code

        Returns:
            ConvertedAmount with conversion result

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("exchange_rates"),
            "base": base,
            "target": target
        }

        async with self.session.get(
            f"{self.BASE_URL}/exchange-rates/convert",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Exchange conversion error: {data}")

            converted_amount = data.get("converted_amount", amount)

            # Calculate rate
            rate = converted_amount / amount if amount > 0 else 1.0

            return ConvertedAmount(
                original_amount=amount,
                original_currency=base,
                target_currency=target,
                converted_amount=converted_amount,
                rate=rate,
                date=data.get("date", "")
            )

    # ==================== Phone Validation ====================

    async def phone_number_validation(self, phone: str, country: Optional[str] = None) -> PhoneValidation:
        """
        Validate a phone number.

        Args:
            phone: Phone number to validate
            country: Optional country code for better validation (e.g., "US")

        Returns:
            PhoneValidation with validation result

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("phone_validation"),
            "phone_number": phone
        }

        if country:
            params["country"] = country

        async with self.session.get(
            f"{self.BASE_URL}/phone_number_validation",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Phone validation error: {data}")

            return PhoneValidation(
                phone_number=data.get("phone_number", phone),
                is_valid=data.get("is_valid_number", False),
                type=data.get("type", ""),
                format=data.get("format", {}).get("international", ""),
                country_code=data.get("country", {}).get("code", ""),
                country_name=data.get("country", {}).get("name", ""),
                location=data.get("location", ""),
                carrier=data.get("carrier", ""),
                line_type=data.get("line_type", "")
            )

    # ==================== Time Services ====================

    async def get_current_time(self, location: str) -> TimeInfo:
        """
        Get current time for a specific location.

        Args:
            location: City name or timezone (e.g., "New York", "Asia/Tokyo")

        Returns:
            TimeInfo with current time details

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("timezone"),
            "location": location
        }

        async with self.session.get(
            f"{self.BASE_URL}/timezone/current_time",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Time API error: {data}")

            return TimeInfo(
                date_time=data.get("datetime", ""),
                timezone=data.get("timezone_id", ""),
                timezone_name=data.get("timezone_name", ""),
                utc_offset=data.get("gmt_offset", ""),
                day_of_year=data.get("day_of_year", 0),
                day_of_week=data.get("day_of_week", 0),
                week_number=data.get("week_of_year", 0)
            )

    async def convert_time(
        self,
        base_location: str,
        base_date: str,
        target_location: str
    ) -> TimeInfo:
        """
        Convert time from one timezone to another.

        Args:
            base_location: Source location name or timezone
            base_date: Source datetime (ISO 8601 format)
            target_location: Target location name or timezone

        Returns:
            TimeInfo with converted time details

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("timezone"),
            "base_location": base_location,
            "base_date": base_date,
            "target_location": target_location
        }

        async with self.session.get(
            f"{self.BASE_URL}/timezone/convert_time",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Time conversion error: {data}")

            return TimeInfo(
                date_time=data.get("target_datetime", ""),
                timezone=data.get("target_timezone_id", ""),
                timezone_name=data.get("target_timezone_name", ""),
                utc_offset=data.get("target_gmt_offset", ""),
                day_of_year=data.get("target_day_of_year", 0),
                day_of_week=data.get("target_day_of_week", 0),
                week_number=data.get("target_week_of_year", 0)
            )

    # ==================== IP Geolocation ====================

    async def ip_geolocation(self, ip_address: Optional[str] = None) -> IPGeolocation:
        """
        Get geolocation information for an IP address.

        Args:
            ip_address: IP address to lookup. If None, uses caller's IP

        Returns:
            IPGeolocation with location details

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("ip_geolocation")
        }

        if ip_address:
            params["ip_address"] = ip_address

        async with self.session.get(
            f"{self.BASE_URL}/ip_geolocation",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"IP geolocation error: {data}")

            return IPGeolocation(
                ip_address=data.get("ip_address", ip_address or ""),
                city=data.get("city", ""),
                region=data.get("region", ""),
                country=data.get("country", ""),
                country_code=data.get("country_code", ""),
                continent=data.get("continent", ""),
                latitude=data.get("latitude", 0.0),
                longitude=data.get("longitude", 0.0),
                timezone=data.get("timezone", {}).get("name", ""),
                flag=data.get("flag", "")
            )

    # ==================== Email Validation ====================

    async def email_validation(self, email: str) -> EmailValidation:
        """
        Validate an email address.

        Args:
            email: Email address to validate

        Returns:
            EmailValidation with validation result

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        params = {
            "api_key": self._get_key("email_validation"),
            "email": email
        }

        async with self.session.get(
            f"{self.BASE_URL}/email_validation",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Email validation error: {data}")

            return EmailValidation(
                email=data.get("email", email),
                is_valid=data.get("is_valid", {}).get("value", False),
                is_deliverable=data.get("deliverability", {}).get("value", ""),
                is_disposable=data.get("disposable", {}).get("value", ""),
                is_free=data.get("is_free_email", {}).get("value", ""),
                quality_score=data.get("quality_score", 0.0),
                score=data.get("quality_score", 0.0)
            )

    # ==================== Country Holidays ====================

    async def get_country_holidays(
        self,
        country: str,
        year: Optional[int] = None
    ) -> list[CountryHoliday]:
        """
        Get holidays for a specific country.

        Args:
            country: ISO country code (e.g., "US", "JP", "GB")
            year: Year to get holidays for (default: current year)

        Returns:
            List of CountryHoliday objects

        Raises:
            ValueError: If API key is not configured
            aiohttp.ClientError: If request fails
        """
        if year is None:
            year = datetime.now(timezone.utc).year

        params = {
            "api_key": self._get_key("holidays"),
            "country": country,
            "year": year
        }

        async with self.session.get(
            f"{self.BASE_URL}/holidays",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Holidays API error: {data}")

            holidays = data.get("holidays", [])
            return [
                CountryHoliday(
                    holiday_name=h.get("name", ""),
                    date=h.get("date_iso", ""),
                    observed_on=h.get("observed_date_iso", ""),
                    type=h.get("type", ""),
                    nation_wide=h.get("nation_wide", False)
                )
                for h in holidays
            ]


# ==================== Example Usage ====================

async def main():
    """Example usage of Abstract API client"""

    # Example configuration - replace with your actual API keys
    api_keys = {
        "exchange_rates": "your_exchange_rates_api_key",
        "phone_validation": "your_phone_validation_api_key",
        "timezone": "your_timezone_api_key",
        "ip_geolocation": "your_ip_geolocation_api_key",
        "email_validation": "your_email_validation_api_key",
        "holidays": "your_holidays_api_key"
    }

    async with AbstractAPIClient(api_keys=api_keys) as client:
        # Live exchange rates
        rates = await client.live_exchange_rates(base="USD")
        print(f"USD base rates: {rates.rates}")

        # Convert currency
        converted = await client.convert_exchange_rates(100.0, "USD", "EUR")
        print(f"100 USD = {converted.converted_amount} EUR")

        # Phone validation
        phone = await client.phone_number_validation("+14155552671", "US")
        print(f"Phone valid: {phone.is_valid}, Type: {phone.type}")

        # Current time
        time_info = await client.get_current_time("Tokyo")
        print(f"Tokyo time: {time_info.date_time}")

        # Convert time
        converted_time = await client.convert_time(
            "New York",
            "2024-02-27T12:00:00",
            "Tokyo"
        )
        print(f"Converted time: {converted_time.date_time}")

        # IP geolocation
        geo = await client.ip_geolocation("8.8.8.8")
        print(f"IP location: {geo.city}, {geo.country}")

        # Email validation
        email = await client.email_validation("test@example.com")
        print(f"Email valid: {email.is_valid}")

        # Country holidays
        holidays = await client.get_country_holidays("US", 2024)
        print(f"Found {len(holidays)} holidays")
        for h in holidays[:3]:  # Show first 3
            print(f"  - {h.holiday_name}: {h.date}")


if __name__ == "__main__":
    asyncio.run(main())