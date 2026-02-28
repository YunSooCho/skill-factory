"""
Gbiz-info API Client Test Suite
Run with: python test_gbiz_info.py

NOTE: This test requires valid corporate numbers.
"""

import os
from gbiz_info_client import GbizInfoClient, GbizInfoAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("GBIZ_API_KEY")

    # Known valid corporate number (株式会社資生堂)
    # This is a publicly available test company number
    VALID_CORPORATE_NUMBER = "8010001010880"

    client = GbizInfoClient(api_key=API_KEY)

    # Test 1: Search by Corporate Number
    print("\n[Test 1] Searching by corporate number...")
    try:
        response = client.search_by_corporate_number(VALID_CORPORATE_NUMBER)
        data = response.get('data', {})
        print(f"✓ Found company: {data.get('name')}")
        print(f"  Address: {data.get('prefectureName', '')}{data.get('cityName', '')}{data.get('streetNumber', '')}")
        print(f"  Status: {data.get('status')}")
    except GbizInfoAPIError as e:
        print(f"✗ Search failed: {e}")

    # Test 2: Get Detailed Information
    print("\n[Test 2] Getting detailed corporation info...")
    try:
        response = client.get_detailed_info(VALID_CORPORATE_NUMBER)
        data = response.get('data', {})
        print(f"✓ Retrieved detailed info for: {data.get('name')}")
        print(f"  Capital: {data.get('capitalStock')} JPY")
        print(f"  Established: {data.get('establishmentDate')}")
    except GbizInfoAPIError as e:
        print(f"✗ Get details failed: {e}")

    # Test 3: Search by Name
    print("\n[Test 3] Searching by company name...")
    try:
        response = client.search_by_name(
            name="株式会社",
            page=1,
            limit=5
        )
        data = response.get('data', {})
        print(f"✓ Found {len(data.get('hojinInfos', []))} results")
        if data.get('hojinInfos'):
            first_result = data['hojinInfos'][0]
            print(f"  First result: {first_result.get('name')}")
    except GbizInfoAPIError as e:
        print(f"✗ Search by name failed: {e}")

    # Test 4: Advanced Name Search
    print("\n[Test 4] Advanced name search with status filter...")
    try:
        response = client.search_by_name_advanced(
            name="株式会社",
            status="01",  # Active companies only
            exact_match=False,
            limit=10
        )
        data = response.get('data', {})
        print(f"✓ Found {len(data.get('hojinInfos', []))} active companies")
    except GbizInfoAPIError as e:
        print(f"✗ Advanced search failed: {e}")

    # Test 5: Get Corporation Status
    print("\n[Test 5] Getting corporation status...")
    try:
        status = client.get_corporation_status(VALID_CORPORATE_NUMBER)
        data = status.get('data', {})
        print(f"✓ Status: {data.get('status')}")
        print(f"  Company: {data.get('name')}")
        print(f"  Last Update: {data.get('update_date')}")
    except GbizInfoAPIError as e:
        print(f"✗ Get status failed: {e}")

    # Test 6: Invalid Corporate Number
    print("\n[Test 6] Testing invalid corporate number...")
    try:
        response = client.search_by_corporate_number("0000000000000")
        # Some APIs return empty results for invalid numbers
        data = response.get('data', {})
        if not data:
            print("✓ Correctly handled invalid number (empty result)")
        else:
            print("✗ Unexpected result for invalid number")
    except GbizInfoAPIError as e:
        print(f"✗ Error handling test: {e}")

    # Test 7: Search with Pagination
    print("\n[Test 7] Testing pagination...")
    try:
        response = client.search_by_name(
            name="株式会社",
            page=1,
            limit=10
        )
        data = response.get('data', {})
        print(f"✓ Retrieved page 1 with {data.get('hojinInfos', []) and len(data['hojinInfos']) or 0} results")
    except GbizInfoAPIError as e:
        print(f"✗ Pagination test failed: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Some tests may fail if Gbiz-info API has rate limits")
    print("or if the test corporate number has changed. Adjust as needed.")


if __name__ == "__main__":
    main()