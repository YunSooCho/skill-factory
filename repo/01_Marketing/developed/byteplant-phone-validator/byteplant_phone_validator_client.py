"""
Byteplant Phone Validator API Client

Supports:
- Verify Phone Number
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class PhoneValidationResult:
    """Phone number validation response"""
    phone_number: str
    is_valid: bool
    status: str
    country_code: Optional[str]
    location: Optional[str]
    carrier: Optional[str]
    line_type: Optional[str]
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class ByteplantPhoneValidatorClient:
    """
    Byteplant Phone Validator client for phone number validation.

    API Documentation: https://www.byteplant.com/phone-number-validation-api
    This service validates phone numbers globally and provides detailed information.
    """

    BASE_URL = "https://api-1.phone-validator-v4.byteplant.com/api/v1/validate"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Byteplant Phone Validator client.

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

    async def verify_phone_number(
        self,
        phone_number: str,
        country_code: str = "US",
        mode: str = "extensive"
    ) -> PhoneValidationResult:
        """
        Verify a phone number.

        Args:
            phone_number: Phone number to verify (with or without country code)
            country_code: ISO 3166-1 alpha-2 country code (default: "US")
            mode: Validation mode - 'express' or 'extensive' (default: "extensive")

        Returns:
            PhoneValidationResult: Validation result with detailed information

        Raises:
            ValueError: If phone_number is empty or invalid
            aiohttp.ClientError: If API request fails
        """
        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number is required")

        params = {
            "apikey": self.api_key,
            "PhoneNumber": phone_number.strip(),
            "CountryCode": country_code.upper(),
            "Mode": mode
        }

        headers = {
            "User-Agent": "ByteplantPhoneValidatorClient/1.0",
            "Accept": "application/json"
        }

        try:
            async with self.session.get(
                self.BASE_URL,
                params=params,
                headers=headers
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_response(data)

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

    def _parse_response(self, data: Dict[str, Any]) -> PhoneValidationResult:
        """
        Parse API response into PhoneValidationResult.

        Args:
            data: Raw API response

        Returns:
            PhoneValidationResult: Parsed validation result
        """
        # Handle different response formats
        status = data.get("status", "unknown")
        is_valid = status.lower() in ["valid", "ok"]

        return PhoneValidationResult(
            phone_number=data.get("phoneNumber", data.get("number", "")),
            is_valid=is_valid,
            status=status,
            country_code=data.get("countryCode"),
            location=data.get("location", data.get("city")),
            carrier=data.get("carrier", data.get("provider")),
            line_type=data.get("lineType", data.get("type")),
            error_message=data.get("error", data.get("errorMessage")),
            raw_response=data
        )

    async def verify_bulk_phone_numbers(
        self,
        phone_numbers: list[str],
        country_code: str = "US"
    ) -> list[PhoneValidationResult]:
        """
        Validate multiple phone numbers in parallel.

        Args:
            phone_numbers: List of phone numbers to validate
            country_code: Default country code for numbers without one

        Returns:
            List[PhoneValidationResult]: Validation results for all numbers
        """
        if not phone_numbers:
            return []

        tasks = [
            self.verify_phone_number(phone, country_code)
            for phone in phone_numbers
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions in bulk results
        validated_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Create error result
                validated_results.append(PhoneValidationResult(
                    phone_number=phone_numbers[i],
                    is_valid=False,
                    status="error",
                    error_message=str(result)
                ))
            else:
                validated_results.append(result)

        return validated_results


# Convenience function for one-shot validation
async def validate_phone(
    api_key: str,
    phone_number: str,
    country_code: str = "US"
) -> PhoneValidationResult:
    """
    Convenience function for single phone validation.

    Args:
        api_key: API key for authentication
        phone_number: Phone number to validate
        country_code: Country code (default: "US")

    Returns:
        PhoneValidationResult: Validation result
    """
    async with ByteplantPhoneValidatorClient(api_key=api_key) as client:
        return await client.verify_phone_number(phone_number, country_code)