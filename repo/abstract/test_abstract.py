"""
Test suite for Abstract API client
Run with valid API keys to test all endpoints
"""

import asyncio
import os
from abstract_client import AbstractAPIClient


async def test_exchange_rates():
    """Test exchange rates APIs"""
    print("\n=== Testing Exchange Rates ===")

    api_key = os.getenv("ABSTRACT_EXCHANGE_RATES_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"exchange_rates": api_key})

    try:
        # Test 1: Live exchange rates
        print("1. Live Exchange Rates...")
        rates = await client.live_exchange_rates(base="USD")
        print(f"   Base currency: {rates.base}")
        print(f"   EUR rate: {rates.rates.get('EUR', 'N/A')}")
        print(f"   JPY rate: {rates.rates.get('JPY', 'N/A')}")
        assert isinstance(rates.rates, dict), "Rates should be a dictionary"
        print("   ✅ PASSED")

        # Test 2: Convert exchange rates
        print("2. Convert Exchange Rates (100 USD to EUR)...")
        converted = await client.convert_exchange_rates(100.0, "USD", "EUR")
        print(f"   {converted.original_amount} USD = {converted.converted_amount} EUR")
        print(f"   Rate: {converted.rate}")
        assert converted.converted_amount > 0, "Converted amount should be positive"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def test_phone_validation():
    """Test phone validation API"""
    print("\n=== Testing Phone Validation ===")

    api_key = os.getenv("ABSTRACT_PHONE_VALIDATION_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"phone_validation": api_key})

    try:
        print("1. Phone Number Validation (+14155552671)...")
        phone = await client.phone_number_validation("+14155552671", "US")
        print(f"   Phone: {phone.phone_number}")
        print(f"   Valid: {phone.is_valid}")
        print(f"   Type: {phone.type}")
        print(f"   Format: {phone.format}")
        print(f"   Carrier: {phone.carrier}")
        assert isinstance(phone.is_valid, bool), "is_valid should be boolean"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def test_timezone():
    """Test timezone APIs"""
    print("\n=== Testing Timezone APIs ===")

    api_key = os.getenv("ABSTRACT_TIMEZONE_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"timezone": api_key})

    try:
        # Test 1: Get current time
        print("1. Get Current Time (Tokyo)...")
        time_info = await client.get_current_time("Tokyo")
        print(f"   DateTime: {time_info.date_time}")
        print(f"   Timezone: {time_info.timezone}")
        print(f"   UTC Offset: {time_info.utc_offset}")
        assert time_info.date_time, "DateTime should not be empty"
        print("   ✅ PASSED")

        # Test 2: Convert time
        print("2. Convert Time (New York -> Tokyo)...")
        converted = await client.convert_time(
            "New York",
            "2024-02-27T12:00:00",
            "Tokyo"
        )
        print(f"   Converted time: {converted.date_time}")
        print(f"   Target timezone: {converted.timezone}")
        assert converted.date_time, "Converted time should not be empty"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def test_ip_geolocation():
    """Test IP geolocation API"""
    print("\n=== Testing IP Geolocation ===")

    api_key = os.getenv("ABSTRACT_IP_GEOLOCATION_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"ip_geolocation": api_key})

    try:
        print("1. IP Geolocation (8.8.8.8)...")
        geo = await client.ip_geolocation("8.8.8.8")
        print(f"   IP: {geo.ip_address}")
        print(f"   City: {geo.city}")
        print(f"   Country: {geo.country}")
        print(f"   Coordinates: ({geo.latitude}, {geo.longitude})")
        print(f"   Timezone: {geo.timezone}")
        assert isinstance(geo.latitude, (int, float)), "Latitude should be numeric"
        assert isinstance(geo.longitude, (int, float)), "Longitude should be numeric"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def test_email_validation():
    """Test email validation API"""
    print("\n=== Testing Email Validation ===")

    api_key = os.getenv("ABSTRACT_EMAIL_VALIDATION_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"email_validation": api_key})

    try:
        print("1. Email Validation (test@example.com)...")
        email = await client.email_validation("test@example.com")
        print(f"   Email: {email.email}")
        print(f"   Valid: {email.is_valid}")
        print(f"   Deliverable: {email.is_deliverable}")
        print(f"   Disposable: {email.is_disposable}")
        print(f"   Quality Score: {email.quality_score}")
        assert isinstance(email.is_valid, bool), "is_valid should be boolean"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def test_holidays():
    """Test holidays API"""
    print("\n=== Testing Holidays API ===")

    api_key = os.getenv("ABSTRACT_HOLIDAYS_KEY", "test_key")

    client = AbstractAPIClient(api_keys={"holidays": api_key})

    try:
        print("1. Get Country Holidays (US, 2024)...")
        holidays = await client.get_country_holidays("US", 2024)
        print(f"   Total holidays: {len(holidays)}")
        print("   First 3 holidays:")
        for h in holidays[:3]:
            print(f"     - {h.holiday_name}: {h.date} ({h.type})")
        assert isinstance(holidays, list), "Holidays should be a list"
        print("   ✅ PASSED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Abstract API Test Suite")
    print("=" * 60)
    print("\nNote: Set API keys as environment variables to test")
    print("Example:")
    print("  export ABSTRACT_EXCHANGE_RATES_KEY='your_key'")
    print("  export ABSTRACT_PHONE_VALIDATION_KEY='your_key'")
    print("  ... etc")
    print("")

    await test_exchange_rates()
    await test_phone_validation()
    await test_timezone()
    await test_ip_geolocation()
    await test_email_validation()
    await test_holidays()

    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())